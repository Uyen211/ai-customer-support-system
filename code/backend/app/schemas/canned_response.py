from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CannedResponseCreate(BaseModel):
    shortcut: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=150)
    content: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=50)


class CannedResponseUpdate(BaseModel):
    shortcut: Optional[str] = Field(None, min_length=1, max_length=50)
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=50)


class CannedResponseResponse(BaseModel):
    id: UUID
    shortcut: str
    title: str
    content: str
    category: str
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True