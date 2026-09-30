from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.skill import Skill, RoleCatalog
from app.schemas.response import success_response
from app.api.deps import get_current_user

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.get("")
def list_skills(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    skills = db.query(Skill).all()
    data = [
        {
            "id": s.id,
            "name": s.name,
            "code": s.code,
            "category": s.category,
            "description": s.description,
            "proficiency_scale": s.proficiency_scale
        }
        for s in skills
    ]
    return success_response(data=data)

@router.post("")
def create_skill(payload: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    s = Skill(
        name=payload["name"],
        code=payload["code"],
        category=payload["category"],
        description=payload.get("description"),
        proficiency_scale=payload.get("proficiency_scale", 5)
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return success_response(data={"id": s.id, "name": s.name})

@router.get("/roles")
def list_role_catalog(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    roles = db.query(RoleCatalog).all()
    data = [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "category": r.category,
            "required_education": r.required_education,
            "required_experience": r.required_experience
        }
        for r in roles
    ]
    return success_response(data=data)
