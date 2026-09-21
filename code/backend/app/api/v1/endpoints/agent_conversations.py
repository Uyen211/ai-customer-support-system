from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models.user import User
from app.schemas.conversation import (
    AgentSendMessageRequest,
    AgentSendMessageResponse,
    ConversationDetailSchema,
    ConversationMessagesListResponse,
    ConversationQueueItemSchema,
)
from app.services.conversation_service import ConversationService


router = APIRouter(prefix="/agent/conversations", tags=["Agent Live Console"])


@router.get(
    "/queue",
    response_model=List[ConversationQueueItemSchema],
    status_code=status.HTTP_200_OK,
    summary="Danh sách hàng đợi hội thoại cần hỗ trợ (UC 3.3)",
)
def get_queue(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN")),
):
    """Lấy danh sách cuộc trò chuyện đang chờ hỗ trợ người (cờ đỏ / WAITING_HUMAN)."""
    return ConversationService.get_agent_queue(db=db)


@router.post(
    "/{conversation_id}/takeover",
    response_model=ConversationDetailSchema,
    status_code=status.HTTP_200_OK,
    summary="Tiếp quản cuộc trò chuyện (UC 3.3)",
)
def take_over(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN")),
):
    """Nhân viên CSKH tiếp quản một cuộc trò chuyện trong hàng đợi."""
    return ConversationService.take_over_conversation(db=db, conversation_id=conversation_id, user=current_user)


@router.get(
    "/{conversation_id}/messages",
    response_model=ConversationMessagesListResponse,
    status_code=status.HTTP_200_OK,
    summary="Xem lịch sử tin nhắn trước/sau khi tiếp quản (UC 3.3)",
)
def get_messages(
    conversation_id: UUID,
    limit: int = 50,
    before_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN")),
):
    """Tải lịch sử trao đổi của hội thoại cho nhân viên CSKH."""
    return ConversationService.get_conversation_messages_for_agent(
        db=db,
        conversation_id=conversation_id,
        user=current_user,
        limit=min(max(limit, 1), 200),
        before_id=before_id,
    )


@router.post(
    "/{conversation_id}/messages",
    response_model=AgentSendMessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Gửi tin nhắn từ nhân viên CSKH (UC 3.3)",
)
def send_message(
    conversation_id: UUID,
    req: AgentSendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN")),
):
    """Gửi tin nhắn từ nhân viên tới khách hàng (REST fallback, thời gian thực qua WS)."""
    return ConversationService.send_agent_message(
        db=db,
        conversation_id=conversation_id,
        user=current_user,
        content=req.content,
    )