from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CannedResponseCreate(BaseModel):
    shortcut: str = Field(..., description="Phím tắt kích hoạt, bắt đầu bằng '/'")
    title: str = Field(..., max_length=150)
    content: str
    category: str = Field(..., max_length=50)

    @field_validator("shortcut")
    @classmethod
    def validate_shortcut(cls, v):
        v = v.strip()
        if not v.startswith("/"):
            raise ValueError("Phím tắt phải bắt đầu bằng '/' (VD: /hoan-tien).")
        body = v[1:].strip()
        if " " in body:
            raise ValueError("Phím tắt không được chứa khoảng trắng.")
        if not (1 <= len(body) <= 49):
            raise ValueError("Phím tắt phải dài từ 2 đến 50 ký tự (kể cả dấu '/').")
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        v = v.strip()
        if not (3 <= len(v) <= 150):
            raise ValueError("Tiêu đề phải dài từ 3 đến 150 ký tự.")
        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        v = v.strip()
        if not (2 <= len(v) <= 50):
            raise ValueError("Danh mục phải dài từ 2 đến 50 ký tự.")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        v = v.strip()
        if not (5 <= len(v) <= 2000):
            raise ValueError("Nội dung phải dài từ 5 đến 2000 ký tự.")
        return v


class CannedResponseUpdate(BaseModel):
    shortcut: Optional[str] = Field(None, description="Phím tắt kích hoạt, bắt đầu bằng '/'")
    title: Optional[str] = Field(None, max_length=150)
    content: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)

    @field_validator("shortcut")
    @classmethod
    def validate_shortcut(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v.startswith("/"):
            raise ValueError("Phím tắt phải bắt đầu bằng '/' (VD: /hoan-tien).")
        body = v[1:].strip()
        if " " in body:
            raise ValueError("Phím tắt không được chứa khoảng trắng.")
        if not (1 <= len(body) <= 49):
            raise ValueError("Phím tắt phải dài từ 2 đến 50 ký tự (kể cả dấu '/').")
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not (3 <= len(v) <= 150):
            raise ValueError("Tiêu đề phải dài từ 3 đến 150 ký tự.")
        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not (2 <= len(v) <= 50):
            raise ValueError("Danh mục phải dài từ 2 đến 50 ký tự.")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not (5 <= len(v) <= 2000):
            raise ValueError("Nội dung phải dài từ 5 đến 2000 ký tự.")
        return v


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