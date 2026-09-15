# Báo cáo Tổng hợp Đề tài Dự án

## 1. Giới thiệu đề tài

* **Tên đề tài:** Website tư vấn khách hàng tự động và điều phối hỗ trợ thông minh cho chuỗi cửa hàng đồ dùng thú cưng.
* **Bối cảnh & Mục tiêu:**
  Thị trường kinh doanh sản phẩm và dịch vụ chăm sóc thú cưng tại Việt Nam đang tăng trưởng nhanh chóng. Đi kèm với sự mở rộng của các chuỗi bán lẻ đồ dùng thú cưng là lượng tương tác, tin nhắn tư vấn và yêu cầu hỗ trợ từ khách hàng gia tăng đột biến. Trong thực tế vận hành, phần lớn các thắc mắc lặp đi lặp lại xoay quanh việc tư vấn thức ăn hạt, phụ kiện cho chó mèo, kiểm tra hàng còn/hết tại các chi nhánh, hay chính sách bảo hành và đổi trả.
  Dự án xây dựng một hệ thống website chăm sóc khách hàng toàn diện bao gồm 4 khối chức năng kết hợp chặt chẽ:
  * **Trợ lý tư vấn khách hàng tự động (Customer RAG Chatbot):** Tự động tư vấn sản phẩm thú cưng và giải đáp chính sách cửa hàng 24/7 dựa trên tài liệu nội bộ và danh mục sản phẩm, phản hồi câu trả lời dạng gõ chữ trực tiếp (SSE Streaming) và minh bạch nguồn trích dẫn tài liệu (*Citations*).
  * **Bộ giám sát hội thoại ngầm & Khởi tạo yêu cầu hỗ trợ khẩn cấp (AI Auto-Triage):** Tự động lắng nghe hội thoại, phân tích cảm xúc (-1.00 đến +1.00) để chủ động lập phiếu hỗ trợ (Ticket) khẩn cấp; tự động tạm dừng Bot AI (đổi `mode = 'WAITING_HUMAN'`) và phát tin nhắn chuyển tiếp nếu phát hiện thái độ bức xúc ở mức nghiêm trọng (CRITICAL).
  * **Cổng hỗ trợ trực tiếp thời gian thực (Live Support Console):** Cho phép nhân viên CSKH theo dõi danh sách hàng đợi, tiếp quản cuộc trò chuyện (chuyển `mode = 'HUMAN'`), nhắn tin 2 chiều qua WebSocket thời gian thực và sử dụng các câu phản hồi mẫu nhanh (`canned_responses`).
  * **Hệ thống điều phối phân việc, Giám sát cam kết dịch vụ (SLA Engine) & Báo cáo:** Tự động phân chia Ticket cho nhân viên theo khối lượng công việc ít nhất (*Least-Loaded*), kích hoạt đồng hồ đếm ngược SLA (P1: 15p, P2: 60p, P3: 240p), báo động quá hạn và quản lý tiến độ trên bảng Kanban kèm báo cáo thống kê hiệu suất.

* **Công nghệ sử dụng:**
  * **Backend:** FastAPI (Python 3.11) — Hỗ trợ xử lý bất đồng bộ, WebSocket và tích hợp mô hình AI.
  * **Cơ sở dữ liệu & Vector Storage:** **Supabase (PostgreSQL)** — Kết nối qua ORM (SQLAlchemy / asyncpg). Sử dụng extension **`pgvector`** khởi tạo bảng `knowledge_chunks` lưu trữ trực tiếp vector nhúng tài liệu RAG kết hợp chỉ mục HNSW (`vector_cosine_ops`), cùng 9 bảng dữ liệu quan hệ (`users`, `customers`, `conversations`, `messages`, `tickets`, `sla_policies`, `canned_responses`, `ai_rules`, `products`).
  * **Hàng đợi & Truyền thông điệp ngầm:** Redis — Xử lý hàng đợi sự kiện bất đồng bộ (`queue:tickets:pending`), kênh phát sóng báo động (`channel:sla_alerts`) và bộ đệm trạng thái nhân viên thời gian thực (`agent:status:{id}`).
  * **Frontend:** React (Vite) + Tailwind CSS — Giao diện hiển thị thời gian thực, phản hồi nhanh và thân thiện với người dùng.
  * **Đóng gói & Triển khai:** **Docker & Docker Compose** — Đóng gói trọn gói 3 container (`cs_redis`, `cs_backend`, `cs_frontend`).
  * **Kiến trúc:** Event-Driven Architecture + Modular Monolith.

---

## 2. Bảng phân công & Danh mục Chức năng Tổng quan

| **Tên khối chức năng** | **Thành viên thực hiện** | **Tác nhân chính** | **Danh mục các Use Case chi tiết** |
| --- | --- | --- | --- |
| **Khối 1: Trợ lý Tra cứu Thông tin Khách hàng** *(Customer RAG Chatbot)* | **Nguyễn Hà Phương Uyên** *(65KTPM - 235170632)* | Khách hàng | **UC 1.1:** Quản lý tài khoản khách hàng<br>**UC 1.2:** Quản lý phiên trò chuyện<br>**UC 1.3:** Tư vấn sản phẩm và giải đáp chính sách tự động |
| **Khối 2: Giám sát Hội thoại & Khởi tạo Yêu cầu Hỗ trợ Tự động** *(AI Conversation Intelligence & Auto-Triage)* | **Nguyễn Thị Phương Thảo** *(65KTPM - 2351170621)* | Quản lý CSKH, Hệ thống ngầm | **UC 2.1:** Phân tích cảm xúc & Phát hiện khiếu nại ngầm<br>**UC 2.2:** Trích xuất thông tin và khởi tạo ticket khẩn cấp<br>**UC 2.3:** Cấu hình quy tắc cảnh báo linh hoạt |
| **Khối 3: Cổng Hỗ trợ Trực tiếp & Màn hình Làm việc của Nhân viên** *(Real-time Gateway & Live Support Console)* | **Nguyễn Thị Hồng Mai** *(65KTPM - 2351170606)* | Nhân viên CSKH (Agent) | **UC 3.1:** Quản lý tài khoản nhân viên<br>**UC 3.2:** Quản lý trạng thái làm việc của nhân viên<br>**UC 3.3:** Theo dõi hàng đợi và tiếp quản cuộc trò chuyện<br>**UC 3.4:** Quản lý và sử dụng mẫu phản hồi nhanh |
| **Khối 4: Điều phối Phân việc, Theo dõi Hạn Xử lý & Báo cáo** *(Ticket Dispatcher, SLA Engine & Analytics)* | **Nguyễn Minh** *(65KTPM - 2351170607)* | Nhân viên CSKH, Quản trị viên (Admin) | **UC 4.1:** Phân chia công việc tự động<br>**UC 4.2:** Giám sát thời hạn xử lý cam kết<br>**UC 4.3:** Quản lý tiến độ trên bảng Kanban<br>**UC 4.4:** Báo cáo thống kê hiệu suất |

---

## 3. Kiến trúc Luồng Thực hiện Dự án

Sơ đồ luồng phát triển và tích hợp theo từng giai đoạn dựa trên sự phụ thuộc dữ liệu giữa **4 Khối Chức năng Cốt lõi**:

```text
[GIAI ĐOẠN 0: KẾT NỐI NỀN TẢNG DÙNG CHUNG]
- Khởi tạo Repository & Cấu hình Docker / Docker Compose
- Khởi tạo CSDL Supabase PostgreSQL & kích hoạt Extension `pgvector`
- Khởi chạy Redis Event Queue & Pub/Sub
- Thiết lập Migration 10 bảng dữ liệu & Chuẩn hóa Schema/DTO dùng chung
                                │
        ┌──────────────────────┴──────────────────────┐
        │                                             │
[GIAI ĐOẠN 1: PHÁT TRIỂN SONG SONG BẬC 1]     [GIAI ĐOẠN 1: PHÁT TRIỂN SONG SONG BẬC 1]
● Khối 1: Trợ lý Tra cứu Khách hàng           ● Khối 4: Điều phối, SLA Engine & Kanban
  - Đăng ký/Đăng nhập Khách hàng                - Quản lý Hồ sơ & Trạng thái Nhân viên
  - RAG Search (Supabase `knowledge_chunks`)     - Cấu hình Cấp độ SLA & Đếm ngược thời gian
  - Trả lời Streaming & Citation                 - Giao diện Bảng Kanban Quản lý Ticket
● Khối 3: Cổng Hỗ trợ Trực tiếp (Phần 1)
  - Đăng ký/Đăng nhập Nhân viên CSKH
  - Khung Màn hình Trực ca (Live Console)
        │                                             │
        └──────────────────────┬──────────────────────┘
                                │
                 [GIAI ĐOẠN 2: TÍCH HỢP TỰ ĐỘNG PHÂN LOẠI]
                 ● Khối 2: Trợ lý Đánh giá Cảm xúc & Auto-Triage
                   - Phân tích Cảm xúc Tin nhắn (Từ Khối 1)
                   - Phát hiện Khách hàng Tiêu cực / Yêu cầu Gặp Người
                   - Tự động Mở Ticket & Gán Mức độ Ưu tiên P1/P2/P3
                   - Kích hoạt Cờ Chuyển chế độ sang `WAITING_HUMAN` (Tự động Tạm dừng Bot Khối 1)
                                │
                 [GIAI ĐOẠN 3: TÍCH HỢP ĐIỀU PHỐI & REAL-TIME GATEWAY]
                 ● Khối 3: Cổng Hỗ trợ Trực tiếp (Phần 2)
                   - WebSocket Gateway tiếp quản Cuộc hội thoại ngay khi nhận Cờ Chuyển chế độ từ Khối 2
                   - Nhắn tin 2 chiều thời gian thực Khách - Nhân viên
                 ● Khối 4: Thuật toán Điều phối Ticket
                   - Thuật toán Phân việc Tải tối thiểu (Least-Loaded Dispatcher)
                   - Phân bổ Ticket mới mở (từ Khối 2) tới Nhân viên Online (từ Khối 3)
                   - Cảnh báo vi phạm SLA Real-time qua Redis / Notification
                                │
                 [GIAI ĐOẠN 4: ĐÓNG GÓI DOCKER, KIỂM THỬ E2E & BÁO CÁO]
                 - Kiểm thử Toàn trình (End-to-End Testing) luồng Khách chat -> AI Triage -> Phân Ticket -> Agent Tiếp quản
                 - Đóng gói Container Docker (`cs_frontend`, `cs_backend`, `cs_redis`)
                 - Hoàn thiện Tài liệu Phân tích & Báo cáo Thống kê Hiệu suất
```

---

## 4. Phân tích Chi tiết Từng Khối Chức năng & Kịch bản Sử dụng (Use Case)

### Khối 1: Trợ lý Tra cứu Thông tin Khách hàng (Nguyễn Hà Phương Uyên)

* **Giải pháp nghiệp vụ:** Giải quyết bài toán tư vấn viên quá tải do thắc mắc lặp đi lặp lại. Trợ lý ảo hoạt động 24/7, đóng vai trò như một tư vấn viên am hiểu chính sách và sản phẩm đồ dùng thú cưng của chuỗi cửa hàng, trả lời khách hàng ngay lập tức với minh chứng tài liệu rõ ràng, phản hồi hiển thị từng chữ gõ đến đâu đọc đến đó (SSE Streaming).

#### Danh mục các Use Case:
1. **UC 1.1: Quản lý tài khoản khách hàng:** Cho phép khách hàng đăng ký tài khoản mới (họ tên, email, số điện thoại, mật khẩu) và đăng nhập an toàn vào hệ thống.
2. **UC 1.2: Quản lý phiên trò chuyện:** Cho phép khách hàng xem danh sách các cuộc trò chuyện cũ, tiếp tục phiên trò chuyện hoặc mở phiên trò chuyện mới độc lập.
3. **UC 1.3: Tư vấn sản phẩm và giải đáp chính sách tự động:** Tiếp nhận câu hỏi về mặt hàng thú cưng (thức ăn, phụ kiện, tồn kho) và chính sách (đổi trả, giao hàng), tự động truy vấn tài liệu trong bảng `knowledge_chunks` của Supabase để trả lời dạng streaming, hiển thị nút xem trích dẫn nguồn tài liệu (*Citations*). Tự động đề xuất kết nối nhân viên khi không tìm thấy dữ liệu hoặc khi phiên chat ở trạng thái `WAITING_HUMAN`.

---

### Khối 2: Giám sát Hội thoại & Khởi tạo Yêu cầu Hỗ trợ Tự động (Nguyễn Thị Phương Thảo)

* **Giải pháp nghiệp vụ:** Lắng nghe ngầm mọi tương tác giữa khách hàng và trợ lý ảo. Mỗi khi khách hàng thể hiện thái độ giận dữ hoặc gặp sự cố phức tạp, hệ thống tự động trích xuất nguyên nhân và tạo phiếu hỗ trợ khẩn cấp (Ticket) gửi sang cho nhân viên. Khi phát hiện mức độ bức xúc nghiêm trọng (CRITICAL/P1), hệ thống tự động ngắt chế độ trả lời của AI Bot, đổi trạng thái sang `WAITING_HUMAN` và phát tin nhắn hệ thống nhờ khách hàng chờ tư vấn viên.

#### Danh mục các Use Case:
1. **UC 2.1: Phân tích cảm xúc & Phát hiện khiếu nại ngầm:** Phân tích điểm cảm xúc (-1.00 đến +1.00) của tin nhắn khách hàng theo 4 cấp độ (Tích cực, Bình thường, Tiêu cực nhẹ, Bức xúc cao). Tự động bật cờ cảnh báo nguy cơ đỏ khi điểm số <= -0.60 hoặc chứa từ khóa nguy cơ (lừa đảo, dọa kiện, báo công an, tẩy chay).
2. **UC 2.2: Trích xuất thông tin và khởi tạo ticket khẩn cấp:** Trích xuất tóm tắt sự cố, phân loại vào 1 trong 6 danh mục (`Lỗi đơn hàng`, `Đổi trả/Hoàn tiền`, `Sản phẩm lỗi/Hư hại`, `Lỗi thanh toán`, `Thái độ phục vụ`, `Vấn đề khác`), gán mức ưu tiên (P1, P2, P3), tính hạn chót SLA và tự động mở Ticket. Đối với P1, tự động ngắt Bot AI và chuyển phiên chat sang `WAITING_HUMAN`.
3. **UC 2.3: Cấu hình quy tắc cảnh báo linh hoạt:** Cho phép Quản lý CSKH tùy chỉnh danh mục quy tắc, ngưỡng điểm cảm xúc, mức ưu tiên gán và danh sách từ khóa nguy cơ trên giao diện Admin.

---

### Khối 3: Cổng Hỗ trợ Trực tiếp & Màn hình Làm việc của Nhân viên (Nguyễn Thị Hồng Mai)

* **Giải pháp nghiệp vụ:** Cung cấp bàn làm việc thời gian thực (Live Support Console) cho nhân viên CSKH. Cho phép nhân viên quản lý tài khoản nội bộ, chuyển đổi trạng thái hoạt động (ONLINE, BUSY, OFFLINE), xem hàng đợi các phiên chat chờ hỗ trợ, bấm tiếp quản để chuyển `mode` từ `WAITING_HUMAN` sang `HUMAN`, nhắn tin 2 chiều tức thì và sử dụng mẫu phản hồi nhanh (`canned_responses`).

#### Danh mục các Use Case:
1. **UC 3.1: Quản lý tài khoản nhân viên:** Cho phép Admin/Manager khởi tạo tài khoản nhân sự mới (gán vai trò AGENT/MANAGER/ADMIN, gán kỹ năng chuyên môn) và nhân viên đăng nhập bàn làm việc.
2. **UC 3.2: Quản lý trạng thái làm việc của nhân viên:** Cho phép nhân viên chuyển đổi trạng thái cá nhân giữa Trực tuyến (ONLINE), Bận (BUSY), Ngoại tuyến (OFFLINE) để bộ điều phối nhận diện gán việc.
3. **UC 3.3: Theo dõi hàng đợi và tiếp quản cuộc trò chuyện:** Cho phép nhân viên xem các phiên chat bị gắn cờ cảnh báo/chờ hỗ trợ, bấm tiếp quản (khóa chống trùng lặp), ngắt hoàn toàn Bot AI và trao đổi tin nhắn thời gian thực qua WebSocket.
4. **UC 3.4: Quản lý và sử dụng mẫu phản hồi nhanh:** Cho phép nhân viên gõ ký tự `/` để tìm kiếm và chèn nhanh mẫu câu trả lời chuẩn bị sẵn (`canned_responses` như `/chao`, `/xloi`), đồng thời cho phép Quản lý tạo thêm mẫu câu mới vào kho dữ liệu chung.

---

### Khối 4: Điều phối Phân việc, Theo dõi Hạn Xử lý & Báo cáo (Nguyễn Minh)

* **Giải pháp nghiệp vụ:** Tự động hóa phân chia công việc theo khối lượng tải ít nhất (*Least-Loaded*), kiểm soát thời hạn cam kết dịch vụ (SLA Engine), quản lý tiến độ trên bảng Kanban và cung cấp báo cáo thống kê hiệu suất vận hành toàn chuỗi cửa hàng.

#### Danh mục các Use Case:
1. **UC 4.1: Phân chia công việc tự động:** Khi có Ticket mới, tự động lọc danh sách nhân viên đang ONLINE có kỹ năng phù hợp với danh mục sự cố, gán Ticket cho người đang có ít việc nhất (đếm số phiếu `PENDING`/`IN_PROGRESS`). Nếu không có ai trực phù hợp, chuyển Ticket sang "Chờ phân bổ" và cảnh báo Admin phân công thủ công.
2. **UC 4.2: Giám sát thời hạn xử lý cam kết:** Tính mốc hạn chót theo cấp độ ưu tiên (P1: 15p, P2: 60p, P3: 240p), đếm ngược thời gian thực, ghi nhận `SLA Met` khi hoàn thành đúng hạn, hoặc tự động kích hoạt báo động vi phạm (`sla_breached = TRUE`), đổi thẻ sang màu đỏ nhấp nháy và phát thông báo leo thang lên Quản lý qua Redis Pub/Sub & WebSocket.
3. **UC 4.3: Quản lý tiến độ trên bảng Kanban:** Cho phép nhân viên kéo thả hoặc cập nhật trạng thái phiếu hỗ trợ theo tiến độ một chiều (Chờ tiếp nhận $\rightarrow$ Đang xử lý $\rightarrow$ Đã giải quyết $\rightarrow$ Đóng phiếu), yêu cầu nhập tóm tắt kết quả xử lý trước khi ghi nhận giải quyết.
4. **UC 4.4: Báo cáo thống kê hiệu suất:** Cung cấp bộ lọc theo khoảng thời gian, nhân viên, mức ưu tiên, danh mục sự cố và tính toán các biểu đồ chỉ số vận hành (tổng số phiếu, tỷ lệ vi phạm SLA, năng suất nhân viên, phân bổ cảm xúc), hỗ trợ xuất báo cáo Excel.
