from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models.user import User
from app.schemas.user import StaffCreateRequest, StaffStatusUpdateRequest, UserResponse
from app.services.user_service import UserService


admin_router = APIRouter(prefix="/admin/users", tags=["Staff Management"])
agent_router = APIRouter(prefix="/agent", tags=["Agent Presence"])


@admin_router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo tài khoản nhân viên mới (Use Case 3.1)"
)
def create_staff(
    req: StaffCreateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN", "MANAGER")),
):
    return UserService.create_staff(db=db, req=req)


@admin_router.get(
    "",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Danh sách tài khoản nhân viên"
)
def list_staff(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN", "MANAGER")),
):
    return UserService.list_staff(db=db)


@agent_router.put(
    "/status",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật trạng thái làm việc nhân viên (Use Case 3.2)"
)
def update_status(
    req: StaffStatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserService.update_status(db=db, user=current_user, req=req)
