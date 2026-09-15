# THIẾT KẾ & PHÂN TÍCH HỆ THỐNG CHI TIẾT (SYSTEM ANALYSIS & TECHNICAL SPECIFICATION)

> **Tên hệ thống:** Website tư vấn khách hàng tự động và điều phối hỗ trợ thông minh cho chuỗi cửa hàng đồ dùng thú cưng.  
> **Tài liệu chuẩn mực kỹ thuật (Single Source of Truth):** Chứa đầy đủ các quy tắc CSDL, kiến trúc sự kiện thời gian thực, quy trình API, logic xử lý nội bộ, ngoại lệ và thuật toán cho toàn bộ 14 Use Cases phục vụ trực tiếp công tác phát triển phần mềm (Mã nguồn full-stack).

---

# I. Thiết kế Cơ sở Dữ liệu (Supabase PostgreSQL & pgvector Engine)

Hệ thống sử dụng **Supabase PostgreSQL** làm CSDL trung tâm, tích hợp extension `pgvector` cho dữ liệu RAG. Dưới đây là đặc tả chi tiết 10 bảng CSDL master:

### 1. Bảng `users` (Tài khoản & Nhân sự hệ thống)
Lưu trữ thông tin tài khoản nhân sự (Agent, Manager, Admin), trạng thái trực ca và danh mục kỹ năng xử lý chuyên môn.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh duy nhất của nhân viên |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | Email nội bộ đăng nhập và nhận báo động |
| `password_hash` | VARCHAR(255) | NOT NULL | Chuỗi mật khẩu băm an toàn (Bcrypt/Argon2) |
| `full_name` | VARCHAR(100) | NOT NULL | Họ và tên đầy đủ của nhân viên (2-100 ký tự) |
| `phone` | VARCHAR(20) | NULL | Số điện thoại liên hệ (10 chữ số, bắt đầu bằng 0) |
| `role` | VARCHAR(20) | NOT NULL, Default: 'AGENT', CHECK (`role` IN ('AGENT', 'MANAGER', 'ADMIN')) | Vai trò nhân sự trong hệ thống |
| `status` | VARCHAR(20) | NOT NULL, Default: 'OFFLINE', CHECK (`status` IN ('ONLINE', 'BUSY', 'OFFLINE')) | Trạng thái làm việc trực ca thời gian thực |
| `skills` | JSONB | NULL | Mảng JSON các danh mục nghiệp vụ phụ trách (VD: `["Lỗi đơn hàng", "Đổi trả/Hoàn tiền", "Sản phẩm lỗi/Hư hại"]`) |
| `is_active` | BOOLEAN | NOT NULL, Default: `TRUE` | Trạng thái kích hoạt tài khoản (TRUE: Hoạt động, FALSE: Khóa) |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm tạo tài khoản |
| `updated_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm cập nhật thông tin gần nhất |

---

### 2. Bảng `customers` (Tài khoản & Định danh Khách hàng)
Lưu trữ định danh người dùng đăng ký hoặc vãng lai truy cập website tư vấn đồ dùng thú cưng.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh duy nhất của khách hàng |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | Email đăng nhập tiêu chuẩn (gồm `@` và domain, max 255 chars) |
| `password_hash` | VARCHAR(255) | NOT NULL | Chuỗi mật khẩu băm bảo vệ tài khoản |
| `full_name` | VARCHAR(100) | NOT NULL | Họ và tên khách hàng (2-50 ký tự, chữ Việt/Anh và khoảng trắng) |
| `phone` | VARCHAR(20) | NULL | Số điện thoại liên hệ (10 chữ số, bắt đầu bằng 0) |
| `is_active` | BOOLEAN | NOT NULL, Default: `TRUE` | Trạng thái tài khoản (TRUE: Hoạt động, FALSE: Khóa tạm thời) |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm đăng ký tài khoản |
| `updated_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm cập nhật hồ sơ gần nhất |

---

### 3. Bảng `conversations` (Phiên hội thoại CSKH)
Quản lý các phiên trò chuyện giữa Khách hàng và Trợ lý ảo AI hoặc Nhân viên tư vấn trực tiếp.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh duy nhất của phiên trò chuyện |
| `customer_id` | UUID | FK $\rightarrow$ `customers(id)`, NOT NULL | Mã khách hàng sở hữu phiên trò chuyện |
| `assigned_agent_id` | UUID | FK $\rightarrow$ `users(id)`, NULL | Nhân viên tiếp quản (NULL nếu đang phục vụ bởi AI Bot) |
| `mode` | VARCHAR(20) | NOT NULL, Default: 'BOT', CHECK (`mode` IN ('BOT', 'HUMAN', 'WAITING_HUMAN')) | Chế độ phục vụ (`BOT`: AI tự động, `HUMAN`: Nhân viên chat, `WAITING_HUMAN`: Chờ tiếp quản) |
| `is_flagged` | BOOLEAN | NOT NULL, Default: `FALSE` | Cờ cảnh báo đỏ nguy cơ bức xúc/khiếu nại nghiêm trọng |
| `last_sentiment` | VARCHAR(20) | NULL, CHECK (`last_sentiment` IN ('POSITIVE', 'NEUTRAL', 'NEGATIVE', 'CRITICAL')) | Đánh giá cảm xúc ở lượt tin nhắn gần nhất |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm bắt đầu phiên hội thoại |
| `updated_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm có tin nhắn mới gần nhất |

---

### 4. Bảng `messages` (Chi tiết Tin nhắn Hội thoại)
Lưu vết từng lượt tin nhắn trao đổi, kết quả phân tích cảm xúc ngầm và dữ liệu trích dẫn RAG.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh duy nhất của tin nhắn |
| `conversation_id` | UUID | FK $\rightarrow$ `conversations(id)` ON DELETE CASCADE, NOT NULL | Phiên trò chuyện chứa tin nhắn này |
| `sender_type` | VARCHAR(10) | NOT NULL, CHECK (`sender_type` IN ('CUSTOMER', 'BOT', 'AGENT')) | Đối tượng gửi tin nhắn |
| `sender_id` | UUID | NULL | Mã nhân viên gửi tin (NULL nếu `sender_type` là `CUSTOMER` hoặc `BOT`) |
| `content` | TEXT | NOT NULL | Nội dung văn bản tin nhắn (1 đến 4.000 ký tự) |
| `citations` | JSONB | NULL | Mảng JSON trích dẫn nguồn RAG (Tên file, điều khoản, trang, trích đoạn) |
| `sentiment_score` | NUMERIC(4, 2) | NULL | Điểm cảm xúc AI đo lường từ -1.00 đến +1.00 |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm gửi tin nhắn |

---

### 5. Bảng `tickets` (Phiếu Khiếu nại & Yêu cầu Hỗ trợ)
Lưu trữ hồ sơ sự cố, kết quả trích xuất AI, phân công xử lý và theo dõi cam kết SLA.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh duy nhất của Ticket |
| `conversation_id` | UUID | FK $\rightarrow$ `conversations(id)`, NOT NULL | Phiên trò chuyện phát sinh khiếu nại/yêu cầu |
| `assigned_to` | UUID | FK $\rightarrow$ `users(id)`, NULL | Nhân viên tiếp nhận xử lý (NULL nếu chờ phân bổ) |
| `category` | VARCHAR(50) | NOT NULL | Danh mục sự cố (`Lỗi đơn hàng`, `Đổi trả/Hoàn tiền`, `Sản phẩm lỗi/Hư hại`, `Lỗi thanh toán`, `Thái độ phục vụ`, `Vấn đề khác`) |
| `priority` | VARCHAR(10) | NOT NULL, CHECK (`priority` IN ('P1', 'P2', 'P3')) | Mức độ ưu tiên (`P1`: Cực kỳ khẩn cấp, `P2`: Khẩn cấp cao, `P3`: Trung bình) |
| `status` | VARCHAR(20) | NOT NULL, Default: 'PENDING', CHECK (`status` IN ('PENDING', 'IN_PROGRESS', 'RESOLVED', 'CLOSED')) | Trạng thái tiến độ Kanban |
| `summary` | TEXT | NOT NULL | Đoạn tóm tắt sự cố được AI trích xuất (20-255 ký tự) |
| `ai_metadata` | JSONB | NULL | Dữ liệu cấu trúc AI (Bằng chứng trích dẫn, điểm sentiment, lý do gán P1/P2/P3) |
| `sla_deadline` | TIMESTAMPTZ | NOT NULL | Thời điểm hạn chót cam kết hoàn tất xử lý |
| `sla_breached` | BOOLEAN | NOT NULL, Default: `FALSE` | Đánh dấu vi phạm quá hạn cam kết xử lý |
| `resolved_at` | TIMESTAMPTZ | NULL | Thời điểm chính thức chuyển sang `RESOLVED` |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm tạo phiếu hỗ trợ |
| `updated_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm cập nhật trạng thái gần nhất |

---

### 6. Bảng `sla_policies` (Chính sách Khung Thời gian Cam kết SLA)
Định nghĩa quy chuẩn thời gian giải quyết khẩn cấp tối đa theo mức độ ưu tiên.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh chính sách SLA |
| `priority` | VARCHAR(10) | UNIQUE, NOT NULL, CHECK (`priority` IN ('P1', 'P2', 'P3')) | Mức ưu tiên áp dụng (`P1`, `P2`, `P3`) |
| `resolution_time_minutes` | INT | NOT NULL | Thời gian xử lý tối đa cho phép (P1: 15 phút, P2: 60 phút, P3: 240 phút) |
| `escalation_notify_to` | VARCHAR(20) | NOT NULL, Default: 'MANAGER' | Cấp bậc nhận cảnh báo leo thang khi vi phạm (`MANAGER`, `ADMIN`) |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm khởi tạo quy chuẩn SLA |

---

### 7. Bảng `canned_responses` (Kho Mẫu Phản hồi Nhanh)
Lưu trữ các câu trả lời chuẩn hóa hỗ trợ nhân viên gửi nhanh bằng phím tắt.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh mẫu phản hồi |
| `shortcut` | VARCHAR(50) | NOT NULL, UNIQUE | Phím tắt kích hoạt (Bắt buộc bắt đầu bằng `/`, không khoảng trắng, VD: `/chao`, `/xloi_giaohang`) |
| `title` | VARCHAR(150) | NOT NULL | Tiêu đề gợi nhớ mục đích (3-150 ký tự) |
| `content` | TEXT | NOT NULL | Nội dung câu trả lời chuẩn (5-2.000 ký tự) |
| `category` | VARCHAR(50) | NOT NULL | Danh mục nghiệp vụ (VD: `Đơn hàng`, `Vận chuyển`, `Đổi trả`, `Sản phẩm`) |
| `created_by` | UUID | FK $\rightarrow$ `users(id)`, NOT NULL | Mã nhân viên/quản lý khởi tạo mẫu câu |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm tạo mẫu phản hồi |

---

### 8. Bảng `ai_rules` (Quy tắc Kích hoạt & Ngưỡng Cảm xúc AI)
Cấu hình ngưỡng cảm xúc và quy tắc mở ticket tự động cho AI Auto-Triage Engine.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh quy tắc AI |
| `rule_name` | VARCHAR(100) | NOT NULL | Tên quy tắc gợi nhớ (1-100 ký tự) |
| `sentiment_threshold` | NUMERIC(4, 2) | NOT NULL | Ngưỡng điểm số cảm xúc kích hoạt số âm (-1.00 đến 0.00, mặc định -0.60) |
| `target_priority` | VARCHAR(10) | NOT NULL, CHECK (`target_priority` IN ('P1', 'P2', 'P3')) | Mức độ ưu tiên gán tự động khi chạm ngưỡng |
| `is_active` | BOOLEAN | NOT NULL, Default: `TRUE` | Trạng thái bật/tắt kích hoạt áp dụng |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm tạo quy tắc |

---

### 9. Bảng `knowledge_chunks` (Tài liệu RAG & Vector Embedding Supabase `pgvector`)
Lưu trữ các đoạn văn bản chính sách/hướng dẫn đã bóc tách cùng Vector nhúng ngữ nghĩa.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh đoạn trích tài liệu |
| `document_name` | VARCHAR(255) | NOT NULL | Tên file văn bản gốc (VD: `Chinh_sach_doi_tra.pdf`) |
| `content` | TEXT | NOT NULL | Nội dung đoạn văn bản đã chia nhỏ (Chunk) |
| `embedding` | VECTOR(1024) | NULL | Vector nhúng ngữ nghĩa 1024 chiều (BGE/OpenAI) |
| `metadata` | JSONB | NULL | JSON chứa: `page_number`, `section_title`, `clause` để trích dẫn |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm lưu vector dữ liệu |

---

### 10. Bảng `products` (Danh mục & Tồn kho Sản phẩm Thú cưng)
Lưu trữ thông tin mặt hàng, đối tượng vật nuôi, giá bán và tồn kho cửa hàng.

| Tên trường (Column) | Kiểu dữ liệu | Ràng buộc (Constraints) | Mô tả nghiệp vụ & Quy chuẩn kỹ thuật |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh sản phẩm |
| `sku` | VARCHAR(50) | NOT NULL, UNIQUE | Mã quản lý kho hàng (VD: `DOG-ROYAL-MAXI-3KG`) |
| `name` | VARCHAR(255) | NOT NULL | Tên thương mại sản phẩm thú cưng |
| `category` | VARCHAR(100) | NOT NULL | Danh mục (`Thức ăn`, `Cát vệ sinh`, `Phụ kiện`, `Đồ chơi`, `Chăm sóc`) |
| `pet_type` | VARCHAR(50) | NOT NULL, CHECK (`pet_type` IN ('DOG', 'CAT', 'BIRD', 'ALL', 'OTHER')) | Đối tượng thú cưng áp dụng |
| `price` | NUMERIC(12, 2) | NOT NULL, CHECK (`price` >= 0) | Giá niêm yết bán lẻ |
| `sale_price` | NUMERIC(12, 2) | NULL, CHECK (`sale_price` >= 0) | Giá khuyến mãi (nếu có) |
| `stock_quantity` | INT | NOT NULL, Default: 0, CHECK (`stock_quantity` >= 0) | Số lượng tồn kho thực tế |
| `status` | VARCHAR(20) | NOT NULL, Default: 'IN_STOCK', CHECK (`status` IN ('IN_STOCK', 'OUT_OF_STOCK', 'DISCONTINUED')) | Trạng thái kinh doanh |
| `attributes` | JSONB | NULL | JSON chứa trọng lượng, kích thước, xuất xứ, hương vị |
| `description` | TEXT | NULL | Tóm tắt mô tả sản phẩm |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm tạo bản ghi sản phẩm |
| `updated_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm cập nhật giá/kho gần nhất |

---

# II. Kiến trúc Kỹ thuật Thời gian thực & Xử lý Sự kiện (Real-time Architecture)

```text
                      +----------------------------------+
                      |         Khách hàng (Client UI)   |
                      +----------------------------------+
                             /            |            \
                    Auth JWT /             | SSE Stream  \ WebSocket (2-way)
                           /              |              \
                          v               v               v
                +--------------------------------------------------+
                |           FastAPI Gateway & Auth Middleware      |
                +--------------------------------------------------+
                   /              |               |             \
                  /               |               |              \
                 v                v               v               v
   +------------------+  +-----------------+  +------------+  +-------------------+
   | Supabase Vector  |  |  Structured LLM |  | PostgreSQL |  | WebSocket Manager |
   | (knowledge_chunks|  |  Sentiment Engine|  | (Supabase  |  | (Rooms & Sockets) |
   | HNSW Index)      |  |                 |  | 10 Tables) |  |                   |
   +------------------+  +-----------------+  +------------+  +-------------------+
                                  |                                     ^
                         Bắn sự kiện Ticket                              |
                                  v                                     |
                         +-----------------+                            |
                         | Redis Event Bus |----------------------------+
                         | (PubSub & Queue)|    Đẩy Alert vi phạm SLA
                         +-----------------+    và Ticket mới qua WS
                                  |
                                  v
                         +-----------------+
                         | Worker Services |
                         | Dispatch & SLA  |
                         +-----------------+
```

1. **Server-Sent Events (SSE):** Sử dụng Header `Content-Type: text/event-stream` tại `/api/chat/stream` đẩy luồng ký tự `data: {"token": "..."}\n\n` cho RAG Response.
2. **WebSocket Gateway:** Quản lý Connection Pool, chia room `room_conversation_{id}` và `room_agent_{id}`, truyền tin nhắn 2 chiều khi `mode = 'HUMAN'` và phát sự kiện `FLAGGED_CONVERSATION`, `TAKEOVER_SUCCESS`.
3. **Redis Event Bus:**
   - **Queue (`queue:tickets:pending`):** Nhận sự kiện `TICKET_CREATED` từ Auto-Triage để *Ticket Dispatcher Worker* xử lý bất đồng bộ theo thuật toán Least-Loaded.
   - **Pub/Sub (`channel:sla_alerts`):** *SLA Worker* quét quá hạn đẩy thông điệp vi phạm tới WebSocket Manager để bắn thông báo chuông đỏ nhấp nháy cho Manager.
   - **Cache (`agent:status:{user_id}`):** Lưu trạng thái ONLINE/BUSY/OFFLINE và số lượng ticket đang gánh để thuật toán chia việc truy xuất nhanh $O(1)$.
4. **Supabase `pgvector` Engine:** Thực hiện phép tìm kiếm tương đồng Cosine:
   ```sql
   SELECT id, document_name, content, metadata
   FROM knowledge_chunks
   ORDER BY embedding <=> query_embedding
   LIMIT 3;
   ```

---

# III. Phân tích Chi tiết Danh mục Chức năng Hệ thống (Đầy đủ 14 Use Cases)

---

## KHỐI 1: TRỢ LÝ TRA CỨU THÔNG TIN KHÁCH HÀNG (CUSTOMER RAG CHATBOT)

### 1.1. Chức năng (UC 1.1): Quản lý Tài khoản Khách hàng (Đăng ký & Đăng nhập)
* **API Endpoints & Auth:** `POST /api/auth/customer/register`, `POST /api/auth/customer/login`.
* **Dữ liệu đầu vào & Validation:**
  * `full_name`: String, 2-50 ký tự, Regex: chỉ chứa chữ cái tiếng Việt/Anh và khoảng trắng.
  * `email`: String, max 255 chars, đúng định dạng `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`.
  * `phone`: String, 10 chữ số, Regex: `^0[0-9]{9}$` (Tùy chọn).
  * `password`: String, min 8 chars, bắt buộc có ít nhất 1 chữ cái và 1 chữ số.
* **Quy trình xử lý nội bộ:**
  1. **Đăng ký:**
     - Đọc dữ liệu request, kiểm tra validation. Nếu sai trả về HTTP `422 Unprocessable Entity`.
     - Query `SELECT id FROM customers WHERE email = :email`. Nếu đã tồn tại, trả về HTTP `400 Bad Request` (`detail: "Email đã tồn tại"`).
     - Băm mật khẩu bằng Bcrypt (`password_hash = hash(password)`).
     - Chèn dòng mới vào bảng `customers` (`full_name`, `email`, `phone`, `password_hash`, `is_active = TRUE`).
     - Tạo JWT Access Token chứa payload `{ "sub": customer.id, "role": "CUSTOMER" }`.
  2. **Đăng nhập:**
     - Query `SELECT * FROM customers WHERE email = :email`. Nếu không tìm thấy, trả về HTTP `401 Unauthorized`.
     - Kiểm tra `is_active`. Nếu `FALSE`, trả về HTTP `403 Forbidden` (`detail: "Tài khoản bị tạm khóa"`).
     - Xác thực mật khẩu `verify_hash(password, password_hash)`. Nếu sai, tăng biến đếm số lần sai trong Redis (`failed_login:{email}`). Nếu chạm 5 lần/15 phút, cập nhật `is_active = FALSE` tạm thời 15 phút, trả về HTTP `401 Unauthorized` kèm số lượt còn lại.
     - Xác thực thành công: Đặt đếm sai về 0, sinh JWT Token, truy vấn phiên trò chuyện gần nhất trong `conversations` trả về kèm lịch sử 50 tin nhắn trong `messages`.
* **Kết quả & Mã lỗi HTTP:** `200 OK` (Token + Customer Info), `400`, `401`, `403`, `422`.

---

### 1.2. Chức năng (UC 1.2): Quản lý Phiên trò chuyện
* **API Endpoints:** `GET /api/customer/conversations`, `POST /api/customer/conversations`, `GET /api/customer/conversations/{id}/messages`.
* **Quy trình xử lý nội bộ:**
  1. **Tải danh sách phiên chat:**
     - Decode JWT lấy `customer_id`. Truy vấn `SELECT * FROM conversations WHERE customer_id = :customer_id ORDER BY updated_at DESC`.
     - Đối với mỗi phiên, kéo dòng tin nhắn cuối cùng trong `messages` (trích 15 từ đầu) và nhãn `mode` (`BOT`, `HUMAN`, `WAITING_HUMAN`).
  2. **Tải tin nhắn của phiên cũ (Tải phân đoạn - Pagination):**
     - Tiếp nhận `conversation_id`, query `SELECT * FROM messages WHERE conversation_id = :id ORDER BY created_at DESC LIMIT 50 OFFSET :offset`.
     - Kiểm tra `conversations.mode`:
       - Nếu `mode == 'CLOSED'`, trả về cờ `is_readonly = TRUE`.
       - Nếu `mode == 'WAITING_HUMAN'`, trả về `notice: "Cuộc trò chuyện đang chờ nhân viên hỗ trợ"`.
  3. **Tạo phiên trò chuyện mới:**
     - Chèn dòng mới vào `conversations`: `customer_id`, `mode = 'BOT'`, `is_flagged = FALSE`.
     - Chèn tin nhắn chào mừng mặc định vào `messages`: `sender_type = 'BOT'`, `content = 'Xin chào! Mình là Trợ lý tư vấn đồ dùng thú cưng. Bạn cần hỗ trợ thông tin nào hôm nay?'`.
     - Trả về `conversation_id` mới khởi tạo.
  4. **Tự động đóng phiên (Cron Job):**
     - Cron Service quét định kỳ mỗi giờ: `UPDATE conversations SET mode = 'CLOSED' WHERE updated_at < NOW() - INTERVAL '24 hours' AND mode = 'HUMAN'`.

---

### 1.3. Chức năng (UC 1.3): Tư vấn Sản phẩm & Giải đáp Chính sách Tự động (RAG Streaming & Citations)
* **API Endpoints:** `POST /api/chat/stream` (SSE Stream).
* **Dữ liệu đầu vào:** `{ "conversation_id": "UUID", "query": "String (2-1000 chars)" }`.
* **Quy trình xử lý nội bộ:**
  1. Kiểm tra validation `query`. Chèn bản ghi tin nhắn khách hàng vào `messages` (`sender_type = 'CUSTOMER'`, `content = query`).
  2. Truy vấn `conversations.mode` theo `conversation_id`:
     - Nếu `mode IN ('WAITING_HUMAN', 'HUMAN')`: Bỏ qua RAG Engine, không sinh lời đáp AI. Trả về SSE event: `data: {"status": "WAITING_HUMAN", "message": "Nhân viên đang trực tiếp hỗ trợ, vui lòng đợi..."}\n\n`. Kết thúc.
  3. Nếu `mode == 'BOT'`:
     - Gọi Embedding API chuyển `query` thành vector 1024 chiều `query_vec`.
     - Thực hiện Vector Search trên Supabase:
       ```sql
       SELECT id, document_name, content, metadata, (1 - (embedding <=> :query_vec)) AS similarity
       FROM knowledge_chunks
       WHERE (1 - (embedding <=> :query_vec)) >= 0.65
       ORDER BY similarity DESC LIMIT 3;
       ```
     - Đồng thời, nếu `query` chứa các từ khóa sản phẩm (thức ăn, hạt, cát vệ sinh, vòng cổ, chuồng, giá, còn hàng): Query bảng `products` tra cứu thông tin tồn kho `stock_quantity`, `price`, `sale_price` theo SKU/Tên.
  4. **Xử lý Fallback khi không có dữ liệu phù hợp:**
     - Nếu không có chunk nào thỏa mãn `similarity >= 0.65`:
       - Chèn tin nhắn BOT vào `messages`: `content = 'Rất tiếc, thông tin này chưa có trong tài liệu hướng dẫn của cửa hàng. Bạn có muốn kết nối trực tiếp với nhân viên tư vấn không?'`.
       - Trả về gói SSE kèm 2 nút gợi ý: `["Kết nối nhân viên", "Hỏi câu khác"]`.
       - Nếu khách chọn "Kết nối nhân viên": Thực hiện `UPDATE conversations SET mode = 'WAITING_HUMAN', is_flagged = TRUE WHERE id = :id`.
  5. **Streaming & Citations khi có dữ liệu:**
     - Đóng gói Prompt RAG: `Context = [Chunks + Product Catalog Data]`, `User Query = query`.
     - Mở luồng HTTP Response Header `Content-Type: text/event-stream`.
     - Đẩy từng token sinh ra bởi LLM về Client: `data: {"token": "..."}\n\n`.
     - Khi sinh xong, chèn bản ghi BOT vào `messages`: `sender_type = 'BOT'`, `content = full_text`, `citations = JSONB([document_name, page_number, clause, snippet])`.

---

## KHỐI 2: GIÁM SÁT HỘI THOẠI & KHỞI TẠO TICKET TỰ ĐỘNG (AI AUTO-TRIAGE)

### 2.1. Chức năng (UC 2.1): Phân tích Cảm xúc & Phát hiện Khiếu nại Ngầm
* **Tiến trình:** Background Listener Hook kích hoạt ngay khi có tin nhắn mới `sender_type = 'CUSTOMER'` được lưu vào `messages`.
* **Quy trình xử lý nội bộ:**
  1. Đọc tin nhắn mới vừa lưu + 3 tin nhắn liền trước trong cùng `conversation_id` để tạo mạch ngữ cảnh.
  2. Scann từ khóa nguy cơ khẩn cấp trong tin nhắn (`lừa đảo`, `dọa kiện`, `báo công an`, `tẩy chay`, `trả tiền đây`...):
     - Nếu chứa từ khóa nguy cơ: Ép điểm `sentiment_score = -1.00`, gán nhãn `CRITICAL`. Chuyển ngay sang Bước 5.
  3. Nếu không dính từ khóa: Gọi AI Sentiment Classifier (LLM Structured Output) tính điểm `sentiment_score` (-1.00 đến +1.00) và xếp nhãn:
     - `POSITIVE`: +0.30 đến +1.00
     - `NEUTRAL`: -0.29 đến +0.29
     - `NEGATIVE`: -0.59 đến -0.30
     - `CRITICAL`: -1.00 đến -0.60
  4. Cập nhật `UPDATE messages SET sentiment_score = :score WHERE id = :msg_id` và `UPDATE conversations SET last_sentiment = :label WHERE id = :conv_id`.
  5. So sánh `sentiment_score` với mốc ngưỡng cảnh báo trong `ai_rules` (mặc định -0.60):
     - Nếu `sentiment_score <= -0.60`: Cập nhật `UPDATE conversations SET is_flagged = TRUE WHERE id = :conv_id`. Phát tín hiệu WebSocket `FLAGGED_CONVERSATION` tới tất cả Agent đang `ONLINE`. Kích hoạt tiến trình UC 2.2 tự động mở Ticket.
     - **Quy tắc khóa an toàn cờ đỏ:** Khi `is_flagged` đã là `TRUE`, dù các tin nhắn tiếp theo có điểm `POSITIVE`, hệ thống không được tự động xóa cờ đỏ (chỉ xóa khi Agent tiếp quản hoặc đóng Ticket).

---

### 2.2. Chức năng (UC 2.2): Trích xuất Thông tin & Khởi tạo Ticket Khẩn cấp
* **Tiến trình:** Background Worker tiếp nhận tín hiệu từ UC 2.1.
* **Quy trình xử lý nội bộ:**
  1. Kiểm tra xem phiên `conversation_id` này đã có Ticket chưa hoàn thành (`status IN ('PENDING', 'IN_PROGRESS')`) hay chưa.
  2. **Trường hợp ĐÃ CÓ Ticket chưa đóng (Chống tạo trùng lặp - UC 2.2 Luồng con A-1):**
     - Bổ sung ID tin nhắn mới vào trường `ai_metadata.additional_messages` của Ticket cũ.
     - Nếu tin nhắn mới thuộc cấp P1 (điểm <= -0.80 hoặc chứa từ khóa đe dọa): Nâng mức ưu tiên của Ticket cũ lên `priority = 'P1'`, tính lại `sla_deadline = NOW() + INTERVAL '15 minutes'`, phát thông báo WebSocket cập nhật thẻ Ticket cho Agent.
  3. **Trường hợp CHƯA CÓ Ticket:**
     - Gọi LLM trích xuất dữ liệu JSON cấu trúc từ 1-10 tin nhắn gần nhất:
       - `summary`: Tóm tắt sự cố (20-255 ký tự).
       - `category`: 1 trong 6 loại (`Lỗi đơn hàng`, `Đổi trả/Hoàn tiền`, `Sản phẩm lỗi/Hư hại`, `Lỗi thanh toán`, `Thái độ phục vụ`, `Vấn đề khác`).
       - `priority`: `P1` (khi giận dữ đe dọa nặng/lỗi thanh toán), `P2` (sự cố giao hàng/sản phẩm hỏng/bức xúc vừa), `P3` (thắc mắc tiêu cực nhẹ).
  4. **Tính hạn chót SLA (Tra cứu `sla_policies`):**
     - `P1`: `sla_deadline = NOW() + INTERVAL '15 minutes'`
     - `P2`: `sla_deadline = NOW() + INTERVAL '60 minutes'`
     - `P3`: `sla_deadline = NOW() + INTERVAL '240 minutes'`
  5. Chèn bản ghi mới vào bảng `tickets` (`conversation_id`, `category`, `priority`, `status = 'PENDING'`, `summary`, `sla_deadline`, `ai_metadata`).
  6. **Cơ chế ngắt Bot AI ngay lập tức khi khẩn cấp (CRITICAL / P1):**
     - Nếu `priority == 'P1'` hoặc `last_sentiment == 'CRITICAL'`:
       - `UPDATE conversations SET mode = 'WAITING_HUMAN' WHERE id = :conv_id`.
       - Chèn tin nhắn hệ thống vào `messages`: `sender_type = 'BOT'`, `content = 'Hệ thống nhận thấy bạn cần hỗ trợ chuyên sâu, vui lòng chờ trong giây lát tư vấn viên đang vào hỗ trợ bạn.'`.
       - Đẩy sự kiện WebSocket `BOT_PAUSED_NOTICE` tới Client khách hàng.
  7. Đẩy thông điệp `TICKET_CREATED` vào **Redis Queue (`queue:tickets:pending`)**.
  8. **Fallback dự phòng khi AI lỗi (UC 2.2 Ngoại lệ E-1):** Nếu LLM trích xuất thất bại, chèn Ticket mặc định: `summary = "Cần kiểm tra thủ công - Lỗi trích xuất tự động"`, `category = "Vấn đề khác"`, `priority = "P2"`, `sla_deadline = NOW() + 60m`.

---

### 2.3. Chức năng (UC 2.3): Cấu hình Linh hoạt Quy tắc AI Rules
* **API Endpoints:** `GET /api/admin/ai-rules`, `POST /api/admin/ai-rules`, `PUT /api/admin/ai-rules/{id}`.
* **Quy trình xử lý nội bộ:**
  1. Auth Middleware giải mã JWT, kiểm tra `role IN ('MANAGER', 'ADMIN')`. Nếu là `AGENT`, trả về HTTP `403 Forbidden`.
  2. Validation trường thông tin:
     - `rule_name`: String, 1-100 chars, NOT NULL.
     - `sentiment_threshold`: Numeric, bắt buộc phải là số âm trong đoạn [-1.00, 0.00]. Nếu nhập số dương, trả về HTTP `422 Unprocessable Entity` (`detail: "Ngưỡng điểm phải là số âm từ -1.00 đến 0.00"`).
     - `target_priority`: String, CHECK (`target_priority IN ('P1', 'P2', 'P3')`).
  3. Cập nhật hoặc chèn bản ghi vào bảng `ai_rules`.
  4. Xóa Cache Redis quy tắc cũ `DEL cache:ai_rules`. Lần giám sát ngầm tiếp theo sẽ tự nạp lại quy tắc mới từ DB tức thì.
  5. Ghi nhật ký Lịch sử Cấu hình (Audit Log): Đơn vị thực hiện, thời gian, giá trị cũ và mới.

---

## KHỐI 3: CỔNG KẾT NỐI THỜI GIAN THỰC & BÀN LÀM VIỆC NHÂN VIÊN (LIVE SUPPORT CONSOLE)

### 3.1. Chức năng (UC 3.1): Quản lý Tài khoản Nhân viên (Tạo mới & Đăng nhập)
* **API Endpoints:** `POST /api/admin/users` (Tạo tài khoản), `POST /api/auth/agent/login` (Đăng nhập).
* **Quy trình xử lý nội bộ:**
  1. **Tạo tài khoản nhân sự mới (Admin/Manager):**
     - Verify JWT `role IN ('MANAGER', 'ADMIN')`.
     - Validate input: `email` (định dạng email nội bộ, unique), `full_name` (2-100 chars), `role` (`AGENT`/`MANAGER`/`ADMIN`), `skills` (Bắt buộc với AGENT: JSON Array các danh mục xử lý), `password` (min 8 chars, có chữ và số).
     - Băm mật khẩu, chèn vào bảng `users` với `status = 'OFFLINE'`, `is_active = TRUE`.
  2. **Đăng nhập Bàn làm việc CSKH (Agent Login):**
     - Verify `email` và `password_hash`. Nếu sai, trả về HTTP `401 Unauthorized`.
     - Kiểm tra `is_active`. Nếu `FALSE`, trả về HTTP `403 Forbidden` (`detail: "Tài khoản bị khóa"`).
     - Khởi tạo JWT Session làm việc (hiệu lực 24 giờ) chứa `{ "sub": user.id, "role": user.role }`.
     - Trả về Token JWT + Thông tin User. Đặt trạng thái mặc định ban đầu là `OFFLINE`.

---

### 3.2. Chức năng (UC 3.2): Quản lý Trạng thái Làm việc Nhân viên (Agent Presence)
* **API Endpoints:** `PUT /api/agent/status`.
* **Dữ liệu đầu vào:** `{ "status": "ONLINE" | "BUSY" | "OFFLINE" }`.
* **Quy trình xử lý nội bộ:**
  1. Verify JWT Agent Token.
  2. Cập nhật CSDL: `UPDATE users SET status = :status, updated_at = NOW() WHERE id = :user_id`.
  3. Cập nhật Redis Cache: `SET agent:status:{user_id} :status`.
  4. Bắn sự kiện Pub/Sub `AGENT_STATUS_CHANGED` tới Ticket Dispatcher Worker để cập nhật ngay danh sách nhân viên sẵn sàng nhận việc.
  5. **Tự động ngắt mạng (Ngoại lệ E-1):** Khi kết nối WebSocket của Agent bị rớt quá 30 giây, Heartbeat Monitor tự động cập nhật `status = 'OFFLINE'` trong Redis và DB để ngắt gán việc tự động.

---

### 3.3. Chức năng (UC 3.3): Theo dõi Hàng đợi & Tiếp quản Cuộc trò chuyện
* **API Endpoints & WS:** `GET /api/agent/conversations/queue`, `POST /api/agent/conversations/{id}/takeover`, `WS /ws/chat/{conversation_id}`.
* **Quy trình xử lý nội bộ:**
  1. **Tải danh sách Hàng đợi:**
     - Query `SELECT * FROM conversations WHERE is_flagged = TRUE OR mode = 'WAITING_HUMAN' ORDER BY updated_at DESC`.
  2. **Tiếp quản cuộc trò chuyện (Anti-Collision Takeover):**
     - Agent bấm "Tiếp quản", gửi `POST /api/agent/conversations/{id}/takeover`.
     - Gateway mở gỉa dịch với khóa dòng chống tranh chấp:
       ```sql
       SELECT assigned_agent_id, mode FROM conversations WHERE id = :id FOR UPDATE;
       ```
     - Kiểm tra `assigned_agent_id`:
       - Nếu `assigned_agent_id IS NOT NULL` và khác `current_user_id`: Rollback giao dịch, trả về HTTP `409 Conflict` (`detail: "Cuộc trò chuyện đã được nhận bởi nhân viên khác"`). Đặt màn hình của Agent hiện tại về `Read-only`.
       - Nếu `assigned_agent_id IS NULL`:
         ```sql
         UPDATE conversations
         SET assigned_agent_id = :current_user_id, mode = 'HUMAN', is_flagged = FALSE, updated_at = NOW()
         WHERE id = :id;
         ```
  3. **Phát thông báo WebSocket:**
     - WebSocket Server đẩy thông điệp `CHAT_MODE_CHANGED` vào room khách hàng: `"Nhân viên tư vấn [Tên] đã tham gia cuộc trò chuyện"`.
     - Ngắt hoàn toàn bộ máy trả lời tự động của Bot AI cho các tin nhắn tiếp theo.
  4. **Trao đổi tin nhắn 2 chiều thời gian thực:**
     - Mọi tin nhắn từ Agent hoặc Customer gửi qua WebSocket `/ws/chat/{id}` được lưu vào `messages` (`sender_type = 'AGENT'`, `sender_id`, `content`) và broadcast ngay lập tức sang phía đối diện.

---

### 3.4. Chức năng (UC 3.4): Quản lý & Sử dụng Mẫu Phản hồi Nhanh (Canned Responses)
* **API Endpoints:** `GET /api/canned-responses`, `POST /api/canned-responses`.
* **Quy trình xử lý nội bộ:**
  1. **Gợi ý nhanh khi gõ `/`:**
     - Client bắt ký tự `/`, gọi `GET /api/canned-responses?q=shortcut` (hoặc đọc từ Cache Local).
     - Query `SELECT * FROM canned_responses WHERE shortcut ILIKE :q OR title ILIKE :q`.
     - Chọn mẫu: Điền nguyên văn trường `content` vào ô soạn thảo của Agent.
  2. **Tạo mẫu phản hồi mới (Admin/Manager/Agent - UC 3.4 Luồng con A-1):**
     - Input Validation: `shortcut` (bắt buộc bắt đầu bằng `/`, không chứa khoảng trắng, 2-50 chars), `title` (3-150 chars), `category` (2-50 chars), `content` (5-2000 chars).
     - Query `SELECT id FROM canned_responses WHERE shortcut = :shortcut`. Nếu đã tồn tại, trả về HTTP `400 Bad Request` (`detail: "Phím tắt đã tồn tại"`).
     - Chèn bản ghi mới vào `canned_responses` (`created_by = current_user_id`).
     - Bắn sự kiện WebSocket `CANNED_RESPONSE_CREATED` để đồng bộ bảng gợi ý cho tất cả Agent đang trực ca.

---

## KHỐI 4: ĐIỀU PHỐI PHÂN VIỆC, GIÁM SÁT SLA & BÁO CÁO HIỆU SUẤT (DISPATCHER & SLA ENGINE)

### 4.1. Chức năng (UC 4.1): Tự động Phân chia Ticket Thông minh (Least-Loaded Dispatcher Algorithm)
* **Tiến trình:** *Ticket Dispatcher Worker* lắng nghe Redis Queue `queue:tickets:pending`.
* **Thuật toán Phân việc Tải tối thiểu (Least-Loaded Algorithm):**
  1. Worker thực hiện `RPOPLPUSH queue:tickets:pending queue:tickets:processing` lấy `ticket_id`.
  2. Query `SELECT category, priority FROM tickets WHERE id = :ticket_id`.
  3. Lọc danh sách nhân viên đủ điều kiện:
     ```sql
     SELECT id, full_name FROM users
     WHERE role = 'AGENT' AND status = 'ONLINE' AND is_active = TRUE
       AND (skills @> jsonb_build_array(:category) OR skills IS NULL);
     ```
  4. **Xử lý Không có nhân viên hợp lệ (UC 4.1 Luồng rẽ nhánh E-1):**
     - Nếu danh sách lọc rỗng: Cập nhật `UPDATE tickets SET status = 'PENDING', assigned_to = NULL WHERE id = :ticket_id`.
     - Phát tín hiệu báo động đỏ WebSocket `UNASSIGNED_TICKET_ALERT` lên màn hình Admin để phân công thủ công (UC 4.1 Luồng con A-1 via `POST /api/admin/tickets/{id}/assign`).
  5. **Tính tải công việc và Phân công (Khi có ứng viên):**
     - Đếm số lượng Ticket chưa đóng (`status IN ('PENDING', 'IN_PROGRESS')`) của từng nhân viên hợp lệ.
     - Chọn Agent có số lượng Ticket ít nhất. Nếu bằng nhau, chọn Agent có thời điểm nhận việc gần nhất xa nhất (`ORDER BY last_assigned_at ASC`).
     - Gán Ticket:
       ```sql
       UPDATE tickets SET assigned_to = :selected_agent_id, status = 'IN_PROGRESS', updated_at = NOW() WHERE id = :ticket_id;
       ```
     - Bắn sự kiện WebSocket `TICKET_ASSIGNED` về màn hình Console của Agent được nhận việc.

---

### 4.2. Chức năng (UC 4.2): Giám sát Thời hạn Xử lý Cam kết SLA & Báo động Vi phạm
* **Tiến trình:** *SLA Worker Cron Job* chạy định kỳ mỗi 30 giây.
* **Quy trình xử lý nội bộ:**
  1. Quét toàn bộ các Ticket đang mở:
     ```sql
     SELECT id, assigned_to, priority, sla_deadline, sla_breached
     FROM tickets WHERE status IN ('PENDING', 'IN_PROGRESS');
     ```
  2. **Cảnh báo Sắp hết hạn (< 20% thời lượng):**
     - Nếu `(sla_deadline - NOW()) / total_sla_duration < 0.20`: Bắn sự kiện WebSocket `SLA_WARNING` làm thẻ Ticket trên giao diện Agent chuyển sang màu vàng cam.
  3. **Xử lý Hoàn thành Đúng hạn (UC 4.2 Luồng chính step 4):**
     - Khi Agent bấm "Hoàn tất", gửi `POST /api/tickets/{id}/resolve` kèm `resolution_summary` (10-1000 chars).
     - If `NOW() <= sla_deadline`: `UPDATE tickets SET status = 'RESOLVED', resolved_at = NOW(), sla_breached = FALSE`. Ghi nhận `SLA Met`.
  4. **Xử lý Vi phạm Quá hạn SLA (UC 4.2 Luồng rẽ nhánh E-1 - SLA Breach):**
     - If `NOW() > sla_deadline` AND `sla_breached == FALSE`:
       - `UPDATE tickets SET sla_breached = TRUE WHERE id = :ticket_id`.
       - Đẩy thông điệp vi phạm vào **Redis Pub/Sub (`channel:sla_alerts`)**.
       - WebSocket Manager lắng nghe kênh Pub/Sub, chuyển tiếp tín hiệu `SLA_BREACH_ALERT` làm thẻ Ticket trên Kanban đổi sang màu đỏ nhấp nháy, bắn thông báo âm thanh báo động lên màn hình Quản lý CSKH.
       - Ghi nhận điểm trừ vi phạm SLA vào báo cáo hiệu suất của Agent phụ trách.

---

### 4.3. Chức năng (UC 4.3): Quản lý Tiến độ trên Bảng Kanban
* **API Endpoints:** `PATCH /api/tickets/{id}/status`.
* **Dữ liệu đầu vào:** `{ "status": "PENDING" | "IN_PROGRESS" | "RESOLVED" | "CLOSED", "resolution_summary": "String (10-1000 chars)" }`.
* **Quy trình xử lý nội bộ:**
  1. Verify JWT User Token và Phân quyền:
     - Nếu người thao tác là `AGENT`: Kiểm tra `tickets.assigned_to == current_user_id`. Nếu khác, trả về HTTP `403 Forbidden` (`detail: "Bạn không có quyền sửa ticket của nhân viên khác"`).
     - Nếu là `MANAGER` hoặc `ADMIN`: Cho phép cập nhật mọi Ticket.
  2. Kiểm tra Quy tắc Luân chuyển Tiến độ 1 chiều:
     - Hợp lệ: `PENDING` $\rightarrow$ `IN_PROGRESS` $\rightarrow$ `RESOLVED` $\rightarrow$ `CLOSED`.
     - Nếu kéo ngược (VD: `RESOLVED` $\rightarrow$ `IN_PROGRESS`), trả về HTTP `400 Bad Request` (`detail: "Tiến độ chỉ được phép luân chuyển tiến lên"`).
  3. Kiểm tra điều kiện chuyển `RESOLVED`: Bắt buộc `resolution_summary` không được để trống (10-1000 chars). Nếu trống, trả về HTTP `422 Unprocessable Entity`.
  4. Cập nhật `tickets`: Đặt `status = :new_status`. Nếu chuyển `RESOLVED`, dừng đồng hồ SLA đếm ngược, đặt `resolved_at = NOW()`.
  5. Broadcast sự kiện `KANBAN_TICKET_UPDATED` qua WebSocket để đồng bộ thẻ công việc trên màn hình tất cả nhân viên.

---

### 4.4. Chức năng (UC 4.4): Báo cáo Thống kê Hiệu suất
* **API Endpoints:** `GET /api/reports/analytics`, `GET /api/reports/export-excel`.
* **Dữ liệu đầu vào (Query Params):** `from_date` (YYYY-MM-DD), `to_date` (YYYY-MM-DD), `agent_id` (Optional), `priority` (Optional), `category` (Optional).
* **Quy trình xử lý nội bộ:**
  1. Verify JWT `role IN ('MANAGER', 'ADMIN')`. Nếu là `AGENT`, trả về HTTP `403 Forbidden`.
  2. Validation khoảng thời gian: `to_date >= from_date`, `(to_date - from_date) <= 365 days`, `to_date <= CURRENT_DATE`. Nếu sai, trả về HTTP `400 Bad Request`.
  3. Thực hiện các câu lệnh SQL gom nhóm (Aggregation) trên PostgreSQL:
     - **Tổng số phiếu & Phân bổ:** `SELECT category, priority, count(*) FROM tickets WHERE created_at BETWEEN :from_date AND :to_date GROUP BY category, priority;`
     - **Tỷ lệ vi phạm SLA (%):**
       $$\text{Tỷ lệ vi phạm (\%)} = \left( \frac{\text{Số phiếu } sla\_breached = \text{TRUE}}{\text{Tổng số phiếu phát sinh}} \right) \times 100\%$$
     - **Năng suất theo Agent:** Số phiếu đã giải quyết đúng hạn vs quá hạn của từng `assigned_to`.
     - **Phân bổ cảm xúc:** Gom nhóm `last_sentiment` từ `conversations`.
  4. Trả về Response JSON chi tiết cho UI dựng biểu đồ tròn/cột. Hỗ trợ xuất file Excel qua stream binary `.xlsx`.

---

# IV. Sơ đồ Luồng Tuần tự Kỹ thuật (Technical Sequence Flows)

### LUỒNG TUẦN TỰ 1: Tra cứu Tri thức RAG & Sinh câu trả lời Streaming (UC 1.3)

```text
Customer UI            FastAPI Gateway       Supabase Vector        LLM RAG Engine       Supabase DB
    |                         |              (knowledge_chunks)           |                   |
    |--- 1. POST /chat/stream>|                      |                    |                   |
    |   (Token, Query)        |                      |                    |                   |
    |                         |--- 2. Verify JWT --->|                    |                   |
    |                         |    & Get Session     |                    |                   |
    |                         |-------------------------------------------------------------->|
    |                         |    3. Check conversations.mode IN ('WAITING_HUMAN', 'HUMAN')  |
    |                         |       [If YES -> Skip LLM, return waiting notice]             |
    |                         |                                                               |
    |                         |--- 4. INSERT INTO messages (sender_type='CUSTOMER') --------->|
    |                         |<--------------------------------------------------------------|
    |                         |                      |                    |                   |
    |                         |--- 5. HNSW Vector Query (ORDER BY embedding <=> query_emb) -->|
    |                         |<-- 6. Top 3 Chunks + Metadata ------------|                   |
    |                         |                      |                    |                   |
    |                         |--- 7. Stream Prompt (Context + Query) --->|                   |
    |                         |                      |                    |                   |
    |<-- 8. SSE Text Stream --|<-- 9. Yield Token Chunk ------------------|                   |
    |    (Token-by-Token)     |                      |                    |                   |
    |                         |                      |                    |                   |
    |                         |--- 10. INSERT INTO messages (sender_type='BOT', citations) -->|
    |                         |<-- 11. OK ----------------------------------------------------|
```

---

### LUỒNG TUẦN TỰ 2: Giám sát Hội thoại Ngầm & Khởi tạo Ticket Khẩn cấp (UC 2.1 & UC 2.2)

```text
Event Listener         Supabase DB           AI Classifier           Redis Queue
      |                    |                       |                      |
      |-- 1. On Message -->|                       |                      |
      |   Created Event    |                       |                      |
      |                    |                       |                      |
      |-- 2. SELECT 3 ---->|                       |                      |
      |   Recent Messages  |                       |                      |
      |<-- 3. Messages ----|                       |                      |
      |                    |                       |                      |
      |-- 4. Request Sentiment Analysis ---------->|                      |
      |<-- 5. Sentiment Score (-0.85, CRITICAL) ---|                      |
      |                    |                       |                      |
      |-- 6. UPDATE messages (sentiment_score) --->|                      |
      |-- 7. UPDATE conversations (last_sentiment)->|                      |
      |                    |                       |                      |
      |-- 8. SELECT active rules FROM ai_rules --->|                      |
      |<-- 9. Rules List (Threshold = -0.60) ------|                      |
      |                    |                       |                      |
      |-- 10. Score (-0.85) <= Threshold (-0.60) -> Trigger Auto Ticket  |
      |                    |                       |                      |
      |-- 11. Request Structured Extraction ------>|                      |
      |<-- 12. Extracted Data (Summary, Category, Priority P1) ---------|
      |                    |                       |                      |
      |-- 13. INSERT INTO tickets (status='PENDING', priority='P1') ----->|
      |-- 14. UPDATE conversations (is_flagged = TRUE) ------------------>|
      |                    |                       |                      |
      |-- 15. IF CRITICAL -> UPDATE conversations (mode = 'WAITING_HUMAN')|
      |-- 16. INSERT System Message ("Hệ thống nhận thấy bạn cần...") ---->|
      |                    |                       |                      |
      |-- 17. LPUSH TICKET_CREATED Event -------------------------------->|
```

---

### LUỒNG TUẦN TỰ 3: Tiếp quản Phiên trò chuyện từ AI (UC 3.3)

```text
Agent UI           FastAPI Gateway          Supabase DB         WebSocket Manager       Customer UI
   |                      |                      |                      |                    |
   |-- 1. POST Takeover ->|                      |                      |                    |
   |   (conversation_id)  |                      |                      |                    |
   |                      |-- 2. SELECT FOR ---->|                      |                    |
   |                      |   UPDATE conversation|                      |                    |
   |                      |<-- 3. Row State -----|                      |                    |
   |                      |                      |                      |                    |
   |                      |-- 4. Check assigned_agent_id IS NULL?       |                    |
   |                      |   [Valid takeover]   |                      |                    |
   |                      |                      |                      |                    |
   |                      |-- 5. UPDATE conversations ----------------->|                    |
   |                      |   (assigned_agent_id, mode='HUMAN')         |                    |
   |                      |<-- 6. OK -----------------------------------|                    |
   |                      |                      |                      |                    |
   |<-- 7. 200 Success ---|                      |                      |                    |
   |                      |--- 8. Broadcast TAKEOVER Event ------------>|                    |
   |                      |                      |                      |--- 9. Push WS ---->|
   |                      |                      |                      |    System Message  |
   |                      |                      |                      |    "Agent Joined"  |
   |                      |                      |                      |                    |
   |-- 10. Send Message ->|                      |                      |                    |
   |   (WS / Chat Frame)  |-- 11. INSERT INTO messages (sender='AGENT')>|                    |
   |                      |                      |                      |-- 12. Push WS ---->|
   |                      |                      |                      |    Agent Message   |
```

---

### LUỒNG TUẦN TỰ 4: Tự động Phân chia Ticket, Giám sát SLA & Báo động Vi phạm (UC 4.1 & UC 4.2)

```text
Redis Queue/PubSub     Dispatcher Worker        SLA Worker          Supabase DB        WebSocket / UI
        |                      |                    |                    |                   |
        |-- 1. RPOPLPUSH ----->|                    |                    |                   |
        |   TICKET_CREATED     |                    |                    |                   |
        |                      |                    |                    |                   |
        |                      |-- 2. SELECT ONLINE Agents & Skills ---->|                   |
        |                      |<-- 3. Agent List -----------------------|                   |
        |                      |                    |                    |                   |
        |                      |-- 4. Count Active Tickets per Agent --->|                   |
        |                      |<-- 5. Active Counts --------------------|                   |
        |                      |                    |                    |                   |
        |                      |-- 6. Select Least-Loaded Agent          |                   |
        |                      |-- 7. UPDATE tickets (assigned_to, status='IN_PROGRESS') --->|
        |                      |                    |                    |                   |
        |                      |-- 8. Broadcast TICKET_ASSIGNED Event via WS --------------->| (To Agent UI)
        |                      |                    |                    |                   |
        |                      |                    |-- 9. Cron Scan (Every 30s)             |
        |                      |                    |-- 10. SELECT Overdue Tickets ------>|
        |                      |                    |   (NOW() > sla_deadline)               |
        |                      |<-- 11. Overdue List ------------------|                   |
        |                      |                    |                    |                   |
        |                      |                    |-- 12. UPDATE tickets (sla_breached=TRUE)|
        |                      |                    |<-- 13. OK ----------------------------|
        |                      |                    |                    |                   |
        |-- 14. PUBLISH SLA_BREACH Alert -----------|                    |                   |
        |                        (PubSub)           |                    |                   |
        |                                                                |                   |
        |------------------ 15. Listen SLA_BREACH Event ---------------->|--- 16. Push WS -->|
        |                                                                |    Red Alert      |
        |                                                                |    (To Admin UI)  |
```