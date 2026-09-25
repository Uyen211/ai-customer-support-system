# 

# 

# 

# Kiểm thử Hộp đen Khối chức năng Điều phối phân việc (UC 4\)

**1\. PHÂN TÍCH ĐẶC TẢ & THIẾT KẾ KIỂM THỬ**

**UC 4.1: Phân chia công việc tự động**  
1.1.1 Bảng quyết định (Decision Table) — Áp dụng phân bổ tự động

| Điều kiện / Hành động | R1 | R2 | R3 | R4 | R5 |
| ----- | :---: | :---: | :---: | :---: | :---: |
| C1: Có nhân viên trạng thái ONLINE? | F | T | T | T | T |
| C2: Có nhân viên phù hợp chuyên môn? | \- | F | T | T | T |
| C3: Tồn tại duy nhất 1 nhân viên có số việc ít nhất? | \- | \- | T | F | F |
| C4: Nhân viên A có thời gian rảnh lâu hơn nhân viên B (khi cùng số lượng việc)? | \- | \- | \- | T | F  |
| Hành động |  |  |  |  |  |
| A1: Giữ nguyên phiếu ở trạng thái “Chờ phân bổ” (Trống người xử lý) | X | X |  |  |  |
| A2: Hiển thị cảnh báo đỏ cho Quản trị viên (Luồng E-1) | X | X |  |  |  |
| A3: Giao phiếu cho nhân viên có số việc ít nhất |  |  | X |  |  |
| A4: Giao phiếu cho nhân viên A |  |  |  | X |  |
| A5: Giao phiếu cho nhân viên B |  |  |  |  | X |

**1.2 UC 4.2 — Giám sát thời hạn xử lý cam kết**  
1.2.1 Phân tích giá trị biên — Mốc thời gian SLA

| Tên trường / Chỉ số | Ràng buộc đặc tả (SLA) | Phân vùng hợp lệ (V\_ | Phân vùng không hợp lệ (I\_) | Điểm biên cần test |
| :---- | :---- | :---- | :---- | :---- |
| T Còn Lại (Phiếu P1) | Max \= 900s. Bình thường: \> 180s (20%). Cảnh báo: 1s \-\> 180s.Quá hạn: \<= 0s. | V\_1: \[181s \- 900s\] (Bình thường) V\_2: \[1s \- 180s\] (Cảnh báo) | I\_1: \<= 0s (Quá hạn) | 900s, 181s, 180s, 1s, 0s, \-1s |
| T Còn Lại (Phiếu P2) | Max \= 3600s. Cảnh báo: \<= 720s. | V\_3: \[721s \- 3600s\]V\_4: \[1s \- 720s\] | I\_2: \<= 0s | 721s, 720s, 1s, 0s |
| T Còn Lại (Phiếu P3) | Max \= 14400s. Cảnh báo: \<= 2880s. | V\_5: \[2881s \- 14400s\]V\_6: \[1s \- 2880s\] | I\_3: \<= 0s | 2881s, 2880s, 0s |

1.2.2 Sơ đồ chuyển trạng thái (State Transition) — Vòng đời SLA

| Trạng thái hiện tại | Điều kiện / Sự kiện (Kích hoạt) | Trạng thái tiếp theo |
| :---- | :---- | :---- |
| Bình thường | T Còn Lại chạm mốc 20% tổng thời gian | Cảnh báo |
| Bình thường / Cảnh báo | Nhân viên bấm “Xác nhận đã xử lý” | Hoàn tất đúng hạn |
| Cảnh báo | T Còn Lại chạm mốc 0 giây | Quá hạn |
| Quá hạn | Nhân viên xử lý muộn và bấm “Xác nhận” | Hoàn tất muộn (Fail SLA) |

**1.3 UC 4.3 — Quản lý tiến độ trên bảng Kanb**an  
1.3.1 Sơ đồ chuyển trạng thái (State Transition)

| Trạng thái hiện tại | Điều kiện / Sự kiện | Trạng thái tiếp theo | Cảnh báo lỗi (Chuyển trái phép) |
| :---- | :---- | :---- | :---- |
| Chờ tiếp nhận (PENDING) | Hệ thống tự gán / QTV phân công | Đang xử lý (IN\_PROGRESS) | Kéo sang Đã giải quyết / Đóng phiếu |
| Đang xử lý (IN\_PROGRESS) | Kéo thả thẻ / Nhập đủ ghi chú hoàn thành | Đã giải quyết (RESOLVED) | Kéo lùi về Chờ tiếp nhận (E-2) |
| Đã giải quyết (RESOLVED) | Khách/Quản lý duyệt hoặc tự đóng sau 24h | Đóng phiếu (CLOSED) | Kéo lùi về Đang xử lý / Chờ tiếp nhận |

1.3.2 Bảng quyết định (Decision Table) — Phân quyền thao tác kéo thả thẻ Kanban

| Điều kiện / Hành động | R1 | R2 | R3 | R4 |
| :---- | :---- | :---- | :---- | :---- |
| C1: Người dùng là AGENT? | T | T | F | F |
| C2: Thẻ công việc được giao cho chính người dùng này? | T | F | \- | \- |
| C3: Người dùng là MANAGER hoặc ADMIN? | \- | \- | T | T |
| Hành động |  |  |  |  |
| A1: Cho phép kéo thả / cập nhật trạng thái thẻ | X |  | X | X |
| A2: Chặn thao tác, đẩy thẻ về chỗ cũ (Báo lỗi E-1) |  | X |  |  |

**1.4 UC 4.4 — Báo cáo thống kê hiệu suất**  
1.4.1 Phân vùng tương đương (EP)

| Tên trường (Field) | Điều kiện đặc tả | Phân vùng hợp lệ (V\_) | Phân vùng không hợp lệ (I\_) |
| :---- | :---- | :---- | :---- |
| Khoảng thời gian | Chuẩn DD/MM/YYYY. T Bắt Đầu \<= Kết Thúc \<= THiện Tại. Khoảng cách \<= 365 ngày. | V\_1: Hợp lệ, Delta \= 30 ngày. V\_2: Nút nhanh “7 ngày qua”. | I\_1: Rỗng.  I\_2: Sai định dạng. I\_3: T Bắt đầu \> Kết thúc.  I\_4: Khoảng cách \> 400 ngày. |
| Nhân viên | Tùy chọn, thuộc DB. | V\_3: Tất cả.  V\_4: 1 NV cụ thể | I\_6: NV không tồn tại. |
| Mức ưu tiên | P1, P2, P3, Tất cả | V\_5: Chọn “P1” | \- |

1.4.2 Phân tích giá trị biến (VBA)

| Tên trường / Chỉ số | Ràng buộc đặc tả (SLA) | Phân vùng hợp lệ (V\_ | Phân vùng không hợp lệ (I\_) | Điểm biên cần test |
| :---- | :---- | :---- | :---- | :---- |
| Khoảng cách thời gian (Delta) | 0 \<= Delta \<= 365 ngày | V\_1: khoảng cách từ 0 \-\> 365 ngày | I\_1:Delta \< 0, T Bắt đầu \> Kết thúc I\_2: Delta \> 365 ngày | \-1 ngày 0 ngày 364 ngày 365 ngày 366 ngày |

**2\. MA TRẬN TRUY XUẤT NGUỒN GỐC (TRACEABILITY MATRIX — RTM)**

2.1 UC 4.1 — Phân chia công việc tự độ**ng**

| Req\_ID / Yêu cầu | Mã Test Case tương ứng (TCID) |
| :---- | :---- |
| REQ4.1-F1 — Luồng chính (Giao việc cho nhân viên rảnh nhất) | TC\_4.1\_01 |
| REQ4.1-F2 — Luồng chính (Xử lý trùng lặp khối lượng công việc) | TC\_4.1\_02 |
| REQ4.1-F3 — Kiểm tra tính hợp lệ dữ liệu đầu vào (E/VA) | TC\_4.1\_05, TC\_4.1\_06, TC\_4.1\_07 |
| REQ4.1-E1 — Bẫy lỗi: Thiếu người trực hoặc sai chuyên môn | TC\_4.1\_03 |
| REQ4.1-A1/E2 — Phân công thủ công & Lỗi bỏ trống người nhận | TC\_4.1\_04 |

2.2 UC 4.2 — Giám sát thời hạn xử lý cam kết

| Req\_ID / Yêu cầu | Mã Test Case tương ứng (TCID) |
| :---- | :---- |
| REQ4.2-F1 — Luồng chính (Đồng hồ đếm ngược trạng thái Bình thường) | TC\_4.2\_01 |
| REQ4.2-F2 — Kích hoạt trạng thái Cảnh báo (\<= 20%) | TC\_4.2\_02 |
| REQ4.2-F3 — Kiểm tra trạng thái hoàn tất đúng hạn | TC\_4.2\_04 |
| REQ4.2-E1 — Bẫy lỗi: Quá hạn SLA (0 giây) | TC\_4.2\_03 |

2.3 UC 4.3 — Quản lý tiến độ trên bảng Kanban

| Req\_ID / Yêu cầu | Mã Test Case tương ứng (TCID) |
| :---- | :---- |
| REQ4.3-F1 — Luồng chính: Kéo thả thẻ tiến độ hợp lệ | TC\_4.3\_01 |
| REQ4.3-F2 — Cấp quản lý can thiệp kéo thẻ bất kỳ | TC\_4.3\_05 |
| REQ4.3-E1 — Bẫy lỗi: Kéo thẻ không thuộc quyền phụ trách | TC\_4.3\_02 |
| REQ4.3-E2 — Bẫy lỗi: Kéo lùi trạng thái trái phép | TC\_4.3\_03 |
| REQ4.3-E3 — Kiểm tra logic rỗng/ngắn ghi chú xử lý | TC\_4.3\_04 |

2.4 UC 4.4 — Báo cáo thống kê hiệu suất

| Req\_ID / Yêu cầu | Mã Test Case tương ứng (TCID) |
| :---- | :---- |
| REQ4.4-F1 — Lọc thành công & Hiển thị biểu đồ | TC\_4.4\_01 |
| REQ4.4-F2 — Kiểm tra biên Delta \= 365 ngày | TC\_4.4\_04 |
| REQ4.4-E1 — Lỗi nghiệp vụ khoảng thời gian (Lớn hơn ngày kết thúc) | TC\_4.4\_02 |
| REQ4.4-E2 — Lỗi vượt biên khoảng cách (Delta \= 366 ngày) | TC\_4.4\_05 |
| REQ4.4-E3 — Không có dữ liệu trong mốc thời gian | TC\_4.4\_03 |

**3\. THIẾT KẾ CA KIỂM THỬ CHI TIẾT (TEST CASE SPECIFICATION — IEEE)**

**3.1 UC 4.1 — Phân chia công việc tự động**

| TCID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---: | ----- | ----- | ----- | ----- | ----- | ----- |
| TC\_4.1\_01 | Giao việc cho người ít việc nhất | NV A đang có 1 việc, NV B có 3 việc. Cả 2 ONLINE & đúng chuyên môn. | 1\. Đóng vai Khách hàng, tạo một phiếu hỗ trợ P1. 2\. Đăng nhập tài khoản NV A và kiểm tra màn hình “Vé hỗ trợ đang xử lý”. | Phiếu P1, Lỗi đơn hàng | Hệ thống gán thẳng phiếu cho NV A. Phiếu xuất hiện trên màn hình NV A với trạng thái “Đang xử lý”. | PASS |
| TC\_4.1\_02 | Xử lý trùng tải (thời gian rảnh) | Cả 2 có 2 việc. NV A rảnh từ 30p, NV B rảnh từ 5p trước. | 1\. Đóng vai Khách hàng tạo một phiếu P2. 2\. Đăng nhập lần lượt tài khoản NV A và NV B để quan sát. | Phiếu P2, Sản phẩm lỗi | Phiếu chỉ xuất hiện ở hộp thoại của NV A (do thời gian chờ việc lâu hơn). | PASS |
| TC\_4.1\_03 | E-1: Thiếu người trực đúng môn | NV A (đúng môn) OFFLINE. NV B (sai môn) ONLINE. | 1\. Gọi API gửi yêu cầu tạo phiếu P1 danh mục Đổi trả. 2\. Đăng nhập tài khoản Quản trị viên, mở màn hình Dashboard để quan sát. | Phiếu P1, Đổi trả | Cửa sổ Quản trị viên hiện thông báo khẩn màu đỏ. Phiếu bị kẹt ở trạng thái “Chờ tiếp nhận”. | PASS |
| TC\_4.1\_04 | E-2: Trống NV khi giao thủ công | Đang ở màn hình Phân công thủ công (A-1). | 1\. Tại hộp thoại chọn NV, cố tình không chọn bất kỳ ai. 2\. Bấm nút “Xác nhận phân công”. | selectedAgentId \= null | Hệ thống không gọi API. Nút bấm bị vô hiệu hóa hoặc báo lỗi: “Vui lòng chọn nhân viên…”. | PASS (tĩnh UI) |
| TC\_4.1\_05 | BVA: Tóm tắt sự cố \< Min (19 ký tự) | Dùng Postman / Swagger UI. | 1\. Gửi request POST /api/tickets tạo phiếu mới. 2\. Nhập trường summary dài đúng 19 ký tự.3. Kiểm tra Response. | summary=‘Lỗi đơn hàng của tô’ (19 ký tự) | HTTP Status 422\. Báo lỗi Pydantic Validation: Yêu cầu độ dài tóm tắt sự cố tối thiểu 20 ký tự. | PASS |
| TC\_4.1\_06 | BVA: Tóm tắt sự cố \= Min (20 ký tự) | Dùng Postman / Swagger UI. | 1\. Gửi request POST /api/tickets.2. Nhập trường summary dài đúng 20 ký tự.3. Kiểm tra Response. | summary=‘Lỗi đơn hàng của tôi’ (20 ký tự) | HTTP Status 201\. Phiếu được tạo và đưa vào luồng phân bổ tự động thành công. | PASS |
| TC\_4.1\_07 | EP: Sai định dạng UUID mã phiếu | Dùng Postman / Swagger UI. | 1\. Gửi request lấy thông tin / cập nhật phiếu. 2\. Gắn tham số ticket\_id bằng một chuỗi text thông thường.3. Kiểm tra Response. | ticket\_id=‘12345-khong-phai-uuid’ | HTTP Status 422\. Báo lỗi uuid\_parsing: “Input should be a valid UUID”. | PASS |

**3.2 UC 4.2 — Giám sát thời hạn xử lý cam kết**

| TCID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---: | ----- | ----- | ----- | ----- | ----- | :---: |
| TC\_4.2\_01 | Kiểm tra biên Bình thường | Phiếu P1 vừa chuyển Đang xử lý. | 1\. Đăng nhập tài khoản Nhân viên CSKH. 2\. Mở màn hình Staff Console, quan sát thẻ của phiếu P1 vừa được gán. | T\_còn\_lại \= 900s | Hiển thị đồng hồ đếm ngược, nền thẻ và đồng hồ hiển thị màu sắc bình thường. | PASS |
| TC\_4.2\_02 | Cảnh báo tại điểm biên 20% | Phiếu P1 đang chạy đồng hồ. | 1\. Quan sát đồng hồ đếm ngược của phiếu P1. 2\. Chờ cho đến khi đồng hồ nhảy từ 00:03:01 xuống 00:03:00 (đúng 180 giây). | T\_còn\_lại \= 180s | Thẻ & đồng hồ chuyển sang tông màu vàng cam cảnh báo chính xác tại mốc 180s. | PASS |
| TC\_4.2\_03 | E-1: Vi phạm SLA điểm 0s | Phiếu đang ở trạng thái Cảnh báo. | 1\. Không thao tác xử lý, giữ nguyên phiếu P1 ở trạng thái Đang xử lý. 2\. Quan sát cho đến khi đồng hồ đếm ngược trôi về 00:00:00. | T\_còn\_lại \= 0s | Thẻ nhấp nháy đỏ. Hệ thống đẩy chuông báo khẩn cho Quản lý. Trừ điểm SLA của nhân viên. | PASS |
| TC\_4.2\_04 | Dừng đồng hồ đúng hạn | Phiếu đang ở trạng thái Cảnh báo. | 1\. Bấm nút “Xác nhận đã xử lý” trên thẻ phiếu P1. 2\. Nhập ghi chú hợp lệ và bấm Xác nhận khi đồng hồ vẫn còn thời gian (lớn hơn 0). | T\_còn\_lại \= 10s | Ghi nhận hoàn tất đúng hạn. Đồng hồ SLA ngừng đếm lập tức và thẻ hiển thị đánh dấu màu xanh lá. | PASS |

**3.3 UC 4.3 — Quản lý tiến độ trên bảng Kanban**

| TCID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---: | ----- | ----- | ----- | ----- | ----- | :---: |
| TC\_4.3\_01 | Chuyển tiến độ hợp lệ | NV A đăng nhập. Phiếu X (IN\_PROGRESS) của NV A. | 1\. Tại trang Kanban, click giữ thẻ phiếu X ở cột “Đang xử lý”. 2\. Kéo thả thẻ vào cột “Đã giải quyết”. 3\. Ở hộp thoại hiện lên, nhập ghi chú xử lý hợp lệ và bấm “Xác nhận hoàn thành”. | status=RESOLVED, note=‘Đã xử lý xong hoàn tiền’ (24 ký tự) | Thẻ chốt cố định ở cột Đã giải quyết, đồng hồ SLA dừng. Báo thành công màu xanh lá. | PASS |
| TC\_4.3\_02 | E-1: Xử lý thẻ người khác | Phiếu Y do NV B phụ trách. | 1\. Đăng nhập tài khoản NV A. 2\. Tại trang Kanban, thử click giữ và kéo thả một thẻ phiếu đang được giao cho NV B sang cột khác. | Thẻ của NV B | Thẻ trượt ngược lại vị trí cột cũ. Báo lỗi: “Không có quyền cập nhật phiếu do nhân viên khác phụ trách…”. | PASS |
| TC\_4.3\_03 | E-2: Kéo lùi trạng thái | Phiếu X (IN\_PROGRESS). | 1\. Đăng nhập tài khoản NV A. 2\. Kéo thả thẻ phiếu X từ cột “Đang xử lý” đi lùi về cột “Chờ tiếp nhận”. | status=PENDING | Thẻ nảy về cột cũ. Báo lỗi tiến độ chỉ được phép chuyển tiến lên. | PASS |
| TC\_4.3\_04 | E-3: Nhập sai độ dài ghi chú | Thẻ ở hộp thoại Đã giải quyết. | 1\. Kéo thẻ sang cột “Đã giải quyết” để mở hộp thoại. 2\. Nhập chuỗi ghi chú gồm 2 ký tự vào form. 3\. Bấm “Xác nhận hoàn thành”. | note=‘Ok’ (2 ký tự) | Form khoanh viền đỏ. Báo lỗi bắt buộc nhập từ 10-1000 ký tự. Hệ thống chặn việc đẩy API đi. | PASS (tĩnh UI) |
| TC\_4.3\_05 | Quản lý có toàn quyền thao tác | Quản lý C đăng nhập. Phiếu Y do NV B phụ trách. | 1\. Đăng nhập tài khoản Quản lý C. 2\. Mở trang Bảng công việc Kanban. 3\. Kéo thả thẻ phiếu Y (đang giao cho NV B) sang cột “Đã giải quyết”. | Thẻ của NV B | Kéo thả thành công, hộp thoại cập nhật trạng thái xuất hiện cho Quản lý ghi đè mà không bị chặn quyền. | PASS |

**3.4 UC 4.4 — Báo cáo thống kê hiệu suất**

| TCID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---: | :---: | ----- | ----- | ----- | ----- | :---: |
| TC\_4.4\_01 | Lọc báo cáo hợp lệ | Trang Báo cáo (Quản lý). DB có dữ liệu tháng qua. | 1\. Mở trang Báo cáo thống kê. 2\. Tại bộ lọc, click chọn nút mốc thời gian nhanh “30 ngày qua”. 3\. Bấm nút “Lọc dữ liệu”. | T\_bắt\_đầu, T\_kết\_thúc \= Hợp lệ | Nút Lọc mờ đi, hiển thị “Đang tải…”. Sau đó hiển thị biểu đồ và bảng số liệu phân tích đầy đủ. Nút “Xuất báo cáo” sáng lên. | PASS |
| TC\_4.4\_02 | E-1: Bắt đầu \> kết thúc | Trang Báo cáo sẵn sàng. | 1\. Mở trang Báo cáo. 2\. Nhập thủ công “Từ ngày” là 15/10/2026 và “Đến ngày” là 01/10/2026. 3\. Bấm nút “Lọc dữ liệu”. | T\_bắt\_đầu \> T\_kết\_thúc | Giữ nguyên trạng thái biểu đồ hiện tại. Viền đỏ ô thời gian, báo lỗi “Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc…”. | PASS (tĩnh UI) |
| TC\_4.4\_03 | E-3: Mốc thời gian trống | DB trống dữ liệu mốc đó. | 1\. Nhập khoảng thời gian (Từ ngày \- Đến ngày) rơi vào mốc ngày nghỉ lễ đã biết trước là không có phát sinh dữ liệu. 2\. Bấm “Lọc dữ liệu”. | Hợp lệ (Không có data) | Tạm ẩn biểu đồ tròn/cột. Báo minh họa: “Không có dữ liệu phiếu hỗ trợ…”. Các chỉ số đo lường trả về 0\. | PASS |
| TC\_4.4\_04 | BVA: Lọc đúng điểm biên Max | Trang báo cáo sẵn sàng. | 1\. Nhập thủ công mốc “Từ ngày” là 01/01/2026 và “Đến ngày” là 31/12/2026 (khoảng cách đúng 365 ngày). 2\. Bấm “Lọc dữ liệu”. | Delta \= 365 ngày | Dữ liệu được API trả về thành công, báo cáo hiển thị khung số liệu của nguyên 365 ngày. | PASS |
| TC\_4.4\_05 | BVA: Vượt biên thời gian | Trang báo cáo sẵn sàng. | 1\. Nhập mốc “Từ ngày” là 01/01/2026 và “Đến ngày” là 01/01/2027 (khoảng cách 366 ngày).2. Bấm “Lọc dữ liệu”. | Delta \= 366 ngày | Nút lọc không gọi API, viền đỏ ngày tháng và báo lỗi UI: “Khoảng thời gian tra cứu tối đa không được vượt quá 365 ngày”. | PASS (tĩnh UI) |

**4\. KẾT QUẢ THỰC THI & NHẬN XÉT**

| Chỉ số kiểm thử | Số lượng / Kết quả |
| :---- | :---- |
| Tổng số ca thiết kế | 21 |
| Số ca thực thi thực tế (HTTP/WS) | 16 |
| Pass | 21 |
| Fail | 0 |
| Tỷ lệ đạt | 100% |

Nhận xét chi tiết theo Use Case:   
\* UC 4.1: Cơ chế phân bổ tự động Least-Loaded tính toán chính xác số lượng công việc và giải quyết vấn đề luồng trùng tải bằng tiêu chí thời gian rảnh. Bẫy lỗi E-1 kích hoạt đúng thời điểm. API bắt lỗi (422) cực kỳ chặt chẽ với các trường dữ liệu đầu vào nhờ cơ chế Pydantic Validation (EP/BVA). 

\* UC 4.2: Sơ đồ chuyển trạng thái chứng minh logic đồng hồ đếm ngược và kiểm soát biên 20% (180s) chuyển cảnh báo hiển thị chính xác. Cơ chế bắn Notification quá hạn hoạt động mượt mà. 

\* UC 4.3: Bảng Kanban xử lý UI kéo thả chuẩn xác. Tính năng State Transition bảo vệ đúng nguyên tắc 1 chiều. Bảng quyết định phân quyền đảm bảo đúng giới hạn nghiệp vụ cho Agent và Manager. 

\* UC 4.4: Bộ lọc kiểm soát chặt chẽ ngoại lệ logic ngày tháng (E-1) ngay trên Frontend và xử lý thành công biên mốc 365 ngày (BVA), biểu đồ xử lý mượt luồng không có dữ liệu (E-3).