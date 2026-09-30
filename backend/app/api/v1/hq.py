from typing import Optional, List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.db.models.user import User, HQ_ROLES
from app.db.models.institute import Institute
from app.db.models.programme import Programme, Batch, AttendanceRecord, NationalTemplate, CertificateRevocationLog
from app.db.models.quiz import Certificate
from app.db.models.profile import MemberProfile
from app.db.models.placement import Placement
from app.db.models.audit import AuditLog
from app.schemas.response import success_response, error_response
from app.api.deps import get_current_user, require_hq_role, verify_institute_scope

router = APIRouter(prefix="/hq", tags=["NCCT HQ Governance"])

# Pydantic Schemas
class InstituteCreate(BaseModel):
    code: str
    name: str
    institute_type: str = "Regional Institute of Cooperative Management"
    region: str
    state: str
    city: str
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

class InstituteUpdate(BaseModel):
    name: Optional[str] = None
    institute_type: Optional[str] = None
    region: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: Optional[bool] = None

class ProgrammeApprovalUpdate(BaseModel):
    status: str # APPROVED, REJECTED, CHANGES_REQUESTED
    approval_comments: Optional[str] = None
    rejection_reason: Optional[str] = None

class RevokeCertificateRequest(BaseModel):
    reason: str

class NationalTemplateCreate(BaseModel):
    template_type: str # PROGRAMME, COURSE, CERTIFICATE, ATTENDANCE_POLICY, ASSESSMENT_POLICY, FEEDBACK
    title: str
    description: Optional[str] = None
    content_json: str

# 1. GET /api/v1/hq/dashboard
@router.get("/dashboard")
def get_hq_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    total_institutes = db.query(Institute).count()
    active_institutes = db.query(Institute).filter(Institute.is_active == True).count()
    total_programmes = db.query(Programme).count()
    programmes_completed = db.query(Programme).filter(Programme.status == "APPROVED").count()
    
    total_trainees = db.query(MemberProfile).count()
    trainees_completed = db.query(Certificate).count()
    certificates_issued = trainees_completed
    
    total_placements = db.query(Placement).count()
    
    pending_approvals = db.query(Programme).filter(Programme.status == "PENDING_APPROVAL").all()
    approval_queue = [
        {
            "id": p.id,
            "title": p.title,
            "code": p.code,
            "institute_id": p.institute_id,
            "category": p.category,
            "submitted_at": p.submitted_at.isoformat() if p.submitted_at else None,
            "status": p.status
        }
        for p in pending_approvals
    ]

    institutes = db.query(Institute).all()
    comparison_chart = []
    sync_health_data = []
    
    for inst in institutes:
        prog_count = db.query(Programme).filter(Programme.institute_id == inst.id).count()
        trainee_count = db.query(MemberProfile).join(User).filter(User.institute_id == inst.id).count()
        cert_count = db.query(Certificate).join(MemberProfile).join(User).filter(User.institute_id == inst.id).count()
        
        comparison_chart.append({
            "institute_id": inst.id,
            "institute_name": inst.name,
            "code": inst.code,
            "state": inst.state,
            "programmes": prog_count,
            "trainees": trainee_count,
            "certificates": cert_count
        })
        
        sync_health_data.append({
            "institute_id": inst.id,
            "name": inst.name,
            "code": inst.code,
            "status": inst.sync_status or "HEALTHY",
            "last_synced_at": inst.last_synced_at.isoformat() if inst.last_synced_at else None
        })

    recent_audits = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(10).all()
    audit_events = [
        {
            "id": log.id,
            "user_id": log.actor_id,
            "action": log.action,
            "resource": log.entity_type,
            "status": "SUCCESS",
            "ip_address": log.ip_address,
            "timestamp": log.created_at.isoformat() if log.created_at else None
        }
        for log in recent_audits
    ]

    return success_response(
        data={
            "is_demo_data": True,
            "metrics": {
                "total_institutes": total_institutes or 20,
                "active_institutes": active_institutes or 20,
                "total_programmes": total_programmes or 48,
                "programmes_completed": programmes_completed or 34,
                "trainees_enrolled": total_trainees or 2450,
                "trainees_completed": trainees_completed or 1890,
                "attendance_rate": 92.4,
                "assessment_completion": 88.6,
                "certificates_issued": certificates_issued or 1890,
                "placement_outcomes": total_placements or 1420
            },
            "approval_queue": approval_queue,
            "institute_comparison": comparison_chart,
            "sync_health": sync_health_data,
            "recent_audit_events": audit_events
        },
        message="NCCT HQ Consolidated National Dashboard retrieved"
    )

# 2. GET /api/v1/hq/institutes
@router.get("/institutes")
def list_institutes(
    state: Optional[str] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    query = db.query(Institute)
    if state:
        query = query.filter(Institute.state == state)
    if region:
        query = query.filter(Institute.region == region)
    
    institutes = query.order_by(Institute.code.asc()).all()
    return success_response(
        data=[
            {
                "id": inst.id,
                "code": inst.code,
                "name": inst.name,
                "institute_type": inst.institute_type,
                "region": inst.region,
                "state": inst.state,
                "city": inst.city,
                "address": inst.address,
                "contact_email": inst.contact_email,
                "contact_phone": inst.contact_phone,
                "is_active": inst.is_active,
                "sync_status": inst.sync_status,
                "last_synced_at": inst.last_synced_at.isoformat() if inst.last_synced_at else None
            }
            for inst in institutes
        ]
    )

# 3. POST /api/v1/hq/institutes
@router.post("/institutes")
def create_institute(
    payload: InstituteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    existing = db.query(Institute).filter(Institute.code == payload.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Institute code already exists.")
    
    inst = Institute(**payload.dict())
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return success_response(
        data={"id": inst.id, "code": inst.code, "name": inst.name},
        message="Institute registered successfully."
    )

# 4. GET /api/v1/hq/institutes/{id}
@router.get("/institutes/{id}")
def get_institute_detail(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    inst = db.query(Institute).filter(Institute.id == id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    prog_count = db.query(Programme).filter(Programme.institute_id == inst.id).count()
    trainee_count = db.query(MemberProfile).join(User).filter(User.institute_id == inst.id).count()
    
    return success_response(
        data={
            "id": inst.id,
            "code": inst.code,
            "name": inst.name,
            "institute_type": inst.institute_type,
            "region": inst.region,
            "state": inst.state,
            "city": inst.city,
            "address": inst.address,
            "contact_email": inst.contact_email,
            "contact_phone": inst.contact_phone,
            "is_active": inst.is_active,
            "sync_status": inst.sync_status,
            "metrics": {
                "programmes": prog_count,
                "trainees": trainee_count,
            }
        }
    )

# 5. PATCH /api/v1/hq/institutes/{id}
@router.patch("/institutes/{id}")
def update_institute(
    id: str,
    payload: InstituteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    inst = db.query(Institute).filter(Institute.id == id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    update_data = payload.dict(exclude_unset=True)
    for field, val in update_data.items():
        setattr(inst, field, val)
    
    db.commit()
    return success_response(message="Institute details updated.")

# 6. GET /api/v1/hq/programme-approvals
@router.get("/programme-approvals")
def get_programme_approvals(
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    query = db.query(Programme)
    if status_filter:
        query = query.filter(Programme.status == status_filter)
    
    programmes = query.order_by(Programme.created_at.desc()).all()
    results = []
    for p in programmes:
        inst = db.query(Institute).filter(Institute.id == p.institute_id).first()
        results.append({
            "id": p.id,
            "code": p.code,
            "title": p.title,
            "category": p.category,
            "status": p.status,
            "institute_id": p.institute_id,
            "institute_name": inst.name if inst else "Unknown",
            "target_capacity": p.target_capacity,
            "duration_weeks": p.duration_weeks,
            "rejection_reason": p.rejection_reason,
            "approval_comments": p.approval_comments,
            "submitted_at": p.submitted_at.isoformat() if p.submitted_at else None,
            "reviewed_at": p.reviewed_at.isoformat() if p.reviewed_at else None
        })
    return success_response(data=results)

# 7. PATCH /api/v1/hq/programme-approvals/{programme_id}
@router.patch("/programme-approvals/{programme_id}")
def update_programme_approval(
    programme_id: str,
    payload: ProgrammeApprovalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    p = db.query(Programme).filter(Programme.id == programme_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Programme not found")
    
    if payload.status not in ["APPROVED", "REJECTED", "CHANGES_REQUESTED"]:
        raise HTTPException(status_code=400, detail="Invalid approval status")
    
    p.status = payload.status
    p.approved_by_id = current_user.id
    p.approval_comments = payload.approval_comments
    if payload.rejection_reason:
        p.rejection_reason = payload.rejection_reason
    p.reviewed_at = datetime.now(timezone.utc)
    
    db.commit()
    return success_response(
        data={"id": p.id, "status": p.status},
        message=f"Programme {p.code} status updated to {p.status} by HQ."
    )

# 8. GET /api/v1/hq/national-calendar
@router.get("/national-calendar")
def get_national_calendar(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    batches = db.query(Batch).all()
    calendar_events = []
    for b in batches:
        inst = db.query(Institute).filter(Institute.id == b.institute_id).first()
        calendar_events.append({
            "id": b.id,
            "batch_code": b.batch_code,
            "batch_name": b.batch_name,
            "institute_id": b.institute_id,
            "institute_name": inst.name if inst else "Unknown",
            "status": b.status,
            "start_date": b.start_date,
            "end_date": b.end_date,
            "max_trainees": b.max_trainees
        })
    return success_response(data=calendar_events)

# 9. GET /api/v1/hq/analytics
@router.get("/analytics")
def get_hq_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    return success_response(
        data={
            "national_completion_rate": 91.2,
            "placement_rate": 76.5,
            "average_attendance": 93.8,
            "top_performing_institutes": [
                {"code": "RICM-BLR", "name": "RICM Bengaluru", "rating": 98.4},
                {"code": "RICM-GND", "name": "RICM Gandhinagar", "rating": 96.8},
                {"code": "RICM-CHD", "name": "RICM Chandigarh", "rating": 95.2},
                {"code": "ICM-PNE", "name": "ICM Pune", "rating": 94.9}
            ],
            "skill_domain_demand": [
                {"domain": "Cooperative ERP & Accounting", "enrollment_count": 840},
                {"domain": "Digital Banking & UPI Payments", "enrollment_count": 620},
                {"domain": "Agri-Business & Cold Chain", "enrollment_count": 510},
                {"domain": "Governance & Compliance", "enrollment_count": 480}
            ]
        }
    )

# 10. GET /api/v1/hq/reports
@router.get("/reports")
def get_hq_reports(
    report_type: str = "national_summary",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    return success_response(
        data={
            "report_title": f"NCCT National {report_type.replace('_', ' ').title()} Report",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generated_by": current_user.full_name,
            "summary": "Consolidated national metrics across all 20 NCCT institutes.",
            "download_urls": {
                "pdf": f"/api/v1/hq/reports/download?type={report_type}&format=pdf",
                "excel": f"/api/v1/hq/reports/download?type={report_type}&format=excel"
            }
        }
    )

# 11. GET /api/v1/hq/certificates
@router.get("/certificates")
def list_national_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    certs = db.query(Certificate).all()
    results = []
    for c in certs:
        mem = db.query(MemberProfile).filter(MemberProfile.id == c.member_id).first()
        usr = db.query(User).filter(User.id == mem.user_id).first() if mem else None
        inst = db.query(Institute).filter(Institute.id == usr.institute_id).first() if usr and usr.institute_id else None
        
        revoked_log = db.query(CertificateRevocationLog).filter(CertificateRevocationLog.certificate_id == c.id).first()
        
        results.append({
            "id": c.id,
            "certificate_number": c.certificate_number,
            "issued_at": c.issued_at.isoformat() if c.issued_at else None,
            "trainee_name": usr.full_name if usr else "Unknown Trainee",
            "institute_name": inst.name if inst else "NCCT National Registry",
            "status": "REVOKED" if revoked_log else "VALID",
            "revocation_reason": revoked_log.reason if revoked_log else None
        })
    return success_response(data=results)

# 12. POST /api/v1/hq/certificates/{id}/revoke
@router.post("/certificates/{id}/revoke")
def revoke_certificate(
    id: str,
    payload: RevokeCertificateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    cert = db.query(Certificate).filter(Certificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    existing = db.query(CertificateRevocationLog).filter(CertificateRevocationLog.certificate_id == id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Certificate is already revoked.")
    
    log = CertificateRevocationLog(
        certificate_id=cert.id,
        certificate_number=cert.certificate_number,
        revoked_by_id=current_user.id,
        revoked_by_name=current_user.full_name,
        reason=payload.reason
    )
    db.add(log)
    db.commit()
    
    return success_response(
        message=f"Certificate {cert.certificate_number} has been officially revoked by NCCT HQ."
    )

# 13. GET /api/v1/hq/certificates/verify/{certificate_number} (Public QR Verification)
@router.get("/certificates/verify/{certificate_number}")
def verify_certificate_public(
    certificate_number: str,
    db: Session = Depends(get_db)
):
    cert = db.query(Certificate).filter(Certificate.certificate_number == certificate_number).first()
    if not cert:
        return error_response(code="INVALID_CERTIFICATE", message="Certificate record not found in NCCT Central Registry.")
    
    revoked_log = db.query(CertificateRevocationLog).filter(CertificateRevocationLog.certificate_number == certificate_number).first()
    
    mem = db.query(MemberProfile).filter(MemberProfile.id == cert.member_id).first()
    usr = db.query(User).filter(User.id == mem.user_id).first() if mem else None
    inst = db.query(Institute).filter(Institute.id == usr.institute_id).first() if usr and usr.institute_id else None

    return success_response(
        data={
            "is_valid": revoked_log is None,
            "status": "REVOKED" if revoked_log else "VERIFIED_GENUINE",
            "certificate_number": cert.certificate_number,
            "trainee_name": usr.full_name if usr else "Verified Trainee",
            "institute_name": inst.name if inst else "National Council for Cooperative Training",
            "issued_at": cert.issued_at.isoformat() if cert.issued_at else None,
            "revocation_reason": revoked_log.reason if revoked_log else None
        },
        message="NCCT Certificate Verification Response"
    )

# 14. GET /api/v1/hq/audit-logs
@router.get("/audit-logs")
def get_hq_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(50).all()
    return success_response(
        data=[
            {
                "id": log.id,
                "user_id": log.actor_id,
                "action": log.action,
                "resource": log.entity_type,
                "status": "SUCCESS",
                "ip_address": log.ip_address,
                "timestamp": log.created_at.isoformat() if log.created_at else None
            }
            for log in logs
        ]
    )

# 15. GET & POST /api/v1/hq/templates
@router.get("/templates")
def list_national_templates(
    template_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    query = db.query(NationalTemplate)
    if template_type:
        query = query.filter(NationalTemplate.template_type == template_type)
    templates = query.all()
    return success_response(
        data=[
            {
                "id": t.id,
                "template_type": t.template_type,
                "title": t.title,
                "description": t.description,
                "content_json": t.content_json,
                "is_active": t.is_active,
                "created_at": t.created_at.isoformat() if t.created_at else None
            }
            for t in templates
        ]
    )

@router.post("/templates")
def create_national_template(
    payload: NationalTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hq_role)
):
    tmpl = NationalTemplate(
        template_type=payload.template_type,
        title=payload.title,
        description=payload.description,
        content_json=payload.content_json,
        created_by_id=current_user.id
    )
    db.add(tmpl)
    db.commit()
    db.refresh(tmpl)
    return success_response(
        data={"id": tmpl.id, "title": tmpl.title},
        message="National Governance Template published."
    )
