
**1. Phân tích đặc tả & Thiết kế kiểm thử**

**1.1. Phân vùng tương đương (EP) & Phân tích giá trị biên (BVA)**

* **Phương pháp trình bày:** Bảng phân tích theo từng ô nhập liệu (Field).
* *Cột 1: Tên trường dữ liệu.*
* *Cột 2: Điều kiện đặc tả (Ràng buộc).*
* *Cột 3: Phân vùng hợp lệ (Ký hiệu V_).*
* *Cột 4: Phân vùng không hợp lệ (Ký hiệu I_).*
* *Cột 5: Điểm biên cần test.*


* **Quy tắc cốt lõi (Cách tạo ra):**
* **Cách ly từng trường:** Phân tích logic của từng ô nhập liệu một cách độc lập, chưa cần quan tâm chúng kết hợp với nhau ra sao.
* **Tìm đại diện:** Chia dữ liệu thành các vùng mà hệ thống xử lý giống hệt nhau, sau đó chỉ lấy **một giá trị đại diện** cho mỗi vùng để tránh kiểm thử thừa.


* **Khoanh vùng ranh giới:** Bắt buộc bóc tách các điểm cận biên (Max, Min) và vượt biên (Max+, Min-) vì đây là nơi lập trình viên dễ dùng sai toán tử (ví dụ gõ nhầm `<` thành `<=`).





**1.2. Bảng quyết định (Decision Table)**

* **Phương pháp trình bày:** Ma trận Điều kiện - Hành động.


* *Cột 1: Danh sách Điều kiện (Conditions) và Hành động (Actions).*
* *Cột 2 đến n: Các Quy tắc (Rule 1, Rule 2...) - mỗi cột tương đương một luồng nghiệp vụ.*
* *Giá trị ô:* Dùng ký hiệu `T` (True), `F` (False), `-` (Don't care), và `X` (Kích hoạt hành động).




* **Quy tắc cốt lõi (Cách tạo ra):**
* **Giới hạn phạm vi áp dụng:** KHÔNG dùng cho toàn hệ thống hay kiểm tra định dạng chữ/số. Chỉ áp dụng cho hệ thống có **logic tổ hợp (Combinatorial Logic)** dẫn đến nhiều ngã rẽ hành vi.


* **Xác định Condition theo Chốt chặn logic (Validation Gates):** Chốt chặn logic là các rào cản hệ thống bắt buộc phải đi qua để quyết định có cấp quyền xử lý tiếp hay không. Condition phải là câu hỏi Yes/No về trạng thái nghiệp vụ (VD: *Đã điền đủ form chưa? Tài khoản có bị khóa không?*), chứ không phải câu hỏi về định dạng (*Email có chữ @ không?*). Định dạng đã được giải quyết ở EP/BVA.
* **Quy tắc thu gọn (Rule Reduction):** Khi một Condition mang giá trị `F` làm gián đoạn toàn bộ luồng xử lý (VD: Bỏ trống form thì báo lỗi ngay), các Condition phía sau (như *Mật khẩu có đúng không*) không còn ý nghĩa. Đánh dấu gạch ngang `-` (Don't care) để gộp nhánh và giảm tối đa số lượng luật (Rules) không khả thi trên thực tế.





**1.3. Sơ đồ chuyển trạng thái (State Transition) (Áp dụng nếu có)**

* **Phương pháp trình bày:** Bảng hoặc Biểu đồ hình học.
* *Cột 1: Trạng thái hiện tại.*
* *Cột 2: Điều kiện / Sự kiện kích hoạt.*
* *Cột 3: Trạng thái tiếp theo.*


* **Quy tắc cốt lõi:** Bóc tách từ Use Case những đối tượng có "vòng đời" hữu hạn (VD: Đơn hàng *Chờ xử lý $\rightarrow$ Đang giao $\rightarrow$ Hủy*). Mục đích là tìm ra các đường đi hợp lệ và bẫy lỗi các bước nhảy trạng thái trái phép.



---

**2. Ma trận truy xuất nguồn gốc (Traceability Matrix - RTM)**

* **Phương pháp trình bày:** Bảng đối chiếu chéo (Mapping).
* *Cột 1: Mã yêu cầu (Req_ID) hoặc Tên luồng (Luồng chính, E-1, E-2...).*
* *Cột 2: Mã Test Case tương ứng (TC_ID).*


* **Quy tắc cốt lõi:** Thỏa mãn nguyên tắc **100% Coverage**. Không có một Use Case, phân vùng (V_, I_) hay luồng lỗi nào bị bỏ sót không có TC tương ứng, và cũng không có TC nào được tạo ra mà không ánh xạ về một yêu cầu cụ thể.

---

**3. Thiết kế ca kiểm thử chi tiết (Test Case Specification)**

* **Phương pháp trình bày:** Bảng dữ liệu thực thi chuẩn IEEE.
* *TC_ID:* Mã định danh (VD: TC_LOG_01).
* *Mục đích:* Tóm tắt kịch bản.
* *Tiền điều kiện:* Cần có tài khoản sẵn hay không, đang ở màn hình nào.
* *Các bước (Steps):* Thao tác click, nhập liệu thực tế.
* *Dữ liệu đầu vào (Input):* Nhặt giá trị cụ thể từ bảng phân tích EP/BVA ở trên.
* *Kết quả mong đợi (Expected Result):* Ráp hành động từ Bảng quyết định và Use Case.
* *Trạng thái (Status):* Pass / Fail (Chỉ điền khi đã thực thi phần mềm).


* **Quy tắc cốt lõi (Cách tạo ra):**
* **Nguyên tắc "Tổ hợp hợp lệ" (Positive Testing):** Để chứng minh luồng thành công (Happy Path), gộp nhiều giá trị hợp lệ ($V\_$) của các trường khác nhau vào chung một Test Case.
* **Nguyên tắc "Cô lập lỗi" (Negative Testing):** Khi thiết kế Test Case để bẫy lỗi, trong một ca kiểm thử **chỉ được phép chứa duy nhất 1 giá trị không hợp lệ ($I\_$)**, tất cả các trường còn lại phải giữ ở mức hợp lệ. Nếu bạn nhập sai cùng lúc cả Email và Mật khẩu trong một Test Case, bạn sẽ không thể chứng minh được phần mềm đang xử lý đúng chốt chặn Email hay chốt chặn Mật khẩu.
* **Khả năng tái lập (Reproducibility):** Bảng này là kịch bản "cầm tay chỉ việc". Phải viết sao cho một người hoàn toàn không nắm thuật toán vẫn có thể thực hiện tuần tự các bước và đánh giá chính xác kết quả.