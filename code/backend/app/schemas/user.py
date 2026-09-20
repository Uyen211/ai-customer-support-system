from datetime import datetime
from typing import List, Optional
from uuid import UUID
import re

from pydantic import BaseModel, EmailStr, Field, field_validator


VALID_ROLES = {"AGENT", "MANAGER", "ADMIN"}
VALID_STATUSES = {"ONLINE", "BUSY", "OFFLINE"}


class StaffLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email nội bộ đăng nhập")
    password: str = Field(..., description="Mật khẩu tài khoản nhân viên")


class StaffCreateRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    role: str = Field(default="AGENT")
    skills: List[str] = Field(default_factory=list)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
            raise ValueError("Mật khẩu bắt buộc phải chứa ít nhất một chữ cái và một chữ số")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None or value.strip() == "":
            return None
        value = value.strip()
        if not re.match(r"^0\d{9}$", value):
            raise ValueError("Số điện thoại phải gồm 10 chữ số bắt đầu bằng 0")
        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        value = value.upper().strip()
        if value not in VALID_ROLES:
            raise ValueError("Vai trò phải là AGENT, MANAGER hoặc ADMIN")
        return value

    @field_validator("skills")
    @classmethod
    def normalize_skills(cls, value: List[str]) -> List[str]:
        return [item.strip() for item in value if item and item.strip()]

    def validate_business_rules(self) -> None:
        if self.role == "AGENT" and not self.skills:
            raise ValueError("Tài khoản Agent bắt buộc chọn ít nhất 1 kỹ năng xử lý")


class StaffStatusUpdateRequest(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        value = value.upper().strip()
        if value not in VALID_STATUSES:
            raise ValueError("Trạng thái phải là ONLINE, BUSY hoặc OFFLINE")
        return value


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone: Optional[str] = None
    role: str
    status: str
    skills: List[str] = Field(default_factory=list)
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class StaffTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
