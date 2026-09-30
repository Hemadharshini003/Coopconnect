import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class SyncEvent(Base):
    __tablename__ = "sync_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    device_id = Column(String(100), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(String(36), nullable=False)
    operation = Column(String(20), nullable=False)  # CREATE, UPDATE, DELETE
    payload_hash = Column(String(100), nullable=True)
    sync_status = Column(String(50), default="SYNCED")  # PENDING, SYNCED, CONFLICT
    conflict_status = Column(String(50), default="RESOLVED")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    synced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ExternalErpRecord(Base):
    __tablename__ = "external_erp_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    cooperative_id = Column(String(36), ForeignKey("cooperatives.id"), nullable=False)
    source_system = Column(String(100), nullable=False)  # e.g., Tally, SAP, Custom Cooperative ERP
    external_id = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)  # Member, Inventory, Transaction
    payload_json = Column(Text, nullable=True)
    last_synced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sync_status = Column(String(50), default="SUCCESS")
