"""
Orchestrator Pipeline toàn trình cho RAG Assistant (Kiến trúc KH-06 Nâng cấp).
Điều phối 5 bước từ lúc nhận Query -> Decomposer -> Parallel Retrieval -> Synthesizer -> Lưu DB.
"""

import json
import logging
from typing import AsyncGenerator, Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.common.models import Conversation, Message
from app.modules.rag_assistant.decomposer import decomposer_service
from app.modules.rag_assistant.retrievers import parallel_retrieval_service
from app.modules.rag_assistant.synthesizer import synthesizer_service
from app.modules.rag_assistant.schemas import AggregatedContext

logger = logging.getLogger(__name__)

class RAGPipelineService:
    def __init__(self):
        self.decomposer = decomposer_service
        self.retrieval = parallel_retrieval_service
        self.synthesizer = synthesizer_service

    async def stream_chat_pipeline(
        self,
        conversation_id: str,
        user_message: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Thực thi toàn bộ luồng RAG KH-06 và yield SSE chunks dạng dictionary.
        """
        db: Session = SessionLocal()
        try:
            # 1. Kiểm tra trạng thái cuộc trò chuyện
            conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conv and conv.mode in ["WAITING_HUMAN", "HUMAN"]:
                logger.info(f"Cuộc trò chuyện {conversation_id} đang ở mode {conv.mode}. Bỏ qua RAG Bot.")
                notice = "Hệ thống đang chuyển tiếp bạn tới chuyên viên CSKH hỗ trợ trực tiếp. Vui lòng chờ trong giây lát ạ!"
                yield {"event": "token", "data": {"token": notice}}
                yield {"event": "done", "data": {"full_text": notice, "citations": []}}
                return

            # Lưu tin nhắn của Customer vào DB
            cust_msg = Message(
                conversation_id=conversation_id,
                sender_type="CUSTOMER",
                content=user_message
            )
            db.add(cust_msg)
            db.commit()

            # Kéo lịch sử chat gần nhất
            history_rows = (
                db.query(Message)
                .filter(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(6)
                .all()
            )
            chat_history = [
                {"sender_type": m.sender_type, "content": m.content}
                for m in reversed(history_rows)
            ]
        finally:
            db.close()

        # 2. Bước Decomposer & Intent Router (Prompt 1)
        decomposer_res = await self.decomposer.decompose(user_message, chat_history)

        # 3. Bước Parallel Retrieval Workers
        aggregated_ctx: AggregatedContext = await self.retrieval.execute_parallel(
            sub_queries=decomposer_res.sub_queries,
            standalone_query=decomposer_res.standalone_query
        )

        # 4. Bước Multi-Context Synthesizer (Prompt 2) Streaming
        full_response_text = []
        async for token in self.synthesizer.stream_synthesize(aggregated_ctx):
            full_response_text.append(token)
            yield {"event": "token", "data": {"token": token}}

        final_text = "".join(full_response_text)
        citations_data = [c.model_dump() for c in aggregated_ctx.all_citations]

        # 5. Lưu tin nhắn BOT và Citations vào CSDL
        db_save: Session = SessionLocal()
        try:
            bot_msg = Message(
                conversation_id=conversation_id,
                sender_type="BOT",
                content=final_text,
                citations=citations_data if citations_data else None
            )
            db_save.add(bot_msg)
            db_save.commit()
            db_save.refresh(bot_msg)
            logger.info(f"Đã lưu tin nhắn BOT thành công (Message ID: {bot_msg.id})")
        except Exception as e:
            logger.error(f"Lỗi khi lưu tin nhắn BOT vào DB: {e}")
        finally:
            db_save.close()

        # Bắn chunk kết thúc với metadata & citations
        yield {
            "event": "done",
            "data": {
                "full_text": final_text,
                "citations": citations_data,
                "sub_queries_count": len(decomposer_res.sub_queries)
            }
        }

rag_pipeline_service = RAGPipelineService()
