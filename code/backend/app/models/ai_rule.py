import uuid
from sqlalchemy import Column, String, DateTime, Numeric, Text, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class AIRule(Base):
    __tablename__ = "system_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instruction_prompt = Column(Text, nullable=False, default="")
    p1_threshold = Column(Numeric(4, 2), nullable=False, default=-0.60)
    p2_threshold = Column(Numeric(4, 2), nullable=False, default=-0.30)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
