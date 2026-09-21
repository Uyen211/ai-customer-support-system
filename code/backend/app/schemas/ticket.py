import uuid
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

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
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TicketAssignRequest(BaseModel):
    agent_id: uuid.UUID
