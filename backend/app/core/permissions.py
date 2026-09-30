from enum import Enum
from typing import List
from fastapi import HTTPException, status

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    DISTRICT_ADMIN = "DISTRICT_ADMIN"
    COOPERATIVE_ADMIN = "COOPERATIVE_ADMIN"
    TRAINER = "TRAINER"
    MEMBER = "MEMBER"
    EMPLOYEE = "EMPLOYEE"
    EMPLOYER_OR_COOPERATIVE_RECRUITER = "EMPLOYER_OR_COOPERATIVE_RECRUITER"
    AUDITOR = "AUDITOR"

def check_role_permission(user_role: str, allowed_roles: List[UserRole]):
    """Verifies if user role is included in allowed_roles."""
    if user_role not in [r.value for r in allowed_roles] and user_role != UserRole.SUPER_ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: insufficient role permissions."
        )
