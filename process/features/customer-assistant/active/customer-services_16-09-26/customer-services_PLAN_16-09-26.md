# Kế hoạch Kỹ thuật: Backend Service APIs cho Khối 1 (Trợ lý Tra cứu Thông tin Khách hàng)

> **TL;DR:** Xây dựng toàn bộ các Service API backend còn thiếu cho **Khối 1: Trợ lý Tra cứu Thông tin Khách hàng** bao gồm Quản lý Tài khoản Khách hàng (Use Case 1.1: Đăng ký, Đăng nhập JWT, Brute-force lockout), Quản lý Phiên trò chuyện (Use Case 1.2: Danh sách phiên, Tạo phiên kèm lời chào bot, Lịch sử 50 tin nhắn lazy loading, Đóng phiên), và Tích hợp kiểm soát phiên cho Tra cứu RAG Chatbot Streaming (Use Case 1.3).

---

## 1. 🎯 Mục tiêu & Phạm vi (Goals & Scope)

### 1.1. Mục tiêu Cốt lõi
* Hiện thực hóa đầy đủ các nghiệp vụ của **Khối 1** theo đặc tả tại [`docs/overview/phantichhethong.md`](file:///d:/Study/TLU/kiemthu/project/docs/overview/phantichhethong.md) và [`docs/overview/usecase.md`](file:///d:/Study/TLU/kiemthu/project/docs/overview/usecase.md) (UC 1.1, UC 1.2, UC 1.3).
* Cung cấp bộ RESTful API chuẩn mực cho Client UI (Frontend React của Khách hàng):
  * **Auth Khách hàng (UC 1.1)**: Đăng ký tài khoản mới, Đăng nhập an toàn nhận JWT access token, Lấy profile (`/auth/customer/me`), bảo vệ tài khoản khi sai mật khẩu 5 lần liên tiếp (khóa tạm 15 phút).
  * **Quản lý Phiên chat (UC 1.2)**: Xem danh sách các cuộc trò chuyện trước đây kèm tóm tắt tin nhắn cuối, Mở cuộc trò chuyện mới (tự động tạo bản ghi CSDL và gửi câu chào mừng mặc định), Tải lịch sử 50 tin nhắn (Lazy Loading) kèm trích dẫn `citations`, Đóng phiên chat (`mode = 'CLOSED'`).
  * **Tích hợp RAG Chatbot (UC 1.3)**: Kiểm soát trạng thái phiên chat (`CLOSED` / `WAITING_HUMAN` / `BOT`) và xác thực khách hàng khi gọi luồng SSE Streaming `POST /api/chat/stream`.

### 1.2. Ngoài phạm vi (Out of Scope)
* Nghiệp vụ của Nhân viên CSKH & Quản lý (Khối 3: Live Support Console, Quản lý tài khoản nhân sự).
* Nghiệp vụ AI Auto-Triage & Mở Ticket khẩn cấp (Khối 2) và SLA Engine / Dispatcher (Khối 4).

---

## 2. 🏗️ Kiến trúc Kỹ thuật & Luồng Dữ liệu (Architecture & Data Flow)

### 2.1. Sơ đồ Luồng Dữ liệu Khối 1
```text
[Khách hàng (Client UI)]
       │
       ├── 1. POST /api/auth/customer/register hoặc /login ──► [customer_auth_service] ──► [bảng customers]
       │   ◄── Nhận JWT Access Token (customer_id) ────────────┘
       │
       ├── 2. GET /api/conversations ────────────────────────► [conversation_service] ──► [bảng conversations & messages]
       │   ◄── Danh sách phiên & tóm tắt tin nhắn cuối ───────┘
       │
       ├── 3. POST /api/conversations (Tạo phiên mới) ────────► [conversation_service] ──► [INSERT conversation (BOT)]
       │   ◄── Phiên mới + Tin nhắn chào mặc định của Bot ─────┘                      └──► [INSERT message (BOT chào)]
       │
       ├── 4. GET /api/conversations/{id}/messages (Lazy Load) ► [conversation_service] ──► [SELECT 50 messages]
       │   ◄── Lịch sử tin nhắn + citations ──────────────────┘
       │
       └── 5. POST /api/chat/stream (Hỏi đáp RAG) ────────────► [RAGPipelineService] ───► [SQL + pgvector HNSW]
           ◄── SSE Token Stream (text/event-stream) ──────────┘
```

---

## 3. 📂 Touchpoints (Danh sách Tệp Tác động)

### 3.1. Các Tệp Tạo mới
* `code/backend/app/core/security.py`: Module mã hóa mật khẩu (`hashlib`/`bcrypt`), sinh/giải mã JWT token, kiểm soát brute-force lockout 15 phút.
* `code/backend/app/schemas/customer.py`: Pydantic Schemas (`CustomerRegisterRequest`, `CustomerLoginRequest`, `CustomerResponse`, `TokenResponse`).
* `code/backend/app/schemas/conversation.py`: Pydantic Schemas (`ConversationCreateRequest`, `ConversationResponse`, `ConversationListItemSchema`, `MessageItemSchema`, `ConversationMessagesListResponse`).
* `code/backend/app/services/customer_auth_service.py`: Service xử lý logic đăng ký, đăng nhập, xác thực và kiểm soát brute force.
* `code/backend/app/services/conversation_service.py`: Service quản lý phiên trò chuyện, tin nhắn chào mừng, lazy loading lịch sử tin nhắn và đóng phiên.
* `code/backend/app/api/v1/endpoints/customer_auth.py`: Router các API Auth khách hàng (`/api/auth/customer/*`).
* `code/backend/app/api/v1/endpoints/conversation.py`: Router các API Quản lý phiên chat (`/api/conversations/*`).
* `code/backend/tests/test_customer_auth.py`: Bộ kiểm thử tự động cho Use Case 1.1.
* `code/backend/tests/test_conversation.py`: Bộ kiểm thử tự động cho Use Case 1.2.

### 3.2. Các Tệp Cập nhật
* `code/backend/app/core/config.py`: Bổ sung `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`.
* `code/backend/app/api/deps.py`: Bổ sung dependency `get_current_customer` và `get_optional_current_customer`.
* `code/backend/app/schemas/__init__.py`: Export các schemas mới.
* `code/backend/app/api/v1/api.py`: Đăng ký `customer_auth.py` và `conversation.py` vào `api_router`.
* `code/backend/app/api/v1/endpoints/chat.py`: Kiểm tra phiên `mode == 'CLOSED'` và tích hợp thông báo giữ chỗ khi `WAITING_HUMAN`.
* `code/backend/tests/run_tests.py`: Gom các test suites mới vào runner tự động.

---

## 4. 📜 Public Contracts (Giao diện & Schemas)

### 4.1. Schemas Request & Response (`app/schemas/customer.py`)
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class CustomerRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = Field(None, pattern=r"^0\d{9}$")

class CustomerLoginRequest(BaseModel):
    email: EmailStr
    password: str

class CustomerResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    customer: CustomerResponse
```

### 4.2. Schemas Request & Response (`app/schemas/conversation.py`)
```python
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime
from uuid import UUID

class MessageItemSchema(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_type: str
    content: str
    citations: Optional[List[Dict[str, Any]]] = None
    sentiment_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationListItemSchema(BaseModel):
    id: UUID
    mode: str
    is_flagged: bool
    last_sentiment: Optional[str] = None
    last_message_content: Optional[str] = None
    last_message_time: Optional[datetime] = None
    updated_at: datetime

    class Config:
        from_attributes = True

class ConversationMessagesListResponse(BaseModel):
    conversation_id: UUID
    mode: str
    is_flagged: bool
    messages: List[MessageItemSchema]
    total: int
    has_more: bool
```

### 4.3. RESTful API Endpoints Chi Tiết
* `POST /api/auth/customer/register`: Đăng ký tài khoản khách hàng mới.
* `POST /api/auth/customer/login`: Đăng nhập, trả về JWT access token.
* `GET /api/auth/customer/me`: Lấy thông tin tài khoản hiện tại (Header `Authorization: Bearer <token>`).
* `GET /api/conversations`: Lấy danh sách lịch sử các phiên chat của khách hàng hiện tại.
* `POST /api/conversations`: Mở phiên chat mới (tự động nhận tin chào mừng của Bot).
* `GET /api/conversations/{id}`: Xem chi tiết trạng thái phiên chat.
* `GET /api/conversations/{id}/messages`: Lấy lịch sử tin nhắn (hỗ trợ `limit=50` lazy loading).
* `POST /api/conversations/{id}/close`: Đóng phiên trò chuyện.

---

## 5. 💥 Blast Radius (Phạm vi Ảnh hưởng)

* **Packages**: `code/backend/app/core/`, `code/backend/app/schemas/`, `code/backend/app/services/`, `code/backend/app/api/v1/`, `code/backend/tests/`.
* **Risk Class**: **Thấp (Low)**.
* **Compatibility**: Không làm thay đổi cấu trúc bảng CSDL hiện hữu (10 models đã khớp 100%), không gây xung đột với module RAG Assistant.

---

## 6. 📝 Implementation Checklist

1. [ ] Cập nhật cấu hình JWT trong `code/backend/app/core/config.py`.
2. [ ] Tạo module bảo mật & mật khẩu trong `code/backend/app/core/security.py`.
3. [ ] Cập nhật `code/backend/app/api/deps.py` với `get_current_customer`.
4. [ ] Tạo `code/backend/app/schemas/customer.py` và `code/backend/app/schemas/conversation.py`.
5. [ ] Cập nhật `code/backend/app/schemas/__init__.py`.
6. [ ] Tạo dịch vụ `code/backend/app/services/customer_auth_service.py`.
7. [ ] Tạo dịch vụ `code/backend/app/services/conversation_service.py`.
8. [ ] Xây dựng router `code/backend/app/api/v1/endpoints/customer_auth.py`.
9. [ ] Xây dựng router `code/backend/app/api/v1/endpoints/conversation.py`.
10. [ ] Cập nhật `code/backend/app/api/v1/endpoints/chat.py` kiểm tra `mode == 'CLOSED'`.
11. [ ] Đăng ký các router mới vào `code/backend/app/api/v1/api.py`.
12. [ ] Viết bộ kiểm thử `code/backend/tests/test_customer_auth.py`.
13. [ ] Viết bộ kiểm thử `code/backend/tests/test_conversation.py`.
14. [ ] Cập nhật `code/backend/tests/run_tests.py` và xác nhận tất cả test suites đều PASS.

---

## 7. 🎯 Acceptance Criteria (Tiêu Chuẩn Nghiệm Thu Kỹ Thuật)

* **SPEC-1.1 (Customer Register)**: Đăng ký thành công với thông tin hợp lệ; chặn email trùng (E-4), mật khẩu ngắn/không có chữ số (E-2). `proven by:` `test_customer_register`, `strategy:` `Fully-Automated`.
* **SPEC-1.2 (Customer Login & Lockout)**: Đăng nhập thành công trả về JWT token; đăng nhập sai 5 lần liên tiếp trong 15 phút sẽ tạm khóa tài khoản (E-6, E-7). `proven by:` `test_customer_login_lockout`, `strategy:` `Fully-Automated`.
* **SPEC-1.3 (Customer Profile)**: Endpoint `/auth/customer/me` trả về đúng thông tin định danh khách hàng khi có Bearer token. `proven by:` `test_customer_me`, `strategy:` `Fully-Automated`.
* **SPEC-1.4 (Create Conversation)**: Bắt đầu phiên chat mới tạo bản ghi `Conversation` và tự động tạo tin nhắn chào đầu tiên của Bot. `proven by:` `test_create_conversation`, `strategy:` `Fully-Automated`.
* **SPEC-1.5 (Conversation List)**: Lấy danh sách phiên chat trả về đầy đủ tóm tắt tin nhắn cuối, nhãn trạng thái và thời gian cập nhật. `proven by:` `test_get_conversations_list`, `strategy:` `Fully-Automated`.
* **SPEC-1.6 (Lazy Loading Messages)**: Lấy lịch sử tin nhắn trả về tối đa 50 tin nhắn gần nhất kèm metadata trích dẫn `citations`. `proven by:` `test_get_messages_lazy_loading`, `strategy:` `Fully-Automated`.
* **SPEC-1.7 (Close Conversation)**: Đóng phiên chat cập nhật `mode = 'CLOSED'`; chặn chat vào phiên đã đóng. `proven by:` `test_closed_conversation_chat`, `strategy:` `Fully-Automated`.
* **SPEC-1.8 (RAG Stream Integration)**: Endpoint `POST /api/chat/stream` tiếp tục stream token-by-token mượt mà trên các phiên `mode = 'BOT'`. `proven by:` `test_rag_stream`, `strategy:` `Fully-Automated`.

---

## 8. 🔍 Verification Evidence

| Gate / Scenario | Strategy | Proves SPEC Criterion |
| :--- | :--- | :--- |
| `tests/test_customer_auth.py::test_register_and_validations` | Fully-Automated | SPEC-1.1 |
| `tests/test_customer_auth.py::test_login_and_brute_force_lockout` | Fully-Automated | SPEC-1.2 |
| `tests/test_customer_auth.py::test_get_customer_profile_me` | Fully-Automated | SPEC-1.3 |
| `tests/test_conversation.py::test_create_conversation_auto_greeting` | Fully-Automated | SPEC-1.4 |
| `tests/test_conversation.py::test_list_conversations_with_snippets` | Fully-Automated | SPEC-1.5 |
| `tests/test_conversation.py::test_lazy_load_messages_and_citations` | Fully-Automated | SPEC-1.6 |
| `tests/test_conversation.py::test_close_conversation_and_block_chat` | Fully-Automated | SPEC-1.7 |
| `tests/test_rag_pipeline.py::test_e2e_rag_pipeline` | Fully-Automated | SPEC-1.8 |

---

## 9. 🛡️ Test Infra Improvement Notes
(none identified yet)

---

## 10. 🔄 Resume and Execution Handoff
* **Tệp Kế Hoạch**: `process/features/customer-assistant/active/customer-services_16-09-26/customer-services_PLAN_16-09-26.md`
* **Trạng thái**: Đã nghiệm thu Validate Contract (Gate: PASS), sẵn sàng thực thi (EXECUTE).

---

## Validate Contract

Status: PASS
Date: 16-09-26
date: 2026-09-16
generated-by: outer-pvl

Parallel strategy: sequential
Rationale: 7/7 signals favor sequential execution due to clear layered dependency chain (Security -> Schemas -> Services -> Endpoints -> Tests).

Test gates:

| criterion id | behavior | strategy | proving test | gap-resolution |
|---|---|---|---|---|
| SPEC-1.1 | Customer Registration with Email/Password validation | Fully-Automated | `tests/test_customer_auth.py::test_register_and_validations` | B |
| SPEC-1.2 | Customer Login & 15-min Brute Force Lockout | Fully-Automated | `tests/test_customer_auth.py::test_login_and_brute_force_lockout` | B |
| SPEC-1.3 | Customer Profile /me with Bearer JWT | Fully-Automated | `tests/test_customer_auth.py::test_get_customer_profile_me` | B |
| SPEC-1.4 | Create Conversation with Auto Greeting Message | Fully-Automated | `tests/test_conversation.py::test_create_conversation_auto_greeting` | B |
| SPEC-1.5 | Conversation List with Latest Message Snippet | Fully-Automated | `tests/test_conversation.py::test_list_conversations_with_snippets` | B |
| SPEC-1.6 | Lazy Loading Messages (50 items) & Citations | Fully-Automated | `tests/test_conversation.py::test_lazy_load_messages_and_citations` | B |
| SPEC-1.7 | Close Conversation & Block New Messages | Fully-Automated | `tests/test_conversation.py::test_close_conversation_and_block_chat` | B |
| SPEC-1.8 | RAG Chat Stream Integration with Conversation Status | Fully-Automated | `tests/test_rag_pipeline.py::test_e2e_rag_pipeline` | A |

Legacy line form:
- auth: [Fully-automated: python tests/test_customer_auth.py]
- conversation: [Fully-automated: python tests/test_conversation.py]
- rag_stream: [Fully-automated: python tests/test_rag_pipeline.py]

Dimension findings:
- Infra fit: PASS — Cấu trúc Layered Architecture chuẩn mực của FastAPI (`core/`, `schemas/`, `services/`, `api/v1/endpoints/`), hoàn toàn tương thích với ORM SQLAlchemy và CSDL Supabase PostgreSQL.
- Test coverage: PASS — Bao phủ 100% các tiêu chí SPEC cho Use Case 1.1, 1.2, 1.3 với các bài test tự động cho cả Auth, Quản lý phiên và RAG stream.
- Breaking changes: PASS — Bổ sung API endpoints mới (Additive), không làm thay đổi các bảng CSDL hay các API hiện có.
- Security surface: PASS — Mã hóa mật khẩu bằng thuật toán an toàn, JWT HS256 có hạn sử dụng, cơ chế chống dò mật khẩu (5 lần sai -> khóa 15p), cách ly dữ liệu giữa các khách hàng.

Open gaps: none

What this coverage does NOT prove:
- Giao diện UI React frontend thực tế (sẽ được kiểm thử khi phát triển frontend).
- Khả năng chịu tải đồng thời hàng nghìn kết nối (sẽ kiểm thử trong performance benchmark).

Gate: PASS
Accepted by: user (requested validation)

## Autonomous Goal Block

TARGET: Triển khai hoàn chỉnh toàn bộ Backend Services & APIs cho Khối 1 (Trợ lý Tra cứu Khách hàng) theo checklist trong customer-services_PLAN_16-09-26.md.
PER-PHASE LOOP: Research -> Innovate -> Plan -> Validate -> Execute -> Review
HARD STOPS: Không sửa đổi cấu trúc CSDL của các khối khác; dừng lại nếu kiểm thử thất bại.
SAFETY: Toàn bộ mật khẩu phải được băm an toàn; access token phải được xác thực chặt chẽ.
TEST GATES: automated
VALIDATE CONTRACT: customer-services_PLAN_16-09-26.md
START: Step 1 of Implementation Checklist

