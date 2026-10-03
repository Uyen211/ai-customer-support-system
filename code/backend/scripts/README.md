# 🛠️ Backend Scripts & Utilities

Thư mục này chứa các script tiện ích để hỗ trợ quản trị và bảo trì hệ thống database.

## 📄 Danh sách Script

1. **`fix_db.py`**:
   - Tự động bổ sung các cột còn thiếu trong database (ví dụ: `resolution_note` trong bảng `tickets`).
   - Chạy lệnh: `python scripts/fix_db.py`

2. **`reset_chat_data.py`**:
   - Xóa dữ liệu các cuộc hội thoại, tin nhắn và phiếu hỗ trợ (ticket) để dọn dẹp môi trường test.
   - Chạy lệnh: `python scripts/reset_chat_data.py`
