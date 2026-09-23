import uuid
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class TicketBase(BaseModel):
    category: str
    priority: str
    status: str
    summary: str
    ai_metadata: Optional[Dict[str, Any]] = None
    sla_breached: bool = False

class TicketResponse(TicketBase):
    id: uuid.UUID
    conversation_id: uuid.UUID
    assigned_to: Optional[uuid.UUID]
    sla_deadline: datetime
    resolution_note: Optional[str] = None
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TicketAssignRequest(BaseModel):
    agent_id: uuid.UUID

class TicketResolveRequest(BaseModel):
    resolution_note: str = Field(..., min_length=10, max_length=1000, description="Nội dung kết quả xử lý, 10-1000 ký tự.")

    @field_validator("resolution_note")
    @classmethod
    def check_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Nội dung không được chỉ chứa khoảng trắng.")
        return v
