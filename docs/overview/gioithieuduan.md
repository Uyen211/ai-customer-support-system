# Báo cáo Tổng hợp Đề tài Dự án

## 1. Giới thiệu đề tài

* **Tên đề tài:** Hệ thống AI Agent Chăm sóc Khách hàng Tự động & Điều phối Khiếu nại Đa kênh (Omnichannel Customer Support & Smart Ticket Routing System).
* **Bối cảnh & Mục tiêu:**
  Các doanh nghiệp thương mại và bán lẻ thường xuyên đối mặt với tình trạng quá tải tin nhắn chăm sóc khách hàng. Đa phần các thắc mắc mang tính lặp lại (chính sách đổi trả, thời gian giao hàng, quy trình bảo hành), trong khi các khiếu nại nghiêm trọng của khách hàng lại dễ bị trôi tin nhắn và xử lý chậm trễ.
  Dự án xây dựng một hệ thống website chăm sóc khách hàng toàn diện bao gồm 4 khối chức năng kết hợp chặt chẽ:
  * **Trợ lý ảo thông minh (AI Chatbot):** Tự động giải đáp thắc mắc 24/7 dựa trên tài liệu nội bộ của công ty, phản hồi câu trả lời dạng gõ chữ trực tiếp và minh bạch nguồn trích dẫn.
  * **Bộ giám sát hội thoại ngầm & Tự động mở Ticket:** Tự động lắng nghe hội thoại, phát hiện mức độ giận dữ hoặc sự cố nghiêm trọng để chủ động lập phiếu khiếu nại (Ticket) cho nhân viên xử lý; đồng thời tự động tạm dừng Bot AI và phát tin nhắn chuyển tiếp nếu sự cố ở mức khẩn cấp.
  * **Cổng hỗ trợ trực tiếp thời gian thực (Live Support Console):** Cho phép nhân viên CSKH theo dõi danh sách trợ giúp và bấm tiếp quản phiên trò chuyện ngay lập tức khi khách hàng có dấu hiệu bức xúc.
  * **Hệ thống điều phối phân việc & Theo dõi cam kết dịch vụ (SLA Engine):** Tự động chia việc công bằng cho nhân viên theo khối lượng công việc hiện tại, kích hoạt đồng hồ đếm ngược và cảnh báo khi quá hạn xử lý.

* **Công nghệ sử dụng:**
  * **Backend:** FastAPI (Python) — Hỗ trợ xử lý bất đồng bộ, WebSocket và tích hợp thư viện AI.
  * **Cơ sở dữ liệu & Vector Storage:** **Supabase (PostgreSQL)** — Kết nối qua ORM (SQLAlchemy / asyncpg). Sử dụng extension **`pgvector`** khởi tạo bảng `knowledge_chunks` lưu trữ trực tiếp vector nhúng tài liệu RAG kết hợp chỉ mục HNSW (`vector_cosine_ops`), thay thế hoàn toàn ChromaDB.
  * **Hàng đợi & Truyền thông điệp ngầm:** Redis — Xử lý hàng đợi sự kiện bất đồng bộ và bộ đệm trạng thái thời gian thực.
  * **Frontend:** React (Vite) + Tailwind CSS — Giao diện hiển thị thời gian thực, phản hồi nhanh và thân thiện với người dùng.
  * **Đóng gói & Triển khai:** **Docker & Docker Compose** — Đóng gói trọn gói 3 container (`cs_redis`, `cs_backend`, `cs_frontend`). Khi sang máy khác chỉ cần duy nhất 1 lệnh `docker compose up --build -d` là khởi chạy toàn bộ hệ thống tự động mà không cần cài đặt thư viện thủ công.
  * **Kiến trúc:** Event-Driven Architecture + Modular Monolith (chia 3 tầng: Routers/Controllers tiếp nhận HTTP/WS, Services xử lý logic nghiệp vụ RAG/SLA/Triage, và Repositories/Models truy vấn CSDL qua ORM).

---

## 2. Bảng phân công & Danh mục Chức năng Tổng quan

| **Tên khối chức năng** | **Thành viên thực hiện** | **Tác nhân chính** | **Các chức năng chính (Gộp chuẩn nghiệp vụ)** |
| --- | --- | --- | --- |
| **Khối 1: Trợ lý Tra cứu Thông tin Khách hàng** *(Customer RAG Chatbot)* | **Thành viên 1** | Khách hàng | 1. Đăng ký / Đăng nhập & Quản lý phiên trò chuyện<br>2. Tra cứu chính sách và hỏi đáp tự động 24/7 (Bao gồm phản hồi gõ chữ trực tiếp, trích dẫn nguồn tài liệu và xử lý khi không có dữ liệu) |
| **Khối 2: Giám sát Hội thoại & Khởi tạo Yêu cầu Hỗ trợ Tự động** *(AI Conversation Intelligence & Auto-Triage)* | **Thành viên 2** | Quản lý CSKH, Hệ thống ngầm | 1. Giám sát hội thoại ngầm, phân tích cảm xúc & Tự động khởi tạo phiếu hỗ trợ (Ticket) khẩn cấp (Ngắt Bot AI ngay khi đạt ngưỡng nguy cơ CRITICAL và thông báo chuyển tiếp)<br>2. Thiết lập quy tắc và ngưỡng cảm xúc phân loại AI |
| **Khối 3: Cổng Hỗ trợ Trực tiếp & Màn hình Làm việc của Nhân viên** *(Real-time Gateway & Live Support Console)* | **Thành viên 3** | Nhân viên CSKH (Agent) | 1. Giám sát hàng đợi & Tiếp quản cuộc trò chuyện từ Trợ lý ảo<br>2. Nhắn tin hai chiều thời gian thực & Phản hồi nhanh theo mẫu<br>3. Quản lý trạng thái làm việc của nhân viên |
| **Khối 4: Điều phối Phân việc, Theo dõi Hạn Xử lý & Báo cáo** *(Ticket Dispatcher, SLA Engine & Analytics)* | **Thành viên 4** | Nhân viên CSKH, Quản trị viên (Admin) | 1. Tự động phân chia phiếu hỗ trợ cho nhân viên theo khối lượng công việc<br>2. Giám sát thời gian cam kết xử lý (SLA) & Báo động quá hạn<br>3. Quản lý tiến độ công việc trên bảng Kanban & Báo cáo thống kê hiệu suất |

---

## 3. Kiến trúc Luồng Thực hiện Dự án

Sơ đồ luồng phát triển và tích hợp theo từng giai đoạn dựa trên sự phụ thuộc dữ liệu giữa **4 Khối Chức năng Cốt lõi**:

```text
[GIAI ĐOẠN 0: KẾT NỐI NỀN TẢNG DÙNG CHUNG]
- Khởi tạo Repository & Cấu hình Docker / Docker Compose
- Khởi tạo CSDL Supabase PostgreSQL & kích hoạt Extension `pgvector`
- Khởi chạy Redis Event Queue & Pub/Sub
- Thiết lập Migration 9 bảng dữ liệu & Chuẩn hóa Schema/DTO dùng chung
                               │
        ┌──────────────────────┴──────────────────────┐
        │                                             │
[GIAI ĐOẠN 1: PHÁT TRIỂN SONG SONG BẬC 1]     [GIAI ĐOẠN 1: PHÁT TRIỂN SONG SONG BẬC 1]
● Khối 1: Trợ lý Tra cứu Khách hàng           ● Khối 4: Điều phối, SLA Engine & Kanban
  - Đăng ký/Đăng nhập Khách hàng                - Quản lý Hồ sơ & Trạng thái Nhân viên
  - RAG Search (Supabase `knowledge_chunks`)     - Cấu hình Cấp độ SLA & Đếm ngược thời gian
  - Trả lời Streaming & Citation                 - Giao diện Bảng Kanban Quản lý Ticket (Mock)
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
                   - Tự động Mở Ticket & Gán Mức độ Ưu tiên (Liên kết Cấu trúc Ticket từ Khối 4)
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

### Mô tả Chi tiết Phụ thuộc Kỹ thuật giữa Các Khối Chức năng:
1. **Khối 1 (Trợ lý Tra cứu Khách hàng)** & **Khối 3 (Cổng Hỗ trợ Trực tiếp)** khởi tạo độc lập ban đầu, đảm bảo giao diện & cơ chế Auth cho 2 đối tượng người dùng (Khách hàng và Nhân viên CSKH).
2. **Khối 2 (Đánh giá Cảm xúc & Auto-Triage)** đóng vai trò cầu nối dữ liệu trung gian: Đọc tin nhắn nhập vào từ Khối 1 để phân tích cảm xúc, sử dụng cấu trúc Ticket của Khối 4 để tự động mở Ticket. Khi phát hiện cảm xúc tiêu cực, Khối 2 đổi trạng thái cuộc trò chuyện sang `WAITING_HUMAN`, giúp tạm dừng bot Khối 1.
3. **Khối 3 (Cổng Hỗ trợ Real-time)** & **Khối 4 (Điều phối & SLA Engine)** hợp nhất luồng xử lý thực tế: Thuật toán của Khối 4 truy vấn danh sách Nhân viên đang Online ở Khối 3 để tự động gán Ticket (từ Khối 2) theo cơ chế tải tối thiểu (Least-Loaded), đồng thời mở WebSocket Gateway ở Khối 3 để Nhân viên trực ca trò chuyện trực tiếp với Khách hàng.


---

## 4. Phân tích Chi tiết Từng Khối Chức năng & Kịch bản Sử dụng (Use Case)

### Khối 1: Trợ lý Tra cứu Thông tin Khách hàng (Thành viên 1)

* **Giải pháp nghiệp vụ:** Giải quyết bài toán tư vấn viên quá tải do thắc mắc lặp đi lặp lại. Trợ lý ảo hoạt động 24/7, đóng vai trò như một tư vấn viên am hiểu chính sách nội bộ, trả lời khách hàng ngay lập tức với minh chứng tài liệu rõ ràng, phản hồi hiển thị từng chữ gõ đến đâu đọc đến đó giúp người dùng cảm giác như đang chat với tư vấn viên thực sự.

#### Các Chức năng Chính:
1. **Đăng ký / Đăng nhập & Quản lý phiên trò chuyện:** Cho phép khách hàng khởi tạo tài khoản, đăng nhập an toàn và tự động tải lại toàn bộ lịch sử trò chuyện cũ hoặc tạo phiên chat mới.
2. **Tra cứu chính sách và hỏi đáp tự động (RAG Engine qua Supabase Vector):** Tiếp nhận câu hỏi của khách hàng, tự động truy vấn tài liệu nội bộ trong bảng `knowledge_chunks` của Supabase để trả lời chính xác. Chức năng này bao gồm trọn gói:
   * Hiển thị câu trả lời dạng gõ chữ trực tiếp (Streaming) giảm thời gian chờ đợi.
   * Cung cấp nút xem trích dẫn nguồn tài liệu (tên văn bản, điều khoản, số trang từ metadata) để đối chiếu.
   * Tự động đưa ra lời phản hồi mặc định lịch sự và gợi ý kết nối với nhân viên tư vấn khi không tìm thấy dữ liệu hoặc khi phiên chat được chuyển sang trạng thái chờ nhân viên (`WAITING_HUMAN`).

#### Use Case 1: Tra cứu chính sách và hỏi đáp tự động

* **Tên use case:** Tra cứu chính sách và hỏi đáp tự động
* **Tác nhân chính:** Khách hàng
* **Điều kiện bắt đầu:**
  * Khách hàng đã mở khung chat trên trang web.
  * Kho dữ liệu chính sách công ty đã được nạp sẵn vào bảng `knowledge_chunks` trong Supabase.

* **Luồng sự kiện chính:**
  1. Khách hàng nhập nội dung câu hỏi (Ví dụ: "Công ty có chính sách đổi trả hàng bị lỗi do vận chuyển không?") và nhấn gửi.
  2. Hệ thống tiếp nhận và kiểm tra nội dung nhập vào.
  3. Nếu câu hỏi rỗng hoặc chỉ chứa khoảng trắng, hệ thống thực hiện luồng rẽ nhánh E-1.
  4. Hệ thống kiểm tra trạng thái cuộc trò chuyện hiện tại. Nếu trạng thái cuộc trò chuyện đang ở chế độ chờ nhân viên (`mode = 'WAITING_HUMAN'`), hệ thống thực hiện luồng rẽ nhánh E-3.
  5. Hệ thống tiến hành tra cứu các đoạn thông tin liên quan nhất bằng Cosine Similarity từ bảng `knowledge_chunks` trên Supabase.
  6. Nếu không tìm thấy thông tin phù hợp trong kho tài liệu, hệ thống thực hiện luồng rẽ nhánh E-2.
  7. Hệ thống tạo câu trả lời và hiển thị dạng gõ chữ trực tiếp lên khung chat của khách hàng kèm nút xem trích dẫn tài liệu tham khảo.
  8. Hệ thống tự động ghi nhận tin nhắn vào lịch sử cuộc trò chuyện.

* **Luồng con:**
  * **A-1. Xem chi tiết nguồn trích dẫn tài liệu:**
    1. Khách hàng bấm nút "Xem trích dẫn nguồn" bên dưới câu trả lời của Trợ lý ảo.
    2. Hệ thống hiển thị hộp thoại thông tin chứa đoạn văn bản gốc được trích từ tài liệu chính sách.
    3. Use case kết thúc.

* **Luồng rẽ nhánh:**
  * **E-1. Nội dung câu hỏi rỗng:**
    1. Hệ thống báo lỗi "Vui lòng nhập nội dung câu hỏi".
    2. Use case quay lại bước 1.
  * **E-2. Không tìm thấy tài liệu phù hợp:**
    1. Hệ thống hiển thị thông báo: "Rất tiếc, thông tin này chưa có trong tài liệu chính sách của chúng tôi. Bạn có muốn kết nối với nhân viên hỗ trợ không?".
    2. Khách hàng chọn "Đồng ý", hệ thống chuyển cuộc trò chuyện sang trạng thái chờ nhân viên tiếp quản (`WAITING_HUMAN`).
    3. Use case kết thúc.
  * **E-3. Cuộc trò chuyện đang ở trạng thái chờ nhân viên (`WAITING_HUMAN`):**
    1. Trợ lý ảo tạm ngắt chế độ trả lời tự động để tránh can thiệp máy móc.
    2. Hệ thống ghi nhận tin nhắn mới của khách hàng vào lịch sử để nhân viên theo dõi.
    3. Use case kết thúc.

---

### Khối 2: Giám sát Hội thoại & Khởi tạo Yêu cầu Hỗ trợ Tự động (Thành viên 2)

* **Giải pháp nghiệp vụ:** Đóng vai trò như một thanh tra viên ngầm quan sát mọi cuộc trò chuyện giữa khách hàng và trợ lý ảo. Mỗi khi khách hàng thể hiện thái độ tức giận hoặc gặp sự cố phức tạp, hệ thống lập tức trích xuất nguyên nhân và tự động tạo một phiếu hỗ trợ khẩn cấp (Ticket) gửi sang cho nhân viên. **Đặc biệt, khi phát hiện thái độ bức xúc ở cấp độ nghiêm trọng (CRITICAL), hệ thống tự động ngắt chế độ trả lời của AI Bot ngay lập tức, chuyển trạng thái sang `WAITING_HUMAN` và phát tin nhắn hệ thống nhờ khách hàng chờ tư vấn viên, giúp tránh phản hồi máy móc làm bùng nổ khủng hoảng.**

#### Các Chức năng Chính:
1. **Giám sát hội thoại ngầm, phân tích cảm xúc & Tự động khởi tạo phiếu hỗ trợ (Ticket) khẩn cấp:** Tự động lắng nghe tin nhắn mới từ khách hàng và đánh giá điểm cảm xúc dựa trên ngữ cảnh. Khi điểm cảm xúc vượt quá ngưỡng nguy cơ quy định:
   * AI tự động trích xuất thông tin tóm tắt sự cố, phân loại mức ưu tiên (P1, P2, P3), lập phiếu hỗ trợ khẩn cấp ở trạng thái "Chờ tiếp nhận", bật cờ cảnh báo trên phiên chat và phát thông báo sự kiện tới khối điều phối công việc.
   * **Cơ chế ngắt Bot AI lập tức khi gặp nguy cơ CRITICAL:** Nếu phát hiện giận dữ cấp độ khẩn cấp/nghiêm trọng (CRITICAL), hệ thống tự động cập nhật ngay cuộc trò chuyện sang trạng thái `mode = 'WAITING_HUMAN'` và gửi tin nhắn hệ thống: *"Hệ thống nhận thấy bạn cần hỗ trợ chuyên sâu, vui lòng chờ trong giây lát tư vấn viên đang vào hỗ trợ bạn."*. Ở các lượt chat tiếp theo, AI Bot sẽ ngắt tự động trả lời cho đến khi nhân viên nhận tiếp quản.
2. **Thiết lập quy tắc và ngưỡng cảm xúc AI:** Cung cấp giao diện cho phép cấp quản lý tự điều chỉnh danh sách quy tắc (tên quy tắc, ngưỡng điểm cảm xúc kích hoạt, mức ưu tiên gán) mà không cần can thiệp mã nguồn.

#### Use Case 2: Tự động phân tích hội thoại và mở phiếu hỗ trợ khẩn cấp

* **Tên use case:** Tự động phân tích hội thoại và mở phiếu hỗ trợ khẩn cấp
* **Tác nhân chính:** Hệ thống ngầm
* **Điều kiện bắt đầu:**
  * Khách hàng vừa gửi một tin nhắn mới trong phiên chat với Trợ lý ảo.

* **Luồng sự kiện chính:**
  1. Hệ thống tự động thu thập tin nhắn mới cùng các tin nhắn liền trước để lấy ngữ cảnh.
  2. Hệ thống phân tích đo lường chỉ số cảm xúc và xác định loại vấn đề của khách hàng.
  3. Hệ thống đối chiếu kết quả với bảng quy tắc ngưỡng cảnh báo đang áp dụng.
  4. Nếu cảm xúc khách hàng ở mức bình thường (không vượt ngưỡng), hệ thống thực hiện luồng rẽ nhánh E-1.
  5. Hệ thống tự động trích xuất tóm tắt nội dung sự cố và phân loại mức độ ưu tiên (P1/P2/P3).
  6. Hệ thống tự động tạo một phiếu hỗ trợ (Ticket) mới vào hệ thống với trạng thái "Chờ tiếp nhận".
  7. Hệ thống gắn cờ cảnh báo nguy cơ lên phiên chat để làm nổi bật trên màn hình giám sát.
  8. Nếu mức độ bức xúc thuộc cấp độ nghiêm trọng (CRITICAL), hệ thống thực hiện luồng con A-1 để ngắt Bot AI ngay lập tức.
  9. Hệ thống phát thông báo sự kiện "Có Ticket khẩn cấp mới" sang khối điều phối công việc.

* **Luồng con:**
  * **A-1. Tự động ngắt Bot AI và chuyển trạng thái chờ tư vấn viên (CRITICAL Level):**
    1. Hệ thống cập nhật trạng thái phiên chat thành `mode = 'WAITING_HUMAN'`.
    2. Hệ thống tự động đẩy tin nhắn thông báo vào khung chat của khách hàng: *"Hệ thống nhận thấy bạn cần hỗ trợ chuyên sâu, vui lòng chờ trong giây lát tư vấn viên đang vào hỗ trợ bạn."*.
    3. Hệ thống vô hiệu hóa bộ máy trả lời tự động của Trợ lý ảo cho các tin nhắn tiếp theo của phiên chat này.
    4. Use case tiếp tục bước 9 của luồng chính.

* **Luồng rẽ nhánh:**
  * **E-1. Khách hàng có thái độ bình thường (Không vượt ngưỡng cảnh báo):**
    1. Hệ thống ghi nhận điểm cảm xúc vào lịch sử hội thoại để theo dõi xu hướng.
    2. Hệ thống không tạo Ticket và kết thúc tiến trình giám sát ngầm.
    3. Use case kết thúc.

---

### Khối 3: Cổng Hỗ trợ Trực tiếp & Màn hình Làm việc của Nhân viên (Thành viên 3)

* **Giải pháp nghiệp vụ:** Cung cấp bàn làm việc thời gian thực chuyên nghiệp cho nhân viên tư vấn. Khi có sự cố hoặc khách hàng cần hỗ trợ trực tiếp, nhân viên có thể xem danh sách trợ giúp, bấm tiếp quản cuộc trò chuyện để chuyển giao từ trạng thái `WAITING_HUMAN` sang `HUMAN` và nhắn tin hai chiều tức thì với khách hàng mà không bị đứt đoạn hay trôi tin nhắn.

#### Các Chức năng Chính:
1. **Giám sát hàng đợi & Tiếp quản cuộc trò chuyện:** Cho phép nhân viên xem danh sách các cuộc trò chuyện bị gắn cờ cảnh báo hoặc chờ hỗ trợ (`mode = 'WAITING_HUMAN'`), bấm nhận tiếp quản để chuyển sang trạng thái `mode = 'HUMAN'` và chuyển giao thông báo tới khách hàng (có kiểm tra chống xung đột nếu đã có nhân viên khác nhận trước).
2. **Nhắn tin hai chiều thời gian thực & Phản hồi nhanh theo mẫu:** Cho phép nhân viên và khách hàng trao đổi tin nhắn trực tiếp tức thì, hỗ trợ nhân viên sử dụng phím tắt (như `/chao`, `/xloi`) để gọi các mẫu câu phản hồi chuẩn bị sẵn.
3. **Quản lý trạng thái làm việc của nhân viên:** Cho phép nhân viên chủ động thiết lập trạng thái hoạt động cá nhân (Trực tuyến / Sẵn sàng nhận khách, Bận, Ngoại tuyến).

#### Use Case 3: Tiếp quản cuộc trò chuyện từ Trợ lý ảo

* **Tên use case:** Tiếp quản cuộc trò chuyện từ Trợ lý ảo
* **Tác nhân chính:** Nhân viên CSKH
* **Điều kiện bắt đầu:**
  * Nhân viên đã đăng nhập và đang ở trạng thái "Trực tuyến / Sẵn sàng nhận khách".
  * Cuộc trò chuyện của khách hàng đang ở trạng thái Trợ lý ảo tự động trả lời hoặc đang ở trạng thái Chờ nhân viên (`WAITING_HUMAN`).

* **Luồng sự kiện chính:**
  1. Nhân viên chọn một cuộc trò chuyện có gắn cờ cảnh báo hoặc yêu cầu hỗ trợ từ danh sách hàng đợi.
  2. Hệ thống hiển thị toàn bộ lịch sử trò chuyện và bản tóm tắt nguyên nhân sự cố lên màn hình làm việc.
  3. Nhân viên nhấn nút "Tiếp quản cuộc trò chuyện".
  4. Hệ thống kiểm tra trạng thái tiếp quản hiện tại của cuộc trò chuyện.
  5. Nếu cuộc trò chuyện này đã được một nhân viên khác tiếp quản trước đó, hệ thống thực hiện luồng rẽ nhánh E-1.
  6. Hệ thống chuyển trạng thái cuộc trò chuyện thành `mode = 'HUMAN'`.
  7. Hệ thống gửi thông báo đến khung chat của khách hàng: "Nhân viên tư vấn đã tham gia cuộc trò chuyện".
  8. Hệ thống mở khung nhập liệu tin nhắn cho nhân viên trao đổi trực tiếp với khách hàng.

* **Luồng con:**
  * **A-1. Chèn nhanh mẫu câu phản hồi chuẩn bị sẵn:**
    1. Tại ô nhập tin nhắn, nhân viên gõ phím tắt (VD: `/chao`) hoặc bấm chọn danh sách mẫu câu có sẵn.
    2. Hệ thống tự động điền câu chào/xin lỗi chuẩn hóa vào ô nhập liệu.
    3. Nhân viên kiểm tra nội dung và nhấn gửi tin nhắn.
    4. Use case tiếp tục bước 8 của luồng chính.

* **Luồng rẽ nhánh:**
  * **E-1. Cuộc trò chuyện đã được nhân viên khác tiếp quản:**
    1. Hệ thống thông báo: "Cuộc trò chuyện này đã được nhân viên [Tên nhân viên] nhận hỗ trợ".
    2. Hệ thống chuyển giao diện của nhân viên sang chế độ "Chỉ xem".
    3. Use case kết thúc.

---

### Khối 4: Điều phối Phân việc, Theo dõi Hạn Xử lý & Báo cáo (Thành viên 4)

* **Giải pháp nghiệp vụ:** Tự động hóa khâu phân chia công việc và kiểm soát chất lượng cam kết dịch vụ. Hệ thống tự động chia phiếu khiếu nại (Ticket) cho đúng nhân viên đang rảnh việc nhất, đồng thời kích hoạt đồng hồ đếm ngược thời gian cam kết xử lý (SLA); nếu công việc sắp hết hạn mà chưa xong thì tự động phát chuông báo động lên cấp quản lý.

#### Các Chức năng Chính:
1. **Tự động phân chia Ticket thông minh:** Khi có Ticket mới, hệ thống tự động lọc danh sách nhân viên trực tuyến có chuyên môn phù hợp, gán Ticket cho người đang gánh ít việc nhất (Least-Loaded). Nếu không có ai trực, Ticket chuyển sang trạng thái chờ phân bổ và cảnh báo Admin.
2. **Giám sát thời gian cam kết xử lý (SLA) & Báo động quá hạn:** Tính hạn chót theo mức ưu tiên (P1, P2, P3), kích hoạt đồng hồ đếm ngược, ghi nhận hoàn thành đúng hạn (`SLA Met`), và tự động kích hoạt cơ chế báo động chuyển màu đỏ nhấp nháy, bắn thông báo leo thang lên Quản lý khi bị quá hạn (`SLA Breach`).
3. **Quản lý tiến độ trên bảng Kanban & Báo cáo thống kê:** Cho phép kéo thả chuyển trạng thái Ticket trên bảng Kanban (Chờ xử lý $\rightarrow$ Đang xử lý $\rightarrow$ Đã giải quyết $\rightarrow$ Đóng Ticket) và cung cấp biểu đồ báo cáo hiệu suất vận hành chung.

#### Use Case 4: Tự động phân chia Ticket và giám sát hạn xử lý (SLA)

* **Tên use case:** Tự động phân chia Ticket và giám sát hạn xử lý (SLA)
* **Tác nhân chính:** Hệ thống ngầm
* **Điều kiện bắt đầu:**
  * Có một phiếu hỗ trợ (Ticket) khẩn cấp mới được khởi tạo vào hệ thống.

* **Luồng sự kiện chính:**
  1. Hệ thống tiếp nhận thông tin Ticket mới tạo.
  2. Hệ thống quét kiểm tra danh sách các nhân viên đang ở trạng thái Trực tuyến và có chuyên môn phù hợp với loại sự cố.
  3. Nếu không có nhân viên phù hợp đang trực tuyến, hệ thống thực hiện luồng rẽ nhánh E-1.
  4. Hệ thống đếm số lượng công việc chưa hoàn thành của từng nhân viên hợp lệ và gán Ticket cho nhân viên có khối lượng công việc ít nhất.
  5. Hệ thống tra cứu chính sách thời gian (SLA) tương ứng với mức ưu tiên của Ticket (VD: P1 bắt buộc xong trong 15 phút) để tính hạn chót.
  6. Hệ thống kích hoạt đồng hồ đếm ngược hạn xử lý cho Ticket và gửi thông báo công việc mới đến nhân viên được gán.
  7. Nếu nhân viên hoàn thành xử lý sự cố trước hạn chót, hệ thống thực hiện luồng con A-1.
  8. Nếu hết thời gian cam kết mà Ticket vẫn chưa hoàn thành, hệ thống thực hiện luồng rẽ nhánh E-2.

* **Luồng con:**
  * **A-1. Hoàn thành xử lý công việc đúng hạn (SLA Met):**
    1. Nhân viên chuyển trạng thái Ticket sang "Đã giải quyết".
    2. Hệ thống dừng đồng hồ đếm ngược và ghi nhận đạt chuẩn cam kết SLA vào báo cáo hiệu suất.
    3. Use case kết thúc.

* **Luồng rẽ nhánh:**
  * **E-1. Không có nhân viên trực tuyến:**
    1. Hệ thống lưu Ticket vào hàng đợi "Chờ phân bổ".
    2. Hệ thống gửi thông báo cảnh báo lên màn hình của Quản trị viên để phân công thủ công.
    3. Use case kết thúc.
  * **E-2. Quá hạn cam kết xử lý (SLA Breach):**
    1. Đồng hồ đếm ngược chạm mốc 0.
    2. Hệ thống đổi màu thẻ Ticket sang màu đỏ báo động trên toàn bộ màn hình làm việc.
    3. Hệ thống bắn thông báo cảnh báo vi phạm trực tiếp đến cấp Quản lý.
    4. Hệ thống đánh dấu vi phạm SLA vào báo cáo thống kê.
    5. Use case kết thúc.
