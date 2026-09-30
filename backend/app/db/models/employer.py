import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Employer(Base):
    __tablename__ = "employers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=True)
    organisation_name = Column(String(255), nullable=False)
    organisation_type = Column(String(100), default="Cooperative Society") # Dairy Cooperative, PACS, DCCB, Federal Coop, Training Partner
    contact_person = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    verified_status = Column(String(50), default="VERIFIED") # VERIFIED, PENDING
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    recruiters = relationship("RecruiterProfile", back_populates="employer")

class RecruiterProfile(Base):
    __tablename__ = "recruiter_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    employer_id = Column(String(36), ForeignKey("employers.id"), nullable=False)
    designation = Column(String(100), default="Talent Acquisition Officer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User")
    employer = relationship("Employer", back_populates="recruiters")

class CandidateRecommendation(Base):
    __tablename__ = "candidate_recommendations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    trainee_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    match_score = Column(Float, default=0.0)             # Overall 0 - 100
    skill_similarity_score = Column(Float, default=0.0)  # Cosine similarity 0 - 100
    explanation_json = Column(JSON, nullable=True)       # e.g., {"strengths": [...], "gaps": [...], "fairness_note": "No sensitive attributes used"}
    status = Column(String(50), default="RECOMMENDED")   # RECOMMENDED, SHORTLISTED, REJECTED, CONTACTED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    opportunity = relationship("Opportunity")
    trainee = relationship("User")
