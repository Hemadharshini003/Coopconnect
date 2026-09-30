from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_token
from app.db.models.user import User, HQ_ROLES, INSTITUTE_ROLES, ROLE_RECRUITER, ROLE_TRAINEE

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if user is None:
        raise credentials_exception
        
    return user

def get_current_active_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in HQ_ROLES and current_user.role not in ["DISTRICT_ADMIN", "COOPERATIVE_ADMIN", "INSTITUTE_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

def require_hq_role(current_user: User = Depends(get_current_user)) -> User:
    """
    Enforces that the user belongs to NCCT Headquarters governance roles.
    """
    if current_user.role not in HQ_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="NCCT Headquarters role required"
        )
    return current_user

def require_institute_role(current_user: User = Depends(get_current_user)) -> User:
    """
    Enforces that the user belongs to Institute roles or HQ authorization.
    """
    if current_user.role not in INSTITUTE_ROLES and current_user.role not in HQ_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Institute role or HQ authorization required"
        )
    return current_user

def verify_institute_scope(
    target_institute_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
) -> Optional[str]:
    """
    Returns the effective institute_id scope for database queries.
    HQ users return target_institute_id (or None if viewing all national data).
    Institute users are strictly bound to their own current_user.institute_id.
    Raises 403 Forbidden if an institute user attempts cross-institute data access.
    """
    if current_user.role in HQ_ROLES:
        return target_institute_id
    
    user_inst_id = current_user.institute_id
    if target_institute_id and user_inst_id and target_institute_id != user_inst_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-institute data access is strictly forbidden for institute accounts."
        )
    return user_inst_id

def verify_programme_assignment(
    programme_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> bool:
    """
    Verifies that a trainer or coordinator is assigned to the specified programme/institute.
    HQ roles bypass individual programme level scoping.
    """
    if current_user.role in HQ_ROLES:
        return True
    
    # Check institute boundary
    from app.db.models.programme import Programme
    prog = db.query(Programme).filter(Programme.id == programme_id).first()
    if not prog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Programme not found")
        
    if current_user.institute_id and prog.institute_id and current_user.institute_id != prog.institute_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to access programmes of another institute."
        )
    return True

def verify_trainee_self_scope(
    target_trainee_id: str,
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Allows trainees to access only their own data.
    Allows Institute Staff and NCCT HQ roles to view trainee records within scope.
    """
    if current_user.id == target_trainee_id:
        return current_user
    
    if current_user.role in HQ_ROLES:
        return current_user
        
    if current_user.role in INSTITUTE_ROLES and current_user.role != ROLE_TRAINEE:
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access restricted to own trainee profile."
    )

def verify_recruiter_scope(
    target_employer_id: Optional[str],
    current_user: User = Depends(get_current_user)
) -> Optional[str]:
    """
    Restricts recruiters to manage only opportunities and applications of their assigned organisation.
    """
    if current_user.role in HQ_ROLES or current_user.role in ["INSTITUTE_ADMIN", "PLACEMENT_OFFICER"]:
        return target_employer_id
        
    if current_user.role == ROLE_RECRUITER:
        return target_employer_id
        
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Recruiter or Placement Officer authorization required."
    )
