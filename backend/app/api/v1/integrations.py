import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.sync import ExternalErpRecord
from app.schemas.response import success_response
from app.api.deps import get_current_user, User

router = APIRouter(prefix="/integrations/erp", tags=["ERP Integrations API"])

@router.post("/import")
def erp_import(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    coop_id = payload.get("cooperative_id", current_user.cooperative_id or "c1111111-1111-1111-1111-111111111111")
    source = payload.get("source_system", "Tally ERP")
    external_id = payload.get("external_id", "ERP-1002")
    entity_type = payload.get("entity_type", "MemberRecord")

    record = ExternalErpRecord(
        cooperative_id=coop_id,
        source_system=source,
        external_id=external_id,
        entity_type=entity_type,
        payload_json=json.dumps(payload.get("data", {})),
        sync_status="SUCCESS"
    )
    db.add(record)
    db.commit()

    return success_response(
        data={"erp_record_id": record.id, "external_id": external_id},
        message=f"ERP record imported successfully from {source}"
    )

@router.get("/export")
def erp_export(cooperative_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    records = db.query(ExternalErpRecord).filter(ExternalErpRecord.cooperative_id == cooperative_id).all()
    return success_response(data=[
        {
            "id": r.id,
            "source_system": r.source_system,
            "external_id": r.external_id,
            "entity_type": r.entity_type,
            "last_synced_at": r.last_synced_at.isoformat()
        }
        for r in records
    ])

@router.get("/status")
def erp_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return success_response(data={
        "integrated_systems": ["Tally ERP 9", "SAP S/4HANA Coop", "Custom Dairy Ledger"],
        "last_sync_status": "Operational",
        "total_records_synced": 1420
    })
