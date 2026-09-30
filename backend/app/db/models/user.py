import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

# NCCT HQ Roles
ROLE_NCCT_SUPER_ADMIN = "NCCT_SUPER_ADMIN"
ROLE_NCCT_PROGRAMME_ADMIN = "NCCT_PROGRAMME_ADMIN"
ROLE_NCCT_ANALYTICS_OFFICER = "NCCT_ANALYTICS_OFFICER"
ROLE_NCCT_CERTIFICATE_AUTHORITY = "NCCT_CERTIFICATE_AUTHORITY"
ROLE_NCCT_AUDITOR = "NCCT_AUDITOR"

HQ_ROLES = {
    ROLE_NCCT_SUPER_ADMIN,
    ROLE_NCCT_PROGRAMME_ADMIN,
    ROLE_NCCT_ANALYTICS_OFFICER,
    ROLE_NCCT_CERTIFICATE_AUTHORITY,
    ROLE_NCCT_AUDITOR,
    "SUPER_ADMIN" # legacy alias
}

# Institute Level Roles
ROLE_INSTITUTE_ADMIN = "INSTITUTE_ADMIN"
ROLE_INSTITUTE_PROGRAMME_COORDINATOR = "INSTITUTE_PROGRAMME_COORDINATOR"
ROLE_TRAINER = "TRAINER"
ROLE_ATTENDANCE_OPERATOR = "ATTENDANCE_OPERATOR"
ROLE_PLACEMENT_OFFICER = "PLACEMENT_OFFICER"
ROLE_RECRUITER = "RECRUITER"
ROLE_KIOSK_OPERATOR = "KIOSK_OPERATOR"
ROLE_INSTITUTE_AUDITOR = "INSTITUTE_AUDITOR"
ROLE_TRAINEE = "TRAINEE"

INSTITUTE_ROLES = {
    ROLE_INSTITUTE_ADMIN,
    ROLE_INSTITUTE_PROGRAMME_COORDINATOR,
    ROLE_TRAINER,
    ROLE_ATTENDANCE_OPERATOR,
    ROLE_PLACEMENT_OFFICER,
    ROLE_RECRUITER,
    ROLE_KIOSK_OPERATOR,
    ROLE_INSTITUTE_AUDITOR,
    ROLE_TRAINEE,
    "COOPERATIVE_ADMIN", # legacy alias
    "DISTRICT_ADMIN",    # legacy alias
    "MEMBER",            # legacy alias
    "EMPLOYER_OR_COOPERATIVE_RECRUITER" # legacy alias
}

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    preferred_language = Column(String(10), default="en")
    role = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    
    district_id = Column(String(36), ForeignKey("districts.id"), nullable=True)
    cooperative_id = Column(String(36), ForeignKey("cooperatives.id"), nullable=True)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=True)
    
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    institute = relationship("Institute", back_populates="users")
    member_profile = relationship("MemberProfile", back_populates="user", uselist=False)
    employee_profile = relationship("EmployeeProfile", back_populates="user", uselist=False)

class Role(Base):
    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    role_id = Column(String(36), ForeignKey("roles.id"), nullable=False)
    permission_id = Column(String(36), ForeignKey("permissions.id"), nullable=False)
