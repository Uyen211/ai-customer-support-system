# 🔑 Danh Sách Tài Khoản Mẫu & Quyền Hạn (System Accounts)

Tài liệu này tổng hợp toàn bộ các tài khoản mẫu đã được khởi tạo sẵn trong cơ sở dữ liệu (`docs/database/sql.md`) phục vụ kiểm thử và vận hành hệ thống **Omnichannel AI Customer Support System**.

---

## 🔑 Mật Khẩu Mặc Định Chung

> **Mật khẩu cho tất cả tài khoản mẫu (Users & Customers):** `123456`

---

## 1. 👥 Danh Sách Tài Khoản Nhân Viên & Quản Trị (`users` Table)

Các tài khoản này được sử dụng cho **Bàn làm việc CSKH (Live Console)**, **Bảng Kanban SLA**, và **Trang quản trị cấu hình AI Rules**.

| Vai Trò | Mã ID (UUID) | Email Đăng Nhập | Mật Khẩu | Họ Và Tên | Trạng Thái | Kỹ Năng (Skills) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ADMIN** | `a1111111-1111-1111-1111-111111111111` | `admin@brand.com` | `123456` | Quản trị viên Hệ thống | `ONLINE` | `["ALL"]` |
| **MANAGER** | `a2222222-2222-2222-2222-222222222222` | `manager@brand.com` | `123456` | Trưởng phòng CSKH | `ONLINE` | `["ALL"]` |
| **AGENT** | `a3333333-3333-3333-3333-333333333333` | `agent.an@brand.com` | `123456` | Nguyễn Văn An | `ONLINE` | `["Đổi trả", "Giao hàng"]` |
| **AGENT** | `a4444444-4444-4444-4444-444444444444` | `agent.binh@brand.com` | `123456` | Trần Thị Bình | `BUSY` | `["Bảo hành", "Kỹ thuật"]` |

---

## 2. 🛍️ Danh Sách Tài Khoản Khách Hàng (`customers` Table)

Các tài khoản này được sử dụng cho **Trợ lý CSKH AI 24/7 (Customer Chatbot Widget & Web Interface)**.

| STT | Mã ID (UUID) | Email Đăng Nhập | Mật Khẩu | Họ Và Tên | Số Điện Thoại | Phiên Chat Mẫu |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `c1111111-1111-1111-1111-111111111111` | `khachhang1@gmail.com` | `123456` | Lê Hoàng Nam | `0901234567` | Phiên #1 (Mode: `BOT`, Thắc mắc đổi trả) |
| **2** | `c2222222-2222-2222-2222-222222222222` | `khachhang2@gmail.com` | `123456` | Phạm Minh Trang | `0912345678` | Phiên #2 (Mode: `HUMAN`, Khiếu nại giao trễ 5 ngày) |

---

## 3. 🛡️ Quy Định Phân Quyền & Vai Trò (Role & Permissions)

* **ADMIN**: Toàn quyền quản trị hệ thống, thêm/sửa/xóa tài khoản nhân viên, cấu hình AI Rules, xem toàn bộ báo cáo SLA & Kanban.
* **MANAGER**: Giám sát hiệu suất vận hành, nhận thông báo Leo thang SLA (P1/P2 Escalation), điều phối công việc cho Agent, cập nhật Canned Responses (Mẫu phản hồi nhanh).
* **AGENT**: Nhận cuộc trò chuyện chuyển tiếp từ Bot AI, xử lý khiếu nại khách hàng trên Live Console, cập nhật tiến độ Ticket trên bảng Kanban.
* **CUSTOMER**: Trò chuyện trực tiếp với Trợ lý AI Bot 24/7, tra cứu giá & tồn kho sản phẩm, xem trích dẫn tài liệu RAG, yêu cầu chuyển giao sang tư vấn viên.
