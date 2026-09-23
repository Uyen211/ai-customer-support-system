import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    category = Column(String(50), nullable=False)
    priority = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    summary = Column(Text, nullable=False)
    ai_metadata = Column(JSONB, nullable=True)
    sla_deadline = Column(DateTime(timezone=True), nullable=False)
    sla_breached = Column(Boolean, nullable=False, default=False)
    resolution_note = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    conversation = relationship("Conversation", back_populates="tickets")
