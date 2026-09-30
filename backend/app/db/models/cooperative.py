import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Cooperative(Base):
    __tablename__ = "cooperatives"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    registration_number = Column(String(100), unique=True, nullable=False)
    cooperative_type = Column(String(100), nullable=False)  # Dairy, Agriculture, Artisans, Financial, etc.
    description = Column(Text, nullable=True)
    state = Column(String(100), nullable=False, default="Maharashtra")
    district_id = Column(String(36), ForeignKey("districts.id"), nullable=False)
    institute_id = Column(String(36), ForeignKey("institutes.id"), nullable=True)
    block = Column(String(100), nullable=True)
    village = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    logo_url = Column(String(500), nullable=True)
    status = Column(String(50), default="Active")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    institute = relationship("Institute", back_populates="cooperatives")
