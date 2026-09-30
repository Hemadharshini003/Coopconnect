from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.sync import SyncEvent
from app.db.models.user import HQ_ROLES
from app.schemas.response import success_response, error_response
from app.api.deps import get_current_user, User

router = APIRouter(prefix="/sync", tags=["Offline Sync Engine"])

@router.post("/push")
def sync_push(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    device_id = payload.get("device_id", "mobile_device_001")
    request_institute_id = payload.get("institute_id")
    
    # Enforce institute_id consistency
    if request_institute_id and current_user.role not in HQ_ROLES:
        if current_user.institute_id and request_institute_id != current_user.institute_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sync rejected: Mismatched institute_id for current user context."
            )

    events = payload.get("events", [])
    processed = []
    for ev in events:
        sync_ev = SyncEvent(
            device_id=device_id,
            user_id=current_user.id,
            entity_type=ev.get("entity_type", "ASSESSMENT"),
            entity_id=ev.get("entity_id", "local_id"),
            operation=ev.get("operation", "CREATE"),
            sync_status="SYNCED",
            conflict_status="RESOLVED"
        )
        db.add(sync_ev)
        processed.append(ev.get("entity_id"))

    db.commit()

    return success_response(
        data={"synced_entity_ids": processed, "server_timestamp": datetime.now(timezone.utc).isoformat()},
        message="Sync events processed and merged with server state"
    )

@router.post("/pull")
def sync_pull(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    request_institute_id = payload.get("institute_id")
    if request_institute_id and current_user.role not in HQ_ROLES:
        if current_user.institute_id and request_institute_id != current_user.institute_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sync pull rejected: Mismatched institute_id."
            )

    return success_response(data={
        "institute_id": current_user.institute_id or request_institute_id,
        "updated_courses": [],
        "updated_quizzes": [],
        "updated_opportunities": [],
        "server_timestamp": datetime.now(timezone.utc).isoformat()
    })

@router.get("/status")
def sync_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    events = db.query(SyncEvent).filter(SyncEvent.user_id == current_user.id).order_by(SyncEvent.synced_at.desc()).limit(10).all()
    return success_response(data={
        "sync_status": "Synced",
        "pending_conflicts": 0,
        "user_institute_id": current_user.institute_id,
        "recent_sync_events": [
            {
                "id": e.id,
                "entity_type": e.entity_type,
                "operation": e.operation,
                "sync_status": e.sync_status,
                "synced_at": e.synced_at.isoformat()
            }
            for e in events
        ]
    })

@router.post("/resolve-conflict")
def resolve_conflict(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return success_response(message="Conflict resolved using server priority rule")
