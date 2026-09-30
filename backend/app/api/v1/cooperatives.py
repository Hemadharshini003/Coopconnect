from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.cooperative import Cooperative
from app.schemas.response import success_response
from app.api.deps import get_current_user, User

router = APIRouter(prefix="/cooperatives", tags=["Cooperatives"])

@router.get("")
def list_cooperatives(district_id: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Cooperative)
    if district_id:
        query = query.filter(Cooperative.district_id == district_id)
    elif current_user.role == "DISTRICT_ADMIN" and current_user.district_id:
        query = query.filter(Cooperative.district_id == current_user.district_id)
    elif current_user.role == "COOPERATIVE_ADMIN" and current_user.cooperative_id:
        query = query.filter(Cooperative.id == current_user.cooperative_id)

    cooperatives = query.all()
    data = [
        {
            "id": c.id,
            "name": c.name,
            "registration_number": c.registration_number,
            "cooperative_type": c.cooperative_type,
            "state": c.state,
            "district_id": c.district_id,
            "block": c.block,
            "village": c.village,
            "status": c.status
        }
        for c in cooperatives
    ]
    return success_response(data=data)

@router.post("")
def create_cooperative(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    coop = Cooperative(
        name=payload["name"],
        registration_number=payload["registration_number"],
        cooperative_type=payload["cooperative_type"],
        description=payload.get("description"),
        district_id=payload["district_id"],
        block=payload.get("block"),
        village=payload.get("village"),
        address=payload.get("address"),
        phone=payload.get("phone"),
        email=payload.get("email")
    )
    db.add(coop)
    db.commit()
    db.refresh(coop)
    return success_response(data={"id": coop.id, "name": coop.name}, message="Cooperative created successfully")

@router.get("/{id}")
def get_cooperative(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    coop = db.query(Cooperative).filter(Cooperative.id == id).first()
    if not coop:
        raise HTTPException(status_code=404, detail="Cooperative society not found")

    return success_response(data={
        "id": coop.id,
        "name": coop.name,
        "registration_number": coop.registration_number,
        "cooperative_type": coop.cooperative_type,
        "description": coop.description,
        "district_id": coop.district_id,
        "block": coop.block,
        "village": coop.village,
        "address": coop.address,
        "phone": coop.phone,
        "email": coop.email,
        "status": coop.status
    })
