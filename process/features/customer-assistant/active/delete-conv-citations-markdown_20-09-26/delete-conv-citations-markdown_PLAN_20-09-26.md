# Technical Implementation Plan: Delete Conversation, Parent Citations, Markdown Rendering & Header Logo

> **Feature Area:** `customer-assistant`  
> **Task Slug:** `delete-conv-citations-markdown`  
> **Date:** 20-09-26  
> **Status:** ACTIVE  

---

## 1. Overview & Goals

### 🎯 Primary Goals
1. **Chức năng Xóa Cuộc Hội Thoại & Vô Hiệu Hóa Ticket (UC 1.4, UC 2.2, UC 3.3, UC 4.1, UC 4.2, UC 4.3)**:
   - Cho phép khách hàng xóa các phiên trò chuyện trong lịch sử.
   - Tự động vô hiệu hóa (`status = 'CLOSED'`) bất kỳ Ticket hỗ trợ nào đang ở trạng thái `PENDING` hoặc `IN_PROGRESS` liên quan đến phiên hội thoại bị xóa.
   - Đồng bộ thời gian thực ngắt đồng hồ đếm ngược SLA, loại Ticket khỏi hàng đợi chia việc `queue:tickets:pending`, phát sự kiện WebSocket dọn dẹp thẻ khỏi màn hình Console và Kanban của nhân viên CSKH.
2. **Hiển Thị Trích Dẫn RAG Đầy Đủ `parent_content` kèm Mở Rộng / Thu Gọn (UC 1.3)**:
   - Khắc phục lỗi giao diện hiển thị trích dẫn RAG không khớp trường thông tin backend.
   - Truyền chính xác `document_name`, `section_title`, `page_number`, `content_snippet` và `parent_content` (tài liệu gốc) từ Supabase pgvector metadata.
   - Cung cấp nút **"Mở rộng nội dung đầy đủ" / "Thu gọn"** giúp xem toàn văn chính sách mà không bị che khuất.
3. **Định Dạng Văn Bản LLM Markdown Chuẩn (UC 1.3)**:
   - Xử lý câu trả lời từ AI Bot hiển thị đúng chuẩn định dạng Markdown (in đậm `**text**`, chữ nghiêng, danh sách gạch đầu dòng `-`, phân đoạn văn bản) thay vì hiển thị dạng văn bản thô `*x*`.
4. **Đồng Bộ Logo Thương Hiệu [`logo.png`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/assets/logo.png) Trên Header**:
   - Sử dụng file ảnh logo hiện có tại `code/frontend/src/assets/logo.png` hiển thị đồng bộ ở vị trí Header của tất cả các trang (Trang chủ, Trang Chat, Đăng nhập, Đăng ký, Admin Config).

---

## 2. Touchpoints & Target Files

| Package / Module | File Path | Action | Description |
| :--- | :--- | :--- | :--- |
| **Docs** | [`docs/overview/usecase.md`](file:///d:/Study/TLU/kiemthu/project/docs/overview/usecase.md) | **[MODIFY]** | Bổ sung Use Case 1.4 và các luồng ngoại lệ E-3/E-4/E-5 xử lý Ticket vô hiệu hóa khi xóa phiên chat. |
| **Backend Schema** | [`code/backend/app/schemas/rag.py`](file:///d:/Study/TLU/kiemthu/project/code/backend/app/schemas/rag.py) | **[MODIFY]** | Bổ sung trường `parent_content`, `section_title`, `page_number` vào DTO `CitationItem`. |
| **Backend Service** | [`code/backend/app/services/rag/retrievers.py`](file:///d:/Study/TLU/kiemthu/project/code/backend/app/services/rag/retrievers.py) | **[MODIFY]** | Trích xuất `parent_content` từ `metadata` của `knowledge_chunks` đưa vào `CitationItem`. |
| **Backend Service** | [`code/backend/app/services/conversation_service.py`](file:///d:/Study/TLU/kiemthu/project/code/backend/app/services/conversation_service.py) | **[MODIFY]** | Thêm hàm `delete_conversation()`: Cập nhật `tickets.status = 'CLOSED'` và xóa `messages` / `conversations`. |
| **Backend Endpoint** | [`code/backend/app/api/v1/endpoints/conversation.py`](file:///d:/Study/TLU/kiemthu/project/code/backend/app/api/v1/endpoints/conversation.py) | **[MODIFY]** | Thêm REST API `DELETE /api/conversations/{id}`. |
| **Frontend Service** | [`code/frontend/src/services/chatService.js`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/services/chatService.js) | **[MODIFY]** | Thêm method `deleteConversation(id)`. |
| **Frontend Component**| [`code/frontend/src/components/chat/CitationsDrawer.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/components/chat/CitationsDrawer.jsx) | **[MODIFY]** | Sửa khớp trường thông tin trích dẫn + Thêm nút Mở rộng/Thu gọn `parent_content`. |
| **Frontend Component**| [`code/frontend/src/components/chat/MessageItem.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/components/chat/MessageItem.jsx) | **[MODIFY]** | Tích hợp bộ chuyển đổi Markdown render `**in đậm**`, danh sách gạch đầu dòng và ngắt dòng. |
| **Frontend Page** | [`code/frontend/src/pages/customer/ChatPage.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/pages/customer/ChatPage.jsx) | **[MODIFY]** | Thêm nút xóa icon `Trash2` tại từng mục danh sách phiên chat và ở thanh tiêu đề chat. |
| **Frontend Page** | [`code/frontend/src/pages/customer/LandingPage.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/pages/customer/LandingPage.jsx) | **[MODIFY]** | Gắn logo.png vào Header. |
| **Frontend Page** | [`code/frontend/src/pages/auth/CustomerLogin.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/pages/auth/CustomerLogin.jsx) | **[MODIFY]** | Gắn logo.png vào Header. |
| **Frontend Page** | [`code/frontend/src/pages/auth/CustomerRegister.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/pages/auth/CustomerRegister.jsx) | **[MODIFY]** | Gắn logo.png vào Header. |
| **Frontend Page** | [`code/frontend/src/pages/admin/AlertConfigPage.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/pages/admin/AlertConfigPage.jsx) | **[MODIFY]** | Gắn logo.png vào Header. |

---

## 3. Public Contracts & Data Flow

### 3.1 REST API API Endpoint Mới: Xóa Cuộc Hội Thoại
* **Method:** `DELETE /api/conversations/{id}`
* **Headers:** `Authorization: Bearer <access_token>`
* **Process Flow:**
  1. Kiểm tra quyền sở hữu `conversation.customer_id == current_user.id`.
  2. Query các `tickets` liên quan đến `conversation_id`: nếu `status IN ('PENDING', 'IN_PROGRESS')`, cập nhật `UPDATE tickets SET status = 'CLOSED', updated_at = NOW() WHERE conversation_id = :id`.
  3. Xóa các bản ghi `messages` thuộc `conversation_id`.
  4. Xóa bản ghi `conversations` thuộc `id`.
  5. Bắn sự kiện WebSocket `CONVERSATION_DELETED` sang cho Agent/Kanban dọn dẹp hàng đợi.
* **Response (200 OK):** `{"message": "Xóa cuộc trò chuyện thành công", "deleted_id": "..."}`

### 3.2 Citation Data Structure Contract (Dữ liệu Trích dẫn RAG)
```json
{
  "document_name": "Chinh_sach_doi_tra_PET-CS-002.md",
  "section_title": "3.5. Khách đổi ý (không thích, không cần nữa)",
  "page_number": null,
  "content_snippet": "[Chính sách Đổi trả và Hoàn tiền (PET-CS-002) - Mục 3.5 Khách đổi ý]: Thời hạn: Trong 03 ngày kể từ ngày nhận hàng...",
  "parent_content": "CÁC TRƯỜNG HỢP ĐƯỢC ĐỔI TRẢ... 3.5. Khách đổi ý (không thích, không cần nữa). Thời hạn: Trong 03 ngày kể từ ngày nhận hàng. Điều kiện: Sản phẩm còn nguyên seal, chưa qua sử dụng, còn hóa đơn. Xử lý: Đổi sang sản phẩm khác có giá trị bằng hoặc cao hơn..."
}
```

---

## 4. Blast Radius & Dependencies

- **Cơ sở dữ liệu:** Thao tác xóa `conversations` ảnh hưởng tới 2 bảng liên quan `messages` (Cascade delete) và `tickets` (Update `status = 'CLOSED'`).
- **WebSockets / Event Bus:** Bắn thông điệp `CONVERSATION_DELETED` để các client Agent đang trực ca tự động làm mới hàng đợi và ngắt phiên chat trực tiếp.
- **Frontend UI Dependencies:** Thêm component hoặc helper Markdown Parser trong `MessageItem.jsx` (không phá vỡ CSS `whitespace-pre-wrap` cũ).

---

## 5. Implementation Checklist

1. **[Tài liệu Use Case]** Cập nhật [`docs/overview/usecase.md`](file:///d:/Study/TLU/kiemthu/project/docs/overview/usecase.md) với đặc tả Use Case 1.4 và các trường hợp rẽ nhánh Ticket bị vô hiệu hóa cho UC 2.2, 3.3, 4.1, 4.2, 4.3.
2. **[Backend Schema]** Sửa `CitationItem` DTO trong [`code/backend/app/schemas/rag.py`](file:///d:/Study/TLU/kiemthu/project/code/backend/app/schemas/rag.py) hỗ trợ trường `parent_content` và `section_title`.
3. **[Backend Service]** Cập nhật `VectorKnowledgeRetriever` trong [`code/backend/app/services/rag/retrievers.py`](file:///d:/Study/TLU/kiemthu/project/code/backend/app/services/rag/retrievers.py) trích xuất `metadata.parent_content` vào `CitationItem`.
4. **[Backend Service]** Bổ sung hàm `delete_conversation` trong [`code/backend/app/services/conversation_service.py`](file:///d:/Study/TLU/kiemthu/project/code/backend/app/services/conversation_service.py) vô hiệu hóa Ticket liên quan (`status = 'CLOSED'`) và xóa dữ liệu phiên.
5. **[Backend API]** Bổ sung endpoint `DELETE /api/conversations/{id}` trong [`code/backend/app/api/v1/endpoints/conversation.py`](file:///d:/Study/TLU/kiemthu/project/code/backend/app/api/v1/endpoints/conversation.py).
6. **[Frontend Service]** Thêm phương thức `deleteConversation(id)` vào [`code/frontend/src/services/chatService.js`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/services/chatService.js).
7. **[Frontend Component]** Cập nhật [`code/frontend/src/components/chat/CitationsDrawer.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/components/chat/CitationsDrawer.jsx): Hiển thị đúng các trường `document_name`, `section_title`, `content_snippet` và thêm công tắc **"Mở rộng nội dung đầy đủ" / "Thu gọn"** cho `parent_content`.
8. **[Frontend Component]** Cập nhật [`code/frontend/src/components/chat/MessageItem.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/components/chat/MessageItem.jsx): Tích hợp bộ chuyển đổi định dạng Markdown (in đậm `**text**`, danh sách `-`, xuống dòng).
9. **[Frontend Page]** Cập nhật [`code/frontend/src/pages/customer/ChatPage.jsx`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/pages/customer/ChatPage.jsx):
   - Thêm nút xóa icon `Trash2` tại từng mục danh sách phiên chat và ở thanh tiêu đề chat.
   - Thêm Modal xác nhận xóa cuộc trò chuyện.
   - Gắn hình ảnh [`logo.png`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/assets/logo.png) vào góc Top Header.
10. **[Frontend Branding Header]** Đồng bộ gắn hình ảnh [`logo.png`](file:///d:/Study/TLU/kiemthu/project/code/frontend/src/assets/logo.png) vào Top Header của `LandingPage.jsx`, `CustomerLogin.jsx`, `CustomerRegister.jsx`, và `AlertConfigPage.jsx`.

---

## 6. Verification Evidence

| Gate / Scenario | Strategy | Proves SPEC criterion |
| :--- | :--- | :--- |
| **Xóa cuộc trò chuyện & vô hiệu hóa Ticket** | Hybrid (API Test + UI Integration) | Xóa phiên chat thành công, Ticket tương ứng đổi sang `CLOSED` trong DB và biến mất khỏi hàng đợi làm việc. |
| **Trích dẫn parent_content & Mở rộng/Thu gọn** | Hybrid (UI Manual Probe) | Nhấp "Trích dẫn nguồn" hiển thị đúng dữ liệu; bấm "Mở rộng nội dung đầy đủ" bung ra toàn bộ nội dung `parent_content`. |
| **Markdown Rendering cho tin nhắn LLM** | Hybrid (UI Component Test) | Tin nhắn trả về có `**in đậm**` hiển thị bằng thẻ `<strong>` trực quan thay vì hiện nguyên văn dấu `*`. |
| **Header Logo hiển thị ở mọi trang** | Hybrid (UI Visual Inspection) | Ảnh `logo.png` xuất hiện chuẩn kích thước tại Header trên 5 trang chính của ứng dụng. |

---

## 7. Test Infra Improvement Notes
(none identified yet)

---

## 8. Resume and Execution Handoff

* Khi được chấp thuận kế hoạch, chuyển sang chế độ **EXECUTE** để tiến hành chỉnh sửa mã nguồn full-stack theo danh sách 10 bước trong Implementation Checklist.
