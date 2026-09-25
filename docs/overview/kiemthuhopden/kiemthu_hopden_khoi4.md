# THIẾT KẾ KIỂM THỬ HỘP ĐEN - KHỐI CHỨC NĂNG 4: ĐIỀU PHỐI PHÂN VIỆC, GIÁM SÁT SLA & BÁO CÁO HIỆU SUẤT

> **Đối tượng kiểm thử:** Khối chức năng Điều phối phân việc, Giám sát SLA & Báo cáo hiệu suất (Dispatcher & SLA Engine).  
> **Tài liệu tham chiếu đặc tả:** `docs/overview/usecase.md` và `docs/overview/usecase4.md` (Use Cases 4.1, 4.2, 4.3, 4.4).  
> **Nguyên tắc hành văn kiểm thử hộp đen:** Mô tả hoàn toàn từ góc nhìn người dùng cuối (Nhân viên CSKH - Agent / Quản lý CSKH - Manager / Admin) tương tác trên giao diện màn hình Console, bảng công việc Kanban và màn hình Báo cáo. Không đề cập đến thuật toán mã code, cấu trúc DB, tên trường SQL hay Pydantic schema validation. Các trạng thái kỹ thuật được diễn giải dưới dạng thuật ngữ Tiếng Việt kèm chú thích Tiếng Anh theo đúng giao diện hiển thị (VD: *Chờ tiếp nhận (Pending)*, *Đang xử lý (In Progress)*, *Đã giải quyết (Resolved)*, *Đã kết thúc (Closed)*, *Trực tuyến (ONLINE)*, *Vi phạm cam kết (SLA Breached)*).

---

# I. USE CASE 4.1: TỰ ĐỘNG PHÂN CHIA TICKET THÔNG MINH (LEAST-LOADED DISPATCHER)

## 1.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích các tiêu chí phân chia công việc tự động

| Tiêu chí / Trường dữ liệu | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Trạng thái làm việc nhân viên** | • Chỉ gán Ticket cho nhân viên đang ở trạng thái Trực tuyến (`ONLINE`) | **V_STT_01:** Có ít nhất 1 nhân viên ở trạng thái Trực tuyến (`ONLINE`) | **I_STT_01:** Tất cả nhân viên đều ở trạng thái Bận (`BUSY`) hoặc Ngoại tuyến (`OFFLINE`) (E-1) | Trạng thái sẵn sàng nhận việc |
| **Kỹ năng chuyên môn xử lý** | • Nhân viên phải có kỹ năng khớp với danh mục khiếu nại của Ticket | **V_SKILL_01:** Có nhân viên `ONLINE` khớp danh mục kỹ năng sự cố | **I_SKILL_01:** Có nhân viên `ONLINE` nhưng không ai có kỹ năng phù hợp danh mục sự cố (E-1) | Khớp / Không khớp danh mục kỹ năng |
| **Tải công việc hiện tại** | • Ưu tiên gán cho nhân viên có số lượng Ticket chưa đóng (`Pending` / `In Progress`) ít nhất | **V_LOAD_01:** Chọn nhân viên có số Ticket chưa đóng ít nhất | **I_LOAD_01:** Không có ứng viên hợp lệ | Đếm số Ticket đang gánh |
| **Thời gian rảnh lâu nhất** | • Nếu số Ticket đang gánh bằng nhau, chọn người có thời điểm nhận việc gần nhất xa nhất | **V_TIME_01:** Chọn nhân viên có thời gian rảnh lâu hơn | Không áp dụng phân vùng sai | So sánh mốc thời gian chờ việc |

---

## 1.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Tự động Phân chia Ticket (Least-Loaded Dispatcher)

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

# II. USE CASE 4.2: GIÁM SÁT THỜI HẠN XỬ LÝ CAM KẾT SLA & BÁO ĐỘNG VI PHẠM

## 2.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích thời gian đếm ngược SLA theo mức độ ưu tiên

| Mức độ ưu tiên | Ràng buộc thời hạn SLA | Phân vùng Bình thường ($V\_$) | Phân vùng Cảnh báo cam ($V\_$) | Phân vùng Vi phạm đỏ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sự cố P1 (Khẩn cấp)** | Cam kết **15 phút** (900 giây)<br>Cảnh báo $< 20\%$ (180s) | **V_P1_01:** Còn từ 181 đến 900 giây | **V_P1_02:** Còn từ 1 đến 180 giây | **I_P1_01:** Còn $\le 0$ giây (Quá hạn) | 900s, 181s, 180s, 1s, 0s, -1s |
| **Sự cố P2 (Khẩn cấp cao)** | Cam kết **60 phút** (3600 giây)<br>Cảnh báo $< 20\%$ (720s) | **V_P2_01:** Còn từ 721 đến 3600 giây | **V_P2_02:** Còn từ 1 đến 720 giây | **I_P2_01:** Còn $\le 0$ giây (Quá hạn) | 3600s, 721s, 720s, 1s, 0s |
| **Sự cố P3 (Trung bình)** | Cam kết **240 phút** (14400s)<br>Cảnh báo $< 20\%$ (2880s) | **V_P3_01:** Còn từ 2881 đến 14400s | **V_P3_02:** Còn từ 1 đến 2880s | **I_P3_01:** Còn $\le 0$ giây (Quá hạn) | 14400s, 2881s, 2880s, 0s |

---

## 2.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Giám sát SLA & Báo động Vi phạm

*(Tiền đề quy trình: Tiến trình Cron Job kiểm tra thời gian đếm ngược SLA mỗi 30 giây)*

| Điều kiện / Hành động | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
| :--- | :---: | :---: | :---: | :---: |
| **C1: Nhân viên bấm nút "Xác nhận đã xử lý" khi thời gian đếm ngược còn > 0s?** | T | F | F | F |
| **C2: Thời gian đếm ngược còn lại ở mức $< 20\%$ tổng thời lượng SLA?** | - | F | T | T |
| **C3: Thời gian đếm ngược trôi về mốc 0 giây ($\le 0$s)?** | - | - | F | T |
| **H1: Dừng đồng hồ SLA, ghi nhận Hoàn thành Đúng hạn (SLA Met), thẻ hiển thị màu xanh** | X | | | |
| **H2: Giữ đồng hồ đếm ngược, hiển thị thẻ và đồng hồ ở trạng thái màu sắc Bình thường** | | X | | |
| **H3: Đổi thẻ và đồng hồ đếm ngược sang tông màu Vàng Cam cảnh báo** | | | X | |
| **H4: Thẻ chuyển sang màu Đỏ nhấp nháy, bắn âm thanh báo động & trừ điểm SLA (E-1)** | | | | X |

---

## 2.3. Sơ đồ chuyển trạng thái (State Transition)

### Vòng đời Trạng thái SLA của Ticket

| Trạng thái hiện tại | Điều kiện / Sự kiện kích hoạt | Trạng thái tiếp theo |
| :--- | :--- | :--- |
| **Bình thường (SLA Normal)** | Thời gian đếm ngược trôi xuống mốc $< 20\%$ thời lượng SLA | **Cảnh báo (SLA Warning - Nền cam)** |
| **Bình thường / Cảnh báo** | Nhân viên nhấn nút "Xác nhận đã xử lý" khi thời gian còn $> 0$s | **Hoàn thành đúng hạn (SLA Met)** |
| **Cảnh báo (SLA Warning)** | Thời gian đếm ngược trôi về mốc 0 giây ($\le 0$s) | **Vi phạm quá hạn (SLA Breached - Nền đỏ)** |
| **Vi phạm quá hạn (SLA Breached)** | Nhân viên bấm "Xác nhận đã xử lý" muộn | **Hoàn thành quá hạn (SLA Missed)** |

---
---

# III. USE CASE 4.3: QUẢN LÝ TIẾN ĐỘ TRÊN BẢNG KANBAN

## 3.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích Quyền kéo thả thẻ & Nội dung ghi chú xử lý

| Trường dữ liệu / Thao tác | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Luân chuyển trạng thái 1 chiều** | • Luân chuyển tiến theo thứ tự: `Chờ tiếp nhận` $\rightarrow$ `Đang xử lý` $\rightarrow$ `Đã giải quyết` $\rightarrow$ `Đã kết thúc` | **V_FLOW_01:** Kéo thả thẻ công việc tiến theo đúng chiều thứ tự quy định | **I_FLOW_01:** Kéo ngược lùi trạng thái (VD: Kéo từ `Đang xử lý` lùi về `Chờ tiếp nhận`) (E-2) | Luân chuyển tiến lên / kéo lùi |
| **Quyền kéo thả thẻ (Kanban)** | • Nhân viên (Agent) chỉ được kéo thẻ do mình phụ trách<br>• Quản lý/Admin có quyền kéo mọi thẻ | **V_PERM_01:** Agent kéo thả thẻ do chính mình phụ trách<br>**V_PERM_02:** Quản lý/Admin kéo thả thẻ bất kỳ | **I_PERM_01:** Agent cố tình kéo thả thẻ do nhân viên khác phụ trách (E-1) | Phân quyền kéo thả |
| **Ghi chú xử lý sự cố (Summary)** | • Bắt buộc khi chuyển sang `Đã giải quyết` (`RESOLVED`)<br>• Độ dài 10 - 1000 ký tự | **V_NOTE_01:** Chuỗi ghi chú xử lý hợp lệ 10 - 1000 ký tự (VD: *"Đã kiểm tra và hoàn tiền đơn hàng"*) | **I_NOTE_01:** Để trống ghi chú xử lý<br>**I_NOTE_02:** Ngắn hơn 10 ký tự (E-3) | • Biên dưới: 9 ký tự ($I\_$), 10 ký tự ($V\_$), 11 ký tự ($V\_$)<br>• Biên trên: 1000 ký tự ($V\_$), 1001 ký tự ($I\_$) |

---

## 3.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Kéo thả thẻ trên Bảng Kanban

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

# IV. USE CASE 4.4: BÁO CÁO THỐNG KÊ HIỆU SUẤT

## 4.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)

### Bảng phân tích Bộ lọc khoảng thời gian & Xuất báo cáo

| Trường dữ liệu / Chỉ số | Điều kiện đặc tả (Ràng buộc) | Phân vùng hợp lệ ($V\_$) | Phân vùng không hợp lệ ($I\_$) | Điểm biên cần test |
| :--- | :--- | :--- | :--- | :--- |
| **Khoảng thời gian tra cứu (Delta)** | • Ngày bắt đầu phải nhỏ hơn hoặc bằng Ngày kết thúc (`from_date <= to_date`)<br>• Khoảng cách giữa 2 mốc tối đa **365 ngày**<br>• Không chọn mốc trong tương lai | **V_DATE_01:** Khoảng thời gian hợp lệ từ 0 đến 365 ngày (VD: 30 ngày qua)<br>**V_DATE_02:** Chọn nút mốc thời gian nhanh ("7 ngày qua", "30 ngày qua") | **I_DATE_01:** Để trống ngày bắt đầu hoặc ngày kết thúc<br>**I_DATE_02:** Ngày bắt đầu lớn hơn Ngày kết thúc (`from_date > to_date`) (E-1)<br>**I_DATE_03:** Khoảng cách thời gian vượt quá 365 ngày (VD: 366 ngày)<br>**I_DATE_04:** Chọn mốc ngày trong tương lai | • Biên khoảng cách: -1 ngày (Bắt đầu > Kết thúc) ($I\_$), 0 ngày (Trùng ngày) ($V\_$), 364 ngày ($V\_$), 365 ngày ($V\_$), 366 ngày ($I\_$) |
| **Quyền xem báo cáo thống kê** | • Chỉ dành riêng cho vai trò Quản lý (Manager) hoặc Quản trị viên (Admin) | **V_AUTH_01:** Đăng nhập tài khoản Quản lý / Admin | **I_AUTH_01:** Đăng nhập tài khoản Agent thông thường $\rightarrow$ Chặn truy cập | Phân quyền truy cập |

---

## 4.2. Bảng quyết định (Decision Table)

### Bảng quyết định Luồng Lọc dữ liệu & Xuất Báo cáo hiệu suất

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

# V. MA TRẬN TRUY XUẤT NGUỒN GỐC (TRACEABILITY MATRIX - RTM)

| Mã Yêu cầu / Luồng Nghiệp vụ | Nội dung Yêu cầu / Luồng | Mã Ca kiểm thử (Test Case ID) |
| :--- | :--- | :--- |
| **UC 4.1 - Luồng chính** | Tự động phân công Ticket cho nhân viên rảnh nhất & đúng kỹ năng | `TC_DIS_01` |
| **UC 4.1 - Rule 4** | Xử lý trường hợp trùng tải (Giao cho người có thời gian chờ việc lâu hơn) | `TC_DIS_02` |
| **UC 4.1 - E-1** | Bẫy lỗi thiếu nhân viên ONLINE hoặc không có nhân viên đúng kỹ năng | `TC_DIS_03` |
| **UC 4.2 - Luồng chính** | Đồng hồ đếm ngược SLA ở trạng thái màu sắc Bình thường | `TC_DIS_04` |
| **UC 4.2 - Rule 3** | Kích hoạt trạng thái Cảnh báo màu cam khi thời gian SLA còn $< 20\%$ | `TC_DIS_05` |
| **UC 4.2 - E-1** | Quá hạn SLA (0 giây) $\rightarrow$ Thẻ chuyển màu đỏ nhấp nháy & bắn báo động | `TC_DIS_06` |
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

# VI. THIẾT KẾ CA KIỂM THỬ CHI TIẾT (TEST CASE SPECIFICATION - IEEE)

## 6.1. Nhóm Test Case: UC 4.1 - Phân chia công việc tự động

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_01** | Kiểm tra tự động giao Ticket cho nhân viên có ít việc nhất (Happy Path) | Nhân viên A có 1 Ticket đang mở, Nhân viên B có 3 Ticket. Cả 2 đang ONLINE & đúng kỹ năng. | 1. Tạo một phiếu hỗ trợ khẩn cấp P1.<br>2. Đăng nhập tài khoản Nhân viên A và kiểm tra màn hình Bàn làm việc. | Ticket P1, Danh mục `Lỗi đơn hàng` ($V\_$) | Hệ thống tự động gán thẳng phiếu hỗ trợ P1 cho Nhân viên A. Phiếu xuất hiện trên màn hình Bàn làm việc của Nhân viên A ở trạng thái *Đang xử lý (In Progress)*. | Pass |
| **TC_DIS_02** | Kiểm tra xử lý trùng tải công việc (Chọn người có thời gian chờ rảnh lâu hơn) | Nhân viên A và B cùng gánh 2 Ticket. Nhân viên A rảnh 30 phút, Nhân viên B rảnh 5 phút. | 1. Tạo một phiếu hỗ trợ P2.<br>2. Đăng nhập kiểm tra màn hình của cả 2 nhân viên. | Ticket P2, Danh mục `Sản phẩm lỗi` ($V\_$) | Phiếu hỗ trợ P2 được tự động gán cho Nhân viên A (do thời gian chờ việc lâu hơn Nhân viên B). | Pass |
| **TC_DIS_03** | Kiểm tra xử lý khi không có nhân viên trực tuyến đúng kỹ năng (E-1) | Nhân viên A (đúng kỹ năng) OFFLINE. Nhân viên B (sai kỹ năng) ONLINE. | 1. Tạo một phiếu hỗ trợ P1 danh mục `Đổi trả/Hoàn tiền`.<br>2. Đăng nhập tài khoản Quản lý quan sát màn hình. | Ticket P1, Danh mục `Đổi trả/Hoàn tiền` ($I\_$) | Màn hình của Quản lý bật thông báo cảnh báo đỏ. Ticket bị giữ ở trạng thái *Chờ tiếp nhận (Pending)* không có người nhận để Quản lý gán thủ công. | Pass |

---

## 6.2. Nhóm Test Case: UC 4.2 - Giám sát thời hạn xử lý cam kết SLA

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_04** | Kiểm tra đồng hồ đếm ngược SLA ở trạng thái màu sắc Bình thường | Ticket P1 vừa được gán sang trạng thái *Đang xử lý* | 1. Đăng nhập tài khoản Nhân viên CSKH.<br>2. Quan sát thẻ công việc của phiếu P1. | Thời gian còn lại = 900 giây (15 phút) | Thẻ hiển thị đồng hồ đếm ngược từ 15:00. Nền thẻ và đồng hồ hiển thị màu sắc Bình thường. | Pass |
| **TC_DIS_05** | Kiểm tra kích hoạt Cảnh báo màu cam tại mốc $< 20\%$ SLA (180 giây) | Ticket P1 đang chạy đồng hồ đếm ngược | 1. Quan sát đồng hồ đếm ngược trên thẻ phiếu P1.<br>2. Chờ cho đến khi đồng hồ nhảy xuống mốc 03:00 (đúng 180 giây). | Thời gian còn lại = 180 giây ($V\_$) | Thẻ và đồng hồ đếm ngược lập tức đổi sang **tông màu Vàng Cam cảnh báo** chính xác tại mốc 180 giây. | Pass |
| **TC_DIS_06** | Kiểm tra vi phạm quá hạn SLA tại mốc 0 giây (E-1) | Phiên chat đang ở trạng thái Cảnh báo màu cam | 1. Giữ nguyên không bấm xử lý phiếu P1.<br>2. Quan sát đồng hồ khi trôi về mốc 00:00. | Thời gian còn lại = 0 giây ($I\_$) | Thẻ chuyển sang **màu Đỏ nhấp nháy**, hệ thống phát âm thanh báo động vi phạm và gửi cảnh báo đỏ lên màn hình Quản lý. Ghi nhận trừ điểm SLA của nhân viên. | Pass |
| **TC_DIS_07** | Kiểm tra dừng đồng hồ SLA khi bấm hoàn thành đúng hạn | Ticket đang đếm ngược ở mốc Cảnh báo màu cam | 1. Nhấn nút "Xác nhận đã xử lý" trên thẻ phiếu P1.<br>2. Nhập ghi chú xử lý hợp lệ và bấm Xác nhận khi đồng hồ còn $> 0$s. | Ghi chú hợp lệ, thời gian còn lại = 45s ($V\_$) | Ghi nhận Hoàn thành Đúng hạn (SLA Met). Đồng hồ SLA ngừng đếm ngược lập tức và thẻ hiển thị đánh dấu màu xanh lá. | Pass |

---

## 6.3. Nhóm Test Case: UC 4.3 - Quản lý tiến độ trên Bảng Kanban

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_08** | Kiểm tra kéo thả thẻ tiến lên hợp lệ (Happy Path) | Đăng nhập Nhân viên A, có phiếu X ở cột `Đang xử lý` | 1. Kéo thả thẻ phiếu X từ cột `Đang xử lý` sang cột `Đã giải quyết`.<br>2. Tại hộp thoại hiện lên, nhập ghi chú xử lý hợp lệ.<br>3. Bấm "Xác nhận hoàn thành". | Ghi chú: `"Đã kiểm tra và hoàn tiền đơn hàng cho khách"` (40 ký tự) ($V\_$) | Thẻ nằm cố định ở cột `Đã giải quyết`, dừng đồng hồ SLA. Hiển thị thông báo xanh thành công. | Pass |
| **TC_DIS_09** | Kiểm tra chặn Agent kéo thả thẻ do nhân viên khác phụ trách (E-1) | Đăng nhập Nhân viên A, màn hình có phiếu Y của Nhân viên B | 1. Thử kéo thả thẻ phiếu Y của Nhân viên B sang cột khác. | Thao tác trên thẻ Nhân viên B ($I\_$) | Thẻ nảy trượt trở lại vị trí cột cũ. Hiển thị báo lỗi: *"Bạn không có quyền cập nhật phiếu do nhân viên khác phụ trách"*. | Pass |
| **TC_DIS_10** | Kiểm tra chặn kéo lùi trạng thái thẻ công việc (E-2) | Đăng nhập Nhân viên A, phiếu X ở cột `Đang xử lý` | 1. Kéo thả thẻ phiếu X từ cột `Đang xử lý` lùi về cột `Chờ tiếp nhận`. | Kéo lùi trạng thái ($I\_$) | Thẻ nảy về cột cũ `Đang xử lý`. Hiển thị báo lỗi: *"Tiến độ chỉ được phép luân chuyển tiến lên"*. | Pass |
| **TC_DIS_11** | Kiểm tra báo lỗi khi nhập ghi chú xử lý ngắn hơn 10 ký tự (E-3) | Đang mở hộp thoại hoàn thành phiếu ở cột `Đã giải quyết` | 1. Nhập 3 ký tự vào ô ghi chú xử lý.<br>2. Bấm "Xác nhận hoàn thành". | Ghi chú: `"Xong"` (4 ký tự) ($I\_$) | Viền ô nhập hằn đỏ, hiển thị cảnh báo: *"Ghi chú xử lý sự cố bắt buộc từ 10 đến 1000 ký tự"*. Hệ thống chặn thao tác chuyển thẻ. | Pass |
| **TC_DIS_12** | Kiểm tra Quản lý có toàn quyền kéo thả thẻ công việc | Đăng nhập tài khoản Quản lý, chọn phiếu Y của Nhân viên B | 1. Kéo thả thẻ phiếu Y sang cột `Đã giải quyết`.<br>2. Nhập ghi chú xử lý và bấm Xác nhận. | Thao tác bởi Quản lý ($V\_$) | Kéo thả thành công, hộp thoại cập nhật trạng thái xuất hiện cho phép Quản lý ghi đè ghi chú xử lý mà không bị chặn quyền. | Pass |

---

## 6.4. Nhóm Test Case: UC 4.4 - Báo cáo thống kê hiệu suất

| TC_ID | Mục đích kịch bản | Tiền điều kiện | Các bước thực hiện | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_DIS_13** | Kiểm tra lọc báo cáo thống kê hợp lệ (Happy Path) | Đăng nhập tài khoản Quản lý, đang ở màn hình Báo cáo | 1. Click chọn nút lọc nhanh mốc thời gian "30 ngày qua".<br>2. Bấm nút "Lọc dữ liệu". | Mốc "30 ngày qua" ($V\_$) | Hiển thị đầy đủ biểu đồ tròn/cột phân tích và bảng số liệu thống kê. Nút "Xuất báo cáo Excel" sáng lên cho phép bấm tải file. | Pass |
| **TC_DIS_14** | Kiểm tra lọc dữ liệu đúng điểm biên 365 ngày (BVA Max) | Đang ở màn hình Báo cáo | 1. Chọn Ngày bắt đầu là 01/01/2026.<br>2. Chọn Ngày kết thúc là 31/12/2026 (khoảng cách đúng 365 ngày).<br>3. Bấm "Lọc dữ liệu". | Delta = 365 ngày ($V\_$) | Dữ liệu báo cáo được tải thành công, hiển thị trọn vẹn số liệu phân tích của nguyên 365 ngày. | Pass |
| **TC_DIS_15** | Kiểm tra báo lỗi chọn Ngày bắt đầu lớn hơn Ngày kết thúc (E-1) | Đang ở màn hình Báo cáo | 1. Chọn Ngày bắt đầu là 15/10/2026.<br>2. Chọn Ngày kết thúc là 01/10/2026.<br>3. Bấm "Lọc dữ liệu". | `from_date > to_date` ($I\_$) | Giữ nguyên giao diện biểu đồ cũ. Khoanh viền đỏ ô ngày tháng và báo lỗi: *"Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc"*. | Pass |
| **TC_DIS_16** | Kiểm tra báo lỗi khi chọn khoảng thời gian vượt quá 365 ngày (BVA Max+) | Đang ở màn hình Báo cáo | 1. Chọn Ngày bắt đầu là 01/01/2026.<br>2. Chọn Ngày kết thúc là 01/01/2027 (khoảng cách 366 ngày).<br>3. Bấm "Lọc dữ liệu". | Delta = 366 ngày ($I\_$) | Báo lỗi khoanh đỏ ô ngày tháng: *"Khoảng thời gian tra cứu tối đa không được vượt quá 365 ngày"*. Chặn thao tác lọc. | Pass |
| **TC_DIS_17** | Kiểm tra hiển thị giao diện khi mốc thời gian không có dữ liệu (E-3) | Đang ở màn hình Báo cáo | 1. Chọn khoảng thời gian rơi vào ngày nghỉ lễ không có dữ liệu.<br>2. Bấm "Lọc dữ liệu". | Khoảng thời gian trống dữ liệu | Tạm ẩn các biểu đồ tròn/cột, hiển thị hình minh họa trống kèm thông báo: *"Không có dữ liệu phiếu hỗ trợ trong khoảng thời gian này"*. Các chỉ số đo lường trả về 0. | Pass |

---
*Tài liệu kiểm thử hộp đen Khối chức năng 4 được chuẩn hóa hoàn thiện 100%, bổ sung đầy đủ EP/BVA, Decision Table, State Transition, RTM và bộ 17 Test Cases chuẩn IEEE.*