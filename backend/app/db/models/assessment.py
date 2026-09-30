import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class SkillAssessment(Base):
    __tablename__ = "skill_assessments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    member_id = Column(String(36), ForeignKey("member_profiles.id"), nullable=False)
    assessment_type = Column(String(50), default="Initial Readiness")
    status = Column(String(50), default="Submitted")  # In Progress, Submitted, Evaluated
    total_score = Column(Float, default=0.0)
    submitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    reviewed_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    assessment_id = Column(String(36), ForeignKey("skill_assessments.id"), nullable=True)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="MCQ")  # MCQ, Boolean, Text
    options_json = Column(Text, nullable=True)  # JSON string of options
    correct_answer = Column(String(255), nullable=False)
    marks = Column(Integer, default=10)

class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question_id = Column(String(36), ForeignKey("assessment_questions.id"), nullable=False)
    member_id = Column(String(36), ForeignKey("member_profiles.id"), nullable=False)
    answer = Column(Text, nullable=False)
    is_correct = Column(String(10), default="False")
    marks_awarded = Column(Integer, default=0)

class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    member_id = Column(String(36), ForeignKey("member_profiles.id"), nullable=False)
    target_role_id = Column(String(36), ForeignKey("roles_catalog.id"), nullable=False)
    skill_id = Column(String(36), ForeignKey("skills.id"), nullable=False)
    current_level = Column(Integer, default=0)
    required_level = Column(Integer, default=3)
    gap_score = Column(Float, default=0.0)  # Normalized 0 to 100
    priority = Column(String(20), default="High")  # Critical, High, Medium, Low
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
