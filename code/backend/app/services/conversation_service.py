from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from fastapi import HTTPException, status

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.core.redis import redis_client
from app.schemas.conversation import (
    ConversationListItemSchema,
    ConversationDetailSchema,
    ConversationCreateResponse,
    ConversationMessagesListResponse,
    MessageItemSchema,
    ConversationCloseResponse,
    ConversationQueueItemSchema,
    AgentSendMessageResponse,
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

    @staticmethod
    def delete_conversation(db: Session, conversation_id: UUID, customer_id: UUID) -> dict:
        """
        Xóa cuộc hội thoại và tự động vô hiệu hóa các Ticket liên quan (status = 'CLOSED') (Use Case 1.4).
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
                detail="Bạn không có quyền xóa phiên trò chuyện này."
            )
            
        # 1. Vô hiệu hóa các Ticket liên quan (status -> CLOSED) và xóa các Ticket đó
        from app.models.ticket import Ticket
        tickets = db.query(Ticket).filter(Ticket.conversation_id == conversation_id).all()
        for t in tickets:
            t.status = "CLOSED"
            t.resolved_at = datetime.now(timezone.utc)
            if t.ai_metadata and isinstance(t.ai_metadata, dict):
                t.ai_metadata["closure_reason"] = "Phiên hội thoại đã bị khách hàng xóa"
            else:
                t.ai_metadata = {"closure_reason": "Phiên hội thoại đã bị khách hàng xóa"}
        
        db.flush()
        # Xóa các tickets thuộc phiên chat để không vi phạm NotNullViolation khi xóa conversation
        db.query(Ticket).filter(Ticket.conversation_id == conversation_id).delete(synchronize_session=False)

        # 2. Xóa các tin nhắn thuộc phiên hội thoại
        db.query(Message).filter(Message.conversation_id == conversation_id).delete(synchronize_session=False)

        # 3. Xóa bản ghi Conversation
        db.delete(conv)
        db.commit()

        # 4. Thông báo thời gian thực cho console nhân viên (UC 3.3): xóa khỏi hàng đợi + đóng khung chat
        payload = {
            "event": "CONVERSATION_DELETED",
            "payload": {
                "conversation_id": str(conversation_id),
                "deleted_id": str(conversation_id),
            }
        }
        try:
            redis_client.publish("channel:ws_alerts", json.dumps(payload, ensure_ascii=False))
            redis_client.publish(f"channel:chat:{conversation_id}", json.dumps(payload, ensure_ascii=False))
        except Exception:
            pass

        return {
            "status": "success",
            "message": "Đã xóa phiên trò chuyện và vô hiệu hóa phiếu hỗ trợ liên quan.",
            "deleted_id": str(conversation_id)
        }

    # ------------------------------------------------------------------ #
    # UC 3.3: Theo dõi Hàng đợi & Tiếp quản Cuộc trò chuyện (Live Console)
    # ------------------------------------------------------------------ #

    @staticmethod
    def get_agent_queue(db: Session) -> List[ConversationQueueItemSchema]:
        """
        Danh sách hàng đợi cho nhân viên:
        conversations đang bật cờ đỏ (is_flagged) hoặc đang chờ hỗ trợ người (WAITING_HUMAN),
        sắp xếp theo thời gian cập nhật mới nhất (UC 3.3).
        """
        conversations = (
            db.query(Conversation)
            .filter(or_(Conversation.is_flagged == True, Conversation.mode == "WAITING_HUMAN"))
            .order_by(desc(Conversation.updated_at))
            .all()
        )

        results: List[ConversationQueueItemSchema] = []
        for conv in conversations:
            last_msg = (
                db.query(Message)
                .filter(Message.conversation_id == conv.id)
                .order_by(desc(Message.created_at))
                .first()
            )

            snippet = None
            last_time = None
            if last_msg:
                snippet = last_msg.content[:80] + ("..." if len(last_msg.content) > 80 else "")
                last_time = last_msg.created_at

            agent_name = None
            if conv.assigned_agent_id:
                agent = db.query(User).filter(User.id == conv.assigned_agent_id).first()
                agent_name = agent.full_name if agent else None

            customer_name = conv.customer.full_name if conv.customer else None

            results.append(ConversationQueueItemSchema(
                id=conv.id,
                customer_id=conv.customer_id,
                customer_name=customer_name,
                assigned_agent_id=conv.assigned_agent_id,
                assigned_agent_name=agent_name,
                mode=conv.mode,
                is_flagged=conv.is_flagged,
                last_sentiment=conv.last_sentiment,
                last_message_content=snippet,
                last_message_time=last_time,
                created_at=conv.created_at,
                updated_at=conv.updated_at
            ))

        return results

    @staticmethod
    def _agent_can_access(conv: Optional[Conversation], user: User, write: bool = False) -> bool:
        """Kiểm tra quyền của nhân viên trên một phiên trò chuyện."""
        if not conv:
            return False
        if user.role in ("MANAGER", "ADMIN"):
            return True
        if conv.assigned_agent_id == user.id:
            return True
        if write:
            # Phiên chưa ai nhận trong hàng đợi vẫn cho gửi tin (giữ hành vi cũ, chưa tiếp quản)
            return conv.assigned_agent_id is None and (conv.is_flagged or conv.mode == "WAITING_HUMAN")
        # UC 3.3 E-1: phiên đã được nhân viên khác tiếp quản -> vẫn cho ĐỌC (chế độ Chỉ xem)
        return conv.is_flagged or conv.mode in ("WAITING_HUMAN", "HUMAN")

    @staticmethod
    def get_conversation_messages_for_agent(
        db: Session,
        conversation_id: UUID,
        user: User,
        limit: int = 50,
        before_id: Optional[UUID] = None
    ) -> ConversationMessagesListResponse:
        """
        Tải lịch sử tin nhắn cho nhân viên CSKH trước/sau khi tiếp quản (UC 3.3).
        """
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy phiên trò chuyện yêu cầu."
            )
        if not ConversationService._agent_can_access(conv, user):
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

        messages = (
            query.order_by(desc(Message.created_at))
            .limit(limit)
            .all()
        )
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
    def take_over_conversation(db: Session, conversation_id: UUID, user: User) -> ConversationDetailSchema:
        """
        Tiếp quản cuộc trò chuyện với khóa dòng chống tranh chấp (UC 3.3).
        - Khóa bản ghi bằng SELECT ... FOR UPDATE.
        - Nếu đã có nhân viên khác nhận -> 409 Conflict (E-1).
        - Thành công: gán assigned_agent_id, mode = 'HUMAN', gỡ cờ đỏ, ngắt Bot AI.
        """
        conv = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .with_for_update()
            .first()
        )
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy phiên trò chuyện yêu cầu."
            )

        if conv.assigned_agent_id is not None and conv.assigned_agent_id != user.id:
            agent_name = None
            if conv.assigned_agent_id:
                agent = db.query(User).filter(User.id == conv.assigned_agent_id).first()
                agent_name = agent.full_name if agent else None
            detail = (
                f"Cuộc trò chuyện này đã được nhân viên {agent_name} tiếp quản."
                if agent_name
                else "Cuộc trò chuyện này đã được nhân viên khác tiếp quản."
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        conv.assigned_agent_id = user.id
        conv.mode = "HUMAN"
        conv.is_flagged = False
        conv.updated_at = datetime.now(timezone.utc)
        db.flush()

        # Chèn thông báo hệ thống vào khung chat khách hàng (sender_type='BOT' do schema CHECK hạn chế)
        notice_content = f"Nhân viên tư vấn {user.full_name} đã tham gia cuộc trò chuyện."
        notice = Message(
            conversation_id=conv.id,
            sender_type="BOT",
            content=notice_content
        )
        db.add(notice)
        db.commit()
        db.refresh(conv)

        # Broadcast tới room chat của khách + console nhân viên
        payload = {
            "event": "CHAT_MODE_CHANGED",
            "payload": {
                "conversation_id": str(conv.id),
                "mode": "HUMAN",
                "assigned_agent_id": str(user.id),
                "assigned_agent_name": user.full_name,
                "message": notice_content,
                "notice_message": MessageItemSchema.model_validate(notice).model_dump(mode="json"),
            }
        }
        try:
            redis_client.publish(f"channel:chat:{conv.id}", json.dumps(payload, ensure_ascii=False))
            redis_client.publish("channel:ws_alerts", json.dumps(payload, ensure_ascii=False))
        except Exception:
            pass

        return ConversationDetailSchema.model_validate(conv)

    @staticmethod
    def send_agent_message(db: Session, conversation_id: UUID, user: User, content: str) -> AgentSendMessageResponse:
        """
        Gửi tin nhắn từ nhân viên CSKH (REST fallback) lưu sender_type='AGENT'
        và broadcast thời gian thực tới room chat (UC 3.3).
        """
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy phiên trò chuyện yêu cầu."
            )
        if not ConversationService._agent_can_access(conv, user, write=True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền gửi tin nhắn trong phiên trò chuyện này."
            )

        content = (content or "").strip()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vui lòng nhập nội dung tin nhắn trước khi gửi."
            )

        msg = Message(
            conversation_id=conv.id,
            sender_type="AGENT",
            sender_id=user.id,
            content=content
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)

        payload = {
            "type": "message",
            "event": "CHAT_MESSAGE",
            "payload": MessageItemSchema.model_validate(msg).model_dump(mode="json"),
        }
        try:
            redis_client.publish(f"channel:chat:{conv.id}", json.dumps(payload, ensure_ascii=False))
        except Exception:
            pass

        return AgentSendMessageResponse(message=MessageItemSchema.model_validate(msg))

