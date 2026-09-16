import uuid
from sqlalchemy import Column, String, DateTime, Numeric, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    sender_type = Column(String(10), nullable=False)
    sender_id = Column(UUID(as_uuid=True), nullable=True)
    content = Column(Text, nullable=False)
    citations = Column(JSONB, nullable=True)
    sentiment_score = Column(Numeric(4, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
