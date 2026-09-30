import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Institute(Base):
    __tablename__ = "institutes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    institute_type = Column(String(100), default="Regional Institute of Cooperative Management") # RICM or ICM
    region = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    director_name = Column(String(255), nullable=True, default="Dr. NCCT Director")
    total_training_capacity = Column(Integer, default=500)
    is_active = Column(Boolean, default=True)
    sync_status = Column(String(50), default="HEALTHY")
    last_synced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    users = relationship("User", back_populates="institute")
    programmes = relationship("Programme", back_populates="institute")
    cooperatives = relationship("Cooperative", back_populates="institute")
