# 📄 Đặc Tả Yêu Cầu Chức Năng (SPEC): Giao Diện Frontend Khối 1 - Trợ Lý Tra Cứu Khách Hàng

> **Tài liệu tham chiếu:** [gioithieuduan.md](file:///d:/Study/TLU/kiemthu/project/docs/overview/gioithieuduan.md), [phantichhethong.md](file:///d:/Study/TLU/kiemthu/project/docs/overview/phantichhethong.md), [usecase.md](file:///d:/Study/TLU/kiemthu/project/docs/overview/usecase.md), [design_pattern.md](file:///d:/Study/TLU/kiemthu/project/docs/overview/design_pattern.md), [cautruc.md](file:///d:/Study/TLU/kiemthu/project/docs/overview/cautruc.md), [code/backend/README.md](file:///d:/Study/TLU/kiemthu/project/code/backend/README.md).

---

## 1. ## Summary

Tài liệu này xác định các yêu cầu chức năng và ngôn ngữ thị giác (UI/UX Design System) cho **Giao diện Frontend của Khối 1: Trợ lý Tra cứu Thông tin Khách hàng (Customer RAG Chatbot)** trên hệ thống PetHome. Giao diện được thiết kế theo phong cách **Editorial Calm & Organic Minimalism** định hướng tại [design_pattern.md](file:///d:/Study/TLU/kiemthu/project/docs/overview/design_pattern.md) với tông màu bơ kem ấm (`#FFF8E7`), sắc đỏ Sangria Red (`#930500`), xanh mờ Cornflower Blue (`#95BBEA`), font chữ biên tập sang trọng và hình khối bo góc mềm mại (`Squircle`, `Capsule Pill`). Giao diện bao gồm **Trang chủ Marketing giới thiệu chuỗi cửa hàng và dịch vụ CSKH AI** (trước khi đăng nhập), đăng ký/đăng nhập tài khoản an toàn, quản lý danh sách các phiên hội thoại cá nhân, xem lại lịch sử chat (Lazy Loading 50 tin nhắn), và hỏi đáp 24/7 qua luồng phản hồi gõ chữ thời gian thực (SSE Streaming) kèm pop-up minh bạch trích dẫn nguồn (Citations).


---

## 2. ## User Stories / Jobs To Be Done

* **US-1.0 (Trang chủ Marketing & Giới thiệu chuỗi cửa hàng PetHome)**: Là một Người dùng mới/Khách truy cập, tôi muốn xem Trang chủ giới thiệu về chuỗi cửa hàng đồ dùng thú cưng PetHome, các tính năng nổi bật của Trợ lý CSKH AI và các chính sách ưu đãi, để tôi hiểu rõ dịch vụ trước khi Đăng ký / Đăng nhập.
* **US-1.1 (Đăng ký / Đăng nhập tài khoản)**: Là một Khách hàng, tôi muốn có thể đăng ký tài khoản mới hoặc đăng nhập an toàn bằng email/mật khẩu, để toàn bộ lịch sử tư vấn và phiên trò chuyện của tôi được lưu trữ bảo mật.

* **US-1.2 (Xem danh sách lịch sử hội thoại)**: Là một Khách hàng, tôi muốn xem lại danh sách các cuộc trò chuyện trước đây kèm đoạn tin nhắn tóm lược cuối và nhãn trạng thái, để tôi có thể chọn tiếp tục cuộc hội thoại cũ khi cần.
* **US-1.3 (Khởi tạo phiên chat mới với Bot)**: Là một Khách hàng, tôi muốn bấm "Bắt đầu cuộc trò chuyện mới" để mở khung chat sạch sẽ và nhận ngay lời chào tự động cùng các gợi ý chủ đề từ Trợ lý ảo AI PetHome.
* **US-1.4 (Trực quan hóa luồng gõ chữ & Trích dẫn RAG)**: Là một Khách hàng, tôi muốn câu trả lời của AI hiển thị theo dạng gõ chữ trực tiếp (Streaming token-by-token) và có nút xem nguồn tài liệu trích dẫn, để tôi có thể đối chiếu tính chính xác của thông tin chính sách/sản phẩm ngay lập tức.
* **US-1.5 (Thông báo trạng thái phiên & Chuyển giao tư vấn viên)**: Là một Khách hàng, tôi muốn thấy dải thông báo rõ ràng khi phiên chat đã kết thúc hoặc đang ở chế độ chuyển tiếp tới nhân viên tư vấn, để tôi làm chủ được tiến trình hỗ trợ.

---

## 3. ## What The User Wants (Behavioral Outcomes)

1. **Trải nghiệm Xác thực An toàn (Auth Experience)**:
   - Người dùng xem được form Đăng ký / Đăng nhập với các ô nhập rõ ràng: Họ tên, Email, Mật khẩu, Số điện thoại.
   - Form tự động kiểm tra lỗi dữ liệu ngay tại máy khách (Email không đúng định dạng, Mật khẩu < 8 ký tự hoặc thiếu chữ/số, Số điện thoại không đủ 10 số).
   - Hiển thị thông báo đỏ nếu email đã tồn tại, sai mật khẩu, hoặc tài khoản bị tạm khóa 15 phút do gõ sai 5 lần.
   - Sau khi đăng nhập thành công, token JWT được lưu an toàn và giao diện thanh tiêu đề tự động cập nhật tên khách hàng.

2. **Giao diện Khung Chat & Thanh Sidebar Lịch sử (Chat & Sidebar UI)**:
   - Thanh Sidebar bên trái hiển thị danh sách các phiên trò chuyện của khách hàng, sắp xếp mới nhất lên đầu, mỗi mục bao gồm: Tóm tắt 10-15 từ của tin nhắn cuối, thời gian gửi, và nhãn trạng thái (`Trợ lý ảo`, `Chờ nhân viên`, `Nhân viên trực tiếp`, `Đã kết thúc`).
   - Nút **"Bắt đầu cuộc trò chuyện mới"** nổi bật ở đầu Sidebar. Bấm vào sẽ mở phiên chat mới và hiển thị ngay lời chào thân thiện của Bot cùng các nút gợi ý câu hỏi (VD: *"Tư vấn hạt cho chó mèo"*, *"Chính sách đổi trả"*, *"Kiểm tra tồn kho"*).
   - Cuộn lên đầu danh sách tin nhắn sẽ tự động tải thêm các tin nhắn cũ hơn (Lazy Loading 50 tin nhắn/lượt).

3. **Phản hồi gõ chữ trực tiếp & Trích dẫn Tài liệu (SSE Streaming & Citations)**:
   - Khi gửi câu hỏi, hiển thị ngay bong bóng tin nhắn của khách hàng và biểu tượng động *"Trợ lý ảo đang phản hồi..."*.
   - Câu trả lời của AI xuất hiện gõ từng từ theo thời gian thực (Server-Sent Events).
   - Bên dưới câu trả lời hoàn chỉnh của Bot xuất hiện nút **"Xem trích dẫn nguồn"**. Nhấp vào sẽ mở hộp thoại Popover/Drawer hiển thị tên tài liệu (VD: `Chinh_sach_doi_tra.pdf`), số trang, điều khoản và đoạn văn bản gốc phục vụ đối chiếu.

4. **Xử lý Trạng thái Phiên Chuyển giao & Đóng phiên (State Banners)**:
   - Nếu phiên trò chuyện ở trạng thái **`WAITING_HUMAN`**, hiển thị dải thông báo màu cam: *"Cuộc trò chuyện đang được chuyển tiếp tới nhân viên tư vấn. Vui lòng chờ trong giây lát..."*.
   - Nếu phiên trò chuyện ở trạng thái **`HUMAN`**, hiển thị thông báo màu xanh: *"Nhân viên tư vấn [Tên Agent] đã tham gia cuộc trò chuyện"*.
   - Nếu phiên trò chuyện ở trạng thái **`CLOSED`**, vô hiệu hóa ô nhập liệu và hiển thị dải thông báo màu xám: *"Phiên hỗ trợ này đã đóng. Bạn có thể bấm 'Bắt đầu cuộc trò chuyện mới' để được hỗ trợ tiếp."*.

---

## 4. ## Flow / State Diagram

### 4.1. Sơ đồ Luồng Trải nghiệm Khách hàng (User Journey Flow)
```text
 +--------------------------+
 | Khách hàng truy cập Web  |
 +--------------------------+
              │
              ▼
   [Đã Đăng nhập chưa?] ──(Chưa)──► [Màn hình Đăng nhập / Đăng ký]
              │                                   │ (Thành công)
            (Rồi) ◄───────────────────────────────┘
              │
              ▼
 +----------------------------------------------------------------+
 | Màn hình ChatPage (Sidebar Phiên cũ + Khung Chat Hiện tại)     |
 +----------------------------------------------------------------+
      │                                       │
      ├── (Bấm "Tạo phiên mới") ──────────────┼── (Chọn Phiên cũ từ Sidebar)
      │                                       │
      ▼                                       ▼
 [POST /api/conversations]               [GET /api/conversations/{id}/messages]
  - Khởi tạo mode = 'BOT'                 - Tải 50 tin nhắn gần nhất
  - Nhận câu chào & gợi ý                  - Hiển thị lịch sử chat & citations
      │                                       │
      └──────────────────┬────────────────────┘
                         │
                         ▼
             [Khách gõ & gửi câu hỏi]
                         │
                         ▼
         [POST /api/chat/stream (SSE)]
  - Hiển thị bong bóng gõ chữ token-by-token
  - Nút "Xem trích dẫn" hiển thị pop-up trích đoạn gốc
```

### 4.2. Sơ đồ Chuyển đổi Trạng thái Phiên trò chuyện (Conversation Mode State)
```text
                 +-------------------+
                 |    mode = 'BOT'   | ◄── Trợ lý ảo tự động trả lời RAG SSE Stream
                 +-------------------+
                   /               \
 (Khách bức xúc CRITICAL /         (Khách chọn "Kết nối nhân viên" / Out-of-Domain)
  AI Auto-Triage Khối 2)             \
                /                     v
               v             +--------------------------+
 +-------------------------+ | mode = 'WAITING_HUMAN'   | ◄── Dải thông báo cam:
 |  mode = 'WAITING_HUMAN' | +--------------------------+     Ngắt Bot, chờ Agent
 +-------------------------+              │
               │                          │ (Agent bấm tiếp quản ở Khối 3)
               └──────────────┬───────────┘
                              ▼
                     +-------------------+
                     |   mode = 'HUMAN'  | ◄── Dải thông báo xanh:
                     +-------------------+     Agent chat 2 chiều qua WS
                              │
                              │ (Bấm kết thúc phiên / Quá 24h)
                              ▼
                     +-------------------+
                     |  mode = 'CLOSED'  | ◄── Dải thông báo xám: Khóa ô nhập,
                     +-------------------+     gợi ý tạo phiên mới
```

---

## 5. ## Acceptance Criteria (Testable Outcomes)

| Mã AC | Tiêu chuẩn Nghiệm thu (Observable Outcome) | `proven by:` Test Scenario | `strategy:` |
| :--- | :--- | :--- | :--- |
| **AC-1** | Biểu mẫu Đăng ký kiểm tra đúng định dạng email, mật khẩu >= 8 ký tự (chứa chữ và số) và sđt 10 số. Đăng ký thành công lưu JWT vào storage. | `test_customer_register_frontend_validation` | Fully-Automated |
| **AC-2** | Form Đăng nhập gửi đúng payload, nhận JWT token; hiển thị thông báo đỏ khi sai mật khẩu hoặc khi tài khoản bị tạm khóa 15 phút do sai 5 lần. | `test_customer_login_lockout_alerts` | Fully-Automated |
| **AC-3** | Thanh Sidebar tải danh sách cuộc trò chuyện từ `GET /api/conversations`, hiển thị đoạn tóm tắt tin nhắn cuối (10-15 từ) và badge trạng thái (`BOT`, `WAITING_HUMAN`, `HUMAN`, `CLOSED`). | `test_sidebar_conversations_render` | Fully-Automated |
| **AC-4** | Nhấp nút "Bắt đầu cuộc trò chuyện mới" gọi `POST /api/conversations`, làm mới khung chat và hiển thị câu chào tự động kèm các nút gợi ý câu hỏi. | `test_create_new_conversation_ui` | Fully-Automated |
| **AC-5** | Chọn một phiên chat trong Sidebar tải tối đa 50 tin nhắn gần nhất; cuộn lên trên đỉnh khung chat kích hoạt nạp thêm tin nhắn cũ hơn. | `test_messages_lazy_loading_scroll` | Fully-Automated |
| **AC-6** | Gửi tin nhắn kích hoạt luồng SSE `POST /api/chat/stream`, chữ tự động xuất hiện gõ từng từ liên tục trên khung chat; hiển thị nút trích dẫn khi hoàn tất. | `test_sse_token_streaming_render` | Fully-Automated |
| **AC-7** | Bấm nút "Xem trích dẫn nguồn" mở hộp thoại Popover/Drawer hiển thị tên văn bản, trang, điều khoản và trích đoạn nội dung tài liệu gốc. | `test_citations_drawer_popup` | Fully-Automated |
| **AC-8** | Phiên ở trạng thái `CLOSED` sẽ khóa ô nhập văn bản và hiển thị dải thông báo xám. Phiên ở trạng thái `WAITING_HUMAN` hiển thị dải thông báo màu cam. | `test_conversation_mode_status_banners` | Fully-Automated |

---

## 6. ## Out Of Scope

* Giao diện Bàn làm việc Trực tiếp của Nhân viên CSKH (Live Support Console) và tính năng chat 2 chiều WebSocket (thuộc Khối 3).
* Giao diện Bảng quản lý tiến độ Kanban và Đồng hồ đếm ngược SLA (thuộc Khối 4).
* Giao diện Cấu hình Quy tắc cảm xúc AI Rules và Báo cáo Analytics (thuộc Khối 2 & Khối 4).

---

## 7. ## Constraints

* **Công nghệ UI**: Bắt buộc sử dụng React 18, Vite, Tailwind CSS v4 và Lucide Icons.
* **Tương thích API Backend**: Phải kết nối đúng với các RESTful API endpoints đã hoàn thiện tại `code/backend`:
  - `/api/auth/customer/register`, `/api/auth/customer/login`, `/api/auth/customer/me`
  - `/api/conversations`, `/api/conversations/{id}/messages`, `/api/conversations/{id}/close`
  - `/api/chat/stream` (xử lý luồng `text/event-stream`).
* **Bảo mật Token**: JWT token phải được đính kèm tự động trong Header `Authorization: Bearer <token>` cho mọi HTTP request qua Axios Interceptor.

---

## 8. ## Open Questions

* None (Tất cả yêu cầu và quy tắc nghiệp vụ đã được xác minh làm rõ từ tài liệu phân tích hệ thống).

---

## 9. ## Background / Research Findings

* **Kết quả khảo sát Backend**: Phân hệ Backend cho Khối 1 đã hoàn thiện 100% với 10 Bảng CSDL SQLAlchemy ORM, Bộ máy RAG KH-06 (Sub-query decomposition, Hybrid retriever SQL Product + Supabase pgvector HNSW), module Security JWT & Brute-force lockout 15 phút, và đầy đủ bộ test suites tự động (`tests/test_customer_auth.py`, `tests/test_conversation.py`, `tests/test_rag_pipeline.py`).
* **Cấu trúc Thư mục Frontend**: Đã khởi tạo cấu trúc thư mục tiêu chuẩn tại `code/frontend/src/` theo [`cautruc.md`](file:///d:/Study/TLU/kiemthu/project/docs/overview/cautruc.md) bao gồm `components/chat/`, `pages/customer/`, `context/`, `hooks/`, `services/`, `utils/`.
