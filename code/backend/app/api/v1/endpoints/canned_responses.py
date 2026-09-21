from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.user import User
from app.schemas.canned_response import (
    CannedResponseCreate,
    CannedResponseUpdate,
    CannedResponseResponse,
)
from app.services.canned_response_service import CannedResponseService


router = APIRouter(prefix="/canned-responses", tags=["Canned Responses"])


@router.get(
    "",
    response_model=List[CannedResponseResponse],
    status_code=status.HTTP_200_OK,
    summary="Danh sách mẫu phản hồi nhanh (UC 3.4)",
)
def list_canned_responses(
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN")),
):
    """Liệt kê các mẫu phản hồi nhanh, có thể lọc theo danh mục hoặc tìm kiếm."""
    return CannedResponseService.list_responses(db=db, category=category, q=q)


@router.post(
    "",
    response_model=CannedResponseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo mẫu phản hồi nhanh mới (UC 3.4)",
)
def create_canned_response(
    req: CannedResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN")),
):
    return CannedResponseService.create(db=db, req=req, user=current_user)


@router.put(
    "/{response_id}",
    response_model=CannedResponseResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật mẫu phản hồi nhanh (UC 3.4)",
)
def update_canned_response(
    response_id: UUID,
    req: CannedResponseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN")),
):
    return CannedResponseService.update(db=db, response_id=response_id, req=req, user=current_user)


@router.delete(
    "/{response_id}",
    status_code=status.HTTP_200_OK,
    summary="Xóa mẫu phản hồi nhanh (UC 3.4)",
)
def delete_canned_response(
    response_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN")),
):
    return CannedResponseService.delete(db=db, response_id=response_id, user=current_user)