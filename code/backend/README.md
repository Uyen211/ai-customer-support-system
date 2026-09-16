# 🚀 Omnichannel Support Backend (FastAPI Services)

> Backend Server phục vụ Hệ thống Trợ lý Trực ca CSKH AI & Giám sát Vận hành Tự động, tích hợp RAG Chatbot KH-06 (Google Gemini + Supabase pgvector HNSW), AI Auto-Triage, Live Console Gateway & SLA Engine.

---

## 📁 Cấu trúc Thư mục Codebase & Mô tả Tệp

Hệ thống được tổ chức theo kiến trúc **Modular Monolith** sạch sẽ và dễ bảo trì:

```text
code/backend/
├── app/
│   ├── main.py                        # Tệp chạy chính FastAPI App (Khởi tạo server, CORS & đăng ký Routers)
│   ├── core/                          # Tầng Nền tảng & Cấu hình Hệ thống
│   │   ├── config.py                  # Đọc biến môi trường .env (DB DSN, API Key Gemini, Top-K, Model Name)
│   │   ├── database.py                # Kết nối CSDL SQLAlchemy ORM với Supabase PostgreSQL
│   │   └── llm.py                     # LLM Service Client kết nối Google Gemini API (Stream text & JSON Mode)
│   │
│   ├── common/                        # Tầng Mô hình CSDL Dùng chung giữa các Khối
│   │   ├── models.py                  # Khai báo ORM Tables: users, customers, conversations, messages, tickets, products, knowledge_chunks (pgvector 768)
│   │   └── websocket.py               # Connection Manager quản lý phòng chat WebSocket 2 chiều
│   │
│   └── modules/                       # Các Phân hệ Chức năng Kỹ thuật
│       └── rag_assistant/             # PHÂN HỆ RAG CHATBOT KH-06 NÂNG CẤP (KHỐI 1)
│           ├── __init__.py            # Khởi tạo Python Package
│           ├── prompts.py             # Tập 2 Prompts LLM (MERGED_DECOMPOSER_PROMPT chứa DOMAIN BOUNDARY SCOPE & MULTI_CONTEXT_SYNTHESIZER_PROMPT)
│           ├── schemas.py             # Các Pydantic DTOs (SubQueryItem, DecomposerOutputSchema, CitationItem, ChatStreamRequest)
│           ├── embedder.py            # Mô hình VietnameseEmbedder 768 chiều & kiểm tra an toàn token đầu vào (max_seq_length=256)
│           ├── decomposer.py          # QueryDecomposerService: Giải quyết đại từ, bẻ câu hỏi & phân nhãn Intent per sub-query
│           ├── retrievers.py          # Bộ 3 Workers Tra cứu Song song (SQLProductRetriever, VectorKnowledgeRetriever pgvector HNSW, OutOfDomainHandler)
│           ├── synthesizer.py         # MultiContextSynthesizerService: Gom ngữ cảnh đa nguồn & stream câu trả lời token-by-token
│           ├── pipeline.py            # RAGPipelineService: Orchestrator điều phối toàn trình 5 bước & lưu tin nhắn BOT + citations vào CSDL
│           └── router.py              # FastAPI Router cung cấp API Endpoints (/api/chat/stream, /api/chat/health)
│
├── tests/                             # Bộ Kiểm thử Tự động
│   ├── test_rag_pipeline.py           # Unit tests & Integration tests bao phủ 5 SPEC Criteria
│   └── run_tests.py                   # Script chạy test suite tự động bằng unittest runner
├── Dockerfile                         # Container build script
└── requirements.txt                   # Danh sách thư viện Python phụ thuộc
```

---

## 📖 Bảng Chi tiết Vai trò Từng Tệp (File Roles)

| Tệp (File) | Vai trò & Chức năng Kỹ thuật |
| --- | --- |
| `app/main.py` | **Cổng vào ứng dụng FastAPI**: Nạp cấu hình CORS, khởi tạo kết nối CSDL và nhúng Router `/api/chat` vào ứng dụng. |
| `app/core/config.py` | **Cấu hình toàn cục**: Đọc API Key từ tệp `.env`, định nghĩa tham số LLM Model (`gemini-2.5-flash-lite`), Embedding model (`dangvantuan/vietnamese-embedding`) và số lượng chunks `RAG_TOP_K`. |
| `app/core/database.py` | **Quản lý kết nối CSDL**: Khởi tạo SQLAlchemy Engine, Session pooling (`get_db()`) kết nối trực tiếp đến CSDL Supabase PostgreSQL. |
| `app/core/llm.py` | **Client giao tiếp LLM**: Sử dụng thư viện `google.genai` gọi Gemini sinh phản hồi dạng JSON cấu trúc (cho Decomposer) hoặc Stream văn bản token-by-token (cho Synthesizer), có sẵn chế độ Fallback an toàn khi mất mạng. |
| `app/common/models.py` | **Định nghĩa các Bảng CSDL (ORM)**: Chứa định nghĩa cấu trúc bảng `products` (kho hàng), `knowledge_chunks` (vector 768 chiều), `conversations`, `messages`, `tickets`, `users`, `customers`... |
| `app/common/websocket.py` | **Quản lý WebSocket**: Quản lý connection pool và kênh chat thời gian thực giữa nhân viên và khách hàng. |
| `app/modules/rag_assistant/prompts.py` | **Tập Prompt Kỹ thuật**: Chứa Prompt 1 bẻ câu hỏi tích hợp `# DOMAIN BOUNDARY SCOPE` và Prompt 2 tổng hợp đa ngữ cảnh. |
| `app/modules/rag_assistant/schemas.py` | **Chuẩn hóa Đầu vào/Đầu ra (DTOs)**: Định nghĩa các kiểu dữ liệu Pydantic đảm bảo dữ liệu truyền giữa các lớp không bị sai kiểu. |
| `app/modules/rag_assistant/embedder.py` | **Tạo Vector Embedding**: Nạp mô hình 768 chiều, kiểm tra cắt tỉa an toàn văn bản quá dài trước khi tokenize. |
| `app/modules/rag_assistant/decomposer.py` | **Bộ bẻ câu hỏi & Phân Intent**: Gọi LLM Prompt 1 để phân tích `user_query`, trả về danh sách `sub_queries` và Intent tương ứng. |
| `app/modules/rag_assistant/retrievers.py` | **Bộ 3 Workers Tra cứu Song song**: <br>- `SQLProductRetriever`: Lấy giá & tồn kho real-time.<br>- `VectorKnowledgeRetriever`: Search HNSW Cosine trên Supabase pgvector.<br>- `OutOfDomainHandler`: Tạo phản hồi ngoài phạm vi + mời CSKH. |
| `app/modules/rag_assistant/synthesizer.py` | **Bộ Tổng hợp & Stream**: Gom ngữ cảnh từ các workers, gọi LLM Prompt 2 để stream từng token câu trả lời về cho người dùng. |
| `app/modules/rag_assistant/pipeline.py` | **Nhạc trưởng Điều phối (Orchestrator)**: Kiểm tra trạng thái hội thoại (`mode`), chạy 5 bước RAG KH-06 và tự động lưu lịch sử tin nhắn BOT cùng trích dẫn `citations` vào CSDL. |
| `app/modules/rag_assistant/router.py` | **API Router**: Cung cấp API endpoint `/api/chat/stream` cho Frontend gọi qua HTTP SSE Response. |

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
# Khởi tạo venv nếu chưa có
python -m venv venv
venv\Scripts\activate

# Cài đặt thư viện
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
