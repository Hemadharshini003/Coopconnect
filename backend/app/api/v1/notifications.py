from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.audit import Notification
from app.schemas.response import success_response
from app.api.deps import get_current_user, User

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("")
def list_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notifications = db.query(Notification).filter(Notification.recipient_id == current_user.id).order_by(Notification.created_at.desc()).all()
    
    # If empty, return initial demo notification
    if not notifications:
        data = [
            {
                "id": "notif-001",
                "title": "Skill Assessment Evaluation Complete",
                "message": "Your skill profile has been calculated. 3 new course recommendations are available.",
                "type": "SUCCESS",
                "read": False,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "notif-002",
                "title": "New Job Match Found",
                "message": "Pragati Dairy Cooperative posted 'Digital Inventory Assistant' matching your skills (92.5% match).",
                "type": "INFO",
                "read": False,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
    else:
        data = [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "type": n.type,
                "read": n.read_at is not None,
                "created_at": n.created_at.isoformat()
            }
            for n in notifications
        ]

    return success_response(data=data)
