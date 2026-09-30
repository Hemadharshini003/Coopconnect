import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Placement(Base):
    __tablename__ = "placements"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    application_id = Column(String(36), ForeignKey("applications.id"), nullable=False)
    member_id = Column(String(36), ForeignKey("member_profiles.id"), nullable=False)
    opportunity_id = Column(String(36), ForeignKey("opportunities.id"), nullable=False)
    start_date = Column(String(20), nullable=True)
    end_date = Column(String(20), nullable=True)
    outcome = Column(String(100), default="Successful Placement")
    income_before = Column(Float, default=0.0)
    income_after = Column(Float, default=0.0)
    performance_score = Column(Float, default=4.5)
    retention_status = Column(String(50), default="Retained")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
