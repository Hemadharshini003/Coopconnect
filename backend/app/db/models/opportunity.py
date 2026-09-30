import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    cooperative_id = Column(String(36), ForeignKey("cooperatives.id"), nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    opportunity_type = Column(String(50), default="Job")  # Job, Task, Apprenticeship
    required_role_id = Column(String(36), ForeignKey("roles_catalog.id"), nullable=True)
    location = Column(String(255), nullable=True)
    remote_allowed = Column(Boolean, default=False)
    stipend_or_salary = Column(String(100), nullable=True)
    duration = Column(String(50), nullable=True)  # e.g., Full-time, 6 months
    number_of_positions = Column(Integer, default=1)
    deadline = Column(String(20), nullable=True)
    status = Column(String(50), default="Open")  # Open, Closed, Filled
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class OpportunityRequiredSkill(Base):
    __tablename__ = "opportunity_required_skills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False)
    required_level = Column(Integer, default=3)
    priority = Column(String(20), default="High")

class Application(Base):
    __tablename__ = "applications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    member_id = Column(String(36), ForeignKey("member_profiles.id"), nullable=False)
    match_score = Column(Float, default=0.0)
    match_explanation = Column(Text, nullable=True)
    status = Column(String(50), default="Submitted")  # Submitted, Shortlisted, Interviewed, Accepted, Rejected
    applied_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    reviewed_at = Column(DateTime, nullable=True)
    reviewed_by = Column(String(36), nullable=True)
