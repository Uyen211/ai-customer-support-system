# 🚀 Omnichannel Support Backend (FastAPI Services)

> Backend Server phục vụ Hệ thống Trợ lý Trực ca CSKH AI & Giám sát Vận hành Tự động, tích hợp RAG Chatbot KH-06 (Google Gemini + Supabase pgvector HNSW), AI Auto-Triage, Live Console Gateway & SLA Engine.

---

## 📁 Cấu trúc Thư mục Codebase Chuẩn mực

Toàn bộ backend đã được tổ chức lại theo mô hình **Layered Architecture** chuẩn mực của FastAPI:

```text
code/backend/
├── app/
│   ├── api/                           # Tầng Routing (Giao tiếp API với Frontend)
│   │   ├── deps.py                    # Dependency injections (get_db, verify_jwt...)
│   │   └── v1/
│   │       ├── api.py                 # Router trung tâm gom tất cả sub-routers v1
│   │       └── endpoints/
│   │           └── chat.py            # UC 1.2, UC 1.3: Quản lý hội thoại & SSE Stream (/api/chat/stream)
│   │
│   ├── core/                          # Tầng Cấu hình & Client cốt lõi
│   │   ├── config.py                  # Pydantic BaseSettings đọc biến môi trường .env
│   │   ├── llm.py                     # Client Google Gemini API (JSON Mode & SSE Token Stream)
│   │   └── redis.py                   # Client kết nối Redis (Queue, Pub/Sub, Cache)
│   │
│   ├── db/                            # Tầng Cơ sở dữ liệu (Supabase PostgreSQL + pgvector)
│   │   ├── base_class.py              # DeclarativeBase của SQLAlchemy
│   │   ├── session.py                 # Engine, SessionLocal factory và get_db dependency
│   │   └── base.py                    # Import Base và toàn bộ 10 ORM Models
│   │
│   ├── models/                        # Định nghĩa 10 Bảng ORM riêng biệt (SQLAlchemy)
│   │   ├── __init__.py                # Export tất cả models
│   │   ├── user.py                    # Bảng users (Nhân viên CSKH & Admin)
│   │   ├── customer.py                # Bảng customers (Khách hàng)
│   │   ├── conversation.py            # Bảng conversations (Phiên chat)
│   │   ├── message.py                 # Bảng messages (Lịch sử tin nhắn & citations)
│   │   ├── ticket.py                  # Bảng tickets (Phiếu yêu cầu CSKH)
│   │   ├── sla_policy.py              # Bảng sla_policies (Chính sách cam kết SLA)
│   │   ├── canned_response.py         # Bảng canned_responses (Câu trả lời mẫu)
│   │   ├── ai_rule.py                 # Bảng ai_rules (Luật phân loại cảm xúc & ticket)
│   │   ├── product.py                 # Bảng products (Sản phẩm, giá, tồn kho, JSONB attributes)
│   │   └── knowledge_chunk.py         # Bảng knowledge_chunks (Tri thức vector pgvector 768 chiều)
│   │
│   ├── schemas/                       # Pydantic Schemas (Request/Response DTOs)
│   │   ├── __init__.py                # Export schemas
│   │   └── rag.py                     # DTOs: SubQueryItem, DecomposerOutput, Citations, ChatStreamRequest
│   │
│   ├── services/                      # Tầng Nghiệp vụ cốt lõi (Business Logic Layer)
│   │   └── rag/                       # Bộ máy RAG Assistant (Kiến trúc KH-06 Nâng cấp)
│   │       ├── __init__.py            # Export RAG services
│   │       ├── prompts.py             # Tập Prompts LLM (Domain Scope, Sub-query Intent, JSONB attrs)
│   │       ├── embedder.py            # VietnameseEmbedder 768 chiều & token trim safety check
│   │       ├── decomposer.py          # QueryDecomposerService (bẻ câu hỏi & Intent router)
│   │       ├── retrievers.py          # SQLProductRetriever (JSONB), VectorKnowledgeRetriever (HNSW), OutOfDomainHandler
│   │       ├── synthesizer.py         # MultiContextSynthesizerService (Gom & Stream token)
│   │       └── pipeline.py            # RAGPipelineService (Nhạc trưởng điều phối 5 bước)
│   │
│   ├── websocket/                     # Tầng kết nối thời gian thực 2 chiều
│   │   ├── __init__.py
│   │   └── connection_manager.py      # Quản lý connection pools, rooms theo conversation/agent
│   │
│   ├── workers/                       # Tiến trình chạy ngầm bất đồng bộ (Background Tasks)
│   │   ├── __init__.py
│   │   ├── ticket_dispatcher_worker.py# Lắng nghe Redis Queue (queue:tickets:pending)
│   │   └── sla_monitor_worker.py      # Cron job quét vi phạm hạn SLA mỗi 30s, bắn Redis Pub/Sub
│   │
│   └── main.py                        # Điểm khởi chạy ứng dụng FastAPI (CORS, Middlewares, Routes)
│
├── tests/                             # Thư mục kiểm thử & Phòng thí nghiệm (RAG Lab)
│   ├── run_tests.py                   # Test runner tự động (unittest)
│   ├── test_rag_pipeline.py           # Bộ kiểm thử RAG Pipeline KH-06
│   ├── rag_lab/                       # Nơi chứa mã chạy thử nghiệm benchmark KH-01 -> KH-08
│   └── unit/                          # Thư mục chứa Unit tests bổ sung
│
├── Dockerfile                         # Container đóng gói cs_backend
└── requirements.txt                   # Danh sách thư viện cần thiết
```

---

## 📖 Bảng Chi tiết Vai trò Từng Thư mục & Tệp Hiện hữu

### 1. Thư mục `app/`

| Đường dẫn tệp / Thư mục | Vai trò & Chức năng Kỹ thuật |
| --- | --- |
| `app/main.py` | **Cổng vào FastAPI App**: Nạp cấu hình CORS, khởi tạo kết nối & bảng CSDL, mount API Router `/api` và các endpoint `/`, `/health`. |
| `app/api/deps.py` | **Dependencies**: Cung cấp hàm phụ thuộc DB Session (`get_db`) và xác thực người dùng cho các API endpoints. |
| `app/api/v1/api.py` | **Router trung tâm v1**: Gom các router nhánh (chat, auth, agent, tickets...) vào một router duy nhất. |
| `app/api/v1/endpoints/chat.py` | **Chat API**: Cung cấp endpoint SSE Streaming `POST /api/chat/stream` và kiểm tra sức khỏe `GET /api/chat/health`. |
| `app/core/config.py` | **Cấu hình toàn cục**: Đọc và kiểm tra các biến môi trường từ `.env` (DSN Supabase, Gemini Key, Embedding Model...). |
| `app/core/llm.py` | **LLM Service Client**: Client giao tiếp Google Gemini API qua SDK `google.genai`, hỗ trợ JSON Mode, Token Stream và Fallback an toàn. |
| `app/core/redis.py` | **Redis Client**: Kết nối Redis phục vụ hàng đợi tác vụ, Pub/Sub thông báo và Caching. |
| `app/db/base_class.py` | **SQLAlchemy DeclarativeBase**: Khởi tạo lớp `Base` gốc cho tất cả ORM models. |
| `app/db/session.py` | **Database Session**: Khởi tạo SQLAlchemy Engine, SessionLocal factory và `get_db()`. |
| `app/db/base.py` | **Base Aggregator**: Import `Base` và toàn bộ 10 models giúp Alembic và FastAPI nhận diện metadata CSDL. |
| `app/models/` | **10 Bảng CSDL (ORM)**: Mỗi bảng được tách riêng thành 1 file độc lập (`user.py`, `customer.py`, `conversation.py`, `message.py`, `ticket.py`, `sla_policy.py`, `canned_response.py`, `ai_rule.py`, `product.py` hỗ trợ JSONB attributes, `knowledge_chunk.py` hỗ trợ pgvector 768 chiều). |
| `app/schemas/rag.py` | **Pydantic DTOs**: Khai báo các schemas: `SubQueryItem` (với các trường trích xuất `brand`, `size`, `weight_volume`, `price_max/min`, `in_stock_only`), `DecomposerOutputSchema`, `CitationItem`, `AggregatedContext`, `ChatStreamRequest`. |
| `app/services/rag/prompts.py` | **Tập Prompts RAG KH-06**: Prompt 1 (Decomposer + Phạm vi ranh giới + bóc tách JSONB) & Prompt 2 (Synthesizer đa ngữ cảnh). |
| `app/services/rag/embedder.py` | **Vector Embedding**: Sinh vector 768 chiều cho văn bản với cơ chế cắt tỉa an toàn chống tràn token. |
| `app/services/rag/decomposer.py` | **Query Decomposer**: Giải quyết đại từ, bẻ câu hỏi phức hợp thành các sub-queries nguyên tử và phân loại Intent. |
| `app/services/rag/retrievers.py` | **Bộ 3 Workers Tra cứu Song song**: <br>- `SQLProductRetriever`: Tra cứu giá, tồn kho, lọc theo trường JSONB `attributes`.<br>- `VectorKnowledgeRetriever`: Truy vấn vector HNSW trên Supabase pgvector.<br>- `OutOfDomainHandler`: Phản hồi ngoài phạm vi & đề xuất kết nối CSKH. |
| `app/services/rag/synthesizer.py` | **Synthesizer Service**: Gom ngữ cảnh từ các workers, gọi LLM tổng hợp và sinh stream câu trả lời token-by-token. |
| `app/services/rag/pipeline.py` | **Pipeline Orchestrator**: Điều phối toàn bộ luồng 5 bước RAG KH-06 và tự động lưu tin nhắn Bot + citations vào CSDL. |
| `app/websocket/connection_manager.py` | **WebSocket Manager**: Quản lý connection pools, rooms theo từng cuộc trò chuyện thời gian thực. |
| `app/workers/ticket_dispatcher_worker.py` | **Background Dispatcher**: Worker lắng nghe Redis Queue để tự động phân phối Ticket cho nhân viên. |
| `app/workers/sla_monitor_worker.py` | **Background SLA Monitor**: Cron job định kỳ mỗi 30s quét vi phạm thời hạn SLA và phát sự kiện qua Redis Pub/Sub. |

### 2. Thư mục `tests/`

| Đường dẫn tệp / Thư mục | Vai trò & Chức năng Kỹ thuật |
| --- | --- |
| `tests/run_tests.py` | Runner thực thi toàn bộ test suite bằng `unittest`, báo cáo kết quả chi tiết cho toàn bộ module. |
| `tests/test_rag_pipeline.py` | Bộ kiểm thử tự động toàn diện bao phủ 5 SPEC Criteria: Decomposer, SQL Product Lookup, pgvector HNSW, Out-of-Domain, và SSE Endpoint. |
| `tests/rag_lab/` | Thư mục phòng thí nghiệm dành cho việc chạy benchmark so sánh chất lượng giữa các kiến trúc RAG (KH-01 -> KH-08). |
| `tests/unit/` | Thư mục sẵn sàng để bổ sung các bài unit tests cô lập cho từng tầng API/Service mới. |

---

## 🛠️ Danh sách API Endpoints chính

### 1. RAG Chatbot Streaming (`POST /api/chat/stream`)
* **Header:** `Content-Type: application/json`, `Accept: text/event-stream`
* **Request Body:**
  ```json
  {
    "conversation_id": "10000000-0000-0000-0000-000000000001",
    "message": "Cát Cature giá bao nhiêu và phí ship thế nào?"
  }
  ```
* **Response SSE Stream:**
  ```text
  event: token
  data: {"token": "Chào bạn! "}

  event: token
  data: {"token": "PetHome xin báo giá cát Cature là 145.000đ..."}

  event: done
  data: {"full_text": "...", "citations": [...]}
  ```

### 2. RAG Module Health Check (`GET /api/chat/health`)
* **Response:**
  ```json
  {
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
  ```

---

## 💻 Hướng dẫn Khởi chạy & Kiểm thử

### 1. Khởi chạy Server Backend tại máy cục bộ (Dev Mode)
```bash
# Kích hoạt venv
venv\Scripts\activate

# Cài đặt thư viện (nếu có bổ sung)
pip install -r requirements.txt

# Khởi chạy Uvicorn Server
uvicorn app.main:app --reload --port 8000
```

- **Swagger UI API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 2. Chạy bộ Kiểm thử Tự động (Automated Test Suite)
```bash
python tests/run_tests.py
```
