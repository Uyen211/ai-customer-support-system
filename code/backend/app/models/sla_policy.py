import uuid
from sqlalchemy import Column, String, DateTime, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class SLAPolicy(Base):
    __tablename__ = "sla_policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    priority = Column(String(10), unique=True, nullable=False)
    resolution_time_minutes = Column(Integer, nullable=False)
    escalation_notify_to = Column(String(20), nullable=False, default="MANAGER")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
