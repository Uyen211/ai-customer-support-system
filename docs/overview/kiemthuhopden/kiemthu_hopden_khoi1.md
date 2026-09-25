# THIẾT KẾ KIỂM THỬ HỘP ĐEN - KHỐI CHỨC NĂNG 1: TRỢ LÝ TƯ VẤN KHÁCH HÀNG TỰ ĐỘNG

> **Đối tượng kiểm thử:** Khối chức năng Trợ lý tư vấn khách hàng tự động (PetHome Customer Assistant).  
> **Tài liệu tham chiếu đặc tả:** `docs/overview/usecase.md` (Use Cases 1.1, 1.2, 1.3, 1.4).  
> **Nguyên tắc hành văn kiểm thử hộp đen:** Mô tả hoàn toàn từ góc nhìn người dùng cuối (End-User) trên giao diện website/khung chat. Không đề cập tới thuật toán nội bộ, cấu trúc bảng CSDL, tên bảng SQL, cơ chế socket hay thuật toán vector nhúng. Các trạng thái kỹ thuật được diễn giải dưới dạng thuật ngữ Tiếng Việt kèm chú thích Tiếng Anh theo đúng giao diện người dùng (VD: *Đang mở (Open)*, *Đã kết thúc (Closed)*, *Chờ tư vấn viên tiếp quản (Waiting for Agent)*, *Chế độ Trợ lý ảo (Bot mode)*).

---

# I. USE CASE 1.1: QUẢN LÝ TÀI KHOẢN KHÁCH HÀNG (ĐĂNG KÝ & ĐĂNG NHẬP)

## 1.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích theo từng trường dữ liệu

| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Họ và tên** *(Đăng ký)* | • Bắt buộc<br>• Độ dài 2 - 50 ký tự<br>• Chỉ chứa chữ cái tiếng Việt/Anh và khoảng trắng | **V_NAME_01:** Chuỗi chữ hợp lệ có độ dài từ 2 - 50 ký tự (VD: `"Nguyễn Văn A"`) | **I_NAME_01:** Để trống<br>**I_NAME_02:** Chuỗi ngắn hơn 2 ký tự (VD: `"A"`)<br>**I_NAME_03:** Chuỗi dài hơn 50 ký tự<br>**I_NAME_04:** Chứa số hoặc ký tự đặc biệt (VD: `"Nam123"`, `"An@%"`) | • Biên dưới: 1 ký tự ($I\_$), 2 ký tự ($V\_$), 3 ký tự ($V\_$)<br>• Biên trên: 49 ký tự ($V\_$), 50 ký tự ($V\_$), 51 ký tự ($I\_$) |
| **Địa chỉ Email** *(Đăng ký/Đăng nhập)* | • Bắt buộc<br>• Đúng định dạng email tiêu chuẩn (`ten@domain.com`)<br>• Tối đa 255 ký tự<br>• Duy nhất trên hệ thống | **V_EMAIL_01:** Đúng định dạng email, chưa tồn tại, độ dài $\le 255$ ký tự (VD: `"user@gmail.com"`) | **I_EMAIL_01:** Để trống<br>**I_EMAIL_02:** Sai định dạng (VD: `"user@"` , `"user.com"`, `"user@domain"`)<br>**I_EMAIL_03:** Email vượt quá 255 ký tự<br>**I_EMAIL_04:** Email đã tồn tại trên hệ thống | • Biên trên độ dài: 255 ký tự ($V\_$), 256 ký tự ($I\_$) |
| **Số điện thoại** *(Đăng ký)* | • Tùy chọn (Không bắt buộc)<br>• Nếu nhập: Bắt buộc đủ 10 chữ số và bắt đầu bằng số `0` | **V_PHONE_01:** Để trống không nhập<br>**V_PHONE_02:** Đủ 10 chữ số, bắt đầu bằng số `0` (VD: `"0912345678"`) | **I_PHONE_01:** Ít hơn 10 chữ số (VD: `"091234567"`)<br>**I_PHONE_02:** Nhiều hơn 10 chữ số (VD: `"09123456789"`)<br>**I_PHONE_03:** Đủ 10 chữ số nhưng không bắt đầu bằng số `0` (VD: `"1912345678"`)<br>**I_PHONE_04:** Chứa chữ cái hoặc ký tự đặc biệt (VD: `"0912abc345"`) | • Biên độ dài: 9 chữ số ($I\_$), 10 chữ số bắt đầu bằng `0` ($V\_$), 11 chữ số ($I\_$) |
| **Mật khẩu** *(Đăng ký/Đăng nhập)* | • Bắt buộc<br>• Độ dài từ 8 ký tự trở lên<br>• Chứa ít nhất 1 chữ cái và 1 chữ số | **V_PASS_01:** Mật khẩu $\ge 8$ ký tự, chứa cả chữ và số (VD: `"Abc12345"`) | **I_PASS_01:** Để trống<br>**I_PASS_02:** Ít hơn 8 ký tự (VD: `"Abc1234"`)<br>**I_PASS_03:** Chỉ chứa toàn chữ cái, không có số (VD: `"Abcdefgh"`)<br>**I_PASS_04:** Chỉ chứa toàn chữ số, không có chữ (VD: `"12345678"`) | • Biên độ dài: 7 ký tự ($I\_$), 8 ký tự ($V\_$), 9 ký tự ($V\_$) |
| **Xác nhận mật khẩu** *(Đăng ký)* | • Bắt buộc<br>• Phải khớp hoàn toàn từng ký tự với ô Mật khẩu | **V_CONFIRM_01:** Chuỗi trùng khớp hoàn toàn với ô Mật khẩu | **I_CONFIRM_01:** Để trống<br>**I_CONFIRM_02:** Không trùng khớp với ô Mật khẩu (VD: gõ sai 1 ký tự) | Không áp dụng biên (so khớp chuỗi) |

---

## 1.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Đăng ký tài khoản mới

*(Tiền đề quy trình: Người dùng nhấn nút "Tạo tài khoản")*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Đã điền đầy đủ các trường thông tin bắt buộc?** | F | T | T | T | T |
| **C2: Tất cả dữ liệu nhập vào đúng định dạng?** | - | F | T | T | T |
| **C3: Mật khẩu xác nhận trùng khớp với mật khẩu gốc?** | - | - | F | T | T |
| **C4: Địa chỉ Email chưa tồn tại trên hệ thống?** | - | - | - | F | T |
| **H1: Hiển thị lỗi khoanh đỏ ô trống (E-1)** | X | | | | |
| **H2: Hiển thị thông báo lỗi định dạng chi tiết (E-2)** | | X | | | |
| **H3: Báo lỗi "Mật khẩu xác nhận không trùng khớp" (E-3)** | | | X | | |
| **H4: Báo lỗi "Địa chỉ email này đã được sử dụng" (E-4)** | | | | X | |
| **H5: Đăng ký thành công, thông báo xanh & chuyển về Trang chủ** | | | | | X |

### Bảng quyết định Luồng Đăng nhập tài khoản

*(Tiền đề quy trình: Người dùng nhấn nút "Đăng nhập")*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Đã điền đầy đủ Email và Mật khẩu?** | F | T | T | T | T |
| **C2: Địa chỉ Email có tồn tại trên hệ thống?** | - | F | T | T | T |
| **C3: Tài khoản ở trạng thái hoạt động (không bị khóa tạm thời)?** | - | - | F | T | T |
| **C4: Mật khẩu nhập vào chính xác?** | - | - | - | F | T |
| **H1: Báo lỗi để trống trường thông tin (E-1)** | X | | | | |
| **H2: Báo lỗi "Thông tin tài khoản hoặc mật khẩu không chính xác" (E-5)** | | X | | | |
| **H3: Báo lỗi "Tài khoản hiện đang bị tạm khóa..." (E-6)** | | | X | | |
| **H4: Báo lỗi "Thông tin tài khoản hoặc mật khẩu không chính xác" & tăng đếm sai (E-7)** | | | | X | |
| **H5: Đăng nhập thành công, mở cửa sổ chat & tải lịch sử tin nhắn cũ** | | | | | X |

---

## 1.4. Ma trận truy xuất nguồn gốc (Traceability Matrix - RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 1.1 - Luồng chính** | Đăng ký tài khoản mới thành công | `TC_REG_01` |
| **UC 1.1 - E-1** | Để trống trường thông tin bắt buộc | `TC_REG_02`, `TC_LOG_02` |
| **UC 1.1 - E-2** | Định dạng dữ liệu không hợp lệ (Tên, Email, SĐT, Mật khẩu) | `TC_REG_03`, `TC_REG_04`, `TC_REG_05`, `TC_REG_06` |
| **UC 1.1 - E-3** | Xác nhận mật khẩu không khớp | `TC_REG_07` |
| **UC 1.1 - E-4** | Email đã được đăng ký trước đó | `TC_REG_08` |
| **UC 1.1 - A-1** | Đăng nhập tài khoản thành công | `TC_LOG_01` |
| **UC 1.1 - E-5** | Email đăng nhập không tồn tại | `TC_LOG_03` |
| **UC 1.1 - E-6** | Tài khoản đang bị khóa tạm thời | `TC_LOG_04` |
| **UC 1.1 - E-7** | Nhập sai mật khẩu (dưới 5 lần & chạm mốc 5 lần) | `TC_LOG_05`, `TC_LOG_06` |

---

## 1.5. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_REG_01** | Kiểm tra đăng ký tài khoản mới thành công (Happy Path) | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Họ và tên hợp lệ.<br>2. Nhập Email chưa đăng ký.<br>3. Nhập Số điện thoại hợp lệ.<br>4. Nhập Mật khẩu hợp lệ.<br>5. Nhập Xác nhận mật khẩu trùng khớp.<br>6. Nhấn nút "Tạo tài khoản". | • Họ tên: `"Trần Văn An"` ($V\_$)<br>• Email: `"an.tran@gmail.com"` ($V\_$)<br>• SĐT: `"0912345678"` ($V\_$)<br>• Mật khẩu: `"An123456"` ($V\_$)<br>• Xác nhận: `"An123456"` ($V\_$) | Hiển thị thông báo xanh: *"Chúc mừng bạn đã tạo tài khoản thành công! Chào mừng bạn đến với PetHome."*, tự động đăng nhập và chuyển hướng về Trang chủ. | |
| **TC_REG_02** | Kiểm tra đăng ký khi để trống Họ và tên | Đang ở màn hình Đăng ký tài khoản | 1. Để trống ô Họ và tên.<br>2. Điền hợp lệ tất cả các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • Họ tên: `""` ($I\_$)<br>• Các trường khác: Nhập đúng giá trị $V\_$ như `TC_REG_01` | Viền ô "Họ và tên" hằn đỏ, hiển thị thông báo lỗi ngay bên dưới: *"Vui lòng không để trống trường thông tin này"*. Con trỏ nhấp nháy tại ô Họ tên. | |
| **TC_REG_03** | Kiểm tra đăng ký với Họ và tên chứa chữ số | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Họ tên chứa chữ số.<br>2. Điền hợp lệ các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • Họ tên: `"Trần Văn 123"` ($I\_$)<br>• Trường khác: Nhập đúng $V\_$ | Hiển thị thông báo lỗi dưới ô Họ và tên: *"Họ và tên chỉ bao gồm chữ cái tiếng Việt hoặc tiếng Anh và khoảng trắng"*. | |
| **TC_REG_04** | Kiểm tra đăng ký với Email sai định dạng | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Email sai cấu trúc tiêu chuẩn.<br>2. Điền hợp lệ các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • Email: `"an.trangmail.com"` ($I\_$)<br>• Trường khác: Nhập đúng $V\_$ | Hiển thị thông báo lỗi dưới ô Email: *"Địa chỉ email không đúng định dạng"*. | |
| **TC_REG_05** | Kiểm tra đăng ký với Số điện thoại 9 chữ số (Biển lỗi) | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Số điện thoại chỉ có 9 chữ số.<br>2. Điền hợp lệ các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • SĐT: `"091234567"` ($I\_$)<br>• Trường khác: Nhập đúng $V\_$ | Hiển thị thông báo lỗi dưới ô SĐT: *"Số điện thoại phải gồm 10 chữ số bắt đầu bằng số 0"*. | |
| **TC_REG_06** | Kiểm tra đăng ký với Mật khẩu 7 ký tự (Biên lỗi) | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Mật khẩu 7 ký tự.<br>2. Nhập Xác nhận mật khẩu 7 ký tự khớp với Mật khẩu.<br>3. Điền hợp lệ các ô còn lại.<br>4. Nhấn nút "Tạo tài khoản". | • Mật khẩu: `"An12345"` ($I\_$)<br>• Xác nhận: `"An12345"`<br>• Trường khác: Nhập đúng $V\_$ | Hiển thị thông báo lỗi dưới ô Mật khẩu: *"Mật khẩu tối thiểu 8 ký tự gồm chữ và số"*. | |
| **TC_REG_07** | Kiểm tra đăng ký khi Mật khẩu xác nhận không trùng khớp | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Mật khẩu hợp lệ.<br>2. Nhập Xác nhận mật khẩu khác ký tự.<br>3. Nhấn nút "Tạo tài khoản". | • Mật khẩu: `"An123456"` ($V\_$)<br>• Xác nhận: `"An123457"` ($I\_$)<br>• Trường khác: Nhập đúng $V\_$ | Hiển thị thông báo lỗi dưới ô Xác nhận mật khẩu: *"Mật khẩu xác nhận không trùng khớp"*. Ô xác nhận mật khẩu được xóa sạch để gõ lại. | |
| **TC_REG_08** | Kiểm tra đăng ký với Email đã tồn tại trên hệ thống | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Email đã từng đăng ký thành công.<br>2. Điền hợp lệ các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • Email: `"khachhang1@gmail.com"` ($I\_$)<br>• Trường khác: Nhập đúng $V\_$ | Hiển thị thông báo: *"Địa chỉ email này đã được sử dụng. Vui lòng chọn Đăng nhập"* kèm nút gợi ý *"Chuyển sang Đăng nhập"*. | |
| **TC_LOG_01** | Kiểm tra đăng nhập thành công (Happy Path) | Đang ở màn hình Đăng nhập | 1. Nhập Email chính xác.<br>2. Nhập Mật khẩu chính xác.<br>3. Nhấn nút "Đăng nhập". | • Email: `"khachhang1@gmail.com"` ($V\_$)<br>• Mật khẩu: `"123456"` ($V\_$) | Thông báo *"Đăng nhập thành công"*, chuyển hướng về màn hình chính và tải sẵn khung hội thoại cùng lịch sử tin nhắn trao đổi trước đó. | |
| **TC_LOG_02** | Kiểm tra đăng nhập khi để trống Mật khẩu | Đang ở màn hình Đăng nhập | 1. Nhập Email hợp lệ.<br>2. Để trống ô Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | • Email: `"khachhang1@gmail.com"` ($V\_$)<br>• Mật khẩu: `""` ($I\_$) | Báo lỗi viền đỏ ô Mật khẩu: *"Vui lòng không để trống trường thông tin này"*. | |
| **TC_LOG_03** | Kiểm tra đăng nhập với Email không tồn tại | Đang ở màn hình Đăng nhập | 1. Nhập Email chưa từng đăng ký.<br>2. Nhập Mật khẩu ngẫu nhiên.<br>3. Nhấn nút "Đăng nhập". | • Email: `"nodata_user@gmail.com"` ($I\_$)<br>• Mật khẩu: `"12345678"` | Hiển thị cảnh báo lỗi: *"Thông tin tài khoản hoặc mật khẩu không chính xác"*. | |
| **TC_LOG_04** | Kiểm tra đăng nhập vào tài khoản đang bị khóa tạm thời | Tài khoản `khachhang2@gmail.com` vừa bị khóa 15 phút do nhập sai 5 lần | 1. Nhập Email bị khóa.<br>2. Nhập đúng Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | • Email: `"khachhang2@gmail.com"`<br>• Mật khẩu: `"123456"` | Hiển thị thông báo: *"Tài khoản hiện đang bị tạm khóa. Vui lòng quay lại sau hoặc liên hệ bộ phận hỗ trợ"*. | |
| **TC_LOG_05** | Kiểm tra đếm số lần nhập sai mật khẩu (Lần 1 đến lần 4) | Tài khoản `khachhang1@gmail.com` đang hoạt động bình thường | 1. Nhập Email chính xác.<br>2. Nhập Mật khẩu sai.<br>3. Nhấn nút "Đăng nhập". | • Email: `"khachhang1@gmail.com"`<br>• Mật khẩu: `"sai_mat_khau"` ($I\_$) | Báo lỗi: *"Thông tin tài khoản hoặc mật khẩu không chính xác"*. Bộ đếm đếm sai tăng thêm 1 lượt. | |
| **TC_LOG_06** | Kiểm tra tự động khóa tài khoản khi nhập sai mật khẩu 5 lần liên tiếp | Tài khoản `khachhang1@gmail.com` đã nhập sai 4 lần trước đó | 1. Nhập Email chính xác.<br>2. Nhập Mật khẩu sai lần thứ 5.<br>3. Nhấn "Đăng nhập". | • Email: `"khachhang1@gmail.com"`<br>• Mật khẩu: `"sai_mat_khau_5"` ($I\_$) | Hiển thị thông báo: *"Tài khoản hiện đang bị tạm khóa. Vui lòng quay lại sau hoặc liên hệ bộ phận hỗ trợ"*. Tài khoản chuyển sang trạng thái bị khóa 15 phút. | |

---
---

# II. USE CASE 1.2: QUẢN LÝ PHIÊN TRÒ CHUYỆN

## 2.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

*Khối chức năng Quản lý phiên trò chuyện không có các trường nhập liệu dạng biểu mẫu văn bản phức tạp, mà tập trung vào các hành động tương tác chọn lựa (Click) và kiểm tra dữ liệu hiển thị lịch sử.*

### Bảng phân tích hành động tương tác & hiển thị

| Trường dữ liệu / Tương tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Danh sách cuộc trò chuyện cũ** | • Hiển thị phiên trò chuyện thuộc sở hữu của khách hàng<br>• Hiển thị thời gian tin nhắn gần nhất & dòng tóm lược (10-15 từ) | **V_CONV_01:** Danh sách có từ 1 phiên trò chuyện trở lên | **I_CONV_01:** Khách hàng mới chưa từng có phiên trò chuyện nào (Danh sách trống) | Phân vùng danh sách: 0 phiên ($I\_$), 1 phiên ($V\_$) |
| **Trạng thái phiên trò chuyện** | • Nhãn trạng thái hiển thị rõ ràng trên từng phiên | **V_STATUS_01:** Trạng thái Đang mở - Chế độ Trợ lý ảo (Bot mode)<br>**V_STATUS_02:** Trạng thái Đang mở - Chế độ Chờ tư vấn viên tiếp quản (Waiting for Agent)<br>**V_STATUS_03:** Trạng thái Đang mở - Chế độ Tư vấn viên đang hỗ trợ (Human Agent mode) | **I_STATUS_01:** Trạng thái Đã kết thúc (Closed) | Không áp dụng biên (Xác định theo tập nhãn trạng thái) |
| **Tải lịch sử tin nhắn** | • Tải phân đoạn (Lazy Loading)<br>• Tải trước 50 tin nhắn gần nhất | **V_MSG_01:** Số tin nhắn trong phiên $\le 50$ tin<br>**V_MSG_02:** Số tin nhắn trong phiên $> 50$ tin (Tải 50 tin mới nhất, cuộn lên tải thêm) | **I_MSG_01:** Lỗi kết nối đường truyền không tải được tin nhắn | Biên số lượng tin nhắn: 50 tin nhắn (vừa đủ 1 lượt tải phân đoạn), 51 tin nhắn (kích hoạt phân trang cuộn) |

---

## 2.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Tiếp tục cuộc trò chuyện cũ

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: Khách hàng chọn 1 cuộc trò chuyện trong Lịch sử?** | T | T | T | T |
| **C2: Đường truyền mạng ổn định?** | F | T | T | T |
| **C3: Phiên trò chuyện ở trạng thái "Đã kết thúc" (Closed)?** | - | T | F | F |
| **C4: Phiên ở trạng thái "Chờ tư vấn viên tiếp quản" (Waiting for Agent)?** | - | - | T | F |
| **H1: Báo lỗi "Không thể tải nội dung do đường truyền..." & Nút Thử lại (E-4)** | X | | | |
| **H2: Tải tin nhắn cũ, khóa ô nhập & Báo dải thông báo xám phiên đã đóng (E-1)** | | X | | |
| **H3: Tải tin nhắn cũ, mở ô nhập & Báo dải thông báo cam chờ nhân viên (E-2)** | | | X | |
| **H4: Tải nội dung trọn vẹn, mở ô nhập & sẵn sàng trò chuyện với Trợ lý ảo** | | | | X |

---

## 2.3. Sơ đồ chuyển trạng thái (State Transition)

### Trạng thái của một Phiên trò chuyện CSKH

| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- |
| **Khởi tạo mới (New)** | Khách hàng bấm nút "Bắt đầu cuộc trò chuyện mới" | **Đang mở - Trợ lý ảo (Bot mode)** |
| **Đang mở - Trợ lý ảo (Bot mode)** | Khách hàng gửi câu hỏi và nhận trả lời tự động từ AI | **Đang mở - Trợ lý ảo (Bot mode)** |
| **Đang mở - Trợ lý ảo (Bot mode)** | Khách hàng yêu cầu gặp tư vấn viên HOẶC Cảnh báo khiếu nại khẩn cấp | **Chờ tư vấn viên tiếp quản (Waiting for Agent)** |
| **Chờ tư vấn viên tiếp quản (Waiting for Agent)** | Tư vấn viên CSKH nhấn "Tiếp quản cuộc trò chuyện" | **Tư vấn viên đang hỗ trợ (Human Agent mode)** |
| **Tư vấn viên đang hỗ trợ (Human Agent mode)** | Tư vấn viên hoặc Khách hàng bấm "Kết thúc hỗ trợ" | **Đã kết thúc (Closed)** |
| **Đang mở - Trợ lý ảo (Bot mode)** | Không có tương tác mới sau 24 giờ kể từ tin nhắn cuối | **Đã kết thúc (Closed)** |
| **Đã kết thúc (Closed)** | Khách hàng chọn "Bắt đầu cuộc trò chuyện mới" | **Đang mở - Trợ lý ảo (Bot mode)** *(Tạo phiên mới riêng biệt)* |

---

## 2.4. Ma trận truy xuất nguồn gốc (Traceability Matrix - RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 1.2 - Luồng chính** | Xem danh sách và tiếp tục cuộc trò chuyện cũ (Bot mode) | `TC_CONV_01` |
| **UC 1.2 - A-1** | Mở phiên trò chuyện mới độc lập | `TC_CONV_02` |
| **UC 1.2 - E-1** | Tiếp tục phiên trò chuyện đã kết thúc (Closed) | `TC_CONV_03` |
| **UC 1.2 - E-2** | Chọn phiên trò chuyện đang chờ tư vấn viên tiếp quản | `TC_CONV_04` |
| **UC 1.2 - E-3** | Khách hàng mới chưa có lịch sử trò chuyện | `TC_CONV_05` |
| **UC 1.2 - E-4** | Mất kết nối đường truyền khi nạp lịch sử | `TC_CONV_06` |
| **UC 1.2 - Rule 2** | Kiểm tra tải phân đoạn 50 tin nhắn gần nhất | `TC_CONV_07` |

---

## 2.5. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_CONV_01** | Kiểm tra tiếp tục cuộc trò chuyện cũ đang ở chế độ Trợ lý ảo | Đã đăng nhập, có sẵn cuộc trò chuyện đang mở với Trợ lý ảo | 1. Bấm nút "Lịch sử trò chuyện".<br>2. Chọn một cuộc trò chuyện đang mở.<br>3. Kiểm tra giao diện hiển thị. | Click chọn phiên trò chuyện mã `#102` ($V\_$) | Khung chat hiển thị trọn vẹn lịch sử tin nhắn cũ, thanh tiêu đề thể hiện kết nối với Trợ lý ảo, ô nhập văn bản sẵn sàng gõ nội dung tiếp theo. | |
| **TC_CONV_02** | Kiểm tra khởi tạo phiên trò chuyện mới (Luồng con A-1) | Đã đăng nhập, đang mở cửa sổ chat | 1. Bấm nút "Bắt đầu cuộc trò chuyện mới".<br>2. Quan sát khung chat. | Click nút "Bắt đầu cuộc trò chuyện mới" | Tạo phiên mới tinh, hiển thị lời chào tự động: *"Xin chào! Mình là Trợ lý tư vấn PetHome..."* kèm các nút gợi ý chủ đề tư vấn. | |
| **TC_CONV_03** | Kiểm tra chọn phiên trò chuyện đã kết thúc (E-1) | Đã đăng nhập, danh sách có phiên đã "Đã kết thúc" | 1. Bấm nút "Lịch sử trò chuyện".<br>2. Chọn cuộc trò chuyện có nhãn "Đã kết thúc". | Click phiên trò chuyện `#099` (Trạng thái `Closed`) | Lịch sử tin nhắn cũ được tải lên nhưng **khóa ô nhập văn bản**, hiển thị dải thông báo xám: *"Phiên hỗ trợ này đã đóng. Bạn có thể bấm 'Bắt đầu cuộc trò chuyện mới' để được hỗ trợ tiếp."* | |
| **TC_CONV_04** | Kiểm tra chọn phiên đang chờ tư vấn viên tiếp quản (E-2) | Đã đăng nhập, phiên đang ở trạng thái `Waiting for Agent` | 1. Chọn cuộc trò chuyện đang chờ nhân viên.<br>2. Quan sát dải thông báo và ô nhập. | Click phiên trò chuyện `#105` | Hiển thị thông báo màu cam: *"Cuộc trò chuyện đang được chuyển tiếp tới nhân viên tư vấn. Vui lòng chờ trong giây lát..."*. Ô nhập vẫn mở cho phép gửi thêm tin nhắn, Trợ lý ảo tạm ngắt phản hồi tự động. | |
| **TC_CONV_05** | Kiểm tra hiển thị giao diện cho khách hàng mới chưa có lịch sử (E-3) | Tài khoản khách hàng mới vừa đăng ký, chưa có tin nhắn nào | 1. Đăng nhập tài khoản mới.<br>2. Nhấp xem nút "Lịch sử trò chuyện". | Tài khoản chưa có dữ liệu | Hiển thị hình minh họa trống kèm thông báo: *"Bạn chưa có cuộc trò chuyện nào trước đây."* và nút *"Trò chuyện ngay"*. Bấm nút sẽ mở phiên chat mới. | |
| **TC_CONV_06** | Kiểm tra xử lý khi mất kết nối đường truyền (E-4) | Đã đăng nhập, thiết bị ngắt kết nối mạng | 1. Ngắt mạng thiết bị.<br>2. Bấm chọn một cuộc trò chuyện trong lịch sử. | Thao tác chọn khi không có mạng | Hiển thị cảnh báo: *"Không thể tải nội dung do đường truyền không ổn định. Vui lòng bấm 'Thử lại'."* kèm nút "Thử lại". | |
| **TC_CONV_07** | Kiểm tra tính năng tải phân đoạn 50 tin nhắn (Lazy Loading) | Phiên trò chuyện có tổng cộng 70 tin nhắn trao đổi | 1. Chọn mở cuộc trò chuyện có 70 tin nhắn.<br>2. Quan sát số tin nhắn tải đầu tiên.<br>3. Cuộn ngược màn hình chat lên trên cùng. | Cuộn trang lên trên | Ban đầu hệ thống chỉ nạp 50 tin nhắn mới nhất. Khi cuộn lên đỉnh khung chat, hệ thống tự động tải thêm 20 tin nhắn cũ hơn còn lại. | |

---
---

# III. USE CASE 1.3: TƯ VẤN SẢN PHẨM VÀ GIẢI ĐÁP CHÍNH SÁCH TỰ ĐỘNG

## 3.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích ô nhập nội dung câu hỏi tư vấn

| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Nội dung câu hỏi** | • Bắt buộc có nội dung<br>• Độ dài 2 - 1000 ký tự<br>• Không chỉ chứa toàn khoảng trắng<br>• Có thể là câu đơn hoặc câu phức hợp nhiều ý | **V_MSG_01:** Câu hỏi hợp lệ 2 - 1000 ký tự về sản phẩm/giá/tồn kho (VD: *"Pate Royal Canin 2kg giá bao nhiêu?"*)<br>**V_MSG_02:** Câu hỏi hợp lệ về chính sách/bảo hành/đổi trả (VD: *"Shop có chính sách đổi trả hàng hư hỏng như thế nào?"*)<br>**V_MSG_03:** Câu hỏi phức hợp ghép nhiều ý (VD: *"Pate Royal Canin giá bao nhiêu và phí ship thế nào?"*) | **I_MSG_01:** Để trống không nhập gì<br>**I_MSG_02:** Chỉ nhập toàn khoảng trắng (VD: `"   "`)<br>**I_MSG_03:** Nội dung ngắn hơn 2 ký tự (VD: `"A"`)<br>**I_MSG_04:** Nội dung dài vượt quá 1000 ký tự<br>**I_MSG_05:** Câu hỏi ngoài phạm vi kinh doanh (Out of Domain - VD: *"Shop có bán mèo Anh lông ngắn không?"*, *"Dịch vụ khám bệnh thú y bao tiền?"*) | • Biên dưới độ dài: 1 ký tự ($I\_$), 2 ký tự ($V\_$), 3 ký tự ($V\_$)<br>• Biên trên độ dài: 999 ký tự ($V\_$), 1000 ký tự ($V\_$), 1001 ký tự ($I\_$) |

---

## 3.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Xử lý câu hỏi tư vấn khách hàng

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Câu hỏi có nội dung hợp lệ (2-1000 ký tự, không chỉ khoảng trắng)?** | F | T | T | T | T |
| **C2: Đường truyền mạng kết nối ổn định?** | - | F | T | T | T |
| **C3: Phiên chat đang do Tư vấn viên tiếp quản / Chờ tiếp quản (Human mode)?** | - | - | T | F | F |
| **C4: Nội dung thuộc phạm vi sản phẩm/chính sách thú cưng của cửa hàng?** | - | - | - | F | T |
| **H1: Không gửi tin nhắn, báo lỗi "Vui lòng nhập nội dung câu hỏi..." (E-1)** | X | | | | |
| **H2: Dừng gõ chữ, báo lỗi "Đường truyền bị gián đoạn. Vui lòng bấm Thử lại" (E-4)** | | X | | | |
| **H3: Ngắt Trợ lý ảo, lưu tin vào danh sách chờ nhân viên đọc (E-2)** | | | X | | |
| **H4: Trả lời giải thích ngoài phạm vi, gợi ý 2 nút "Kết nối nhân viên" & "Hỏi câu khác" (E-3)** | | | | X | |
| **H5: Sinh phản hồi dạng gõ chữ thời gian thực (SSE Stream), kèm nút "Xem trích dẫn nguồn"** | | | | | X |

---

## 3.4. Ma trận truy xuất nguồn gốc (Traceability Matrix - RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 1.3 - Luồng chính** | Gửi câu hỏi hợp lệ & nhận phản hồi gõ chữ thời gian thực (Single Query) | `TC_RAG_01` |
| **UC 1.3 - Rule 2** | Tư vấn câu hỏi phức hợp nhiều ý (Multi-subquery) | `TC_RAG_02` |
| **UC 1.3 - A-1** | Xem trích dẫn nguồn tài liệu & mở rộng nội dung đầy đủ | `TC_RAG_03` |
| **UC 1.3 - E-1** | Để trống hoặc chỉ nhập khoảng trắng trong ô câu hỏi | `TC_RAG_04` |
| **UC 1.3 - E-2** | Gửi câu hỏi khi phiên đang do Nhân viên CSKH hỗ trợ | `TC_RAG_05` |
| **UC 1.3 - E-3** | Hỏi các nội dung ngoài phạm vi kinh doanh (Out of Domain) | `TC_RAG_06`, `TC_RAG_07` |
| **UC 1.3 - E-4** | Gián đoạn đường truyền khi đang phát phản hồi | `TC_RAG_08` |
| **UC 1.3 - BVA** | Kiểm tra giới hạn độ dài nội dung câu hỏi (1 ký tự & 1001 ký tự) | `TC_RAG_09`, `TC_RAG_10` |

---

## 3.5. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_RAG_01** | Kiểm tra tư vấn sản phẩm đơn lẻ thành công (Happy Path) | Khung chat ở chế độ Trợ lý ảo (`Bot mode`) | 1. Nhập câu hỏi về giá sản phẩm.<br>2. Nhấn nút "Gửi" (hoặc bấm phím Enter).<br>3. Quan sát hiệu ứng phản hồi. | Nội dung: `"Cát vệ sinh Cature 6L giá bao nhiêu?"` ($V\_$) | Hiển thị biểu tượng động Trợ lý ảo đang phản hồi, sau đó câu trả lời xuất hiện dưới dạng **luồng gõ chữ thời gian thực**. Bên dưới đính kèm nút *"Xem trích dẫn nguồn"*. | |
| **TC_RAG_02** | Kiểm tra tư vấn câu hỏi phức hợp đa ý | Khung chat ở chế độ Trợ lý ảo (`Bot mode`) | 1. Nhập câu hỏi phức hợp chứa 3 ý hỏi khác nhau.<br>2. Nhấn nút "Gửi". | Nội dung: `"Pate Royal Canin 2kg giá bao nhiêu, có sẵn hàng không và phí ship thế nào?"` ($V\_$) | Trợ lý ảo trả lời trọn vẹn đầy đủ cả 3 ý (Giá bán, Tình trạng tồn kho, Phí giao hàng) trình bày dạng danh sách gạch đầu dòng rõ ràng, ngắt đoạn trực quan. | |
| **TC_RAG_03** | Kiểm tra xem chi tiết nguồn trích dẫn & Mở rộng văn bản (Luồng con A-1) | Trợ lý ảo vừa trả lời thành công câu hỏi ở `TC_RAG_01` | 1. Bấm nút "Xem trích dẫn nguồn" dưới tin nhắn phản hồi.<br>2. Quan sát hộp thoại thông tin (pop-up).<br>3. Bấm nút "Mở rộng nội dung đầy đủ". | Click nút *"Xem trích dẫn nguồn"* $\rightarrow$ Click *"Mở rộng nội dung đầy đủ"* | Hộp thoại pop-up hiển thị tên file chính sách tham chiếu, vị trí mục/trang và đoạn trích lược. Khi bấm "Mở rộng nội dung đầy đủ", đoạn văn bản chính sách xem trước được mở rộng hiển thị toàn văn không bị khuất. | |
| **TC_RAG_04** | Kiểm tra gửi nội dung chỉ có khoảng trắng (E-1) | Khung chat đang mở | 1. Nhập 5 dấu khoảng trắng vào ô chat.<br>2. Nhấn nút "Gửi". | Nội dung: `"     "` ($I\_$) | Hệ thống không gửi tin nhắn, hiển thị nhắc nhở ngay tại ô nhập: *"Vui lòng nhập nội dung câu hỏi trước khi gửi"*. Con trỏ giữ nguyên tại ô nhập. | |
| **TC_RAG_05** | Kiểm tra gửi câu hỏi khi phiên do Tư vấn viên hỗ trợ (E-2) | Phiên trò chuyện đang ở chế độ Tư vấn viên (`Human Agent mode`) | 1. Nhập câu hỏi mới.<br>2. Nhấn nút "Gửi". | Nội dung: `"Shop còn mở cửa không?"` | Trợ lý ảo **tạm ngắt phản hồi tự động**. Tin nhắn được lưu vào danh sách chờ nhân viên đọc. Hiển thị dải thông báo: *"Nhân viên tư vấn đang tiếp nhận cuộc trò chuyện, vui lòng chờ trong giây lát..."*. | |
| **TC_RAG_06** | Kiểm tra xử lý câu hỏi ngoài phạm vi kinh doanh (E-3) | Khung chat ở chế độ Trợ lý ảo (`Bot mode`) | 1. Nhập câu hỏi mua động vật sống (không thuộc mặt hàng đồ dùng thú cưng).<br>2. Nhấn nút "Gửi". | Nội dung: `"Shop có bán chó Poodle con thuần chủng không?"` ($I\_$) | Trợ lý ảo trả lời lịch sự giải thích cửa hàng PetHome chỉ chuyên kinh doanh sản phẩm đồ dùng & phụ kiện thú cưng nên không bán chó mèo sống. Đưa ra 2 gợi ý: *"Kết nối nhân viên"* và *"Hỏi câu khác"*. | |
| **TC_RAG_07** | Kiểm tra thao tác chuyển tư vấn viên khi hỏi câu ngoài phạm vi | Đang ở kết quả của `TC_RAG_06` | 1. Nhấn chọn nút "Kết nối nhân viên". | Click chọn nút *"Kết nối nhân viên"* | Trạng thái phiên chuyển sang *Chờ tư vấn viên tiếp quản (Waiting for Agent)*. Hiển thị tin nhắn thông báo chờ tư vấn viên tham gia hỗ trợ. | |
| **TC_RAG_08** | Kiểm tra xử lý gián đoạn kết nối khi đang phát phản hồi (E-4) | Trợ lý ảo đang gõ từng ký tự câu trả lời trên màn hình | 1. Ngắt kết nối mạng bất ngờ giữa chừng khi đang sinh phản hồi.<br>2. Quan sát giao diện.<br>3. Bật lại mạng và bấm nút "Thử lại". | Ngắt mạng $\rightarrow$ Kết nối lại mạng | Trợ lý ảo ngừng hiệu ứng gõ chữ, hiển thị thông báo lỗi: *"Đường truyền bị gián đoạn. Vui lòng bấm 'Thử lại'."*. Khi bấm "Thử lại", luồng trả lời được tiếp tục phát lại. | |
| **TC_RAG_09** | Kiểm tra nhập câu hỏi 1 ký tự (Biên lỗi dưới) | Khung chat đang mở | 1. Gõ đúng 1 ký tự vào ô chat.<br>2. Nhấn "Gửi". | Nội dung: `"?"` ($I\_$) | Báo lỗi nhắc nhở: *"Nội dung câu hỏi phải chứa từ 2 ký tự trở lên"*. | |
| **TC_RAG_10** | Kiểm tra nhập câu hỏi 1001 ký tự (Biên lỗi trên) | Khung chat đang mở | 1. Dán một đoạn văn bản dài 1001 ký tự vào ô gõ.<br>2. Nhấn "Gửi". | Nội dung: Chuỗi văn bản 1001 ký tự ($I\_$) | Ô nhập liệu tự động chặn không cho gõ/dán vượt quá 1000 ký tự (hoặc hiển thị cảnh báo đỏ dưới ô nhập: *"Nội dung câu hỏi vượt quá độ dài tối đa 1000 ký tự"*). | |

---
---

# IV. USE CASE 1.4: XÓA PHIÊN TRÒ CHUYỆN & VÔ HIỆU HÓA TICKET LIÊN QUAN

## 4.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích hành động xóa & đối tượng liên quan

| Đối tượng / Thao tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Quyền sở hữu phiên trò chuyện** | • Chỉ được phép xóa phiên thuộc tài khoản của chính mình | **V_DELETE_01:** Phiên trò chuyện do chính tài khoản đang đăng nhập tạo ra | **I_DELETE_01:** Thao tác xóa phiên trò chuyện của tài khoản người dùng khác | Không áp dụng biên (Kiểm tra quyền sở hữu) |
| **Phiếu hỗ trợ (Ticket) liên quan** | • Xóa phiên chat sẽ vô hiệu hóa đồng bộ Ticket đang phát sinh từ phiên đó | **V_TICKET_01:** Phiên không có Ticket nào kèm theo<br>**V_TICKET_02:** Phiên có Ticket ở trạng thái *Chờ tiếp nhận (Pending)* hoặc *Đang xử lý (In Progress)* | **I_TICKET_01:** Ticket liên quan đã ở trạng thái *Đã kết thúc (Closed)* trước đó | Không áp dụng biên (Theo tập trạng thái Ticket) |
| **Hộp thoại xác nhận (Modal Gate)** | • Bắt buộc thông qua hộp thoại xác nhận trước khi thực hiện xóa vĩnh viễn | **V_CONFIRM_01:** Khách hàng bấm nút "Xác nhận xóa"<br>**V_CONFIRM_02:** Khách hàng bấm nút "Hủy" (hoặc nhấp ra ngoài) | **I_CONFIRM_01:** Mất kết nối đường truyền mạng đúng thời điểm bấm xác nhận | Không áp dụng biên (Lựa chọn Yes/No) |

---

## 4.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Xóa phiên trò chuyện

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: Bấm biểu tượng thùng rác "Xóa cuộc trò chuyện"?** | T | T | T | T |
| **C2: Chọn "Xác nhận xóa" trên hộp thoại cảnh báo?** | F | T | T | T |
| **C3: Đường truyền mạng ổn định tại thời điểm xóa?** | - | F | T | T |
| **C4: Phiên trò chuyện có Ticket liên quan ở trạng thái Chờ tiếp nhận/Đang xử lý?** | - | - | F | T |
| **H1: Đóng hộp thoại, giữ nguyên phiên chat và Ticket không đổi (Luồng con A-1)** | X | | | |
| **H2: Báo lỗi "Lỗi kết nối đường truyền. Không thể xóa...", giữ nguyên dữ liệu (E-1)** | | X | | |
| **H3: Xóa vĩnh viễn tin nhắn & xóa phiên chat khỏi danh sách lịch sử** | | | X | X |
| **H4: Đồng bộ chuyển Ticket liên quan sang trạng thái Đã kết thúc (Closed - Vô hiệu hóa)** | | | | X |

---

## 4.3. Sơ đồ chuyển trạng thái (State Transition)

### Chuyển trạng thái của Phiên trò chuyện & Ticket khi thực hiện Xóa

| Đối tượng | Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- | :--- |
| **Phiên trò chuyện** | **Đang tồn tại (Active)** | Bấm biểu tượng thùng rác $\rightarrow$ Chọn "Hủy" | **Đang tồn tại (Active)** |
| **Phiên trò chuyện** | **Đang tồn tại (Active)** | Bấm biểu tượng thùng rác $\rightarrow$ Chọn "Xác nhận xóa" | **Bị xóa vĩnh viễn (Deleted)** |
| **Ticket hỗ trợ** | **Chờ tiếp nhận (Pending)** | Phiên trò chuyện chứa Ticket này bị xóa | **Đã kết thúc (Closed - Vô hiệu hóa)** |
| **Ticket hỗ trợ** | **Đang xử lý (In Progress)** | Phiên trò chuyện chứa Ticket này bị xóa | **Đã kết thúc (Closed - Vô hiệu hóa)** |

---

## 4.4. Ma trận truy xuất nguồn gốc (Traceability Matrix - RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 1.4 - Luồng chính** | Xóa phiên trò chuyện thông thường thành công | `TC_DEL_01` |
| **UC 1.4 - Rule 3** | Xóa phiên trò chuyện và tự động vô hiệu hóa Ticket liên quan | `TC_DEL_02` |
| **UC 1.4 - A-1** | Hủy bỏ thao tác xóa trên hộp thoại xác nhận | `TC_DEL_03` |
| **UC 1.4 - E-1** | Mất kết nối đường truyền khi đang thực hiện xóa | `TC_DEL_04` |
| **UC 1.4 - E-2** | Xóa phiên trò chuyện không còn tồn tại | `TC_DEL_05` |

---
---

# IV. USE CASE 1.4: XÓA PHIÊN TRÒ CHUYỆN & VÔ HIỆU HÓA TICKET LIÊN QUAN

## 4.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích hành động xóa & đối tượng liên quan

| Đối tượng / Thao tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Quyền sở hữu phiên trò chuyện** | • Chỉ được phép xóa phiên thuộc tài khoản của chính mình | **V_DELETE_01:** Phiên trò chuyện do chính tài khoản đang đăng nhập tạo ra | **I_DELETE_01:** Thao tác xóa phiên trò chuyện của tài khoản người dùng khác | Không áp dụng biên (Kiểm tra quyền sở hữu) |
| **Phiếu hỗ trợ (Ticket) liên quan** | • Xóa phiên chat sẽ vô hiệu hóa đồng bộ Ticket đang phát sinh từ phiên đó | **V_TICKET_01:** Phiên không có Ticket nào kèm theo<br>**V_TICKET_02:** Phiên có Ticket ở trạng thái *Chờ tiếp nhận (Pending)* hoặc *Đang xử lý (In Progress)* | **I_TICKET_01:** Ticket liên quan đã ở trạng thái *Đã kết thúc (Closed)* trước đó | Không áp dụng biên (Theo tập trạng thái Ticket) |
| **Hộp thoại xác nhận (Modal Gate)** | • Bắt buộc thông qua hộp thoại xác nhận trước khi thực hiện xóa vĩnh viễn | **V_CONFIRM_01:** Khách hàng bấm nút "Xác nhận xóa"<br>**V_CONFIRM_02:** Khách hàng bấm nút "Hủy" (hoặc nhấp ra ngoài) | **I_CONFIRM_01:** Mất kết nối đường truyền mạng đúng thời điểm bấm xác nhận | Không áp dụng biên (Lựa chọn Yes/No) |

---

## 4.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Xóa phiên trò chuyện

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: Bấm biểu tượng thùng rác "Xóa cuộc trò chuyện"?** | T | T | T | T |
| **C2: Chọn "Xác nhận xóa" trên hộp thoại cảnh báo?** | F | T | T | T |
| **C3: Đường truyền mạng ổn định tại thời điểm xóa?** | - | F | T | T |
| **C4: Phiên trò chuyện có Ticket liên quan ở trạng thái Chờ tiếp nhận/Đang xử lý?** | - | - | F | T |
| **H1: Đóng hộp thoại, giữ nguyên phiên chat và Ticket không đổi (Luồng con A-1)** | X | | | |
| **H2: Báo lỗi "Lỗi kết nối đường truyền. Không thể xóa...", giữ nguyên dữ liệu (E-1)** | | X | | |
| **H3: Xóa vĩnh viễn tin nhắn & xóa phiên chat khỏi danh sách lịch sử** | | | X | X |
| **H4: Đồng bộ chuyển Ticket liên quan sang trạng thái Đã kết thúc (Closed - Vô hiệu hóa)** | | | | X |

---

## 4.3. Sơ đồ chuyển trạng thái (State Transition)

### Chuyển trạng thái của Phiên trò chuyện & Ticket khi thực hiện Xóa

| Đối tượng | Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- | :--- |
| **Phiên trò chuyện** | **Đang tồn tại (Active)** | Bấm biểu tượng thùng rác $\rightarrow$ Chọn "Hủy" | **Đang tồn tại (Active)** |
| **Phiên trò chuyện** | **Đang tồn tại (Active)** | Bấm biểu tượng thùng rác $\rightarrow$ Chọn "Xác nhận xóa" | **Bị xóa vĩnh viễn (Deleted)** |
| **Ticket hỗ trợ** | **Chờ tiếp nhận (Pending)** | Phiên trò chuyện chứa Ticket này bị xóa | **Đã kết thúc (Closed - Vô hiệu hóa)** |
| **Ticket hỗ trợ** | **Đang xử lý (In Progress)** | Phiên trò chuyện chứa Ticket này bị xóa | **Đã kết thúc (Closed - Vô hiệu hóa)** |

---

## 4.4. Ma trận truy xuất nguồn gốc (Traceability Matrix - RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 1.4 - Luồng chính** | Xóa phiên trò chuyện thông thường thành công | `TC_DEL_01` |
| **UC 1.4 - Rule 3** | Xóa phiên trò chuyện và tự động vô hiệu hóa Ticket liên quan | `TC_DEL_02` |
| **UC 1.4 - A-1** | Hủy bỏ thao tác xóa trên hộp thoại xác nhận | `TC_DEL_03` |
| **UC 1.4 - E-1** | Mất kết nối đường truyền khi đang thực hiện xóa | `TC_DEL_04` |
| **UC 1.4 - E-2** | Xóa phiên trò chuyện không còn tồn tại | `TC_DEL_05` |

---

## 4.5. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DEL_01** | Kiểm tra xóa phiên trò chuyện không có Ticket đính kèm | Đang mở danh sách lịch sử trò chuyện, chọn 1 phiên thường | 1. Rê chuột vào mục cuộc trò chuyện cần xóa.<br>2. Nhấn biểu tượng thùng rác *"Xóa cuộc trò chuyện"*.<br>3. Tại hộp thoại xác nhận, bấm *"Xác nhận xóa"*. | Click nút thùng rác $\rightarrow$ Click *"Xác nhận xóa"* ($V\_$) | Hộp thoại đóng lại, hiển thị dải thông báo xanh: *"Đã xóa cuộc trò chuyện thành công!"*. Phiên trò chuyện biến mất vĩnh viễn khỏi danh sách lịch sử. | |
| **TC_DEL_02** | Kiểm tra xóa phiên trò chuyện có chứa Ticket đang mở | Phiên trò chuyện `#108` đang phát sinh 1 Ticket hỗ trợ ở trạng thái *Đang xử lý (In Progress)* | 1. Thực hiện xóa phiên trò chuyện `#108`.<br>2. Bấm *"Xác nhận xóa"*. | Click *"Xác nhận xóa"* | Phiên trò chuyện bị xóa khỏi lịch sử. Ticket liên quan tự động chuyển sang trạng thái **Đã kết thúc (Closed)** kèm ghi nhận lý do *"Phiên hội thoại đã bị khách hàng xóa"*, đồng hồ SLA dừng đếm ngược và Ticket gỡ khỏi hàng đợi. | |
| **TC_DEL_03** | Kiểm tra hủy bỏ thao tác xóa cuộc trò chuyện (Luồng con A-1) | Màn hình đang hiển thị hộp thoại xác nhận xóa cuộc trò chuyện | 1. Nhấn nút "Hủy" (hoặc nhấp ra ngoài hộp thoại). | Click chọn nút *"Hủy"* | Hộp thoại xác nhận đóng lại. Phiên trò chuyện và mọi dữ liệu phiếu hỗ trợ liên quan được giữ nguyên vẹn không bị thay đổi. | |
| **TC_DEL_04** | Kiểm tra xử lý khi mất kết nối mạng lúc xóa (E-1) | Màn hình hiển thị hộp thoại xác nhận xóa, ngắt mạng thiết bị | 1. Ngắt kết nối mạng.<br>2. Bấm nút *"Xác nhận xóa"*. | Thao tác bấm khi ngắt mạng | Hệ thống không thực hiện xóa, hiển thị cảnh báo đỏ: *"Lỗi kết nối đường truyền. Không thể xóa cuộc trò chuyện lúc này. Vui lòng thử lại!"*. Phiên chat được khôi phục nguyên vẹn. | |
| **TC_DEL_05** | Kiểm tra xóa phiên trò chuyện đã bị xóa ở thiết bị/cửa sổ khác (E-2) | Phiên chat đã bị xóa ở cửa sổ trình duyệt khác trước đó vài giây | 1. Bấm nút thùng rác xóa phiên chat.<br>2. Bấm *"Xác nhận xóa"*. | Thao tác trên bản ghi đã mất | Hiển thị cảnh báo lỗi: *"Phiên trò chuyện này không còn tồn tại"*. Hệ thống tự động làm mới danh sách lịch sử trò chuyện. | |

---
*Tài liệu kiểm thử hộp đen Khối chức năng 1 được biên soạn hoàn chỉnh tuân thủ cấu trúc tài liệu mẫu `cau-truc-kiem-thu-hop-den.md` và chuẩn ngữ phong từ góc nhìn End-User.*
