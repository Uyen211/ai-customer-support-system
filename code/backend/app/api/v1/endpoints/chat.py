"""
FastAPI Router cho RAG Assistant (Kiến trúc KH-06 Nâng cấp).
Cung cấp Endpoint Streaming qua HTTP Server-Sent Events (SSE).
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.rag import ChatStreamRequest
from app.services.rag.pipeline import rag_pipeline_service

router = APIRouter(prefix="/chat", tags=["RAG Chatbot"])

@router.post("/stream", summary="Gửi tin nhắn và nhận phản hồi SSE Stream từ AI Bot")
async def chat_stream(request: ChatStreamRequest):
    """
    Endpoint nhận câu hỏi của khách hàng và stream kết quả tổng hợp token-by-token
    theo đúng chuẩn Server-Sent Events (SSE).
    """
    return StreamingResponse(
        rag_pipeline_service.execute_stream(
            conversation_id=request.conversation_id,
            user_message=request.message
        ),
        media_type="text/event-stream"
    )

@router.get("/health", summary="Kiểm tra trạng thái sẵn sàng của phân hệ RAG")
async def rag_health():
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
