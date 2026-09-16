code/backend/
├── app/
│   ├── api/                           # Tầng Routing (Giao tiếp với Frontend)
│   │   ├── deps.py                    # Dependencies (get_db, verify_jwt, get_current_user)
│   │   └── v1/
│   │       ├── api.py                 # Gom tất cả router v1
│   │       ├── endpoints/
│   │       │   ├── auth.py            # UC 1.1, UC 3.1: Đăng ký, đăng nhập Customer & Agent
│   │       │   ├── chat.py            # UC 1.2, UC 1.3: Quản lý hội thoại & SSE Stream (/chat/stream)
│   │       │   ├── agent.py           # UC 3.2, UC 3.3: Quản lý trạng thái trực, hàng đợi, tiếp quản
│   │       │   ├── tickets.py         # UC 4.3: Kanban board, cập nhật trạng thái phiếu
│   │       │   ├── canned_responses.py# UC 3.4: Mẫu phản hồi nhanh
│   │       │   ├── ai_rules.py        # UC 2.3: Cấu hình quy tắc cảm xúc & ticket
│   │       │   └── reports.py         # UC 4.4: Báo cáo phân tích hiệu suất, xuất Excel
│   │
│   ├── core/                          # Cấu hình cốt lõi dùng chung
│   │   ├── config.py                  # Pydantic BaseSettings (đọc từ code/.env)
│   │   ├── security.py                # Băm Bcrypt, sinh và xác thực JWT token
│   │   └── redis.py                   # Kết nối Redis Client (Queue, Pub/Sub, Cache)
│   │
│   ├── db/                            # Tầng Cơ sở dữ liệu (Supabase PostgreSQL + pgvector)
│   │   ├── session.py                 # Khởi tạo async_engine và async_sessionmaker
│   │   ├── base.py                    # Import Base và toàn bộ models để Alembic nhận diện
│   │   └── base_class.py              # DeclarativeBase của SQLAlchemy
│   │
│   ├── models/                        # Định nghĩa 10 Bảng dữ liệu CSDL (SQLAlchemy ORM)
│   │   ├── user.py                    # Bảng users
│   │   ├── customer.py                # Bảng customers
│   │   ├── conversation.py            # Bảng conversations
│   │   ├── message.py                 # Bảng messages
│   │   ├── ticket.py                  # Bảng tickets
│   │   ├── sla_policy.py              # Bảng sla_policies
│   │   ├── canned_response.py         # Bảng canned_responses
│   │   ├── ai_rule.py                 # Bảng ai_rules
│   │   ├── knowledge_chunk.py         # Bảng knowledge_chunks (sử dụng pgvector Vector(1024))
│   │   └── product.py                 # Bảng products
│   │
│   ├── schemas/                       # Pydantic Schemas (Request/Response validation)
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── ticket.py
│   │   ├── product.py
│   │   └── rag.py                     # Schema JSON cho Decomposer, Sub-queries, Citations
│   │
│   ├── services/                      # Nghiệp vụ logic chính (Business Logic Layer)
│   │   ├── auth_service.py            # Xử lý logic đăng nhập, xác thực
│   │   ├── rag/                       # Bộ máy RAG (Triển khai kiến trúc KH-06 Nâng cấp)
│   │
│   ├── websocket/                     # Tầng kết nối thời gian thực 2 chiều
│   │   ├── connection_manager.py      # Quản lý connection pools, rooms theo conversation/agent
│   │   └── endpoint.py                # WS endpoint: /ws/chat/{conversation_id}
│   │
│   └── workers/                       # Tiến trình chạy ngầm bất đồng bộ (Background Tasks)
│       ├── ticket_dispatcher_worker.py# Lắng nghe Redis Queue (queue:tickets:pending)
│       └── sla_monitor_worker.py      # Cron job quét vi phạm hạn SLA mỗi 30s, bắn Redis Pub/Sub
│
├── tests/                             # Thư mục kiểm thử & Phòng thí nghiệm (RAG Lab)
│   ├── rag_lab/                       # Nơi chứa mã chạy thử nghiệm KH-01 -> KH-08
│   │   ├── test_runner.py
│   │   └── testcases.json
│   └── unit/
│
├── Dockerfile                         # Container đóng gói cs_backend
├── requirements.txt                   # Danh sách thư viện cần thiết
└── main.py                            # Điểm khởi chạy ứng dụng FastAPI (lifespan, CORS, middlewares)