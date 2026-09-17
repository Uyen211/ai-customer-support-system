# Kế hoạch Kỹ thuật: Module RAG Assistant Pipeline (Kiến trúc KH-06 Nâng cấp)

> **TL;DR:** Xây dựng toàn bộ module RAG Assistant (`code/backend/app/modules/rag_assistant/`) theo kiến trúc **KH-06 Nâng cấp** (Hybrid RAG + Sub-query Decomposition + Per-subquery Intent Router + Loại bỏ Score Thresholding), hỗ trợ streaming SSE token-by-token và tra cứu song song CSDL `products` (SQL) và `knowledge_chunks` (pgvector).

---

## 1. 🎯 Mục tiêu & Phạm vi (Goals & Scope)

### 1.1. Mục tiêu Cốt lõi
* Hiện thực hóa chính xác kiến trúc RAG đã được phê duyệt tại [`docs/overview/kh06_revised_architecture.md`](file:///d:/Study/TLU/kiemthu/project/docs/overview/kh06_revised_architecture.md).
* Bẻ câu hỏi phức tạp thành danh sách `sub_queries` nguyên tử với Intent và Target Source độc lập cho từng ý.
* Tra cứu song song bất đồng bộ (`asyncio.gather`):
  * CSDL Quan hệ `products` (SQL Parameterized Query trên PostgreSQL).
  * CSDL Vector `knowledge_chunks` (Cosine Similarity trên Supabase `pgvector` HNSW Index).
  * Nhánh `OUT_OF_DOMAIN` tự động sinh phản hồi Fallback lịch sự + gợi ý chuyển sang Nhân viên CSKH.
* Tổng hợp đa ngữ cảnh và sinh câu trả lời Streaming qua chuẩn **SSE (`text/event-stream`)** cho Client UI.

### 1.2. Ngoài phạm vi (Out of Scope)
* Giao diện UI React frontend (thuộc phase riêng của Khối 1).
* Xử lý WebSocket 2 chiều khi Human tiếp quản (thuộc Khối 3 - Live Support Console).

---

## 2. 🏗️ Kiến trúc Kỹ thuật & Luồng Dữ liệu (Architecture & Data Flow)

### 2.1. Chuỗi Xử lý 5 Bước (Sequential Pipeline)
1. **Request Ingestion**: Router `/api/chat/stream` tiếp nhận `user_query`, `conversation_id`, kiểm tra trạng thái hội thoại (`conversations.mode`).
2. **Decomposer & Intent Router (LLM Call 1)**: `QueryDecomposerService` gọi LLM với `MERGED_DECOMPOSER_PROMPT_KH06`, áp dụng `# DOMAIN BOUNDARY SCOPE`, trả về `DecomposerOutputSchema` chứa danh sách `sub_queries`.
3. **Parallel Dispatcher Execution**: `ParallelRetrievalService` phân phối đồng thời:
   - `SQL_PRODUCT` $\rightarrow$ `SQLProductRetriever` (truy vấn bảng `products`).
   - `VECTOR_KNOWLEDGE` $\rightarrow$ `VectorKnowledgeRetriever` (tạo embedding qua `VietnameseEmbedder` và query `knowledge_chunks` pgvector).
   - `OUT_OF_DOMAIN` $\rightarrow$ `OutOfDomainHandler` (sinh fallback note).
   - `GREETING_CHITCHAT` / `HUMAN_AGENT_REQUEST` $\rightarrow$ handler chuyên biệt.
4. **Context Aggregator**: Gom toàn bộ kết quả thành chuỗi `<aggregated_contexts>` có cấu trúc phân theo từng Sub-query ID.
5. **Multi-Context Synthesizer (LLM Call 2)**: `MultiContextSynthesizerService` stream các token câu trả lời về Client qua SSE, sau đó lưu bản ghi hoàn chỉnh kèm `citations` vào bảng `messages`.

---

## 3. 📂 Touchpoints (Danh sách Tệp tác động)

### 3.1. Các Tệp Tạo mới
* `code/backend/app/modules/rag_assistant/prompts.py`: Chứa `MERGED_DECOMPOSER_PROMPT_KH06` và `MULTI_CONTEXT_SYNTHESIZER_PROMPT_KH06`.
* `code/backend/app/modules/rag_assistant/schemas.py`: Pydantic models (`SubQueryItem`, `DecomposerOutputSchema`, `ChatStreamRequest`, `AggregatedContextItem`, v.v.).
* `code/backend/app/modules/rag_assistant/models.py`: SQLAlchemy models cho `Product`, `KnowledgeChunk`, `Conversation`, `Message`.
* `code/backend/app/modules/rag_assistant/decomposer.py`: Service phân tích, bẻ câu hỏi và định tuyến Intent per sub-query.
* `code/backend/app/modules/rag_assistant/retrievers.py`: Các worker tra cứu song song (SQL Product, Vector Knowledge, Out-of-domain).
* `code/backend/app/modules/rag_assistant/synthesizer.py`: Service tổng hợp ngữ cảnh và stream câu trả lời LLM.
* `code/backend/app/modules/rag_assistant/pipeline.py`: Orchestrator điều phối toàn trình luồng KH-06.
* `code/backend/app/modules/rag_assistant/router.py`: API Endpoints (`POST /api/chat/stream`, `POST /api/chat/message`).
* `code/backend/tests/test_rag_pipeline.py`: Bộ unit test & integration test cho toàn bộ module.

### 3.2. Các Tệp Cập nhật
* `code/backend/app/main.py`: Đăng ký router `rag_assistant.router` vào FastAPI app.
* `code/backend/app/core/config.py`: Bổ sung cấu hình OpenAI / LLM Model name (`gpt-4o-mini` hoặc Gemini), Embedding dimensions (768/1024), Top-K parameters.

---

## 4. 📜 Public Contracts (Giao diện & Schemas)

### 4.1. Request & Response DTOs (`schemas.py`)
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class SubQueryItem(BaseModel):
    id: int
    query: str
    intent: Literal["SQL_PRODUCT", "VECTOR_KNOWLEDGE", "OUT_OF_DOMAIN", "GREETING_CHITCHAT", "HUMAN_AGENT_REQUEST"]
    target_source: Literal["SQL_PRODUCT", "VECTOR_KNOWLEDGE", "NONE"]
    product_search_keyword: Optional[str] = None
    pet_type: Optional[str] = None
    category: Optional[str] = None

class DecomposerOutputSchema(BaseModel):
    standalone_query: str
    reasoning: str
    is_complex: bool
    sub_queries: List[SubQueryItem]

class ChatStreamRequest(BaseModel):
    conversation_id: str
    message: str

class CitationItem(BaseModel):
    document_name: str
    metadata: Dict[str, Any]
    content_snippet: str
```

### 4.2. API Endpoints
* `POST /api/chat/stream`: Header `Accept: text/event-stream`, Body: `ChatStreamRequest`. Trả về SSE Stream dạng chunks `data: {"token": "..."}\n\n` và chunk kết thúc `data: {"event": "done", "citations": [...]}\n\n`.

---

## 5. 💥 Blast Radius (Phạm vi Ảnh hưởng)
* **Packages**: `code/backend/app/modules/rag_assistant`, `code/backend/app/main.py`.
* **Risk Class**: **Thấp - Trung bình** (Module độc lập, không làm ảnh hưởng tới logic của các khối khác khi chưa kích hoạt cờ).

---

## 6. 📝 Implementation Checklist (Danh sách Thực thi Chi tiết)

### Giai đoạn 1: Cấu hình & Mô hình Dữ liệu (Data Models & Schemas)
- [ ] **Step 1.1**: Cập nhật `code/backend/app/core/config.py` bổ sung cấu hình `LLM_MODEL`, `EMBEDDING_MODEL_NAME`, `RAG_TOP_K`.
- [ ] **Step 1.2**: Khởi tạo `code/backend/app/modules/rag_assistant/models.py` với các ORM Table mappings (`products`, `knowledge_chunks`, `conversations`, `messages`).
- [ ] **Step 1.3**: Khởi tạo `code/backend/app/modules/rag_assistant/schemas.py` định nghĩa đầy đủ các Pydantic DTOs.
- [ ] **Step 1.4**: Khởi tạo `code/backend/app/modules/rag_assistant/prompts.py` với `MERGED_DECOMPOSER_PROMPT_KH06` (chứa `# DOMAIN BOUNDARY SCOPE`) và `MULTI_CONTEXT_SYNTHESIZER_PROMPT_KH06`.

### Giai đoạn 2: Xây dựng Bộ Decomposer & Parallel Retrievers
- [ ] **Step 2.1**: Hiện thực hóa `code/backend/app/modules/rag_assistant/decomposer.py` (`QueryDecomposerService` gọi LLM Structured Output phân tích JSON).
- [ ] **Step 2.2**: Hiện thực hóa `SQLProductRetriever` trong `code/backend/app/modules/rag_assistant/retrievers.py` (query SQL bảng `products`).
- [ ] **Step 2.3**: Hiện thực hóa `VectorKnowledgeRetriever` trong `retrievers.py` (tích hợp `VietnameseEmbedder`, truy vấn pgvector HNSW trên `knowledge_chunks`, không dùng score threshold).
- [ ] **Step 2.4**: Hiện thực hóa `OutOfDomainHandler` và `ChitchatHandler` trong `retrievers.py`.
- [ ] **Step 2.5**: Hiện thực hóa `ParallelRetrievalService` sử dụng `asyncio.gather` để chạy đồng thời các sub-query workers.

### Giai đoạn 3: Multi-Context Synthesizer & RAG Pipeline Orchestrator
- [ ] **Step 3.1**: Hiện thực hóa `code/backend/app/modules/rag_assistant/synthesizer.py` (`MultiContextSynthesizerService` gom `<aggregated_contexts>` và stream kết quả).
- [ ] **Step 3.2**: Hiện thực hóa `code/backend/app/modules/rag_assistant/pipeline.py` (`RAGPipelineService` tích hợp trọn gói Step 1 $\rightarrow$ Step 5, lưu lịch sử `messages` và `citations`).
- [ ] **Step 3.3**: Hiện thực hóa `code/backend/app/modules/rag_assistant/router.py` (endpoint `/api/chat/stream` hỗ trợ SSE Streaming và kiểm tra `conversations.mode`).
- [ ] **Step 3.4**: Đăng ký router vào `code/backend/app/main.py`.

### Giai đoạn 4: Kiểm thử Tự động & Đánh giá Toàn trình (Verification)
- [ ] **Step 4.1**: Viết bộ unit tests cho `QueryDecomposerService` kiểm tra phân loại In-Domain, Out-of-Domain, và Mixed Sub-queries.
- [ ] **Step 4.2**: Viết integration tests cho `ParallelRetrievalService` kết nối DB thật.
- [ ] **Step 4.3**: Viết End-to-End Test cho Endpoint `/api/chat/stream` kiểm tra dòng SSE trả về và lưu `messages`.

---

## Verification Evidence

| Gate / Scenario | Strategy | Proves SPEC criterion |
|---|---|---|
| **Test Decomposer JSON Output** | Fully-Automated | Bẻ đúng 2-3 sub-queries, gán chuẩn intent `SQL_PRODUCT`, `VECTOR_KNOWLEDGE`, `OUT_OF_DOMAIN`. |
| **Test SQL Product Catalog Lookup** | Fully-Automated | Lấy đúng giá, tồn kho thực tế của sản phẩm từ bảng `products`. |
| **Test Vector pgvector Retrieval** | Fully-Automated | Trích xuất Top-3 chunks chính sách/FAQ liên quan mà không bị nghẽn bởi Score Thresholding. |
| **Test Out-of-Domain Fallback per Sub-query** | Fully-Automated | Sub-query ngoài domain sinh đúng thông báo ngoài phạm vi + câu hỏi nối máy CSKH. |
| **Test SSE Token Streaming Flow** | Hybrid | Endpoint `/api/chat/stream` trả về `text/event-stream` liên tục, mượt mà và lưu bản ghi `messages` hoàn chỉnh. |

---

## Risk Predictions & Failure Modes

1. **Rủi ro LLM Decomposer sinh JSON lỗi:**
   * *Khắc phục:* Sử dụng JSON Mode / Structured Output của OpenAI/Gemini và Pydantic Validator; có cơ chế fallback quay về single-query vector search nếu JSON parse thất bại.
2. **Rủi ro Timeout khi truy vấn song song:**
   * *Khắc phục:* Đặt `timeout=5.0s` cho từng worker trong `asyncio.gather(return_exceptions=True)`, worker nào lỗi sẽ trả về placeholder rỗng thay vì làm sập toàn bộ request.
3. **Rủi ro Kết nối CSDL pgvector chậm:**
   * *Khắc phục:* Sử dụng Connection Pooling qua SQLAlchemy ORM với `pool_pre_ping=True` và chỉ mục HNSW đã được đánh sẵn trên cột `embedding`.

---

## Test Infra Improvement Notes
(none identified yet)

---

## Resume and Execution Handoff

1. **Selected Plan File Path**: `process/features/rag-assistant/active/rag-kh06-pipeline_16-09-26/rag-kh06-pipeline_PLAN_16-09-26.md`
## Validate Contract

Status: PASS
Date: 16-09-26
date: 2026-09-16
generated-by: outer-pvl

Parallel strategy: sequential
Rationale: Triển khai tuần tự theo từng tầng phụ thuộc (Models/Schemas -> Decomposer/Retrievers -> Pipeline/Router -> Test) trong cùng module `rag_assistant`.

Test gates:

| criterion id | behavior | strategy | proving test | gap-resolution |
|---|---|---|---|---|
| SPEC-RAG-01 | Decomposer bẻ sub-queries & gán Intent per sub-query | Fully-Automated | `pytest tests/test_rag_pipeline.py::test_decomposer_subqueries_and_intents` | B |
| SPEC-RAG-02 | Truy vấn SQL CSDL `products` lấy đúng giá & tồn kho real-time | Fully-Automated | `pytest tests/test_rag_pipeline.py::test_sql_product_catalog_retrieval` | B |
| SPEC-RAG-03 | Truy vấn HNSW `pgvector` trên bảng `knowledge_chunks` (768-dim) không dùng Score Threshold | Fully-Automated | `pytest tests/test_rag_pipeline.py::test_pgvector_hnsw_retrieval` | B |
| SPEC-RAG-04 | Xử lý Out-of-Domain fallback per sub-query + gợi ý CSKH | Fully-Automated | `pytest tests/test_rag_pipeline.py::test_out_of_domain_fallback_handling` | B |
| SPEC-RAG-05 | Streaming SSE token-by-token và ghi nhận messages + citations | Hybrid | `pytest tests/test_rag_pipeline.py::test_sse_chat_stream_endpoint` | B |

Dimension findings:
- Infra fit: PASS — CSDL Supabase PostgreSQL đã có sẵn bảng `knowledge_chunks` với vector 768 chiều & chỉ mục HNSW `idx_knowledge_chunks_embedding_hnsw` (`vector_cosine_ops`), cùng bảng `products` có chỉ mục B-tree & GIN.
- Test coverage: PASS — Toàn bộ 5 kịch bản cốt lõi đều được bao phủ bởi các testcase tự động và hybrid SSE test.
- Breaking changes: PASS — Module mới được đóng gói độc lập trong `app/modules/rag_assistant/`, không làm gián đoạn các bảng hay router hiện hữu.
- Security surface: PASS — Sử dụng Parameterized SQL Query chống SQL Injection; kiểm tra xác thực và conversation mode trước khi gọi LLM.

Open gaps: none

What this coverage does NOT prove:
- Độ trễ mạng thực tế khi gọi API LLM (OpenAI/Gemini) trong điều kiện nghẽn mạng internet công cộng.
- Giao diện người dùng React Frontend hiển thị SSE (sẽ được kiểm thử ở pha tích hợp Frontend Khối 1).

Gate: PASS
Accepted by: user

---

## Autonomous Goal Block

```text
TARGET: Implement and verify RAG Assistant Module with KH-06 Architecture in code/backend/app/modules/rag_assistant
PER-PHASE LOOP:
1. Config & Schemas (config.py, models.py, schemas.py, prompts.py)
2. Decomposer & Parallel Retrievers (decomposer.py, retrievers.py)
3. Synthesizer, Pipeline & Router (synthesizer.py, pipeline.py, router.py, main.py)
4. Verification & Testing (tests/test_rag_pipeline.py)
SAFETY: Non-destructive to other modules. Use Parameterized SQL. Validate all JSON schemas.
TEST GATES: pytest tests/test_rag_pipeline.py
START: Begin with Phase 1
```


