# I. Thiết kế cơ sở dữ liệu (Supabase PostgreSQL & pgvector)

**1. Bảng `users` (Tài khoản & Nhân sự hệ thống)**

|**Tên trường (Column)**|**Kiểu dữ liệu (PostgreSQL)**|**Ràng buộc (Constraints)**|**Mô tả nghiệp vụ**|
|---|---|---|---|
|`id`|UUID|PK, Default: `gen_random_uuid()`|Mã định danh nhân viên/quản trị|
|`email`|VARCHAR(255)|NOT NULL, UNIQUE|Email đăng nhập và nhận thông báo|
|`password_hash`|VARCHAR(255)|NOT NULL|Mật khẩu tài khoản băm an toàn|
|`full_name`|VARCHAR(100)|NOT NULL|Họ và tên nhân viên|
|`phone`|VARCHAR(20)|NULL|Số điện thoại liên hệ|
|`role`|VARCHAR(20)|NOT NULL, Default: 'AGENT', CHECK (`role` IN ('AGENT', 'MANAGER', 'ADMIN'))|Vai trò nhân sự trong hệ thống|
|`status`|VARCHAR(20)|NOT NULL, Default: 'OFFLINE', CHECK (`status` IN ('ONLINE', 'BUSY', 'OFFLINE'))|Trạng thái làm việc của nhân viên|
|`skills`|JSONB|NULL|Danh sách các kỹ năng/danh mục xử lý chuyên môn|
|`is_active`|BOOLEAN|NOT NULL, Default: `TRUE`|Trạng thái tài khoản (khóa/mở)|
|`created_at`|TIMESTAMPTZ|NOT NULL, Default: `NOW()`|Thời gian tạo tài khoản|
|`updated_at`|TIMESTAMPTZ|NOT NULL, Default: `NOW()`|Thời gian cập nhật thông tin gần nhất|

---

**2. Bảng `customers` (Khách hàng)**
Lưu trữ định danh người dùng vãng lai hoặc tài khoản khách truy cập cổng trò chuyện.

| Tên trường (Column) | Kiểu dữ liệu (PostgreSQL) | Ràng buộc (Constraints) | Mô tả nghiệp vụ |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh khách hàng |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | Email đăng nhập và nhận thông báo |
| `password_hash` | VARCHAR(255) | NOT NULL | Mật khẩu tài khoản băm an toàn |
| `full_name` | VARCHAR(100) | NOT NULL | Họ và tên khách hàng |
| `phone` | VARCHAR(20) | NULL | Số điện thoại liên hệ |
| `is_active` | BOOLEAN | NOT NULL, Default: `TRUE` | Trạng thái tài khoản (khóa/mở) |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời gian đăng ký tài khoản |
| `updated_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời gian cập nhật thông tin gần nhất |

---

**3. Bảng `conversations` (Phiên hội thoại)**

|**Tên trường (Column)**|**Kiểu dữ liệu (PostgreSQL)**|**Ràng buộc (Constraints)**|**Mô tả nghiệp vụ**|
|---|---|---|---|
|`id`|UUID|PK, Default: `gen_random_uuid()`|Mã định danh phiên hội thoại|
|`customer_id`|UUID|FK $\rightarrow$ `customers(id)`, NOT NULL|Khách hàng sở hữu phiên chat|
|`assigned_agent_id`|UUID|FK $\rightarrow$ `users(id)`, NULL|Nhân viên đang tiếp quản phiên (NULL nếu AI đang chat)|
|`mode`|VARCHAR(20)|NOT NULL, Default: 'BOT', CHECK (`mode` IN ('BOT', 'HUMAN', 'WAITING_HUMAN'))|Chế độ hội thoại: Trợ lý ảo hay Nhân viên trực tiếp|
|`is_flagged`|BOOLEAN|NOT NULL, Default: `FALSE`|Cờ cảnh báo nguy cơ khủng hoảng/cảm xúc tiêu cực|
|`last_sentiment`|VARCHAR(20)|NULL, CHECK (`last_sentiment` IN ('POSITIVE', 'NEUTRAL', 'NEGATIVE', 'CRITICAL'))|Đánh giá cảm xúc ở tin nhắn gần nhất|
|`created_at`|TIMESTAMPTZ|NOT NULL, Default: `NOW()`|Thời gian bắt đầu phiên|
|`updated_at`|TIMESTAMPTZ|NOT NULL, Default: `NOW()`|Thời gian có cập nhật tin nhắn mới|

---

**4. Bảng `messages` (Tin nhắn hội thoại)**
Lưu vết chi tiết trao đổi, hỗ trợ trích dẫn RAG và dữ liệu ngữ cảnh cho giám sát AI.

| **Tên trường (Column)** | **Kiểu dữ liệu (PostgreSQL)** | **Ràng buộc (Constraints)** | **Mô tả nghiệp vụ** |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh tin nhắn |
| `conversation_id` | UUID | FK $\rightarrow$ `conversations(id)` ON DELETE CASCADE, NOT NULL | Phiên chat chứa tin nhắn này |
| `sender_type` | VARCHAR(10) | NOT NULL, CHECK (`sender_type` IN ('CUSTOMER', 'BOT', 'AGENT')) | Đối tượng gửi tin |
| `sender_id` | UUID | NULL | ID nhân viên (nếu `sender_type` = 'AGENT') |
| `content` | TEXT | NOT NULL | Nội dung văn bản của tin nhắn |
| `citations` | JSONB | NULL | Dữ liệu trích dẫn nguồn RAG (Metadata chunk, tài liệu tham khảo) |
| `sentiment_score` | NUMERIC(4, 2) | NULL | Điểm số cảm xúc của tin nhắn (tính toán ngầm từ AI) |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm gửi tin nhắn |

---

**5. Bảng `tickets` (Phiếu khiếu nại & yêu cầu hỗ trợ)**
Lưu trữ thông tin xử lý sự cố, phân tích cấu trúc AI, phân công và kiểm soát SLA.

|**Tên trường (Column)**|**Kiểu dữ liệu (PostgreSQL)**|**Ràng buộc (Constraints)**|**Mô tả nghiệp vụ**|
|---|---|---|---|
|`id`|UUID|PK, Default: `gen_random_uuid()`|Mã định danh Ticket|
|`conversation_id`|UUID|FK $\rightarrow$ `conversations(id)`, NOT NULL|Phiên chat phát sinh Ticket|
|`assigned_to`|UUID|FK $\rightarrow$ `users(id)`, NULL|Nhân viên tiếp nhận xử lý (NULL nếu đang chờ phân bổ)|
|`category`|VARCHAR(50)|NOT NULL|Danh mục sự cố (VD: Đổi trả hàng, Bảo hành, Giao hàng)|
|`priority`|VARCHAR(10)|NOT NULL, CHECK (`priority` IN ('P1', 'P2', 'P3'))|Mức độ ưu tiên do AI gán (P1: Khẩn cấp, P2: Cao, P3: Vừa)|
|`status`|VARCHAR(20)|NOT NULL, Default: 'PENDING', CHECK (`status` IN ('PENDING', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'))|Trạng thái tiến độ trên bảng Kanban|
|`summary`|TEXT|NOT NULL|Tóm tắt sự cố được AI trích xuất tự động|
|`ai_metadata`|JSONB|NULL|Cấu trúc phân tích AI: Sentiment, intent, lý do phân loại|
|`sla_deadline`|TIMESTAMPTZ|NOT NULL|Hạn chót cam kết giải quyết Ticket|
|`sla_breached`|BOOLEAN|NOT NULL, Default: `FALSE`|Đánh dấu vi phạm quá hạn cam kết xử lý|
|`resolved_at`|TIMESTAMPTZ|NULL|Thời điểm Ticket chuyển sang trạng thái RESOLVED|
|`created_at`|TIMESTAMPTZ|NOT NULL, Default: `NOW()`|Thời điểm tạo ticket|
|`updated_at`|TIMESTAMPTZ|NOT NULL, Default: `NOW()`|Thời gian cập nhật trạng thái gần nhất|

---

**6. Bảng `sla_policies` (Chính sách cam kết chất lượng)**
Cung cấp căn cứ tính toán thời hạn xử lý tự động cho động cơ SLA.

|**Tên trường (Column)**|**Kiểu dữ liệu (PostgreSQL)**|**Ràng buộc (Constraints)**|**Mô tả nghiệp vụ**|
|---|---|---|---|
|`id`|UUID|PK, Default: `gen_random_uuid()`|Mã chính sách SLA|
|`priority`|VARCHAR(10)|UNIQUE, NOT NULL, CHECK (`priority` IN ('P1', 'P2', 'P3'))|Mức độ ưu tiên áp dụng|
|`resolution_time_minutes`|INT|NOT NULL|Thời gian tối đa quy định phải xử lý xong (phút)|
|`escalation_notify_to`|VARCHAR(20)|NOT NULL, Default: 'MANAGER'|Đối tượng nhận cảnh báo khi vi phạm (Lead/Manager)|
|`created_at`|TIMESTAMPTZ|NOT NULL, Default: `NOW()`|Thời gian cấu hình chính sách|

---

**7. Bảng `canned_responses` (Mẫu phản hồi nhanh)**
Hỗ trợ nhân viên gửi nhanh các mẫu trả lời chuẩn bị sẵn qua bàn làm việc thời gian thực.

| **Tên trường (Column)** | **Kiểu dữ liệu (PostgreSQL)** | **Ràng buộc (Constraints)** | **Mô tả nghiệp vụ** |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã mẫu phản hồi |
| `shortcut` | VARCHAR(50) | NOT NULL, UNIQUE | Phím tắt kích hoạt nhanh (VD: `/chao`, `/xloi`) |
| `title` | VARCHAR(150) | NOT NULL | Tiêu đề danh mục câu trả lời |
| `content` | TEXT | NOT NULL | Nội dung định dạng sẵn tự động điền vào ô chat |
| `category` | VARCHAR(50) | NOT NULL | Danh mục nghiệp vụ của mẫu trả lời |
| `created_by` | UUID | FK $\rightarrow$ `users(id)`, NOT NULL | Quản lý/Nhân viên khởi tạo |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm tạo câu phản hồi mẫu |

---

**8. Bảng `ai_rules` (Quy tắc kích hoạt & Ngưỡng cảm xúc AI)**
Cho phép Quản lý CSKH tùy biến điều kiện tạo ticket tự động mà không cần sửa code.

|**Tên trường (Column)**|**Kiểu dữ liệu (PostgreSQL)**|**Ràng buộc (Constraints)**|**Mô tả nghiệp vụ**|
|---|---|---|---|
|`id`|UUID|PK, Default: `gen_random_uuid()`|Mã quy tắc phân loại|
|`rule_name`|VARCHAR(100)|NOT NULL|Tên định danh quy tắc (VD: Phát hiện giận dữ cấp độ cao)|
|`sentiment_threshold`|NUMERIC(4, 2)|NOT NULL|Ngưỡng điểm cảm xúc kích hoạt mở ticket ngầm|
|`target_priority`|VARCHAR(10)|NOT NULL, CHECK (`target_priority` IN ('P1', 'P2', 'P3'))|Mức độ ưu tiên sẽ gán tự động khi chạm ngưỡng|
|`is_active`|BOOLEAN|NOT NULL, Default: `TRUE`|Trạng thái kích hoạt áp dụng của quy tắc|
|`created_at`|TIMESTAMPTZ|NOT NULL, Default: `NOW()`|Thời gian tạo quy tắc|

---

**9. Bảng `knowledge_chunks` (Lưu trữ tài liệu RAG & Vector Embedding - Supabase pgvector)**
Lưu trữ toàn bộ các đoạn văn bản chia nhỏ từ tài liệu chính sách cùng vector nhúng ngữ nghĩa.

|**Tên trường (Column)**|**Kiểu dữ liệu (PostgreSQL)**|**Ràng buộc (Constraints)**|**Mô tả nghiệp vụ**|
|---|---|---|---|
|`id`|UUID|PK, Default: `gen_random_uuid()`|Mã định danh đoạn trích tài liệu|
|`document_name`|VARCHAR(255)|NOT NULL|Tên tài liệu/chính sách (VD: `Chinh_sach_doi_tra.pdf`)|
|`content`|TEXT|NOT NULL|Nội dung đoạn văn bản đã chia nhỏ (chunk)|
|`embedding`|VECTOR(1024)|NULL|Vector nhúng ngữ nghĩa (1024 chiều)|
|`metadata`|JSONB|NULL|Siêu dữ liệu: Số trang, chương, điều khoản phục vụ trích dẫn Citations|
|`created_at`|TIMESTAMPTZ|NOT NULL, Default: `NOW()`|Thời điểm lưu dữ liệu|

Dựa theo chuẩn định dạng và phong cách trình bày trong tài liệu `phantichhethong.md` của bạn, dưới đây là bảng đặc tả chi tiết cho **Bảng `products**` cùng câu lệnh DDL hoàn chỉnh để bạn đưa trực tiếp vào phần thiết kế cơ sở dữ liệu:

---

**10. Bảng `products` (Danh mục & Tồn kho sản phẩm thú cưng)**
Lưu trữ thông tin định lượng, phân loại và trạng thái kho thực tế của các sản phẩm đồ dùng thú cưng phục vụ kiểm tra tức thời (Real-time catalog lookup) kết hợp cùng mô hình RAG.

| **Tên trường (Column)** | **Kiểu dữ liệu (PostgreSQL)** | **Ràng buộc (Constraints)** | **Mô tả nghiệp vụ** |
| --- | --- | --- | --- |
| `id` | UUID | PK, Default: `gen_random_uuid()` | Mã định danh duy nhất của sản phẩm |
| `sku` | VARCHAR(50) | NOT NULL, UNIQUE | Mã quản lý kho hàng (VD: `CAT-ROYAL-INDOOR-2KG`) |
| `name` | VARCHAR(255) | NOT NULL | Tên thương mại đầy đủ của sản phẩm |
| `category` | VARCHAR(100) | NOT NULL | Danh mục sản phẩm (VD: Thức ăn, Cát vệ sinh, Phụ kiện, Đồ chơi) |
| `pet_type` | VARCHAR(50) | NOT NULL, CHECK (`pet_type` IN ('DOG', 'CAT', 'BIRD', 'ALL', 'OTHER')) | Đối tượng vật nuôi áp dụng |
| `price` | NUMERIC(12, 2) | NOT NULL, CHECK (`price` >= 0) | Giá niêm yết bán lẻ hiện tại |
| `sale_price` | NUMERIC(12, 2) | NULL, CHECK (`sale_price` >= 0) | Giá khuyến mãi (nếu có chương trình giảm giá) |
| `stock_quantity` | INT | NOT NULL, Default: 0, CHECK (`stock_quantity` >= 0) | Số lượng tồn kho thực tế |
| `status` | VARCHAR(20) | NOT NULL, Default: 'IN_STOCK', CHECK (`status` IN ('IN_STOCK', 'OUT_OF_STOCK', 'DISCONTINUED')) | Trạng thái kinh doanh sản phẩm |
| `attributes` | JSONB | NULL | Thuộc tính linh hoạt cho đồ thú cưng: trọng lượng, kích cỡ, hương vị, xuất xứ |
| `description` | TEXT | NULL | Tóm tắt thông tin sản phẩm hiển thị nhanh |
| `created_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm tạo sản phẩm trong hệ thống |
| `updated_at` | TIMESTAMPTZ | NOT NULL, Default: `NOW()` | Thời điểm cập nhật giá/tồn kho gần nhất |

---

# II. Kiến trúc Kỹ thuật Thời gian thực & Xử lý Sự kiện (Real-time Architecture)

Hệ thống được thiết kế theo kiến trúc hướng sự kiện (Event-Driven Architecture) kết hợp với **Supabase PostgreSQL** làm cơ sở dữ liệu trung tâm lưu trữ cả dữ liệu quan hệ lẫn vector nhúng `pgvector`:

```
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
   | HNSW Index)      |  |                 |  |  8 Tables) |  |                   |
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

### 1. Cơ chế Truyền dữ liệu Phản hồi gõ chữ (SSE - Server-Sent Events)
* **Phân hệ sử dụng:** Khối 1 — Trợ lý Tra cứu Thông tin Khách hàng (RAG Chatbot).
* **Nguyên lý hoạt động:**
  * Khách hàng gửi câu hỏi thông qua HTTP POST request tới endpoint `/api/chat/stream`.
  * Gateway kiểm tra `conversations.mode`. Nếu `mode == 'WAITING_HUMAN'`, Gateway bỏ qua luồng LLM và trả về phản hồi giữ nguyên trạng thái chờ nhân viên.
  * Nếu `mode == 'BOT'`, Gateway chuyển câu hỏi thành vector nhúng, thực hiện truy vấn tương đồng Cosine (`vector_cosine_ops`) trên bảng `knowledge_chunks` của **Supabase PostgreSQL** qua ORM.
  * Đưa ngữ cảnh đoạn trích kết quả vào Prompt gọi LLM RAG Engine dưới dạng luồng (Streaming API).
  * FastAPI trả về cho Client một HTTP Response với Header `Content-Type: text/event-stream`.
  * Các mảng ký tự (chunks) câu trả lời do LLM sinh ra được đẩy ngay lập tức về Client theo định dạng `data: {"token": "..."}\n\n`.
  * Trình duyệt Client lắng nghe sự kiện `onmessage` và ghép từng ký tự vào khung chat theo thời gian thực mà không cần duy trì kết nối hai chiều đắt đỏ như WebSocket.

### 2. Kênh Kết nối Thời gian thực hai chiều (WebSocket Gateway)
* **Phân hệ sử dụng:** Khối 3 (Live Support Console) & Khối 1 (Khi nhân viên tiếp quản).
* **Nguyên lý hoạt động:**
  * **Quản lý kết nối (Connection Pool & Rooms):** Hệ thống WebSocket Server duy trì các phòng chat theo mã cuộc trò chuyện `room_conversation_{id}` và phòng cá nhân nhân viên `room_agent_{id}`.
  * **Đồng bộ tin nhắn hai chiều:** Khi phiên chat chuyển sang `mode = 'HUMAN'`, toàn bộ tin nhắn từ khách hàng hoặc nhân viên được truyền qua kết nối WebSocket song lập (`/ws/chat/{conversation_id}`).
  * **Thông báo sự kiện thời gian thực (Event Broadcast):**
    * Khi phát hiện nguy cơ CRITICAL ở Khối 2, hệ thống đẩy sự kiện `BOT_PAUSED_NOTICE` báo khách hàng chờ tư vấn viên và cập nhật `mode = 'WAITING_HUMAN'`.
    * Khi nhân viên bấm tiếp quản, WebSocket gửi sự kiện `TAKEOVER_SUCCESS` về phía khách hàng và ngắt hoàn toàn máy bot.
    * Khi có phiên chat mới bị gắn cờ cảnh báo (`is_flagged = TRUE`), WebSocket Server phát tín hiệu `FLAGGED_CONVERSATION` tới toàn bộ màn hình của các nhân viên đang `ONLINE`.

### 3. Hàng đợi Sự kiện & Pub/Sub ngầm (Redis Event Queue & Pub/Sub)
* **Phân hệ sử dụng:** Tích hợp giữa Khối 2 (AI Auto-Triage), Khối 4 (Ticket Dispatcher) và Khối 3 (Live Support Console).
* **Nguyên lý hoạt động:**
  * **Redis Queue (`queue:tickets:pending`):** Khi Khối 2 tự động mở một Ticket khẩn cấp mới, thông điệp JSON chứa thông tin Ticket được đẩy (`LPUSH`) vào hàng đợi Redis. Tiến trình ngầm *Ticket Dispatcher Worker* chờ nhận thông điệp (`RPOPLPUSH`) để thực hiện thuật toán chia việc Least-Loaded bất đồng bộ mà không làm nghẽn luồng xử lý chính.
  * **Redis Pub/Sub (`channel:sla_alerts`):** Động cơ SLA quét định kỳ phát hiện Ticket vi phạm quá hạn (`sla_breached = TRUE`), lập tức `PUBLISH` thông điệp vi phạm vào kênh Redis. Kênh này được WebSocket Gateway lắng nghe và chuyển tiếp ngay lập tức đến giao diện của Quản lý CSKH dưới dạng chuông/thông báo đỏ khẩn cấp.
  * **Redis Cache Trạng thái Nhân viên:** Lưu trữ trạng thái hoạt động tức thời của nhân viên (`agent:status:{user_id}` = ONLINE/BUSY/OFFLINE) và đếm số việc đang mở giúp thuật toán Least-Loaded phân chia công việc nhanh trong $O(1)$.

### 4. Lưu trữ & Truy vấn Vector Ngữ nghĩa (Supabase pgvector Engine)
* **Phân hệ sử dụng:** Khối 1 — Trợ lý Tra cứu Thông tin Khách hàng.
* **Nguyên lý hoạt động:**
  * Dữ liệu tài liệu chính sách (PDF/Docx) được chia nhỏ thành các đoạn văn bản (chunks).
  * Hệ thống tạo vector nhúng (Embedding) và chèn dữ liệu vào bảng `knowledge_chunks` trên **Supabase PostgreSQL**.
  * Chỉ mục **HNSW Index (`vector_cosine_ops`)** đảm bảo truy vấn khoảng cách Cosine đạt tốc độ vài miligiây.
  * Khi khách hàng đặt câu hỏi, Gateway tạo vector query và thực hiện phép so sánh khoảng cách Cosine trực tiếp bằng SQL/ORM trên Supabase:
    ```sql
    SELECT id, document_name, content, metadata
    FROM knowledge_chunks
    ORDER BY embedding <=> query_embedding
    LIMIT 3;
    ```
  * Siêu dữ liệu trong trường `metadata` (số trang, chương, điều khoản) được trích xuất để đóng gói vào trường `citations` (JSONB) trong bảng `messages`.

---

# III. Phân tích Chi tiết Danh mục Chức năng Hệ thống

Dưới đây là mô tả chi tiết quy trình xử lý nội bộ, dữ liệu đầu vào/đầu ra và cách các cấu phần hệ thống (API Gateway, Supabase PostgreSQL, Redis, WebSocket) tương tác với nhau để thực hiện từng chức năng theo 4 khối:

## KHỐI 1: TRỢ LÝ TRA CỨU THÔNG TIN KHÁCH HÀNG (CUSTOMER RAG CHATBOT)

### 1.1. Chức năng: Đăng ký / Đăng nhập & Khởi tạo Phiên trò chuyện
* **Tác nhân:** Khách hàng (Client UI).
* **Dữ liệu đầu vào:** Email, mật khẩu, họ tên, số điện thoại (khi đăng ký) hoặc Email, mật khẩu (khi đăng nhập).
* **Quy trình xử lý nội bộ:**
  1. Gateway tiếp nhận request tại `/auth/customer/register` hoặc `/auth/customer/login`.
  2. Truy vấn bảng `customers` trên Supabase kiểm tra email và mật khẩu băm (`password_hash`).
  3. Khi đăng nhập thành công, sinh mã Token JWT chứa Payload `customer_id`.
  4. Client truy cập khung chat, gửi JWT token qua WebSocket hoặc HTTP Header.
  5. Gateway giải mã JWT, lấy `customer_id` và truy vấn bảng `conversations` tìm phiên chat gần nhất có `mode != 'CLOSED'`.
  6. Nếu chưa có phiên, chèn bản ghi mới vào bảng `conversations` (`mode = 'BOT'`, `customer_id`). Nếu đã có, truy vấn bảng `messages` kéo 50 tin nhắn gần nhất trả về Client UI.
* **Kết quả đầu ra:** Chuỗi JWT Token, thông tin khách hàng và lịch sử tin nhắn của phiên chat hiện tại.
* **Xử lý ngoại lệ:** Email trùng báo lỗi `400 Bad Request`; Sai mật khẩu báo lỗi `401 Unauthorized`.

### 1.2. Chức năng: Tra cứu Tri thức RAG & Sinh câu trả lời Streaming (Bao gồm Citations & Fallback)
* **Tác nhân:** Khách hàng.
* **Dữ liệu đầu vào:** Câu hỏi văn bản, mã phiên chat (`conversation_id`).
* **Quy trình xử lý nội bộ:**
  1. Ghi nhận tin nhắn người dùng vào bảng `messages` (`sender_type = 'CUSTOMER'`).
  2. Gateway truy vấn bảng `conversations` kiểm tra `mode`. Nếu `mode == 'WAITING_HUMAN'` hoặc `mode == 'HUMAN'`, bỏ qua luồng gọi AI RAG, dừng trả lời tự động để chờ nhân viên trực tiếp hỗ trợ.
  3. Nếu `mode == 'BOT'`, câu hỏi được chuyển tiếp vào **Module RAG Pipeline Xử lý Nâng cao (Kiến trúc KH-06: Hybrid RAG + Sub-query Decomposition & Per-subquery Intent Router)**:
     * Giải quyết đồng tham chiếu (Coreference Resolution) & Bẻ câu hỏi phức tạp thành các `sub_queries` nguyên tử.
     * Phân loại Intent & gán Target Source độc lập cho từng `sub_query` (`SQL_PRODUCT`, `VECTOR_KNOWLEDGE`, `OUT_OF_DOMAIN`, `GREETING_CHITCHAT`, `HUMAN_AGENT_REQUEST`) dựa trên phạm vi cửa hàng.
     * Thực thi truy vấn song song hai nguồn dữ liệu: CSDL Quan hệ `products` (giá, tồn kho real-time) và Supabase `pgvector` trên bảng `knowledge_chunks` (chính sách, FAQ, hướng dẫn sử dụng).
     * Loại bỏ hoàn toàn cơ chế Score Thresholding, xử lý Fallback Out-of-domain linh hoạt cho từng ý ngoài phạm vi và gợi ý kết nối nhân viên tư vấn.
     > 📌 **Chi tiết Kỹ thuật Module RAG Pipeline KH-06**:
     > Toàn bộ kiến trúc chi tiết từ A-Z, sơ đồ luồng dữ liệu song song, đặc tả 2 Prompts LLM (`MERGED_DECOMPOSER_PROMPT` tích hợp `# DOMAIN BOUNDARY SCOPE` và `MULTI_CONTEXT_SYNTHESIZER_PROMPT`), cấu trúc JSON Schema và kịch bản testcase thực nghiệm được đặc tả chi tiết tại:
     > 👉 [**Đặc tả Kiến trúc Kỹ thuật & Luồng Xử lý RAG KH-06 Nâng cấp**](file:///d:/Study/TLU/kiemthu/project/docs/overview/kh06_revised_architecture.md).
  4. Sau khi Context Aggregator hợp nhất ngữ cảnh từ SQL, Vector DB và thông báo Fallback, LLM Multi-Context Synthesizer sinh câu trả lời hoàn chỉnh dưới dạng luồng **SSE (`text/event-stream`)** đẩy từng token về Client UI.
  5. Khi hoàn tất, tạo bản ghi mới trong bảng `messages`: `sender_type = 'BOT'`, `content` = văn bản hoàn chỉnh, `citations` = JSONB chứa thông tin trích dẫn từ `metadata` của `knowledge_chunks`.
* **Kết quả đầu ra:** Luồng gõ chữ trực tiếp trên khung chat, thông tin trích dẫn minh bạch và bản ghi tin nhắn mới trong CSDL Supabase.
* **Xử lý ngoại lệ:** Lỗi kết nối LLM/Supabase $\rightarrow$ trả về câu thông báo lỗi hệ thống tạm thời.

---

## KHỐI 2: GIÁM SÁT HỘI THOẠI & KHỞI TẠO TICKET TỰ ĐỘNG (AI AUTO-TRIAGE)

### 2.1. Chức năng: Giám sát Hội thoại Ngầm, Phân tích Cảm xúc & Tự động Khởi tạo Ticket Khẩn cấp
* **Tác nhân:** Tiến trình ngầm (Event Listener Hook & AI Engine).
* **Dữ liệu đầu vào:** Tin nhắn mới từ phía khách hàng (`message_id`, `content`, `conversation_id`).
* **Quy trình xử lý nội bộ:**
  1. Khi tin nhắn `sender_type = 'CUSTOMER'` được chèn vào bảng `messages`, Listener bắt sự kiện và truy vấn 3 tin nhắn liền trước trong cùng `conversation_id`.
  2. Đóng gói chuỗi hội thoại gửi tới mô hình AI Phân tích Cảm xúc (Structured Output LLM) để tính chỉ số `sentiment_score` (-1.00 đến +1.00) và xếp loại (POSITIVE, NEUTRAL, NEGATIVE, CRITICAL).
  3. Cập nhật `sentiment_score` trong bảng `messages` và `last_sentiment` trong bảng `conversations`.
  4. Nạp các quy tắc kích hoạt từ bảng `ai_rules`. So sánh `sentiment_score` với ngưỡng `sentiment_threshold`.
  5. Nếu chạm/vượt ngưỡng nguy cơ:
     * Gọi LLM trích xuất dữ liệu có cấu trúc: tóm tắt sự cố (`summary`), danh mục lỗi (`category`), mức ưu tiên (`priority` = P1/P2/P3).
     * Tra cứu bảng `sla_policies` để tính `sla_deadline = NOW() + resolution_time_minutes`.
     * Chèn bản ghi mới vào bảng `tickets`: `conversation_id`, `category`, `priority`, `summary`, `status = 'PENDING'`, `sla_deadline`, `ai_metadata`.
     * Cập nhật bảng `conversations`: bật cờ `is_flagged = TRUE`.
     * **Xử lý ngắt Bot AI ngay lập tức khi gặp nguy cơ CRITICAL:** Khi phát hiện mức độ giận dữ ở cấp độ nghiêm trọng (CRITICAL):
       * Hệ thống cập nhật bảng `conversations`: `mode = 'WAITING_HUMAN'`.
       * Tự động tạo một tin nhắn hệ thống trong bảng `messages`: `sender_type = 'BOT'`, `content = 'Hệ thống nhận thấy bạn cần hỗ trợ chuyên sâu, vui lòng chờ trong giây lát tư vấn viên đang vào hỗ trợ bạn.'`.
       * Đẩy thông điệp tin nhắn hệ thống qua WebSocket tới giao diện khách hàng. Các lượt chat tiếp theo của khách hàng sẽ không kích hoạt AI trả lời tự động nữa.
     * Đẩy gói thông điệp `TICKET_CREATED` vào **Redis Queue (`queue:tickets:pending`)**.
* **Kết quả đầu ra:** Điểm cảm xúc được ghi nhận, Ticket khẩn cấp được khởi tạo ngầm, AI Bot ngắt trả lời tự động nếu khẩn cấp và bắn sự kiện qua Redis Queue.
* **Xử lý ngoại lệ:** Nếu điểm cảm xúc ở ngưỡng an toàn $\rightarrow$ kết thúc tiến trình, không mở Ticket.

### 2.2. Chức năng: Cấu hình Linh hoạt Quy tắc AI Rules
* **Tác nhân:** Quản lý CSKH (Manager / Admin).
* **Dữ liệu đầu vào:** Thông tin quy tắc mới hoặc cập nhật (tên quy tắc, ngưỡng cảm xúc, mức ưu tiên gán, trạng thái kích hoạt).
* **Quy trình xử lý nội bộ:**
  1. Quản lý truy cập trang Cấu hình AI Rules trên màn hình Admin.
  2. Gửi request `POST /api/admin/ai-rules` hoặc `PUT /api/admin/ai-rules/{id}`.
  3. Gateway kiểm tra quyền tài khoản (`role IN ('MANAGER', 'ADMIN')`).
  4. Cập nhật/Chèn bản ghi vào bảng `ai_rules`.
  5. Xóa Cache quy tắc cũ trong Redis để tiến trình AI Auto-Triage tự nạp quy tắc mới ngay lập tức.
* **Kết quả đầu ra:** Bản ghi quy tắc phân loại mới áp dụng tức thì cho hệ thống.

---

## KHỐI 3: CỔNG KẾT NỐI THỜI GIAN THỰC & BÀN LÀM VIỆC NHÂN VIÊN (LIVE SUPPORT CONSOLE)

### 3.1. Chức năng: Giám sát Hàng đợi & Tiếp quản Cuộc trò chuyện
* **Tác nhân:** Nhân viên CSKH (Agent).
* **Dữ liệu đầu vào:** Trạng thái trực tuyến của nhân viên và thao tác nhấn nút "Tiếp quản" trên phiên chat (`conversation_id`).
* **Quy trình xử lý nội bộ:**
  1. Màn hình Console truy vấn `GET /api/agent/conversations?is_flagged=true` và lắng nghe kênh WebSocket để lấy danh sách cuộc trò chuyện cần hỗ trợ (các phiên `is_flagged = TRUE` hoặc `mode = 'WAITING_HUMAN'`).
  2. Nhân viên bấm tiếp quản, gửi request `POST /api/agent/conversations/{id}/takeover`.
  3. Gateway thực hiện khóa dòng (`SELECT FOR UPDATE`) trong `conversations`.
  4. Kiểm tra `assigned_agent_id`:
     * Nếu đã có người tiếp quản trước đó $\rightarrow$ Trả về `409 Conflict`, đặt màn hình của Agent hiện tại về "Read-only".
     * Nếu chưa ai nhận $\rightarrow$ Cập nhật `assigned_agent_id = current_user_id`, `mode = 'HUMAN'`, `is_flagged = FALSE`.
  5. Phát thông điệp qua WebSocket Server đến khách hàng: sự kiện `CHAT_MODE_CHANGED` báo *"Nhân viên hỗ trợ đã tham gia"*, đồng thời duy trì việc ngắt bộ máy trả lời tự động của BOT.
* **Kết quả đầu ra:** Quyền điều khiển thuộc về nhân viên; khách hàng nhận thông báo chuyển giao qua WebSocket.

### 3.2. Chức năng: Nhắn tin Hai chiều Thời gian thực & Phản hồi Nhanh theo Mẫu
* **Tác nhân:** Khách hàng và Nhân viên CSKH.
* **Dữ liệu đầu vào:** Tin nhắn văn bản hoặc phím tắt (VD: `/chao`, `/xloi`) qua kết nối WebSocket.
* **Quy trình xử lý nội bộ:**
  1. Khi nhân viên gõ phím tắt `/`, Client đọc bảng `canned_responses` tự động điền mẫu câu trả lời chuẩn bị sẵn vào ô nhập tin nhắn.
  2. Khi gửi tin nhắn, WebSocket Gateway lưu bản ghi mới vào bảng `messages` (`sender_type` = 'AGENT' hoặc 'CUSTOMER', `sender_id`, `content`).
  3. Cập nhật mốc thời gian `updated_at` trong bảng `conversations`.
  4. Đẩy gói tin qua kênh WebSocket để hiển thị tức thì trên cả màn hình Khách hàng và Nhân viên.
* **Kết quả đầu ra:** Tin nhắn hiển thị tức thì hai chiều giữa Khách hàng và Nhân viên.

### 3.3. Chức năng: Quản lý Trạng thái Làm việc Nhân viên (Agent Presence)
* **Tác nhân:** Nhân viên CSKH.
* **Dữ liệu đầu vào:** Thao tác chọn trạng thái (ONLINE, BUSY, OFFLINE) trên Console.
* **Quy trình xử lý nội bộ:**
  1. Gửi request `PUT /api/agent/status` với Payload `status`.
  2. Cập nhật trường `status` trong bảng `users`.
  3. Cập nhật trạng thái tức thời vào **Redis Cache (`agent:status:{user_id}`)**.
  4. Bắn sự kiện `AGENT_STATUS_CHANGED` sang bộ điều phối Ticket Dispatcher để cập nhật danh sách trực ca.
* **Kết quả đầu ra:** Trạng thái làm việc mới của nhân viên được ghi nhận toàn hệ thống.

---

## KHỐI 4: ĐIỀU PHỐI PHÂN VIỆC, GIÁM SÁT SLA & BÁO CÁO HIỆU SUẤT (DISPATCHER & SLA ENGINE)

### 4.1. Chức năng: Tự động Phân chia Ticket Thông minh (Least-Loaded Dispatcher Algorithm)
* **Tác nhân:** Tiến trình ngầm (Ticket Dispatcher Worker).
* **Dữ liệu đầu vào:** Sự kiện `TICKET_CREATED` từ Redis Queue (`queue:tickets:pending`).
* **Quy trình xử lý nội bộ:**
  1. Dispatcher Worker nhận `ticket_id` từ Redis Queue.
  2. Truy vấn bảng `tickets` lấy thông tin `category` và `priority` của Ticket.
  3. Quét bảng `users` (hoặc đọc Redis Cache) lọc các nhân viên thỏa mãn: `status = 'ONLINE'` và `skills` chứa `category`.
  4. Nếu không có ai phù hợp $\rightarrow$ Đặt Ticket ở trạng thái `assigned_to = NULL`, `status = 'PENDING'` và phát cảnh báo lên màn hình Admin.
  5. Nếu có nhân viên phù hợp $\rightarrow$ Đếm số lượng Ticket đang xử lý của từng người, chọn nhân viên có ít việc nhất (Least-Loaded).
  6. Cập nhật `tickets`: `assigned_to = selected_agent_id`, `status = 'IN_PROGRESS'`.
  7. Đẩy thông báo WebSocket `TICKET_ASSIGNED` về màn hình của nhân viên được gán.
* **Kết quả đầu ra:** Ticket được gán cho nhân viên phù hợp và hiển thị trên bảng việc cá nhân.

### 4.2. Chức năng: Giám sát Cam kết SLA & Báo động Vi phạm (SLA Engine & Escalation)
* **Tác nhân:** Tiến trình ngầm (SLA Worker) & Redis Pub/Sub.
* **Dữ liệu đầu vào:** Mốc thời gian đếm ngược `sla_deadline` của Ticket.
* **Quy trình xử lý nội bộ:**
  1. SLA Worker chạy chu kỳ quét bảng `tickets` kiểm tra trạng thái xử lý và `sla_deadline`.
  2. Nếu nhân viên hoàn thành Ticket trước mốc hạn $\rightarrow$ Cập nhật `status = 'RESOLVED'`, `resolved_at = NOW()`, ghi nhận đạt chuẩn `SLA Met`.
  3. Nếu `NOW() > sla_deadline` mà Ticket chưa hoàn thành và `sla_breached = FALSE`:
     * Đánh dấu `sla_breached = TRUE` trong bảng `tickets`.
     * Tra cứu `sla_policies` xác định cấp báo động (`escalation_notify_to` = 'MANAGER').
     * Đẩy thông điệp vi phạm vào **Redis Pub/Sub (`channel:sla_alerts`)**.
     * WebSocket Manager nhận từ Pub/Sub và phát sự kiện `SLA_BREACH_ALERT` làm thẻ Ticket trên Kanban đổi sang màu đỏ nhấp nháy trên màn hình Quản lý.
* **Kết quả đầu ra:** Đánh dấu chỉ số vi phạm trong CSDL và báo động đỏ thời gian thực lên giao diện quản trị.

### 4.3. Chức năng: Quản lý Tiến độ trên Bảng Kanban & Báo cáo Thống kê Hiệu suất
* **Tác nhân:** Nhân viên CSKH & Quản lý CSKH.
* **Dữ liệu đầu vào:** Thao tác kéo thả chuyển trạng thái Ticket trên Kanban hoặc yêu cầu lọc báo cáo.
* **Quy trình xử lý nội bộ:**
  1. Khi kéo thả Ticket: Gửi `PATCH /api/tickets/{id}/status`, cập nhật bảng `tickets`, đồng bộ trạng thái Kanban qua WebSocket.
  2. Khi xem báo cáo: Gửi `GET /api/reports/analytics`, Gateway thực hiện các câu truy vấn gom nhóm (Aggregation) trên PostgreSQL tính tỷ lệ vi phạm SLA, năng suất nhân viên và phân bổ cảm xúc để trả về dạng biểu đồ trực quan.
* **Kết quả đầu ra:** Trạng thái Ticket được đồng bộ tức thì trên Kanban và các biểu đồ báo cáo hiệu suất vận hành hiển thị trực quan.

---

# IV. Phân tích Luồng Tuần tự Kỹ thuật (Technical Sequence Flows)

### LUỒNG TUẦN TỰ 1: Tra cứu chính sách và hỏi đáp tự động (RAG Streaming Flow)

**Các thành phần nội bộ tương tác:**
* `Customer UI`: Giao diện khách hàng.
* `FastAPI Gateway`: Kênh API & Middleware xác thực JWT.
* `Supabase DB (knowledge_chunks)`: CSDL PostgreSQL với HNSW Index vector nhúng.
* `LLM RAG Engine`: Bộ sinh câu trả lời tự nhiên.
* `PostgreSQL (Supabase)`: CSDL các bảng `conversations`, `messages`.

```
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

### LUỒNG TUẦN TỰ 2: Giám sát hội thoại ngầm & Tự động khởi tạo Ticket khẩn cấp (AI Auto-Triage Flow)

**Các thành phần nội bộ tương tác:**
* `Event Listener`: Tiến trình lắng nghe tin nhắn mới.
* `AI Classifier`: LLM phân tích cảm xúc & trích xuất JSON cấu trúc.
* `Supabase DB`: Lưu vết `messages`, `conversations`, `tickets`, `ai_rules`.
* `Redis Queue`: Hàng đợi thông điệp sự kiện (`queue:tickets:pending`).

```
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

### LUỒNG TUẦN TỰ 3: Tiếp quản phiên trò chuyện từ AI (Agent Takeover Flow)

**Các thành phần nội bộ tương tác:**
* `Agent UI`: Giao diện làm việc của tư vấn viên.
* `FastAPI Gateway`: Xử lý logic nghiệp vụ và khóa giao dịch.
* `Supabase DB`: CSDL các bảng `conversations`, `users`, `messages`, `canned_responses`.
* `WebSocket Manager`: Bộ điều phối kết nối thời gian thực.
* `Customer UI`: Giao diện chat phía khách hàng.

```
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

### LUỒNG TUẦN TỰ 4: Tự động phân chia Ticket, Giám sát SLA & Báo động Vi phạm (Dispatcher & SLA Engine Flow)

**Các thành phần nội bộ tương tác:**
* `Redis Queue / PubSub`: Hàng đợi thông điệp và kênh phát sóng sự kiện.
* `Ticket Dispatcher`: Tiến trình phân chia công việc ngầm.
* `SLA Worker`: Tiến trình ngầm quét vi phạm hạn xử lý.
* `Supabase DB`: CSDL các bảng `tickets`, `users`, `sla_policies`.
* `WebSocket Manager`: Đẩy thông báo thời gian thực.
* `Agent / Admin UI`: Giao diện người dùng.

```
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