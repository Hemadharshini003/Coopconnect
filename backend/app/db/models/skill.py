import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Skill(Base):
    __tablename__ = "skills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    category = Column(String(100), nullable=False)  # Digital, ERP, Operations, Financial, Communication
    description = Column(Text, nullable=True)
    proficiency_scale = Column(Integer, default=5)  # 1 to 5
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RoleCatalog(Base):
    __tablename__ = "roles_catalog"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    required_education = Column(String(100), nullable=True)
    required_experience = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RoleRequiredSkill(Base):
    __tablename__ = "role_required_skills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    role_id = Column(String(36), ForeignKey("roles_catalog.id"), nullable=False)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False)
    required_level = Column(Integer, default=3)  # 1 to 5
    priority = Column(String(20), default="High")  # Low, Medium, High, Critical

class MemberSkill(Base):
    __tablename__ = "member_skills"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    member_id = Column(String(36), ForeignKey("member_profiles.id"), nullable=False)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False)
    current_level = Column(Integer, default=1)  # 1 to 5
    evidence_source = Column(String(100), default="Self Assessment")  # Assessment, Course Completion, Manager Verified
    confidence_score = Column(Float, default=0.8)  # 0.0 to 1.0
    last_assessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
