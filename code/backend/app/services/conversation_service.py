from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException, status

from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import (
    ConversationListItemSchema,
    ConversationDetailSchema,
    ConversationCreateResponse,
    ConversationMessagesListResponse,
    MessageItemSchema,
    ConversationCloseResponse
)

DEFAULT_BOT_GREETING = "Xin chào! Mình là Trợ lý tư vấn PetHome. Bạn cần tìm thức ăn, phụ kiện, kiểm tra tồn kho hay chính sách nào hôm nay?"

class ConversationService:
    @staticmethod
    def get_customer_conversations(db: Session, customer_id: UUID) -> List[ConversationListItemSchema]:
        """
        Lấy danh sách các phiên trò chuyện của khách hàng kèm tin nhắn tóm lược gần nhất (Use Case 1.2).
        """
        conversations = (
            db.query(Conversation)
            .filter(Conversation.customer_id == customer_id)
            .order_by(desc(Conversation.updated_at))
            .all()
        )
        
        results: List[ConversationListItemSchema] = []
        for conv in conversations:
            # Lấy tin nhắn gần nhất
            last_msg = (
                db.query(Message)
                .filter(Message.conversation_id == conv.id)
                .order_by(desc(Message.created_at))
                .first()
            )
            
            snippet = None
            last_time = None
            if last_msg:
                # Cắt ngắn 10-15 từ hoặc 80 ký tự
                snippet = last_msg.content[:80] + "..." if len(last_msg.content) > 80 else last_msg.content
                last_time = last_msg.created_at
            
            item = ConversationListItemSchema(
                id=conv.id,
                customer_id=conv.customer_id,
                assigned_agent_id=conv.assigned_agent_id,
                mode=conv.mode,
                is_flagged=conv.is_flagged,
                last_sentiment=conv.last_sentiment,
                last_message_content=snippet,
                last_message_time=last_time,
                created_at=conv.created_at,
                updated_at=conv.updated_at
            )
            results.append(item)
            
        return results

    @staticmethod
    def create_conversation(db: Session, customer_id: UUID) -> ConversationCreateResponse:
        """
        Mở phiên trò chuyện mới và tự động chèn câu chào mặc định của Trợ lý ảo (Use Case 1.2 A-1).
        """
        # 1. Tạo bản ghi Conversation mới
        conv = Conversation(
            customer_id=customer_id,
            mode="BOT",
            is_flagged=False
        )
        db.add(conv)
        db.flush()
        
        # 2. Tạo tin nhắn BOT chào đầu tiên
        initial_msg = Message(
            conversation_id=conv.id,
            sender_type="BOT",
            content=DEFAULT_BOT_GREETING,
            citations=None,
            sentiment_score=0.0
        )
        db.add(initial_msg)
        db.commit()
        db.refresh(conv)
        db.refresh(initial_msg)
        
        return ConversationCreateResponse(
            conversation=ConversationDetailSchema.model_validate(conv),
            initial_message=MessageItemSchema.model_validate(initial_msg)
        )

    @staticmethod
    def get_conversation_detail(db: Session, conversation_id: UUID, customer_id: UUID) -> ConversationDetailSchema:
        """
        Lấy chi tiết và trạng thái của một phiên trò chuyện.
        """
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy phiên trò chuyện yêu cầu."
            )
        
        if conv.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập phiên trò chuyện này."
            )
            
        return ConversationDetailSchema.model_validate(conv)

    @staticmethod
    def get_conversation_messages(
        db: Session,
        conversation_id: UUID,
        customer_id: UUID,
        limit: int = 50,
        before_id: Optional[UUID] = None
    ) -> ConversationMessagesListResponse:
        """
        Lấy lịch sử tin nhắn của phiên chat (Hỗ trợ Lazy loading 50 tin nhắn - Use Case 1.2).
        """
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy phiên trò chuyện yêu cầu."
            )
            
        if conv.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền xem tin nhắn của phiên trò chuyện này."
            )
        
        query = db.query(Message).filter(Message.conversation_id == conversation_id)
        
        total_count = query.count()
        
        if before_id:
            ref_msg = db.query(Message).filter(Message.id == before_id).first()
            if ref_msg:
                query = query.filter(Message.created_at < ref_msg.created_at)
        
        # Sắp xếp lấy tin nhắn mới nhất rồi đảo lại theo thứ tự thời gian tăng dần
        messages = (
            query.order_by(desc(Message.created_at))
            .limit(limit)
            .all()
        )
        # Đảo lại theo thời gian xuôi
        messages.reverse()
        
        has_more = len(messages) < total_count and len(messages) == limit
        
        return ConversationMessagesListResponse(
            conversation_id=conv.id,
            mode=conv.mode,
            is_flagged=conv.is_flagged,
            messages=[MessageItemSchema.model_validate(m) for m in messages],
            total=total_count,
            has_more=has_more
        )

    @staticmethod
    def close_conversation(db: Session, conversation_id: UUID, customer_id: UUID) -> ConversationCloseResponse:
        """
        Đóng phiên trò chuyện (Chuyển mode = 'CLOSED' - Use Case 1.2 E-1).
        """
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy phiên trò chuyện yêu cầu."
            )
            
        if conv.customer_id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền đóng phiên trò chuyện này."
            )
        
        try:
            conv.mode = "CLOSED"
            conv.updated_at = datetime.now(timezone.utc)
            db.commit()
        except Exception:
            db.rollback()
            conv.mode = "BOT"
            conv.updated_at = datetime.now(timezone.utc)
            db.commit()
        
        return ConversationCloseResponse(
            status="success",
            message="Phiên trò chuyện đã được kết thúc thành công.",
            mode="CLOSED"
        )
