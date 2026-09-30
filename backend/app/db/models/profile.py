import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class MemberProfile(Base):
    __tablename__ = "member_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    cooperative_id = Column(String(36), ForeignKey("cooperatives.id"), nullable=False)
    membership_number = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(String(20), nullable=True)
    gender = Column(String(20), nullable=True)
    education_level = Column(String(100), nullable=True)
    occupation = Column(String(100), nullable=True)
    years_of_experience = Column(Integer, default=0)
    preferred_language = Column(String(10), default="en")
    location = Column(String(255), nullable=True)
    availability = Column(String(50), default="Immediate")
    profile_completion_percentage = Column(Float, default=0.0)
    consent_for_matching = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="member_profile")

class EmployeeProfile(Base):
    __tablename__ = "employee_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    cooperative_id = Column(String(36), ForeignKey("cooperatives.id"), nullable=False)
    employee_number = Column(String(100), unique=True, nullable=False)
    designation = Column(String(100), nullable=False)
    joining_date = Column(String(20), nullable=True)
    employment_type = Column(String(50), default="Full-time")
    reporting_manager_id = Column(String(36), nullable=True)
    current_status = Column(String(50), default="Active")

    user = relationship("User", back_populates="employee_profile")
