import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Venue(Base):
    __tablename__ = "venues"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), default="CLASSROOM")  # CLASSROOM, LAB, HALL, ONLINE
    capacity = Column(Integer, default=40)
    equipment_json = Column(JSON, nullable=True)  # e.g., ["PROJECTOR", "AC", "DIGITAL_BOARD", "COMPUTERS"]
    availability_status = Column(String(50), default="AVAILABLE")  # AVAILABLE, UNDER_MAINTENANCE
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    institute = relationship("Institute")

class TimetableSession(Base):
    __tablename__ = "timetable_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=False)
    programme_id = Column(String(36), ForeignKey("training_programmes.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    module_id = Column(String(36), ForeignKey("courses.id"), nullable=True)
    title = Column(String(255), nullable=False)
    session_date = Column(String(20), nullable=False)  # YYYY-MM-DD
    start_time = Column(String(10), nullable=False)   # HH:MM (24-hr format)
    end_time = Column(String(10), nullable=False)     # HH:MM
    venue_id = Column(String(36), ForeignKey("venues.id"), nullable=True)
    trainer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    delivery_mode = Column(String(50), default="OFFLINE")  # OFFLINE, ONLINE, HYBRID
    session_status = Column(String(50), default="SCHEDULED")  # SCHEDULED, COMPLETED, CANCELLED, RESCHEDULED
    attendance_required = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    programme = relationship("Programme")
    batch = relationship("Batch")
    venue = relationship("Venue")
    trainer = relationship("User")
    conflicts = relationship("TimetableConflict", back_populates="session", cascade="all, delete-orphan")

class TimetableConflict(Base):
    __tablename__ = "timetable_conflicts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("timetable_sessions.id"), nullable=False)
    conflict_type = Column(String(100), nullable=False)  # TRAINER_DOUBLE_BOOKED, VENUE_DOUBLE_BOOKED, CAPACITY_EXCEEDED, OUTSIDE_PROGRAMME_DATE
    severity = Column(String(50), default="HIGH")        # LOW, MEDIUM, HIGH, BLOCKER
    details = Column(Text, nullable=False)
    status = Column(String(50), default="UNRESOLVED")     # UNRESOLVED, RESOLVED, OVERRIDDEN
    resolved_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    session = relationship("TimetableSession", back_populates="conflicts")
