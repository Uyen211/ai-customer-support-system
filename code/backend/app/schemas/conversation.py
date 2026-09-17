from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime
from uuid import UUID

class MessageItemSchema(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_type: str
    sender_id: Optional[UUID] = None
    content: str
    citations: Optional[List[Dict[str, Any]]] = None
    sentiment_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationListItemSchema(BaseModel):
    id: UUID
    customer_id: UUID
    assigned_agent_id: Optional[UUID] = None
    mode: str
    is_flagged: bool
    last_sentiment: Optional[str] = None
    last_message_content: Optional[str] = None
    last_message_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ConversationDetailSchema(BaseModel):
    id: UUID
    customer_id: UUID
    assigned_agent_id: Optional[UUID] = None
    mode: str
    is_flagged: bool
    last_sentiment: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ConversationCreateResponse(BaseModel):
    conversation: ConversationDetailSchema
    initial_message: MessageItemSchema

class ConversationMessagesListResponse(BaseModel):
    conversation_id: UUID
    mode: str
    is_flagged: bool
    messages: List[MessageItemSchema]
    total: int
    has_more: bool

class ConversationCloseResponse(BaseModel):
    status: str = "success"
    message: str = "Phiên trò chuyện đã được kết thúc thành công."
    mode: str = "CLOSED"
