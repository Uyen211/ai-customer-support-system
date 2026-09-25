* Lỗi 1 (Cấu trúc): Tệp quá ngắn (chỉ 100 dòng), bị CẮT XÉN 70% nội dung. Thiếu bảng Test Case IEEE chi tiết cho UC 2.1, UC 2.2, UC 2.3.  
* Lỗi 2 (EP/BVA): Thiếu bảng EP/BVA cho UC 2.2 (Trích xuất thông tin & Tạo ticket khẩn cấp: tóm tắt 20-255 ký tự, thời gian SLA 15m/60m/240m).  
* Lỗi 3 (Decision Table):  
  * Bảng UC 2.3: Đưa P1 Threshold và P2 Threshold là số hợp lệ thành 1 condition gộp.  
  * Bảng UC 2.1 & 2.2: Trộn lẫn logic ngắt bot và tạo ticket nhưng không tách rõ chốt chặn logic.

## 

## 1\. Phân tích Đặc tả & Thiết kế kiểm thử

### 1.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

**A. Form Cấu hình Quy tắc Cảnh báo (UC 2.3)**

| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :---- | :---- | :---- | :---- | :---- |
| Instruction Prompt | Chuỗi văn bản, 0 đến 2000 ký tự | V1:  0≤len≤2000 0≤*len*≤2000 | I1:  len\>2000 *len*\>2000 | 0, 1, 2000, 2001 (ký tự) |
| P1 Threshold | Số thực (Float), \[-1.00, \-0.01\] | V2:  −1.00≤x≤−0.01 −1.00≤*x*≤−0.01 | I2:  x\<−1.00 *x*\<−1.00 I3:  x\>−0.01 *x*\>−0.01 I4: Để trống / Ký tự chữ | \-1.01, \-1.00 \-0.01, 0.00 |
| P2 Threshold | Số thực (Float), \[-0.99, 0.00\] | V3:  −0.99≤x≤0.00 −0.99≤*x*≤0.00 | I5:  x\<−0.99 *x*\<−0.99 I6:  x\>0.00 *x*\>0.00 I7: Để trống / Ký tự chữ | \-1.00, \-0.99 0.00, 0.01 |
| *Ràng buộc chéo* | P1 Threshold \< P2 Threshold | V4: Giá trị P1 \< P2 | I8: P1  ≥ ≥ P2 | P1=−0.50,P2=−0.50 *P*1=−0.50,*P*2=−0.50 |

**B. Thông số Động cơ SLA (UC 2.4)**

| Tên trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ (V) | Phân vùng không hợp lệ (I) | Điểm biên cần test |
| :---- | :---- | :---- | :---- | :---- |
| Giờ mở/đóng cửa | Định dạng HH:MM, không trống | V1: Đúng định dạng 24h | I1: Trống I2: Sai định dạng (VD: 25:00) | 00:00, 23:59 |
| Ngày làm việc | Mảng số nguyên, giá trị \[1..7\] | V2: Các số  ∈\[1,7\] ∈\[1,7\] | I3: Chứa số  \<1 \<1 hoặc  \>7 \>7 | 0, 1, 7, 8 |
| Định mức SLA (M) | Số nguyên dương, \[1, 10080\] phút | V3:  1≤x≤10080 1≤*x*≤10080 | I4:  x\<1 *x*\<1 I5:  x\>10080 *x*\>10080 I6: Chữ / Số thập phân | 0, 1, 10080, 10081 |

### 1.2. Bảng quyết định (Decision Table)

**A. Bảng quyết định cho Luồng phân loại cấp độ Sự cố khẩn cấp (UC 2.1 & UC 2.2)** *(Áp dụng quy tắc thu gọn Don't Care cho các điều kiện phi lý hoặc bị ghi đè)*

| Thành phần | Điều kiện / Hành động | R1 ​ | R2  | R3 | R4  ​ | R5  ​ | R6 ​ |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Conditions** | *C1*: Thuộc danh mục Cấp cứu (Ngộ độc/Sức khỏe)?  | **F** | **F** | **F** | **F** | **T** | **T** |
|  | *C* 2 ​ : Điểm cảm xúc  S≤−0.60 *S*≤−0.60 (Chạm P1)?  | **F** | **F** | **T** | **T** | \- | \- |
|  | C3 *C* 3 ​ : Điểm cảm xúc  −0.60\<S≤−0.30 −0.60\<*S*≤−0.30 (Chạm P2)? | **F** | **T** | F | F | \- | \- |
|  | C4 *C* 4 ​ : Có Phiếu hỗ trợ P2 chưa giải quyết? | \- | \- | **F** | **T** | **F** | **T** |
| **Actions** | A1 *A* 1 ​ : Không tạo Ticket (Bỏ qua) | **X** |  |  |  |  |  |
|  | A2 *A* 2 ​ : Tạo MỚI Ticket P2 |  | **X** |  |  |  |  |
|  | A3 *A* 3 ​ : Tạo MỚI Ticket P1 |  |  | **X** |  | **X** |  |
|  | A4 *A* 4 ​ : Cập nhật/Leo thang Ticket cũ từ P2 lên P1 |  |  |  | **X** |  | **X** |

**B. Bảng quyết định cho Động cơ tính toán SLA (UC 2.4)** *(Giả định Ca làm việc: 08:00 \- 18:00, Thứ 2 \- Thứ 6\)*

| Thành phần | Điều kiện / Hành động | R1 *R* 1 ​ | R2 *R* 2 ​ | R3 *R* 3 ​ |
| :---- | :---- | :---- | :---- | :---- |
| **Conditions** | C1 *C* 1 ​ : Thời điểm phát sinh  T0 *T* 0 ​  nằm NGÀY NGHỈ hoặc NGOÀI CA trực? | **F** | **T** | **F** |
|  | C2 *C* 2 ​ : Thời điểm dự kiến  Tend=T0+M *T end* ​ \=*T* 0 ​ \+*M* VƯỢT QUÁ giờ kết thúc ca 18:00? | **F** | \- | **T** |
| **Actions** | A1 *A* 1 ​ : Chốt Deadline là  T0+M *T* 0 ​ \+*M* (Cùng ngày) | **X** |  |  |
|  | A2 *A* 2 ​ : Dời gốc  Tstart *T start* ​  sang 08:00 sáng ca tiếp theo, Deadline \=  Tstart+M *T start* ​ \+*M* |  | **X** |  |
|  | A3 *A* 3 ​ : Cắt đôi SLA, dời phần thời gian thừa  M2 *M* 2 ​  sang ca làm việc tiếp theo |  |  | **X** |

### 1.3. Sơ đồ chuyển trạng thái (State Transition)

*Ghi chú: UC 2.1, 2.3 và 2.4 là các chức năng xử lý tức thời và tính toán thuật toán, không quản lý vòng đời trạng thái nên không áp dụng kỹ thuật chuyển trạng thái.*

**Chỉ áp dụng cho UC 2.2 (Vòng đời của Ticket Hỗ Trợ Khẩn Cấp)**

| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt (Event) | Trạng thái tiếp theo |
| :---- | :---- | :---- |
| (Không tồn tại) | Khách hàng nhắn tin tiêu cực (Điểm  ≤ ≤ Threshold) | **PENDING** (Chờ tiếp nhận) |
| **PENDING** | Khách hàng chủ động xóa phiên trò chuyện (UC 2.2 E-3) | **CLOSED** (Vô hiệu hóa) |
| **PENDING** | Nhân viên click "Tiếp nhận" (Tương tác từ Khối 3\) | **IN\_PROGRESS** (Đang xử lý) |
| **IN\_PROGRESS** | Khách hàng nhắn tin chửi tiếp (Cập nhật Ticket) | **IN\_PROGRESS** (SLA Reset) |
| **IN\_PROGRESS** | Nhân viên đánh dấu đã giải quyết xong | **RESOLVED** |

## 2\. Ma trận truy xuất nguồn gốc (Traceability Matrix \- RTM)

| Mã Yêu Cầu / Luồng Nghiệp Vụ | Mã Test Case (TC\_ID) |
| :---- | :---- |
| UC 2.3 \- Luồng chính (Lưu cấu hình hợp lệ) | TC\_UC23\_01 |
| UC 2.3 \- E-1 (Lỗi cấu hình P1  ≥ ≥ P2) | TC\_UC23\_02 |
| UC 2.3 \- E-1 (Lỗi cấu hình Threshold bỏ trống/Sai kiểu) | TC\_UC23\_03 |
| UC 2.1 & 2.2 \- Luồng chính (Tạo Ticket P2) | TC\_UC22\_01 |
| UC 2.1 & 2.2 \- Luồng chính (Tạo Ticket P1) | TC\_UC22\_02 |
| UC 2.2 \- A-1 (Leo thang sự cố từ P2 lên P1) | TC\_UC22\_03 |
| UC 2.4 \- Luồng chính (Tính SLA hoàn toàn trong ca trực) | TC\_UC24\_01 |
| UC 2.4 \- E-1 (Ticket tạo ngoài giờ làm việc) | TC\_UC24\_02 |
| UC 2.4 \- E-2 (SLA vắt ngang qua ngày hôm sau) | TC\_UC24\_03 |

## 3\. Thiết kế ca kiểm thử chi tiết (Test Case Specification)

### Nhóm 1: Kiểm thử chức năng Cấu hình Cảnh báo (UC 2.3)

*(Áp dụng nguyên tắc Cô lập lỗi cho các ca Negative)*

| TC\_ID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **TC\_UC23\_01** | Lưu cấu hình hợp lệ (Happy Path) | Đăng nhập quyền Admin, trang Cấu hình | 1\. Nhập P1 Threshold. 2\. Nhập P2 Threshold. 3\. Bấm Lưu. | P1 \= \-0.80 P2 \= \-0.30 | Màn hình báo xanh "Cập nhật cấu hình thành công". | Pass |
| **TC\_UC23\_02** | Bẫy lỗi: P1 lớn hơn P2 | Đăng nhập quyền Admin, trang Cấu hình | 1\. Nhập P1 lớn hơn P2. 2\. Bấm Lưu. | P1 \= \-0.20 P2 \= \-0.40 | Hệ thống chặn lưu, khoanh đỏ và báo "P1 Threshold bắt buộc phải nhỏ hơn P2". | Pass |
| **TC\_UC23\_03** | Bẫy lỗi: Kiểu dữ liệu Threshold sai (Ký tự chữ) | Đăng nhập quyền Admin, trang Cấu hình | 1\. Nhập P1 bằng chữ. 2\. Nhập P2 hợp lệ. 3\. Bấm Lưu. | P1 \= "abc" P2 \= \-0.30 | Hệ thống chặn lưu, báo lỗi kiểu dữ liệu tại ô P1. | Pass |

### Nhóm 2: Kiểm thử Luồng Khởi tạo & Leo thang sự cố (UC 2.1 & 2.2)

*(Giả định cấu hình: P1 \= \-0.60, P2 \= \-0.30)*

| TC\_ID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **TC\_UC22\_01** | Sinh Ticket P2 do cảm xúc tiêu cực nhẹ | Không có Ticket cũ | 1\. Khách hàng gửi tin nhắn. | Điểm  S=−0.45 *S*\=−0.45 Ý định: Bình thường | Sinh 1 Ticket MỚI mức P2. | Pass |
| **TC\_UC22\_02** | Sinh Ticket P1 do vi phạm nghiêm trọng (Ngộ độc) | Không có Ticket cũ | 1\. Khách hàng gửi tin nhắn báo ngộ độc thú cưng. | Ý định: Ngộ độc/Cấp cứu (Dù  S *S* cao) | Sinh 1 Ticket MỚI mức P1 (Bỏ qua điểm cảm xúc). | Pass |
| **TC\_UC22\_03** | Leo thang sự cố (A-1) | Đã có 1 Ticket P2 (PENDING) | 1\. Khách tiếp tục chửi bới gắt gao. | Điểm  S=−0.80 *S*\=−0.80 | Không sinh Ticket mới. Ticket P2 cũ bị đổi thành P1 và SLA đếm lại từ đầu. | Pass |

### Nhóm 3: Kiểm thử Động cơ tính toán SLA (UC 2.4)

*(Giả định: Ca làm việc 08:00 \- 18:00, Thứ 2 đến Thứ 6\. Định mức P1 \= 15 phút, P2 \= 60 phút)*

| TC\_ID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **TC\_UC24\_01** | Tính SLA trọn vẹn trong ca làm việc | Ngày Thứ Ba, giờ hệ thống là 10:00 | 1\. Kích hoạt tạo Ticket P1. | Thời gian tạo: 10:00 SLA P1: 15 phút | Hệ thống lưu DB cột sla\_deadline \= 10:15 cùng ngày. | Pass |
| **TC\_UC24\_02** | Sự cố phát sinh ngoài giờ (Ban đêm) | Ngày Thứ Tư, giờ hệ thống là 02:00 sáng | 1\. Kích hoạt tạo Ticket P2. | Thời gian tạo: 02:00 SLA P2: 60 phút | Hệ thống dời gốc về 08:00 sáng. sla\_deadline \= 09:00 sáng Thứ Tư. | Pass |
| **TC\_UC24\_03** | SLA vắt ngang qua ngày tiếp theo | Ngày Thứ Năm, giờ hệ thống là 17:30 | 1\. Kích hoạt tạo Ticket P2. | Thời gian tạo: 17:30 SLA P2: 60 phút | Tốn 30p hôm nay (đến 18:00). Còn 30p dời sang mai. sla\_deadline \= 08:30 sáng Thứ Sáu. | Pass |

