# THIẾT KẾ KIỂM THỬ HỘP ĐEN - KHỐI CHỨC NĂNG 2: GIÁM SÁT HỘI THOẠI & KHỞI TẠO YÊU CẦU HỖ TRỢ KHẨN CẤP

> **Đối tượng kiểm thử:** Khối chức năng Giám sát hội thoại và Khởi tạo yêu cầu hỗ trợ khẩn cấp (AI Auto-Triage & Emergency Ticket Engine).  
> **Tài liệu tham chiếu đặc tả:** `docs/overview/usecase.md` (Use Cases 2.1, 2.2, 2.3).  
> **Nguyên tắc hành văn kiểm thử hộp đen:** Mô tả hoàn toàn từ góc nhìn người dùng cuối (End-User / Khách hàng / Quản lý CSKH) trên giao diện website và màn hình làm việc. Không đề cập tới thuật toán nội bộ, cấu trúc bảng CSDL, tên bảng SQL, cơ chế WebSocket hay thuật toán AI. Các trạng thái kỹ thuật được diễn giải dưới dạng thuật ngữ Tiếng Việt kèm chú thích Tiếng Anh theo đúng giao diện hiển thị (VD: *Bức xúc cao (Critical)*, *Tiêu cực nhẹ (Negative)*, *Tích cực (Positive)*, *Chờ tiếp nhận (Pending)*, *Đang xử lý (In Progress)*, *Đã kết thúc (Closed)*, *Chế độ Trợ lý ảo (Bot mode)*, *Chờ tư vấn viên tiếp quản (Waiting for Agent)*).

---

# I. USE CASE 2.1: PHÂN TÍCH CẢM XÚC & ĐÁNH GIÁ NGUY CƠ TỰ ĐỘNG

## 1.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích theo từng trường dữ liệu / chỉ số đánh giá

| Trường dữ liệu / Chỉ số | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Độ dài tin nhắn khách gửi** | • Bắt buộc từ 2 - 1000 ký tự<br>• Không chỉ chứa toàn khoảng trắng | **V_MSG_01:** Chuỗi tin nhắn hợp lệ có độ dài từ 2 - 1000 ký tự | **I_MSG_01:** Để trống không nhập gì<br>**I_MSG_02:** Chỉ chứa toàn khoảng trắng<br>**I_MSG_03:** Ngắn hơn 2 ký tự (1 ký tự)<br>**I_MSG_04:** Dài vượt quá 1000 ký tự | • Biên dưới: 1 ký tự ($I\_$), 2 ký tự ($V\_$), 3 ký tự ($V\_$)<br>• Biên trên: 999 ký tự ($V\_$), 1000 ký tự ($V\_$), 1001 ký tự ($I\_$) |
| **Thang điểm cảm xúc tin nhắn** *(Do hệ thống đánh giá ngầm)* | • Thang điểm từ -1.00 đến +1.00<br>• Quy ước làm tròn 2 chữ số thập phân | **V_SENT_01:** Điểm Bức xúc cao: [-1.00 đến -0.60]<br>**V_SENT_02:** Điểm Tiêu cực nhẹ: [-0.59 đến -0.30]<br>**V_SENT_03:** Điểm Bình thường: [-0.29 đến +0.29]<br>**V_SENT_04:** Điểm Tích cực: [+0.30 đến +1.00] | **I_SENT_01:** Hệ thống phân tích gặp sự cố / Quá thời gian phản hồi (vượt quá 3 giây) $\rightarrow$ Ghi nhận điểm mặc định 0.00 (Bình thường) | • Mốc ranh giới P1: -1.00 ($V\_$), -0.60 ($V\_$), -0.59 ($V\_$)<br>• Mốc ranh giới P2: -0.59 ($V\_$), -0.30 ($V\_$), -0.29 ($V\_$)<br>• Mốc an toàn: +1.00 ($V\_$) |
| **Trạng thái cờ cảnh báo đỏ (is_flagged)** | • Tự động bật cờ đỏ khi điểm cảm xúc $\le -0.30$ | **V_FLAG_01:** Bật cờ cảnh báo đỏ khi điểm cảm xúc đạt mốc P1 hoặc P2 ($\le -0.30$) | **I_FLAG_01:** Điểm cảm xúc an toàn ($> -0.30$) và chưa từng bị cờ đỏ $\rightarrow$ Giữ trạng thái bình thường | Không áp dụng biên (Cờ bật/tắt) |

---

## 1.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Phân tích cảm xúc & Đánh giá nguy cơ

*(Tiền đề quy trình: Khách hàng gửi 1 tin nhắn mới trong phiên trò chuyện đang ở chế độ Trợ lý ảo - Bot mode)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1: Tin nhắn có độ dài hợp lệ (2-1000 ký tự, không chỉ khoảng trắng)?** | F | T | T | T | T | T |
| **C2: Tiến trình phân tích thành công (không bị quá 3 giây/lỗi đường truyền)?** | - | F | T | T | T | T |
| **C3: Điểm cảm xúc thuộc mức Bức xúc cao (-1.00 đến -0.60)?** | - | - | T | F | F | F |
| **C4: Điểm cảm xúc thuộc mức Tiêu cực nhẹ (-0.59 đến -0.30)?** | - | - | - | T | F | F |
| **C5: Khách có nhu cầu gặp nhân viên hoặc hỏi ngoài phạm vi (Out-of-Domain)?** | - | - | - | - | T | F |
| **H1: Bỏ qua phân tích, giữ nguyên trạng thái phiên chat (E-1)** | X | | | | | |
| **H2: Ghi nhận điểm mặc định 0.00 (Bình thường), duy trì cuộc hội thoại (E-3)** | | X | | | | |
| **H3: Bật cờ cảnh báo đỏ, chuyển luồng tạo Ticket P1 khẩn cấp & ngắt Bot AI** | | | X | | | |
| **H4: Bật cờ cảnh báo đỏ, chuyển luồng tạo Ticket P2 & duy trì Bot AI** | | | | X | | |
| **H5: Chuyển luồng tạo Ticket P3 (Trung bình) & ngắt Bot AI chờ tư vấn viên** | | | | | X | |
| **H6: Ghi nhận điểm cảm xúc bình thường/tích cực, duy trì Bot AI hỗ trợ (E-2)** | | | | | | X |

---
---

# II. USE CASE 2.2: KHỞI TẠO PHIẾU HỖ TRỢ KHẨN CẤP VÀ CHUYỂN GIAO CSKH

## 2.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích thông tin Phiếu hỗ trợ (Ticket) và Cam kết SLA

| Trường dữ liệu / Chỉ số | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Đoạn tóm tắt sự cố (Summary)** | • Do hệ thống tự động trích xuất từ 1-10 tin nhắn gần nhất<br>• Độ dài bắt buộc từ 20 đến 255 ký tự | **V_SUM_01:** Chuỗi tóm tắt trích xuất hợp lệ 20 - 255 ký tự | **I_SUM_01:** Trích xuất thất bại / Lỗi nội dung $\rightarrow$ Ghi nhận tóm tắt mặc định: *"Cần kiểm tra thủ công - Lỗi trích xuất tự động"* (E-1) | • Biên dưới: 19 ký tự ($I\_$), 20 ký tự ($V\_$), 21 ký tự ($V\_$)<br>• Biên trên: 254 ký tự ($V\_$), 255 ký tự ($V\_$), 256 ký tự ($I\_$) |
| **Danh mục khiếu nại (Category)** | • Thuộc 1 trong 6 danh mục chuẩn hóa của cửa hàng | **V_CAT_01:** Thuộc danh mục: `Lỗi đơn hàng`, `Đổi trả/Hoàn tiền`, `Sản phẩm lỗi/Hư hại`, `Lỗi thanh toán`, `Thái độ phục vụ` | **I_CAT_01:** Trích xuất không xác định được danh mục $\rightarrow$ Ghi nhận danh mục mặc định: *"Vấn đề khác"* (E-1) | Tập hợp 6 danh mục chuẩn hóa |
| **Mức độ ưu tiên & Hạn chót SLA** | • Phân loại P1, P2, P3 với thời hạn đếm ngược cam kết xử lý tương ứng | **V_SLA_01:** Mức P1 (Cực kỳ khẩn cấp) - SLA đếm ngược đúng **15 phút**<br>**V_SLA_02:** Mức P2 (Khẩn cấp cao) - SLA đếm ngược đúng **60 phút**<br>**V_SLA_03:** Mức P3 (Trung bình) - SLA đếm ngược đúng **240 phút** | **I_SLA_01:** Không xác định mức ưu tiên | • Mốc SLA P1: Đúng 15 phút (900 giây)<br>• Mốc SLA P2: Đúng 60 phút (3600 giây)<br>• Mốc SLA P3: Đúng 240 phút (14400 giây) |
| **Kiểm tra Ticket trùng lặp** | • Mỗi phiên trò chuyện tại một thời điểm chỉ tồn tại tối đa 1 Ticket chưa đóng | **V_TKT_01:** Phiên trò chuyện chưa có Ticket nào ở trạng thái Chờ tiếp nhận/Đang xử lý $\rightarrow$ Tạo Ticket mới | **I_TKT_01:** Phiên đã có sẵn 1 Ticket chưa đóng $\rightarrow$ Thực hiện gom nội dung phàn nàn mới vào Ticket cũ, không tạo trùng (Luồng con A-1) | Không áp dụng biên (Có / Chưa có Ticket mở) |

---

## 2.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Khởi tạo Phiếu hỗ trợ khẩn cấp & Chuyển giao

*(Tiền đề quy trình: Tiến trình nhận được tín hiệu yêu cầu hỗ trợ khẩn cấp P1/P2/P3 từ UC 2.1)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Khách hàng thực hiện xóa phiên trò chuyện trong lúc đang tạo Ticket?** | T | F | F | F | F |
| **C2: Phiên trò chuyện đã có sẵn 1 Phiếu hỗ trợ chưa đóng (Pending/In Progress)?** | - | T | F | F | F |
| **C3: Trích xuất thông tin tự động (Tóm tắt sự cố & Danh mục) thành công?** | - | - | F | T | T |
| **C4: Mức độ ưu tiên của sự cố là P1 (hoặc khiếu nại mới thuộc cấp P1)?** | - | - | - | T | F |
| **H1: Hủy tác vụ, đặt Ticket sang trạng thái Đã kết thúc (Closed - Vô hiệu hóa) (E-3)** | X | | | | |
| **H2: Gom nội dung mới vào Ticket cũ, nếu mức mới cao hơn (P1) thì nâng P1 & reset SLA 15 phút (A-1)** | | X | | | |
| **H3: Tạo Ticket với thông tin mặc định (Summary: "Cần kiểm tra thủ công...", Category: "Vấn đề khác") (E-1)** | | | X | | |
| **H4: Tạo Ticket P1 (SLA 15m), chuyển phiên sang "Chờ tư vấn viên", gửi lời xin lỗi xoa dịu & ngắt Bot AI** | | | | X | |
| **H5: Tạo Ticket P2 (SLA 60m), gửi phiếu ngầm tới hàng đợi & duy trì Bot AI hỗ trợ khách** | | | | | X |

---

## 2.3. Sơ đồ chuyển trạng thái (State Transition)

### Vòng đời Tiến trình Xử lý Phiếu hỗ trợ khẩn cấp (Ticket)

| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- |
| **Khởi tạo mới (New)** | Hệ thống phát hiện sự cố P1/P2/P3 từ cuộc trò chuyện | **Chờ tiếp nhận (Pending)** *(Gán đồng hồ SLA đếm ngược)* |
| **Chờ tiếp nhận (Pending)** | Sự cố có diễn biến khẩn cấp hơn (Khách chửi gắt hơn từ P2 lên P1) | **Chờ tiếp nhận (Pending)** *(Đặt lại SLA 15 phút)* |
| **Chờ tiếp nhận (Pending)** | Tư vấn viên CSKH nhấn "Tiếp quản cuộc trò chuyện" | **Đang xử lý (In Progress)** |
| **Đang xử lý (In Progress)** | Tư vấn viên nhập nội dung giải quyết và bấm "Hoàn tất" | **Đã giải quyết (Resolved)** |
| **Chờ tiếp nhận / Đang xử lý** | Khách hàng thực hiện xóa phiên trò chuyện (UC 1.4) | **Đã kết thúc (Closed - Vô hiệu hóa)** |

---
---

# III. USE CASE 2.3: CẤU HÌNH QUY TẮC PHÂN LOẠI SỰ CỐ VÀ CẢNH BÁO

## 3.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích các trường cấu hình trên màn hình Quản trị

| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Ngưỡng điểm kích hoạt P1 (p1_threshold)** | • Bắt buộc là số âm trong đoạn [-1.00, 0.00]<br>• Bắt buộc phải nhỏ hơn Ngưỡng điểm P2 | **V_P1_01:** Số âm trong khoảng [-1.00 đến < p2_threshold] (VD: `-0.60`) | **I_P1_01:** Để trống không nhập<br>**I_P1_02:** Số dương (VD: `0.50`)<br>**I_P1_03:** Nhỏ hơn -1.00 (VD: `-1.50`)<br>**I_P1_04:** Lớn hơn hoặc bằng Ngưỡng điểm P2 (VD: `-0.20` khi P2 là `-0.30`) | • Biên dưới: -1.00 ($V\_$), -1.01 ($I\_$)<br>• Cận biên P2: `p2_threshold - 0.01` ($V\_$), `p2_threshold` ($I\_$) |
| **Ngưỡng điểm kích hoạt P2 (p2_threshold)** | • Bắt buộc là số âm trong đoạn [-1.00, 0.00]<br>• Bắt buộc phải lớn hơn Ngưỡng điểm P1 | **V_P2_01:** Số âm trong khoảng [> p1_threshold đến 0.00] (VD: `-0.30`) | **I_P2_01:** Để trống không nhập<br>**I_P2_02:** Số dương (VD: `0.20`)<br>**I_P2_03:** Nhỏ hơn hoặc bằng Ngưỡng điểm P1 (VD: `-0.70` khi P1 là `-0.60`) | • Biên trên: 0.00 ($V\_$), 0.01 ($I\_$)<br>• Cận biên P1: `p1_threshold + 0.01` ($V\_$), `p1_threshold` ($I\_$) |
| **Hướng dẫn nghiệp vụ bằng ngôn ngữ tự nhiên** | • Văn bản hướng dẫn tự do giải thích quy tắc phân loại | **V_PROMPT_01:** Đoạn văn bản mô tả nghiệp vụ (VD: *"Nếu khách phản ánh sai mẫu mã sản phẩm, phân loại vào P1"*) | **I_PROMPT_01:** Để trống không nhập hướng dẫn | Phân vùng chuỗi có dữ liệu / để trống |
| **Quyền truy cập màn hình cấu hình** | • Chỉ dành riêng cho vai trò Quản lý (Manager) hoặc Quản trị viên (Admin) | **V_AUTH_01:** Đăng nhập với tài khoản có vai trò Quản lý / Admin | **I_AUTH_01:** Đăng nhập với tài khoản Nhân viên tư vấn (Agent) $\rightarrow$ Chặn truy cập | Phân quyền truy cập |

---

## 3.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Cấu hình Quy tắc Cảnh báo

*(Tiền đề quy trình: Quản lý/Admin bấm nút "Lưu thay đổi" trên màn hình Cấu hình Quy tắc Cảnh báo)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: Người dùng có quyền Quản lý (Manager) hoặc Quản trị viên (Admin)?** | F | T | T | T |
| **C2: Các trường ngưỡng điểm P1, P2 là số âm hợp lệ trong khoảng [-1.00, 0.00]?** | - | F | T | T |
| **C3: Ngưỡng điểm kích hoạt P1 nhỏ hơn Ngưỡng điểm kích hoạt P2 (P1 < P2)?** | - | - | F | T |
| **H1: Chặn truy cập, hiển thị thông báo lỗi phân quyền "Bạn không có quyền..."** | X | | | |
| **H2: Hiển thị lỗi cảnh báo đỏ: "Ngưỡng điểm cấu hình phải là số âm từ -1.00 đến 0.00" (E-1)** | | X | | |
| **H3: Hiển thị lỗi cảnh báo đỏ: "Điểm kích hoạt P1 phải nhỏ hơn điểm kích hoạt P2" (E-1)** | | | X | |
| **H4: Lưu thành công, thông báo xanh "Cập nhật cấu hình thành công" & áp dụng tức thì** | | | | X |

---
---

# IV. MA TRẬN TRUY XUẤT NGUỒN GỐC (TRACEABILITY MATRIX - RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 2.1 - Luồng chính** | Đánh giá tin nhắn tiêu cực nhẹ (P2) & Bức xúc cao (P1) | `TC_AUC_01`, `TC_AUC_02` |
| **UC 2.1 - E-1** | Bỏ qua phân tích tin nhắn rỗng / khoảng trắng / 1 ký tự | `TC_AUC_03` |
| **UC 2.1 - E-2** | Điểm cảm xúc bình thường / tích cực (Không chạm ngưỡng nguy cơ) | `TC_AUC_04` |
| **UC 2.1 - E-3** | Sự cố tiến trình phân tích bị quá 3 giây (Fallback về 0.00) | `TC_AUC_05` |
| **UC 2.1 - Rule 3** | Quy tắc duy trì cờ đỏ (Không tự động gỡ cờ đỏ khi khách hạ giận) | `TC_AUC_06` |
| **UC 2.2 - Luồng chính** | Khởi tạo Phiếu hỗ trợ P1 khẩn cấp (SLA 15m) & P2 (SLA 60m) | `TC_AUC_07`, `TC_AUC_08` |
| **UC 2.2 - A-1** | Gom khiếu nại mới vào Ticket cũ & Nâng priority lên P1 nếu gắt hơn | `TC_AUC_09` |
| **UC 2.2 - E-1** | Sự cố trích xuất thông tin $\rightarrow$ Tạo Ticket với thông tin mặc định | `TC_AUC_10` |
| **UC 2.2 - E-3** | Vô hiệu hóa Ticket (Closed) khi phiên trò chuyện bị khách xóa | `TC_AUC_11` |
| **UC 2.3 - Luồng chính** | Quản lý cập nhật bộ quy tắc cấu hình thành công | `TC_AUC_12` |
| **UC 2.3 - E-1** | Lỗi nhập ngưỡng điểm P1 lớn hơn hoặc bằng P2 | `TC_AUC_13` |
| **UC 2.3 - Rule 1** | Chặn nhân viên tư vấn (Agent) truy cập trang cấu hình | `TC_AUC_14` |

---
---

# V. THIẾT KẾ CA KIỂM THỬ CHI TIẾT (TEST CASE SPECIFICATION - IEEE)

## 5.1. Nhóm Test Case: UC 2.1 - Phân tích cảm xúc & Đánh giá nguy cơ

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_AUC_01** | Kiểm tra phân tích tin nhắn thuộc mức Bức xúc cao P1 (Happy Path) | Khu vực chat ở chế độ Trợ lý ảo, ngưỡng P1 là `-0.60` | 1. Nhập tin nhắn thể hiện sự giận dữ gắt gao.<br>2. Nhấn nút "Gửi".<br>3. Quan sát phản hồi và giao diện. | Nội dung: `"Shop lừa đảo, chuyển tiền xong không thấy giao hàng, làm ăn như rác rưởi!"` ($V\_$) | Hệ thống đánh giá điểm cảm xúc $\le -0.60$ (`CRITICAL`), bật cờ cảnh báo đỏ trên phiên trò chuyện, ngắt phản hồi tự động của AI Bot và gửi câu xin lỗi xoa dịu. Cuộc trò chuyện đưa lên vị trí ưu tiên hàng đợi. | Pass |
| **TC_AUC_02** | Kiểm tra phân tích tin nhắn thuộc mức Tiêu cực nhẹ P2 | Cấu hình ngưỡng P2 là `-0.30` | 1. Nhập tin nhắn phàn nàn nhẹ.<br>2. Nhấn nút "Gửi". | Nội dung: `"Giao hàng chậm quá shop ơi, đợi mãi không thấy đâu chán ghê."` ($V\_$) | Điểm cảm xúc xếp mức Tiêu cực nhẹ (`NEGATIVE`), bật cờ cảnh báo đỏ, tự động khởi tạo ngầm phiếu hỗ trợ P2. Trợ lý ảo **vẫn tiếp tục duy trì trả lời tự động** cho khách. | Pass |
| **TC_AUC_03** | Kiểm tra gửi tin nhắn 1 ký tự (Bỏ qua phân tích - E-1) | Đang ở cửa sổ chat với Trợ lý ảo | 1. Gõ 1 ký tự duy nhất.<br>2. Nhấn nút "Gửi". | Nội dung: `"A"` ($I\_$) | Khung chat báo lỗi nhắc nhở: *"Nội dung câu hỏi phải chứa từ 2 ký tự trở lên"*. Tiến trình không chấm điểm cảm xúc, giữ nguyên trạng thái phiên chat. | Pass |
| **TC_AUC_04** | Kiểm tra gửi tin nhắn khen ngợi tích cực (E-2) | Khung chat đang ở trạng thái bình thường | 1. Nhập tin nhắn khen dịch vụ.<br>2. Nhấn nút "Gửi". | Nội dung: `"Shop giao hàng siêu nhanh, nhân viên tư vấn nhiệt tình lắm!"` ($V\_$) | Đánh giá điểm cảm xúc Tích cực (`POSITIVE`), ghi nhận lịch sử phiên chat. Không bật cờ cảnh báo đỏ, AI Bot tiếp tục hỗ trợ bình thường. | Pass |
| **TC_AUC_05** | Kiểm tra xử lý sự cố tiến trình phân tích quá 3 giây (E-3) | Hệ thống nghẽn mạng / Phân tích phản hồi chậm | 1. Gửi một tin nhắn bất kỳ.<br>2. Giả lập tiến trình phân tích phản hồi vượt quá 3 giây. | Nội dung: `"Tôi muốn hỏi về đơn hàng"` | Tiến trình tự động ghi nhận điểm cảm xúc mặc định là `0.00` (Bình thường). Cuộc hội thoại của khách hàng không bị ngắt quãng hay báo lỗi crash. | Pass |
| **TC_AUC_06** | Kiểm tra quy tắc duy trì cờ đỏ khi khách nói câu tích cực tiếp theo | Phiên trò chuyện đã bị bật cờ đỏ ở `TC_AUC_01` trước đó | 1. Khách hàng gửi tiếp một tin nhắn ngắn có thái độ nguội bớt.<br>2. Quan sát cờ cảnh báo đỏ trên giao diện. | Nội dung: `"Dạ vâng shop kiểm tra giúp em"` | Hệ thống ghi nhận điểm cảm xúc tin mới, nhưng **tuyệt đối không tự động gỡ cờ đỏ** của phiên trò chuyện. Cờ đỏ tiếp tục duy trì cho tới khi tư vấn viên vào tiếp quản. | Pass |

---

## 5.2. Nhóm Test Case: UC 2.2 - Khởi tạo Phiếu hỗ trợ khẩn cấp

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_AUC_07** | Kiểm tra khởi tạo Phiếu hỗ trợ khẩn cấp P1 (SLA 15 phút) | Phiên trò chuyện vừa phát sinh sự cố Bức xúc cao P1 | 1. Quan sát bảng công việc của nhân viên CSKH.<br>2. Kiểm tra thông tin phiếu hỗ trợ mới đẻ ra. | Tín hiệu chuyển từ `TC_AUC_01` | Một Phiếu hỗ trợ mới xuất hiện ở trạng thái *Chờ tiếp nhận (Pending)*, danh mục khiếu nại và tóm tắt sự cố được tự động điền đầy đủ. Đồng hồ SLA đếm ngược đúng **15 phút**. | Pass |
| **TC_AUC_08** | Kiểm tra khởi tạo Phiếu hỗ trợ P2 (SLA 60 phút) | Phiên trò chuyện phát sinh phàn nàn P2 | 1. Quan sát danh sách hàng đợi công việc. | Tín hiệu từ `TC_AUC_02` | Phiếu hỗ trợ mới được tạo ra ngầm với mức ưu tiên P2, trạng thái *Chờ tiếp nhận (Pending)* và đồng hồ SLA đếm ngược đúng **60 phút**. | Pass |
| **TC_AUC_09** | Kiểm tra leo thang sự cố và nâng SLA từ P2 lên P1 (Luồng con A-1) | Phiên chat đã có sẵn 1 Ticket P2 chưa đóng từ `TC_AUC_08` | 1. Khách hàng gửi tiếp 1 tin nhắn chửi bới gắt gao thuộc cấp P1.<br>2. Kiểm tra phiếu hỗ trợ hiện tại trên màn hình nhân viên. | Nội dung: `"Tôi sẽ báo công an nếu không xử lý ngay!"` | Hệ thống **không tạo trùng Ticket mới**, mà gom tin nhắn mới vào Ticket P2 cũ, tự động nâng mức ưu tiên của Ticket cũ lên **P1** và reset đồng hồ SLA đếm ngược về **15 phút**. | Pass |
| **TC_AUC_10** | Kiểm tra khởi tạo Ticket với thông tin mặc định khi lỗi trích xuất (E-1) | Tiến trình tự động trích xuất nội dung bị gián đoạn/lỗi | 1. Phát tín hiệu tạo Ticket khi trích xuất thông tin thất bại. | Dữ liệu trích xuất rỗng / lỗi | Tạo Phiếu hỗ trợ khẩn cấp với thông tin mặc định: Tóm tắt sự cố là *"Cần kiểm tra thủ công - Lỗi trích xuất tự động"* và Danh mục là *"Vấn đề khác"*. Đồng hồ SLA đếm ngược 60 phút. | Pass |
| **TC_AUC_11** | Kiểm tra tự động vô hiệu hóa Ticket khi khách xóa phiên chat (E-3) | Có 1 Ticket P1 đang ở trạng thái *Chờ tiếp nhận (Pending)* | 1. Khách hàng thực hiện xóa phiên trò chuyện (UC 1.4).<br>2. Kiểm tra thẻ Ticket trên bảng công việc nhân viên. | Thao tác Xóa phiên trò chuyện | Ticket liên quan lập tức tự động chuyển sang trạng thái **Đã kết thúc (Closed - Vô hiệu hóa)** với lý do *"Phiên hội thoại đã bị khách hàng xóa"*, ngắt đồng hồ SLA và gỡ khỏi hàng đợi phân công. | Pass |

---

## 5.3. Nhóm Test Case: UC 2.3 - Cấu hình Quy tắc Phân loại Cảnh báo

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_AUC_12** | Kiểm tra Quản lý cập nhật quy tắc cấu hình thành công (Happy Path) | Đăng nhập tài khoản Quản lý (Manager), đang ở trang "Cấu hình Cảnh báo" | 1. Nhập Ngưỡng P1 hợp lệ.<br>2. Nhập Ngưỡng P2 hợp lệ.<br>3. Nhập văn bản Hướng dẫn nghiệp vụ.<br>4. Bấm nút "Lưu thay đổi". | • P1: `-0.70` ($V\_$)<br>• P2: `-0.35` ($V\_$)<br>• Hướng dẫn: `"Ưu tiên P1 cho lỗi thanh toán"` | Hiển thị thông báo xanh: *"Cập nhật cấu hình thành công"*. Mọi tin nhắn tiếp theo của khách hàng được phân tích dựa trên bộ quy tắc mới này ngay lập tức. | Pass |
| **TC_AUC_13** | Kiểm tra báo lỗi khi nhập Ngưỡng P1 lớn hơn P2 (E-1) | Đang ở trang "Cấu hình Cảnh báo" | 1. Nhập Ngưỡng P1 lớn hơn P2.<br>2. Bấm nút "Lưu thay đổi". | • P1: `-0.20` ($I\_$)<br>• P2: `-0.50` ($V\_$) | Thao tác lưu bị chặn, hiển thị thông báo lỗi màu đỏ ngay dưới ô nhập: *"Điểm kích hoạt P1 phải nhỏ hơn điểm kích hoạt P2"*. | Pass |
| **TC_AUC_14** | Kiểm tra chặn Nhân viên tư vấn (Agent) truy cập trang cấu hình | Đăng nhập tài khoản Nhân viên tư vấn (`agent.an@brand.com`) | 1. Cố gắng điều hướng truy cập vào đường dẫn trang Cấu hình Quy tắc. | Điều hướng trang Cấu hình | Hệ thống chặn truy cập, hiển thị thông báo lỗi: *"Bạn không có quyền truy cập trang cấu hình này"* và chuyển hướng về màn hình Bàn làm việc CSKH. | Pass |

---
*Tài liệu kiểm thử hộp đen Khối chức năng 2 đã được chuẩn hóa trọn vẹn 100%, bổ sung đầy đủ EP/BVA, Decision Table, State Transition, RTM và bộ 14 Test Cases chuẩn IEEE.*
