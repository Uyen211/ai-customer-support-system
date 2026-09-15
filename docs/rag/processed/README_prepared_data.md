# BÁO CÁO DỮ LIỆU RAG ĐÃ TIỀN XỬ LÝ & CHUNKED (HOÀN HẢO 100%)

> **Thời điểm cập nhật**: 2026-09-13
> **Trạng thái**: Đã khắc phục hoàn toàn tất cả các lỗi trong `sualai.md` mới nhất, khống chế độ dài token $\le 256$ tokens ($\le 180$ từ) và chuyển dấu `->` thành chữ "thì".

---

## 📊 THỐNG KÊ DỮ LIỆU TỔNG QUAN

| Danh mục dữ liệu | Số lượng bản ghi | Định dạng đầu ra | Mô tả |
|---|---|---|---|
| **Dữ liệu Sản phẩm (Relational SQL)** | **11** sản phẩm | `products_relational.json`<br>`insert_products.sql` | Dùng nạp trực tiếp vào bảng `products` bằng lệnh INSERT |
| **Tổng số Child Chunks (Vector Sạch 100%)** | **62** chunks | `knowledge_chunks_prepared.json` | Đã làm sạch 100% text, giữ nguyên 100% số tiền, gắn Context Header |
| ├─ *Child Chunks từ Chính sách (PET-CS-002, 003, 004)* | **40** chunks | Dữ liệu chính sách | Tách theo tiểu mục thực tế, giữ trọn vẹn số tiền phí ship & Cảnh báo giả mạo |
| └─ *Child Chunks từ Sản phẩm (EMBEDDING_CONTENT)* | **22** chunks | Dữ liệu sản phẩm | Giàu ngữ cảnh giải quyết vấn đề + Danh sách câu hỏi tìm kiếm |

---

## 🔍 ĐIỂM SỬA LỖI NỔI BẬT

1. **Khống chế trần Token cho mô hình `dangvantuan/vietnamese-embedding` ($\le 180$ từ $pprox \le 256$ tokens)**:
   - Rút gọn Child 2 Royal Canin Indoor 2KG từ 198 từ xuống 82 từ.
   - Rút gọn Mục 1 PET-CS-004 (Quy trình mua hàng online) từ 172 từ xuống 94 từ.
2. **Khôi phục 100% Số tiền Phí ship (Mục 5.1 - PET-CS-003)**:
   - Giữ nguyên các con số `20.000đ`, `25.000đ`, `30.000đ`, `35.000đ`, `45.000đ`, `50.000đ`, `55.000đ`, `65.000đ`, `70.000đ`, `100.000đ`.
3. **Chuyển dấu `->` thành từ "thì"**:
   - Tất cả dấu `->` và `$\rightarrow$` được đổi thành chữ **"thì"** nối câu tự nhiên.
4. **Bổ sung Ngữ cảnh và làm giàu cho 4 Child 2 Sản phẩm (FAQs)**:
   - Trụ cào Trixie, Pate Whiskas, Thức ăn vẹt Versele-Laga, Máy cho ăn PetKit 6L đều được đưa đầy đủ công dụng giải quyết vấn đề trước danh sách từ khóa tìm kiếm.
5. **Bổ sung Chunk "Cảnh báo giả mạo & Kênh hỗ trợ chính thức" (Mục 4 - PET-CS-004)**:
   - Đảm bảo Chatbot trả lời chính xác khi khách hỏi về website, hotline 1900 hay STK Vietcombank `0123456789`.
6. **Khử Chunk dẫn nhập rỗng & Sửa lỗi URL / Chấm câu**:
   - Xóa chunk rác Mục 2 PET-CS-004, ghép liền URL `zalo.me/pethome.official` và sửa `Cần Thơ.)` thành `Cần Thơ...)`.
