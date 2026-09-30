from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.opportunity import Application, Opportunity
from app.db.models.profile import MemberProfile
from app.db.models.user import User
from app.schemas.response import success_response
from app.api.deps import get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.get("/me")
def get_my_applications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    mp = db.query(MemberProfile).filter(MemberProfile.user_id == current_user.id).first()
    if not mp:
        return success_response(data=[])

    apps = db.query(Application, Opportunity).join(Opportunity, Application.opportunity_id == Opportunity.id).filter(Application.member_id == mp.id).all()
    data = [
        {
            "id": a.id,
            "opportunity_id": o.id,
            "opportunity_title": o.title,
            "opportunity_type": o.opportunity_type,
            "match_score": a.match_score,
            "status": a.status,
            "applied_at": a.applied_at
        }
        for a, o in apps
    ]
    return success_response(data=data)

@router.patch("/{id}/status")
def update_application_status(id: str, payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    app = db.query(Application).filter(Application.id == id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    new_status = payload.get("status", "Accepted")
    app.status = new_status
    app.reviewed_by = current_user.id
    db.commit()

    return success_response(data={"application_id": app.id, "status": app.status}, message=f"Application status updated to {new_status}")
