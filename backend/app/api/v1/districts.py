from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.district import District
from app.schemas.response import success_response
from app.api.deps import get_current_user

router = APIRouter(prefix="/districts", tags=["Districts"])

@router.get("")
def list_districts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    districts = db.query(District).all()
    data = [
        {
            "id": d.id,
            "name": d.name,
            "state": d.state,
            "country": d.country,
            "code": d.code
        }
        for d in districts
    ]
    return success_response(data=data)
