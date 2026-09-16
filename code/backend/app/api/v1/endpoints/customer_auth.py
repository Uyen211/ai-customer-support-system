from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_customer
from app.models.customer import Customer
from app.schemas.customer import (
    CustomerRegisterRequest,
    CustomerLoginRequest,
    CustomerResponse,
    TokenResponse
)
from app.services.customer_auth_service import CustomerAuthService

router = APIRouter(prefix="/auth/customer", tags=["Customer Auth"])

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản khách hàng mới (Use Case 1.1)"
)
def register(
    req: CustomerRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Đăng ký tài khoản khách hàng mới:
    - Họ và tên: 2-50 ký tự
    - Email: Định dạng chuẩn, không trùng lặp
    - Mật khẩu: Tối thiểu 8 ký tự, gồm cả chữ và số
    - Số điện thoại (tùy chọn): 10 chữ số bắt đầu bằng số 0
    """
    return CustomerAuthService.register_customer(db=db, req=req)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Đăng nhập tài khoản khách hàng (Use Case 1.1 A-1)"
)
def login(
    req: CustomerLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Đăng nhập tài khoản khách hàng bằng email và mật khẩu:
    - Trả về Access Token chuẩn JWT (HS256)
    - Tự động khóa 15 phút nếu nhập sai mật khẩu 5 lần liên tiếp
    """
    return CustomerAuthService.login_customer(db=db, req=req)

@router.get(
    "/me",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin cá nhân khách hàng đang đăng nhập"
)
def get_me(
    current_customer: Customer = Depends(get_current_customer)
):
    """
    Lấy thông tin tài khoản của khách hàng hiện tại dựa trên Bearer Token trong Header.
    """
    return CustomerResponse.model_validate(current_customer)
