from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import re

class CustomerRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=50, description="Họ và tên khách hàng (2-50 ký tự)")
    email: EmailStr = Field(..., description="Địa chỉ email chuẩn")
    password: str = Field(..., min_length=8, description="Mật khẩu tối thiểu 8 ký tự, gồm cả chữ và số")
    phone: Optional[str] = Field(None, description="Số điện thoại gồm 10 chữ số bắt đầu bằng 0")

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Mật khẩu phải có độ dài từ 8 ký tự trở lên")
        if not re.search(r"[A-Za-z]", v) or not re.search(r"\d", v):
            raise ValueError("Mật khẩu bắt buộc phải chứa ít nhất một chữ cái và một chữ số")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip() != "":
            v = v.strip()
            if not re.match(r"^0\d{9}$", v):
                raise ValueError("Số điện thoại phải gồm 10 chữ số bắt đầu bằng 0")
            return v
        return None

class CustomerLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Địa chỉ email đăng nhập")
    password: str = Field(..., description="Mật khẩu tài khoản")

class CustomerResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    customer: CustomerResponse
