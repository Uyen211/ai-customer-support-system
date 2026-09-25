* Lỗi 1 (Ngôn từ & Góc nhìn Hộp đen): Trong bảng Test Cases sử dụng các từ ngữ code: POST /api/admin/users, HTTP 401, Token AGENT, WS rớt connection, sender\_type=AGENT.  
* Lỗi 2 (Decision Table UC 3.1):  
  * Thiếu Bảng quyết định cho Luồng Tạo tài khoản nhân sự mới (chỉ mới có luồng Đăng nhập A-1).  
* Lỗi 3 (Decision Table UC 3.3):  
  * Đưa Thao tác là GHI (gửi tin) làm Condition (đây là loại hành động/sự kiện).

**MỤC LỤC**

**1\. Phân tích đặc tả & Thiết kế kiểm thử**

    **1.1 UC 3.1 — Quản lý tài khoản nhân viên (EP/BVA, Decision Table, State Transition)**

    **1.2 UC 3.2 — Quản lý trạng thái làm việc của nhân viên**

    **1.3 UC 3.3 — Theo dõi hàng đợi và tiếp quản cuộc trò chuyện**

    **1.4 UC 3.4 — Quản lý và sử dụng mẫu phản hồi nhanh**

**2\. Ma trận truy xuất nguồn gốc (Traceability Matrix — RTM)**

**3\. Thiết kế ca kiểm thử chi tiết (Test Case Specification — IEEE)**

**4\. Kết quả thực thi & Nhận xét**

**1\. PHÂN TÍCH ĐẶC TẢ & THIẾT KẾ KIỂM THỬ**

**1.1 UC 3.1 — Quản lý tài khoản nhân viên**

***1.1.1 Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA) — Tạo tài khoản nhân sự***

| Field | Điều kiện đặc tả | Phân vùng hợp lệ (V\_) | Phân vùng không hợp lệ (I\_) | Điểm biên cần test |
| ----- | ----- | ----- | ----- | ----- |
| Họ và tên | Bắt buộc, 2–100 ký tự | Chuỗi 2–100 (VD: Nguyen Van Test) | \< 2; \> 100; bỏ trống | Min=2 (Ab); Max=100 (A×100); Min−=1 (A); Max+=101; rỗng () |
| Email nội bộ | Bắt buộc, đúng định dạng, duy nhất | ten@pethome.vn (EmailStr hợp lệ) | Sai định dạng; trùng đã tồn tại; dài \> 255 | 256 ký tự (Max+=1); trùng email đã có |
| Số điện thoại | Tùy chọn; nếu có: 10 chữ số, đầu 0 | Bỏ trống; 0 \+ 9 chữ số | 9 chữ số; không bắt đầu 0 | Đúng 10 số đầu 0; 9 số; đầu khác 0 |
| Mật khẩu | Bắt buộc, ≥ 8 ký tự, gồm chữ & số | ≥ 8 ký tự \+ đủ chữ & số (Passw0rd) | \< 8; toàn chữ cái; toàn chữ số | Min=8; Min−=7 (Pass123); thiếu chữ số; thiếu chữ cái |
| Vai trò (Role) | Chỉ AGENT / MANAGER / ADMIN | AGENT, MANAGER, ADMIN | Giá trị khác (VD: STAFF) | Ngoài tập hợp (STAFF) |
| Kỹ năng (AGENT) | AGENT bắt buộc ≥ 1 kỹ năng | AGENT có ≥ 1 kỹ năng | AGENT có 0 kỹ năng | 0 kỹ năng (I\_); ≥ 1 kỹ năng (V\_) |
| Kỹ năng (MGMT) | KHÔNG bắt buộc cho MANAGER/ADMIN | MANAGER với skills=\[\] | — | — |
| Phân quyền | Chỉ ADMIN/MANAGER tạo tài khoản | ADMIN/MANAGER gọi thành công | Không token; token AGENT | Xác thực (401); phân quyền (403) |

 

***Bảng EP & BVA — Đăng nhập Bàn làm việc (Luồng con A-1)***

| Field | Điều kiện đặc tả | Phân vùng hợp lệ (V\_) | Phân vùng không hợp lệ (I\_) | Điểm biên cần test |
| ----- | ----- | ----- | ----- | ----- |
| Email \+ Mật khẩu | Bắt buộc, đúng định dạng | Tồn tại \+ mật khẩu đúng → token, status=OFFLINE | Bỏ trống; không tồn tại; sai mật khẩu | Rỗng; không tồn tại; sai mật khẩu |
| Trạng thái tài khoản | Phải Hoạt động (is\_active=true) | Tài khoản Hoạt động | Tài khoản Khóa → chặn (E-5) | Khóa đăng nhập với mật khẩu đúng |
| Phiên làm việc | Token hợp lệ | Gọi /me với token nhân viên | Không token; token khách hàng | Không token (401); sai vai trò (401) |

 

***1.1.2 Bảng quyết định (Decision Table) — Đăng nhập nhân viên (A-1)***

| Điều kiện / Hành động | R1 | R2 | R3 | R4 | R5 |
| ----- | :---: | :---: | :---: | :---: | :---: |
| C: Đã nhập đủ email & mật khẩu? | F | T | T | T | T |
| C: Tài khoản tồn tại? | \- | F | T | T | T |
| C: Tài khoản bị khóa (is\_active=false)? | \- | \- | T | F | F |
| C: Mật khẩu đúng? | \- | \- | \- | F | T |
| A: E-1 Báo lỗi bỏ trống trường bắt buộc | X |   |   |   |   |
| A: E-6 Báo lỗi email/mật khẩu không chính xác |   | X |   | X |   |
| A: E-5 Cảnh báo tài khoản khóa/ngừng kích hoạt |   |   | X |   |   |
| A: Khởi tạo phiên an toàn (token, OFFLINE) |   |   |   |   | X |
| TC tiêu biểu | TC\_ACC\_25 | TC\_ACC\_22/23 | TC\_ACC\_24 | TC\_ACC\_22 | TC\_ACC\_21 |

 

***1.1.3 Sơ đồ chuyển trạng thái (State Transition) — Tài khoản nhân viên***

| Trạng thái hiện tại | Điều kiện / Sự kiện | Trạng thái tiếp theo |
| ----- | ----- | ----- |
| Hoạt động (mới tạo, OFFLINE) | Quản trị viên khóa (is\_active=false) | Khóa |
| Khóa | Quản trị viên mở khóa (is\_active=true) | Hoạt động |
| Hoạt động | Đăng nhập thành công (A-1) | Hoạt động \+ phiên làm việc (mặc định OFFLINE, ≤ 24h) |
| Hoạt động | Đăng nhập bằng tài khoản khóa | Hoạt động (chặn qua E-5) |
| Khóa | Đăng nhập với mật khẩu đúng | Khóa (vẫn chặn, E-5) |

 

**1.2 UC 3.2 — Quản lý trạng thái làm việc của nhân viên**

***1.2.1 Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)***

| Field | Điều kiện đặc tả | Phân vùng hợp lệ (V\_) | Phân vùng không hợp lệ (I\_) | Điểm biên cần test |
| ----- | ----- | ----- | ----- | ----- |
| Trạng thái (status) | Chỉ ONLINE / BUSY / OFFLINE, chuẩn hóa hoa | ONLINE, BUSY, OFFLINE | Giá trị khác (AWAY); rỗng | Đúng tập hợp; ngoài tập hợp; rỗng |
| Viết hoa/thường | Không phân biệt hoa thường | online (thường) → ONLINE | — | Chữ thường |
| Xác thực | Chỉ nhân viên đã đăng nhập | Token nhân viên hợp lệ | Không token; token khách hàng | Không token (401); sai vai trò (401) |
| Đồng bộ | Cập nhật tức thời toàn hệ thống | Đọc lại qua /me phản ánh đúng | — | Sau khi đổi, đọc lại trạng thái |

 

***1.2.2 Bảng quyết định (Decision Table) — Cập nhật trạng thái***

| Điều kiện / Hành động | R1 | R2 | R3 |
| ----- | :---: | :---: | :---: |
| C: Token xác thực hợp lệ (nhân viên)? | F | T | T |
| C: Giá trị ∈ {ONLINE, BUSY, OFFLINE}? | \- | F | T |
| A: 401 — chưa xác thực / sai vai trò | X |   |   |
| A: 422 — trạng thái không hợp lệ |   | X |   |
| A: 200 — ghi nhận & đồng bộ trạng thái mới |   |   | X |
| TC tiêu biểu | TC\_STT\_07/08 | TC\_STT\_05/06 | TC\_STT\_01–04 |

 

***1.2.3 Sơ đồ chuyển trạng thái (State Transition) — Trạng thái làm việc***

| Trạng thái hiện tại | Điều kiện / Sự kiện | Trạng thái tiếp theo |
| ----- | ----- | ----- |
| OFFLINE | Nhân viên chọn ONLINE | ONLINE |
| ONLINE | Nhân viên chọn BUSY | BUSY |
| BUSY | Nhân viên chọn OFFLINE | OFFLINE |
| ONLINE/BUSY | Mất kết nối realtime \> 30s (E-1) | OFFLINE (tự động) |
| OFFLINE | WS kết nối lại / chọn lại trạng thái | ONLINE (tự động) / tùy chọn |

 

**1.3 UC 3.3 — Theo dõi hàng đợi và tiếp quản cuộc trò chuyện**

***1.3.1 Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)***

| Field | Điều kiện đặc tả | Phân vùng hợp lệ (V\_) | Phân vùng không hợp lệ (I\_) | Điểm biên cần test |
| ----- | ----- | ----- | ----- | ----- |
| Nội dung tin nhắn | Bắt buộc, 1–4000 ký tự | 1–4000 ký tự | Rỗng; \> 4000 ký tự | Min=1 (a); Min−=0 (rỗng); Max+=4001 |
| ID phiên | Phiên tồn tại | ID hợp lệ có trong DB | ID không tồn tại | UUID ngẫu nhiên (404) |
| Xác thực | Chỉ nhân viên có phiên hợp lệ | Token AGENT/MANAGER/ADMIN | Không token; token khách hàng | Không token (401); sai vai trò (401) |
| Cờ đỏ / chế độ chờ | WAITING\_HUMAN \+ is\_flagged=true | Phiên trong hàng đợi (kèm tên khách \+ tin cuối) | Phiên đã ai tiếp quản → không còn cờ | Có/không cờ đỏ |
| Quyền tiếp quản | Chỉ phiên chưa ai nhận | Chưa có assigned\_agent → nhận thành công | Đã có NV khác → 409 (E-1) | Xung đột (409); không tồn tại (404) |
| Đọc/ghi (Chỉ xem) | NV đọc mọi phiên cờ đỏ/chờ/human; chỉ chủ phiên ghi | Chủ phiên ghi (201); NV khác đọc (200) | NV khác ghi vào phiên người khác → 403 | Đọc (200) / Ghi (403) |
| Xóa phiên (E-4) | Khách xóa phiên đang được tiếp quản | Xóa OK, phát CONVERSATION\_DELETED, gỡ hàng đợi | Sau xóa truy vấn → 404 | Sự kiện realtime; 404 sau xóa |

 

***1.3.2 Bảng quyết định (Decision Table) — Tiếp quản & ghi tin nhắn***

| Điều kiện / Hành động | R1 | R2 | R3 | R4 | R5 |
| ----- | :---: | :---: | :---: | :---: | :---: |
| C: Phiên tồn tại? | F | T | T | T | T |
| C: Phiên cờ đỏ/chờ & chưa ai nhận? | \- | F | T | \- | \- |
| C: Là chính nhân viên được gán? | \- | \- | \- | T | F |
| C: Thao tác là GHI (gửi tin)? | \- | \- | \- | T | T |
| A: 404 — phiên không tồn tại | X |   |   |   |   |
| A: 409 — đã có NV khác tiếp quản (E-1) |   | X |   |   |   |
| A: 200 — giao quyền tiếp quản, gỡ cờ đỏ, ngắt Bot AI |   |   | X |   |   |
| A: 201 — lưu tin sender\_type=AGENT (D-1) |   |   |   | X |   |
| A: 403 — khóa ghi, chế độ Chỉ xem (E-1) |   |   |   |   | X |
| TC tiêu biểu | TC\_QTK\_14 | TC\_QTK\_11 | TC\_QTK\_04/05 | TC\_QTK\_07/10 | TC\_QTK\_12/13 |

 

***1.3.3 Sơ đồ chuyển trạng thái (State Transition) — Phiên trò chuyện***

| Trạng thái hiện tại | Điều kiện / Sự kiện | Trạng thái tiếp theo |
| ----- | ----- | ----- |
| BOT | Khách yêu cầu gặp tư vấn viên / AI dựng cờ đỏ | WAITING\_HUMAN (cờ đỏ, vào hàng đợi) |
| WAITING\_HUMAN | Nhân viên tiếp quản thành công (B-3) | HUMAN (gỡ cờ đỏ, ngắt Bot AI) |
| WAITING\_HUMAN / HUMAN | Khách xóa phiên (E-4) | Đã xóa (phát CONVERSATION\_DELETED, gỡ hàng đợi) |
| HUMAN (của NV khác) | NV thứ hai tiếp quản / ghi tin (E-1) | HUMAN (không đổi — từ chối 409; khóa ghi 403, Chỉ xem) |

 

**1.4 UC 3.4 — Quản lý và sử dụng mẫu phản hồi nhanh**

***1.4.1 Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)***

| Field | Điều kiện đặc tả | Phân vùng hợp lệ (V\_) | Phân vùng không hợp lệ (I\_) | Điểm biên cần test |
| ----- | ----- | ----- | ----- | ----- |
| Phím tắt (shortcut) | Bắt đầu /, liền không khoảng trắng, body 1–49 (tổng 2–50), duy nhất | /chao; body 1–49 | Không bắt đầu /; có khoảng trắng; body 0; body 50; trùng | Body min=1; Max+=50; thiếu /; có khoảng trắng; trùng (400) |
| Tiêu đề (title) | Bắt buộc, 3–150 ký tự | 3–150 ký tự | \< 3; \> 150; rỗng | Min=3 (Abc); Min−=2 (Ab); Max+=151; rỗng |
| Nội dung (content) | Bắt buộc, 5–2000 ký tự | 5–2000 ký tự | \< 5; \> 2000 | Min=5 (Abcde); Min−=4 (Abcd); Max+=2001 |
| Danh mục (category) | Bắt buộc, 2–50 ký tự | 2–50 ký tự | \< 2; \> 50 | Min=2 (XY); Min−=1 (X) |
| Xác thực & phân quyền | AGENT/MANAGER/ADMIN; sửa/xóa: chủ mẫu hoặc quản lý | Chủ sở hữu (200); MANAGER/ADMIN (200) | Không token (401); token khách (401); NV khác (403); xóa lặp (404) | KHÔNG token; sai vai trò; không phải chủ; xóa lặp |
| Tìm kiếm / lọc | Tra cứu theo từ khóa (q) & danh mục | Tìm thấy ≥ 1 mẫu khớp | Không khớp → danh sách rỗng (E-1) | Từ khóa có kết quả; từ khóa không có kết quả |

 

***1.4.2 Bảng quyết định (Decision Table) — Quyền chỉnh sửa / xóa mẫu phản hồi***

| Điều kiện / Hành động | R1 | R2 | R3 | R4 |
| ----- | :---: | :---: | :---: | :---: |
| C: Đã xác thực (AGENT/MANAGER/ADMIN)? | F | T | T | T |
| C: Là chủ sở hữu mẫu (created\_by \= user)? | \- | F | T | \- |
| C: Vai trò MANAGER/ADMIN? | \- | T | \- | T |
| A: 401 — chưa xác thực / sai vai trò | X |   |   |   |
| A: 403 — không phải chủ, không phải quản lý |   | X |   |   |
| A: 200 — cho phép chỉnh sửa/xóa |   |   | X | X |
| TC tiêu biểu | TC\_CAN\_15/16 | TC\_CAN\_20/23 | TC\_CAN\_19/24 | TC\_CAN\_22 |

 

***1.4.3 Sơ đồ chuyển trạng thái (State Transition)***

*Không áp dụng — UC 3.4 thuần CRUD (tạo / đọc / sửa / xóa) cho kho mẫu, không có vòng đời hữu hạn của đối tượng; đã thay bằng ma trận quyền ở mục 1.4.2.*

**2\. MA TRẬN TRUY XUẤT NGUỒN GỐC (TRACEABILITY MATRIX — RTM)**

Nguyên tắc thỏa mãn: 100% Coverage — mọi luồng chính, luồng con, ngoại lệ (E-x) và quy tắc nghiệp vụ đều có TC tương ứng; mọi TC đều ánh xạ về yêu cầu cụ thể.

**2.1 UC 3.1 — Quản lý tài khoản nhân viên**

| Req\_ID / Yêu cầu | Mã Test Case tương ứng (TC\_ID) |
| ----- | ----- |
| REQ3.1-F1 — Luồng chính: Tạo tài khoản nhân sự (toàn V\_) | TC\_ACC\_01, 04, 05, 11, 13, 18, 31 |
| REQ3.1-F2 — Khởi tạo trạng thái mặc định OFFLINE | TC\_ACC\_01 |
| REQ3.1-A1 — Luồng con: Đăng nhập Bàn làm việc | TC\_ACC\_21, 25, 26, 27, 28 |
| REQ3.1-E1 — Bỏ trống trường bắt buộc | TC\_ACC\_25, 30 |
| REQ3.1-E2 — Định dạng dữ liệu không hợp lệ | TC\_ACC\_02, 03, 06, 08, 09, 10, 12, 14, 15, 16 |
| REQ3.1-E3 — Mật khẩu xác nhận không khớp (giao diện) | TC\_ACC\_32 (tĩnh UI) |
| REQ3.1-E4 — Email đã tồn tại | TC\_ACC\_07 |
| REQ3.1-E5 — Tài khoản bị khóa | TC\_ACC\_24 |
| REQ3.1-E6 — Thông tin đăng nhập không chính xác | TC\_ACC\_22, 23 |
| REQ3.1-BR1 — Tính duy nhất email | TC\_ACC\_07 |
| REQ3.1-BR2 — AGENT bắt buộc ≥ 1 kỹ năng | TC\_ACC\_17 |
| REQ3.1-BR3 — Đăng nhập luôn OFFLINE | TC\_ACC\_01, 21 |
| REQ3.1-BR4 — Phiên hiệu lực ≤ 24h | TC\_ACC\_21, 27 |
| REQ3.1-QTKN — Phân quyền tạo tài khoản (RBAC) | TC\_ACC\_19, 20 |

 

**2.2 UC 3.2 — Quản lý trạng thái làm việc**

| Req\_ID / Yêu cầu | Mã Test Case tương ứng (TC\_ID) |
| ----- | ----- |
| REQ3.2-F1 — Chuyển đổi trạng thái OFFLINE/ONLINE/BUSY | TC\_STT\_01, 02, 03, 04, 09 |
| REQ3.2-E1 — Mất kết nối realtime → tự OFFLINE & kết nối lại | TC\_STT\_10 (thực tế), TC\_STT\_11 (tĩnh UI) |
| REQ3.2-BR1 — Chỉ ONLINE nhận việc mới | TC\_STT\_01 |
| REQ3.2-BR2 — BUSY tạm dừng nhận việc mới | TC\_STT\_02 |
| REQ3.2-BR3 — Đồng bộ tức thời | TC\_STT\_09 |
| (Bổ sung) — Xác thực khi đổi trạng thái | TC\_STT\_05, 06, 07, 08 |

 

**2.3 UC 3.3 — Theo dõi hàng đợi & tiếp quản cuộc trò chuyện**

| Req\_ID / Yêu cầu | Mã Test Case tương ứng (TC\_ID) |
| ----- | ----- |
| REQ3.3-F1 — Xem hàng đợi (cờ đỏ, tên khách, tin cuối) | TC\_QTK\_01, 02, 03 |
| REQ3.3-F2 — Tải lịch sử & tiếp quản cuộc trò chuyện | TC\_QTK\_04, 05, 06 |
| REQ3.3-F3 — Nhắn tin hai chiều (D-1, sender\_type=AGENT) | TC\_QTK\_07, 10 |
| REQ3.3-E1 — Phiên đã bị NV khác tiếp quản → 409 \+ Chỉ xem | TC\_QTK\_11, 12, 13 |
| REQ3.3-E2 — Nội dung tin nhắn rỗng | TC\_QTK\_08 (API 422\) \+ TC\_QTK\_16 (tĩnh UI) |
| REQ3.3-E3 — Mất kết nối thời gian thực khi gửi | TC\_QTK\_17 (tĩnh UI) |
| REQ3.3-E4 — Phiên bị xóa khi đang tiếp quản | TC\_QTK\_15 |
| REQ3.3-BR1 — Chống xung đột 1 phiên \= 1 NV | TC\_QTK\_11 |
| REQ3.3-BR2 — Ngắt hoàn toàn Bot AI khi tiếp quản | TC\_QTK\_04 |
| REQ3.3-BR3 — Minh bạch lịch sử | TC\_QTK\_06 |
| REQ3.3-BR5 — Dọn thẻ khỏi hàng đợi khi phiên bị xóa | TC\_QTK\_15 |
| (Bổ sung) — Phiên không tồn tại; độ dài tin nhắn | TC\_QTK\_14, 09 |

 

**2.4 UC 3.4 — Quản lý và sử dụng mẫu phản hồi nhanh**

| Req\_ID / Yêu cầu | Mã Test Case tương ứng (TC\_ID) |
| ----- | ----- |
| REQ3.4-F1 — Gõ / hiển thị bảng gợi ý, chèn mẫu | TC\_CAN\_29 (tĩnh UI) |
| REQ3.4-F2 — Tra cứu/danh sách mẫu (lọc category, tìm q) | TC\_CAN\_17, 18, 28 |
| REQ3.4-A1 — Khởi tạo mẫu phản hồi mới | TC\_CAN\_01, 04, 07, 10, 13 |
| REQ3.4-E1 — Không tìm thấy mẫu phù hợp | TC\_CAN\_26 (API) \+ TC\_CAN\_30 (tĩnh UI) |
| REQ3.4-E2 — Bỏ trống trường bắt buộc | TC\_CAN\_27 |
| REQ3.4-E3 — Phím tắt sai định dạng / đã tồn tại | TC\_CAN\_02, 03, 05, 14 |
| REQ3.4-BR1 — Tính duy nhất phím tắt | TC\_CAN\_14, 21 |
| REQ3.4-BR2 — Chỉnh sửa mẫu trước khi gửi | TC\_CAN\_19 |
| REQ3.4-BR3 — Đồng bộ dùng chung | TC\_CAN\_17, 28 |
| REQ3.4-PQ — Phân quyền truy cập & chỉnh sửa | TC\_CAN\_15, 16, 20, 22, 23, 24, 25 |

 

**3\. THIẾT KẾ CA KIỂM THỬ CHI TIẾT (TEST CASE SPECIFICATION — IEEE)**

Quy ước trạng thái: PASS \= thực thi trên hệ thống thật đạt kỳ vọng. TC ghi chú (tĩnh UI) \= kiểm thử tĩnh mã nguồn giao diện (bằng chứng file:dòng), không qua thao tác trình duyệt.

**3.1 UC 3.1 — Quản lý tài khoản nhân viên**

| TC\_ID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---: | ----- | ----- | ----- | ----- | ----- | :---: |
| TC\_ACC\_01 | Tạo AGENT hợp lệ (Happy Path tổ hợp toàn V\_) | Đăng nhập ADMIN; biểu mẫu tạo nhân sự | 1\. Điền họ tên, email, SĐT, vai trò AGENT, kỹ năng, mật khẩu.2\. Bấm 'Tạo tài khoản nhân sự' | full\_name='Nguyen Van Test'; email=kt.ag1.\*@pethome.vn; phone=0912345678; role=AGENT; skills=\['Doi tra'\]; password='Agent@12345' | HTTP 201; role=AGENT, status=OFFLINE, is\_active=true | PASS |
| TC\_ACC\_02 | Họ tên \< Min (1 ký tự) | Như trên | Nhập họ tên A | full\_name='A' | 422 (string\_too\_short, min=2) | PASS |
| TC\_ACC\_03 | Họ tên \> Max (101 ký tự) | Như trên | Nhập họ tên A×101 | full\_name='A'\*101 | 422 | PASS |
| TC\_ACC\_04 | Họ tên \= Min (2 ký tự) | Như trên | Nhập họ tên Ab | full\_name='Ab' | 201 | PASS |
| TC\_ACC\_05 | Họ tên \= Max (100 ký tự) | Như trên | Nhập họ tên A×100 | full\_name='A'\*100 | 201 | PASS |
| TC\_ACC\_06 | Email sai định dạng | Như trên | Nhập email không hợp lệ | email='khongphaiemail' | 422 | PASS |
| TC\_ACC\_07 | Email trùng đã tồn tại (E-4) | Đã có email ag1 | Nhập email giống TC\_ACC\_01 | email \= email của ag1 | 400, 'đã được sử dụng' | PASS |
| TC\_ACC\_08 | Email \> 255 ký tự (Max+=1 \= 256\) | Như trên | Nhập email siêu dài | email='a'\*251+'@x.vn' (256 ký tự) | 422/400 (chặn) | PASS |
| TC\_ACC\_09 | SĐT 9 chữ số (I\_) | Như trên | Nhập SĐT thiếu 1 số | phone='091234567' | 422 | PASS |
| TC\_ACC\_10 | SĐT đầu khác 0 (I\_) | Như trên | Nhập SĐT đầu 1 | phone='1912345678' | 422 | PASS |
| TC\_ACC\_11 | SĐT hợp lệ 10 số đầu 0 (V\_) | Như trên | Nhập SĐT chuẩn | phone='0987654321' | 201 | PASS |
| TC\_ACC\_12 | Mật khẩu 7 ký tự (\< Min 8\) | Như trên | Nhập mật khẩu ngắn | password='Pass123' | 422 | PASS |
| TC\_ACC\_13 | Mật khẩu \= Min 8, đủ chữ & số | Như trên | Nhập mật khẩu chuẩn | password='Passw0rd' | 201 | PASS |
| TC\_ACC\_14 | Mật khẩu thiếu chữ số | Như trên | Nhập mật khẩu toàn chữ | password='Passworddd' | 422 (cần chữ cái & số) | PASS |
| TC\_ACC\_15 | Mật khẩu toàn chữ số (thiếu chữ cái) | Như trên | Nhập mật khẩu toàn số | password='12345678' | 422 | PASS |
| TC\_ACC\_16 | Vai trò không hợp lệ (I\_) | Như trên | Chọn vai trò STAFF | role='STAFF' | 422 | PASS |
| TC\_ACC\_17 | AGENT bỏ trống kỹ năng (QTKN) | Như trên | Không chọn kỹ năng | skills=\[\] | 422 (bắt buộc ≥ 1 kỹ năng) | PASS |
| TC\_ACC\_18 | MANAGER không cần kỹ năng (V\_) | Như trên | Tạo MANAGER, skills rỗng | role=MANAGER, skills=\[\] | 201 role=MANAGER | PASS |
| TC\_ACC\_19 | Không kèm token khi tạo (I\_) | Chưa đăng nhập | Gọi API tạo tài khoản | Không có Authorization | 401 | PASS |
| TC\_ACC\_20 | AGENT gọi API tạo tài khoản (RBAC) | Đăng nhập bởi AGENT | Dùng token AGENT gọi tạo | token AGENT | 403 | PASS |
| TC\_ACC\_21 | Đăng nhập hợp lệ (A-1 Happy Path) | AG1 tạo thành công | Nhập email \+ mật khẩu đúng, bấm Đăng nhập | email=ag1; password='Agent@12345' | 200, access\_token, role=AGENT, status=OFFLINE | PASS |
| TC\_ACC\_22 | Đăng nhập sai mật khẩu (E-6) | AG1 tồn tại | Nhập sai mật khẩu | password='SaiMatKhau1' | 401 'không chính xác' | PASS |
| TC\_ACC\_23 | Email không tồn tại (E-6) | — | Nhập email lạ | email='khongtontai@pethome.vn' | 401 | PASS |
| TC\_ACC\_24 | Tài khoản bị khóa đăng nhập (E-5) | Tài khoản LOCKED is\_active=false | Nhập đúng mật khẩu của tài khoản khóa | email=locked; password đúng | 403 'khóa' | PASS |
| TC\_ACC\_25 | Bỏ trống email khi đăng nhập (E-1) | Màn hình đăng nhập | Để trống email | email='' | 422 | PASS |
| TC\_ACC\_26 | Gọi /me không token | — | Gọi endpoint thông tin bản thân | Không token | 401 | PASS |
| TC\_ACC\_27 | /me với token hợp lệ | Đăng nhập AG1 | Gọi /me | token AG1 | 200, đúng email | PASS |
| TC\_ACC\_28 | /me bằng token khách hàng (sai vai trò) | Khách đã đăng ký | Gọi /me | token khách hàng | 401 (từ chối vai trò) | PASS |
| TC\_ACC\_30 | Tạo tài khoản bỏ trống Họ tên (E-1) | Đăng nhập ADMIN | Bỏ trống họ tên | full\_name='' | 422 | PASS |
| TC\_ACC\_31 | Bỏ trống SĐT — trường tùy chọn (V\_) | Đăng nhập ADMIN | Không nhập SĐT | phone='' | 201 (SĐT rỗng chấp nhận) | PASS |
| TC\_ACC\_32 | Mật khẩu xác nhận không khớp (E-3) | (tĩnh UI) | Nhập confirm\_password khác password | confirm\_password='KhacPassword' | Ép hiển thị lỗi 'Mật khẩu xác nhận không trùng khớp' — StaffConsole.jsx:146 | PASS (tĩnh UI) |

 

**3.2 UC 3.2 — Quản lý trạng thái làm việc**

| TC\_ID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---: | ----- | ----- | ----- | ----- | ----- | :---: |
| TC\_STT\_01 | OFFLINE → ONLINE | AG1 đăng nhập, OFFLINE | Chọn 'Trực tuyến' (ONLINE) | status='ONLINE' | 200, status=ONLINE | PASS |
| TC\_STT\_02 | ONLINE → BUSY | Đang ONLINE | Chọn 'Bận' (BUSY) | status='BUSY' | 200, status=BUSY | PASS |
| TC\_STT\_03 | BUSY → OFFLINE | Đang BUSY | Chọn 'Ngoại tuyến' (OFFLINE) | status='OFFLINE' | 200, status=OFFLINE | PASS |
| TC\_STT\_04 | Chuẩn hóa chữ thường | Đang OFFLINE | Nhập trạng thái chữ thường | status='online' | 200, chuẩn hóa status=ONLINE | PASS |
| TC\_STT\_05 | Trạng thái không hợp lệ (I\_) | Đã đăng nhập | Gửi trạng thái AWAY | status='AWAY' | 422 | PASS |
| TC\_STT\_06 | Trạng thái rỗng (I\_) | Đã đăng nhập | Gửi trạng thái rỗng | status='' | 422 | PASS |
| TC\_STT\_07 | Đổi trạng thái không token (I\_) | Chưa đăng nhập | Gọi API đổi trạng thái | Không token | 401 | PASS |
| TC\_STT\_08 | Token khách hàng đổi trạng thái (I\_) | Khách đăng nhập | Dùng token khách gọi đổi status | token khách hàng | 401 | PASS |
| TC\_STT\_09 | Đồng bộ trạng thái toàn hệ thống | Đã ONLINE | Đổi ONLINE → đọc lại /me | status='ONLINE' | 200, /me phản ánh status=ONLINE | PASS |
| TC\_STT\_10 | E-1: rớt kết nối → tự OFFLINE | AG1 ONLINE | Mở WS /ws/alerts, đóng kết nối, chờ \< 40s | đóng WebSocket | Sau \> 30s status tự chuyển OFFLINE (presence heartbeat) | PASS |
| TC\_STT\_11 | E-1: chỉ báo kết nối & tự kết nối lại | (tĩnh UI) | Rớt mạng | — | Hiển thị 'Reconnecting...' \+ tự kết nối lại — AgentLiveChat.jsx:324 | PASS (tĩnh UI) |

 

**3.3 UC 3.3 — Theo dõi hàng đợi & tiếp quản cuộc trò chuyện**

| TC\_ID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---: | ----- | ----- | ----- | ----- | ----- | :---: |
| TC\_QTK\_01 | Xem hàng đợi không token | — | Mở hàng đợi khi chưa đăng nhập | Không token | 401 | PASS |
| TC\_QTK\_02 | Token khách xem hàng đợi | Khách đăng nhập | Dùng token khách gọi xem hàng đợi | token khách hàng | 401 | PASS |
| TC\_QTK\_03 | Xem hàng đợi (cờ đỏ, tên khách, tin cuối) | Phiên A: WAITING\_HUMAN \+ cờ đỏ | Đăng nhập AGENT, mở trang hàng đợi | token AG1 | 200; list chứa phiên A kèm customer\_name, last\_message\_content | PASS |
| TC\_QTK\_04 | Tiếp quản phiên chưa ai nhận (B-3) | Phiên A chưa gán | Bấm 'Tiếp quản' phiên A | POST takeover(A) | 200; mode=HUMAN, gán AG1, gỡ cờ đỏ, ngắt Bot AI | PASS |
| TC\_QTK\_05 | Gỡ cờ đỏ khỏi hàng đợi sau tiếp quản | Đã tiếp quản A | Trở lại xem hàng đợi | GET queue | 200; phiên A KHÔNG còn trong hàng đợi | PASS |
| TC\_QTK\_06 | Xem lịch sử tin nhắn trước/sau tiếp quản | Phiên A có tin khách \+ tin BOT | Mở khung chat phiên A | GET messages(A) | 200; có tin sender\_type=CUSTOMER (và BOT) | PASS |
| TC\_QTK\_07 | Nhân viên gửi tin hợp lệ (D-1) | Đang chat phiên A | Gõ nội dung, bấm Gửi | content='Chao ban, toi se ho tro ban ngay.' | 201; sender\_type=AGENT | PASS |
| TC\_QTK\_08 | Gửi tin rỗng (E-2) | Đang chat phiên A | Để trống nội dung, bấm Gửi | content='' | 422 (min\_length=1) | PASS |
| TC\_QTK\_09 | Gửi tin \> 4000 ký tự (Max+=1) | Đang chat phiên A | Nhập tin siêu dài | content='x'\*4001 | 422 (max\_length=4000) | PASS |
| TC\_QTK\_10 | Gửi tin 1 ký tự (Min hợp lệ) | Đang chat phiên A | Nhập tin 1 ký tự | content='a' | 201 | PASS |
| TC\_QTK\_11 | Tiếp quản phiên của NV khác (E-1) | Phiên B do AG2 tiếp quản | AG1 bấm 'Tiếp quản' phiên B | POST takeover(B) bằng AG1 | 409; nêu tên NV đã tiếp quản | PASS |
| TC\_QTK\_12 | Đọc phiên do NV khác tiếp quản (Chỉ xem) | Phiên B của AG2 | AG1 mở xem lịch sử phiên B | GET messages(B) bằng AG1 | 200 (đọc được — Chỉ xem) | PASS |
| TC\_QTK\_13 | Ghi tin vào phiên của NV khác (E-1) | Phiên B của AG2 | AG1 gửi tin vào phiên B | POST messages(B) bằng AG1 | 403 (chặn ghi) | PASS |
| TC\_QTK\_14 | Tiếp quản phiên không tồn tại | — | Gọi tiếp quản ID lạ | POST takeover(UUID ngẫu nhiên) | 404 | PASS |
| TC\_QTK\_15 | E-4: khách xóa phiên khi đang tiếp quản | Phiên C do AG1 tiếp quản | Khách xóa phiên C → AG1 xem lại | DELETE /conversations/C (khách); GET messages(C) | DELETE 200; phát CONVERSATION\_DELETED; messages→404; phiên biến mất khỏi hàng đợi | PASS |
| TC\_QTK\_16 | E-2: vô hiệu nút Gửi khi rỗng (tĩnh UI) | (tĩnh UI) | Để trống nội dung | content='' | Nút Gửi bị mờ, không gửi — AgentLiveChat.jsx:593 | PASS (tĩnh UI) |
| TC\_QTK\_17 | E-3: mất kết nối khi gửi (tĩnh UI) | (tĩnh UI) | Rớt mạng | — | Chỉ báo 'Reconnecting...' \+ tự kết nối lại — AgentLiveChat.jsx:324 | PASS (tĩnh UI) |

 

**3.4 UC 3.4 — Quản lý và sử dụng mẫu phản hồi nhanh**

| TC\_ID | Mục đích | Tiền điều kiện | Các bước (Steps) | Đầu vào (Input) | Kết quả mong đợi (Expected) | Trạng thái |
| :---: | ----- | ----- | ----- | ----- | ----- | :---: |
| TC\_CAN\_01 | Tạo mẫu hợp lệ (Happy Path) | Đăng nhập AG1 | Cài đặt mẫu → 'Thêm mẫu câu mới' → điền đầy đủ → 'Lưu mẫu câu' | shortcut='/chao-xxx'; title='Loi chao mung'; content='Chao ban, PetHome xin chao.'; category='Chao hoi' | 201; shortcut chuẩn hóa không dấu '/', id trả về | PASS |
| TC\_CAN\_02 | Phím tắt không bắt đầu / (E-3) | Đăng nhập AG1 | Nhập shortcut thiếu / | shortcut='thieu slashXXX' | 422 | PASS |
| TC\_CAN\_03 | Phím tắt chứa khoảng trắng (E-3) | Như trên | Nhập shortcut có khoảng trắng | shortcut='/co khoangXXX' | 422 | PASS |
| TC\_CAN\_04 | Phím tắt body 1 ký tự (Min hợp lệ) | Như trên | Nhập shortcut tối thiểu | shortcut='/aXXXX' | 201 | PASS |
| TC\_CAN\_05 | Phím tắt body 50 ký tự (Max+=1) | Như trên | Nhập shortcut siêu dài | shortcut='/' \+ 'b'\*50 | 422 (body ≤ 49\) | PASS |
| TC\_CAN\_06 | Tiêu đề 2 ký tự (\< Min 3\) | Như trên | Nhập tiêu đề ngắn | title='Ab' | 422 | PASS |
| TC\_CAN\_07 | Tiêu đề 3 ký tự (Min hợp lệ) | Như trên | Nhập tiêu đề chuẩn | title='Abc' | 201 | PASS |
| TC\_CAN\_08 | Tiêu đề 151 ký tự (Max+=1) | Như trên | Nhập tiêu đề dài | title='C'\*151 | 422 (≤ 150\) | PASS |
| TC\_CAN\_09 | Nội dung 4 ký tự (\< Min 5\) | Như trên | Nhập nội dung ngắn | content='Abcd' | 422 | PASS |
| TC\_CAN\_10 | Nội dung 5 ký tự (Min hợp lệ) | Như trên | Nhập nội dung chuẩn | content='Abcde' | 201 | PASS |
| TC\_CAN\_11 | Nội dung 2001 ký tự (Max+=1) | Như trên | Nhập nội dung dài | content='D'\*2001 | 422 (≤ 2000\) | PASS |
| TC\_CAN\_12 | Danh mục 1 ký tự (\< Min 2\) | Như trên | Nhập danh mục ngắn | category='X' | 422 | PASS |
| TC\_CAN\_13 | Danh mục 2 ký tự (Min hợp lệ) | Như trên | Nhập danh mục chuẩn | category='XY' | 201 | PASS |
| TC\_CAN\_14 | Phím tắt trùng (E-3) | Đã có /chao-xxx | Tạo mẫu phím tắt trùng | shortcut trùng TC\_CAN\_01 | 400 'Phím tắt đã tồn tại.' | PASS |
| TC\_CAN\_15 | Tạo mẫu không token | — | Gọi API tạo mẫu | Không token | 401 | PASS |
| TC\_CAN\_16 | Token khách hàng truy cập mẫu | Khách đăng nhập | Gọi danh sách mẫu | token khách hàng | 401 | PASS |
| TC\_CAN\_17 | Xem danh sách mẫu | Đăng nhập AG1 | Mở màn hình quản lý mẫu | GET /canned-responses | 200; có mẫu vừa tạo (TC\_CAN\_01) | PASS |
| TC\_CAN\_18 | Lọc theo danh mục | Có mẫu 'Chao hoi' | Lọc theo danh mục | category='Chao hoi' | 200; chỉ trả mẫu đúng danh mục | PASS |
| TC\_CAN\_19 | Chủ sở hữu cập nhật mẫu | Sở hữu mẫu TC\_CAN\_01 | Sửa tiêu đề | PUT {title='Tieu de da sua'} | 200; title mới | PASS |
| TC\_CAN\_20 | NV khác chỉnh sửa mẫu (I\_) | Có mẫu của AG1 | AG2 sửa mẫu của AG1 | PUT bằng AG2 | 403 | PASS |
| TC\_CAN\_21 | Đổi phím tắt trùng mẫu khác | Có 2 mẫu | Đổi shortcut sang trùng | PUT {shortcut='/c5-xxx'} | 400 | PASS |
| TC\_CAN\_22 | MANAGER chỉnh mẫu của NV khác | Có mẫu của AG1 | MANAGER sửa mẫu | PUT bằng MANAGER | 200 | PASS |
| TC\_CAN\_23 | NV khác xóa mẫu (I\_) | Có mẫu của AG1 | AG2 xóa mẫu của AG1 | DELETE bằng AG2 | 403 | PASS |
| TC\_CAN\_24 | Xóa mẫu (chủ sở hữu) | Sở hữu mẫu | Xóa mẫu của mình | DELETE bằng AG1 | 200 'success' | PASS |
| TC\_CAN\_25 | Xóa mẫu đã xóa (I\_) | Mẫu đã bị xóa | Xóa lại lần 2 | DELETE lặp | 404 | PASS |
| TC\_CAN\_26 | E-1: từ khóa không khớp → rỗng | Có danh sách mẫu | Tìm kiếm từ khóa lạ | q='khong-co-mau-nay-xyz' | 200; danh sách rỗng | PASS |
| TC\_CAN\_27 | E-2: bỏ trống trường bắt buộc | Đăng nhập AG1 | Tạo mẫu với tiêu đề rỗng | title='' | 422 | PASS |
| TC\_CAN\_28 | Tìm kiếm khớp từ khóa | Có mẫu TC\_CAN\_01 | Tìm theo từ khóa | q=ts (mã trong shortcut) | 200; chứa mẫu vừa tạo | PASS |
| TC\_CAN\_29 | F1: gõ / gợi ý & chèn nhanh (tĩnh UI) | (tĩnh UI) | Tại ô chat gõ / → chọn mẫu | '/chao' | Hiện bảng gợi ý, chèn văn bản vào ô soạn thảo — AgentLiveChat.jsx:231 | PASS (tĩnh UI) |
| TC\_CAN\_30 | E-1: không tìm thấy mẫu (tĩnh UI) | (tĩnh UI) | Gõ từ khóa không khớp | // | Bảng gợi ý báo danh sách rỗng — AgentLiveChat.jsx:519 | PASS (tĩnh UI) |

 

**4\. KẾT QUẢ THỰC THI & NHẬN XÉT**

| Chỉ số kiểm thử | Số lượng / Kết quả |
| ----- | :---: |
| Tổng số ca thiết kế | 89 |
| Số ca thực thi thực tế (HTTP/WS) | 83 |
| Số ca kiểm thử tĩnh giao diện (bằng chứng mã nguồn) | 6 |
| Pass | 89 |
| Fail | 0 |
| Tỷ lệ đạt | 100% |

 

**Nhận xét chi tiết theo Use Case**

• UC 3.1: Hệ thống chặn đúng toàn bộ nhánh lỗi (định dạng, trùng email, mật khẩu yếu, khóa tài khoản, phân quyền RBAC). Email bị chặn tại tầng chung (trả 422\) khi vượt độ dài 255 — không rò thông tin tồn tại email.

• UC 3.2: Chuẩn hóa trạng thái chữ thường → hoa (TC\_STT\_04) và cơ chế E-1 (rớt kết nối → tự OFFLINE sau \~30s) hoạt động đúng nhờ Presence Monitor.

• UC 3.3: Cơ chế chống xung đột tiếp quản (409), Chỉ xem (đọc được / ghi bị chặn 403\) và sự kiện CONVERSATION\_DELETED qua Redis đều đạt; lịch sử tin nhắn minh bạch đúng sender\_type.

• UC 3.4: Toàn bộ ràng buộc biên (shortcut/title/content/category) và ma trận quyền (chủ sở hữu / MANAGER) chạy đúng; tìm kiếm/lọc mẫu dùng chung hoạt động.

• Các xác nhận thuần client-side còn lại (E-3 xác nhận mật khẩu, chỉ báo kết nối realtime, vô hiệu nút gửi, bảng gợi ý /) đã kiểm chứng tĩnh bằng mã nguồn giao diện, ghi rõ file:dòng tại từng TC.

