from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.canned_response import CannedResponse
from app.models.user import User
from app.schemas.canned_response import (
    CannedResponseCreate,
    CannedResponseUpdate,
    CannedResponseResponse,
)


class CannedResponseService:
    """Nghiệp vụ mẫu phản hồi nhanh (UC 3.4)."""

    @staticmethod
    def _can_manage(response: CannedResponse, user: User) -> bool:
        if user.role in ("MANAGER", "ADMIN"):
            return True
        return response.created_by == user.id

    @staticmethod
    def create(db: Session, req: CannedResponseCreate, user: User) -> CannedResponseResponse:
        shortcut = req.shortcut.strip()
        exists = db.query(CannedResponse).filter(CannedResponse.shortcut == shortcut).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Shortcut '/{shortcut}' đã tồn tại. Vui lòng chọn shortcut khác.",
            )

        response = CannedResponse(
            shortcut=shortcut,
            title=req.title.strip(),
            content=req.content.strip(),
            category=req.category.strip(),
            created_by=user.id,
        )
        db.add(response)
        db.commit()
        db.refresh(response)
        return CannedResponseResponse.model_validate(response)

    @staticmethod
    def list_responses(
        db: Session,
        category: Optional[str] = None,
        q: Optional[str] = None,
    ) -> List[CannedResponseResponse]:
        query = db.query(CannedResponse)
        if category:
            query = query.filter(CannedResponse.category == category)
        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    CannedResponse.title.ilike(like),
                    CannedResponse.content.ilike(like),
                    CannedResponse.shortcut.ilike(like),
                )
            )
        items = query.order_by(CannedResponse.shortcut.asc()).all()
        return [CannedResponseResponse.model_validate(i) for i in items]

    @staticmethod
    def update(db: Session, response_id: UUID, req: CannedResponseUpdate, user: User) -> CannedResponseResponse:
        item = db.query(CannedResponse).filter(CannedResponse.id == response_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy mẫu phản hồi nhanh.",
            )
        if not CannedResponseService._can_manage(item, user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền chỉnh sửa mẫu phản hồi này.",
            )

        if req.shortcut is not None:
            new_shortcut = req.shortcut.strip()
            conflict = db.query(CannedResponse).filter(
                CannedResponse.shortcut == new_shortcut,
                CannedResponse.id != response_id,
            ).first()
            if conflict:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Shortcut '/{new_shortcut}' đã tồn tại. Vui lòng chọn shortcut khác.",
                )
            item.shortcut = new_shortcut
        if req.title is not None:
            item.title = req.title.strip()
        if req.content is not None:
            item.content = req.content.strip()
        if req.category is not None:
            item.category = req.category.strip()

        db.commit()
        db.refresh(item)
        return CannedResponseResponse.model_validate(item)

    @staticmethod
    def delete(db: Session, response_id: UUID, user: User) -> dict:
        item = db.query(CannedResponse).filter(CannedResponse.id == response_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy mẫu phản hồi nhanh.",
            )
        if not CannedResponseService._can_manage(item, user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền xóa mẫu phản hồi này.",
            )

        db.delete(item)
        db.commit()
        return {"status": "success", "message": "Đã xóa mẫu phản hồi nhanh.", "deleted_id": str(response_id)}