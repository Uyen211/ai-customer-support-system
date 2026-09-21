from fastapi import APIRouter
from app.api.v1.endpoints.chat import router as chat_router
from app.api.v1.endpoints.customer_auth import router as customer_auth_router
from app.api.v1.endpoints.conversation import router as conversation_router
from app.api.v1.endpoints.staff_auth import router as staff_auth_router
from app.api.v1.endpoints.staff import admin_router as staff_admin_router, agent_router as agent_router
from app.api.v1.endpoints.config import router as config_router
from app.api.v1.endpoints.tickets import router as tickets_router
from app.api.v1.endpoints.ws_alerts import router as ws_alerts_router

api_router = APIRouter()

# Đăng ký Router Tickets (Phân công công việc)
api_router.include_router(tickets_router)
api_router.include_router(ws_alerts_router)


# 1. Đăng ký Router Xác thực Khách hàng (Use Case 1.1)
api_router.include_router(customer_auth_router)

# 2. Đăng ký Router Quản lý Phiên trò chuyện (Use Case 1.2)
api_router.include_router(conversation_router)

# 3. Đăng ký Router RAG Chatbot Streaming (Use Case 1.3)
api_router.include_router(chat_router)

# 4. Đăng ký Router Tài khoản nhân viên & trạng thái làm việc (Use Case 3.1, 3.2)
api_router.include_router(staff_auth_router)
api_router.include_router(staff_admin_router)
api_router.include_router(agent_router)
# 4. Đăng ký Router Cấu hình Hệ thống (Use Case 2.3)
api_router.include_router(config_router, prefix="/configs", tags=["configs"])
