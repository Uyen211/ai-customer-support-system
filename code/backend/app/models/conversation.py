import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    assigned_agent_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    mode = Column(String(20), nullable=False, default="BOT")
    is_flagged = Column(Boolean, nullable=False, default=False)
    last_sentiment = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="conversation", cascade="all, delete-orphan")
