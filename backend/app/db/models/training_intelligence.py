import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class TrainingHealthScore(Base):
    __tablename__ = "training_health_scores"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=False)
    trainee_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    programme_id = Column(String(36), ForeignKey("training_programmes.id"), nullable=True)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=True)
    
    # Explainable Weighted Component Scores (0-100 normalized)
    attendance_component = Column(Float, default=100.0)   # 25% weight
    learning_component = Column(Float, default=100.0)     # 20% weight
    assessment_component = Column(Float, default=100.0)   # 25% weight
    engagement_component = Column(Float, default=100.0)   # 15% weight
    support_component = Column(Float, default=100.0)      # 15% weight
    
    total_score = Column(Float, default=100.0)           # 0 - 100 overall
    risk_level = Column(String(50), default="LOW")        # LOW (80-100), MEDIUM (60-79), HIGH (<60)
    risk_reasons_json = Column(JSON, nullable=True)      # e.g., ["Consecutive absence 2 days", "Failed ERP Quiz"]
    recommended_actions_json = Column(JSON, nullable=True) # e.g., ["Assign Remedial ERP Module", "Schedule 1-on-1"]
    model_version = Column(String(50), default="RULE_V1")
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    trainee = relationship("User", foreign_keys=[trainee_id])
    institute = relationship("Institute")

class RiskAlert(Base):
    __tablename__ = "risk_alerts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=False)
    trainee_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    programme_id = Column(String(36), ForeignKey("training_programmes.id"), nullable=True)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=True)
    health_score_id = Column(String(36), ForeignKey("training_health_scores.id"), nullable=True)
    alert_type = Column(String(100), default="SUPPORT_RECOMMENDED") # SUPPORT_RECOMMENDED, URGENT_REVIEW
    severity = Column(String(50), default="MEDIUM") # LOW, MEDIUM, HIGH
    reasons_json = Column(JSON, nullable=True)
    status = Column(String(50), default="ACTIVE")   # ACTIVE, ACKNOWLEDGED, RESOLVED
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True) # Trainer User ID
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime, nullable=True)

    trainee = relationship("User", foreign_keys=[trainee_id])
    assigned_trainer = relationship("User", foreign_keys=[assigned_to])

class TraineeIntervention(Base):
    __tablename__ = "trainee_interventions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=False)
    trainee_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    programme_id = Column(String(36), ForeignKey("training_programmes.id"), nullable=True)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=True)
    risk_alert_id = Column(String(36), ForeignKey("risk_alerts.id"), nullable=True)
    intervention_type = Column(String(100), nullable=False) # REMEDIAL_COURSE, MENTOR_SESSION, TRAINER_CALL, LANGUAGE_SUPPORT, OFFLINE_CONTENT_PACKAGE, EXTRA_PRACTICE_QUIZ, ATTENDANCE_FOLLOWUP, TECHNICAL_SUPPORT
    reason = Column(Text, nullable=False)
    assigned_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    due_date = Column(String(20), nullable=True)
    status = Column(String(50), default="ASSIGNED") # ASSIGNED, IN_PROGRESS, COMPLETED, CANCELLED
    outcome_notes = Column(Text, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    trainee = relationship("User", foreign_keys=[trainee_id])
    trainer = relationship("User", foreign_keys=[assigned_by])
