"""
Pipeline Orchestrator cho RAG Assistant (Kiến trúc KH-06 Nâng cấp).
Điều phối toàn bộ luồng: Bẻ câu hỏi -> Tra cứu song song -> Gom ngữ cảnh -> Stream câu trả lời -> Tự động lưu DB.
"""

import json
import logging
from typing import AsyncGenerator, Dict, Any, Optional, List
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.rag import AggregatedContext
from app.services.rag.decomposer import decomposer_service
from app.services.rag.retrievers import parallel_retrieval_service
from app.services.rag.synthesizer import synthesizer_service

logger = logging.getLogger(__name__)

class RAGPipelineService:
    """Orchestrator điều phối toàn trình 5 bước theo Kiến trúc RAG KH-06."""

    async def execute_stream(
        self,
        conversation_id: str,
        user_message: str
    ) -> AsyncGenerator[str, None]:
        logger.info(f"=== [BẮT ĐẦU RAG KH-06 PIPELINE] Conversation: {conversation_id} ===")
        
        # 0. Kiểm tra trạng thái hội thoại và lấy lịch sử chat
        db: Session = SessionLocal()
        chat_history = []
        try:
            conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conv:
                if conv.mode == "AGENT":
                    logger.info(f"Hội thoại {conversation_id} đang ở chế độ AGENT. Bỏ qua RAG Pipeline.")
                    yield f"event: error\ndata: {json.dumps({'error': 'Conversation is assigned to human agent'})}\n\n"
                    return

                # Lấy 6 tin nhắn gần nhất
                recent_msgs = db.query(Message).filter(
                    Message.conversation_id == conversation_id
                ).order_by(Message.created_at.desc()).limit(6).all()
                
                for m in reversed(recent_msgs):
                    role = "user" if m.sender_type == "CUSTOMER" else "assistant"
                    chat_history.append({"role": role, "content": m.content})
        finally:
            db.close()

        # BƯỚC 1: Query Decomposition & Per-subquery Intent Routing
        decomposer_output = await decomposer_service.decompose(
            query=user_message,
            chat_history=chat_history
        )
        standalone_query = decomposer_output.standalone_query

        # BƯỚC 2: Parallel Retrieval Workers (SQL, Vector HNSW, OutOfDomain)
        aggregated_context: AggregatedContext = await parallel_retrieval_service.retrieve_all(
            sub_queries=decomposer_output.sub_queries
        )
        aggregated_context.standalone_query = standalone_query

        # BƯỚC 3 & 4: Multi-Context Synthesizer Stream
        full_response_text = ""
        try:
            async for token in synthesizer_service.generate_response_stream(
                aggregated_context=aggregated_context,
                chat_history=chat_history
            ):
                full_response_text += token
                data_payload = json.dumps({"token": token}, ensure_ascii=False)
                yield f"event: token\ndata: {data_payload}\n\n"
        except Exception as e:
            logger.error(f"Lỗi khi stream synthesizer: {e}")
            error_msg = "Xin lỗi, hệ thống gặp sự cố khi tổng hợp câu trả lời. Vui lòng thử lại sau."
            full_response_text = error_msg
            yield f"event: token\ndata: {json.dumps({'token': error_msg}, ensure_ascii=False)}\n\n"

        # BƯỚC 5: Tự động lưu tin nhắn Bot và citations vào CSDL
        citations_data = [c.model_dump() for c in aggregated_context.all_citations]
        self._save_bot_message_to_db(
            conversation_id=conversation_id,
            content=full_response_text,
            citations=citations_data
        )

        # Gửi sự kiện done kết thúc SSE Stream
        done_payload = json.dumps({
            "full_text": full_response_text,
            "citations": citations_data,
            "standalone_query": standalone_query,
            "is_complex": decomposer_output.is_complex
        }, ensure_ascii=False)
        yield f"event: done\ndata: {done_payload}\n\n"
        logger.info(f"=== [HOÀN THÀNH RAG KH-06 PIPELINE] ===")

    def _save_bot_message_to_db(self, conversation_id: str, content: str, citations: List[Dict[str, Any]]):
        """Lưu tin nhắn của BOT cùng danh sách trích dẫn vào bảng messages."""
        db: Session = SessionLocal()
        try:
            # Kiểm tra xem conversation có tồn tại không
            conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conv:
                bot_msg = Message(
                    conversation_id=conv.id,
                    sender_type="BOT",
                    content=content,
                    citations=citations
                )
                db.add(bot_msg)
                db.commit()
                logger.info(f"Đã lưu tin nhắn BOT vào CSDL cho conversation: {conversation_id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Lỗi khi lưu tin nhắn BOT vào CSDL: {e}")
        finally:
            db.close()

rag_pipeline_service = RAGPipelineService()
