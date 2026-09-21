"""
Pipeline Orchestrator cho RAG Assistant (Kiến trúc KH-06 Nâng cấp).
Điều phối toàn bộ luồng: Bẻ câu hỏi -> Tra cứu song song -> Gom ngữ cảnh -> Stream câu trả lời -> Tự động lưu DB.
"""

import json
import logging
from datetime import datetime, timezone, timedelta
from typing import AsyncGenerator, Dict, Any, Optional, List
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.ticket import Ticket
from app.models.ai_rule import AIRule
from app.core.redis import redis_client
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
        
        # Validation E-1 (Độ dài tin nhắn)
        if not user_message or len(user_message.strip()) < 2 or len(user_message) > 1000:
            logger.info("Tin nhắn không hợp lệ, trả về lỗi E-1.")
            yield f"event: error\ndata: {json.dumps({'error': 'Tin nhắn không hợp lệ. Vui lòng nhập từ 2 đến 1000 ký tự.'}, ensure_ascii=False)}\n\n"
            return

        # 0. Kiểm tra trạng thái hội thoại và lấy lịch sử chat
        db: Session = SessionLocal()
        chat_history = []
        try:
            conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conv:
                if conv.mode == "CLOSED":
                    logger.info(f"Hội thoại {conversation_id} đã đóng (CLOSED). Bỏ qua RAG Pipeline.")
                    yield f"event: error\ndata: {json.dumps({'error': 'Phiên hỗ trợ này đã đóng. Bạn có thể bấm Bắt đầu cuộc trò chuyện mới để được hỗ trợ tiếp.'}, ensure_ascii=False)}\n\n"
                    return
                elif conv.mode == "WAITING_HUMAN":
                    logger.info(f"Hội thoại {conversation_id} đang chờ nhân viên (WAITING_HUMAN).")
                    yield f"event: notice\ndata: {json.dumps({'message': 'Cuộc trò chuyện đang được chuyển tiếp tới nhân viên tư vấn. Vui lòng chờ trong giây lát...'}, ensure_ascii=False)}\n\n"
                    return
                elif conv.mode in ["HUMAN", "AGENT"]:
                    logger.info(f"Hội thoại {conversation_id} đang ở chế độ HUMAN. Bỏ qua RAG Pipeline.")
                    yield f"event: notice\ndata: {json.dumps({'message': 'Nhân viên tư vấn đang tiếp nhận cuộc trò chuyện.'}, ensure_ascii=False)}\n\n"
                    return

                # Lưu tin nhắn của khách hàng vào CSDL
                user_msg = Message(
                    conversation_id=conv.id,
                    sender_type="CUSTOMER",
                    content=user_message
                )
                db.add(user_msg)
                conv.updated_at = datetime.now(timezone.utc)
                db.commit()

                # Lấy tin nhắn gần nhất và lọc bỏ các thông báo lỗi hệ thống
                recent_msgs = db.query(Message).filter(
                    Message.conversation_id == conversation_id
                ).order_by(Message.created_at.desc()).limit(12).all()
                
                raw_history = []
                for m in reversed(recent_msgs):
                    if not m.content or not m.content.strip():
                        continue
                    # Lọc bỏ tin nhắn lỗi hệ thống cũ để tránh gây nhiễu Prompt LLM
                    if "Xin lỗi, hệ thống gặp sự cố khi tổng hợp" in m.content:
                        continue
                    role = "user" if m.sender_type == "CUSTOMER" else "assistant"
                    raw_history.append({"role": role, "content": m.content})

                # KH-06 Windowing: Giữ tối đa 6 tin nhắn sạch gần nhất
                chat_history = raw_history[-6:]
        finally:
            db.close()


        # BƯỚC 1: Query Decomposition & Per-subquery Intent Routing
        decomposer_output = await decomposer_service.decompose(
            query=user_message,
            chat_history=chat_history
        )
        standalone_query = decomposer_output.standalone_query

        # BƯỚC 1.5: Incident Evaluation & Guardrail (UC 2.1 & 2.2)
        sentiment_score = decomposer_output.sentiment_score
        llm_urgency = decomposer_output.urgency_level
        final_priority = None

        # Lấy Dynamic Config từ Cache/DB
        alert_config = self._get_alert_config()
        p1_thresh = alert_config["p1_threshold"]
        p2_thresh = alert_config["p2_threshold"]

        # Guardrail an toàn
        sentiment_label = "NEUTRAL"
        if sentiment_score <= p1_thresh:
            final_priority = "P1"
            sentiment_label = "CRITICAL"
        elif sentiment_score <= p2_thresh:
            final_priority = "P2"
            sentiment_label = "NEGATIVE"
        else:
            final_priority = llm_urgency  # Có thể là P1/P2/P3 hoặc None
            if sentiment_score < -0.29:
                sentiment_label = "NEGATIVE"
            elif sentiment_score > 0.29:
                sentiment_label = "POSITIVE"

        # Cập nhật Sticky Red Flag & Lưu điểm vào CSDL
        db: Session = SessionLocal()
        try:
            conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conv:
                if final_priority in ["P1", "P2"] or sentiment_score <= p2_thresh:
                    conv.is_flagged = True
                conv.last_sentiment = sentiment_label
                
                user_msg_db = db.query(Message).filter(
                    Message.conversation_id == conversation_id,
                    Message.sender_type == "CUSTOMER"
                ).order_by(Message.created_at.desc()).first()
                if user_msg_db:
                    user_msg_db.sentiment_score = sentiment_score
                
                if final_priority in ["P1", "P2", "P3"]:
                    ticket, is_new = self._create_or_update_ticket(db, conv, final_priority, decomposer_output)
                    if is_new:
                        redis_client.lpush("queue:tickets:pending", str(ticket.id))
                db.commit()
        except Exception as e:
            logger.error(f"Lỗi cập nhật cờ đỏ và ticket: {e}")
            db.rollback()
        finally:
            db.close()

        # BƯỚC 1.6: Graceful Handover cho P1
        if final_priority == "P1":
            logger.info("Kích hoạt Graceful Handover cho P1 qua SSE Stream")
            apology_msg = "Mình rất xin lỗi về trải nghiệm này. Hệ thống đã đánh dấu yêu cầu khẩn cấp và nhân viên CSKH đang vào hỗ trợ bạn ngay lập tức."
            
            db: Session = SessionLocal()
            try:
                conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
                if conv:
                    conv.mode = "WAITING_HUMAN"
                    db.commit()
            except Exception as e:
                db.rollback()
            finally:
                db.close()
            
            # Tự stream thẳng qua SSE mà không gọi RAG/Synthesizer
            yield f"event: token\ndata: {json.dumps({'token': apology_msg}, ensure_ascii=False)}\n\n"
            self._save_bot_message_to_db(conversation_id, apology_msg, [])
            
            done_payload = json.dumps({
                "full_text": apology_msg,
                "citations": [],
                "standalone_query": standalone_query,
                "is_complex": False
            }, ensure_ascii=False)
            yield f"event: done\ndata: {done_payload}\n\n"
            logger.info(f"=== [HOÀN THÀNH RAG KH-06 PIPELINE (GRACEFUL HANDOVER)] ===")
            return

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

    def _create_or_update_ticket(self, db: Session, conv: Conversation, priority: str, output):
        """Khởi tạo hoặc cập nhật phiếu hỗ trợ (UC 2.2)."""
        existing_ticket = db.query(Ticket).filter(
            Ticket.conversation_id == conv.id,
            Ticket.status.in_(["PENDING", "IN_PROGRESS"])
        ).first()

        summary = output.incident_summary or "Cần kiểm tra thủ công - Lỗi trích xuất"
        category = output.incident_category or "Vấn đề khác"
        sla_minutes = {"P1": 15, "P2": 60, "P3": 240}.get(priority, 240)

        if existing_ticket:
            p_rank = {"P1": 1, "P2": 2, "P3": 3}
            if p_rank.get(priority, 3) < p_rank.get(existing_ticket.priority, 3):
                existing_ticket.priority = priority
                existing_ticket.sla_deadline = datetime.now(timezone.utc) + timedelta(minutes=sla_minutes)
            
            existing_ticket.summary += f"\n[Update]: {summary}"
            return existing_ticket, False
        else:
            new_ticket = Ticket(
                conversation_id=conv.id,
                category=category,
                priority=priority,
                summary=summary,
                sla_deadline=datetime.now(timezone.utc) + timedelta(minutes=sla_minutes),
                ai_metadata={"sentiment_score": float(output.sentiment_score)}
            )
            db.add(new_ticket)
            db.flush()
            return new_ticket, True

    def _get_alert_config(self) -> Dict[str, Any]:
        """Lấy cấu hình cảnh báo từ Redis (ưu tiên) hoặc DB."""
        try:
            cached = redis_client.hgetall("cache:alert_rules")
            if cached and "p1_threshold" in cached:
                return {
                    "p1_threshold": float(cached["p1_threshold"]),
                    "p2_threshold": float(cached["p2_threshold"]),
                    "instruction_prompt": cached.get("instruction_prompt", "")
                }
        except Exception as e:
            logger.error(f"Redis cache lỗi: {e}")
            
        db: Session = SessionLocal()
        try:
            rule = db.query(AIRule).first()
            p1_thresh = float(rule.p1_threshold) if rule else -0.60
            p2_thresh = float(rule.p2_threshold) if rule else -0.30
            instruction = rule.instruction_prompt if rule else ""
            
            try:
                redis_client.hset("cache:alert_rules", mapping={
                    "p1_threshold": str(p1_thresh),
                    "p2_threshold": str(p2_thresh),
                    "instruction_prompt": instruction
                })
                # Cache 1 tiếng nếu cần
                redis_client.expire("cache:alert_rules", 3600)
            except:
                pass
                
            return {"p1_threshold": p1_thresh, "p2_threshold": p2_thresh, "instruction_prompt": instruction}
        finally:
            db.close()

rag_pipeline_service = RAGPipelineService()
