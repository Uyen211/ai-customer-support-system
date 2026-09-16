from fastapi import APIRouter
from app.api.v1.endpoints.chat import router as chat_router

api_router = APIRouter()

# Đăng ký Router chat (prefix: /chat -> URL: /api/v1/chat/stream hoặc /api/chat/stream tùy prefix mount)
api_router.include_router(chat_router)
