TRƯỜNG ĐẠI HỌC THỦY LỢI

**KHOA CÔNG NGHỆ THÔNG TIN**

**BÁO CÁO BÀI TẬP LỚN MÔN HỌC**

**KIỂM THỬ VÀ ĐẢM BẢO CHẤT LƯỢNG PHẦN MỀM** 

**Đề tài:**

**KIỂM THỬ WEBSITE TƯ VẤN KHÁCH HÀNG TỰ ĐỘNG VÀ ĐIỀU PHỐI HỖ TRỢ THÔNG MINH CHO CHUỖI CỬA HÀNG ĐỒ DÙNG THÚ CƯNG**

**Nhóm sinh viên thực hiện:** Nhóm **7**

**Thành viên nhóm:**    	    	

* Nguyễn Hà Phương Uyên - 65KTPM - 235170632

* Nguyễn Thị Phương Thảo - 65KTPM - 2351170621

* Nguyễn Thị Hồng Mai - 65KTPM - 2351170606

* Nguyễn Minh - 65KTPM - 2351170607

**Giảng viên phụ trách môn học:** Nguyễn Thị Phương Dung

Hà Nội, năm 2026

# **MỤC LỤC** {#mục-lục}

[**MỤC LỤC**](#mục-lục)

[**I. TỔNG QUAN ĐỀ TÀI VÀ PHÂN CÔNG THỰC HIỆN**](#tổng-quan-đề-tài-và-phân-công-thực-hiện)

[1. Giới thiệu đề tài](#1.-giới-thiệu-đề-tài)

[2. Các chức năng chính trong đề tài](#2.-các-chức-năng-chính-trong-đề-tài)

[2.1. Phân hệ Trợ lý tư vấn khách hàng tự động](#2.1.-phân-hệ-trợ-lý-tư-vấn-khách-hàng-tự-động)

[2.2. Phân hệ Giám sát hội thoại ngầm và Khởi tạo yêu cầu hỗ trợ khẩn cấp](#2.2.-phân-hệ-giám-sát-hội-thoại-ngầm-và-khởi-tạo-yêu-cầu-hỗ-trợ-khẩn-cấp)

[2.3. Phân hệ Cổng hỗ trợ trực tiếp dành cho nhân viên tư vấn](#2.3.-phân-hệ-cổng-hỗ-trợ-trực-tiếp-dành-cho-nhân-viên-tư-vấn)

[2.4. Phân hệ Điều phối phân việc, Giám sát cam kết dịch vụ và Báo cáo](#2.4.-phân-hệ-điều-phối-phân-việc,-giám-sát-cam-kết-dịch-vụ-và-báo-cáo)

[3. Phân công công việc](#3.-phân-công-công-việc)

[**II. ĐẶC TẢ YÊU CẦU CHỨC NĂNG HỆ THỐNG VÀ THIẾT KẾ KIỂM THỬ HỘP ĐEN**](#ii.-đặc-tả-yêu-cầu-chức-năng-hệ-thống)

[Use case 1.1: Quản lý tài khoản khách hàng](#uc-1-1)

[Use case 1.2: Quản lý phiên trò chuyện](#uc-1-2)

[Use case 1.3: Tư vấn sản phẩm và giải đáp chính sách tự động](#uc-1-3)

[Use case 1.4: Xóa phiên trò chuyện & vô hiệu hóa Ticket liên quan](#uc-1-4)

[Use case 2.1: Phân tích cảm xúc & Đánh giá nguy cơ tự động](#uc-2-1)

[Use case 2.2: Khởi tạo phiếu hỗ trợ khẩn cấp và chuyển giao CSKH](#uc-2-2)

[Use case 2.3: Cấu hình quy tắc phân loại sự cố và cảnh báo](#uc-2-3)

[Use case 3.1: Quản lý tài khoản nhân viên](#uc-3-1)

[Use case 3.2: Quản lý trạng thái làm việc của nhân viên](#uc-3-2)

[Use case 3.3: Theo dõi hàng đợi và tiếp quản cuộc trò chuyện](#uc-3-3)

[Use case 3.4: Quản lý và sử dụng mẫu phản hồi nhanh](#uc-3-4)

[Use case 4.1: Phân chia công việc tự động](#uc-4-1)

[Use case 4.2: Giám sát thời hạn xử lý cam kết](#uc-4-2)

[Use case 4.3: Quản lý tiến độ trên bảng Kanban](#uc-4-3)

[Use case 4.4: Báo cáo thống kê hiệu suất](#uc-4-4)

---

# **I. TỔNG QUAN ĐỀ TÀI VÀ PHÂN CÔNG THỰC HIỆN** {#tổng-quan-đề-tài-và-phân-công-thực-hiện}

## **1. Giới thiệu đề tài** {#1.-giới-thiệu-đề-tài}

Thị trường kinh doanh sản phẩm và dịch vụ chăm sóc thú cưng tại Việt Nam đang ghi nhận mức tăng trưởng nhanh chóng. Đi kèm với sự mở rộng quy mô của các chuỗi bán lẻ là lượng tương tác, tin nhắn tư vấn và yêu cầu hỗ trợ từ khách hàng gia tăng đột biến. Trong thực tế vận hành, phần lớn các thắc mắc thường lặp lại xoay quanh thông tin mặt hàng, cách chọn thức ăn, phụ kiện phù hợp cho từng giống loài, kiểm tra tồn kho tại các chi nhánh, hay chính sách bảo hành và đổi trả. Việc nhân viên tư vấn phải liên tục trả lời thủ công các câu hỏi cơ bản dẫn đến tình trạng quá tải, kéo dài thời gian phản hồi và dễ làm trôi các khiếu nại nghiêm trọng. Ngược lại, việc ứng dụng các kịch bản tự động truyền thống thường cứng nhắc, thiếu ngữ cảnh và dễ gây ức chế cho người mua khi phát sinh sự cố.

Xuất phát từ bài toán thực tế đó, đề tài "***Website tư vấn khách hàng tự động và điều phối hỗ trợ thông minh cho chuỗi cửa hàng đồ dùng thú cưng***" được triển khai nhằm xây dựng một giải pháp toàn diện, kết hợp hài hòa giữa khả năng tự động hóa và sự can thiệp kịp thời của con người.

Hệ thống hướng đến hai mục tiêu cốt lõi:

1. Đối với khách hàng: Cho phép người nuôi thú cưng tra cứu thông tin sản phẩm và chính sách cửa hàng 24/7 một cách chính xác, tự nhiên như đang trò chuyện với tư vấn viên am hiểu.  
2. Đối với chuỗi cửa hàng: Xây dựng quy trình tiếp nhận, sàng lọc và phân phối yêu cầu hỗ trợ một cách khoa học. Hệ thống tự động nhận diện sớm các tình huống khách hàng bức xúc để chuyển giao ngay cho nhân viên phụ trách, đồng thời phân bổ công việc đồng đều và giám sát tiến độ xử lý khiếu nại nhằm duy trì chất lượng dịch vụ đồng nhất trên toàn hệ thống.  

## **2. Các chức năng chính trong đề tài** {#2.-các-chức-năng-chính-trong-đề-tài}

Hệ thống được thiết kế xoay quanh bốn nhóm chức năng nghiệp vụ trọng tâm, phục vụ từ trải nghiệm tương tác của người dùng đến công tác quản lý và vận hành nội bộ:

### ***2.1. Phân hệ Trợ lý tư vấn khách hàng tự động*** {#2.1.-phân-hệ-trợ-lý-tư-vấn-khách-hàng-tự-động}

* **Quản lý tài khoản khách hàng**: Khách hàng có thể đăng ký tài khoản, đăng nhập.  
* **Quản lý cuộc hội thoại**: theo dõi và tiếp tục các đoạn hội thoại trước đó hoặc mở phiên trò chuyện mới bất kỳ lúc nào.  
* **Tư vấn sản phẩm và giải đáp chính sách tự động**: Trợ lý ảo tiếp nhận câu hỏi của người mua để phản hồi ngay lập tức dạng luồng gõ chữ thời gian thực kèm trích dẫn nguồn.  
* **Xóa phiên trò chuyện & vô hiệu hóa Ticket liên quan**: Khách hàng có thể xóa các phiên trò chuyện của mình, hệ thống tự động vô hiệu hóa Ticket liên quan.

### ***2.2. Phân hệ Giám sát hội thoại ngầm và Khởi tạo yêu cầu hỗ trợ khẩn cấp*** {#2.2.-phân-hệ-giám-sát-hội-thoại-ngầm-và-khởi-tạo-yêu-cầu-hỗ-trợ-khẩn-cấp}

* **Phân tích cảm xúc & Đánh giá nguy cơ tự động**: Đánh giá chỉ số cảm xúc theo ngữ cảnh.  
* **Khởi tạo phiếu hỗ trợ khẩn cấp và chuyển giao CSKH**: Tự động mở ticket khẩn cấp và ngắt bot khi khẩn cấp.  
* **Cấu hình quy tắc phân loại sự cố và cảnh báo**: Quản lý thiết lập các quy tắc cảnh báo linh hoạt.

### ***2.3. Phân hệ Cổng hỗ trợ trực tiếp dành cho nhân viên tư vấn*** {#2.3.-phân-hệ-cổng-hỗ-trợ-trực-tiếp-dành-cho-nhân-viên-tư-vấn}

* **Quản lý tài khoản nhân viên**: Đăng ký, đăng nhập tài khoản làm việc nội bộ.  
* **Quản lý trạng thái làm việc**: Bật/tắt trạng thái Trực tuyến (ONLINE), Bận (BUSY), Ngoại tuyến (OFFLINE).  
* **Theo dõi hàng đợi và tiếp quản cuộc trò chuyện**: Tiếp quản phiên tư vấn và chat thời gian thực.  
* **Quản lý và sử dụng mẫu phản hồi nhanh**: Tra cứu phím tắt `/` để chèn nhanh câu trả lời chuẩn.

### ***2.4. Phân hệ Điều phối phân việc, Giám sát cam kết dịch vụ và Báo cáo*** {#2.4.-phân-hệ-điều-phối-phân-việc,-giám-sát-cam-kết-dịch-vụ-và-báo-cáo}

* **Phân chia công việc tự động**: Tự động chia việc cho nhân viên rảnh nhất theo kỹ năng.  
* **Giám sát thời hạn xử lý cam kết**: Đếm ngược SLA theo mức độ khẩn cấp (P1, P2, P3).  
* **Quản lý tiến độ trên bảng Kanban**: Kéo thả thẻ công việc cập nhật tiến độ.  
* **Báo cáo thống kê hiệu suất**: Biểu đồ phân tích hiệu suất và tỷ lệ vi phạm SLA.

## **3. Phân công công việc** {#3.-phân-công-công-việc}

| STT | Thành viên phụ trách | Phân hệ chức năng | Chi tiết các chức năng đảm nhiệm |
| :---: | ----- | ----- | ----- |
| 1 | Nguyễn Hà Phương Uyên | Phân hệ Trợ lý tư vấn khách hàng tự động | 1. Quản lý tài khoản khách hàng<br>2. Quản lý phiên hội thoại<br>3. Tư vấn sản phẩm và giải đáp chính sách tự động<br>4. Xóa phiên trò chuyện & vô hiệu hóa Ticket |
| 2 | Nguyễn Thị Phương Thảo | Phân hệ Giám sát hội thoại ngầm và Khởi tạo yêu cầu hỗ trợ khẩn cấp | 1. Phân tích cảm xúc & Đánh giá nguy cơ tự động<br>2. Khởi tạo phiếu hỗ trợ khẩn cấp và chuyển giao CSKH<br>3. Cấu hình quy tắc phân loại sự cố và cảnh báo |
| 3 | Nguyễn Thị Hồng Mai | Phân hệ Cổng hỗ trợ trực tiếp dành cho nhân viên tư vấn | 1. Quản lý tài khoản nhân viên<br>2. Quản lý trạng thái làm việc của nhân viên<br>3. Theo dõi hàng đợi và tiếp quản cuộc trò chuyện<br>4. Quản lý và sử dụng mẫu phản hồi nhanh |
| 4 | Nguyễn Minh | Phân hệ Điều phối phân việc, Giám sát cam kết dịch vụ và Báo cáo | 1. Phân chia công việc tự động<br>2. Giám sát thời hạn xử lý cam kết<br>3. Quản lý tiến độ trên bảng Kanban<br>4. Báo cáo thống kê hiệu suất |

---

# **II. ĐẶC TẢ YÊU CẦU CHỨC NĂNG HỆ THỐNG VÀ THIẾT KẾ KIỂM THỬ HỘP ĐEN** {#ii.-đặc-tả-yêu-cầu-chức-năng-hệ-thống}


### Use case 1.1: Quản lý tài khoản khách hàng {#uc-1-1}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Khách hàng |
| **Điều kiện bắt đầu** | 1. Khách hàng đã truy cập vào trang web của chuỗi cửa hàng đồ dùng thú cưng.<br>2. Thiết bị của khách hàng có kết nối mạng ổn định tới hệ thống. |
| **Luồng sự kiện chính (Đăng ký tài khoản mới)** | 1. Khách hàng chọn nút "Đăng ký" trên thanh điều hướng của website.<br>2. Hệ thống hiển thị biểu mẫu "Đăng ký tài khoản khách hàng" gồm các trường thông tin:<br>• Họ và tên: Bắt buộc; nhập chữ tiếng Việt hoặc tiếng Anh cùng khoảng trắng, độ dài 2-50 ký tự.<br>• Địa chỉ Email: Bắt buộc; đúng định dạng email tiêu chuẩn (VD: tennguoidung@domain.com), tối đa 255 ký tự.<br>• Số điện thoại: Tùy chọn; nếu nhập phải đủ 10 chữ số bắt đầu bằng số 0.<br>• Mật khẩu: Bắt buộc; độ dài từ 8 ký tự trở lên, chứa ít nhất một chữ cái và một chữ số.<br>• Xác nhận mật khẩu: Bắt buộc; nhập lại chính xác mật khẩu ở trên.<br>(Lưu ý: Biểu mẫu có sẵn liên kết "Bạn đã có tài khoản? Đăng nhập ngay". Nếu chọn, thực hiện Luồng con A-1).<br>3. Khách hàng điền đầy đủ thông tin.<br>4. Khách hàng nhấn nút "Tạo tài khoản".<br>5. Hệ thống kiểm tra thông tin bắt buộc. Nếu để trống, thực hiện E-1.<br>6. Hệ thống kiểm tra định dạng dữ liệu (email, số điện thoại, mật khẩu). Nếu sai, thực hiện E-2.<br>7. Hệ thống so khớp mật khẩu xác nhận. Nếu không khớp, thực hiện E-3.<br>8. Hệ thống kiểm tra sự tồn tại của email. Nếu đã được đăng ký, thực hiện E-4.<br>9. Hệ thống ghi nhận tài khoản mới vào cơ sở dữ liệu với trạng thái hoạt động bình thường, tự động thiết lập phiên đăng nhập.<br>10. Đầu ra: Hệ thống hiển thị thông báo xanh: "Chúc mừng bạn đã tạo tài khoản thành công! Chào mừng bạn đến với PetHome.", chuyển hướng về Trang chủ và cập nhật hiển thị tên khách hàng trên thanh điều hướng. |
| **Luồng con (A-1: Đăng nhập tài khoản)** | 1. Khách hàng chọn liên kết "Đăng nhập ngay" (hoặc bấm nút "Đăng nhập" trên thanh điều hướng).<br>2. Hệ thống hiển thị biểu mẫu "Đăng nhập" gồm:<br>• Địa chỉ Email: Bắt buộc.<br>• Mật khẩu: Bắt buộc.<br>3. Khách hàng nhập email và mật khẩu.<br>4. Khách hàng nhấn "Đăng nhập".<br>5. Nếu để trống, thực hiện E-1.<br>6. Nếu email không tồn tại, thực hiện E-5.<br>7. Nếu tài khoản bị khóa/vô hiệu hóa, thực hiện E-6.<br>8. Nếu sai mật khẩu, thực hiện E-7.<br>9. Hệ thống khởi tạo phiên làm việc, đặt lại bộ đếm đăng nhập sai về 0 và tải lịch sử trao đổi gần nhất.<br>10. Đầu ra: Thông báo "Đăng nhập thành công", cập nhật giao diện và mở khung hội thoại chứa lịch sử tin nhắn trước đó.<br>11. Use Case kết thúc thành công. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Bỏ trống trường thông tin bắt buộc<br>1. Hệ thống làm sáng viền đỏ tại ô trống và hiển thị lỗi: "Vui lòng không để trống trường thông tin này".<br>2. Giữ nguyên nội dung ô hợp lệ khác và đưa con trỏ về ô trống đầu tiên.<br>3. Khách hàng chỉnh sửa và tiếp tục.<br><br>E-2: Định dạng dữ liệu không hợp lệ<br>1. Báo lỗi chi tiết tại ô không hợp lệ (VD: "Địa chỉ email không đúng định dạng", "Số điện thoại phải gồm 10 chữ số bắt đầu bằng 0", "Mật khẩu tối thiểu 8 ký tự gồm chữ và số").<br>2. Xóa dữ liệu ô sai để nhập lại.<br><br>E-3: Xác nhận mật khẩu không khớp<br>1. Hiển thị cảnh báo đỏ dưới ô Xác nhận mật khẩu: "Mật khẩu xác nhận không trùng khớp".<br>2. Xóa ô xác nhận mật khẩu để người dùng gõ lại.<br><br>E-4: Địa chỉ Email đã tồn tại<br>1. Hiển thị cảnh báo: "Địa chỉ email này đã được sử dụng. Vui lòng chọn Đăng nhập".<br>2. Hiển thị nút gợi ý "Chuyển sang Đăng nhập".<br><br>E-5: Email đăng nhập không tồn tại<br>1. Thông báo lỗi: "Thông tin tài khoản hoặc mật khẩu không chính xác".<br><br>E-6: Tài khoản đang bị khóa<br>1. Thông báo: "Tài khoản hiện đang bị tạm khóa. Vui lòng quay lại sau hoặc liên hệ bộ phận hỗ trợ".<br>2. Kết thúc thất bại.<br><br>E-7: Nhập sai mật khẩu<br>1. Tăng số lần sai thêm 1. Nếu sai 5 lần liên tiếp, chuyển sang E-6 (khóa tạm thời 15 phút).<br>2. Nếu chưa mốc 5, báo lỗi "Thông tin tài khoản hoặc mật khẩu không chính xác" kèm số lượt thử còn lại. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Tính duy nhất của tài khoản: Mỗi khách hàng sở hữu 1 tài khoản duy nhất tương ứng với 1 Email.<br>2. Bảo vệ dò mật khẩu: Nhập sai mật khẩu 5 lần liên tiếp trong 15 phút sẽ tự động khóa đăng nhập 15 phút.<br>3. Duy trì ngữ cảnh: Sau khi đăng nhập thành công, hệ thống gán tài khoản với phiên trò chuyện hiện tại và tải lại đầy đủ tin nhắn cũ.<br>4. Quy định mật khẩu: Tối thiểu 8 ký tự, bắt buộc chứa cả chữ và số. |

#### **Kiểm thử hộp đen Use case 1.1: Quản lý tài khoản khách hàng**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Họ và tên** *(Đăng ký)* | • Bắt buộc<br>• Độ dài 2 - 50 ký tự<br>• Chỉ chứa chữ cái tiếng Việt/Anh và khoảng trắng | **V_NAME_01:** Chuỗi chữ hợp lệ có độ dài từ 2 - 50 ký tự (VD: `"Nguyễn Văn A"`) | **I_NAME_01:** Để trống<br>**I_NAME_02:** Chuỗi ngắn hơn 2 ký tự (VD: `"A"`)<br>**I_NAME_03:** Chuỗi dài hơn 50 ký tự<br>**I_NAME_04:** Chứa số hoặc ký tự đặc biệt (VD: `"Nam123"`, `"An@%"`) | • Biên dưới: 1 ký tự (I), 2 ký tự (V), 3 ký tự (V)<br>• Biên trên: 49 ký tự (V), 50 ký tự (V), 51 ký tự (I) |
| **Địa chỉ Email** *(Đăng ký/Đăng nhập)* | • Bắt buộc<br>• Đúng định dạng email tiêu chuẩn (`ten@domain.com`)<br>• Tối đa 255 ký tự<br>• Duy nhất trên hệ thống | **V_EMAIL_01:** Đúng định dạng email, chưa tồn tại, độ dài $≤ 255$ ký tự (VD: `"user@gmail.com"`) | **I_EMAIL_01:** Để trống<br>**I_EMAIL_02:** Sai định dạng (VD: `"user@"` , `"user.com"`, `"user@domain"`)<br>**I_EMAIL_03:** Email vượt quá 255 ký tự<br>**I_EMAIL_04:** Email đã tồn tại trên hệ thống | • Biên trên độ dài: 255 ký tự (V), 256 ký tự (I) |
| **Số điện thoại** *(Đăng ký)* | • Tùy chọn (Không bắt buộc)<br>• Nếu nhập: Bắt buộc đủ 10 chữ số và bắt đầu bằng số `0` | **V_PHONE_01:** Để trống không nhập<br>**V_PHONE_02:** Đủ 10 chữ số, bắt đầu bằng số `0` (VD: `"0912345678"`) | **I_PHONE_01:** Ít hơn 10 chữ số (VD: `"091234567"`)<br>**I_PHONE_02:** Nhiều hơn 10 chữ số (VD: `"09123456789"`)<br>**I_PHONE_03:** Đủ 10 chữ số nhưng không bắt đầu bằng số `0` (VD: `"1912345678"`)<br>**I_PHONE_04:** Chứa chữ cái hoặc ký tự đặc biệt (VD: `"0912abc345"`) | • Biên độ dài: 9 chữ số (I), 10 chữ số bắt đầu bằng `0` (V), 11 chữ số (I) |
| **Mật khẩu** *(Đăng ký/Đăng nhập)* | • Bắt buộc<br>• Độ dài từ 8 ký tự trở lên<br>• Chứa ít nhất 1 chữ cái và 1 chữ số | **V_PASS_01:** Mật khẩu $≥ 8$ ký tự, chứa cả chữ và số (VD: `"Abc12345"`) | **I_PASS_01:** Để trống<br>**I_PASS_02:** Ít hơn 8 ký tự (VD: `"Abc1234"`)<br>**I_PASS_03:** Chỉ chứa toàn chữ cái, không có số (VD: `"Abcdefgh"`)<br>**I_PASS_04:** Chỉ chứa toàn chữ số, không có chữ (VD: `"12345678"`) | • Biên độ dài: 7 ký tự (I), 8 ký tự (V), 9 ký tự (V) |
| **Xác nhận mật khẩu** *(Đăng ký)* | • Bắt buộc<br>• Phải khớp hoàn toàn từng ký tự với ô Mật khẩu | **V_CONFIRM_01:** Chuỗi trùng khớp hoàn toàn với ô Mật khẩu | **I_CONFIRM_01:** Để trống<br>**I_CONFIRM_02:** Không trùng khớp với ô Mật khẩu (VD: gõ sai 1 ký tự) | Không áp dụng biên (so khớp chuỗi) |

---

##### 2. Bảng quyết định (Decision Table)


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

##### 3. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

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

##### 4. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_REG_01** | Kiểm tra đăng ký tài khoản mới thành công (Happy Path) | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Họ và tên hợp lệ.<br>2. Nhập Email chưa đăng ký.<br>3. Nhập Số điện thoại hợp lệ.<br>4. Nhập Mật khẩu hợp lệ.<br>5. Nhập Xác nhận mật khẩu trùng khớp.<br>6. Nhấn nút "Tạo tài khoản". | • Họ tên: `"Trần Văn An"` (V)<br>• Email: `"an.tran@gmail.com"` (V)<br>• SĐT: `"0912345678"` (V)<br>• Mật khẩu: `"An123456"` (V)<br>• Xác nhận: `"An123456"` (V) | Hiển thị thông báo xanh: *"Chúc mừng bạn đã tạo tài khoản thành công! Chào mừng bạn đến với PetHome."*, tự động đăng nhập và chuyển hướng về Trang chủ. | |
| **TC_REG_02** | Kiểm tra đăng ký khi để trống Họ và tên | Đang ở màn hình Đăng ký tài khoản | 1. Để trống ô Họ và tên.<br>2. Điền hợp lệ tất cả các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • Họ tên: `""` (I)<br>• Các trường khác: Nhập đúng giá trị (V) như `TC_REG_01` | Viền ô "Họ và tên" hằn đỏ, hiển thị thông báo lỗi ngay bên dưới: *"Vui lòng không để trống trường thông tin này"*. Con trỏ nhấp nháy tại ô Họ tên. | |
| **TC_REG_03** | Kiểm tra đăng ký với Họ và tên chứa chữ số | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Họ tên chứa chữ số.<br>2. Điền hợp lệ các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • Họ tên: `"Trần Văn 123"` (I)<br>• Trường khác: Nhập đúng (V) | Hiển thị thông báo lỗi dưới ô Họ và tên: *"Họ và tên chỉ bao gồm chữ cái tiếng Việt hoặc tiếng Anh và khoảng trắng"*. | |
| **TC_REG_04** | Kiểm tra đăng ký với Email sai định dạng | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Email sai cấu trúc tiêu chuẩn.<br>2. Điền hợp lệ các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • Email: `"an.trangmail.com"` (I)<br>• Trường khác: Nhập đúng (V) | Hiển thị thông báo lỗi dưới ô Email: *"Địa chỉ email không đúng định dạng"*. | |
| **TC_REG_05** | Kiểm tra đăng ký với Số điện thoại 9 chữ số (Biển lỗi) | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Số điện thoại chỉ có 9 chữ số.<br>2. Điền hợp lệ các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • SĐT: `"091234567"` (I)<br>• Trường khác: Nhập đúng (V) | Hiển thị thông báo lỗi dưới ô SĐT: *"Số điện thoại phải gồm 10 chữ số bắt đầu bằng số 0"*. | |
| **TC_REG_06** | Kiểm tra đăng ký với Mật khẩu 7 ký tự (Biên lỗi) | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Mật khẩu 7 ký tự.<br>2. Nhập Xác nhận mật khẩu 7 ký tự khớp với Mật khẩu.<br>3. Điền hợp lệ các ô còn lại.<br>4. Nhấn nút "Tạo tài khoản". | • Mật khẩu: `"An12345"` (I)<br>• Xác nhận: `"An12345"`<br>• Trường khác: Nhập đúng (V) | Hiển thị thông báo lỗi dưới ô Mật khẩu: *"Mật khẩu tối thiểu 8 ký tự gồm chữ và số"*. | |
| **TC_REG_07** | Kiểm tra đăng ký khi Mật khẩu xác nhận không trùng khớp | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Mật khẩu hợp lệ.<br>2. Nhập Xác nhận mật khẩu khác ký tự.<br>3. Nhấn nút "Tạo tài khoản". | • Mật khẩu: `"An123456"` (V)<br>• Xác nhận: `"An123457"` (I)<br>• Trường khác: Nhập đúng (V) | Hiển thị thông báo lỗi dưới ô Xác nhận mật khẩu: *"Mật khẩu xác nhận không trùng khớp"*. Ô xác nhận mật khẩu được xóa sạch để gõ lại. | |
| **TC_REG_08** | Kiểm tra đăng ký với Email đã tồn tại trên hệ thống | Đang ở màn hình Đăng ký tài khoản | 1. Nhập Email đã từng đăng ký thành công.<br>2. Điền hợp lệ các ô còn lại.<br>3. Nhấn nút "Tạo tài khoản". | • Email: `"khachhang1@gmail.com"` (I)<br>• Trường khác: Nhập đúng (V) | Hiển thị thông báo: *"Địa chỉ email này đã được sử dụng. Vui lòng chọn Đăng nhập"* kèm nút gợi ý *"Chuyển sang Đăng nhập"*. | |
| **TC_LOG_01** | Kiểm tra đăng nhập thành công (Happy Path) | Đang ở màn hình Đăng nhập | 1. Nhập Email chính xác.<br>2. Nhập Mật khẩu chính xác.<br>3. Nhấn nút "Đăng nhập". | • Email: `"khachhang1@gmail.com"` (V)<br>• Mật khẩu: `"123456"` (V) | Thông báo *"Đăng nhập thành công"*, chuyển hướng về màn hình chính và tải sẵn khung hội thoại cùng lịch sử tin nhắn trao đổi trước đó. | |
| **TC_LOG_02** | Kiểm tra đăng nhập khi để trống Mật khẩu | Đang ở màn hình Đăng nhập | 1. Nhập Email hợp lệ.<br>2. Để trống ô Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | • Email: `"khachhang1@gmail.com"` (V)<br>• Mật khẩu: `""` (I) | Báo lỗi viền đỏ ô Mật khẩu: *"Vui lòng không để trống trường thông tin này"*. | |
| **TC_LOG_03** | Kiểm tra đăng nhập với Email không tồn tại | Đang ở màn hình Đăng nhập | 1. Nhập Email chưa từng đăng ký.<br>2. Nhập Mật khẩu ngẫu nhiên.<br>3. Nhấn nút "Đăng nhập". | • Email: `"nodata_user@gmail.com"` (I)<br>• Mật khẩu: `"12345678"` | Hiển thị cảnh báo lỗi: *"Thông tin tài khoản hoặc mật khẩu không chính xác"*. | |
| **TC_LOG_04** | Kiểm tra đăng nhập vào tài khoản đang bị khóa tạm thời | Tài khoản `khachhang2@gmail.com` vừa bị khóa 15 phút do nhập sai 5 lần | 1. Nhập Email bị khóa.<br>2. Nhập đúng Mật khẩu.<br>3. Nhấn nút "Đăng nhập". | • Email: `"khachhang2@gmail.com"`<br>• Mật khẩu: `"123456"` | Hiển thị thông báo: *"Tài khoản hiện đang bị tạm khóa. Vui lòng quay lại sau hoặc liên hệ bộ phận hỗ trợ"*. | |
| **TC_LOG_05** | Kiểm tra đếm số lần nhập sai mật khẩu (Lần 1 đến lần 4) | Tài khoản `khachhang1@gmail.com` đang hoạt động bình thường | 1. Nhập Email chính xác.<br>2. Nhập Mật khẩu sai.<br>3. Nhấn nút "Đăng nhập". | • Email: `"khachhang1@gmail.com"`<br>• Mật khẩu: `"sai_mat_khau"` (I) | Báo lỗi: *"Thông tin tài khoản hoặc mật khẩu không chính xác"*. Bộ đếm đếm sai tăng thêm 1 lượt. | |
| **TC_LOG_06** | Kiểm tra tự động khóa tài khoản khi nhập sai mật khẩu 5 lần liên tiếp | Tài khoản `khachhang1@gmail.com` đã nhập sai 4 lần trước đó | 1. Nhập Email chính xác.<br>2. Nhập Mật khẩu sai lần thứ 5.<br>3. Nhấn "Đăng nhập". | • Email: `"khachhang1@gmail.com"`<br>• Mật khẩu: `"sai_mat_khau_5"` (I) | Hiển thị thông báo: *"Tài khoản hiện đang bị tạm khóa. Vui lòng quay lại sau hoặc liên hệ bộ phận hỗ trợ"*. Tài khoản chuyển sang trạng thái bị khóa 15 phút. | |

---
---

---

### Use case 1.2: Quản lý phiên trò chuyện {#uc-1-2}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Khách hàng |
| **Điều kiện bắt đầu** | 1. Khách hàng đã truy cập website PetHome và đăng nhập thành công.<br>2. Khách hàng mở khung "Tư vấn trực tuyến" ở góc màn hình. |
| **Luồng sự kiện chính (Xem danh sách và Tiếp tục cuộc trò chuyện cũ)** | 1. Khách hàng chọn nút "Lịch sử trò chuyện" trên thanh tiêu đề cửa sổ chat.<br>2. Hệ thống tải và hiển thị danh sách các phiên trò chuyện trước đây của khách hàng. Mỗi mục gồm:<br>• Thời gian tin nhắn gần nhất (ngày/tháng/năm giờ:phút).<br>• Dòng tin nhắn tóm lược gần nhất (10-15 từ đầu).<br>• Nhãn trạng thái phiên: Đang mở (giao tiếp với Bot/Nhân viên) hoặc Đã kết thúc.<br>(Trên giao diện luôn có nút "Bắt đầu cuộc trò chuyện mới". Nếu chọn, thực hiện Luồng con A-1).<br>3. Khách hàng bấm chọn cuộc trò chuyện cũ muốn tiếp tục.<br>4. Hệ thống kiểm tra tình trạng phiên trò chuyện:<br>• Nếu đã "Đã kết thúc", thực hiện luồng rẽ nhánh E-1.<br>• Nếu đang ở chế độ chờ nhân viên tư vấn tiếp quản, thực hiện luồng rẽ nhánh E-2.<br>5. Hệ thống tải nội dung trao đổi gần nhất và hiển thị đầy đủ lên khung chat.<br>6. Hệ thống cuộn màn hình xuống tin nhắn mới nhất và kích hoạt ô nhập liệu.<br>7. Đầu ra: Lịch sử trao đổi hiển thị trọn vẹn, thanh tiêu đề thể hiện rõ trạng thái kết nối với Trợ lý ảo, ô nhập sẵn sàng cho khách hàng gõ nội dung tiếp theo. |
| **Luồng con (A-1: Mở phiên trò chuyện mới)** | 1. Khách hàng bấm nút "Bắt đầu cuộc trò chuyện mới".<br>2. Hệ thống tạo một phiên trò chuyện mới độc lập, gán cho tài khoản khách hàng và kích hoạt Trợ lý ảo phục vụ.<br>3. Hệ thống làm mới khung chat và gửi câu chào tự động: "Xin chào! Mình là Trợ lý tư vấn PetHome. Bạn cần tìm thức ăn, phụ kiện, kiểm tra tồn kho hay chính sách nào hôm nay?".<br>4. Hệ thống hiển thị các nút gợi ý chủ đề (VD: "Tư vấn hạt cho chó mèo", "Chính sách đổi trả", "Kiểm tra tồn kho").<br>5. Khách hàng gõ câu hỏi hoặc bấm chọn gợi ý.<br>6. Đầu ra: Khung chat hiển thị phiên mới với lời chào và nút gợi ý thân thiện.<br>7. Use Case kết thúc thành công. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Phiên trò chuyện đã đóng/kết thúc<br>1. Hệ thống tải lịch sử tin nhắn cũ nhưng khóa ô nhập và hiển thị dải thông báo xám: "Phiên hỗ trợ này đã đóng. Bạn có thể bấm 'Bắt đầu cuộc trò chuyện mới' để được hỗ trợ tiếp."<br>2. Nếu bấm tạo mới, chuyển sang bước 2 của Luồng con A-1.<br><br>E-2: Phiên trò chuyện đang chờ nhân viên tiếp quản<br>1. Hệ thống hiển thị thông báo màu cam: "Cuộc trò chuyện đang được chuyển tiếp tới nhân viên tư vấn. Vui lòng chờ trong giây lát...".<br>2. Ô nhập văn bản vẫn mở để khách hàng gửi bổ sung tin nhắn.<br>3. Trợ lý ảo tạm ngắt phản hồi tự động trong phiên này.<br><br>E-3: Danh sách lịch sử trống (Khách hàng mới)<br>1. Hiển thị hình minh họa kèm thông báo: "Bạn chưa có cuộc trò chuyện nào trước đây." và nút "Trò chuyện ngay".<br>2. Bấm nút sẽ chuyển sang Luồng con A-1.<br><br>E-4: Mất kết nối đường truyền<br>1. Hiển thị cảnh báo: "Không thể tải nội dung do đường truyền không ổn định. Vui lòng bấm 'Thử lại'."<br>2. Bấm "Thử lại" để nạp lại nội dung. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Bảo mật lịch sử: Khách hàng chỉ được xem phiên hội thoại thuộc về tài khoản của mình.<br>2. Tải phân đoạn (Lazy Loading): Mặc định tải trước 50 tin nhắn gần nhất. Cuộn lên trên sẽ tải thêm tin nhắn cũ hơn.<br>3. Độc lập ngữ cảnh: Mỗi phiên trò chuyện mới là một luồng trao đổi độc lập.<br>4. Tự động đóng phiên: Phiên không có tương tác mới quá 24 giờ sau khi hỗ trợ sẽ tự động chuyển sang trạng thái "Đã kết thúc". |

#### **Kiểm thử hộp đen Use case 1.2: Quản lý phiên trò chuyện**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

*Khối chức năng Quản lý phiên trò chuyện không có các trường nhập liệu dạng biểu mẫu văn bản phức tạp, mà tập trung vào các hành động tương tác chọn lựa (Click) và kiểm tra dữ liệu hiển thị lịch sử.*


| Trường dữ liệu / Tương tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Danh sách cuộc trò chuyện cũ** | • Hiển thị phiên trò chuyện thuộc sở hữu của khách hàng<br>• Hiển thị thời gian tin nhắn gần nhất & dòng tóm lược (10-15 từ) | **V_CONV_01:** Danh sách có từ 1 phiên trò chuyện trở lên | **I_CONV_01:** Khách hàng mới chưa từng có phiên trò chuyện nào (Danh sách trống) | Phân vùng danh sách: 0 phiên (I), 1 phiên (V) |
| **Trạng thái phiên trò chuyện** | • Nhãn trạng thái hiển thị rõ ràng trên từng phiên | **V_STATUS_01:** Trạng thái Đang mở - Chế độ Trợ lý ảo (Bot mode)<br>**V_STATUS_02:** Trạng thái Đang mở - Chế độ Chờ tư vấn viên tiếp quản (Waiting for Agent)<br>**V_STATUS_03:** Trạng thái Đang mở - Chế độ Tư vấn viên đang hỗ trợ (Human Agent mode) | **I_STATUS_01:** Trạng thái Đã kết thúc (Closed) | Không áp dụng biên (Xác định theo tập nhãn trạng thái) |
| **Tải lịch sử tin nhắn** | • Tải phân đoạn (Lazy Loading)<br>• Tải trước 50 tin nhắn gần nhất | **V_MSG_01:** Số tin nhắn trong phiên $≤ 50$ tin<br>**V_MSG_02:** Số tin nhắn trong phiên $> 50$ tin (Tải 50 tin mới nhất, cuộn lên tải thêm) | **I_MSG_01:** Lỗi kết nối đường truyền không tải được tin nhắn | Biên số lượng tin nhắn: 50 tin nhắn (vừa đủ 1 lượt tải phân đoạn), 51 tin nhắn (kích hoạt phân trang cuộn) |

---

##### 2. Bảng quyết định (Decision Table)


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

##### 3. Sơ đồ chuyển trạng thái (State Transition Diagram)


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

##### 4. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

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

##### 5. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_CONV_01** | Kiểm tra tiếp tục cuộc trò chuyện cũ đang ở chế độ Trợ lý ảo | Đã đăng nhập, có sẵn cuộc trò chuyện đang mở với Trợ lý ảo | 1. Bấm nút "Lịch sử trò chuyện".<br>2. Chọn một cuộc trò chuyện đang mở.<br>3. Kiểm tra giao diện hiển thị. | Click chọn phiên trò chuyện mã `#102` (V) | Khung chat hiển thị trọn vẹn lịch sử tin nhắn cũ, thanh tiêu đề thể hiện kết nối với Trợ lý ảo, ô nhập văn bản sẵn sàng gõ nội dung tiếp theo. | |
| **TC_CONV_02** | Kiểm tra khởi tạo phiên trò chuyện mới (Luồng con A-1) | Đã đăng nhập, đang mở cửa sổ chat | 1. Bấm nút "Bắt đầu cuộc trò chuyện mới".<br>2. Quan sát khung chat. | Click nút "Bắt đầu cuộc trò chuyện mới" | Tạo phiên mới tinh, hiển thị lời chào tự động: *"Xin chào! Mình là Trợ lý tư vấn PetHome..."* kèm các nút gợi ý chủ đề tư vấn. | |
| **TC_CONV_03** | Kiểm tra chọn phiên trò chuyện đã kết thúc (E-1) | Đã đăng nhập, danh sách có phiên đã "Đã kết thúc" | 1. Bấm nút "Lịch sử trò chuyện".<br>2. Chọn cuộc trò chuyện có nhãn "Đã kết thúc". | Click phiên trò chuyện `#099` (Trạng thái `Closed`) | Lịch sử tin nhắn cũ được tải lên nhưng **khóa ô nhập văn bản**, hiển thị dải thông báo xám: *"Phiên hỗ trợ này đã đóng. Bạn có thể bấm 'Bắt đầu cuộc trò chuyện mới' để được hỗ trợ tiếp."* | |
| **TC_CONV_04** | Kiểm tra chọn phiên đang chờ tư vấn viên tiếp quản (E-2) | Đã đăng nhập, phiên đang ở trạng thái `Waiting for Agent` | 1. Chọn cuộc trò chuyện đang chờ nhân viên.<br>2. Quan sát dải thông báo và ô nhập. | Click phiên trò chuyện `#105` | Hiển thị thông báo màu cam: *"Cuộc trò chuyện đang được chuyển tiếp tới nhân viên tư vấn. Vui lòng chờ trong giây lát..."*. Ô nhập vẫn mở cho phép gửi thêm tin nhắn, Trợ lý ảo tạm ngắt phản hồi tự động. | |
| **TC_CONV_05** | Kiểm tra hiển thị giao diện cho khách hàng mới chưa có lịch sử (E-3) | Tài khoản khách hàng mới vừa đăng ký, chưa có tin nhắn nào | 1. Đăng nhập tài khoản mới.<br>2. Nhấp xem nút "Lịch sử trò chuyện". | Tài khoản chưa có dữ liệu | Hiển thị hình minh họa trống kèm thông báo: *"Bạn chưa có cuộc trò chuyện nào trước đây."* và nút *"Trò chuyện ngay"*. Bấm nút sẽ mở phiên chat mới. | |
| **TC_CONV_06** | Kiểm tra xử lý khi mất kết nối đường truyền (E-4) | Đã đăng nhập, thiết bị ngắt kết nối mạng | 1. Ngắt mạng thiết bị.<br>2. Bấm chọn một cuộc trò chuyện trong lịch sử. | Thao tác chọn khi không có mạng | Hiển thị cảnh báo: *"Không thể tải nội dung do đường truyền không ổn định. Vui lòng bấm 'Thử lại'."* kèm nút "Thử lại". | |
| **TC_CONV_07** | Kiểm tra tính năng tải phân đoạn 50 tin nhắn (Lazy Loading) | Phiên trò chuyện có tổng cộng 70 tin nhắn trao đổi | 1. Chọn mở cuộc trò chuyện có 70 tin nhắn.<br>2. Quan sát số tin nhắn tải đầu tiên.<br>3. Cuộn ngược màn hình chat lên trên cùng. | Cuộn trang lên trên | Ban đầu hệ thống chỉ nạp 50 tin nhắn mới nhất. Khi cuộn lên đỉnh khung chat, hệ thống tự động tải thêm 20 tin nhắn cũ hơn còn lại. | |

---
---

---

### Use case 1.3: Tư vấn sản phẩm và giải đáp chính sách tự động {#uc-1-3}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Khách hàng |
| **Điều kiện bắt đầu** | 1. Khách hàng đã mở khung trò chuyện với Trợ lý ảo PetHome.<br>2. Phiên hội thoại đang ở chế độ Trợ lý ảo (`mode == 'BOT'`).<br>3. Cơ sở dữ liệu danh mục sản phẩm, tồn kho và kho tài liệu chính sách đã sẵn sàng trên hệ thống. |
| **Luồng sự kiện chính (Tư vấn đa ý, bóc tách thuộc tính & Sinh phản hồi streaming)** | 1. Tại khung chat, khách hàng gõ câu hỏi hoặc yêu cầu tư vấn (độ dài 2 - 1000 ký tự). Câu hỏi có thể là câu đơn hoặc câu phức hợp ghép nhiều ý (VD: *"Pate Royal Canin 2kg giá bao nhiêu, chính sách freeship thế nào và shop có bán mèo Anh lông ngắn không?"*).<br>2. Khách hàng nhấn nút "Gửi" (hoặc phím Enter).<br>3. Hệ thống kiểm tra tin nhắn. Nếu rỗng hoặc chỉ có khoảng trắng, thực hiện E-1.<br>4. Hệ thống kiểm tra chế độ phiên chat. Nếu đang ở chế độ chờ/đã có nhân viên hỗ trợ (`WAITING_HUMAN` / `HUMAN`), thực hiện E-2.<br>5. Hệ thống hiển thị biểu tượng động "Trợ lý ảo đang phản hồi..." trên khung chat.<br>6. Hệ thống thực hiện quy trình xử lý thông minh qua **RAG Pipeline (Kiến trúc KH-06)**:<br>• **Phân rã câu hỏi & Nhận diện Ý định (Sub-query Decomposition & Intent Router):** Bẻ câu hỏi phức hợp thành các câu hỏi nhỏ nguyên tử, giải quyết đại từ thay thế dựa vào lịch sử chat và phân loại Intent cho từng câu hỏi nhỏ (`SQL_PRODUCT`, `VECTOR_KNOWLEDGE`, `OUT_OF_DOMAIN`, `GREETING_CHITCHAT`, `HUMAN_AGENT_REQUEST`).<br>• **Truy vấn Thông tin Sản phẩm SQL (`SQL_PRODUCT`):** Bóc tách chính xác từ khóa tên sản phẩm, danh mục, loại thú cưng và các thuộc tính linh hoạt (`brand`, `size`, `weight_volume`, `price_max/min`, `in_stock_only`) để tìm kiếm dữ liệu real-time trong CSDL sản phẩm.<br>• **Truy vấn Tri thức Chính sách Vector (`VECTOR_KNOWLEDGE`):** Tạo vector nhúng (768 chiều) và tìm kiếm ngữ nghĩa Cosine HNSW trong cơ sở dữ liệu tri thức về chính sách đổi trả, giao hàng, bảo hành và hướng dẫn chăm sóc.<br>• **Xử lý Ý định Ngoài phạm vi (`OUT_OF_DOMAIN`):** Nếu câu hỏi chứa các nội dung ngoài phạm vi kinh doanh của cửa hàng đồ dùng thú cưng (VD: hỏi mua động vật sống như chó/mèo con, dịch vụ khám bệnh thú y, thông tin xã hội...), hệ thống tự động nhận diện và đóng gói thông báo giải thích phạm vi kèm lời mời chuyển kết nối sang Nhân viên CSKH nếu cần.<br>7. **Tổng hợp & Sinh câu trả lời Streaming:** Hệ thống tổng hợp dữ liệu từ tất cả các nhánh, sinh câu trả lời tự nhiên dưới dạng luồng **gõ chữ thời gian thực (SSE Streaming)** trả về Client UI.<br>8. Bên dưới tin nhắn phản hồi, hệ thống đính kèm nút "Xem trích dẫn nguồn" (cho phép bấm vào để thực hiện Luồng con A-1).<br>9. Hệ thống tự động ghi nhận tin nhắn phản hồi và metadata trích dẫn vào lịch sử trao đổi.<br>10. Đầu ra: Câu trả lời tư vấn hiển thị rõ ràng từng đoạn theo thời gian thực; đầy đủ trích dẫn nguồn; ô nhập làm mới sẵn sàng cho câu hỏi tiếp theo. |
| **Luồng con (A-1: Xem chi tiết nguồn tài liệu trích dẫn & Mở rộng parent_content)** | 1. Khách hàng bấm nút "Xem trích dẫn nguồn" đính kèm bên dưới tin nhắn trả lời.<br>2. Hệ thống hiển thị hộp thoại thông tin (pop-up) chứa chi tiết các căn cứ tra cứu:<br>• Tên tài liệu/chính sách tham chiếu (VD: `Chinh_sach_doi_tra_PET-CS-002.md`).<br>• Vị trí tham chiếu (Mục, trang, tiêu đề phần).<br>• Đoạn trích lược ngắn (Snippet).<br>• Nội dung đầy đủ (`parent_content`): Mặc định hiển thị một phần preview; khách hàng bấm nút "Mở rộng nội dung đầy đủ" để xem toàn văn đoạn tài liệu hoặc bấm "Thu gọn" để xem lại dạng xem trước.<br>3. Khách hàng xem xong nhấn nút "Đóng" (hoặc nhấp chuột ra ngoài).<br>4. Hệ thống đóng hộp thoại và quay lại màn hình chat bình thường.<br>5. Use Case kết thúc thành công. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Bỏ trống nội dung câu hỏi<br>1. Hệ thống không gửi tin nhắn, hiển thị nhắc nhở: "Vui lòng nhập nội dung câu hỏi trước khi gửi".<br>2. Đưa con trỏ chuột về lại ô nhập liệu.<br><br>E-2: Cuộc trò chuyện đang ở chế độ Nhân viên hỗ trợ<br>1. Trợ lý ảo tạm ngắt phản hồi tự động.<br>2. Hệ thống vẫn tiếp nhận tin nhắn của khách hàng, chuyển vào danh sách chờ nhân viên đọc.<br>3. Hiển thị dải thông báo: "Nhân viên tư vấn đang tiếp nhận cuộc trò chuyện, vui lòng chờ trong giây lát...".<br><br>E-3: Câu hỏi ngoài phạm vi kinh doanh (Out of Domain)<br>1. Hệ thống nhận diện câu hỏi nằm ngoài phạm vi kinh doanh của cửa hàng Đồ dùng & Phụ kiện Thú cưng (VD: hỏi mua chó mèo sống, dịch vụ mổ thú y...).<br>2. Trợ lý ảo tự động trả lời lịch sự giải thích rõ PetHome chuyên kinh doanh sản phẩm đồ dùng/phụ kiện thú cưng nên không cung cấp mặt hàng/dịch vụ này.<br>3. Trợ lý ảo chủ động gợi ý: "Bạn có muốn kết nối với Nhân viên CSKH để được hỗ trợ chi tiết hơn không?" kèm 2 lựa chọn: "Kết nối nhân viên" và "Hỏi câu khác".<br>4. Nếu chọn "Kết nối nhân viên": Chuyển trạng thái phiên chat sang chờ nhân viên tiếp quản.<br><br>E-4: Gián đoạn kết nối đường truyền streaming<br>1. Nếu kết nối bị ngắt giữa chừng khi đang sinh câu trả lời, hiệu ứng gõ chữ dừng lại.<br>2. Hiển thị thông báo: "Đường truyền bị gián đoạn. Vui lòng bấm 'Thử lại'."<br>3. Khách hàng bấm "Thử lại", hệ thống tiến hành phát lại luồng trả lời. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Nguyên tắc phản hồi chính xác dựa trên căn cứ thực tế: Mọi câu trả lời về giá, tồn kho, thuộc tính và chính sách phải dựa trên dữ liệu thực tế từ hệ thống, không tự bịa đặt thông tin.<br>2. Trả lời trọn vẹn câu hỏi đa ý (Multi-subquery Coverage): Nếu câu hỏi chứa nhiều ý nhỏ, Trợ lý ảo phải giải đáp đầy đủ từng ý dưới dạng các mục rõ ràng.<br>3. Trải nghiệm gõ chữ thời gian thực (SSE Streaming): Phản hồi được truyền về theo cơ chế luồng ký tự liên tục.<br>4. Định dạng phản hồi trực quan (Markdown Rendering): Phản hồi từ AI Bot được trình bày chuẩn Markdown (in đậm `**văn bản**`, danh sách gạch đầu dòng `-`, ngắt dòng rõ ràng) giúp khách hàng dễ quan sát.<br>5. Hiển thị trích dẫn đầy đủ (Full Citation Parent Content): Hộp thoại trích dẫn hiển thị đoạn văn bản gốc và cung cấp tính năng "Mở rộng nội dung đầy đủ" để khách hàng xem toàn văn chính sách mà không bị khuất.<br>6. Ưu tiên con người (Human Handover): Khi phiên chuyển sang nhân viên hỗ trợ, Trợ lý ảo lập tức tắt tính năng tự trả lời.<br>7. Xử lý Out-of-Domain chuẩn mực: Không báo lỗi hệ thống cứng nhắc mà giải thích phạm vi cửa hàng và mở hướng kết nối nhân viên tư vấn. |

#### **Kiểm thử hộp đen Use case 1.3: Tư vấn sản phẩm và giải đáp chính sách tự động**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Nội dung câu hỏi** | • Bắt buộc có nội dung<br>• Độ dài 2 - 1000 ký tự<br>• Không chỉ chứa toàn khoảng trắng<br>• Có thể là câu đơn hoặc câu phức hợp nhiều ý | **V_MSG_01:** Câu hỏi hợp lệ 2 - 1000 ký tự về sản phẩm/giá/tồn kho (VD: *"Pate Royal Canin 2kg giá bao nhiêu?"*)<br>**V_MSG_02:** Câu hỏi hợp lệ về chính sách/bảo hành/đổi trả (VD: *"Shop có chính sách đổi trả hàng hư hỏng như thế nào?"*)<br>**V_MSG_03:** Câu hỏi phức hợp ghép nhiều ý (VD: *"Pate Royal Canin giá bao nhiêu và phí ship thế nào?"*) | **I_MSG_01:** Để trống không nhập gì<br>**I_MSG_02:** Chỉ nhập toàn khoảng trắng (VD: `"   "`)<br>**I_MSG_03:** Nội dung ngắn hơn 2 ký tự (VD: `"A"`)<br>**I_MSG_04:** Nội dung dài vượt quá 1000 ký tự<br>**I_MSG_05:** Câu hỏi ngoài phạm vi kinh doanh (Out of Domain - VD: *"Shop có bán mèo Anh lông ngắn không?"*, *"Dịch vụ khám bệnh thú y bao tiền?"*) | • Biên dưới độ dài: 1 ký tự (I), 2 ký tự (V), 3 ký tự (V)<br>• Biên trên độ dài: 999 ký tự (V), 1000 ký tự (V), 1001 ký tự (I) |

---

##### 2. Bảng quyết định (Decision Table)


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

##### 3. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

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

##### 4. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_RAG_01** | Kiểm tra tư vấn sản phẩm đơn lẻ thành công (Happy Path) | Khung chat ở chế độ Trợ lý ảo (`Bot mode`) | 1. Nhập câu hỏi về giá sản phẩm.<br>2. Nhấn nút "Gửi" (hoặc bấm phím Enter).<br>3. Quan sát hiệu ứng phản hồi. | Nội dung: `"Cát vệ sinh Cature 6L giá bao nhiêu?"` (V) | Hiển thị biểu tượng động Trợ lý ảo đang phản hồi, sau đó câu trả lời xuất hiện dưới dạng **luồng gõ chữ thời gian thực**. Bên dưới đính kèm nút *"Xem trích dẫn nguồn"*. | |
| **TC_RAG_02** | Kiểm tra tư vấn câu hỏi phức hợp đa ý | Khung chat ở chế độ Trợ lý ảo (`Bot mode`) | 1. Nhập câu hỏi phức hợp chứa 3 ý hỏi khác nhau.<br>2. Nhấn nút "Gửi". | Nội dung: `"Pate Royal Canin 2kg giá bao nhiêu, có sẵn hàng không và phí ship thế nào?"` (V) | Trợ lý ảo trả lời trọn vẹn đầy đủ cả 3 ý (Giá bán, Tình trạng tồn kho, Phí giao hàng) trình bày dạng danh sách gạch đầu dòng rõ ràng, ngắt đoạn trực quan. | |
| **TC_RAG_03** | Kiểm tra xem chi tiết nguồn trích dẫn & Mở rộng văn bản (Luồng con A-1) | Trợ lý ảo vừa trả lời thành công câu hỏi ở `TC_RAG_01` | 1. Bấm nút "Xem trích dẫn nguồn" dưới tin nhắn phản hồi.<br>2. Quan sát hộp thoại thông tin (pop-up).<br>3. Bấm nút "Mở rộng nội dung đầy đủ". | Click nút *"Xem trích dẫn nguồn"* $→$ Click *"Mở rộng nội dung đầy đủ"* | Hộp thoại pop-up hiển thị tên file chính sách tham chiếu, vị trí mục/trang và đoạn trích lược. Khi bấm "Mở rộng nội dung đầy đủ", đoạn văn bản chính sách xem trước được mở rộng hiển thị toàn văn không bị khuất. | |
| **TC_RAG_04** | Kiểm tra gửi nội dung chỉ có khoảng trắng (E-1) | Khung chat đang mở | 1. Nhập 5 dấu khoảng trắng vào ô chat.<br>2. Nhấn nút "Gửi". | Nội dung: `"     "` (I) | Hệ thống không gửi tin nhắn, hiển thị nhắc nhở ngay tại ô nhập: *"Vui lòng nhập nội dung câu hỏi trước khi gửi"*. Con trỏ giữ nguyên tại ô nhập. | |
| **TC_RAG_05** | Kiểm tra gửi câu hỏi khi phiên do Tư vấn viên hỗ trợ (E-2) | Phiên trò chuyện đang ở chế độ Tư vấn viên (`Human Agent mode`) | 1. Nhập câu hỏi mới.<br>2. Nhấn nút "Gửi". | Nội dung: `"Shop còn mở cửa không?"` | Trợ lý ảo **tạm ngắt phản hồi tự động**. Tin nhắn được lưu vào danh sách chờ nhân viên đọc. Hiển thị dải thông báo: *"Nhân viên tư vấn đang tiếp nhận cuộc trò chuyện, vui lòng chờ trong giây lát..."*. | |
| **TC_RAG_06** | Kiểm tra xử lý câu hỏi ngoài phạm vi kinh doanh (E-3) | Khung chat ở chế độ Trợ lý ảo (`Bot mode`) | 1. Nhập câu hỏi mua động vật sống (không thuộc mặt hàng đồ dùng thú cưng).<br>2. Nhấn nút "Gửi". | Nội dung: `"Shop có bán chó Poodle con thuần chủng không?"` (I) | Trợ lý ảo trả lời lịch sự giải thích cửa hàng PetHome chỉ chuyên kinh doanh sản phẩm đồ dùng & phụ kiện thú cưng nên không bán chó mèo sống. Đưa ra 2 gợi ý: *"Kết nối nhân viên"* và *"Hỏi câu khác"*. | |
| **TC_RAG_07** | Kiểm tra thao tác chuyển tư vấn viên khi hỏi câu ngoài phạm vi | Đang ở kết quả của `TC_RAG_06` | 1. Nhấn chọn nút "Kết nối nhân viên". | Click chọn nút *"Kết nối nhân viên"* | Trạng thái phiên chuyển sang *Chờ tư vấn viên tiếp quản (Waiting for Agent)*. Hiển thị tin nhắn thông báo chờ tư vấn viên tham gia hỗ trợ. | |
| **TC_RAG_08** | Kiểm tra xử lý gián đoạn kết nối khi đang phát phản hồi (E-4) | Trợ lý ảo đang gõ từng ký tự câu trả lời trên màn hình | 1. Ngắt kết nối mạng bất ngờ giữa chừng khi đang sinh phản hồi.<br>2. Quan sát giao diện.<br>3. Bật lại mạng và bấm nút "Thử lại". | Ngắt mạng $→$ Kết nối lại mạng | Trợ lý ảo ngừng hiệu ứng gõ chữ, hiển thị thông báo lỗi: *"Đường truyền bị gián đoạn. Vui lòng bấm 'Thử lại'."*. Khi bấm "Thử lại", luồng trả lời được tiếp tục phát lại. | |
| **TC_RAG_09** | Kiểm tra nhập câu hỏi 1 ký tự (Biên lỗi dưới) | Khung chat đang mở | 1. Gõ đúng 1 ký tự vào ô chat.<br>2. Nhấn "Gửi". | Nội dung: `"?"` (I) | Báo lỗi nhắc nhở: *"Nội dung câu hỏi phải chứa từ 2 ký tự trở lên"*. | |
| **TC_RAG_10** | Kiểm tra nhập câu hỏi 1001 ký tự (Biên lỗi trên) | Khung chat đang mở | 1. Dán một đoạn văn bản dài 1001 ký tự vào ô gõ.<br>2. Nhấn "Gửi". | Nội dung: Chuỗi văn bản 1001 ký tự (I) | Ô nhập liệu tự động chặn không cho gõ/dán vượt quá 1000 ký tự (hoặc hiển thị cảnh báo đỏ dưới ô nhập: *"Nội dung câu hỏi vượt quá độ dài tối đa 1000 ký tự"*). | |

---
---

---

### Use case 1.4: Xóa phiên trò chuyện & vô hiệu hóa Ticket liên quan {#uc-1-4}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Khách hàng |
| **Điều kiện bắt đầu** | 1. Khách hàng đã truy cập website PetHome và đăng nhập thành công.<br>2. Khách hàng mở danh sách lịch sử trò chuyện. |
| **Luồng sự kiện chính (Xóa phiên trò chuyện và vô hiệu hóa Ticket)** | 1. Tại danh sách các phiên trò chuyện, khách hàng rê chuột vào mục cuộc trò chuyện muốn xóa và bấm biểu tượng thùng rác "Xóa cuộc trò chuyện".<br>2. Hệ thống hiển thị hộp thoại xác nhận (Modal): *"Bạn có chắc chắn muốn xóa cuộc trò chuyện này? Toàn bộ tin nhắn và phiếu hỗ trợ liên quan (nếu có) sẽ bị xóa hoặc vô hiệu hóa."* kèm 2 nút "Xác nhận xóa" và "Hủy".<br>3. Nếu khách hàng chọn "Hủy", thực hiện Luồng con A-1.<br>4. Khách hàng bấm nút "Xác nhận xóa".<br>5. Hệ thống kiểm tra các Phiếu Hỗ trợ (Ticket) đang gắn liền với phiên trò chuyện này:<br>• Nếu có Ticket ở trạng thái `PENDING` hoặc `IN_PROGRESS`, hệ thống chuyển trạng thái Ticket sang `CLOSED` (Vô hiệu hóa) kèm lý do ghi nhận "Phiên hội thoại đã bị khách hàng xóa", ngắt đồng hồ SLA và gỡ Ticket khỏi hàng đợi chia việc.<br>6. Hệ thống thực hiện xóa toàn bộ lịch sử tin nhắn và xóa phiên trò chuyện khỏi cơ sở dữ liệu.<br>7. Hệ thống làm mới danh sách lịch sử trò chuyện và chuyển giao diện về trạng thái chưa chọn phiên.<br>8. Đầu ra: Dải thông báo xanh: *"Đã xóa cuộc trò chuyện thành công!"*, phiên trò chuyện biến mất khỏi lịch sử và các phiếu hỗ trợ liên quan được ghi nhận vô hiệu hóa. |
| **Luồng con (A-1: Hủy bỏ thao tác xóa)** | 1. Khách hàng bấm nút "Hủy" hoặc nhấp ra ngoài hộp thoại xác nhận.<br>2. Hệ thống đóng hộp thoại xác nhận, giữ nguyên phiên trò chuyện và các phiếu hỗ trợ liên quan mà không thay đổi bất kỳ dữ liệu nào.<br>3. Use Case kết thúc thành công. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Gián đoạn kết nối đường truyền khi xóa<br>1. Hệ thống không thực hiện xóa và hiển thị cảnh báo đỏ: "Lỗi kết nối đường truyền. Không thể xóa cuộc trò chuyện lúc này. Vui lòng thử lại!".<br>2. Giữ nguyên phiên trò chuyện và khôi phục trạng thái giao diện.<br><br>E-2: Phiên trò chuyện không tồn tại hoặc đã bị xóa trước đó<br>1. Hệ thống báo lỗi: "Phiên trò chuyện này không còn tồn tại".<br>2. Tự động làm mới danh sách lịch sử trò chuyện. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Phân quyền sở hữu: Khách hàng chỉ được phép xóa các phiên trò chuyện thuộc sở hữu của tài khoản mình.<br>2. Xác nhận bắt buộc (Confirmation Gate): Thao tác xóa bắt buộc phải đi qua bước xác nhận để tránh xóa nhầm dữ liệu.<br>3. Vô hiệu hóa Ticket đồng bộ: Khi xóa phiên chat, mọi Ticket đang phát sinh từ phiên này phải lập tức chuyển sang trạng thái vô hiệu hóa (`CLOSED`), dừng đếm ngược SLA và loại khỏi hàng đợi phân công nhân viên.<br>4. Tính không thể khôi phục: Thao tác xóa phiên trò chuyện là vĩnh viễn, toàn bộ tin nhắn liên quan không thể khôi phục sau khi xác nhận. |

#### **Kiểm thử hộp đen Use case 1.4: Xóa phiên trò chuyện & vô hiệu hóa Ticket liên quan**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Đối tượng / Thao tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Quyền sở hữu phiên trò chuyện** | • Chỉ được phép xóa phiên thuộc tài khoản của chính mình | **V_DELETE_01:** Phiên trò chuyện do chính tài khoản đang đăng nhập tạo ra | **I_DELETE_01:** Thao tác xóa phiên trò chuyện của tài khoản người dùng khác | Không áp dụng biên (Kiểm tra quyền sở hữu) |
| **Phiếu hỗ trợ (Ticket) liên quan** | • Xóa phiên chat sẽ vô hiệu hóa đồng bộ Ticket đang phát sinh từ phiên đó | **V_TICKET_01:** Phiên không có Ticket nào kèm theo<br>**V_TICKET_02:** Phiên có Ticket ở trạng thái *Chờ tiếp nhận (Pending)* hoặc *Đang xử lý (In Progress)* | **I_TICKET_01:** Ticket liên quan đã ở trạng thái *Đã kết thúc (Closed)* trước đó | Không áp dụng biên (Theo tập trạng thái Ticket) |
| **Hộp thoại xác nhận (Modal Gate)** | • Bắt buộc thông qua hộp thoại xác nhận trước khi thực hiện xóa vĩnh viễn | **V_CONFIRM_01:** Khách hàng bấm nút "Xác nhận xóa"<br>**V_CONFIRM_02:** Khách hàng bấm nút "Hủy" (hoặc nhấp ra ngoài) | **I_CONFIRM_01:** Mất kết nối đường truyền mạng đúng thời điểm bấm xác nhận | Không áp dụng biên (Lựa chọn Yes/No) |

---

##### 2. Bảng quyết định (Decision Table)


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

##### 3. Sơ đồ chuyển trạng thái (State Transition Diagram)


| Đối tượng | Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- | :--- |
| **Phiên trò chuyện** | **Đang tồn tại (Active)** | Bấm biểu tượng thùng rác $→$ Chọn "Hủy" | **Đang tồn tại (Active)** |
| **Phiên trò chuyện** | **Đang tồn tại (Active)** | Bấm biểu tượng thùng rác $→$ Chọn "Xác nhận xóa" | **Bị xóa vĩnh viễn (Deleted)** |
| **Ticket hỗ trợ** | **Chờ tiếp nhận (Pending)** | Phiên trò chuyện chứa Ticket này bị xóa | **Đã kết thúc (Closed - Vô hiệu hóa)** |
| **Ticket hỗ trợ** | **Đang xử lý (In Progress)** | Phiên trò chuyện chứa Ticket này bị xóa | **Đã kết thúc (Closed - Vô hiệu hóa)** |

---

##### 4. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 1.4 - Luồng chính** | Xóa phiên trò chuyện thông thường thành công | `TC_DEL_01` |
| **UC 1.4 - Rule 3** | Xóa phiên trò chuyện và tự động vô hiệu hóa Ticket liên quan | `TC_DEL_02` |
| **UC 1.4 - A-1** | Hủy bỏ thao tác xóa trên hộp thoại xác nhận | `TC_DEL_03` |
| **UC 1.4 - E-1** | Mất kết nối đường truyền khi đang thực hiện xóa | `TC_DEL_04` |
| **UC 1.4 - E-2** | Xóa phiên trò chuyện không còn tồn tại | `TC_DEL_05` |

---

##### 5. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DEL_01** | Kiểm tra xóa phiên trò chuyện không có Ticket đính kèm | Đang mở danh sách lịch sử trò chuyện, chọn 1 phiên thường | 1. Rê chuột vào mục cuộc trò chuyện cần xóa.<br>2. Nhấn biểu tượng thùng rác *"Xóa cuộc trò chuyện"*.<br>3. Tại hộp thoại xác nhận, bấm *"Xác nhận xóa"*. | Click nút thùng rác $→$ Click *"Xác nhận xóa"* (V) | Hộp thoại đóng lại, hiển thị dải thông báo xanh: *"Đã xóa cuộc trò chuyện thành công!"*. Phiên trò chuyện biến mất vĩnh viễn khỏi danh sách lịch sử. | |
| **TC_DEL_02** | Kiểm tra xóa phiên trò chuyện có chứa Ticket đang mở | Phiên trò chuyện `#108` đang phát sinh 1 Ticket hỗ trợ ở trạng thái *Đang xử lý (In Progress)* | 1. Thực hiện xóa phiên trò chuyện `#108`.<br>2. Bấm *"Xác nhận xóa"*. | Click *"Xác nhận xóa"* | Phiên trò chuyện bị xóa khỏi lịch sử. Ticket liên quan tự động chuyển sang trạng thái **Đã kết thúc (Closed)** kèm ghi nhận lý do *"Phiên hội thoại đã bị khách hàng xóa"*, đồng hồ SLA dừng đếm ngược và Ticket gỡ khỏi hàng đợi. | |
| **TC_DEL_03** | Kiểm tra hủy bỏ thao tác xóa cuộc trò chuyện (Luồng con A-1) | Màn hình đang hiển thị hộp thoại xác nhận xóa cuộc trò chuyện | 1. Nhấn nút "Hủy" (hoặc nhấp ra ngoài hộp thoại). | Click chọn nút *"Hủy"* | Hộp thoại xác nhận đóng lại. Phiên trò chuyện và mọi dữ liệu phiếu hỗ trợ liên quan được giữ nguyên vẹn không bị thay đổi. | |
| **TC_DEL_04** | Kiểm tra xử lý khi mất kết nối mạng lúc xóa (E-1) | Màn hình hiển thị hộp thoại xác nhận xóa, ngắt mạng thiết bị | 1. Ngắt kết nối mạng.<br>2. Bấm nút *"Xác nhận xóa"*. | Thao tác bấm khi ngắt mạng | Hệ thống không thực hiện xóa, hiển thị cảnh báo đỏ: *"Lỗi kết nối đường truyền. Không thể xóa cuộc trò chuyện lúc này. Vui lòng thử lại!"*. Phiên chat được khôi phục nguyên vẹn. | |
| **TC_DEL_05** | Kiểm tra xóa phiên trò chuyện đã bị xóa ở thiết bị/cửa sổ khác (E-2) | Phiên chat đã bị xóa ở cửa sổ trình duyệt khác trước đó vài giây | 1. Bấm nút thùng rác xóa phiên chat.<br>2. Bấm *"Xác nhận xóa"*. | Thao tác trên bản ghi đã mất | Hiển thị cảnh báo lỗi: *"Phiên trò chuyện này không còn tồn tại"*. Hệ thống tự động làm mới danh sách lịch sử trò chuyện. | |

---
*Tài liệu kiểm thử hộp đen Khối chức năng 1 được biên soạn hoàn chỉnh tuân thủ cấu trúc tài liệu mẫu `cau-truc-kiem-thu-hop-den.md` và chuẩn ngữ phong từ góc nhìn End-User.*

---

### Use case 2.1: Phân tích cảm xúc & Đánh giá nguy cơ tự động {#uc-2-1}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tên Use Case** | **Phân tích cảm xúc & Đánh giá nguy cơ tự động** |
| **Tác nhân** | Hệ thống (Tiến trình tự động) |
| **Điều kiện bắt đầu** | 1. Khách hàng vừa gửi thành công một tin nhắn văn bản mới trong phiên trò chuyện.<br><br>2. Phiên trò chuyện đang ở chế độ Trợ lý ảo tự động phục vụ (BOT mode). Nếu phiên đang do Nhân viên tiếp quản, hệ thống sẽ tự động bỏ qua tiến trình này. |
| **Luồng sự kiện chính** | 1. Hệ thống tiếp nhận nội dung tin nhắn mới từ khách hàng.<br><br>2. Hệ thống kiểm tra tính hợp lệ của văn bản: độ dài bắt buộc từ 2 đến 1000 ký tự và không chỉ chứa khoảng trắng. Nếu không hợp lệ, thực hiện Luồng rẽ nhánh E-1.<br><br>3. Hệ thống thiết lập ngữ cảnh hoàn chỉnh bằng cách kết hợp tin nhắn hiện tại với tối đa 5 tin nhắn trao đổi liền kề trước đó (tổng cộng không quá 6 tin nhắn gần nhất).<br><br>4. Hệ thống phân tích sắc thái ngữ nghĩa của toàn bộ chuỗi ngữ cảnh để tính điểm cảm xúc theo thang đo từ -1.00 đến +1.00 (quy ước làm tròn đến 2 chữ số thập phân). Nếu quá trình đánh giá gặp trục trặc hoặc quá thời gian phản hồi (vượt quá 3 giây), thực hiện E-3.<br><br>5. Hệ thống xếp loại kết quả vào 4 nhóm cảm xúc:<br><br>• **Tích cực:** Điểm từ +0.30 đến +1.00.<br><br>• **Bình thường:** Điểm từ -0.29 đến +0.29.<br><br>• **Tiêu cực nhẹ:** Điểm từ -0.59 đến -0.30.<br><br>• **Bức xúc cao:** Điểm từ -1.00 đến -0.60.<br><br>6. Hệ thống lưu kết quả điểm số và nhãn cảm xúc vào lịch sử theo dõi của phiên trò chuyện.<br><br>7. Hệ thống xác định mức độ nguy cơ sự cố:<br><br>• Nếu thuộc mức **Bức xúc cao** (-1.00 đến -0.60): Gán mức ưu tiên **P1 (Cực kỳ khẩn cấp)**.<br><br>• Nếu thuộc mức **Tiêu cực nhẹ** (-0.59 đến -0.30): Gán mức ưu tiên **P2 (Khẩn cấp cao)**.<br><br>• Nếu thuộc mức **Bình thường** hoặc **Tích cực** (lớn hơn -0.30): Đánh giá thêm ý định (Intent) của người dùng. Nếu khách có ý định gặp nhân viên hoặc hỏi ngoài phạm vi kinh doanh (Out-of-Domain), gán mức ưu tiên **P3 (Trung bình)**. Nếu không, thực hiện E-2.<br><br>8. Hệ thống bật cờ cảnh báo đỏ cho phiên trò chuyện (đối với P1, P2), đồng thời chuyển tiếp dữ liệu sự cố sang **Use Case 2.2 (Trích xuất thông tin và khởi tạo ticket khẩn cấp)**.<br><br>9. **Đầu ra:** Phiên trò chuyện được cập nhật điểm cảm xúc mới; đối với P1/P2, cờ cảnh báo đỏ được kích hoạt và đưa cuộc trò chuyện lên danh sách ưu tiên trên màn hình làm việc của nhân viên trực ca. |
| **Luồng con** | Không có. |
| **Luồng rẽ nhánh (Ngoại lệ)** | **E-1: Tin nhắn không hợp lệ**<br><br>1. Tin nhắn rỗng, chỉ chứa khoảng trắng hoặc không đạt độ dài quy định (ít hơn 2 ký tự hoặc dài hơn 1000 ký tự).<br><br>2. Hệ thống bỏ qua, không chấm điểm cảm xúc và giữ nguyên trạng thái hiện tại của phiên hội thoại.<br><br><br>**E-2: Điểm cảm xúc ở mức an toàn (Không chạm ngưỡng nguy cơ)**<br><br>1. Hệ thống ghi nhận điểm cảm xúc bình thường vào lịch sử phiên trò chuyện.<br><br>2. Nếu phiên trò chuyện trước đó đã có cờ cảnh báo đỏ, hệ thống duy trì cờ đỏ (tuyệt đối không tự động hạ cảnh báo).<br><br>3. Tiến trình kết thúc.<br><br><br>**E-3: Sự cố quá trình phân tích ngữ nghĩa**<br><br>1. Tiến trình phân tích gặp lỗi hoặc vượt quá thời gian phản hồi cho phép (quá 3 giây).<br><br>2. Hệ thống ghi nhận điểm cảm xúc mặc định là 0.00 (Bình thường) để đảm bảo không làm gián đoạn cuộc hội thoại của khách hàng.<br><br>3. Ghi nhận lỗi vào nhật ký theo dõi và kết thúc tiến trình. |
| **Quy tắc Nghiệp vụ (Business Rules)** | 1. **Phạm vi giám sát:** Chỉ thực hiện đánh giá cảm xúc đối với các tin nhắn do Khách hàng gửi đến.<br><br>2. **Đánh giá theo ngữ cảnh:** Bắt buộc kết hợp cửa sổ ngữ cảnh tối đa 6 tin nhắn gần nhất nhằm nhận diện chính xác các câu trả lời ngắn hoặc câu có đại từ thay thế.<br><br>3. **Nguyên tắc duy trì cờ đỏ:** Cờ cảnh báo đỏ một khi đã bật chỉ được gỡ bỏ khi có nhân viên tư vấn tiếp nhận phiên hoặc yêu cầu hỗ trợ liên quan được đóng.<br><br>4. **Ngưỡng kích hoạt cảnh báo:** Mọi điểm số từ -0.30 trở xuống đều bắt buộc phải kích hoạt cờ cảnh báo đỏ và chuyển sang quy trình xử lý khẩn cấp. |

#### **Kiểm thử hộp đen Use case 2.1: Phân tích cảm xúc & Đánh giá nguy cơ tự động**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Trường dữ liệu / Chỉ số | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Độ dài tin nhắn khách gửi** | • Bắt buộc từ 2 - 1000 ký tự<br>• Không chỉ chứa toàn khoảng trắng | **V_MSG_01:** Chuỗi tin nhắn hợp lệ có độ dài từ 2 - 1000 ký tự | **I_MSG_01:** Để trống không nhập gì<br>**I_MSG_02:** Chỉ chứa toàn khoảng trắng<br>**I_MSG_03:** Ngắn hơn 2 ký tự (1 ký tự)<br>**I_MSG_04:** Dài vượt quá 1000 ký tự | • Biên dưới: 1 ký tự (I), 2 ký tự (V), 3 ký tự (V)<br>• Biên trên: 999 ký tự (V), 1000 ký tự (V), 1001 ký tự (I) |
| **Thang điểm cảm xúc tin nhắn** *(Do hệ thống đánh giá ngầm)* | • Thang điểm từ -1.00 đến +1.00<br>• Quy ước làm tròn 2 chữ số thập phân | **V_SENT_01:** Điểm Bức xúc cao: [-1.00 đến -0.60]<br>**V_SENT_02:** Điểm Tiêu cực nhẹ: [-0.59 đến -0.30]<br>**V_SENT_03:** Điểm Bình thường: [-0.29 đến +0.29]<br>**V_SENT_04:** Điểm Tích cực: [+0.30 đến +1.00] | **I_SENT_01:** Hệ thống phân tích gặp sự cố / Quá thời gian phản hồi (vượt quá 3 giây) $→$ Ghi nhận điểm mặc định 0.00 (Bình thường) | • Mốc ranh giới P1: -1.00 (V), -0.60 (V), -0.59 (V)<br>• Mốc ranh giới P2: -0.59 (V), -0.30 (V), -0.29 (V)<br>• Mốc an toàn: +1.00 (V) |
| **Trạng thái cờ cảnh báo đỏ (is_flagged)** | • Tự động bật cờ đỏ khi điểm cảm xúc $≤ -0.30$ | **V_FLAG_01:** Bật cờ cảnh báo đỏ khi điểm cảm xúc đạt mốc P1 hoặc P2 ($≤ -0.30$) | **I_FLAG_01:** Điểm cảm xúc an toàn ($> -0.30$) và chưa từng bị cờ đỏ $→$ Giữ trạng thái bình thường | Không áp dụng biên (Cờ bật/tắt) |

---

##### 2. Bảng quyết định (Decision Table)


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

---

### Use case 2.2: Khởi tạo phiếu hỗ trợ khẩn cấp và chuyển giao CSKH {#uc-2-2}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tên Use Case** | **Khởi tạo phiếu hỗ trợ khẩn cấp và chuyển giao CSKH** |
| **Tác nhân** | Hệ thống (Tiến trình tự động) |
| **Điều kiện bắt đầu** | 1. Phiên trò chuyện được gán mức ưu tiên P1/P2/P3 từ UC 2.1 HOẶC nhận được yêu cầu kết nối nhân viên trực tiếp từ Khách hàng thông qua Khối 1.<br><br>2. Thông tin lịch sử tin nhắn đã được lưu trữ đầy đủ. |
| **Luồng sự kiện chính** | 1. Hệ thống tiếp nhận tín hiệu yêu cầu hỗ trợ từ phiên trò chuyện kèm theo mức độ ưu tiên (P1, P2 hoặc P3).<br><br>2. Hệ thống kiểm tra: Nếu phiên trò chuyện chưa có Phiếu Hỗ trợ nào đang ở trạng thái "Chờ tiếp nhận" hoặc "Đang xử lý", tiếp tục bước 3. Nếu đã có, thực hiện Luồng con A-1.<br><br>3. Hệ thống phân tích nội dung cuộc trò chuyện để tự động trích xuất các thông tin cốt lõi bao gồm: Tóm tắt sự cố (20-255 ký tự) và Danh mục khiếu nại (VD: Lỗi đơn hàng, Đổi trả/Hoàn tiền, Thái độ phục vụ...). Nếu trích xuất thất bại, thực hiện E-1.<br><br>4. Hệ thống thiết lập thời hạn cam kết xử lý (SLA) đếm ngược dựa trên mức độ ưu tiên:<br>• **P1:** Bắt buộc xử lý trong vòng 15 phút.<br>• **P2:** Bắt buộc xử lý trong vòng 60 phút.<br>• **P3:** Bắt buộc xử lý trong vòng 240 phút.<br><br>5. Hệ thống sinh ra một Phiếu Hỗ trợ mới với trạng thái "Chờ tiếp nhận" và đưa vào hàng đợi của bộ phận CSKH.<br><br>6. Hệ thống kiểm tra mức độ ưu tiên: Nếu là P2, Trợ lý ảo vẫn tiếp tục duy trì hội thoại để hỗ trợ khách hàng trong khi phiếu hỗ trợ được gửi ngầm đến hàng đợi. Nếu là P1 hoặc P3, thực hiện tiếp bước 7.<br><br>7. Đối với sự cố P1 hoặc yêu cầu P3, hệ thống thay đổi trạng thái của phiên trò chuyện sang "Chờ nhân viên hỗ trợ".<br><br>8. Hệ thống phản hồi tức thời cho khách hàng tùy theo ngữ cảnh:<br>• **Đối với P1:** Gửi thông báo xoa dịu khẩn cấp: *"Mình rất xin lỗi về trải nghiệm này. Hệ thống đã đánh dấu yêu cầu khẩn cấp và nhân viên CSKH đang vào hỗ trợ bạn ngay lập tức."*<br>• **Đối với P3:** Gửi thông báo chờ lịch sự: *"Hệ thống đã ghi nhận yêu cầu của bạn, tư vấn viên sẽ phản hồi bạn trong thời gian sớm nhất."*<br><br>9. Hệ thống chính thức vô hiệu hóa tính năng tự động trả lời (Bot) cho phiên trò chuyện đối với P1 và P3.<br><br>10. **Đầu ra:** Phiếu hỗ trợ mới hiển thị trên bảng công việc của nhân viên trực ca kèm đồng hồ SLA đếm ngược. Khách hàng nhận được thông báo chuyển máy phù hợp mà không bị ngắt quãng. |
| **Luồng con** | **A-1: Cập nhật phiếu hỗ trợ hiện có**<br><br>1. Hệ thống phát hiện đã có sẵn một Phiếu Hỗ trợ chưa đóng.<br><br>2. Hệ thống thêm nội dung phàn nàn mới vào phần nhật ký của phiếu hiện tại.<br><br>3. Hệ thống so sánh mức độ: Nếu mức độ ưu tiên mới cao hơn mức cũ (ví dụ từ P2 tăng lên P1), hệ thống cập nhật lại mức ưu tiên thành P1 và đặt lại đồng hồ đếm ngược SLA xuống còn 15 phút.<br><br>4. Chuyển tiếp sang Bước 6 của luồng chính. |
| **Luồng rẽ nhánh (Ngoại lệ)** | **E-1: Sự cố trích xuất thông tin**<br><br>1. Quá trình trích xuất thông tin bị lỗi hoặc không xác định được danh mục.<br><br>2. Hệ thống tạo phiếu với thông tin mặc định: Tóm tắt "Cần kiểm tra thủ công - Lỗi trích xuất" và Danh mục "Vấn đề khác".<br><br>3. Tiếp tục Bước 4 của luồng chính.<br><br><br>**E-2: Lỗi kết nối cơ sở dữ liệu**<br><br>1. Việc lưu Phiếu Hỗ trợ thất bại do lỗi hệ thống.<br><br>2. Hệ thống lưu tạm yêu cầu vào danh sách chờ và tự động thử tạo lại (retry) định kỳ mỗi 1 phút cho đến khi thành công.<br><br><br>**E-3: Phiên trò chuyện bị xóa / Ticket bị vô hiệu hóa**<br><br>1. Nếu khách hàng thực hiện xóa phiên trò chuyện trong lúc hệ thống đang tự động trích xuất hoặc cập nhật phiếu hỗ trợ, tiến trình tự động hủy tác vụ ngầm.<br><br>2. Hệ thống đánh dấu Phiếu Hỗ trợ sang trạng thái `CLOSED` (Vô hiệu hóa) kèm lý do "Phiên hội thoại đã bị khách hàng xóa", loại phiếu khỏi danh sách chờ phân công. |
| **Quy tắc Nghiệp vụ (Business Rules)** | 1. **Chống trùng lặp:** Tuyệt đối không tạo nhiều phiếu hỗ trợ cho cùng một phiên trò chuyện tại cùng một thời điểm. Mọi khiếu nại phát sinh thêm phải được gom vào phiếu đang mở.<br><br>2. **Đảm bảo trải nghiệm (Graceful Handover):** Khi chuyển sang trạng thái "Chờ nhân viên" (P1), hệ thống bắt buộc phải gửi xong câu xoa dịu trước khi ngắt tính năng trả lời tự động, tránh việc khách hàng bị bỏ rơi đột ngột.<br><br>3. **Vô hiệu hóa ticket khi xóa phiên:** Nếu phiên trò chuyện bị xóa, ticket liên quan lập tức ngắt tiến trình tự động và chuyển sang trạng thái vô hiệu hóa (`CLOSED`). |

#### **Kiểm thử hộp đen Use case 2.2: Khởi tạo phiếu hỗ trợ khẩn cấp và chuyển giao CSKH**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Trường dữ liệu / Chỉ số | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Đoạn tóm tắt sự cố (Summary)** | • Do hệ thống tự động trích xuất từ 1-10 tin nhắn gần nhất<br>• Độ dài bắt buộc từ 20 đến 255 ký tự | **V_SUM_01:** Chuỗi tóm tắt trích xuất hợp lệ 20 - 255 ký tự | **I_SUM_01:** Trích xuất thất bại / Lỗi nội dung $→$ Ghi nhận tóm tắt mặc định: *"Cần kiểm tra thủ công - Lỗi trích xuất tự động"* (E-1) | • Biên dưới: 19 ký tự (I), 20 ký tự (V), 21 ký tự (V)<br>• Biên trên: 254 ký tự (V), 255 ký tự (V), 256 ký tự (I) |
| **Danh mục khiếu nại (Category)** | • Thuộc 1 trong 6 danh mục chuẩn hóa của cửa hàng | **V_CAT_01:** Thuộc danh mục: `Lỗi đơn hàng`, `Đổi trả/Hoàn tiền`, `Sản phẩm lỗi/Hư hại`, `Lỗi thanh toán`, `Thái độ phục vụ` | **I_CAT_01:** Trích xuất không xác định được danh mục $→$ Ghi nhận danh mục mặc định: *"Vấn đề khác"* (E-1) | Tập hợp 6 danh mục chuẩn hóa |
| **Mức độ ưu tiên & Hạn chót SLA** | • Phân loại P1, P2, P3 với thời hạn đếm ngược cam kết xử lý tương ứng | **V_SLA_01:** Mức P1 (Cực kỳ khẩn cấp) - SLA đếm ngược đúng **15 phút**<br>**V_SLA_02:** Mức P2 (Khẩn cấp cao) - SLA đếm ngược đúng **60 phút**<br>**V_SLA_03:** Mức P3 (Trung bình) - SLA đếm ngược đúng **240 phút** | **I_SLA_01:** Không xác định mức ưu tiên | • Mốc SLA P1: Đúng 15 phút (900 giây)<br>• Mốc SLA P2: Đúng 60 phút (3600 giây)<br>• Mốc SLA P3: Đúng 240 phút (14400 giây) |
| **Kiểm tra Ticket trùng lặp** | • Mỗi phiên trò chuyện tại một thời điểm chỉ tồn tại tối đa 1 Ticket chưa đóng | **V_TKT_01:** Phiên trò chuyện chưa có Ticket nào ở trạng thái Chờ tiếp nhận/Đang xử lý $→$ Tạo Ticket mới | **I_TKT_01:** Phiên đã có sẵn 1 Ticket chưa đóng $→$ Thực hiện gom nội dung phàn nàn mới vào Ticket cũ, không tạo trùng (Luồng con A-1) | Không áp dụng biên (Có / Chưa có Ticket mở) |

---

##### 2. Bảng quyết định (Decision Table)


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

##### 3. Sơ đồ chuyển trạng thái (State Transition Diagram)


| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- |
| **Khởi tạo mới (New)** | Hệ thống phát hiện sự cố P1/P2/P3 từ cuộc trò chuyện | **Chờ tiếp nhận (Pending)** *(Gán đồng hồ SLA đếm ngược)* |
| **Chờ tiếp nhận (Pending)** | Sự cố có diễn biến khẩn cấp hơn (Khách chửi gắt hơn từ P2 lên P1) | **Chờ tiếp nhận (Pending)** *(Đặt lại SLA 15 phút)* |
| **Chờ tiếp nhận (Pending)** | Tư vấn viên CSKH nhấn "Tiếp quản cuộc trò chuyện" | **Đang xử lý (In Progress)** |
| **Đang xử lý (In Progress)** | Tư vấn viên nhập nội dung giải quyết và bấm "Hoàn tất" | **Đã giải quyết (Resolved)** |
| **Chờ tiếp nhận / Đang xử lý** | Khách hàng thực hiện xóa phiên trò chuyện (UC 1.4) | **Đã kết thúc (Closed - Vô hiệu hóa)** |

---
---

---

### Use case 2.3: Cấu hình quy tắc phân loại sự cố và cảnh báo {#uc-2-3}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tên Use Case** | **Cấu hình quy tắc phân loại sự cố và cảnh báo** |
| **Tác nhân** | Quản lý CSKH / Quản trị viên |
| **Điều kiện bắt đầu** | 1. Người dùng đã đăng nhập thành công vào hệ thống với vai trò Quản lý (Manager) hoặc Quản trị viên (Admin).<br><br>2. Người dùng truy cập vào trang "Cấu hình Quy tắc Cảnh báo". |
| **Luồng sự kiện chính** | 1. Hệ thống hiển thị giao diện cấu hình bao gồm các thông số: Hướng dẫn phân loại sự cố (văn bản tự do), Ngưỡng điểm kích hoạt mức P1, Ngưỡng điểm kích hoạt mức P2.<br><br>2. Người dùng chọn chức năng chỉnh sửa và nhập/cập nhật nội dung hướng dẫn nghiệp vụ bằng ngôn ngữ tự nhiên (Ví dụ: "Nếu khách hàng phản ánh sai kích thước sản phẩm hoặc gửi sai mẫu mã, bắt buộc phân loại vào P1").<br><br>3. Người dùng điều chỉnh các mốc ngưỡng điểm cảm xúc nếu có nhu cầu.<br><br>4. Người dùng xác nhận và nhấn nút "Lưu thay đổi".<br><br>5. Hệ thống kiểm tra tính hợp lệ của dữ liệu đầu vào. Nếu dữ liệu không hợp lệ, thực hiện E-1.<br><br>6. Hệ thống lưu trữ các quy tắc cấu hình mới vào cơ sở dữ liệu.<br><br>7. Hệ thống tự động triển khai tức thời các quy tắc mới vào hệ thống phân tích ở Use Case 2.1.<br><br>8. **Đầu ra:** Giao diện hiển thị thông báo "Cập nhật cấu hình thành công". Mọi tin nhắn tiếp theo của khách hàng sẽ được hệ thống phân tích dựa trên bộ quy tắc mới nhất này. |
| **Luồng con** | **A-1: Hủy bỏ thay đổi**<br><br>1. Tại bất kỳ thời điểm nào trước khi lưu, người dùng nhấn nút "Hủy" hoặc điều hướng sang trang khác.<br><br>2. Hệ thống hiển thị cảnh báo xác nhận (nếu có thay đổi chưa lưu).<br><br>3. Người dùng đồng ý hủy, hệ thống không ghi nhận bất kỳ thay đổi nào và khôi phục dữ liệu hiển thị về trạng thái lưu gần nhất. |
| **Luồng rẽ nhánh (Ngoại lệ)** | **E-1: Thông tin cấu hình không hợp lệ**<br><br>1. Hệ thống phát hiện các lỗi như: Bỏ trống hướng dẫn phân loại, ngưỡng điểm cấu hình không phải là số âm, hoặc điểm kích hoạt P1 không nhỏ hơn điểm kích hoạt P2 (ví dụ -0.60 phải nhỏ hơn -0.30).<br><br>2. Hệ thống chặn thao tác lưu và hiển thị cảnh báo màu đỏ ngay dưới trường dữ liệu bị lỗi.<br><br>3. Người dùng phải chỉnh sửa lại dữ liệu cho hợp lệ để tiếp tục thao tác lưu. |
| **Quy tắc Nghiệp vụ (Business Rules)** | 1. **Phân quyền truy cập:** Nhân viên tư vấn thông thường (Agent) không có quyền xem hoặc chỉnh sửa trang cấu hình này.<br><br>2. **Tính linh hoạt ngôn ngữ (Dynamic Prompting):** Hệ thống phải có khả năng hiểu và áp dụng các hướng dẫn nghiệp vụ được viết bằng ngôn ngữ tự nhiên thay vì bắt buộc người dùng nhập danh sách từ khóa cứng nhắc (hardcode).<br><br>3. **Hiệu lực tức thời:** Bất kỳ thay đổi cấu hình nào sau khi lưu thành công phải lập tức có tác dụng đối với toàn bộ các phiên trò chuyện đang diễn ra, không yêu cầu khởi động lại hệ thống. |

#### **Kiểm thử hộp đen Use case 2.3: Cấu hình quy tắc phân loại sự cố và cảnh báo**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Ngưỡng điểm kích hoạt P1 (p1_threshold)** | • Bắt buộc là số âm trong đoạn [-1.00, 0.00]<br>• Bắt buộc phải nhỏ hơn Ngưỡng điểm P2 | **V_P1_01:** Số âm trong khoảng [-1.00 đến < p2_threshold] (VD: `-0.60`) | **I_P1_01:** Để trống không nhập<br>**I_P1_02:** Số dương (VD: `0.50`)<br>**I_P1_03:** Nhỏ hơn -1.00 (VD: `-1.50`)<br>**I_P1_04:** Lớn hơn hoặc bằng Ngưỡng điểm P2 (VD: `-0.20` khi P2 là `-0.30`) | • Biên dưới: -1.00 (V), -1.01 (I)<br>• Cận biên P2: `p2_threshold - 0.01` (V), `p2_threshold` (I) |
| **Ngưỡng điểm kích hoạt P2 (p2_threshold)** | • Bắt buộc là số âm trong đoạn [-1.00, 0.00]<br>• Bắt buộc phải lớn hơn Ngưỡng điểm P1 | **V_P2_01:** Số âm trong khoảng [> p1_threshold đến 0.00] (VD: `-0.30`) | **I_P2_01:** Để trống không nhập<br>**I_P2_02:** Số dương (VD: `0.20`)<br>**I_P2_03:** Nhỏ hơn hoặc bằng Ngưỡng điểm P1 (VD: `-0.70` khi P1 là `-0.60`) | • Biên trên: 0.00 (V), 0.01 (I)<br>• Cận biên P1: `p1_threshold + 0.01` (V), `p1_threshold` (I) |
| **Hướng dẫn nghiệp vụ bằng ngôn ngữ tự nhiên** | • Văn bản hướng dẫn tự do giải thích quy tắc phân loại | **V_PROMPT_01:** Đoạn văn bản mô tả nghiệp vụ (VD: *"Nếu khách phản ánh sai mẫu mã sản phẩm, phân loại vào P1"*) | **I_PROMPT_01:** Để trống không nhập hướng dẫn | Phân vùng chuỗi có dữ liệu / để trống |
| **Quyền truy cập màn hình cấu hình** | • Chỉ dành riêng cho vai trò Quản lý (Manager) hoặc Quản trị viên (Admin) | **V_AUTH_01:** Đăng nhập với tài khoản có vai trò Quản lý / Admin | **I_AUTH_01:** Đăng nhập với tài khoản Nhân viên tư vấn (Agent) $→$ Chặn truy cập | Phân quyền truy cập |

---

##### 2. Bảng quyết định (Decision Table)


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


| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 2.1 - Luồng chính** | Đánh giá tin nhắn tiêu cực nhẹ (P2) & Bức xúc cao (P1) | `TC_AUC_01`, `TC_AUC_02` |
| **UC 2.1 - E-1** | Bỏ qua phân tích tin nhắn rỗng / khoảng trắng / 1 ký tự | `TC_AUC_03` |
| **UC 2.1 - E-2** | Điểm cảm xúc bình thường / tích cực (Không chạm ngưỡng nguy cơ) | `TC_AUC_04` |
| **UC 2.1 - E-3** | Sự cố tiến trình phân tích bị quá 3 giây (Fallback về 0.00) | `TC_AUC_05` |
| **UC 2.1 - Rule 3** | Quy tắc duy trì cờ đỏ (Không tự động gỡ cờ đỏ khi khách hạ giận) | `TC_AUC_06` |
| **UC 2.2 - Luồng chính** | Khởi tạo Phiếu hỗ trợ P1 khẩn cấp (SLA 15m) & P2 (SLA 60m) | `TC_AUC_07`, `TC_AUC_08` |
| **UC 2.2 - A-1** | Gom khiếu nại mới vào Ticket cũ & Nâng priority lên P1 nếu gắt hơn | `TC_AUC_09` |
| **UC 2.2 - E-1** | Sự cố trích xuất thông tin $→$ Tạo Ticket với thông tin mặc định | `TC_AUC_10` |
| **UC 2.2 - E-3** | Vô hiệu hóa Ticket (Closed) khi phiên trò chuyện bị khách xóa | `TC_AUC_11` |
| **UC 2.3 - Luồng chính** | Quản lý cập nhật bộ quy tắc cấu hình thành công | `TC_AUC_12` |
| **UC 2.3 - E-1** | Lỗi nhập ngưỡng điểm P1 lớn hơn hoặc bằng P2 | `TC_AUC_13` |
| **UC 2.3 - Rule 1** | Chặn nhân viên tư vấn (Agent) truy cập trang cấu hình | `TC_AUC_14` |

---
---



| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_AUC_01** | Kiểm tra phân tích tin nhắn thuộc mức Bức xúc cao P1 (Happy Path) | Khu vực chat ở chế độ Trợ lý ảo, ngưỡng P1 là `-0.60` | 1. Nhập tin nhắn thể hiện sự giận dữ gắt gao.<br>2. Nhấn nút "Gửi".<br>3. Quan sát phản hồi và giao diện. | Nội dung: `"Shop lừa đảo, chuyển tiền xong không thấy giao hàng, làm ăn như rác rưởi!"` (V) | Hệ thống đánh giá điểm cảm xúc $≤ -0.60$ (`CRITICAL`), bật cờ cảnh báo đỏ trên phiên trò chuyện, ngắt phản hồi tự động của AI Bot và gửi câu xin lỗi xoa dịu. Cuộc trò chuyện đưa lên vị trí ưu tiên hàng đợi. | Pass |
| **TC_AUC_02** | Kiểm tra phân tích tin nhắn thuộc mức Tiêu cực nhẹ P2 | Cấu hình ngưỡng P2 là `-0.30` | 1. Nhập tin nhắn phàn nàn nhẹ.<br>2. Nhấn nút "Gửi". | Nội dung: `"Giao hàng chậm quá shop ơi, đợi mãi không thấy đâu chán ghê."` (V) | Điểm cảm xúc xếp mức Tiêu cực nhẹ (`NEGATIVE`), bật cờ cảnh báo đỏ, tự động khởi tạo ngầm phiếu hỗ trợ P2. Trợ lý ảo **vẫn tiếp tục duy trì trả lời tự động** cho khách. | Pass |
| **TC_AUC_03** | Kiểm tra gửi tin nhắn 1 ký tự (Bỏ qua phân tích - E-1) | Đang ở cửa sổ chat với Trợ lý ảo | 1. Gõ 1 ký tự duy nhất.<br>2. Nhấn nút "Gửi". | Nội dung: `"A"` (I) | Khung chat báo lỗi nhắc nhở: *"Nội dung câu hỏi phải chứa từ 2 ký tự trở lên"*. Tiến trình không chấm điểm cảm xúc, giữ nguyên trạng thái phiên chat. | Pass |
| **TC_AUC_04** | Kiểm tra gửi tin nhắn khen ngợi tích cực (E-2) | Khung chat đang ở trạng thái bình thường | 1. Nhập tin nhắn khen dịch vụ.<br>2. Nhấn nút "Gửi". | Nội dung: `"Shop giao hàng siêu nhanh, nhân viên tư vấn nhiệt tình lắm!"` (V) | Đánh giá điểm cảm xúc Tích cực (`POSITIVE`), ghi nhận lịch sử phiên chat. Không bật cờ cảnh báo đỏ, AI Bot tiếp tục hỗ trợ bình thường. | Pass |
| **TC_AUC_05** | Kiểm tra xử lý sự cố tiến trình phân tích quá 3 giây (E-3) | Hệ thống nghẽn mạng / Phân tích phản hồi chậm | 1. Gửi một tin nhắn bất kỳ.<br>2. Giả lập tiến trình phân tích phản hồi vượt quá 3 giây. | Nội dung: `"Tôi muốn hỏi về đơn hàng"` | Tiến trình tự động ghi nhận điểm cảm xúc mặc định là `0.00` (Bình thường). Cuộc hội thoại của khách hàng không bị ngắt quãng hay báo lỗi crash. | Pass |
| **TC_AUC_06** | Kiểm tra quy tắc duy trì cờ đỏ khi khách nói câu tích cực tiếp theo | Phiên trò chuyện đã bị bật cờ đỏ ở `TC_AUC_01` trước đó | 1. Khách hàng gửi tiếp một tin nhắn ngắn có thái độ nguội bớt.<br>2. Quan sát cờ cảnh báo đỏ trên giao diện. | Nội dung: `"Dạ vâng shop kiểm tra giúp em"` | Hệ thống ghi nhận điểm cảm xúc tin mới, nhưng **tuyệt đối không tự động gỡ cờ đỏ** của phiên trò chuyện. Cờ đỏ tiếp tục duy trì cho tới khi tư vấn viên vào tiếp quản. | Pass |

---


| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_AUC_07** | Kiểm tra khởi tạo Phiếu hỗ trợ khẩn cấp P1 (SLA 15 phút) | Phiên trò chuyện vừa phát sinh sự cố Bức xúc cao P1 | 1. Quan sát bảng công việc của nhân viên CSKH.<br>2. Kiểm tra thông tin phiếu hỗ trợ mới đẻ ra. | Tín hiệu chuyển từ `TC_AUC_01` | Một Phiếu hỗ trợ mới xuất hiện ở trạng thái *Chờ tiếp nhận (Pending)*, danh mục khiếu nại và tóm tắt sự cố được tự động điền đầy đủ. Đồng hồ SLA đếm ngược đúng **15 phút**. | Pass |
| **TC_AUC_08** | Kiểm tra khởi tạo Phiếu hỗ trợ P2 (SLA 60 phút) | Phiên trò chuyện phát sinh phàn nàn P2 | 1. Quan sát danh sách hàng đợi công việc. | Tín hiệu từ `TC_AUC_02` | Phiếu hỗ trợ mới được tạo ra ngầm với mức ưu tiên P2, trạng thái *Chờ tiếp nhận (Pending)* và đồng hồ SLA đếm ngược đúng **60 phút**. | Pass |
| **TC_AUC_09** | Kiểm tra leo thang sự cố và nâng SLA từ P2 lên P1 (Luồng con A-1) | Phiên chat đã có sẵn 1 Ticket P2 chưa đóng từ `TC_AUC_08` | 1. Khách hàng gửi tiếp 1 tin nhắn chửi bới gắt gao thuộc cấp P1.<br>2. Kiểm tra phiếu hỗ trợ hiện tại trên màn hình nhân viên. | Nội dung: `"Tôi sẽ báo công an nếu không xử lý ngay!"` | Hệ thống **không tạo trùng Ticket mới**, mà gom tin nhắn mới vào Ticket P2 cũ, tự động nâng mức ưu tiên của Ticket cũ lên **P1** và reset đồng hồ SLA đếm ngược về **15 phút**. | Pass |
| **TC_AUC_10** | Kiểm tra khởi tạo Ticket với thông tin mặc định khi lỗi trích xuất (E-1) | Tiến trình tự động trích xuất nội dung bị gián đoạn/lỗi | 1. Phát tín hiệu tạo Ticket khi trích xuất thông tin thất bại. | Dữ liệu trích xuất rỗng / lỗi | Tạo Phiếu hỗ trợ khẩn cấp với thông tin mặc định: Tóm tắt sự cố là *"Cần kiểm tra thủ công - Lỗi trích xuất tự động"* và Danh mục là *"Vấn đề khác"*. Đồng hồ SLA đếm ngược 60 phút. | Pass |
| **TC_AUC_11** | Kiểm tra tự động vô hiệu hóa Ticket khi khách xóa phiên chat (E-3) | Có 1 Ticket P1 đang ở trạng thái *Chờ tiếp nhận (Pending)* | 1. Khách hàng thực hiện xóa phiên trò chuyện (UC 1.4).<br>2. Kiểm tra thẻ Ticket trên bảng công việc nhân viên. | Thao tác Xóa phiên trò chuyện | Ticket liên quan lập tức tự động chuyển sang trạng thái **Đã kết thúc (Closed - Vô hiệu hóa)** với lý do *"Phiên hội thoại đã bị khách hàng xóa"*, ngắt đồng hồ SLA và gỡ khỏi hàng đợi phân công. | Pass |

---


| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_AUC_12** | Kiểm tra Quản lý cập nhật quy tắc cấu hình thành công (Happy Path) | Đăng nhập tài khoản Quản lý (Manager), đang ở trang "Cấu hình Cảnh báo" | 1. Nhập Ngưỡng P1 hợp lệ.<br>2. Nhập Ngưỡng P2 hợp lệ.<br>3. Nhập văn bản Hướng dẫn nghiệp vụ.<br>4. Bấm nút "Lưu thay đổi". | • P1: `-0.70` (V)<br>• P2: `-0.35` (V)<br>• Hướng dẫn: `"Ưu tiên P1 cho lỗi thanh toán"` | Hiển thị thông báo xanh: *"Cập nhật cấu hình thành công"*. Mọi tin nhắn tiếp theo của khách hàng được phân tích dựa trên bộ quy tắc mới này ngay lập tức. | Pass |
| **TC_AUC_13** | Kiểm tra báo lỗi khi nhập Ngưỡng P1 lớn hơn P2 (E-1) | Đang ở trang "Cấu hình Cảnh báo" | 1. Nhập Ngưỡng P1 lớn hơn P2.<br>2. Bấm nút "Lưu thay đổi". | • P1: `-0.20` (I)<br>• P2: `-0.50` (V) | Thao tác lưu bị chặn, hiển thị thông báo lỗi màu đỏ ngay dưới ô nhập: *"Điểm kích hoạt P1 phải nhỏ hơn điểm kích hoạt P2"*. | Pass |
| **TC_AUC_14** | Kiểm tra chặn Nhân viên tư vấn (Agent) truy cập trang cấu hình | Đăng nhập tài khoản Nhân viên tư vấn (`agent.an@brand.com`) | 1. Cố gắng điều hướng truy cập vào đường dẫn trang Cấu hình Quy tắc. | Điều hướng trang Cấu hình | Hệ thống chặn truy cập, hiển thị thông báo lỗi: *"Bạn không có quyền truy cập trang cấu hình này"* và chuyển hướng về màn hình Bàn làm việc CSKH. | Pass |

---
*Tài liệu kiểm thử hộp đen Khối chức năng 2 đã được chuẩn hóa trọn vẹn 100%, bổ sung đầy đủ EP/BVA, Decision Table, State Transition, RTM và bộ 14 Test Cases chuẩn IEEE.*

---

### Use case 3.1: Quản lý tài khoản nhân viên {#uc-3-1}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Nhân viên CSKH / Quản trị viên |
| **Điều kiện bắt đầu** | 1. Người dùng mở trang Cổng thông tin nội bộ chuỗi cửa hàng PetHome.<br>2. Kết nối mạng ổn định. |
| **Luồng sự kiện chính (Đăng ký tài khoản nhân viên mới)** | 1. Người dùng chọn "Đăng ký tài khoản nhân sự" trên màn hình quản trị nội bộ.<br>2. Hệ thống hiển thị biểu mẫu bao gồm:<br>• Họ và tên: Bắt buộc (2-100 ký tự).<br>• Email nội bộ: Bắt buộc (VD: nhanvien@pethome.vn).<br>• Số điện thoại: Tùy chọn (10 chữ số bắt đầu bằng 0).<br>• Vai trò: Agent, Manager, hoặc Admin.<br>• Kỹ năng chuyên môn: Đánh dấu danh mục xử lý (Đổi trả, Giao hàng, Tư vấn sản phẩm, Khiếu nại).<br>• Mật khẩu & Xác nhận mật khẩu: Bắt buộc (tối thiểu 8 ký tự, gồm cả chữ và số).<br>(Có sẵn liên kết "Đã có tài khoản? Đăng nhập ngay" -> Luồng con A-1).<br>3. Điền đầy đủ thông tin.<br>4. Nhấn nút "Tạo tài khoản nhân sự".<br>5. Kiểm tra trường bắt buộc. Nếu để trống, thực hiện E-1.<br>6. Kiểm tra định dạng. Nếu sai, thực hiện E-2.<br>7. Kiểm tra mật khẩu xác nhận. Nếu sai, thực hiện E-3.<br>8. Kiểm tra sự tồn tại của email. Nếu trùng, thực hiện E-4.<br>9. Lưu tài khoản mới với trạng thái mặc định Ngoại tuyến (OFFLINE).<br>10. Đầu ra: Thông báo "Tạo tài khoản nhân viên thành công!", làm mới biểu mẫu và cập nhật danh sách nhân sự. |
| **Luồng con (A-1: Đăng nhập Bàn làm việc CSKH)** | 1. Nhấp liên kết "Đăng nhập ngay".<br>2. Hiển thị biểu mẫu Đăng nhập (Email nội bộ, Mật khẩu).<br>3. Nhập thông tin và bấm "Đăng nhập".<br>4. Nếu để trống, thực hiện E-1.<br>5. Nếu tài khoản bị khóa, thực hiện E-5.<br>6. Nếu sai thông tin đăng nhập, thực hiện E-6.<br>7. Khởi tạo phiên làm việc an toàn.<br>8. Đầu ra: Chuyển hướng vào giao diện Bàn làm việc CSKH (Live Support Console) với trạng thái mặc định OFFLINE.<br>9. Use Case kết thúc thành công. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Bỏ trống trường thông tin bắt buộc<br>1. Khoanh đỏ ô trống và báo lỗi: "Vui lòng không để trống trường thông tin này".<br><br>E-2: Định dạng dữ liệu không hợp lệ<br>1. Hiển thị thông báo lỗi cụ thể tại ô vi phạm.<br><br>E-3: Mật khẩu xác nhận không khớp<br>1. Báo lỗi: "Mật khẩu xác nhận không trùng khớp".<br><br>E-4: Email đã tồn tại<br>1. Báo lỗi: "Địa chỉ email này đã được sử dụng".<br><br>E-5: Tài khoản đang bị khóa<br>1. Hiển thị cảnh báo: "Tài khoản hiện đang bị khóa hoặc ngừng kích hoạt".<br><br>E-6: Thông tin đăng nhập không chính xác<br>1. Báo lỗi: "Địa chỉ email hoặc mật khẩu không chính xác". |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Tính duy nhất: Mỗi nhân viên sở hữu 1 email nội bộ duy nhất.<br>2. Ràng buộc chuyên môn: Tạo tài khoản Agent bắt buộc chọn ít nhất 1 danh mục kỹ năng xử lý.<br>3. Trạng thái ban đầu: Đăng nhập thành công luôn ở trạng thái OFFLINE.<br>4. Thời hạn phiên: Phiên làm việc có hiệu lực tối đa 24 giờ. |

#### **Kiểm thử hộp đen Use case 3.1: Quản lý tài khoản nhân viên**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Họ và tên** *(Tạo tài khoản)* | • Bắt buộc<br>• Độ dài 2 - 100 ký tự | **V_NAME_01:** Chuỗi chữ hợp lệ từ 2 - 100 ký tự (VD: `"Nguyễn Văn Bình"`) | **I_NAME_01:** Để trống<br>**I_NAME_02:** Ngắn hơn 2 ký tự (1 ký tự)<br>**I_NAME_03:** Dài hơn 100 ký tự | • Biên dưới: 1 ký tự (I), 2 ký tự (V), 3 ký tự (V)<br>• Biên trên: 99 ký tự (V), 100 ký tự (V), 101 ký tự (I) |
| **Email nội bộ** *(Tạo tài khoản / Đăng nhập)* | • Bắt buộc<br>• Đúng định dạng email nội bộ (`ten@domain.com`)<br>• Tối đa 255 ký tự<br>• Duy nhất trên hệ thống | **V_EMAIL_01:** Email nội bộ hợp lệ, chưa tồn tại trên hệ thống (VD: `"agent.binh@brand.com"`) | **I_EMAIL_01:** Để trống<br>**I_EMAIL_02:** Sai cấu trúc định dạng email<br>**I_EMAIL_03:** Email vượt quá 255 ký tự<br>**I_EMAIL_04:** Email đã tồn tại trên hệ thống | • Biên trên độ dài: 255 ký tự (V), 256 ký tự (I)<br>• Kiểm tra trùng lặp email đã có |
| **Số điện thoại** *(Tạo tài khoản)* | • Tùy chọn (Không bắt buộc)<br>• Nếu nhập: Đủ 10 chữ số, bắt đầu bằng số `0` | **V_PHONE_01:** Để trống không nhập<br>**V_PHONE_02:** Đủ 10 chữ số bắt đầu bằng số `0` (VD: `"0987654321"`) | **I_PHONE_01:** Ít hơn 10 chữ số<br>**I_PHONE_02:** Nhiều hơn 10 chữ số<br>**I_PHONE_03:** Không bắt đầu bằng số `0`<br>**I_PHONE_04:** Chứa chữ cái/ký tự đặc biệt | • Biên độ dài: 9 chữ số (I), 10 chữ số bắt đầu số `0` (V), 11 chữ số (I) |
| **Mật khẩu** *(Tạo tài khoản / Đăng nhập)* | • Bắt buộc<br>• Tối thiểu 8 ký tự trở lên<br>• Chứa ít nhất 1 chữ cái và 1 chữ số | **V_PASS_01:** Mật khẩu $≥ 8$ ký tự, chứa đủ chữ và số (VD: `"Agent1234"`)| **I_PASS_01:** Để trống<br>**I_PASS_02:** Ngắn hơn 8 ký tự (7 ký tự)<br>**I_PASS_03:** Chỉ chứa chữ cái, thiếu số<br>**I_PASS_04:** Chỉ chứa chữ số, thiếu chữ | • Biên độ dài: 7 ký tự (I), 8 ký tự (V), 9 ký tự (V) |
| **Kỹ năng chuyên môn** *(Dành cho Agent)* | • Bắt buộc đối với tài khoản vai trò Agent: Phải chọn ít nhất 1 danh mục kỹ năng | **V_SKILL_01:** Chọn từ 1 danh mục kỹ năng trở lên (VD: `["Đổi trả", "Giao hàng"]`) | **I_SKILL_01:** Tạo tài khoản vai trò Agent nhưng không tích chọn kỹ năng nào (0 kỹ năng) | Biên số lượng kỹ năng chọn: 0 kỹ năng (I), 1 kỹ năng (V) |
| **Quyền khởi tạo tài khoản** | • Chỉ dành cho tài khoản có vai trò Quản lý (Manager) hoặc Quản trị viên (Admin) | **V_AUTH_01:** Đăng nhập với tài khoản Quản lý / Admin để tạo tài khoản nhân sự mới | **I_AUTH_01:** Đăng nhập với tài khoản Agent thông thường | Phân quyền thao tác |

---

##### 2. Bảng quyết định (Decision Table)


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

##### 3. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

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

##### 4. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_01** | Kiểm tra Quản lý tạo tài khoản nhân viên mới thành công (Happy Path) | Đăng nhập tài khoản Quản lý, đang ở màn hình Quản lý nhân sự | 1. Nhập Họ tên hợp lệ.<br>2. Nhập Email nội bộ mới.<br>3. Nhập SĐT hợp lệ.<br>4. Chọn Vai trò là Agent.<br>5. Chọn 2 Kỹ năng chuyên môn.<br>6. Nhập Mật khẩu hợp lệ.<br>7. Bấm nút "Tạo tài khoản nhân sự". | • Họ tên: `"Nguyễn Văn Bình"` (V)<br>• Email: `"agent.binh@brand.com"` (V)<br>• SĐT: `"0987654321"` (V)<br>• Vai trò: Agent<br>• Kỹ năng: `["Đổi trả", "Giao hàng"]`<br>• Mật khẩu: `"Agent1234"` | Thông báo xanh: *"Tạo tài khoản nhân viên thành công!"*, làm mới biểu mẫu và tài khoản mới xuất hiện trong danh sách ở trạng thái Ngoại tuyến (OFFLINE). | Pass |
| **TC_LCS_02** | Kiểm tra tạo tài khoản khi để trống Email | Đang ở màn hình Tạo tài khoản nhân sự | 1. Để trống ô Email.<br>2. Điền hợp lệ các ô còn lại.<br>3. Bấm "Tạo tài khoản nhân sự". | • Email: `""` (I)<br>• Các ô khác: Nhập đúng V | Viền ô Email hằn đỏ, hiển thị thông báo lỗi ngay bên dưới: *"Vui lòng không để trống trường thông tin này"*. | Pass |
| **TC_LCS_03** | Kiểm tra tạo tài khoản với Mật khẩu 7 ký tự (Biên lỗi) | Đang ở màn hình Tạo tài khoản nhân sự | 1. Nhập Mật khẩu 7 ký tự.<br>2. Điền hợp lệ các ô còn lại.<br>3. Bấm "Tạo tài khoản nhân sự". | • Mật khẩu: `"Agent12"` (I)<br>• Các ô khác: Nhập đúng V | Báo lỗi dưới ô Mật khẩu: *"Mật khẩu tối thiểu 8 ký tự gồm chữ và số"*. | Pass |
| **TC_LCS_04** | Kiểm tra tạo tài khoản với Email đã tồn tại | Đang ở màn hình Tạo tài khoản nhân sự | 1. Nhập Email đã có trên hệ thống.<br>2. Điền hợp lệ các ô còn lại.<br>3. Bấm "Tạo tài khoản nhân sự". | • Email: `"agent.an@brand.com"` (I)<br>• Các ô khác: Nhập đúng V | Hiển thị cảnh báo lỗi: *"Địa chỉ email này đã được sử dụng"*. | Pass |
| **TC_LCS_05** | Kiểm tra tạo tài khoản Agent nhưng không chọn kỹ năng nào | Đang ở màn hình Tạo tài khoản nhân sự | 1. Chọn Vai trò là Agent.<br>2. Không tích chọn kỹ năng nào.<br>3. Bấm "Tạo tài khoản nhân sự". | • Vai trò: Agent<br>• Kỹ năng: Không chọn (0 kỹ năng) (I) | Báo lỗi màu đỏ: *"Tạo tài khoản Nhân viên tư vấn bắt buộc chọn ít nhất 1 danh mục kỹ năng xử lý"*. | Pass |
| **TC_LCS_06** | Kiểm tra Đăng nhập Bàn làm việc CSKH thành công | Đang ở màn hình Đăng nhập nội bộ | 1. Nhập Email nội bộ chính xác.<br>2. Nhập Mật khẩu chính xác.<br>3. Nhấn nút "Đăng nhập". | • Email: `"agent.an@brand.com"` (V)<br>• Mật khẩu: `"123456"` (V) | Chuyển hướng thành công vào giao diện Bàn làm việc CSKH (Live Support Console) với trạng thái mặc định ban đầu là Ngoại tuyến (OFFLINE). | Pass |
| **TC_LCS_07** | Kiểm tra Đăng nhập vào tài khoản nhân viên đang bị khóa | Tài khoản `agent.binh@brand.com` bị khóa | 1. Nhập Email nhân viên bị khóa.<br>2. Nhập đúng Mật khẩu.<br>3. Bấm "Đăng nhập". | • Email: `"agent.binh@brand.com"`<br>• Mật khẩu: `"123456"` | Hiển thị cảnh báo: *"Tài khoản hiện đang bị khóa hoặc ngừng kích hoạt"*. | Pass |
| **TC_LCS_08** | Kiểm tra Đăng nhập sai Mật khẩu | Đang ở màn hình Đăng nhập nội bộ | 1. Nhập Email chính xác.<br>2. Nhập Mật khẩu sai.<br>3. Bấm "Đăng nhập". | • Email: `"agent.an@brand.com"`<br>• Mật khẩu: `"sai_mat_khau"` (I) | Báo lỗi: *"Địa chỉ email hoặc mật khẩu không chính xác"*. | Pass |

---

### Use case 3.2: Quản lý trạng thái làm việc của nhân viên {#uc-3-2}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Nhân viên CSKH |
| **Điều kiện bắt đầu** | 1. Nhân viên đã đăng nhập Bàn làm việc CSKH (Live Support Console).<br>2. Duy trì kết nối mạng thời gian thực tới hệ thống. |
| **Luồng sự kiện chính (Chuyển đổi trạng thái làm việc)** | 1. Nhân viên nhấp chọn thanh trạng thái ở góc trên bên phải màn hình.<br>2. Hệ thống hiển thị danh sách 3 trạng thái:<br>• Trực tuyến (ONLINE): Chấm xanh; sẵn sàng tiếp nhận cuộc trò chuyện mới và nhận phân công ticket.<br>• Bận (BUSY): Chấm cam; tạm dừng phân công việc mới (đang xử lý khiếu nại khó/nghỉ giải lao).<br>• Ngoại tuyến (OFFLINE): Chấm xám; kết thúc ca trực.<br>3. Nhân viên chọn trạng thái muốn chuyển (VD: chuyển từ OFFLINE sang ONLINE).<br>4. Hệ thống kiểm tra kết nối thời gian thực. Nếu mất mạng, thực hiện E-1.<br>5. Ghi nhận và đồng bộ trạng thái mới toàn hệ thống.<br>6. Nếu chuyển sang ONLINE, kích hoạt tiếp nhận thông báo cuộc trò chuyện và phân công ticket tự động.<br>7. Đầu ra: Đổi màu chỉ thị trạng thái và hiển thị thông báo: "Đã chuyển sang trạng thái Trực tuyến - Bạn đã sẵn sàng tiếp nhận hỗ trợ!". |
| **Luồng con** | Không có. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Gián đoạn kết nối thời gian thực<br>1. Hệ thống tự động chuyển chỉ thị trạng thái sang màu xám (OFFLINE) để tránh gán nhầm việc khi nhân viên rớt mạng.<br>2. Hiển thị dải cảnh báo màu cam: "Đang mất kết nối thời gian thực. Hệ thống đang tự động kết nối lại...".<br>3. Khi có mạng trở lại, dải cảnh báo tự biến mất và nhân viên có thể chọn lại trạng thái. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Tiêu chí sẵn sàng nhận việc: Chỉ nhân viên ở trạng thái ONLINE mới được hệ thống phân công ticket tự động.<br>2. Ý nghĩa trạng thái BUSY: Tạm dừng gán việc mới nhưng nhân viên vẫn tiếp tục xử lý các công việc đã nhận trước đó.<br>3. Đồng bộ tức thời: Trạng thái được cập nhật lập tức tới bộ máy điều phối công việc mà không có độ trễ. |

#### **Kiểm thử hộp đen Use case 3.2: Quản lý trạng thái làm việc của nhân viên**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Trường dữ liệu / Thao tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Trạng thái làm việc (Status)** | • Thuộc 1 trong 3 trạng thái chuẩn hóa | **V_STT_01:** Trạng thái Trực tuyến (`ONLINE`) - Chấm xanh<br>**V_STT_02:** Trạng thái Bận (`BUSY`) - Chấm cam<br>**V_STT_03:** Trạng thái Ngoại tuyến (`OFFLINE`) - Chấm xám | **I_STT_01:** Trạng thái không thuộc tập hợp quy định (VD: Rỗng) | Tập hợp 3 trạng thái chuẩn hóa |
| **Đường truyền mạng thời gian thực** | • Duy trì kết nối đường truyền liên tục | **V_NET_01:** Đường truyền mạng kết nối ổn định | **I_NET_01:** Đường truyền bị ngắt kết nối quá 30 giây (E-1) | Mốc thời gian ngắt kết nối: 29 giây (vẫn giữ trạng thái), 30 giây (chuyển tự động `OFFLINE`) |

---

##### 2. Bảng quyết định (Decision Table)


*(Tiền đề quy trình: Nhân viên nhấp chọn một trạng thái trên thanh chỉ thị trạng thái)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 |
| :--- | :---: | :---: | :---: |
| **C1: Đã đăng nhập tài khoản nhân viên hợp lệ?** | F | T | T |
| **C2: Đường truyền mạng thời gian thực ổn định (không mất mạng > 30s)?** | - | F | T |
| **H1: Chặn thao tác, chuyển hướng về trang Đăng nhập** | X | | |
| **H2: Tự động đổi chỉ thị sang màu xám (OFFLINE) & Hiện dải cảnh báo cam (E-1)** | | X | |
| **H3: Cập nhật màu chỉ thị, đồng bộ trạng thái mới & kích hoạt nhận việc (nếu ONLINE)** | | | X |

---

##### 3. Sơ đồ chuyển trạng thái (State Transition Diagram)


| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- |
| **Ngoại tuyến (OFFLINE)** | Nhân viên chọn trạng thái "Trực tuyến" | **Trực tuyến (ONLINE)** *(Kích hoạt tự động nhận việc)* |
| **Trực tuyến (ONLINE)** | Nhân viên chọn trạng thái "Bận" | **Bận (BUSY)** *(Tạm dừng phân công việc mới)* |
| **Bận (BUSY)** | Nhân viên chọn trạng thái "Trực tuyến" | **Trực tuyến (ONLINE)** |
| **Trực tuyến (ONLINE) / Bận (BUSY)** | Mất kết nối đường truyền mạng quá 30 giây | **Ngoại tuyến (OFFLINE)** *(Tự động chuyển ngầm)* |
| **Ngoại tuyến (OFFLINE)** | Đường truyền mạng kết nối trở lại | **Trực tuyến / Bận** *(Khôi phục chọn trạng thái)* |

---
---

##### 4. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 3.2 - Luồng chính** | Chuyển đổi trạng thái làm việc (ONLINE / BUSY / OFFLINE) | `TC_LCS_09`, `TC_LCS_10` |
| **UC 3.2 - E-1** | Mất kết nối đường truyền mạng quá 30 giây (Tự động đổi OFFLINE) | `TC_LCS_11` |

##### 5. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_09** | Kiểm tra chuyển trạng thái từ OFFLINE sang ONLINE (Happy Path) | Đã đăng nhập Live Console, trạng thái đang là OFFLINE (Chấm xám) | 1. Nhấp chọn thanh trạng thái ở góc trên bên phải.<br>2. Chọn trạng thái "Trực tuyến" (ONLINE). | Click chọn "Trực tuyến" (V) | Nút chỉ thị chuyển sang **màu xanh lá (ONLINE)**, hiển thị thông báo: *"Đã chuyển sang trạng thái Trực tuyến - Bạn đã sẵn sàng tiếp nhận hỗ trợ!"*. Kích hoạt tự động nhận phân công ticket. | Pass |
| **TC_LCS_10** | Kiểm tra chuyển trạng thái từ ONLINE sang BUSY | Trạng thái hiện tại đang là ONLINE | 1. Nhấp thanh trạng thái.<br>2. Chọn trạng thái "Bận" (BUSY). | Click chọn "Bận" (V) | Nút chỉ thị chuyển sang **màu cam (BUSY)**, thông báo chuyển trạng thái thành công. Tạm dừng phân công ticket mới nhưng vẫn giữ các việc đang xử lý. | Pass |
| **TC_LCS_11** | Kiểm tra tự động đổi trạng thái sang OFFLINE khi mất mạng > 30s (E-1) | Đã đăng nhập, trạng thái đang là ONLINE | 1. Ngắt kết nối mạng thiết bị.<br>2. Quan sát nút chỉ thị sau 30 giây. | Ngắt mạng 30 giây | Nút chỉ thị trạng thái tự động đổi sang **màu xám (OFFLINE)**. Hiển thị dải cảnh báo cam: *"Đang mất kết nối thời gian thực. Hệ thống đang tự động kết nối lại..."*. | Pass |

---

### Use case 3.3: Theo dõi hàng đợi và tiếp quản cuộc trò chuyện {#uc-3-3}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Nhân viên CSKH (Khách hàng cùng tương tác) |
| **Điều kiện bắt đầu** | 1. Nhân viên đăng nhập thành công Bàn làm việc CSKH.<br>2. Trạng thái nhân viên ở chế độ ONLINE.<br>3. Cuộc trò chuyện của khách hàng đang ở chế độ Trợ lý ảo hoặc danh sách chờ hỗ trợ (bật cờ đỏ/khách yêu cầu gặp tư vấn viên). |
| **Luồng sự kiện chính (Tiếp quản cuộc trò chuyện & Nhắn tin hai chiều)** | 1. Nhân viên theo dõi danh sách hàng đợi bên trái màn hình và chọn phiên trò chuyện cần hỗ trợ.<br>2. Hệ thống tải toàn bộ lịch sử trao đổi cũ, bản tóm tắt sự cố và điểm cảm xúc khách hàng lên khung hiển thị.<br>3. Nhân viên kiểm tra và bấm nút "Tiếp quản cuộc trò chuyện".<br>4. Nếu cuộc trò chuyện đã được nhân viên khác bấm nhận trước đó ít giây, thực hiện E-1.<br>5. Hệ thống xác nhận quyền tiếp quản cho nhân viên hiện tại, tự động gỡ cờ đỏ trên hàng đợi và ngắt chế độ trả lời tự động của Trợ lý ảo trong phiên này.<br>6. Hệ thống gửi thông báo tự động vào khung chat khách hàng: "Nhân viên tư vấn đã tham gia cuộc trò chuyện".<br>7. Mở khóa ô nhập tin nhắn cho nhân viên.<br>8. Nhân viên gõ nội dung tư vấn (1-4000 ký tự).<br>9. Nhấn nút "Gửi" (hoặc phím Enter).<br>10. Nếu để trống, thực hiện E-2.<br>11. Nếu mất kết nối mạng thời gian thực khi gửi, thực hiện E-3.<br>12. Lưu tin nhắn với `sender_type = 'AGENT'` và hiển thị ngay tức thì sang màn hình khách hàng.<br>13. Hai bên nhắn tin tương tác thời gian thực cho đến khi hoàn tất hỗ trợ.<br>14. Đầu ra: Thẻ cuộc trò chuyện trên hàng đợi chuyển sang "Đang hỗ trợ", tin nhắn hai chiều hiển thị mượt mà không độ trễ. |
| **Luồng con** | Không có. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Phiên trò chuyện đã được nhân viên khác tiếp quản trước<br>1. Hệ thống báo lỗi: "Cuộc trò chuyện này đã được nhân viên [Họ tên] tiếp quản".<br>2. Tự động chuyển màn hình của nhân viên hiện tại sang chế độ "Chỉ xem" và ẩn nút tiếp quản.<br><br>E-2: Nội dung tin nhắn gửi đi bị rỗng<br>1. Nút Gửi bị mờ và hiển thị nhắc nhở: "Vui lòng nhập nội dung tin nhắn trước khi gửi".<br><br>E-3: Gián đoạn kết nối mạng thời gian thực<br>1. Tin nhắn xuất hiện biểu tượng đỏ kèm nút "Thử gửi lại" và cảnh báo mất kết nối.<br>2. Khi có mạng trở lại, bấm "Thử gửi lại" để phát lại tin nhắn.<br><br>E-4: Phiên trò chuyện bị xóa khi đang tiếp quản hoặc đang chat<br>1. Nếu khách hàng xóa cuộc trò chuyện trong lúc nhân viên đang mở màn hình chat hoặc chuẩn bị tiếp quản, hệ thống gửi thông báo WebSocket `CONVERSATION_DELETED`.<br>2. Ẩn nút gửi tin nhắn và hiển thị dải thông báo xám: "Cuộc trò chuyện này đã bị khách hàng xóa. Phiếu hỗ trợ tương ứng đã chuyển sang trạng thái vô hiệu hóa."<br>3. Tự động gỡ thẻ phiên trò chuyện khỏi hàng đợi làm việc của nhân viên. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Chống xung đột hỗ trợ: Mỗi cuộc trò chuyện tại một thời điểm chỉ cho phép 1 nhân viên chính thức tiếp quản.<br>2. Ngắt hoàn toàn Bot AI: Khi nhân viên tiếp quản thành công, Trợ lý ảo lập tức tắt tính năng tự động trả lời.<br>3. Minh bạch lịch sử: Toàn bộ tin nhắn trao đổi được lưu trữ chính xác theo thời gian kèm định danh nhân viên.<br>4. Tự động cuộn trang: Khung chat ở cả 2 phía tự động cuộn xuống dòng mới nhất khi có tin nhắn mới.<br>5. Xử lý phiên bị xóa: Khi cuộc trò chuyện bị khách hàng xóa, thẻ hàng đợi của nhân viên sẽ tự động đóng và dọn dẹp khỏi màn hình làm việc thời gian thực. |

#### **Kiểm thử hộp đen Use case 3.3: Theo dõi hàng đợi và tiếp quản cuộc trò chuyện**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Thao tác / Trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Tiếp quản cuộc trò chuyện (Takeover)** | • Chỉ cho phép tiếp quản phiên chat chưa có nhân viên nào nhận | **V_TK_01:** Bấm "Tiếp quản" cuộc trò chuyện chưa có nhân viên phụ trách | **I_TK_01:** Bấm "Tiếp quản" cuộc trò chuyện đã bị nhân viên khác nhận trước đó vài giây (E-1) | Xung đột tranh chấp tiếp quản |
| **Nội dung tin nhắn tư vấn** | • Bắt buộc từ 1 - 4000 ký tự | **V_MSG_01:** Chuỗi tin nhắn tư vấn từ 1 - 4000 ký tự | **I_MSG_01:** Để trống không nhập tin nhắn<br>**I_MSG_02:** Tin nhắn dài vượt quá 4000 ký tự | • Biên dưới: 0 ký tự (I), 1 ký tự (V), 2 ký tự (V)<br>• Biên trên: 3999 ký tự (V), 4000 ký tự (V), 4001 ký tự (I) |
| **Quyền gửi tin nhắn (Ghi)** | • Chỉ nhân viên đã tiếp quản mới được gửi tin nhắn vào phiên chat | **V_WRITE_01:** Nhân viên đã tiếp quản phiên chat gửi tin nhắn | **I_WRITE_01:** Nhân viên khác chưa tiếp quản cố tình gửi tin nhắn vào phiên của người khác | Màn hình ở chế độ Chỉ xem (Read-only) |

---

##### 2. Bảng quyết định (Decision Table)


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

##### 3. Sơ đồ chuyển trạng thái (State Transition Diagram)


| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- |
| **Chờ tư vấn viên (Waiting for Agent)** | Nhân viên A bấm nút "Tiếp quản cuộc trò chuyện" thành công | **Tư vấn viên A đang hỗ trợ (Human Agent mode)** |
| **Chờ tư vấn viên (Waiting for Agent)** | Nhân viên B bấm tiếp quản khi Nhân viên A đã bấm nhận trước | **Chế độ Chỉ xem đối với Nhân viên B (Read-only)** |
| **Tư vấn viên A đang hỗ trợ** | Nhân viên A bấm "Kết thúc hỗ trợ" | **Đã kết thúc (Closed)** |

---
---

##### 4. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 3.3 - Luồng chính** | Tiếp quản cuộc trò chuyện & Nhắn tin 2 chiều thời gian thực | `TC_LCS_12`, `TC_LCS_13` |
| **UC 3.3 - E-1** | Xung đột tiếp quản (Người khác bấm trước) → Chế độ Chỉ xem | `TC_LCS_14` |
| **UC 3.3 - E-2** | Để trống tin nhắn tư vấn hoặc vượt quá 4000 ký tự | `TC_LCS_15` |

##### 5. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_12** | Kiểm tra tiếp quản cuộc trò chuyện thành công (Happy Path) | Trạng thái ONLINE, hàng đợi có 1 phiên chat màu đỏ đang chờ hỗ trợ | 1. Nhấn chọn phiên chat cần hỗ trợ.<br>2. Bấm nút "Tiếp quản cuộc trò chuyện". | Click nút "Tiếp quản cuộc trò chuyện" (V) | Xác nhận quyền tiếp quản, tự động gỡ cờ đỏ, ngắt trả lời của Bot AI và gửi thông báo tự động vào chat khách hàng: *"Nhân viên tư vấn đã tham gia cuộc trò chuyện"*. Mở khóa ô nhập cho nhân viên. | Pass |
| **TC_LCS_13** | Kiểm tra nhắn tin 2 chiều thời gian thực | Nhân viên đã tiếp quản thành công ở `TC_LCS_12` | 1. Nhập nội dung tư vấn vào ô chat.<br>2. Nhấn nút "Gửi" (hoặc phím Enter). | Nội dung: `"Chào bạn, mình là An tư vấn viên PetHome. Mình có thể hỗ trợ gì cho bạn ạ?"` (V) | Tin nhắn tư vấn hiển thị lập tức sang khung chat của khách hàng với vai trò Nhân viên tư vấn. | Pass |
| **TC_LCS_14** | Kiểm tra xung đột tiếp quản khi người khác nhận trước (E-1) | Phiên chat `#105` đang chờ hỗ trợ | 1. Nhân viên A chuẩn bị bấm tiếp quản.<br>2. Nhân viên B bấm tiếp quản trước 1 giây.<br>3. Nhân viên A bấm tiếp quản ngay sau đó. | Thao tác bấm sau | Báo lỗi: *"Cuộc trò chuyện đã được nhận bởi nhân viên khác"*. Đặt màn hình của Nhân viên A về **Chế độ Chỉ xem (Read-only)**, khóa ô nhập tin nhắn. | Pass |
| **TC_LCS_15** | Kiểm tra gửi tin nhắn rỗng (E-2) | Nhân viên đang ở khung chat đã tiếp quản | 1. Để trống ô nhập tin nhắn.<br>2. Nhấn nút "Gửi". | Nội dung: `""` (I) | Nút gửi không kích hoạt (hoặc báo nhắc nhở: *"Vui lòng nhập nội dung tin nhắn tư vấn"*). | Pass |

---

### Use case 3.4: Quản lý và sử dụng mẫu phản hồi nhanh {#uc-3-4}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Nhân viên CSKH, Quản lý CSKH |
| **Điều kiện bắt đầu** | 1. Người dùng đăng nhập tài khoản Nhân viên hoặc Quản lý.<br>2. Kết nối mạng ổn định. |
| **Luồng sự kiện chính (Tìm kiếm và chèn nhanh mẫu câu)** | 1. Tại ô nhập tin nhắn, nhân viên gõ ký tự `/`.<br>2. Hệ thống hiển thị bảng gợi ý các mẫu phản hồi (Phím tắt, Tiêu đề, Danh mục).<br>3. Nhân viên gõ từ khóa phím tắt (VD: `/chao`, `/xloi`, `/doitra`) hoặc phím mũi tên để duyệt.<br>(Nếu cần tạo thêm mẫu câu mới, thực hiện Luồng con A-1).<br>4. Nếu từ khóa không khớp mẫu nào, thực hiện E-1.<br>5. Nhân viên bấm phím Enter hoặc nhấp chọn mẫu câu.<br>6. Hệ thống tự động điền văn bản mẫu vào ô soạn thảo.<br>7. Nhân viên đọc lại, chỉnh sửa thêm chi tiết và bấm "Gửi".<br>8. Đầu ra: Tin nhắn mẫu chuẩn mực được gửi ngay tới khung chat khách hàng. |
| **Luồng con (A-1: Khởi tạo mẫu phản hồi mới vào kho dữ liệu)** | 1. Quản lý hoặc Nhân viên truy cập "Cài đặt mẫu phản hồi nhanh".<br>2. Bấm nút "Thêm mẫu câu mới".<br>3. Điền biểu mẫu:<br>• Phím tắt kích hoạt: Bắt buộc (bắt đầu bằng `/`, viết liền không dấu, VD: `/chao`, `/huongdan_doitra`).<br>• Tiêu đề gợi nhớ: Bắt buộc (3-150 ký tự).<br>• Danh mục nghiệp vụ: Bắt buộc (2-50 ký tự).<br>• Nội dung câu trả lời chuẩn: Bắt buộc (5-2000 ký tự).<br>4. Nhấn "Lưu mẫu câu".<br>5. Nếu để trống, thực hiện E-2. Nếu phím tắt trùng/sai định dạng, thực hiện E-3.<br>6. Lưu mẫu câu vào cơ sở dữ liệu chung.<br>7. Đầu ra: Thông báo "Thêm mẫu phản hồi nhanh thành công!", cập nhật mẫu câu vào danh mục dùng chung.<br>8. Use Case kết thúc thành công. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Không tìm thấy mẫu câu phù hợp<br>1. Bảng gợi ý hiển thị: "Không tìm thấy mẫu câu phù hợp".<br>2. Nhân viên gõ trả lời thủ công.<br><br>E-2: Để trống trường thông tin bắt buộc khi tạo mẫu<br>1. Báo lỗi đỏ dưới ô chưa điền thông tin.<br><br>E-3: Phím tắt không hợp lệ hoặc đã bị trùng lặp<br>1. Báo lỗi: "Phím tắt bắt buộc bắt đầu bằng '/' và không chứa khoảng trắng" hoặc "Phím tắt này đã được sử dụng". |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Tính duy nhất phím tắt: Mỗi phím tắt (bắt đầu bằng `/`) là mã duy nhất trên toàn hệ thống.<br>2. Quyền chỉnh sửa: Mẫu câu sau khi chèn vào ô chat cho phép nhân viên tùy biến chỉnh sửa trước khi gửi.<br>3. Đồng bộ dùng chung: Mẫu câu mới tạo có hiệu lực tức thì cho toàn bộ nhân viên trực ca. |

#### **Kiểm thử hộp đen Use case 3.4: Quản lý và sử dụng mẫu phản hồi nhanh**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Tên trường / Thao tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Phím tắt (Shortcut)** | • Bắt buộc bắt đầu bằng ký tự `/`<br>• Không chứa khoảng trắng<br>• Độ dài 2 - 50 ký tự<br>• Duy nhất trên hệ thống | **V_CUT_01:** Chuỗi phím tắt hợp lệ bắt đầu `/`, chưa tồn tại (VD: `/chao`, `/xloi_giaohang`) | **I_CUT_01:** Để trống<br>**I_CUT_02:** Không bắt đầu bằng ký tự `/` (VD: `chao`)<br>**I_CUT_03:** Chứa khoảng trắng (VD: `/chao ban`)<br>**I_CUT_04:** Phím tắt đã tồn tại trên hệ thống | • Biên độ dài: 1 ký tự (`/`) (I), 2 ký tự (`/a`) (V), 50 ký tự (V), 51 ký tự (I)<br>• Kiểm tra ký tự đầu `/` |
| **Tiêu đề gợi nhớ** | • Bắt buộc, độ dài 3 - 150 ký tự | **V_TITLE_01:** Chuỗi tiêu đề hợp lệ 3 - 150 ký tự | **I_TITLE_01:** Để trống<br>**I_TITLE_02:** Ngắn hơn 3 ký tự | • Biên độ dài: 2 ký tự (I), 3 ký tự (V), 150 ký tự (V) |
| **Nội dung mẫu câu** | • Bắt buộc, độ dài 5 - 2000 ký tự | **V_CONT_01:** Chuỗi nội dung mẫu hợp lệ 5 - 2000 ký tự | **I_CONT_01:** Để trống<br>**I_CONT_02:** Ngắn hơn 5 ký tự | • Biên độ dài: 4 ký tự (I), 5 ký tự (V), 2000 ký tự (V) |
| **Gõ ký tự `/` ô soạn thảo** | • Bắt ký tự `/` hiển thị bảng gợi ý danh sách mẫu câu | **V_SUGG_01:** Gõ ký tự `/` hiển thị bảng danh sách gợi ý | **I_SUGG_01:** Gõ các ký tự khác (không hiện danh sách gợi ý mẫu) | Ký tự mở bảng gợi ý `/` |

---

##### 2. Bảng quyết định (Decision Table)


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
| **UC 3.3 - E-1** | Xung đột tiếp quản (Người khác bấm trước) $→$ Chế độ Chỉ xem | `TC_LCS_15` |
| **UC 3.3 - E-2** | Để trống tin nhắn tư vấn hoặc vượt quá 4000 ký tự | `TC_LCS_16` |
| **UC 3.4 - Luồng chính** | Gõ `/` gợi ý mẫu phản hồi & Tạo mẫu phản hồi mới thành công | `TC_LCS_17`, `TC_LCS_18` |
| **UC 3.4 - E-4** | Tạo mẫu phản hồi trùng phím tắt / sai ký tự `/` | `TC_LCS_19` |

---
---



| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_01** | Kiểm tra Quản lý tạo tài khoản nhân viên mới thành công (Happy Path) | Đăng nhập tài khoản Quản lý, đang ở màn hình Quản lý nhân sự | 1. Nhập Họ tên hợp lệ.<br>2. Nhập Email nội bộ mới.<br>3. Nhập SĐT hợp lệ.<br>4. Chọn Vai trò là Agent.<br>5. Chọn 2 Kỹ năng chuyên môn.<br>6. Nhập Mật khẩu hợp lệ.<br>7. Bấm nút "Tạo tài khoản nhân sự". | • Họ tên: `"Nguyễn Văn Bình"` (V)<br>• Email: `"agent.binh@brand.com"` (V)<br>• SĐT: `"0987654321"` (V)<br>• Vai trò: Agent<br>• Kỹ năng: `["Đổi trả", "Giao hàng"]`<br>• Mật khẩu: `"Agent1234"` | Thông báo xanh: *"Tạo tài khoản nhân viên thành công!"*, làm mới biểu mẫu và tài khoản mới xuất hiện trong danh sách ở trạng thái Ngoại tuyến (OFFLINE). | Pass |
| **TC_LCS_02** | Kiểm tra tạo tài khoản khi để trống Email | Đang ở màn hình Tạo tài khoản nhân sự | 1. Để trống ô Email.<br>2. Điền hợp lệ các ô còn lại.<br>3. Bấm "Tạo tài khoản nhân sự". | • Email: `""` (I)<br>• Các ô khác: Nhập đúng (V) | Viền ô Email hằn đỏ, hiển thị thông báo lỗi ngay bên dưới: *"Vui lòng không để trống trường thông tin này"*. | Pass |
| **TC_LCS_03** | Kiểm tra tạo tài khoản với Mật khẩu 7 ký tự (Biên lỗi) | Đang ở màn hình Tạo tài khoản nhân sự | 1. Nhập Mật khẩu 7 ký tự.<br>2. Điền hợp lệ các ô còn lại.<br>3. Bấm "Tạo tài khoản nhân sự". | • Mật khẩu: `"Agent12"` (I)<br>• Các ô khác: Nhập đúng (V) | Báo lỗi dưới ô Mật khẩu: *"Mật khẩu tối thiểu 8 ký tự gồm chữ và số"*. | Pass |
| **TC_LCS_04** | Kiểm tra tạo tài khoản với Email đã tồn tại | Đang ở màn hình Tạo tài khoản nhân sự | 1. Nhập Email đã có trên hệ thống.<br>2. Điền hợp lệ các ô còn lại.<br>3. Bấm "Tạo tài khoản nhân sự". | • Email: `"agent.an@brand.com"` (I)<br>• Các ô khác: Nhập đúng (V) | Hiển thị cảnh báo lỗi: *"Địa chỉ email này đã được sử dụng"*. | Pass |
| **TC_LCS_05** | Kiểm tra tạo tài khoản Agent nhưng không chọn kỹ năng nào | Đang ở màn hình Tạo tài khoản nhân sự | 1. Chọn Vai trò là Agent.<br>2. Không tích chọn kỹ năng nào.<br>3. Bấm "Tạo tài khoản nhân sự". | • Vai trò: Agent<br>• Kỹ năng: Không chọn (0 kỹ năng) (I) | Báo lỗi màu đỏ: *"Tạo tài khoản Nhân viên tư vấn bắt buộc chọn ít nhất 1 danh mục kỹ năng xử lý"*. | Pass |
| **TC_LCS_06** | Kiểm tra Đăng nhập Bàn làm việc CSKH thành công | Đang ở màn hình Đăng nhập nội bộ | 1. Nhập Email nội bộ chính xác.<br>2. Nhập Mật khẩu chính xác.<br>3. Nhấn nút "Đăng nhập". | • Email: `"agent.an@brand.com"` (V)<br>• Mật khẩu: `"123456"` (V) | Chuyển hướng thành công vào giao diện Bàn làm việc CSKH (Live Support Console) với trạng thái mặc định ban đầu là Ngoại tuyến (OFFLINE). | Pass |
| **TC_LCS_07** | Kiểm tra Đăng nhập vào tài khoản nhân viên đang bị khóa | Tài khoản `agent.binh@brand.com` bị khóa | 1. Nhập Email nhân viên bị khóa.<br>2. Nhập đúng Mật khẩu.<br>3. Bấm "Đăng nhập". | • Email: `"agent.binh@brand.com"`<br>• Mật khẩu: `"123456"` | Hiển thị cảnh báo: *"Tài khoản hiện đang bị khóa hoặc ngừng kích hoạt"*. | Pass |
| **TC_LCS_08** | Kiểm tra Đăng nhập sai Mật khẩu | Đang ở màn hình Đăng nhập nội bộ | 1. Nhập Email chính xác.<br>2. Nhập Mật khẩu sai.<br>3. Bấm "Đăng nhập". | • Email: `"agent.an@brand.com"`<br>• Mật khẩu: `"sai_mat_khau"` (I) | Báo lỗi: *"Địa chỉ email hoặc mật khẩu không chính xác"*. | Pass |

---


| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_09** | Kiểm tra chuyển trạng thái từ OFFLINE sang ONLINE (Happy Path) | Đã đăng nhập Live Console, trạng thái đang là OFFLINE (Chấm xám) | 1. Nhấp chọn thanh trạng thái ở góc trên bên phải.<br>2. Chọn trạng thái "Trực tuyến" (ONLINE). | Click chọn "Trực tuyến" (V) | Nút chỉ thị chuyển sang **màu xanh lá (ONLINE)**, hiển thị thông báo: *"Đã chuyển sang trạng thái Trực tuyến - Bạn đã sẵn sàng tiếp nhận hỗ trợ!"*. Kích hoạt tự động nhận phân công ticket. | Pass |
| **TC_LCS_10** | Kiểm tra chuyển trạng thái từ ONLINE sang BUSY | Trạng thái hiện tại đang là ONLINE | 1. Nhấp thanh trạng thái.<br>2. Chọn trạng thái "Bận" (BUSY). | Click chọn "Bận" (V) | Nút chỉ thị chuyển sang **màu cam (BUSY)**, thông báo chuyển trạng thái thành công. Tạm dừng phân công ticket mới nhưng vẫn giữ các việc đang xử lý. | Pass |
| **TC_LCS_11** | Kiểm tra tự động đổi trạng thái sang OFFLINE khi mất mạng > 30s (E-1) | Đã đăng nhập, trạng thái đang là ONLINE | 1. Ngắt kết nối mạng thiết bị.<br>2. Quan sát nút chỉ thị sau 30 giây. | Ngắt mạng 30 giây | Nút chỉ thị trạng thái tự động đổi sang **màu xám (OFFLINE)**. Hiển thị dải cảnh báo cam: *"Đang mất kết nối thời gian thực. Hệ thống đang tự động kết nối lại..."*. | Pass |

---


| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_12** | Kiểm tra tiếp quản cuộc trò chuyện thành công (Happy Path) | Trạng thái ONLINE, hàng đợi có 1 phiên chat màu đỏ đang chờ hỗ trợ | 1. Nhấn chọn phiên chat cần hỗ trợ.<br>2. Bấm nút "Tiếp quản cuộc trò chuyện". | Click nút "Tiếp quản cuộc trò chuyện" (V) | Xác nhận quyền tiếp quản, tự động gỡ cờ đỏ, ngắt trả lời của Bot AI và gửi thông báo tự động vào chat khách hàng: *"Nhân viên tư vấn đã tham gia cuộc trò chuyện"*. Mở khóa ô nhập cho nhân viên. | Pass |
| **TC_LCS_13** | Kiểm tra nhắn tin 2 chiều thời gian thực | Nhân viên đã tiếp quản thành công ở `TC_LCS_12` | 1. Nhập nội dung tư vấn vào ô chat.<br>2. Nhấn nút "Gửi" (hoặc phím Enter). | Nội dung: `"Chào bạn, mình là An tư vấn viên PetHome. Mình có thể hỗ trợ gì cho bạn ạ?"` (V) | Tin nhắn tư vấn hiển thị lập tức sang khung chat của khách hàng với vai trò Nhân viên tư vấn. | Pass |
| **TC_LCS_14** | Kiểm tra xung đột tiếp quản khi người khác nhận trước (E-1) | Phiên chat `#105` đang chờ hỗ trợ | 1. Nhân viên A chuẩn bị bấm tiếp quản.<br>2. Nhân viên B bấm tiếp quản trước 1 giây.<br>3. Nhân viên A bấm tiếp quản ngay sau đó. | Thao tác bấm sau | Báo lỗi: *"Cuộc trò chuyện đã được nhận bởi nhân viên khác"*. Đặt màn hình của Nhân viên A về **Chế độ Chỉ xem (Read-only)**, khóa ô nhập tin nhắn. | Pass |
| **TC_LCS_15** | Kiểm tra gửi tin nhắn rỗng (E-2) | Nhân viên đang ở khung chat đã tiếp quản | 1. Để trống ô nhập tin nhắn.<br>2. Nhấn nút "Gửi". | Nội dung: `""` (I) | Nút gửi không kích hoạt (hoặc báo nhắc nhở: *"Vui lòng nhập nội dung tin nhắn tư vấn"*). | Pass |

---


| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_16** | Kiểm tra gõ phím tắt `/` gợi ý danh sách mẫu câu | Đang ở khung chat tư vấn | 1. Tại ô nhập văn bản, gõ ký tự `/`.<br>2. Quan sát menu thả xuống. | Nội dung: `/` (V) | Hiển thị menu danh sách gợi ý các mẫu phản hồi nhanh kèm phím tắt và tiêu đề. Bấm chọn mẫu câu sẽ chèn nguyên văn nội dung vào ô gõ. | Pass |
| **TC_LCS_17** | Kiểm tra tạo Mẫu phản hồi nhanh mới thành công | Đang ở màn hình Quản lý Mẫu phản hồi | 1. Nhập Phím tắt bắt đầu bằng `/`.<br>2. Nhập Tiêu đề.<br>3. Chọn Danh mục.<br>4. Nhập Nội dung mẫu.<br>5. Bấm "Lưu mẫu câu". | • Phím tắt: `/xloi_tre` (V)<br>• Tiêu đề: `"Xin lỗi giao hàng trễ"`<br>• Danh mục: `"Vận chuyển"`<br>• Nội dung: `"PetHome rất xin lỗi vì..."` | Thông báo *"Tạo mẫu phản hồi mới thành công"*. Mẫu câu mới lập tức có hiệu lực cho tất cả nhân viên đang trực ca khi gõ `/xloi_tre`. | Pass |
| **TC_LCS_18** | Kiểm tra báo lỗi khi tạo phím tắt không bắt đầu bằng `/` | Đang ở màn hình Tạo mẫu phản hồi | 1. Nhập Phím tắt không có ký tự `/` đầu.<br>2. Bấm "Lưu mẫu câu". | • Phím tắt: `xloi_tre` (I) | Hiển thị thông báo lỗi ngay dưới ô Phím tắt: *"Phím tắt bắt buộc phải bắt đầu bằng ký tự / và không chứa khoảng trắng"*. | Pass |

---
*Tài liệu kiểm thử hộp đen Khối chức năng 3 được chuẩn hóa toàn bộ 100%, tuân thủ cấu trúc chuẩn và đạt góc nhìn người dùng cuối (End-User).*

---
*Tài liệu kiểm thử hộp đen Khối chức năng 3 được chuẩn hóa toàn bộ 100%, tuân thủ cấu trúc chuẩn và đạt góc nhìn người dùng cuối (End-User).*

##### 3. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 3.4 - Luồng chính** | Gõ `/` gợi ý mẫu phản hồi & Tạo mẫu phản hồi mới thành công | `TC_LCS_16`, `TC_LCS_17` |
| **UC 3.4 - E-4** | Tạo mẫu phản hồi trùng phím tắt / sai ký tự `/` | `TC_LCS_18` |

##### 4. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LCS_16** | Kiểm tra gõ phím tắt `/` gợi ý danh sách mẫu câu | Đang ở khung chat tư vấn | 1. Tại ô nhập văn bản, gõ ký tự `/`.<br>2. Quan sát menu thả xuống. | Nội dung: `/` (V) | Hiển thị menu danh sách gợi ý các mẫu phản hồi nhanh kèm phím tắt và tiêu đề. Bấm chọn mẫu câu sẽ chèn nguyên văn nội dung vào ô gõ. | Pass |
| **TC_LCS_17** | Kiểm tra tạo Mẫu phản hồi nhanh mới thành công | Đang ở màn hình Quản lý Mẫu phản hồi | 1. Nhập Phím tắt bắt đầu bằng `/`.<br>2. Nhập Tiêu đề.<br>3. Chọn Danh mục.<br>4. Nhập Nội dung mẫu.<br>5. Bấm "Lưu mẫu câu". | • Phím tắt: `/xloi_tre` (V)<br>• Tiêu đề: `"Xin lỗi giao hàng trễ"`<br>• Danh mục: `"Vận chuyển"`<br>• Nội dung: `"PetHome rất xin lỗi vì..."` | Thông báo *"Tạo mẫu phản hồi mới thành công"*. Mẫu câu mới lập tức có hiệu lực cho tất cả nhân viên đang trực ca khi gõ `/xloi_tre`. | Pass |
| **TC_LCS_18** | Kiểm tra báo lỗi khi tạo phím tắt không bắt đầu bằng `/` | Đang ở màn hình Tạo mẫu phản hồi | 1. Nhập Phím tắt không có ký tự `/` đầu.<br>2. Bấm "Lưu mẫu câu". | • Phím tắt: `xloi_tre` (I) | Hiển thị thông báo lỗi ngay dưới ô Phím tắt: *"Phím tắt bắt buộc phải bắt đầu bằng ký tự / và không chứa khoảng trắng"*. | Pass |

---

### Use case 4.1: Phân chia công việc tự động {#uc-4-1}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Hệ thống ngầm |
| **Điều kiện bắt đầu** | 1. Có một phiếu hỗ trợ khẩn cấp mới được khởi tạo ở trạng thái "Chờ tiếp nhận" và chưa có người phụ trách.<br>2. Danh sách nhân sự và chuyên môn trực ca của nhân viên đã được kích hoạt trong hệ thống. |
| **Luồng sự kiện chính (Tự động chia việc cho nhân viên rảnh nhất)** | 1. Hệ thống tiếp nhận thông tin từ phiếu hỗ trợ mới và tiến hành kiểm tra tính hợp lệ của các trường dữ liệu đầu vào bắt buộc:<br>• Mã phiếu hỗ trợ: Chuỗi ký tự định danh, chiều dài cố định chính xác 36 ký tự, cấu tạo từ các chữ cái in thường a-f, chữ cái in hoa A-F, chữ số 0-9 và dấu gạch ngang phân tách.<br>• Danh mục sự cố: Chuỗi ký tự, bắt buộc phải khớp tuyệt đối với một trong sáu giá trị: Lỗi đơn hàng, Đổi trả/Hoàn tiền, Sản phẩm lỗi, Lỗi thanh toán, Thái độ phục vụ, hoặc Vấn đề khác.<br>• Mức độ ưu tiên: Chuỗi ký tự, bắt buộc phải khớp chính xác một trong ba giá trị: P1, P2, hoặc P3.<br>• Tóm tắt sự cố: Chuỗi văn bản chữ tự nhiên, yêu cầu độ dài đạt tối thiểu 20 ký tự và giới hạn tối đa là 255 ký tự.<br>2. Hệ thống quét danh sách nhân viên tư vấn đang ở trạng thái làm việc "Trực tuyến".<br>3. Hệ thống lọc ra các nhân viên trực tuyến có kỹ năng xử lý phù hợp với danh mục sự cố của phiếu. Nếu không có nhân viên trực tuyến nào phù hợp, hệ thống thực hiện luồng rẽ nhánh E-1.<br>4. Hệ thống đếm số lượng công việc chưa hoàn tất (các phiếu đang ở trạng thái "Chờ tiếp nhận" hoặc "Đang xử lý") của từng nhân viên hợp lệ.<br>5. Hệ thống chọn nhân viên có kết quả đếm số lượng công việc ở mức thấp nhất (giá trị tối thiểu từ 0 trở lên) để phân công. Nếu có từ hai nhân viên trở lên sở hữu số lượng phiếu bằng nhau, hệ thống truy xuất dữ liệu thời gian và ưu tiên chọn người có khoảng cách từ lúc nhận việc lần cuối đến thời điểm hiện tại là lớn nhất.<br>6. Hệ thống gán phiếu hỗ trợ cho nhân viên được chọn và chuyển trạng thái phiếu sang "Đang xử lý".<br>7. Hệ thống chuyển tiếp thông tin phiếu sang chức năng Giám sát thời hạn xử lý cam kết để theo dõi tiến độ.<br>8. Đầu ra: Phiếu hỗ trợ hiển thị trên màn hình làm việc cá nhân của nhân viên được chỉ định kèm thông báo nổi góc màn hình: "Bạn có một phiếu hỗ trợ mới được phân công!". Trạng thái người phụ trách trên danh sách công việc chung được cập nhật theo tên nhân viên. |
| **Luồng con (A-1: Quản trị viên can thiệp phân công thủ công)** | 1. Tại luồng rẽ nhánh E-1, khi phiếu bị chuyển vào danh sách "Chờ phân bổ" do thiếu nhân sự phù hợp, Quản trị viên mở màn hình quản lý danh sách công việc.<br>2. Quản trị viên bấm vào phiếu đang chờ và chọn nút "Phân công thủ công".<br>3. Hệ thống mở cửa sổ giao việc gồm danh sách toàn bộ nhân viên tư vấn kèm trạng thái làm việc hiện tại và số việc đang xử lý của từng người.<br>4. Quản trị viên chọn một nhân viên và bấm "Giao việc".<br>5. Nếu Quản trị viên chưa chọn nhân viên mà đã bấm giao việc, hệ thống thực hiện luồng rẽ nhánh E-2.<br>6. Hệ thống gán phiếu hỗ trợ cho nhân viên được chỉ định, chuyển trạng thái sang "Đang xử lý" và kích hoạt thông báo nhận việc cho nhân viên đó.<br>7. Đầu ra: Phiếu hỗ trợ biến mất khỏi hàng chờ chưa phân bổ và xuất hiện trên bảng việc của nhân viên được chỉ định.<br>8. Use Case kết thúc thành công. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Không có nhân viên trực tuyến phù hợp chuyên môn<br>1. Hệ thống giữ nguyên phiếu hỗ trợ ở trạng thái "Chờ phân bổ" và để trống người xử lý.<br>2. Hệ thống phát âm thanh cảnh báo và hiển thị thông báo khẩn màu cam trên màn hình Quản trị viên: "Có phiếu hỗ trợ chưa có nhân viên tiếp nhận do thiếu người trực phù hợp!".<br>3. Quản trị viên tiếp nhận cảnh báo và xử lý qua Luồng con A-1.<br><br>E-2: Chưa chọn nhân viên khi phân công thủ công<br>1. Hệ thống làm sáng viền đỏ khung chọn nhân viên và hiển thị dòng chữ nhắc nhở: "Vui lòng chọn một nhân viên tiếp nhận trước khi bấm Giao việc".<br>2. Quản trị viên chọn nhân viên từ danh sách và bấm "Giao việc" lại từ bước 4 của Luồng con A-1. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Nguyên tắc phân chia tải tối thiểu: Hệ thống luôn ưu tiên giao việc cho nhân viên đang trực ca có ít đầu việc đang mở nhất nhằm cân bằng khối lượng công việc, tránh người quá tải trong khi người khác ngồi trống việc.<br>2. Tiêu chuẩn tính tải công việc: Khối lượng việc của một nhân viên chỉ tính tổng số các phiếu đang ở trạng thái "Chờ tiếp nhận" hoặc "Đang xử lý". Các phiếu đã đánh dấu giải quyết xong hoặc đã đóng hoàn toàn không được tính vào tải.<br>3. Điều kiện nhân sự hợp lệ: Chỉ những nhân viên đang ở trạng thái làm việc "Trực tuyến" (ONLINE) và có chuyên môn bao hàm danh mục của sự cố mới đủ điều kiện tham gia nhận phân công tự động. Nhân viên đang ở trạng thái Bận (BUSY) hoặc Ngoại tuyến (OFFLINE) sẽ bị bỏ qua. |

#### **Kiểm thử hộp đen Use case 4.1: Phân chia công việc tự động**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Tiêu chí / Trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Trạng thái làm việc nhân viên** | • Chỉ gán Ticket cho nhân viên đang ở trạng thái Trực tuyến (`ONLINE`) | **V_STT_01:** Có ít nhất 1 nhân viên ở trạng thái Trực tuyến (`ONLINE`) | **I_STT_01:** Tất cả nhân viên đều ở trạng thái Bận (`BUSY`) hoặc Ngoại tuyến (`OFFLINE`) (E-1) | Trạng thái sẵn sàng nhận việc |
| **Kỹ năng chuyên môn xử lý** | • Nhân viên phải có kỹ năng khớp với danh mục khiếu nại của Ticket | **V_SKILL_01:** Có nhân viên `ONLINE` khớp danh mục kỹ năng sự cố | **I_SKILL_01:** Có nhân viên `ONLINE` nhưng không ai có kỹ năng phù hợp danh mục sự cố (E-1) | Khớp / Không khớp danh mục kỹ năng |
| **Tải công việc hiện tại** | • Ưu tiên gán cho nhân viên có số lượng Ticket chưa đóng (`Pending` / `In Progress`) ít nhất | **V_LOAD_01:** Chọn nhân viên có số Ticket chưa đóng ít nhất | **I_LOAD_01:** Không có ứng viên hợp lệ | Đếm số Ticket đang gánh |
| **Thời gian rảnh lâu nhất** | • Nếu số Ticket đang gánh bằng nhau, chọn người có thời điểm nhận việc gần nhất xa nhất | **V_TIME_01:** Chọn nhân viên có thời gian rảnh lâu hơn | Không áp dụng phân vùng sai | So sánh mốc thời gian chờ việc |

---

##### 2. Bảng quyết định (Decision Table)


*(Tiền đề quy trình: Có một Phiếu hỗ trợ mới rơi vào hàng đợi xử lý)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Tồn tại ít nhất 1 nhân viên ở trạng thái Trực tuyến (ONLINE)?** | F | T | T | T | T |
| **C2: Tồn tại nhân viên Trực tuyến có kỹ năng khớp với danh mục sự cố?** | - | F | T | T | T |
| **C3: Tồn tại 1 nhân viên có số lượng công việc ít hơn tất cả những người khác?** | - | - | T | F | F |
| **C4: Tồn tại 1 nhân viên có thời gian rảnh lâu hơn các ứng viên đồng tải?** | - | - | - | T | F |
| **H1: Giữ Ticket ở "Chờ tiếp nhận", bắn báo động đỏ cho Quản lý (E-1)** | X | X | | | X |
| **H2: Tự động phân công Ticket cho nhân viên có số lượng công việc ít nhất** | | | X | | |
| **H3: Phân công Ticket cho nhân viên có thời gian rảnh lâu nhất trong nhóm đồng tải** | | | | X | |

---
---

##### 3. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 4.1 - Luồng chính** | Tự động phân công Ticket cho nhân viên rảnh nhất & đúng kỹ năng | `TC_DIS_01` |
| **UC 4.1 - Rule 4** | Xử lý trường hợp trùng tải (Giao cho người có thời gian chờ việc lâu hơn) | `TC_DIS_02` |
| **UC 4.1 - E-1** | Bẫy lỗi thiếu nhân viên ONLINE hoặc không có nhân viên đúng kỹ năng | `TC_DIS_03` |

##### 4. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_01** | Kiểm tra tự động giao Ticket cho nhân viên có ít việc nhất (Happy Path) | Nhân viên A có 1 Ticket đang mở, Nhân viên B có 3 Ticket. Cả 2 đang ONLINE & đúng kỹ năng. | 1. Tạo một phiếu hỗ trợ khẩn cấp P1.<br>2. Đăng nhập tài khoản Nhân viên A và kiểm tra màn hình Bàn làm việc. | Ticket P1, Danh mục `Lỗi đơn hàng` (V) | Hệ thống tự động gán thẳng phiếu hỗ trợ P1 cho Nhân viên A. Phiếu xuất hiện trên màn hình Bàn làm việc của Nhân viên A ở trạng thái *Đang xử lý (In Progress)*. | Pass |
| **TC_DIS_02** | Kiểm tra xử lý trùng tải công việc (Chọn người có thời gian chờ rảnh lâu hơn) | Nhân viên A và B cùng gánh 2 Ticket. Nhân viên A rảnh 30 phút, Nhân viên B rảnh 5 phút. | 1. Tạo một phiếu hỗ trợ P2.<br>2. Đăng nhập kiểm tra màn hình của cả 2 nhân viên. | Ticket P2, Danh mục `Sản phẩm lỗi` (V) | Phiếu hỗ trợ P2 được tự động gán cho Nhân viên A (do thời gian chờ việc lâu hơn Nhân viên B). | Pass |
| **TC_DIS_03** | Kiểm tra xử lý khi không có nhân viên trực tuyến đúng kỹ năng (E-1) | Nhân viên A (đúng kỹ năng) OFFLINE. Nhân viên B (sai kỹ năng) ONLINE. | 1. Tạo một phiếu hỗ trợ P1 danh mục `Đổi trả/Hoàn tiền`.<br>2. Đăng nhập tài khoản Quản lý quan sát màn hình. | Ticket P1, Danh mục `Đổi trả/Hoàn tiền` (I) | Màn hình của Quản lý bật thông báo cảnh báo đỏ. Ticket bị giữ ở trạng thái *Chờ tiếp nhận (Pending)* không có người nhận để Quản lý gán thủ công. | Pass |

---

### Use case 4.2: Giám sát thời hạn xử lý cam kết {#uc-4-2}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Hệ thống ngầm (Nhân viên CSKH và Quản lý CSKH tiếp nhận kết quả giám sát) |
| **Điều kiện bắt đầu** | 1. Phiếu hỗ trợ đã được phân công cho nhân viên và chuyển sang trạng thái "Đang xử lý".<br>2. Khung chính sách thời gian xử lý theo mức độ ưu tiên đã được ban hành trong hệ thống. |
| **Luồng sự kiện chính (Kích hoạt đếm ngược và ghi nhận hoàn thành đúng hạn)** | 1. Hệ thống tiếp nhận thông tin từ phiếu hỗ trợ vừa được giao việc và tiến hành kiểm tra tính hợp lệ của các trường dữ liệu đầu vào bắt buộc:<br>• Mã phiếu hỗ trợ: Chuỗi ký tự định danh, độ dài cố định chính xác 36 ký tự, định dạng UUID v4, bao gồm chữ cái in thường a-f, in hoa A-F, chữ số 0-9 và dấu gạch ngang phân tách.<br>• Mức độ ưu tiên: Chuỗi ký tự, bắt buộc thuộc một trong ba giá trị hợp lệ: P1: 15 phút, P2: 60 phút, hoặc P3: 240 phút.<br>• Thời hạn xử lý cam kết (T_cam_kết): Thời lượng tối đa quy định theo mức độ ưu tiên: P1 (Cực kỳ khẩn cấp): 900 giây; P2 (Khẩn cấp cao): 3.600 giây; P3 (Trung bình): 14.400 giây.<br>2. Hệ thống tính toán mốc thời gian hạn chót cần hoàn tất sự việc và hiển thị đồng hồ đếm ngược trực tiếp trên thẻ công việc.<br>• Thời điểm hạn chót = T_bắt_đầu + T_cam_kết.<br>3. Hệ thống liên tục chạy ngầm để theo dõi, đối chiếu thời gian còn lại (T_còn_lại, tính bằng giây) và phân loại trạng thái:<br>• Trạng thái Bình thường: T_còn_lại > 20% tổng thời gian cam kết (P1 > 180 giây; P2 > 720 giây; P3 > 2.880 giây).<br>• Trạng thái Cảnh báo: 1 giây ≤ T_còn_lại ≤ 20% tổng thời gian cam kết.<br>• Nếu T_còn_lại ≤ 0 giây, hệ thống thực hiện luồng rẽ nhánh E-1.<br>4. Khi nhân viên xử lý xong khiếu nại cho khách hàng, nhân viên chọn nút "Hoàn tất xử lý" trên thẻ công việc.<br>5. Hệ thống hiển thị biểu mẫu yêu cầu nhập kết quả xử lý: Nội dung kết quả xử lý là chuỗi văn bản chữ tự nhiên bắt buộc, không được rỗng hoặc chỉ chứa khoảng trắng, yêu cầu độ dài kí tự trong đoạn [10, 1.000].<br>6. Nhân viên nhập nội dung và bấm "Xác nhận hoàn thành".<br>7. Hệ thống kiểm tra dữ liệu nội dung. Nếu độ dài < 10 ký tự, > 1.000 ký tự, hoặc chuỗi không hợp lệ, hệ thống thực hiện luồng rẽ nhánh E-2.<br>8. Hệ thống dừng đồng hồ đếm ngược, chuyển trạng thái phiếu sang "Đã giải quyết" và ghi nhận đạt chuẩn cam kết thời gian.<br>9. Đầu ra: Thẻ công việc chuyển sang màu xanh lá cây với nhãn "Đạt chuẩn cam kết". Hệ thống hiển thị thông báo nổi: "Phiếu hỗ trợ đã được xử lý thành công đúng thời hạn!". |
| **Luồng con** | Không có. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Quá hạn thời gian cam kết xử lý (Vi phạm cam kết dịch vụ)<br>1. Đồng hồ đếm ngược chạm mốc 0 trong khi phiếu vẫn ở trạng thái "Đang xử lý".<br>2. Hệ thống đánh dấu phiếu này ở trạng thái vi phạm thời hạn xử lý.<br>3. Thẻ công việc trên màn hình nhân viên và danh sách giám sát chung lập tức chuyển sang màu đỏ nhấp nháy nổi bật.<br>4. Hệ thống kích hoạt cơ chế báo động leo thang: phát tín hiệu chuông cảnh báo đỏ và gửi thông báo trực tiếp lên bảng theo dõi của Quản lý CSKH với nội dung: "Phiếu hỗ trợ [Mã phiếu] do nhân viên [Tên nhân viên] phụ trách đã quá hạn xử lý!".<br>5. Hệ thống ghi nhận điểm trừ vi phạm cam kết vào báo cáo hiệu suất định kỳ của nhân viên phụ trách.<br>6. Khi nhân viên hoàn thành xử lý muộn, hệ thống vẫn cho phép nhập kết quả giải quyết theo bước 5 của luồng chính nhưng ghi nhận nhãn "Hoàn thành quá hạn".<br><br>E-2: Để trống nội dung kết quả xử lý<br>1. Hệ thống khoanh viền đỏ ô nhập nội dung và hiển thị dòng chữ báo lỗi: "Vui lòng nhập tóm tắt kết quả đã xử lý cho khách hàng trước khi đóng phiếu".<br>2. Hệ thống giữ nguyên phiếu ở trạng thái "Đang xử lý" và đồng hồ đếm ngược tiếp tục chạy.<br>3. Nhân viên nhập lại nội dung giải quyết và quay lại bước 6 của luồng chính. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Khung thời gian cam kết theo mức ưu tiên: Thời hạn xử lý bắt buộc được gắn chặt với mức độ khẩn cấp của sự cố: Mức P1 bắt buộc hoàn tất trong vòng 15 phút; Mức P2 tối đa 60 phút; Mức P3 tối đa 240 phút (4 giờ).<br>2. Tiêu chí xác định đạt hoặc vi phạm cam kết: Phiếu hỗ trợ chỉ được tính là hoàn thành đúng cam kết nếu nhân viên bấm xác nhận giải quyết khi đồng hồ đếm ngược chưa về 0. Mọi trường hợp hoàn tất sau mốc này đều bị hệ thống ghi nhận là vi phạm.<br>3. Cơ chế báo động leo thang bắt buộc: Ngay khi xảy ra vi phạm quá hạn, hệ thống bắt buộc phải phát cảnh báo tức thì tới cấp Quản lý để can thiệp kịp thời, không để khiếu nại của khách hàng bị bỏ quên hoặc xử lý chậm trễ. |

#### **Kiểm thử hộp đen Use case 4.2: Giám sát thời hạn xử lý cam kết**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Mức độ ưu tiên | Ràng buộc thời hạn SLA | Phân vùng Bình thường (V) | Phân vùng Cảnh báo cam (V) | Phân vùng Vi phạm đỏ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sự cố P1 (Khẩn cấp)** | Cam kết **15 phút** (900 giây)<br>Cảnh báo $< 20\%$ (180s) | **V_P1_01:** Còn từ 181 đến 900 giây | **V_P1_02:** Còn từ 1 đến 180 giây | **I_P1_01:** Còn $≤ 0$ giây (Quá hạn) | 900s, 181s, 180s, 1s, 0s, -1s |
| **Sự cố P2 (Khẩn cấp cao)** | Cam kết **60 phút** (3600 giây)<br>Cảnh báo $< 20\%$ (720s) | **V_P2_01:** Còn từ 721 đến 3600 giây | **V_P2_02:** Còn từ 1 đến 720 giây | **I_P2_01:** Còn $≤ 0$ giây (Quá hạn) | 3600s, 721s, 720s, 1s, 0s |
| **Sự cố P3 (Trung bình)** | Cam kết **240 phút** (14400s)<br>Cảnh báo $< 20\%$ (2880s) | **V_P3_01:** Còn từ 2881 đến 14400s | **V_P3_02:** Còn từ 1 đến 2880s | **I_P3_01:** Còn $≤ 0$ giây (Quá hạn) | 14400s, 2881s, 2880s, 0s |

---

##### 2. Bảng quyết định (Decision Table)


*(Tiền đề quy trình: Tiến trình Cron Job kiểm tra thời gian đếm ngược SLA mỗi 30 giây)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: Nhân viên bấm nút "Xác nhận đã xử lý" khi thời gian đếm ngược còn > 0s?** | T | F | F | F |
| **C2: Thời gian đếm ngược còn lại ở mức $< 20\%$ tổng thời lượng SLA?** | - | F | T | T |
| **C3: Thời gian đếm ngược trôi về mốc 0 giây ($≤ 0$s)?** | - | - | F | T |
| **H1: Dừng đồng hồ SLA, ghi nhận Hoàn thành Đúng hạn (SLA Met), thẻ hiển thị màu xanh** | X | | | |
| **H2: Giữ đồng hồ đếm ngược, hiển thị thẻ và đồng hồ ở trạng thái màu sắc Bình thường** | | X | | |
| **H3: Đổi thẻ và đồng hồ đếm ngược sang tông màu Vàng Cam cảnh báo** | | | X | |
| **H4: Thẻ chuyển sang màu Đỏ nhấp nháy, bắn âm thanh báo động & trừ điểm SLA (E-1)** | | | | X |

---

##### 3. Sơ đồ chuyển trạng thái (State Transition Diagram)


| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- |
| **Bình thường (SLA Normal)** | Thời gian đếm ngược trôi xuống mốc $< 20\%$ thời lượng SLA | **Cảnh báo (SLA Warning - Nền cam)** |
| **Bình thường / Cảnh báo** | Nhân viên nhấn nút "Xác nhận đã xử lý" khi thời gian còn $> 0$s | **Hoàn thành đúng hạn (SLA Met)** |
| **Cảnh báo (SLA Warning)** | Thời gian đếm ngược trôi về mốc 0 giây ($≤ 0$s) | **Vi phạm quá hạn (SLA Breached - Nền đỏ)** |
| **Vi phạm quá hạn (SLA Breached)** | Nhân viên bấm "Xác nhận đã xử lý" muộn | **Hoàn thành quá hạn (SLA Missed)** |

---
---

##### 4. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 4.2 - Luồng chính** | Đồng hồ đếm ngược SLA ở trạng thái màu sắc Bình thường | `TC_DIS_04` |
| **UC 4.2 - Rule 3** | Kích hoạt trạng thái Cảnh báo màu cam khi thời gian SLA còn < 20% | `TC_DIS_05` |
| **UC 4.2 - E-1** | Quá hạn SLA (0 giây) → Thẻ chuyển màu đỏ nhấp nháy & bắn báo động | `TC_DIS_06` |
| **UC 4.2 - Rule 1** | Dừng đồng hồ SLA đúng hạn khi nhân viên bấm "Xác nhận đã xử lý" | `TC_DIS_07` |

##### 5. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_04** | Kiểm tra đồng hồ đếm ngược SLA ở trạng thái màu sắc Bình thường | Ticket P1 vừa được gán sang trạng thái *Đang xử lý* | 1. Đăng nhập tài khoản Nhân viên CSKH.<br>2. Quan sát thẻ công việc của phiếu P1. | Thời gian còn lại = 900 giây (15 phút) | Thẻ hiển thị đồng hồ đếm ngược từ 15:00. Nền thẻ và đồng hồ hiển thị màu sắc Bình thường. | Pass |
| **TC_DIS_05** | Kiểm tra kích hoạt Cảnh báo màu cam tại mốc < 20% SLA (180 giây) | Ticket P1 đang chạy đồng hồ đếm ngược | 1. Quan sát đồng hồ đếm ngược trên thẻ phiếu P1.<br>2. Chờ cho đến khi đồng hồ nhảy xuống mốc 03:00 (đúng 180 giây). | Thời gian còn lại = 180 giây (V) | Thẻ và đồng hồ đếm ngược lập tức đổi sang **tông màu Vàng Cam cảnh báo** chính xác tại mốc 180 giây. | Pass |
| **TC_DIS_06** | Kiểm tra vi phạm quá hạn SLA tại mốc 0 giây (E-1) | Phiên chat đang ở trạng thái Cảnh báo màu cam | 1. Giữ nguyên không bấm xử lý phiếu P1.<br>2. Quan sát đồng hồ khi trôi về mốc 00:00. | Thời gian còn lại = 0 giây (I) | Thẻ chuyển sang **màu Đỏ nhấp nháy**, hệ thống phát âm thanh báo động vi phạm và gửi cảnh báo đỏ lên màn hình Quản lý. Ghi nhận trừ điểm SLA của nhân viên. | Pass |
| **TC_DIS_07** | Kiểm tra dừng đồng hồ SLA khi bấm hoàn thành đúng hạn | Ticket đang đếm ngược ở mốc Cảnh báo màu cam | 1. Nhấn nút "Xác nhận đã xử lý" trên thẻ phiếu P1.<br>2. Nhập ghi chú xử lý hợp lệ và bấm Xác nhận khi đồng hồ còn > 0s. | Ghi chú hợp lệ, thời gian còn lại = 45s (V) | Ghi nhận Hoàn thành Đúng hạn (SLA Met). Đồng hồ SLA ngừng đếm ngược lập tức và thẻ hiển thị đánh dấu màu xanh lá. | Pass |

---

### Use case 4.3: Quản lý tiến độ trên bảng Kanban {#uc-4-3}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Nhân viên CSKH, Quản lý CSKH, Quản trị viên |
| **Điều kiện bắt đầu** | 1. Người dùng đã đăng nhập thành công vào hệ thống bằng tài khoản Nhân viên, Quản lý hoặc Quản trị viên.<br>2. Bảng Kanban đang hiển thị ít nhất một phiếu hỗ trợ mà người dùng có quyền cập nhật tiến độ. |
| **Luồng sự kiện chính (Kéo thả thẻ công việc sang trạng thái Đã giải quyết)** | 1. Người dùng mở mục "Bảng công việc Kanban" trên thanh điều hướng.<br>2. Hệ thống hiển thị bảng Kanban gồm 4 cột tiến độ: "Chờ tiếp nhận", "Đang xử lý", "Đã giải quyết" và "Đóng phiếu". Mỗi thẻ công việc hiển thị đầy đủ thông tin mã phiếu, tóm tắt sự cố, nhãn ưu tiên và đồng hồ đếm ngược.<br>3. Nhân viên nhấn giữ một thẻ phiếu hỗ trợ ở cột "Đang xử lý" và kéo thả sang cột "Đã giải quyết".<br>4. Hệ thống tiếp nhận thông tin thẻ phiếu và tiến hành kiểm tra tính hợp lệ của các trường dữ liệu đầu vào bắt buộc:<br>• Mã phiếu hỗ trợ: Chuỗi ký tự định danh, chiều dài cố định chính xác 36 ký tự, định dạng UUID v4, gồm chữ cái in thường a-f, in hoa A-F, chữ số 0-9 và dấu gạch ngang phân tách.<br>• Trạng thái hiện tại: Chuỗi ký tự, bắt buộc phải khớp chính xác giá trị "Đang xử lý".<br>• Trạng thái đích: Chuỗi ký tự, bắt buộc phải khớp chính xác giá trị "Đã giải quyết".<br>5. Hệ thống kiểm tra quyền hạn xử lý phiếu của người dùng. Nếu phiếu không thuộc quyền phụ trách của nhân viên đang thao tác (và nhân viên không có vai trò Quản lý/Quản trị viên), hệ thống thực hiện luồng rẽ nhánh E-1.<br>6. Hệ thống kiểm tra quy tắc luân chuyển trạng thái một chiều. Nếu hướng chuyển trạng thái không hợp lệ (ví dụ kéo ngược về trạng thái trước đó), hệ thống thực hiện luồng rẽ nhánh E-2.<br>7. Hệ thống hiển thị biểu mẫu yêu cầu ghi nhận kết quả xử lý: Nội dung kết quả xử lý là chuỗi văn bản chữ tự nhiên bắt buộc; không được rỗng hoặc chỉ chứa khoảng trắng; độ dài nằm trong đoạn biên [10, 1.000] ký tự.<br>8. Nhân viên nhập nội dung kết quả xử lý và nhấn nút "Xác nhận hoàn thành".<br>9. Hệ thống kiểm tra dữ liệu nội dung kết quả xử lý. Nếu độ dài < 10 ký tự, > 1.000 ký tự hoặc chuỗi rỗng/khoảng trắng, hệ thống thực hiện luồng rẽ nhánh E-3.<br>10. Hệ thống kiểm tra kết nối mạng truyền dữ liệu. Nếu mất kết nối trong quá trình lưu dữ liệu về máy chủ, hệ thống thực hiện luồng rẽ nhánh E-4.<br>11. Hệ thống cập nhật trạng thái phiếu sang "Đã giải quyết", dừng đồng hồ đếm ngược cam kết thời gian, lưu vết thời điểm hoàn tất và tài khoản người thực hiện.<br>12. Đầu ra: Hệ thống đóng hộp thoại, hiển thị thông báo nổi màu xanh lá ở góc màn hình: "Cập nhật trạng thái phiếu hỗ trợ thành công!", thẻ công việc nằm cố định tại cột "Đã giải quyết" với nhãn ghi nhận kết quả và đồng hồ đếm ngược dừng lại. |
| **Luồng con (A-1: Cập nhật tiến độ từ màn hình chi tiết phiếu)** | 1. Thay vì kéo thả thẻ, nhân viên nhấp đúp chuột vào một thẻ phiếu trên bảng Kanban để mở cửa sổ "Chi tiết phiếu hỗ trợ".<br>2. Hệ thống hiển thị đầy đủ thông tin sự cố, lịch sử trao đổi và nút chọn "Cập nhật trạng thái".<br>3. Nhân viên nhấp vào danh sách chọn trạng thái. Hệ thống chỉ hiển thị các trạng thái hợp lệ được phép tiến tới tiếp theo (ví dụ: đang ở "Đang xử lý" thì chỉ cho chọn "Đã giải quyết").<br>4. Nhân viên chọn trạng thái "Đã giải quyết" và bấm nút "Lưu thay đổi".<br>5. Hệ thống hiển thị hộp thoại yêu cầu nhập kết quả xử lý giống bước 7 của luồng chính.<br>6. Nhân viên nhập nội dung và bấm "Xác nhận hoàn thành" để tiếp tục từ bước 9 của luồng chính. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Phiếu không thuộc quyền phụ trách của nhân viên<br>1. Hệ thống từ chối cập nhật, tạo hiệu ứng trượt trả thẻ công việc về lại vị trí ban đầu.<br>2. Hệ thống hiển thị thông báo cảnh báo màu đỏ: "Bạn không có quyền cập nhật phiếu hỗ trợ do nhân viên khác phụ trách!".<br>3. Use Case kết thúc thất bại.<br><br>E-2: Chuyển trạng thái không hợp lệ<br>1. Hệ thống từ chối cho thả thẻ vào cột đích và trả thẻ về vị trí cột cũ.<br>2. Hệ thống hiển thị thông báo lỗi: "Tiến độ phiếu chỉ được phép chuyển tiến lên theo quy trình, không thể chuyển ngược lại trạng thái trước đó!".<br>3. Use Case kết thúc thất bại.<br><br>E-3: Bỏ trống hoặc nhập sai định dạng độ dài nội dung kết quả xử lý<br>1. Hệ thống khoanh viền đỏ ô nhập liệu và hiển thị dòng chữ cảnh báo dưới chân ô: "Nội dung kết quả xử lý là bắt buộc, độ dài từ 10 đến 1.000 ký tự".<br>2. Hệ thống giữ nguyên hộp thoại và giữ thẻ phiếu ở trạng thái "Đang xử lý".<br>3. Nhân viên nhập lại nội dung đúng quy cách và quay lại bước 8 của luồng chính.<br><br>E-4: Mất kết nối mạng trong lúc lưu dữ liệu<br>1. Hệ thống không thể gửi dữ liệu cập nhật về máy chủ.<br>2. Hệ thống đưa thẻ phiếu về lại cột ban đầu, giữ nguyên trạng thái cũ và hiển thị thông báo: "Mất kết nối mạng, chưa cập nhật được trạng thái. Vui lòng thử lại!".<br>3. Nhân viên kiểm tra kết nối và thao tác lại từ bước 3 của luồng chính. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Phân quyền thao tác trên thẻ công việc: Nhân viên tư vấn chỉ có quyền kéo thả hoặc cập nhật trạng thái đối với các phiếu được phân công trực tiếp cho mình. Quản lý CSKH và Quản trị viên có quyền can thiệp, chuyển trạng thái cho mọi phiếu trên bảng Kanban.<br>2. Quy tắc luân chuyển tiến độ một chiều: Tiến độ của phiếu hỗ trợ bắt buộc phải đi theo trình tự tiến lên: Chờ tiếp nhận → Đang xử lý → Đã giải quyết → Đóng phiếu. Hệ thống không cho phép nhân viên tự ý kéo lùi thẻ về các trạng thái trước đó.<br>3. Điều kiện hoàn tất phiếu: Để đưa một phiếu sang trạng thái "Đã giải quyết", nhân viên bắt buộc phải cung cấp tóm tắt kết quả xử lý với độ dài từ 10 đến 1.000 ký tự nhằm phục vụ lưu vết đối soát và đánh giá chất lượng phục vụ.<br>4. Điểm dừng đồng hồ cam kết dịch vụ: Ngay khi phiếu được ghi nhận sang trạng thái "Đã giải quyết", đồng hồ đếm ngược sẽ dừng lại. Mốc thời gian hoàn tất này là căn cứ duy nhất để xác định phiếu đó đạt chuẩn hay vi phạm cam kết thời gian xử lý. |

#### **Kiểm thử hộp đen Use case 4.3: Quản lý tiến độ trên bảng Kanban**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Trường dữ liệu / Thao tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Luân chuyển trạng thái 1 chiều** | • Luân chuyển tiến theo thứ tự: `Chờ tiếp nhận` $→$ `Đang xử lý` $→$ `Đã giải quyết` $→$ `Đã kết thúc` | **V_FLOW_01:** Kéo thả thẻ công việc tiến theo đúng chiều thứ tự quy định | **I_FLOW_01:** Kéo ngược lùi trạng thái (VD: Kéo từ `Đang xử lý` lùi về `Chờ tiếp nhận`) (E-2) | Luân chuyển tiến lên / kéo lùi |
| **Quyền kéo thả thẻ (Kanban)** | • Nhân viên (Agent) chỉ được kéo thẻ do mình phụ trách<br>• Quản lý/Admin có quyền kéo mọi thẻ | **V_PERM_01:** Agent kéo thả thẻ do chính mình phụ trách<br>**V_PERM_02:** Quản lý/Admin kéo thả thẻ bất kỳ | **I_PERM_01:** Agent cố tình kéo thả thẻ do nhân viên khác phụ trách (E-1) | Phân quyền kéo thả |
| **Ghi chú xử lý sự cố (Summary)** | • Bắt buộc khi chuyển sang `Đã giải quyết` (`RESOLVED`)<br>• Độ dài 10 - 1000 ký tự | **V_NOTE_01:** Chuỗi ghi chú xử lý hợp lệ 10 - 1000 ký tự (VD: *"Đã kiểm tra và hoàn tiền đơn hàng"*) | **I_NOTE_01:** Để trống ghi chú xử lý<br>**I_NOTE_02:** Ngắn hơn 10 ký tự (E-3) | • Biên dưới: 9 ký tự (I), 10 ký tự (V), 11 ký tự (V)<br>• Biên trên: 1000 ký tự (V), 1001 ký tự (I) |

---

##### 2. Bảng quyết định (Decision Table)


*(Tiền đề quy trình: Người dùng kéo thả một thẻ công việc trên bảng Kanban)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: Người thao tác là Quản lý/Admin HOẶC là Nhân viên phụ trách thẻ này?** | F | T | T | T |
| **C2: Thao tác kéo thả tuân thủ đúng thứ tự tiến tiến độ 1 chiều?** | - | F | T | T |
| **C3: Nếu chuyển sang "Đã giải quyết", ghi chú xử lý đạt từ 10-1000 ký tự?** | - | - | F | T |
| **H1: Chặn thao tác, đẩy thẻ về cột cũ & Báo lỗi "Bạn không có quyền..." (E-1)** | X | | | |
| **H2: Chặn thao tác, đẩy thẻ về cột cũ & Báo lỗi "Tiến độ chỉ được luân chuyển tiến" (E-2)** | | X | | |
| **H3: Hiển thị cảnh báo đỏ bên dưới hộp thoại: "Ghi chú xử lý tối thiểu từ 10 ký tự" (E-3)** | | | X | |
| **H4: Cập nhật vị trí thẻ sang cột mới thành công, dừng đồng hồ SLA (nếu Resolved)** | | | | X |

---
---

##### 3. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 4.3 - Luồng chính** | Kéo thả thẻ công việc tiến lên theo đúng thứ tự 1 chiều | `TC_DIS_08` |
| **UC 4.3 - E-1** | Bẫy lỗi Agent cố tình kéo thả thẻ do nhân viên khác phụ trách | `TC_DIS_09` |
| **UC 4.3 - E-2** | Bẫy lỗi kéo ngược lùi trạng thái thẻ công việc | `TC_DIS_10` |
| **UC 4.3 - E-3** | Báo lỗi khi ghi chú xử lý ngắn hơn 10 ký tự | `TC_DIS_11` |
| **UC 4.3 - Rule 1** | Quản lý/Admin có toàn quyền kéo thả thẻ công việc bất kỳ | `TC_DIS_12` |

##### 4. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_08** | Kiểm tra kéo thả thẻ tiến lên hợp lệ (Happy Path) | Đăng nhập Nhân viên A, có phiếu X ở cột `Đang xử lý` | 1. Kéo thả thẻ phiếu X từ cột `Đang xử lý` sang cột `Đã giải quyết`.<br>2. Tại hộp thoại hiện lên, nhập ghi chú xử lý hợp lệ.<br>3. Bấm "Xác nhận hoàn thành". | Ghi chú: `"Đã kiểm tra và hoàn tiền đơn hàng cho khách"` (40 ký tự) (V) | Thẻ nằm cố định ở cột `Đã giải quyết`, dừng đồng hồ SLA. Hiển thị thông báo xanh thành công. | Pass |
| **TC_DIS_09** | Kiểm tra chặn Agent kéo thả thẻ do nhân viên khác phụ trách (E-1) | Đăng nhập Nhân viên A, màn hình có phiếu Y của Nhân viên B | 1. Thử kéo thả thẻ phiếu Y của Nhân viên B sang cột khác. | Thao tác trên thẻ Nhân viên B (I) | Thẻ nảy trượt trở lại vị trí cột cũ. Hiển thị báo lỗi: *"Bạn không có quyền cập nhật phiếu do nhân viên khác phụ trách"*. | Pass |
| **TC_DIS_10** | Kiểm tra chặn kéo lùi trạng thái thẻ công việc (E-2) | Đăng nhập Nhân viên A, phiếu X ở cột `Đang xử lý` | 1. Kéo thả thẻ phiếu X từ cột `Đang xử lý` lùi về cột `Chờ tiếp nhận`. | Kéo lùi trạng thái (I) | Thẻ nảy về cột cũ `Đang xử lý`. Hiển thị báo lỗi: *"Tiến độ chỉ được phép luân chuyển tiến lên"*. | Pass |
| **TC_DIS_11** | Kiểm tra báo lỗi khi ghi chú xử lý ngắn hơn 10 ký tự (E-3) | Đang mở hộp thoại hoàn thành phiếu ở cột `Đã giải quyết` | 1. Nhập 3 ký tự vào ô ghi chú xử lý.<br>2. Bấm "Xác nhận hoàn thành". | Ghi chú: `"Xong"` (4 ký tự) (I) | Viền ô nhập hằn đỏ, hiển thị cảnh báo: *"Ghi chú xử lý sự cố bắt buộc từ 10 đến 1000 ký tự"*. Hệ thống chặn thao tác chuyển thẻ. | Pass |
| **TC_DIS_12** | Kiểm tra Quản lý có toàn quyền kéo thả thẻ công việc | Đăng nhập tài khoản Quản lý, chọn phiếu Y của Nhân viên B | 1. Kéo thả thẻ phiếu Y sang cột `Đã giải quyết`.<br>2. Nhập ghi chú xử lý và bấm Xác nhận. | Thao tác bởi Quản lý (V) | Kéo thả thành công, hộp thoại cập nhật trạng thái xuất hiện cho phép Quản lý ghi đè ghi chú xử lý mà không bị chặn quyền. | Pass |

---

### Use case 4.4: Báo cáo thống kê hiệu suất {#uc-4-4}

| Thuộc tính | Nội dung đặc tả chi tiết |
| :--- | :--- |
| **Tác nhân** | Quản lý CSKH, Quản trị viên |
| **Điều kiện bắt đầu** | 1. Người dùng đã đăng nhập vào hệ thống bằng tài khoản có vai trò Quản lý CSKH hoặc Quản trị viên.<br>2. Hệ thống đã có dữ liệu về các cuộc trò chuyện và các phiếu hỗ trợ đã phát sinh trong quá trình vận hành. |
| **Luồng sự kiện chính (Lọc và xem biểu đồ số liệu vận hành tổng hợp)** | 1. Người dùng chọn mục "Báo cáo thống kê" trên thanh điều hướng quản trị.<br>2. Hệ thống hiển thị màn hình bộ lọc gồm các trường thông tin đầu vào với quy chuẩn kiểm thử cụ thể:<br>• Khoảng thời gian (Từ ngày - Đến ngày): Trường bắt buộc; định dạng ngày chuẩn DD/MM/YYYY. Ràng buộc biên: T_bắt_đầu <= T_kết_thúc, T_kết_thúc <= T_hiện_tại, và khoảng cách thời gian ΔT = T_kết_thúc - T_bắt_đầu <= 365 ngày.<br>• Nhân viên phụ trách: Trường tùy chọn; chuỗi ký tự chọn từ danh sách nhân viên hiện có hoặc mặc định "Tất cả nhân viên".<br>• Mức độ ưu tiên: Trường tùy chọn; lọc theo một trong các giá trị P1, P2, P3 hoặc mặc định "Tất cả các mức".<br>• Danh mục sự cố: Trường tùy chọn; chọn một trong sáu danh mục sự cố hợp lệ hoặc mặc định "Tất cả danh mục". (Lưu ý: Người dùng có thể sử dụng các nút chọn nhanh khoảng thời gian có sẵn bằng cách thực hiện Luồng con A-1).<br>3. Người dùng thiết lập các tiêu chí lọc mong muốn và nhấn nút "Lọc dữ liệu". Nút bấm tạm thời chuyển sang trạng thái mờ kèm biểu tượng "Đang tải dữ liệu..." để tránh bấm lặp thao tác.<br>4. Hệ thống kiểm tra tính hợp lệ của khoảng thời gian đã nhập theo các quy chuẩn dữ liệu (định dạng DD/MM/YYYY, T_bắt_đầu <= T_kết_thúc, T_kết_thúc <= T_hiện_tại, và ΔT <= 365 ngày). Nếu vi phạm bất kỳ điều kiện nào, hệ thống thực hiện luồng rẽ nhánh E-1.<br>5. Nếu kết nối máy chủ bị gián đoạn khi đang truy xuất dữ liệu, hệ thống thực hiện luồng rẽ nhánh E-2.<br>6. Hệ thống tổng hợp toàn bộ các phiếu hỗ trợ phát sinh trong khoảng thời gian thỏa mãn điều kiện lọc. Nếu không có dữ liệu nào phát sinh, hệ thống thực hiện luồng rẽ nhánh E-3.<br>7. Hệ thống tính toán các chỉ số vận hành cốt lõi:<br>• Tổng số phiếu phát sinh (N_tổng), số phiếu đã giải quyết (N_giải_quyết), số phiếu đang xử lý (N_đang_xử_lý), số phiếu vi phạm cam kết thời gian (N_vi_phạm).<br>• Tỷ lệ vi phạm cam kết SLA: Công thức tính toán cụ thể: Tỷ lệ vi phạm (%) = (N_vi_phạm / N_tổng) * 100%. Nếu N_tổng = 0, Tỷ lệ vi phạm = 0%.<br>• Tỷ lệ phân bổ cảm xúc của khách hàng (Tích cực, Bình thường, Tiêu cực nhẹ, Bức xúc cao).<br>8. Đầu ra: Hệ thống hiển thị kết quả gồm các khối số liệu tổng quan nổi bật ở trên cùng, biểu đồ tròn phân bổ mức độ cam kết xử lý và biểu đồ cột so sánh năng suất giải quyết giữa các nhân viên. Góc màn hình hiển thị nút "Xuất báo cáo" (cho phép xuất dữ liệu ra tệp bảng tính excel để lưu trữ). |
| **Luồng con (A-1: Chọn nhanh khoảng thời gian thống kê)** | 1. Tại bước 2 của luồng chính, thay vì tự chọn từng ngày trên lịch, người dùng bấm vào một trong các nút chọn mốc thời gian nhanh gồm: "Hôm nay", "7 ngày qua", "30 ngày qua", hoặc "Tháng này".<br>2. Hệ thống tự động tính toán và điền chính xác giá trị vào hai ô "Từ ngày" và "Đến ngày" theo định dạng DD/MM/YYYY tương ứng, đảm bảo các ràng buộc T_bắt_đầu <= T_kết_thúc, T_kết_thúc <= T_hiện_tại và ΔT <= 365 ngày.<br>3. Người dùng kiểm tra lại và nhấn nút "Lọc dữ liệu" để tiếp tục từ bước 3 của luồng chính. |
| **Luồng rẽ nhánh (Ngoại lệ)** | E-1: Khoảng thời gian lọc không hợp lệ<br>1. Hệ thống kiểm tra và phát hiện lỗi dữ liệu thời gian vi phạm quy chuẩn (sai định dạng DD/MM/YYYY, T_bắt_đầu > T_kết_thúc, T_kết_thúc > T_hiện_tại, hoặc ΔT > 365 ngày).<br>2. Hệ thống làm sáng viền đỏ tại ô thời gian bị sai và hiển thị câu thông báo lỗi cụ thể ngay dưới chân ô nhập liệu (Ví dụ: "Ngày nhập không đúng định dạng DD/MM/YYYY", "Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc", "Ngày kết thúc không được vượt quá ngày hiện tại", hoặc "Khoảng thời gian tra cứu tối đa không vượt quá 365 ngày").<br>3. Hệ thống giữ nguyên nút "Lọc dữ liệu" ở trạng thái mờ và giữ nguyên các giá trị bộ lọc đã chọn khác.<br>4. Người dùng điều chỉnh lại khoảng thời gian hợp lệ theo chỉ dẫn và quay lại bước 3 của luồng chính.<br><br>E-2: Gián đoạn kết nối khi tải số liệu thống kê<br>1. Hệ thống không thể tải dữ liệu báo cáo do lỗi đường truyền mạng hoặc máy chủ không phản hồi.<br>2. Hệ thống hiển thị hộp cảnh báo màu vàng cam ở giữa khung báo cáo: "Không thể tải dữ liệu báo cáo do mất kết nối. Vui lòng kiểm tra lại đường truyền và thử lại!" kèm nút bấm "Thử lại".<br>3. Người dùng bấm "Thử lại", hệ thống gửi lại yêu cầu truy xuất từ bước 3 của luồng chính.<br><br>E-3: Không có dữ liệu phát sinh trong khoảng thời gian lọc<br>1. Trong khoảng thời gian người dùng chọn, hệ thống không ghi nhận bất kỳ phiếu hỗ trợ hay lượt khiếu nại nào phát sinh (N_tổng = 0).<br>2. Hệ thống tạm ẩn các biểu đồ phân tích, hiển thị hình ảnh minh họa cùng dòng chữ thông báo: "Không có dữ liệu phiếu hỗ trợ nào phát sinh trong khoảng thời gian đã chọn".<br>3. Các ô số liệu tổng quan hiển thị giá trị mặc định N_tổng = 0, N_giải_quyết = 0, N_đang_xử_lý = 0, N_vi_phạm = 0 và Tỷ lệ vi phạm SLA = 0%.<br>4. Người dùng có thể chọn lại khoảng thời gian khác rộng hơn để tiếp tục tra cứu. |
| **Quy tắc Nghiệp vụ (Business Rules / Logic)** | 1. Phân quyền truy xuất số liệu: Báo cáo thống kê vận hành chỉ được cung cấp cho tài khoản có vai trò Quản lý CSKH hoặc Quản trị viên hệ thống. Nhân viên tư vấn thông thường không có quyền truy cập vào màn hình này để bảo mật dữ liệu hiệu suất của toàn chuỗi.<br>2. Phạm vi tính toán báo cáo: Một phiếu hỗ trợ được tính vào báo cáo nếu thời điểm khởi tạo phiếu nằm trong khoảng thời gian lọc (tính từ 00:00:00 của ngày bắt đầu T_bắt_đầu đến 23:59:59 của ngày kết thúc T_kết_thúc). Các phiếu bị hủy bỏ hoặc đánh dấu rác/trùng lặp sẽ bị loại trừ.<br>3. Quy chuẩn tính tỷ lệ vi phạm cam kết SLA: Tỷ lệ vi phạm được tính theo công thức Tỷ lệ vi phạm (%) = (N_vi_phạm / N_tổng) * 100%, kết quả hiển thị theo dạng phần trăm (%) và được làm tròn đến một chữ số thập phân. Trường hợp N_tổng = 0 thì tỷ lệ mặc định hiển thị là 0%.<br>4. Tính khách quan của dữ liệu: Toàn bộ số liệu và biểu đồ trên màn hình báo cáo là dữ liệu chỉ xem (Read-only). Người dùng không được phép chỉnh sửa số liệu trực tiếp trên bảng thống kê để đảm bảo tính minh bạch và chính xác trong việc đánh giá nhân sự. |

#### **Kiểm thử hộp đen Use case 4.4: Báo cáo thống kê hiệu suất**

##### 1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)


| Trường dữ liệu / Chỉ số | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Khoảng thời gian tra cứu (Delta)** | • Ngày bắt đầu phải nhỏ hơn hoặc bằng Ngày kết thúc (`from_date <= to_date`)<br>• Khoảng cách giữa 2 mốc tối đa **365 ngày**<br>• Không chọn mốc trong tương lai | **V_DATE_01:** Khoảng thời gian hợp lệ từ 0 đến 365 ngày (VD: 30 ngày qua)<br>**V_DATE_02:** Chọn nút mốc thời gian nhanh ("7 ngày qua", "30 ngày qua") | **I_DATE_01:** Để trống ngày bắt đầu hoặc ngày kết thúc<br>**I_DATE_02:** Ngày bắt đầu lớn hơn Ngày kết thúc (`from_date > to_date`) (E-1)<br>**I_DATE_03:** Khoảng cách thời gian vượt quá 365 ngày (VD: 366 ngày)<br>**I_DATE_04:** Chọn mốc ngày trong tương lai | • Biên khoảng cách: -1 ngày (Bắt đầu > Kết thúc) (I), 0 ngày (Trùng ngày) (V), 364 ngày (V), 365 ngày (V), 366 ngày (I) |
| **Quyền xem báo cáo thống kê** | • Chỉ dành riêng cho vai trò Quản lý (Manager) hoặc Quản trị viên (Admin) | **V_AUTH_01:** Đăng nhập tài khoản Quản lý / Admin | **I_AUTH_01:** Đăng nhập tài khoản Agent thông thường $→$ Chặn truy cập | Phân quyền truy cập |

---

##### 2. Bảng quyết định (Decision Table)


*(Tiền đề quy trình: Quản lý/Admin bấm nút "Lọc dữ liệu" hoặc "Xuất báo cáo Excel")*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **C1: Người thao tác có quyền Quản lý (Manager) hoặc Quản trị viên (Admin)?** | F | T | T | T | T |
| **C2: Khoảng thời gian chọn hợp lệ (Ngày bắt đầu <= Ngày kết thúc)?** | - | F | T | T | T |
| **C3: Khoảng cách giữa 2 mốc thời gian không vượt quá 365 ngày (Delta <= 365)?** | - | - | F | T | T |
| **C4: Khoảng thời gian tra cứu có tồn tại dữ liệu phiếu hỗ trợ trong CSDL?** | - | - | - | F | T |
| **H1: Chặn truy cập, hiển thị thông báo lỗi "Bạn không có quyền xem báo cáo"** | X | | | | |
| **H2: Hiển thị lỗi khoanh đỏ ô ngày: "Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc" (E-1)** | | X | | | |
| **H3: Hiển thị lỗi khoanh đỏ ô ngày: "Khoảng thời gian tra cứu tối đa không vượt quá 365 ngày"** | | | X | | |
| **H4: Tạm ẩn biểu đồ, hiển thị hình minh họa trống "Không có dữ liệu phiếu hỗ trợ..." (E-3)** | | | | X | |
| **H5: Hiển thị biểu đồ tròn/cột phân tích & Kích hoạt nút "Xuất báo cáo Excel" sáng lên** | | | | | X |

---
---


| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 4.1 - Luồng chính** | Tự động phân công Ticket cho nhân viên rảnh nhất & đúng kỹ năng | `TC_DIS_01` |
| **UC 4.1 - Rule 4** | Xử lý trường hợp trùng tải (Giao cho người có thời gian chờ việc lâu hơn) | `TC_DIS_02` |
| **UC 4.1 - E-1** | Bẫy lỗi thiếu nhân viên ONLINE hoặc không có nhân viên đúng kỹ năng | `TC_DIS_03` |
| **UC 4.2 - Luồng chính** | Đồng hồ đếm ngược SLA ở trạng thái màu sắc Bình thường | `TC_DIS_04` |
| **UC 4.2 - Rule 3** | Kích hoạt trạng thái Cảnh báo màu cam khi thời gian SLA còn $< 20\%$ | `TC_DIS_05` |
| **UC 4.2 - E-1** | Quá hạn SLA (0 giây) $→$ Thẻ chuyển màu đỏ nhấp nháy & bắn báo động | `TC_DIS_06` |
| **UC 4.2 - Rule 1** | Dừng đồng hồ SLA đúng hạn khi nhân viên bấm "Xác nhận đã xử lý" | `TC_DIS_07` |
| **UC 4.3 - Luồng chính** | Kéo thả thẻ công việc tiến lên theo đúng thứ tự 1 chiều | `TC_DIS_08` |
| **UC 4.3 - E-1** | Bẫy lỗi Agent cố tình kéo thả thẻ do nhân viên khác phụ trách | `TC_DIS_09` |
| **UC 4.3 - E-2** | Bẫy lỗi kéo ngược lùi trạng thái thẻ công việc | `TC_DIS_10` |
| **UC 4.3 - E-3** | Báo lỗi khi ghi chú xử lý ngắn hơn 10 ký tự | `TC_DIS_11` |
| **UC 4.3 - Rule 1** | Quản lý/Admin có toàn quyền kéo thả thẻ công việc bất kỳ | `TC_DIS_12` |
| **UC 4.4 - Luồng chính** | Lọc dữ liệu báo cáo thành công & Hiển thị biểu đồ phân tích | `TC_DIS_13` |
| **UC 4.4 - BVA** | Kiểm tra mốc lọc đúng điểm biên tối đa 365 ngày | `TC_DIS_14` |
| **UC 4.4 - E-1** | Báo lỗi khi chọn Ngày bắt đầu lớn hơn Ngày kết thúc | `TC_DIS_15` |
| **UC 4.4 - BVA** | Báo lỗi khi chọn khoảng thời gian vượt biên (366 ngày) | `TC_DIS_16` |
| **UC 4.4 - E-3** | Mốc thời gian tra cứu không có dữ liệu | `TC_DIS_17` |

---
---



| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_01** | Kiểm tra tự động giao Ticket cho nhân viên có ít việc nhất (Happy Path) | Nhân viên A có 1 Ticket đang mở, Nhân viên B có 3 Ticket. Cả 2 đang ONLINE & đúng kỹ năng. | 1. Tạo một phiếu hỗ trợ khẩn cấp P1.<br>2. Đăng nhập tài khoản Nhân viên A và kiểm tra màn hình Bàn làm việc. | Ticket P1, Danh mục `Lỗi đơn hàng` (V) | Hệ thống tự động gán thẳng phiếu hỗ trợ P1 cho Nhân viên A. Phiếu xuất hiện trên màn hình Bàn làm việc của Nhân viên A ở trạng thái *Đang xử lý (In Progress)*. | Pass |
| **TC_DIS_02** | Kiểm tra xử lý trùng tải công việc (Chọn người có thời gian chờ rảnh lâu hơn) | Nhân viên A và B cùng gánh 2 Ticket. Nhân viên A rảnh 30 phút, Nhân viên B rảnh 5 phút. | 1. Tạo một phiếu hỗ trợ P2.<br>2. Đăng nhập kiểm tra màn hình của cả 2 nhân viên. | Ticket P2, Danh mục `Sản phẩm lỗi` (V) | Phiếu hỗ trợ P2 được tự động gán cho Nhân viên A (do thời gian chờ việc lâu hơn Nhân viên B). | Pass |
| **TC_DIS_03** | Kiểm tra xử lý khi không có nhân viên trực tuyến đúng kỹ năng (E-1) | Nhân viên A (đúng kỹ năng) OFFLINE. Nhân viên B (sai kỹ năng) ONLINE. | 1. Tạo một phiếu hỗ trợ P1 danh mục `Đổi trả/Hoàn tiền`.<br>2. Đăng nhập tài khoản Quản lý quan sát màn hình. | Ticket P1, Danh mục `Đổi trả/Hoàn tiền` (I) | Màn hình của Quản lý bật thông báo cảnh báo đỏ. Ticket bị giữ ở trạng thái *Chờ tiếp nhận (Pending)* không có người nhận để Quản lý gán thủ công. | Pass |

---


| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_04** | Kiểm tra đồng hồ đếm ngược SLA ở trạng thái màu sắc Bình thường | Ticket P1 vừa được gán sang trạng thái *Đang xử lý* | 1. Đăng nhập tài khoản Nhân viên CSKH.<br>2. Quan sát thẻ công việc của phiếu P1. | Thời gian còn lại = 900 giây (15 phút) | Thẻ hiển thị đồng hồ đếm ngược từ 15:00. Nền thẻ và đồng hồ hiển thị màu sắc Bình thường. | Pass |
| **TC_DIS_05** | Kiểm tra kích hoạt Cảnh báo màu cam tại mốc $< 20\%$ SLA (180 giây) | Ticket P1 đang chạy đồng hồ đếm ngược | 1. Quan sát đồng hồ đếm ngược trên thẻ phiếu P1.<br>2. Chờ cho đến khi đồng hồ nhảy xuống mốc 03:00 (đúng 180 giây). | Thời gian còn lại = 180 giây (V) | Thẻ và đồng hồ đếm ngược lập tức đổi sang **tông màu Vàng Cam cảnh báo** chính xác tại mốc 180 giây. | Pass |
| **TC_DIS_06** | Kiểm tra vi phạm quá hạn SLA tại mốc 0 giây (E-1) | Phiên chat đang ở trạng thái Cảnh báo màu cam | 1. Giữ nguyên không bấm xử lý phiếu P1.<br>2. Quan sát đồng hồ khi trôi về mốc 00:00. | Thời gian còn lại = 0 giây (I) | Thẻ chuyển sang **màu Đỏ nhấp nháy**, hệ thống phát âm thanh báo động vi phạm và gửi cảnh báo đỏ lên màn hình Quản lý. Ghi nhận trừ điểm SLA của nhân viên. | Pass |
| **TC_DIS_07** | Kiểm tra dừng đồng hồ SLA khi bấm hoàn thành đúng hạn | Ticket đang đếm ngược ở mốc Cảnh báo màu cam | 1. Nhấn nút "Xác nhận đã xử lý" trên thẻ phiếu P1.<br>2. Nhập ghi chú xử lý hợp lệ và bấm Xác nhận khi đồng hồ còn $> 0$s. | Ghi chú hợp lệ, thời gian còn lại = 45s (V) | Ghi nhận Hoàn thành Đúng hạn (SLA Met). Đồng hồ SLA ngừng đếm ngược lập tức và thẻ hiển thị đánh dấu màu xanh lá. | Pass |

---


| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_08** | Kiểm tra kéo thả thẻ tiến lên hợp lệ (Happy Path) | Đăng nhập Nhân viên A, có phiếu X ở cột `Đang xử lý` | 1. Kéo thả thẻ phiếu X từ cột `Đang xử lý` sang cột `Đã giải quyết`.<br>2. Tại hộp thoại hiện lên, nhập ghi chú xử lý hợp lệ.<br>3. Bấm "Xác nhận hoàn thành". | Ghi chú: `"Đã kiểm tra và hoàn tiền đơn hàng cho khách"` (40 ký tự) (V) | Thẻ nằm cố định ở cột `Đã giải quyết`, dừng đồng hồ SLA. Hiển thị thông báo xanh thành công. | Pass |
| **TC_DIS_09** | Kiểm tra chặn Agent kéo thả thẻ do nhân viên khác phụ trách (E-1) | Đăng nhập Nhân viên A, màn hình có phiếu Y của Nhân viên B | 1. Thử kéo thả thẻ phiếu Y của Nhân viên B sang cột khác. | Thao tác trên thẻ Nhân viên B (I) | Thẻ nảy trượt trở lại vị trí cột cũ. Hiển thị báo lỗi: *"Bạn không có quyền cập nhật phiếu do nhân viên khác phụ trách"*. | Pass |
| **TC_DIS_10** | Kiểm tra chặn kéo lùi trạng thái thẻ công việc (E-2) | Đăng nhập Nhân viên A, phiếu X ở cột `Đang xử lý` | 1. Kéo thả thẻ phiếu X từ cột `Đang xử lý` lùi về cột `Chờ tiếp nhận`. | Kéo lùi trạng thái (I) | Thẻ nảy về cột cũ `Đang xử lý`. Hiển thị báo lỗi: *"Tiến độ chỉ được phép luân chuyển tiến lên"*. | Pass |
| **TC_DIS_11** | Kiểm tra báo lỗi khi nhập ghi chú xử lý ngắn hơn 10 ký tự (E-3) | Đang mở hộp thoại hoàn thành phiếu ở cột `Đã giải quyết` | 1. Nhập 3 ký tự vào ô ghi chú xử lý.<br>2. Bấm "Xác nhận hoàn thành". | Ghi chú: `"Xong"` (4 ký tự) (I) | Viền ô nhập hằn đỏ, hiển thị cảnh báo: *"Ghi chú xử lý sự cố bắt buộc từ 10 đến 1000 ký tự"*. Hệ thống chặn thao tác chuyển thẻ. | Pass |
| **TC_DIS_12** | Kiểm tra Quản lý có toàn quyền kéo thả thẻ công việc | Đăng nhập tài khoản Quản lý, chọn phiếu Y của Nhân viên B | 1. Kéo thả thẻ phiếu Y sang cột `Đã giải quyết`.<br>2. Nhập ghi chú xử lý và bấm Xác nhận. | Thao tác bởi Quản lý (V) | Kéo thả thành công, hộp thoại cập nhật trạng thái xuất hiện cho phép Quản lý ghi đè ghi chú xử lý mà không bị chặn quyền. | Pass |

---


| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_13** | Kiểm tra lọc báo cáo thống kê hợp lệ (Happy Path) | Đăng nhập tài khoản Quản lý, đang ở màn hình Báo cáo | 1. Click chọn nút lọc nhanh mốc thời gian "30 ngày qua".<br>2. Bấm nút "Lọc dữ liệu". | Mốc "30 ngày qua" (V) | Hiển thị đầy đủ biểu đồ tròn/cột phân tích và bảng số liệu thống kê. Nút "Xuất báo cáo Excel" sáng lên cho phép bấm tải file. | Pass |
| **TC_DIS_14** | Kiểm tra lọc dữ liệu đúng điểm biên 365 ngày (BVA Max) | Đang ở màn hình Báo cáo | 1. Chọn Ngày bắt đầu là 01/01/2026.<br>2. Chọn Ngày kết thúc là 31/12/2026 (khoảng cách đúng 365 ngày).<br>3. Bấm "Lọc dữ liệu". | Delta = 365 ngày (V) | Dữ liệu báo cáo được tải thành công, hiển thị trọn vẹn số liệu phân tích của nguyên 365 ngày. | Pass |
| **TC_DIS_15** | Kiểm tra báo lỗi chọn Ngày bắt đầu lớn hơn Ngày kết thúc (E-1) | Đang ở màn hình Báo cáo | 1. Chọn Ngày bắt đầu là 15/10/2026.<br>2. Chọn Ngày kết thúc là 01/10/2026.<br>3. Bấm "Lọc dữ liệu". | `from_date > to_date` (I) | Giữ nguyên giao diện biểu đồ cũ. Khoanh viền đỏ ô ngày tháng và báo lỗi: *"Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc"*. | Pass |
| **TC_DIS_16** | Kiểm tra báo lỗi khi chọn khoảng thời gian vượt quá 365 ngày (BVA Max+) | Đang ở màn hình Báo cáo | 1. Chọn Ngày bắt đầu là 01/01/2026.<br>2. Chọn Ngày kết thúc là 01/01/2027 (khoảng cách 366 ngày).<br>3. Bấm "Lọc dữ liệu". | Delta = 366 ngày (I) | Báo lỗi khoanh đỏ ô ngày tháng: *"Khoảng thời gian tra cứu tối đa không được vượt quá 365 ngày"*. Chặn thao tác lọc. | Pass |
| **TC_DIS_17** | Kiểm tra hiển thị giao diện khi mốc thời gian không có dữ liệu (E-3) | Đang ở màn hình Báo cáo | 1. Chọn khoảng thời gian rơi vào ngày nghỉ lễ không có dữ liệu.<br>2. Bấm "Lọc dữ liệu". | Khoảng thời gian trống dữ liệu | Tạm ẩn các biểu đồ tròn/cột, hiển thị hình minh họa trống kèm thông báo: *"Không có dữ liệu phiếu hỗ trợ trong khoảng thời gian này"*. Các chỉ số đo lường trả về 0. | Pass |

---
*Tài liệu kiểm thử hộp đen Khối chức năng 4 được chuẩn hóa hoàn thiện 100%, bổ sung đầy đủ EP/BVA, Decision Table, State Transition, RTM và bộ 17 Test Cases chuẩn IEEE.*

##### 3. Ma trận truy xuất nguồn gốc ca kiểm thử (RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 4.4 - Luồng chính** | Lọc dữ liệu báo cáo thành công & Hiển thị biểu đồ phân tích | `TC_DIS_13` |
| **UC 4.4 - BVA** | Kiểm tra mốc lọc đúng điểm biên tối đa 365 ngày | `TC_DIS_14` |
| **UC 4.4 - E-1** | Báo lỗi khi chọn Ngày bắt đầu lớn hơn Ngày kết thúc | `TC_DIS_15` |
| **UC 4.4 - BVA** | Báo lỗi khi chọn khoảng thời gian vượt biên (366 ngày) | `TC_DIS_16` |
| **UC 4.4 - E-3** | Mốc thời gian tra cứu không có dữ liệu | `TC_DIS_17` |

##### 4. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_13** | Kiểm tra lọc báo cáo thống kê hợp lệ (Happy Path) | Đăng nhập tài khoản Quản lý, đang ở màn hình Báo cáo | 1. Click chọn nút lọc nhanh mốc thời gian "30 ngày qua".<br>2. Bấm nút "Lọc dữ liệu". | Mốc "30 ngày qua" (V) | Hiển thị đầy đủ biểu đồ tròn/cột phân tích và bảng số liệu thống kê. Nút "Xuất báo cáo Excel" sáng lên cho phép bấm tải file. | Pass |
| **TC_DIS_14** | Kiểm tra lọc dữ liệu đúng điểm biên 365 ngày (BVA Max) | Đang ở màn hình Báo cáo | 1. Chọn Ngày bắt đầu là 01/01/2026.<br>2. Chọn Ngày kết thúc là 31/12/2026 (khoảng cách đúng 365 ngày).<br>3. Bấm "Lọc dữ liệu". | Delta = 365 ngày (V) | Dữ liệu báo cáo được tải thành công, hiển thị trọn vẹn số liệu phân tích của nguyên 365 ngày. | Pass |
| **TC_DIS_15** | Kiểm tra báo lỗi chọn Ngày bắt đầu lớn hơn Ngày kết thúc (E-1) | Đang ở màn hình Báo cáo | 1. Chọn Ngày bắt đầu là 15/10/2026.<br>2. Chọn Ngày kết thúc là 01/10/2026.<br>3. Bấm "Lọc dữ liệu". | `from_date > to_date` (I) | Giữ nguyên giao diện biểu đồ cũ. Khoanh viền đỏ ô ngày tháng và báo lỗi: *"Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc"*. | Pass |
| **TC_DIS_16** | Kiểm tra báo lỗi khi chọn khoảng thời gian vượt quá 365 ngày (BVA Max+) | Đang ở màn hình Báo cáo | 1. Chọn Ngày bắt đầu là 01/01/2026.<br>2. Chọn Ngày kết thúc là 01/01/2027 (khoảng cách 366 ngày).<br>3. Bấm "Lọc dữ liệu". | Delta = 366 ngày (I) | Báo lỗi khoanh đỏ ô ngày tháng: *"Khoảng thời gian tra cứu tối đa không được vượt quá 365 ngày"*. Chặn thao tác lọc. | Pass |
| **TC_DIS_17** | Kiểm tra hiển thị giao diện khi mốc thời gian không có dữ liệu (E-3) | Đang ở màn hình Báo cáo | 1. Chọn khoảng thời gian rơi vào ngày nghỉ lễ không có dữ liệu.<br>2. Bấm "Lọc dữ liệu". | Khoảng thời gian trống dữ liệu | Tạm ẩn các biểu đồ tròn/cột, hiển thị hình minh họa trống kèm thông báo: *"Không có dữ liệu phiếu hỗ trợ trong khoảng thời gian này"*. Các chỉ số đo lường trả về 0. | Pass |

---
