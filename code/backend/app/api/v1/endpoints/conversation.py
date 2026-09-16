from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_customer
from app.models.customer import Customer
from app.schemas.conversation import (
    ConversationListItemSchema,
    ConversationDetailSchema,
    ConversationCreateResponse,
    ConversationMessagesListResponse,
    ConversationCloseResponse
)
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["Conversations (Khối 1)"])

@router.get(
    "",
    response_model=List[ConversationListItemSchema],
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách các phiên trò chuyện của khách hàng (Use Case 1.2)"
)
def list_conversations(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Tải danh sách các cuộc trò chuyện trước đây của khách hàng, kèm theo:
    - Thời gian tin nhắn gần nhất
    - Đoạn tóm tắt tin nhắn cuối (10-15 từ)
    - Trạng thái phiên (BOT, HUMAN, WAITING_HUMAN, CLOSED)
    """
    return ConversationService.get_customer_conversations(db=db, customer_id=current_customer.id)

@router.post(
    "",
    response_model=ConversationCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Bắt đầu cuộc trò chuyện mới (Use Case 1.2 A-1)"
)
def create_conversation(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Mở một phiên trò chuyện mới cho khách hàng:
    - Tự động kích hoạt Trợ lý ảo (mode = 'BOT')
    - Gửi lời chào mừng mở đầu kèm câu hỏi gợi ý
    """
    return ConversationService.create_conversation(db=db, customer_id=current_customer.id)

@router.get(
    "/{conversation_id}",
    response_model=ConversationDetailSchema,
    status_code=status.HTTP_200_OK,
    summary="Xem chi tiết trạng thái của phiên trò chuyện"
)
def get_conversation_detail(
    conversation_id: UUID,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin chi tiết và trạng thái chế độ hoạt động của phiên chat.
    """
    return ConversationService.get_conversation_detail(
        db=db,
        conversation_id=conversation_id,
        customer_id=current_customer.id
    )

@router.get(
    "/{conversation_id}/messages",
    response_model=ConversationMessagesListResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy lịch sử tin nhắn của phiên chat - Lazy Loading 50 tin nhắn (Use Case 1.2)"
)
def get_conversation_messages(
    conversation_id: UUID,
    limit: int = Query(50, ge=1, le=100, description="Số lượng tin nhắn tối đa mỗi lần tải"),
    before_id: Optional[UUID] = Query(None, description="Tải các tin nhắn cũ hơn message_id này"),
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Tải danh sách tin nhắn theo phân đoạn (mặc định 50 tin nhắn gần nhất):
    - Đầy đủ thông tin sender (BOT, CUSTOMER, AGENT)
    - Metadata trích dẫn tài liệu RAG (citations)
    - Hỗ trợ cuộn trang tải thêm (has_more)
    """
    return ConversationService.get_conversation_messages(
        db=db,
        conversation_id=conversation_id,
        customer_id=current_customer.id,
        limit=limit,
        before_id=before_id
    )

@router.post(
    "/{conversation_id}/close",
    response_model=ConversationCloseResponse,
    status_code=status.HTTP_200_OK,
    summary="Đóng / kết thúc phiên trò chuyện (Use Case 1.2 E-1)"
)
def close_conversation(
    conversation_id: UUID,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Chuyển trạng thái phiên trò chuyện sang 'CLOSED' (Đã kết thúc).
    """
    return ConversationService.close_conversation(
        db=db,
        conversation_id=conversation_id,
        customer_id=current_customer.id
    )
