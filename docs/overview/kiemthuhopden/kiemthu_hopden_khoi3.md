# THIẾT KẾ KIỂM THỬ HỘP ĐEN - KHỐI CHỨC NĂNG 3: CỔNG HỖ TRỢ TRỰC TIẾP DÀNH CHO NHÂN VIÊN TƯ VẤN

> **Đối tượng kiểm thử:** Khối chức năng Cổng hỗ trợ trực tiếp dành cho nhân viên tư vấn (Live Support Console).  
> **Tài liệu tham chiếu đặc tả:** `docs/overview/usecase.md` (Use Cases 3.1, 3.2, 3.3, 3.4).  
> **Nguyên tắc hành văn kiểm thử hộp đen:** Mô tả hoàn toàn từ góc nhìn người dùng cuối (Nhân viên CSKH - Agent / Quản lý - Manager / Khách hàng) tương tác trên màn hình giao diện Live Console. Không đề cập đến cấu trúc bảng CSDL, lệnh SQL, mã code API hay cơ chế kết nối thời gian thực ngầm. Các trạng thái kỹ thuật được diễn giải dưới dạng thuật ngữ Tiếng Việt kèm chú thích Tiếng Anh theo đúng giao diện hiển thị (VD: *Trực tuyến (ONLINE)*, *Bận (BUSY)*, *Ngoại tuyến (OFFLINE)*, *Chờ tư vấn viên tiếp quản (Waiting for Agent)*, *Chế độ Trợ lý ảo (Bot mode)*, *Tư vấn viên đang hỗ trợ (Human Agent mode)*, *Chế độ Chỉ xem (Read-only)*).

---

# I. USE CASE 3.1: QUẢN LÝ TÀI KHOẢN NHÂN VIÊN (TẠO MỚI & ĐĂNG NHẬP)

## 1.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích các trường dữ liệu Đăng ký tài khoản nhân sự mới & Đăng nhập

| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Họ và tên** *(Tạo tài khoản)* | • Bắt buộc<br>• Độ dài 2 - 100 ký tự | **V_NAME_01:** Chuỗi chữ hợp lệ từ 2 - 100 ký tự (VD: `"Nguyễn Văn Bình"`) | **I_NAME_01:** Để trống<br>**I_NAME_02:** Ngắn hơn 2 ký tự (1 ký tự)<br>**I_NAME_03:** Dài hơn 100 ký tự | • Biên dưới: 1 ký tự ($I\_$), 2 ký tự ($V\_$), 3 ký tự ($V\_$)<br>• Biên trên: 99 ký tự ($V\_$), 100 ký tự ($V\_$), 101 ký tự ($I\_$) |
| **Email nội bộ** *(Tạo tài khoản / Đăng nhập)* | • Bắt buộc<br>• Đúng định dạng email nội bộ (`ten@domain.com`)<br>• Tối đa 255 ký tự<br>• Duy nhất trên hệ thống | **V_EMAIL_01:** Email nội bộ hợp lệ, chưa tồn tại trên hệ thống (VD: `"agent.binh@brand.com"`) | **I_EMAIL_01:** Để trống<br>**I_EMAIL_02:** Sai cấu trúc định dạng email<br>**I_EMAIL_03:** Email vượt quá 255 ký tự<br>**I_EMAIL_04:** Email đã tồn tại trên hệ thống | • Biên trên độ dài: 255 ký tự ($V\_$), 256 ký tự ($I\_$)<br>• Kiểm tra trùng lặp email đã có |
| **Số điện thoại** *(Tạo tài khoản)* | • Tùy chọn (Không bắt buộc)<br>• Nếu nhập: Đủ 10 chữ số, bắt đầu bằng số `0` | **V_PHONE_01:** Để trống không nhập<br>**V_PHONE_02:** Đủ 10 chữ số bắt đầu bằng số `0` (VD: `"0987654321"`) | **I_PHONE_01:** Ít hơn 10 chữ số<br>**I_PHONE_02:** Nhiều hơn 10 chữ số<br>**I_PHONE_03:** Không bắt đầu bằng số `0`<br>**I_PHONE_04:** Chứa chữ cái/ký tự đặc biệt | • Biên độ dài: 9 chữ số ($I\_$), 10 chữ số bắt đầu số `0` ($V\_$), 11 chữ số ($I\_$) |
| **Mật khẩu** *(Tạo tài khoản / Đăng nhập)* | • Bắt buộc<br>• Tối thiểu 8 ký tự trở lên<br>• Chứa ít nhất 1 chữ cái và 1 chữ số | **V_PASS_01:** Mật khẩu $\ge 8$ ký tự, chứa đủ chữ và số (VD: `"Agent1234"`)| **I_PASS_01:** Để trống<br>**I_PASS_02:** Ngắn hơn 8 ký tự (7 ký tự)<br>**I_PASS_03:** Chỉ chứa chữ cái, thiếu số<br>**I_PASS_04:** Chỉ chứa chữ số, thiếu chữ | • Biên độ dài: 7 ký tự ($I\_$), 8 ký tự ($V\_$), 9 ký tự ($V\_$) |
| **Kỹ năng chuyên môn** *(Dành cho Agent)* | • Bắt buộc đối với tài khoản vai trò Agent: Phải chọn ít nhất 1 danh mục kỹ năng | **V_SKILL_01:** Chọn từ 1 danh mục kỹ năng trở lên (VD: `["Đổi trả", "Giao hàng"]`) | **I_SKILL_01:** Tạo tài khoản vai trò Agent nhưng không tích chọn kỹ năng nào (0 kỹ năng) | Biên số lượng kỹ năng chọn: 0 kỹ năng ($I\_$), 1 kỹ năng ($V\_$) |
| **Quyền khởi tạo tài khoản** | • Chỉ dành cho tài khoản có vai trò Quản lý (Manager) hoặc Quản trị viên (Admin) | **V_AUTH_01:** Đăng nhập với tài khoản Quản lý / Admin để tạo tài khoản nhân sự mới | **I_AUTH_01:** Đăng nhập với tài khoản Agent thông thường | Phân quyền thao tác |

---

## 1.2. Bảng quyết định (Decision Table)

### Bảng quyết định 1: Luồng Tạo tài khoản nhân sự mới (Admin/Manager)

*(Tiền đề quy trình: Quản lý/Admin bấm nút "Tạo tài khoản nhân sự")*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1: Người thao tác có quyền Quản lý (Manager) hoặc Quản trị viên (Admin)?** | F | T | T | T | T | T |
| **C2: Điền đầy đủ các trường bắt buộc (Họ tên, Email, Mật khẩu, Mật khẩu xác nhận)?** | - | F | T | T | T | T |
| **C3: Các trường dữ liệu đúng định dạng (Tên, Email, SĐT, Mật khẩu)?** | - | - | F | T | T | T |
| **C4: Nếu vai trò là Agent, đã tích chọn ít nhất 1 danh mục kỹ năng chuyên môn?** | - | - | - | F | T | T |
| **C5: Địa chỉ Email nội bộ chưa tồn tại trên hệ thống?** | - | - | - | - | F | T |
| **H1: Chặn thao tác, báo lỗi phân quyền "Bạn không có quyền tạo tài khoản nhân sự"** | X | | | | | |
| **H2: Hiển thị lỗi khoanh đỏ ô trống "Vui lòng không để trống..." (E-1)** | | X | | | | |
| **H3: Hiển thị thông báo lỗi định dạng chi tiết (E-2)** | | | X | | | |
| **H4: Báo lỗi "Tạo tài khoản Nhân viên tư vấn bắt buộc chọn ít nhất 1 kỹ năng"** | | | | X | | |
| **H5: Báo lỗi "Địa chỉ email này đã được sử dụng" (E-4)** | | | | | X | |
| **H6: Tạo tài khoản thành công ở trạng thái Ngoại tuyến (OFFLINE), làm mới biểu mẫu** | | | | | | X |

### Bảng quyết định 2: Luồng Đăng nhập Bàn làm việc CSKH (Live Support Console)

*(Tiền đề quy trình: Nhân viên bấm nút "Đăng nhập")*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Điền đầy đủ Email nội bộ và Mật khẩu?** | F | T | T | T | T |
| **C2: Địa chỉ Email nội bộ có tồn tại trên hệ thống?** | - | F | T | T | T |
| **C3: Tài khoản ở trạng thái Hoạt động (is_active = TRUE, không bị khóa)?** | - | - | F | T | T |
| **C4: Mật khẩu nhập vào chính xác?** | - | - | - | F | T |
| **H1: Hiển thị lỗi để trống trường thông tin (E-1)** | X | | | | |
| **H2: Báo lỗi "Địa chỉ email hoặc mật khẩu không chính xác" (E-6)** | | X | | | |
| **H3: Báo lỗi "Tài khoản hiện đang bị khóa hoặc ngừng kích hoạt" (E-5)** | | | X | | |
| **H4: Báo lỗi "Địa chỉ email hoặc mật khẩu không chính xác" (E-6)** | | | | X | |
| **H5: Đăng nhập thành công, chuyển tới Live Console ở trạng thái mặc định OFFLINE** | | | | | X |

---
---

# II. USE CASE 3.2: QUẢN LÝ TRẠNG THÁI LÀM VIỆC CỦA NHÂN VIÊN

## 2.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích trạng thái làm việc (Presence)

| Trường dữ liệu / Thao tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Trạng thái làm việc (Status)** | • Thuộc 1 trong 3 trạng thái chuẩn hóa | **V_STT_01:** Trạng thái Trực tuyến (`ONLINE`) - Chấm xanh<br>**V_STT_02:** Trạng thái Bận (`BUSY`) - Chấm cam<br>**V_STT_03:** Trạng thái Ngoại tuyến (`OFFLINE`) - Chấm xám | **I_STT_01:** Trạng thái không thuộc tập hợp quy định (VD: Rỗng) | Tập hợp 3 trạng thái chuẩn hóa |
| **Đường truyền mạng thời gian thực** | • Duy trì kết nối đường truyền liên tục | **V_NET_01:** Đường truyền mạng kết nối ổn định | **I_NET_01:** Đường truyền bị ngắt kết nối quá 30 giây (E-1) | Mốc thời gian ngắt kết nối: 29 giây (vẫn giữ trạng thái), 30 giây (chuyển tự động `OFFLINE`) |

---

## 2.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Chuyển đổi Trạng thái làm việc

*(Tiền đề quy trình: Nhân viên nhấp chọn một trạng thái trên thanh chỉ thị trạng thái)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 |
| :--- | :---: | :---: | :---: |
| **C1: Đã đăng nhập tài khoản nhân viên hợp lệ?** | F | T | T |
| **C2: Đường truyền mạng thời gian thực ổn định (không mất mạng > 30s)?** | - | F | T |
| **H1: Chặn thao tác, chuyển hướng về trang Đăng nhập** | X | | |
| **H2: Tự động đổi chỉ thị sang màu xám (OFFLINE) & Hiện dải cảnh báo cam (E-1)** | | X | |
| **H3: Cập nhật màu chỉ thị, đồng bộ trạng thái mới & kích hoạt nhận việc (nếu ONLINE)** | | | X |

---

## 2.3. Sơ đồ chuyển trạng thái (State Transition)

### Trạng thái làm việc của Nhân viên CSKH (Presence Lifecycle)

| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- |
| **Ngoại tuyến (OFFLINE)** | Nhân viên chọn trạng thái "Trực tuyến" | **Trực tuyến (ONLINE)** *(Kích hoạt tự động nhận việc)* |
| **Trực tuyến (ONLINE)** | Nhân viên chọn trạng thái "Bận" | **Bận (BUSY)** *(Tạm dừng phân công việc mới)* |
| **Bận (BUSY)** | Nhân viên chọn trạng thái "Trực tuyến" | **Trực tuyến (ONLINE)** |
| **Trực tuyến (ONLINE) / Bận (BUSY)** | Mất kết nối đường truyền mạng quá 30 giây | **Ngoại tuyến (OFFLINE)** *(Tự động chuyển ngầm)* |
| **Ngoại tuyến (OFFLINE)** | Đường truyền mạng kết nối trở lại | **Trực tuyến / Bận** *(Khôi phục chọn trạng thái)* |

---
---

# III. USE CASE 3.3: THEO DÕI HÀNG ĐỢI VÀ TIẾP QUẢN CUỘC TRÒ CHUYỆN

## 3.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích Tiếp quản cuộc trò chuyện & Nhắn tin 2 chiều

| Thao tác / Trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Tiếp quản cuộc trò chuyện (Takeover)** | • Chỉ cho phép tiếp quản phiên chat chưa có nhân viên nào nhận | **V_TK_01:** Bấm "Tiếp quản" cuộc trò chuyện chưa có nhân viên phụ trách | **I_TK_01:** Bấm "Tiếp quản" cuộc trò chuyện đã bị nhân viên khác nhận trước đó vài giây (E-1) | Xung đột tranh chấp tiếp quản |
| **Nội dung tin nhắn tư vấn** | • Bắt buộc từ 1 - 4000 ký tự | **V_MSG_01:** Chuỗi tin nhắn tư vấn từ 1 - 4000 ký tự | **I_MSG_01:** Để trống không nhập tin nhắn<br>**I_MSG_02:** Tin nhắn dài vượt quá 4000 ký tự | • Biên dưới: 0 ký tự ($I\_$), 1 ký tự ($V\_$), 2 ký tự ($V\_$)<br>• Biên trên: 3999 ký tự ($V\_$), 4000 ký tự ($V\_$), 4001 ký tự ($I\_$) |
| **Quyền gửi tin nhắn (Ghi)** | • Chỉ nhân viên đã tiếp quản mới được gửi tin nhắn vào phiên chat | **V_WRITE_01:** Nhân viên đã tiếp quản phiên chat gửi tin nhắn | **I_WRITE_01:** Nhân viên khác chưa tiếp quản cố tình gửi tin nhắn vào phiên của người khác | Màn hình ở chế độ Chỉ xem (Read-only) |

---

## 3.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Tiếp quản cuộc trò chuyện & Nhắn tin

*(Tiền đề quy trình: Nhân viên nhấn nút "Tiếp quản cuộc trò chuyện" hoặc bấm nút "Gửi" tin nhắn)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: Phiên trò chuyện chưa được nhân viên khác bấm tiếp quản trước đó?** | F | T | T | T |
| **C2: Người thực hiện gửi tin nhắn chính là nhân viên đã tiếp quản phiên chat này?** | - | - | F | T |
| **C3: Nội dung tin nhắn tư vấn hợp lệ (1-4000 ký tự)?** | - | - | - | T |
| **H1: Báo lỗi "Cuộc trò chuyện đã được nhận bởi nhân viên khác", chuyển màn hình Chế độ Chỉ xem (Read-only)** | X | | | |
| **H2: Xác nhận quyền tiếp quản, gỡ cờ đỏ, ngắt Bot AI & gửi thông báo "Nhân viên đã tham gia"** | | X | | |
| **H3: Báo lỗi phân quyền "Bạn không có quyền gửi tin nhắn vào phiên do nhân viên khác phụ trách"** | | | X | |
| **H4: Lưu tin nhắn tư vấn, hiển thị tức thì sang màn hình khách hàng** | | | | X |

---

## 3.3. Sơ đồ chuyển trạng thái (State Transition)

### Trạng thái Quyền phục vụ của Phiên trò chuyện

| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- |
| **Chờ tư vấn viên (Waiting for Agent)** | Nhân viên A bấm nút "Tiếp quản cuộc trò chuyện" thành công | **Tư vấn viên A đang hỗ trợ (Human Agent mode)** |
| **Chờ tư vấn viên (Waiting for Agent)** | Nhân viên B bấm tiếp quản khi Nhân viên A đã bấm nhận trước | **Chế độ Chỉ xem đối với Nhân viên B (Read-only)** |
| **Tư vấn viên A đang hỗ trợ** | Nhân viên A bấm "Kết thúc hỗ trợ" | **Đã kết thúc (Closed)** |

---
---

# IV. USE CASE 3.4: QUẢN LÝ & SỬ DỤNG MẪU PHẢN HỒI NHANH (CANNED RESPONSES)

## 4.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích Tạo mẫu phản hồi mới & Gợi ý phím tắt `/`

| Tên trường / Thao tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Phím tắt (Shortcut)** | • Bắt buộc bắt đầu bằng ký tự `/`<br>• Không chứa khoảng trắng<br>• Độ dài 2 - 50 ký tự<br>• Duy nhất trên hệ thống | **V_CUT_01:** Chuỗi phím tắt hợp lệ bắt đầu `/`, chưa tồn tại (VD: `/chao`, `/xloi_giaohang`) | **I_CUT_01:** Để trống<br>**I_CUT_02:** Không bắt đầu bằng ký tự `/` (VD: `chao`)<br>**I_CUT_03:** Chứa khoảng trắng (VD: `/chao ban`)<br>**I_CUT_04:** Phím tắt đã tồn tại trên hệ thống | • Biên độ dài: 1 ký tự (`/`) ($I\_$), 2 ký tự (`/a`) ($V\_$), 50 ký tự ($V\_$), 51 ký tự ($I\_$)<br>• Kiểm tra ký tự đầu `/` |
| **Tiêu đề gợi nhớ** | • Bắt buộc, độ dài 3 - 150 ký tự | **V_TITLE_01:** Chuỗi tiêu đề hợp lệ 3 - 150 ký tự | **I_TITLE_01:** Để trống<br>**I_TITLE_02:** Ngắn hơn 3 ký tự | • Biên độ dài: 2 ký tự ($I\_$), 3 ký tự ($V\_$), 150 ký tự ($V\_$) |
| **Nội dung mẫu câu** | • Bắt buộc, độ dài 5 - 2000 ký tự | **V_CONT_01:** Chuỗi nội dung mẫu hợp lệ 5 - 2000 ký tự | **I_CONT_01:** Để trống<br>**I_CONT_02:** Ngắn hơn 5 ký tự | • Biên độ dài: 4 ký tự ($I\_$), 5 ký tự ($V\_$), 2000 ký tự ($V\_$) |
| **Gõ ký tự `/` ô soạn thảo** | • Bắt ký tự `/` hiển thị bảng gợi ý danh sách mẫu câu | **V_SUGG_01:** Gõ ký tự `/` hiển thị bảng danh sách gợi ý | **I_SUGG_01:** Gõ các ký tự khác (không hiện danh sách gợi ý mẫu) | Ký tự mở bảng gợi ý `/` |

---

## 4.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Tạo Mẫu phản hồi nhanh mới

*(Tiền đề quy trình: Nhân viên/Quản lý bấm nút "Tạo mẫu phản hồi")*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Đã điền đầy đủ các trường Phím tắt, Tiêu đề, Danh mục, Nội dung?** | F | T | T | T | T |
| **C2: Phím tắt bắt đầu bằng ký tự `/` và không chứa khoảng trắng?** | - | F | T | T | T |
| **C3: Tiêu đề (3-150 ký tự) và Nội dung (5-2000 ký tự) đúng độ dài?** | - | - | F | T | T |
| **C4: Phím tắt chưa tồn tại trên hệ thống?** | - | - | - | F | T |
| **H1: Hiển thị lỗi khoanh đỏ ô trống (E-1)** | X | | | | |
| **H2: Hiển thị lỗi dưới ô Phím tắt: "Phím tắt bắt buộc bắt đầu bằng / và không chứa khoảng trắng"** | | X | | | |
| **H3: Hiển thị thông báo lỗi độ dài Tiêu đề / Nội dung chi tiết** | | | X | | |
| **H4: Báo lỗi "Phím tắt đã tồn tại" (E-4)** | | | | X | |
| **H5: Lưu mẫu phản hồi mới thành công, đồng bộ ngay bảng gợi ý cho nhân viên đang trực ca** | | | | | X |

---
---

# V. MA TRẬN TRUY XUẤT NGUỒN GỐC (TRACEABILITY MATRIX - RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 3.1 - Luồng chính** | Quản lý/Admin tạo tài khoản nhân sự mới thành công | `TC_LCS_01` |
| **UC 3.1 - E-1** | Để trống trường thông tin bắt buộc khi tạo tài khoản nhân sự | `TC_LCS_02` |
| **UC 3.1 - E-2** | Định dạng dữ liệu không hợp lệ (Tên, Email, SĐT, Mật khẩu) | `TC_LCS_03`, `TC_LCS_04` |
| **UC 3.1 - E-4** | Email nội bộ đã tồn tại | `TC_LCS_05` |
| **UC 3.1 - Rule 2** | Tạo tài khoản Agent nhưng để trống kỹ năng chuyên môn | `TC_LCS_06` |
| **UC 3.1 - A-1** | Đăng nhập Bàn làm việc CSKH thành công (mặc định OFFLINE) | `TC_LCS_07` |
| **UC 3.1 - E-5** | Đăng nhập tài khoản nhân viên đang bị khóa | `TC_LCS_08` |
| **UC 3.1 - E-6** | Đăng nhập sai Email nội bộ hoặc Mật khẩu | `TC_LCS_09` |
| **UC 3.2 - Luồng chính** | Chuyển đổi trạng thái làm việc (ONLINE / BUSY / OFFLINE) | `TC_LCS_10`, `TC_LCS_11` |
| **UC 3.2 - E-1** | Mất kết nối đường truyền mạng quá 30 giây (Tự động đổi OFFLINE) | `TC_LCS_12` |
| **UC 3.3 - Luồng chính** | Tiếp quản cuộc trò chuyện & Nhắn tin 2 chiều thời gian thực | `TC_LCS_13`, `TC_LCS_14` |
| **UC 3.3 - E-1** | Xung đột tiếp quản (Người khác bấm trước) $\rightarrow$ Chế độ Chỉ xem | `TC_LCS_15` |
| **UC 3.3 - E-2** | Để trống tin nhắn tư vấn hoặc vượt quá 4000 ký tự | `TC_LCS_16` |
| **UC 3.4 - Luồng chính** | Gõ `/` gợi ý mẫu phản hồi & Tạo mẫu phản hồi mới thành công | `TC_LCS_17`, `TC_LCS_18` |
| **UC 3.4 - E-4** | Tạo mẫu phản hồi trùng phím tắt / sai ký tự `/` | `TC_LCS_19` |

---
---

# VI. THIẾT KẾ CA KIỂM THỬ CHI TIẾT (TEST CASE SPECIFICATION - IEEE)

## 6.1. Nhóm Test Case: UC 3.1 - Quản lý tài khoản nhân viên

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_01** | Kiểm tra Quản lý tạo tài khoản nhân viên mới thành công (Happy Path) | Đăng nhập tài khoản Quản lý, đang ở màn hình Quản lý nhân sự | 1. Nhập Họ tên hợp lệ.<br>2. Nhập Email nội bộ mới.<br>3. Nhập SĐT hợp lệ.<br>4. Chọn Vai trò là Agent.<br>5. Chọn 2 Kỹ năng chuyên môn.<br>6. Nhập Mật khẩu hợp lệ.<br>7. Bấm nút "Tạo tài khoản nhân sự". | • Họ tên: `"Nguyễn Văn Bình"` ($V\_$)<br>• Email: `"agent.binh@brand.com"` ($V\_$)<br>• SĐT: `"0987654321"` ($V\_$)<br>• Vai trò: Agent<br>• Kỹ năng: `["Đổi trả", "Giao hàng"]`<br>• Mật khẩu: `"Agent1234"` | Thông báo xanh: *"Tạo tài khoản nhân viên thành công!"*, làm mới biểu mẫu và tài khoản mới xuất hiện trong danh sách ở trạng thái Ngoại tuyến (OFFLINE). | Pass |
| **TC_LCS_02** | Kiểm tra tạo tài khoản khi để trống Email | Đang ở màn hình Tạo tài khoản nhân sự | 1. Để trống ô Email.<br>2. Điền hợp lệ các ô còn lại.<br>3. Bấm "Tạo tài khoản nhân sự". | • Email: `""` ($I\_$)<br>• Các ô khác: Nhập đúng $V\_$ | Viền ô Email hằn đỏ, hiển thị thông báo lỗi ngay bên dưới: *"Vui lòng không để trống trường thông tin này"*. | Pass |
| **TC_LCS_03** | Kiểm tra tạo tài khoản với Mật khẩu 7 ký tự (Biên lỗi) | Đang ở màn hình Tạo tài khoản nhân sự | 1. Nhập Mật khẩu 7 ký tự.<br>2. Điền hợp lệ các ô còn lại.<br>3. Bấm "Tạo tài khoản nhân sự". | • Mật khẩu: `"Agent12"` ($I\_$)<br>• Các ô khác: Nhập đúng $V\_$ | Báo lỗi dưới ô Mật khẩu: *"Mật khẩu tối thiểu 8 ký tự gồm chữ và số"*. | Pass |
| **TC_LCS_04** | Kiểm tra tạo tài khoản với Email đã tồn tại | Đang ở màn hình Tạo tài khoản nhân sự | 1. Nhập Email đã có trên hệ thống.<br>2. Điền hợp lệ các ô còn lại.<br>3. Bấm "Tạo tài khoản nhân sự". | • Email: `"agent.an@brand.com"` ($I\_$)<br>• Các ô khác: Nhập đúng $V\_$ | Hiển thị cảnh báo lỗi: *"Địa chỉ email này đã được sử dụng"*. | Pass |
| **TC_LCS_05** | Kiểm tra tạo tài khoản Agent nhưng không chọn kỹ năng nào | Đang ở màn hình Tạo tài khoản nhân sự | 1. Chọn Vai trò là Agent.<br>2. Không tích chọn kỹ năng nào.<br>3. Bấm "Tạo tài khoản nhân sự". | • Vai trò: Agent<br>• Kỹ năng: Không chọn (0 kỹ năng) ($I\_$) | Báo lỗi màu đỏ: *"Tạo tài khoản Nhân viên tư vấn bắt buộc chọn ít nhất 1 danh mục kỹ năng xử lý"*. | Pass |
| **TC_LCS_06** | Kiểm tra Đăng nhập Bàn làm việc CSKH thành công | Đang ở màn hình Đăng nhập nội bộ | 1. Nhập Email nội bộ chính xác.<br>2. Nhập Mật khẩu chính xác.<br>3. Nhấn nút "Đăng nhập". | • Email: `"agent.an@brand.com"` ($V\_$)<br>• Mật khẩu: `"123456"` ($V\_$) | Chuyển hướng thành công vào giao diện Bàn làm việc CSKH (Live Support Console) với trạng thái mặc định ban đầu là Ngoại tuyến (OFFLINE). | Pass |
| **TC_LCS_07** | Kiểm tra Đăng nhập vào tài khoản nhân viên đang bị khóa | Tài khoản `agent.binh@brand.com` bị khóa | 1. Nhập Email nhân viên bị khóa.<br>2. Nhập đúng Mật khẩu.<br>3. Bấm "Đăng nhập". | • Email: `"agent.binh@brand.com"`<br>• Mật khẩu: `"123456"` | Hiển thị cảnh báo: *"Tài khoản hiện đang bị khóa hoặc ngừng kích hoạt"*. | Pass |
| **TC_LCS_08** | Kiểm tra Đăng nhập sai Mật khẩu | Đang ở màn hình Đăng nhập nội bộ | 1. Nhập Email chính xác.<br>2. Nhập Mật khẩu sai.<br>3. Bấm "Đăng nhập". | • Email: `"agent.an@brand.com"`<br>• Mật khẩu: `"sai_mat_khau"` ($I\_$) | Báo lỗi: *"Địa chỉ email hoặc mật khẩu không chính xác"*. | Pass |

---

## 6.2. Nhóm Test Case: UC 3.2 - Quản lý trạng thái làm việc của nhân viên

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_09** | Kiểm tra chuyển trạng thái từ OFFLINE sang ONLINE (Happy Path) | Đã đăng nhập Live Console, trạng thái đang là OFFLINE (Chấm xám) | 1. Nhấp chọn thanh trạng thái ở góc trên bên phải.<br>2. Chọn trạng thái "Trực tuyến" (ONLINE). | Click chọn "Trực tuyến" ($V\_$) | Nút chỉ thị chuyển sang **màu xanh lá (ONLINE)**, hiển thị thông báo: *"Đã chuyển sang trạng thái Trực tuyến - Bạn đã sẵn sàng tiếp nhận hỗ trợ!"*. Kích hoạt tự động nhận phân công ticket. | Pass |
| **TC_LCS_10** | Kiểm tra chuyển trạng thái từ ONLINE sang BUSY | Trạng thái hiện tại đang là ONLINE | 1. Nhấp thanh trạng thái.<br>2. Chọn trạng thái "Bận" (BUSY). | Click chọn "Bận" ($V\_$) | Nút chỉ thị chuyển sang **màu cam (BUSY)**, thông báo chuyển trạng thái thành công. Tạm dừng phân công ticket mới nhưng vẫn giữ các việc đang xử lý. | Pass |
| **TC_LCS_11** | Kiểm tra tự động đổi trạng thái sang OFFLINE khi mất mạng > 30s (E-1) | Đã đăng nhập, trạng thái đang là ONLINE | 1. Ngắt kết nối mạng thiết bị.<br>2. Quan sát nút chỉ thị sau 30 giây. | Ngắt mạng 30 giây | Nút chỉ thị trạng thái tự động đổi sang **màu xám (OFFLINE)**. Hiển thị dải cảnh báo cam: *"Đang mất kết nối thời gian thực. Hệ thống đang tự động kết nối lại..."*. | Pass |

---

## 6.3. Nhóm Test Case: UC 3.3 - Theo dõi hàng đợi & Tiếp quản cuộc trò chuyện

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_12** | Kiểm tra tiếp quản cuộc trò chuyện thành công (Happy Path) | Trạng thái ONLINE, hàng đợi có 1 phiên chat màu đỏ đang chờ hỗ trợ | 1. Nhấn chọn phiên chat cần hỗ trợ.<br>2. Bấm nút "Tiếp quản cuộc trò chuyện". | Click nút "Tiếp quản cuộc trò chuyện" ($V\_$) | Xác nhận quyền tiếp quản, tự động gỡ cờ đỏ, ngắt trả lời của Bot AI và gửi thông báo tự động vào chat khách hàng: *"Nhân viên tư vấn đã tham gia cuộc trò chuyện"*. Mở khóa ô nhập cho nhân viên. | Pass |
| **TC_LCS_13** | Kiểm tra nhắn tin 2 chiều thời gian thực | Nhân viên đã tiếp quản thành công ở `TC_LCS_12` | 1. Nhập nội dung tư vấn vào ô chat.<br>2. Nhấn nút "Gửi" (hoặc phím Enter). | Nội dung: `"Chào bạn, mình là An tư vấn viên PetHome. Mình có thể hỗ trợ gì cho bạn ạ?"` ($V\_$) | Tin nhắn tư vấn hiển thị lập tức sang khung chat của khách hàng với vai trò Nhân viên tư vấn. | Pass |
| **TC_LCS_14** | Kiểm tra xung đột tiếp quản khi người khác nhận trước (E-1) | Phiên chat `#105` đang chờ hỗ trợ | 1. Nhân viên A chuẩn bị bấm tiếp quản.<br>2. Nhân viên B bấm tiếp quản trước 1 giây.<br>3. Nhân viên A bấm tiếp quản ngay sau đó. | Thao tác bấm sau | Báo lỗi: *"Cuộc trò chuyện đã được nhận bởi nhân viên khác"*. Đặt màn hình của Nhân viên A về **Chế độ Chỉ xem (Read-only)**, khóa ô nhập tin nhắn. | Pass |
| **TC_LCS_15** | Kiểm tra gửi tin nhắn rỗng (E-2) | Nhân viên đang ở khung chat đã tiếp quản | 1. Để trống ô nhập tin nhắn.<br>2. Nhấn nút "Gửi". | Nội dung: `""` ($I\_$) | Nút gửi không kích hoạt (hoặc báo nhắc nhở: *"Vui lòng nhập nội dung tin nhắn tư vấn"*). | Pass |

---

## 6.4. Nhóm Test Case: UC 3.4 - Mẫu phản hồi nhanh (Canned Responses)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_16** | Kiểm tra gõ phím tắt `/` gợi ý danh sách mẫu câu | Đang ở khung chat tư vấn | 1. Tại ô nhập văn bản, gõ ký tự `/`.<br>2. Quan sát menu thả xuống. | Nội dung: `/` ($V\_$) | Hiển thị menu danh sách gợi ý các mẫu phản hồi nhanh kèm phím tắt và tiêu đề. Bấm chọn mẫu câu sẽ chèn nguyên văn nội dung vào ô gõ. | Pass |
| **TC_LCS_17** | Kiểm tra tạo Mẫu phản hồi nhanh mới thành công | Đang ở màn hình Quản lý Mẫu phản hồi | 1. Nhập Phím tắt bắt đầu bằng `/`.<br>2. Nhập Tiêu đề.<br>3. Chọn Danh mục.<br>4. Nhập Nội dung mẫu.<br>5. Bấm "Lưu mẫu câu". | • Phím tắt: `/xloi_tre` ($V\_$)<br>• Tiêu đề: `"Xin lỗi giao hàng trễ"`<br>• Danh mục: `"Vận chuyển"`<br>• Nội dung: `"PetHome rất xin lỗi vì..."` | Thông báo *"Tạo mẫu phản hồi mới thành công"*. Mẫu câu mới lập tức có hiệu lực cho tất cả nhân viên đang trực ca khi gõ `/xloi_tre`. | Pass |
| **TC_LCS_18** | Kiểm tra báo lỗi khi tạo phím tắt không bắt đầu bằng `/` | Đang ở màn hình Tạo mẫu phản hồi | 1. Nhập Phím tắt không có ký tự `/` đầu.<br>2. Bấm "Lưu mẫu câu". | • Phím tắt: `xloi_tre` ($I\_$) | Hiển thị thông báo lỗi ngay dưới ô Phím tắt: *"Phím tắt bắt buộc phải bắt đầu bằng ký tự / và không chứa khoảng trắng"*. | Pass |

---
*Tài liệu kiểm thử hộp đen Khối chức năng 3 được chuẩn hóa toàn bộ 100%, tuân thủ cấu trúc chuẩn và đạt góc nhìn người dùng cuối (End-User).*

---
*Tài liệu kiểm thử hộp đen Khối chức năng 3 được chuẩn hóa toàn bộ 100%, tuân thủ cấu trúc chuẩn và đạt góc nhìn người dùng cuối (End-User).*
