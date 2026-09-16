import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class AIRule(Base):
    __tablename__ = "ai_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_name = Column(String(100), nullable=False)
    sentiment_threshold = Column(Numeric(4, 2), nullable=False)
    target_priority = Column(String(10), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
