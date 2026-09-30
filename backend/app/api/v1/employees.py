from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.profile import EmployeeProfile
from app.db.models.user import User
from app.schemas.response import success_response
from app.api.deps import get_current_user

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("")
def list_employees(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    emps = db.query(EmployeeProfile, User).join(User, EmployeeProfile.user_id == User.id).all()
    data = [
        {
            "id": ep.id,
            "user_id": u.id,
            "employee_number": ep.employee_number,
            "full_name": u.full_name,
            "email": u.email,
            "designation": ep.designation,
            "employment_type": ep.employment_type,
            "current_status": ep.current_status
        }
        for ep, u in emps
    ]
    return success_response(data=data)
