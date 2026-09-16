"""
API Router cho RAG Assistant (Kiến trúc KH-06 Nâng cấp).
Cung cấp Endpoint SSE Streaming `/api/chat/stream` và Endpoint `/api/chat/message`.
"""

import json
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.rag_assistant.schemas import ChatStreamRequest, ChatMessageResponse
from app.modules.rag_assistant.pipeline import rag_pipeline_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["RAG Chatbot Assistant"])

@router.post("/stream")
async def chat_stream_endpoint(request: ChatStreamRequest):
    """
    Endpoint Streaming phản hồi RAG theo chuẩn Server-Sent Events (SSE).
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Nội dung câu hỏi không được để trống.")

    async def sse_event_generator():
        try:
            async for chunk in rag_pipeline_service.stream_chat_pipeline(
                conversation_id=request.conversation_id,
                user_message=request.message.strip()
            ):
                event_type = chunk.get("event", "message")
                data_json = json.dumps(chunk.get("data", {}), ensure_ascii=False)
                yield f"event: {event_type}\ndata: {data_json}\n\n"
        except Exception as e:
            logger.error(f"Lỗi trong quá trình SSE stream: {e}")
            err_data = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"event: error\ndata: {err_data}\n\n"

    return StreamingResponse(
        sse_event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.get("/health")
def rag_health_check():
    return {
        "status": "online",
        "module": "RAG Assistant KH-06",
        "features": [
            "Sub-query Decomposition",
            "Per-subquery Intent Router",
            "Parallel SQL + pgvector HNSW Retrieval",
            "No Score Thresholding",
            "Out-of-Domain Graceful Fallback",
            "SSE Token Streaming"
        ]
    }
