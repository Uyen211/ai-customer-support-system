from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.user import StaffLoginRequest, StaffTokenResponse, UserResponse
from app.services.user_service import UserService


router = APIRouter(prefix="/auth/agent", tags=["Staff Auth"])


@router.post(
    "/login",
    response_model=StaffTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Đăng nhập Bàn làm việc CSKH (Use Case 3.1)"
)
def login(req: StaffLoginRequest, db: Session = Depends(get_db)):
    return UserService.login_staff(db=db, req=req)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin nhân viên đang đăng nhập"
)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
