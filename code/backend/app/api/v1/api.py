from fastapi import APIRouter
from app.api.v1.endpoints.chat import router as chat_router
from app.api.v1.endpoints.customer_auth import router as customer_auth_router
from app.api.v1.endpoints.conversation import router as conversation_router
from app.api.v1.endpoints.config import router as config_router

api_router = APIRouter()

# 1. Đăng ký Router Xác thực Khách hàng (Use Case 1.1)
api_router.include_router(customer_auth_router)

# 2. Đăng ký Router Quản lý Phiên trò chuyện (Use Case 1.2)
api_router.include_router(conversation_router)

# 3. Đăng ký Router RAG Chatbot Streaming (Use Case 1.3)
api_router.include_router(chat_router)

# 4. Đăng ký Router Cấu hình Hệ thống (Use Case 2.3)
api_router.include_router(config_router, prefix="/configs", tags=["configs"])
