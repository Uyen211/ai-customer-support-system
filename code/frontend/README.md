# 🎨 Omnichannel Support Frontend (React + Vite + Tailwind CSS)

> Mã nguồn Giao diện Người dùng (Frontend Single Page Application) phục vụ Hệ thống Trợ lý Trực ca CSKH AI & Giám sát Vận hành Tự động, bao gồm Khung Chatbot tự động cho Khách hàng, Bàn làm việc thời gian thực (Live Console) cho Nhân viên CSKH và Bảng quản lý tiến độ SLA (Kanban Board) cho Quản lý.

---

## 📁 Cấu trúc Thư mục Kỹ thuật (Project Directory Structure)

Mã nguồn Frontend được tổ chức chuẩn hóa theo mô hình **Feature-driven Modular Design**:

```text
code/frontend/
├── public/                            # Tài nguyên tĩnh phục vụ public URL
│   ├── sounds/                        # Âm thanh thông báo & chuông báo động
│   │   └── alert.mp3                  # Chuông báo động khi vi phạm SLA / Ticket P1 khẩn cấp
│   └── vite.svg
│
├── src/
│   ├── assets/                        # Hình ảnh, biểu tượng (icons) tĩnh nội bộ
│   │
│   ├── components/                    # Bộ các React UI Components tái sử dụng
│   │   ├── common/                    # Các UI Component nguyên tử dùng chung
│   │   │   ├── Button.jsx             # Nút bấm chuẩn hóa theo Design System
│   │   │   ├── Input.jsx              # Ô nhập dữ liệu kèm kiểm tra lỗi
│   │   │   ├── Modal.jsx              # Hộp thoại Modal Popup
│   │   │   ├── Badge.jsx              # Nhãn trạng thái (P1/P2/P3, ONLINE/BUSY, Mode)
│   │   │   └── LoadingSpinner.jsx     # Biểu tượng chờ nạp dữ liệu
│   │   │
│   │   ├── chat/                      # Các Components cho Khối 1 (Customer Chatbot)
│   │   │   ├── ChatWindow.jsx         # Cửa sổ hội thoại chính
│   │   │   ├── MessageList.jsx        # Khung danh sách tin nhắn
│   │   │   ├── MessageItem.jsx        # Bong bóng tin nhắn & hiệu ứng gõ chữ gõ từng từ
│   │   │   ├── CitationsDrawer.jsx    # Popover / Drawer hiển thị trích dẫn nguồn tài liệu RAG
│   │   │   └── SuggestionButtons.jsx  # Nút gợi ý chủ đề ("Kết nối nhân viên", "Hỏi câu khác")
│   │   │
│   │   ├── agent/                     # Các Components cho Khối 3 (Live Support Console)
│   │   │   ├── QueueList.jsx          # Hàng đợi cuộc trò chuyện cần trợ giúp / cờ đỏ
│   │   │   ├── LiveChatArea.jsx       # Màn hình chat hai chiều real-time Nhân viên - Khách hàng
│   │   │   ├── StatusSwitcher.jsx     # Bộ chuyển trạng thái nhân viên (ONLINE / BUSY / OFFLINE)
│   │   │   ├── CannedResponsePicker.jsx # Menu gợi ý mẫu câu phản hồi nhanh qua phím tắt `/`
│   │   │   └── TakeoverModal.jsx      # Hộp thoại xác nhận tiếp quản phiên trò chuyện
│   │   │
│   │   └── kanban/                    # Các Components cho Khối 4 (Kanban & SLA Engine)
│   │       ├── KanbanBoard.jsx        # Bảng tiến độ 4 cột (Pending, In Progress, Resolved, Closed)
│   │       ├── KanbanColumn.jsx       # Cột chứa các thẻ công việc
│   │       ├── TicketCard.jsx         # Thẻ Ticket tích hợp đồng hồ đếm ngược SLA & đổi màu đỏ quá hạn
│   │       └── ResolveTicketModal.jsx # Popup bắt buộc nhập kết quả xử lý khi giải quyết Ticket
│   │
│   ├── context/                       # Quản lý State toàn cục bằng React Context API
│   │   ├── AuthContext.jsx            # State lưu trữ JWT token, thông tin user & phân quyền Role
│   │   └── SocketContext.jsx          # Khởi tạo và quản lý kết nối WebSocket / Socket.io
│   │
│   ├── hooks/                         # Custom React Hooks đóng gói logic nghiệp vụ
│   │   ├── useAuth.js                 # Hook thao tác Đăng ký, Đăng nhập, Đăng xuất nhanh
│   │   ├── useSSEChat.js              # Hook kết nối luồng SSE Stream (`/chat/stream`) token-by-token
│   │   ├── useSocket.js               # Hook lắng nghe sự kiện WebSocket real-time (`TICKET_ASSIGNED`, `SLA_BREACH_ALERT`)
│   │   └── useSLATimer.js             # Hook tính toán thời gian đếm ngược SLA & đổi màu cảnh báo
│   │
│   ├── pages/                         # Các trang màn hình chính (Pages)
│   │   ├── auth/                      # Phân hệ Xác thực
│   │   │   ├── CustomerLogin.jsx      # Trang đăng nhập Khách hàng
│   │   │   ├── CustomerRegister.jsx   # Trang đăng ký tài khoản Khách hàng
│   │   │   └── AgentLogin.jsx         # Trang đăng nhập Nhân sự nội bộ (Agent / Manager)
│   │   │
│   │   ├── customer/                  # Phân hệ Khách hàng
│   │   │   └── ChatPage.jsx           # Màn hình chat tư vấn RAG tự động 24/7
│   │   │
│   │   └── admin/                     # Phân hệ Quản trị & Nhân sự CSKH
│   │       ├── LiveConsolePage.jsx    # Bàn làm việc thời gian thực của Nhân viên CSKH
│   │       ├── KanbanPage.jsx         # Bàn theo dõi tiến độ Ticket & Đồng hồ SLA
│   │       ├── AIRulesPage.jsx        # Trang cấu hình quy tắc & ngưỡng cảm xúc AI
│   │       └── ReportsPage.jsx        # Màn hình báo cáo chỉ số vận hành & xuất Excel
│   │
│   ├── services/                      # Tầng gọi API mạng (Network API Layer - Axios)
│   │   ├── api.js                     # Khởi tạo Axios Instance (cấu hình Base URL, Interceptors gán Bearer JWT)
│   │   ├── authService.js             # Đăng ký, đăng nhập Customer & Agent
│   │   ├── chatService.js             # Lấy danh sách phiên chat, lịch sử tin nhắn
│   │   ├── ticketService.js           # Truy vấn Ticket, kéo thả Kanban, cập nhật SLA
│   │   ├── cannedService.js           # Truy vấn & quản lý mẫu phản hồi nhanh
│   │   └── reportService.js           # Tải báo cáo thống kê & tải file Excel
│   │
│   ├── utils/                         # Hàm tiện ích & Hằng số dùng chung
│   │   ├── formatters.js              # Định dạng tiền tệ VNĐ (VD: `145.000đ`), định dạng ngày giờ (`DD/MM/YYYY HH:mm`)
│   │   └── constants.js               # Định nghĩa các Enum: STATUS, PRIORITY (P1, P2, P3), MODE (BOT, HUMAN, WAITING_HUMAN)
│   │
│   ├── App.jsx                        # Component gốc điều phối Routing & Provider Wrappers
│   ├── main.jsx                       # Điểm gắn kết React DOM
│   └── index.css                      # Import Tailwind CSS directives & Custom Design System
│
├── Dockerfile                         # Container build giao diện bằng Nginx / Node
├── package.json                       # Khai báo thư viện phụ thuộc
├── README.md                          # Tài liệu hướng dẫn cấu trúc thư mục (File hiện tại)
└── vite.config.js                     # Cấu hình Vite Dev Server & Proxy API về Backend
```

---

## 📖 Hướng Dẫn Sử Dụng & Vai Trò Các Thư Mục Chính

### 1. Thư mục `src/components/`
Chứa toàn bộ các thành phần giao diện UI được chia nhỏ để tái sử dụng.
* **`common/`**: Chứa các thẻ UI dùng chung cho toàn bộ ứng dụng như Button, Input, Modal, Spinner.
* **`chat/`**: Chứa các component khung chat phía Khách hàng (hiển thị danh sách tin nhắn, bong bóng chat gõ từng từ, Drawer xem trích dẫn tài liệu RAG).
* **`agent/`**: Chứa giao diện làm việc thời gian thực cho Nhân viên CSKH (hàng đợi khách cần hỗ trợ, ô chat 2 chiều, menu mẫu câu trả lời nhanh).
* **`kanban/`**: Chứa giao diện bảng quản lý công việc (thẻ Ticket đếm ngược SLA, đổi màu đỏ nhấp nháy khi quá hạn).

### 2. Thư mục `src/pages/`
Chứa các trang chính tương ứng với các tuyến đường dẫn (Routes) của ứng dụng:
* **`auth/`**: Các trang đăng ký, đăng nhập dành cho Khách hàng và Nhân viên CSKH.
* **`customer/`**: Trang chat tư vấn trực tuyến dành cho Khách hàng (`ChatPage.jsx`).
* **`admin/`**: Các trang bàn làm việc CSKH (`LiveConsolePage.jsx`), Quản lý Ticket (`KanbanPage.jsx`), Cấu hình AI (`AIRulesPage.jsx`), và Báo cáo (`ReportsPage.jsx`).

### 3. Thư mục `src/services/`
Đóng vai trò là cầu nối giao tiếp HTTP RESTful API tới Server Backend:
* File **`api.js`** tự động đính kèm Token JWT vào Header `Authorization: Bearer <token>` cho mọi request.
* Các file service (`authService.js`, `chatService.js`, `ticketService.js`...) gom nhóm các câu gọi API theo từng phân hệ nghiệp vụ.

### 4. Thư mục `src/hooks/`
Đóng gói các logic phức tạp bất đồng bộ để các Component dễ dàng gọi lại:
* **`useSSEChat.js`**: Quản lý luồng gõ chữ thời gian thực từ API Backend `/api/chat/stream`.
* **`useSocket.js`**: Kết nối WebSocket song lập để nhận sự kiện tức thì (Ticket mới, cảnh báo vi phạm SLA).
* **`useSLATimer.js`**: Tự động tính toán số giây còn lại của Ticket và cập nhật màu sắc cảnh báo theo thời gian thực.

---

## 🚀 Khởi Chạy Nhanh (Quick Start)

### 1. Cài đặt Thư viện
```bash
cd code/frontend
npm install
```

### 2. Khởi chạy ở Chế độ Development
```bash
npm run dev
```
Giao diện sẽ chạy tại địa chỉ mặc định: [http://localhost:5173](http://localhost:5173) (tự động Proxy request `/api` về Backend Server `http://localhost:8000`).

### 3. Build sản xuất (Production Build)
```bash
npm run build
```
