import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Programme(Base):
    __tablename__ = "programmes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), default="Cooperative Management & Tech")
    duration_weeks = Column(Integer, default=4)
    target_capacity = Column(Integer, default=50)
    
    # Workflow status: DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, CHANGES_REQUESTED
    status = Column(String(50), default="DRAFT", index=True)
    proposed_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    approved_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    approval_comments = Column(Text, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    start_date = Column(String(20), nullable=True)
    end_date = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    institute = relationship("Institute", back_populates="programmes")
    batches = relationship("Batch", back_populates="programme", cascade="all, delete-orphan")

class Batch(Base):
    __tablename__ = "batches"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    programme_id = Column(String(36), ForeignKey("programmes.id"), nullable=False)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=False)
    batch_code = Column(String(50), unique=True, index=True, nullable=False)
    batch_name = Column(String(255), nullable=False)
    max_trainees = Column(Integer, default=40)
    status = Column(String(50), default="UPCOMING") # UPCOMING, ONGOING, COMPLETED, CANCELLED
    start_date = Column(String(20), nullable=True)
    end_date = Column(String(20), nullable=True)
    trainer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    programme = relationship("Programme", back_populates="batches")
    attendance_records = relationship("AttendanceRecord", back_populates="batch", cascade="all, delete-orphan")

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    trainee_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    date = Column(String(20), nullable=False) # YYYY-MM-DD
    status = Column(String(20), default="PRESENT") # PRESENT, ABSENT, LATE, EXCUSED
    session_topic = Column(String(255), nullable=True)
    marked_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    batch = relationship("Batch", back_populates="attendance_records")

class NationalTemplate(Base):
    __tablename__ = "national_templates"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    template_type = Column(String(50), nullable=False) # PROGRAMME, COURSE, CERTIFICATE, ATTENDANCE_POLICY, ASSESSMENT_POLICY, FEEDBACK
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content_json = Column(Text, nullable=False) # Stored JSON structure/schema
    is_active = Column(Boolean, default=True)
    created_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class CertificateRevocationLog(Base):
    __tablename__ = "certificate_revocation_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    certificate_id = Column(String(36), nullable=False)
    certificate_number = Column(String(100), nullable=False)
    revoked_by_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    revoked_by_name = Column(String(255), nullable=False)
    reason = Column(Text, nullable=False)
    revoked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
