# **_Use case 4.1: Phân chia công việc tự động_** 

|**Tên Use Case**|**Phân chia công việc tự động**|
|---|---|
|Tác nhân|Hệ thống ngầm|
|Điều kiện bắt đầu|1. Có một phiếu hỗ trợ khẩn cấp mới được khởi tạo ở<br>trạng thái "Chờ tiếp nhận" và chưa có người phụ trách.<br>2. Danh sách nhân sự và chuyên môn trực ca của nhân<br>viên đã được kích hoạt trong hệ thống.|
|Luồng sự kiện chính<br>(Tự động chia việc<br>cho nhân viên rảnh<br>nhất)|1. Hệ thống tiếp nhận thông tin từ phiếu hỗ trợ mới và<br>tiến hành kiểm tra tính hợp lệ của các trường dữ liệu<br>đầu vào bắt buộc:<br>- Mã phiếu hỗ trợ: Chuỗi ký tự định danh, chiều dài cố<br>định chính xác 36 ký tự, cấu tạo từ các chữ cái in<br>thường a-f, chữ cái in hoa A-F, chữ số 0-9 và dấu gạch<br>ngang phân tách.<br>- Danh mục sự cố: Chuỗi ký tự, bắt buộc phải khớp<br>tuyệt đối với một trong sáu giá trị: Lỗi đơn hàng, Đổi<br>trả/Hoàn tiền, Sản phẩm lỗi, Lỗi thanh toán, Thái độ<br>phục vụ, hoặc Vấn đề khác.<br>- Mức độ ưu tiên: Chuỗi ký tự, bắt buộc phải khớp<br>chính xác một trong ba giá trị: P1, P2, hoặc P3.<br>- Tóm tắt sự cố: Chuỗi văn bản chữ tự nhiên, yêu cầu độ<br>dài đạt tối thiểu 20 ký tự và giới hạn tối đa là 255 ký tự.<br>2. Hệ thống quét danh sách nhân viên tư vấn đang ở<br>trạng thái làm việc "Trực tuyến".<br>3. Hệ thống lọc ra các nhân viên trực tuyến có kỹ năng<br>xử lý phù hợp với danh mục sự cố của phiếu. Nếu<br>không có nhân viên trực tuyến nào phù hợp, hệ thống<br>thực hiện luồng rẽ nhánh E-1.|



||4. Hệ thống đếm số lượng công việc chưa hoàn tất (các<br>phiếu đang ở trạng thái "Chờ tiếp nhận" hoặc "Đang xử<br>lý") của từng nhân viên hợp lệ.<br>5. Hệ thống chọn nhân viên có kết quả đếm số lượng<br>công việc ở mức thấp nhất (giá trị tối thiểu từ 0 trở lên)<br>để phân công. Nếu có từ hai nhân viên trở lên sở hữu số<br>lượng phiếu bằng nhau, hệ thống truy xuất dữ liệu thời<br>gian và ưu tiên chọn người có khoảng cách từ lúc nhận<br>việc lần cuối đến thời điểm hiện tại là lớn nhất.<br>6. Hệ thống gán phiếu hỗ trợ cho nhân viên được chọn<br>và chuyển trạng thái phiếu sang "Đang xử lý".<br>7. Hệ thống chuyển tiếp thông tin phiếu sang chức năng<br>Giám sát thời hạn xử lý cam kết để theo dõi tiến độ.<br>8. Đầu ra: Phiếu hỗ trợ hiển thị trên màn hình làm việc<br>cá nhân của nhân viên được chỉ định kèm thông báo nổi<br>góc màn hình: "Bạn có một phiếu hỗ trợ mới được phân<br>công!". Trạng thái người phụ trách trên danh sách công<br>việc chung được cập nhật theo tên nhân viên.|
|---|---|
|Luồng<br>con<br>(A-1:<br>Quản trị viên can<br>thiệp phân công thủ<br>công)|1. Tại luồng rẽ nhánh E-1, khi phiếu bị chuyển vào danh<br>sách "Chờ phân bổ" do thiếu nhân sự phù hợp, Quản trị<br>viên mở màn hình quản lý danh sách công việc.<br>2. Quản trị viên bấm vào phiếu đang chờ và chọn nút<br>"Phân công thủ công".<br>3. Hệ thống mở cửa sổ giao việc gồm danh sách toàn bộ<br>nhân viên tư vấn kèm trạng thái làm việc hiện tại và số<br>việc đang xử lý của từng người.<br>4. Quản trị viên chọn một nhân viên và bấm "Giao<br>việc".<br>5. Nếu Quản trị viên chưa chọn nhân viên mà đã bấm<br>giao việc, hệ thống thực hiện luồng rẽ nhánh E-2.<br>6. Hệ thống gán phiếu hỗ trợ cho nhân viên được chỉ<br>định, chuyển trạng thái sang "Đang xử lý" và kích hoạt<br>thông báo nhận việc cho nhân viên đó.|



||7. Đầu ra: Phiếu hỗ trợ biến mất khỏi hàng chờ chưa<br>phân bổ và xuất hiện trên bảng việc của nhân viên được<br>chỉ định.<br>8. Use Case kết thúc thành công.|
|---|---|
|Luồng rẽ nhánh|E-1: Không có nhân viên trực tuyến phù hợp chuyên<br>môn<br>1. Hệ thống giữ nguyên phiếu hỗ trợ ở trạng thái "Chờ<br>phân bổ" và để trống người xử lý.<br>2. Hệ thống phát âm thanh cảnh báo và hiển thị thông<br>báo khẩn màu cam trên màn hình Quản trị viên: "Có<br>phiếu hỗ trợ chưa có nhân viên tiếp nhận do thiếu người<br>trực phù hợp!"<br>3. Quản trị viên tiếp nhận cảnh báo và xử lý qua Luồng<br>con A-1.<br>E-2: Chưa chọn nhân viên khi phân công thủ công<br>1. Hệ thống làm sáng viền đỏ khung chọn nhân viên và<br>hiển thị dòng chữ nhắc nhở: "Vui lòng chọn một nhân<br>viên tiếp nhận trước khi bấm Giao việc".<br>2. Quản trị viên chọn nhân viên từ danh sách và bấm<br>"Giao việc" lại từ bước 4 của Luồng con A-1.|
|Quy tắc Nghiệp vụ<br>(Business Rules /<br>Logic)|1. Nguyên tắc phân chia tải tối thiểu: Hệ thống luôn ưu<br>tiên giao việc cho nhân viên đang trực ca có ít đầu việc<br>đang mở nhất nhằm cân bằng khối lượng công việc,<br>tránh người quá tải trong khi người khác ngồi trống<br>việc.<br>2. Tiêu chuẩn tính tải công việc: Khối lượng việc của<br>một nhân viên chỉ tính tổng số các phiếu đang ở trạng<br>thái "Chờ tiếp nhận" hoặc "Đang xử lý". Các phiếu đã<br>đánh dấu giải quyết xong hoặc đã đóng hoàn toàn không<br>được tính vào tải.<br>3. Điều kiện nhân sự hợp lệ: Chỉ những nhân viên đang<br>ở trạng thái làm việc "Trực tuyến" (ONLINE) và có<br>chuyên môn bao hàm danh mục của sự cố mới đủ điều<br>kiện tham gia nhận phân công tự động. Nhân viên đang|



ở trạng thái Bận (BUSY) hoặc Ngoại tuyến (OFFLINE) sẽ bị bỏ qua. 

# **_Use case 4.2: Giám sát thời hạn xử lý cam kết_** 

|**Tên Use Case**|**Giám sát thời hạn xử lý cam kết**|
|---|---|
|Tác nhân|Hệ thống ngầm (Nhân viên CSKH và Quản lý CSKH<br>tiếp nhận kết quả giám sát)|
|Điều kiện bắt đầu|1. Phiếu hỗ trợ đã được phân công cho nhân viên và<br>chuyển sang trạng thái "Đang xử lý".<br>2. Khung chính sách thời gian xử lý theo mức độ ưu tiên<br>đã được ban hành trong hệ thống.|
|Luồng sự kiện chính<br>(Kích hoạt đếm ngược<br>và ghi nhận hoàn thành<br>đúng hạn)|1. . Hệ thống tiếp nhận thông tin từ phiếu hỗ trợ vừa<br>được giao việc và tiến hành kiểm tra tính hợp lệ của các<br>trường dữ liệu đầu vào bắt buộc:<br>- Mã phiếu hỗ trợ: Chuỗi ký tự định danh, độ dài cố định<br>chính xác 36 ký tự, định dạng UUID v4, bao gồm chữ<br>cái in thường a-f, in hoa A-F, chữ số 0-9 và dấu gạch<br>ngang phân tách.<br>- Mức độ ưu tiên: Chuỗi ký tự, bắt buộc thuộc một trong<br>ba giá trị hợp lệ: P1: 15 phút, P2: 60 phút, hoặc P3: 240<br>phút.|
||- Thời hạn xử lý cam kết (T_cam_kết): Thời lượng tối đa<br>quy định theo mức độ ưu tiên: P1 (Cực kỳ khẩn cấp):<br>900 giây; P2 (Khẩn cấp cao): 3.600 giây; P3 (Trung<br>bình): 14.400 giây.<br>2. Hệ thống tính toán mốc thời gian hạn chót cần hoàn<br>tất sự việc và hiển thị đồng hồ đếm ngược trực tiếp trên<br>thẻ công việc.<br>●Thời điểm hạn chót = T_bắt_đầu+ T_cam_kết|



||3. Hệ thống liên tục chạy ngầm để theo dõi, đối chiếu<br>thời gian còn lại (T_còn_lại, tính bằng giây) và phân loại<br>trạng thái:<br>-<br>Trạng thái Bình thường: T_còn_lại > 20% tổng<br>thời gian cam kết (P1 > 180 giây; P2 > 720 giây;<br>P3 > 2.880 giây).<br>-<br>Trạng thái Cảnh báo: 1 giây ≤ T_còn_lại ≤ 20%<br>tổng thời gian cam kết.<br>-<br>Nếu T_còn_lại ≤ 0 giây, hệ thống thực hiện luồng<br>rẽ nhánh E-1.<br>4. Khi nhân viên xử lý xong khiếu nại cho khách hàng,<br>nhân viên chọn nút "Hoàn tất xử lý" trên thẻ công việc.<br>5. Hệ thống hiển thị biểu mẫu yêu cầu nhập kết quả xử<br>lý gồm:<br>- Hệ thống yêu cầu nhập Nội dung kết quả xử lý. Dữ liệu<br>bắt buộc là chuỗi văn bản chữ tự nhiên, không được rỗng<br>hoặc chỉ chứa khoảng trắng, yêu cầu độ dài kí tự trong<br>đoạn  [10, 1.000]<br>6. Nhân viên nhập nội dung và bấm "Xác nhận hoàn<br>thành".<br>7. Hệ thống kiểm tra dữ liệu nội dung. Nếu độ dài < 10<br>ký tự, > 1.000 ký tự, hoặc chuỗi không hợp lệ, hệ thống<br>thực hiện luồng rẽ nhánh E-2.<br>8. Hệ thống dừng đồng hồ đếm ngược, chuyển trạng thái<br>phiếu sang "Đã giải quyết" và ghi nhận đạt chuẩn cam<br>kết thời gian.<br>9. Đầu ra: Thẻ công việc chuyển sang màu xanh lá cây<br>với nhãn "Đạt chuẩn cam kết". Hệ thống hiển thị thông<br>báo nổi: "Phiếu hỗ trợ đã được xử lý thành công đúng<br>thời hạn!".|
|---|---|
|Luồng con|Không có.|
|Luồng rẽ nhánh|E-1: Quá hạn thời gian cam kết xử lý (Vi phạm cam kết<br>dịch vụ)|



||1. Đồng hồ đếm ngược chạm mốc 0 trong khi phiếu vẫn<br>ở trạng thái "Đang xử lý".<br>2. Hệ thống đánh dấu phiếu này ở trạng thái vi phạm<br>thời hạn xử lý.<br>3. Thẻ công việc trên màn hình nhân viên và danh sách<br>giám sát chung lập tức chuyển sang màu đỏ nhấp nháy<br>nổi bật.<br>4. Hệ thống kích hoạt cơ chế báo động leo thang: phát<br>tín hiệu chuông cảnh báo đỏ và gửi thông báo trực tiếp<br>lên bảng theo dõi của Quản lý CSKH với nội dung:<br>"Phiếu hỗ trợ [Mã phiếu] do nhân viên [Tên nhân viên]<br>phụ trách đã quá hạn xử lý!"<br>5. Hệ thống ghi nhận điểm trừ vi phạm cam kết vào báo<br>cáo hiệu suất định kỳ của nhân viên phụ trách.<br>6. Khi nhân viên hoàn thành xử lý muộn, hệ thống vẫn<br>cho phép nhập kết quả giải quyết theo bước 5 của luồng<br>chính nhưng ghi nhận nhãn "Hoàn thành quá hạn".<br>E-2: Để trống nội dung kết quả xử lý<br>1. Hệ thống khoanh viền đỏ ô nhập nội dung và hiển thị<br>dòng chữ báo lỗi: "Vui lòng nhập tóm tắt kết quả đã xử<br>lý cho khách hàng trước khi đóng phiếu".<br>2. Hệ thống giữ nguyên phiếu ở trạng thái "Đang xử lý"<br>và đồng hồ đếm ngược tiếp tục chạy.<br>3. Nhân viên nhập lại nội dung giải quyết và quay lại<br>bước 6 của luồng chính.|
|---|---|
|Quy tắc Nghiệp vụ<br>(Business Rules / Logic)|1. Khung thời gian cam kết theo mức ưu tiên: Thời hạn<br>xử lý bắt buộc được gắn chặt với mức độ khẩn cấp của<br>sự cố: Mức P1 bắt buộc hoàn tất trong vòng 15 phút;<br>Mức P2 tối đa 60 phút; Mức P3 tối đa 240 phút (4 giờ).<br>2. Tiêu chí xác định đạt hoặc vi phạm cam kết: Phiếu hỗ<br>trợ chỉ được tính là hoàn thành đúng cam kết nếu nhân<br>viên bấm xác nhận giải quyết khi đồng hồ đếm ngược|



|chưa về 0. Mọi trường hợp hoàn tất sau mốc này đều bị<br>hệ thống ghi nhận là vi phạm.|
|---|
|3. Cơ chế báo động leo thang bắt buộc: Ngay khi xảy ra<br>vi phạm quá hạn, hệ thống bắt buộc phải phát cảnh báo<br>tức thì tới cấp Quản lý để can thiệp kịp thời, không để<br>khiếu nại của khách hàng bị bỏ quên hoặc xử lý chậm<br>trễ.|



# **_Use case 4.3: Quản lý tiến độ trên bảng Kanban_** 

|**Tên Use Case**|**Quản lý tiến độ trên bảng Kanban**|
|---|---|
|Tác nhân|Nhân viên CSKH, Quản lý CSKH, Quản trị viên|
|Điều kiện bắt đầu|1. Người dùng đã đăng nhập thành công vào hệ thống<br>bằng tài khoản Nhân viên, Quản lý hoặc Quản trị<br>viên.|
||2. Bảng Kanban đang hiển thị ít nhất một phiếu hỗ trợ<br>mà người dùng có quyền cập nhật tiến độ.|
|Luồng sự kiện chính<br>(Kéo thả thẻ công việc<br>sang trạng thái Đã giải<br>quyết)|1. Người dùng mở mục "Bảng công việc Kanban"<br>trên thanh điều hướng.<br>2. Hệ thống hiển thị bảng Kanban gồm 4 cột tiến độ:<br>"Chờ tiếp nhận", "Đang xử lý", "Đã giải quyết" và<br>"Đóng phiếu". Mỗi thẻ công việc hiển thị đầy đủ<br>thông tin mã phiếu, tóm tắt sự cố, nhãn ưu tiên và<br>đồng hồ đếm ngược.|
||3. Nhân viên nhấn giữ một thẻ phiếu hỗ trợ ở cột<br>"Đang xử lý" và kéo thả sang cột "Đã giải quyết".<br>4. Hệ thống tiếp nhận thông tin thẻ phiếu và tiến hành<br>kiểm tra tính hợp lệ của các trường dữ liệu đầu vào<br>bắt buộc:|
||- Mã phiếu hỗ trợ: Chuỗi ký tự định danh, chiều dài<br>cố định chính xác 36 ký tự, định dạng UUID v4, gồm<br>chữ cái in thường a-f, in hoa A-F, chữ số 0-9 và dấu<br>gạch ngang phân tách.|



- Trạng thái hiện tại: Chuỗi ký tự, bắt buộc phải khớp chính xác giá trị "Đang xử lý". - Trạng thái đích: Chuỗi ký tự, bắt buộc phải khớp chính xác giá trị "Đã giải quyết". 5. Hệ thống kiểm tra quyền hạn xử lý phiếu của người dùng. Nếu phiếu không thuộc quyền phụ trách của nhân viên đang thao tác (và nhân viên không có vai trò Quản lý/Quản trị viên), hệ thống thực hiện luồng rẽ nhánh E-1. 

6. Hệ thống kiểm tra quy tắc luân chuyển trạng thái một chiều. Nếu hướng chuyển trạng thái không hợp lệ (ví dụ kéo ngược về trạng thái trước đó), hệ thống thực hiện luồng rẽ nhánh E-2. 7. Hệ thống hiển thị biểu mẫu yêu cầu ghi nhận giải pháp kết quả xử lý với trường thông tin: - Nội dung kết quả xử lý: Chuỗi văn bản chữ tự nhiên bắt buộc; không được rỗng hoặc chỉ chứa khoảng trắng; độ dài nằm trong đoạn biên [10, 1.000] ký tự. 8. Nhân viên nhập nội dung kết quả xử lý và nhấn nút "Xác nhận hoàn thành". 9. Hệ thống kiểm tra dữ liệu nội dung kết quả xử lý. Nếu độ dài < 10 ký tự, > 1.000 ký tự hoặc chuỗi rỗng/khoảng trắng, hệ thống thực hiện luồng rẽ nhánh E-3. 10. Hệ thống kiểm tra kết nối mạng truyền dữ liệu. Nếu mất kết nối trong quá trình lưu dữ liệu về máy chủ, hệ thống thực hiện luồng rẽ nhánh E-4. 11. Hệ thống cập nhật trạng thái phiếu sang "Đã giải quyết", dừng đồng hồ đếm ngược cam kết thời gian, lưu vết thời điểm hoàn tất và tài khoản người thực hiện. 

12. Đầu ra: Hệ thống đóng hộp thoại, hiển thị thông báo nổi màu xanh lá ở góc màn hình: "Cập nhật trạng thái phiếu hỗ trợ thành công!", thẻ công việc nằm cố 

||định tại cột "Đã giải quyết" với nhãn ghi nhận kết quả<br>và đồng hồ đếm ngược dừng lại.|
|---|---|
|Luồng con (A-1: Cập<br>nhật tiến độ từ màn<br>hình chi tiết phiếu)|1. Thay vì kéo thả thẻ, nhân viên nhấp đúp chuột vào<br>một thẻ phiếu trên bảng Kanban để mở cửa sổ "Chi<br>tiết phiếu hỗ trợ".<br>2. Hệ thống hiển thị đầy đủ thông tin sự cố, lịch sử<br>trao đổi và nút chọn "Cập nhật trạng thái".<br>3. Nhân viên nhấp vào danh sách chọn trạng thái. Hệ<br>thống chỉ hiển thị các trạng thái hợp lệ được phép tiến<br>tới tiếp theo (ví dụ: đang ở "Đang xử lý" thì chỉ cho<br>chọn "Đã giải quyết").<br>4. Nhân viên chọn trạng thái "Đã giải quyết" và bấm<br>nút "Lưu thay đổi".<br>5. Hệ thống hiển thị hộp thoại yêu cầu nhập kết quả<br>xử lý giống bước 7 của luồng chính.<br>6. Nhân viên nhập nội dung và bấm "Xác nhận hoàn<br>thành" để tiếp tục từ bước 9 của luồng chính.|
|Luồng rẽ nhánh|E-1: Phiếu không thuộc quyền phụ trách của nhân<br>viên<br>1. Hệ thống từ chối cập nhật, tạo hiệu ứng trượt trả<br>thẻ công việc về lại vị trí ban đầu.<br>2. Hệ thống hiển thị thông báo cảnh báo màu đỏ:<br>"Bạn không có quyền cập nhật phiếu hỗ trợ do nhân<br>viên khác phụ trách!"<br>3. Use Case kết thúc thất bại.<br>E-2: Chuyển trạng thái không hợp lệ<br>1. Hệ thống từ chối cho thả thẻ vào cột đích và trả thẻ<br>về vị trí cột cũ.<br>2. Hệ thống hiển thị thông báo lỗi: "Tiến độ phiếu chỉ<br>được phép chuyển tiến lên theo quy trình, không thể<br>chuyển ngược lại trạng thái trước đó!"<br>3. Use Case kết thúc thất bại.|



|||E-3: Bỏ trống hoặc nhập sai định dạng độ dài nội<br>dung kết quả xử lý<br>1. Hệ thống khoanh viền đỏ ô nhập liệu và hiển thị<br>dòng chữ cảnh báo dưới chân ô: "Nội dung kết quả xử<br>lý là bắt buộc, độ dài từ 10 đến 1.000 ký tự".<br>2. Hệ thống giữ nguyên hộp thoại và giữ thẻ phiếu ở<br>trạng thái "Đang xử lý".<br>3. Nhân viên nhập lại nội dung đúng quy cách và<br>quay lại bước 8 của luồng chính.<br>E-4: Mất kết nối mạng trong lúc lưu dữ liệu<br>1. Hệ thống không thể gửi dữ liệu cập nhật về máy<br>chủ.<br>2. Hệ thống đưa thẻ phiếu về lại cột ban đầu, giữ<br>nguyên trạng thái cũ và hiển thị thông báo: "Mất kết<br>nối mạng, chưa cập nhật được trạng thái. Vui lòng thử<br>lại!"<br>3. Nhân viên kiểm tra kết nối và thao tác lại từ bước 3<br>của luồng chính.|
|---|---|---|
|Quy tắc Nghiệp<br>(Business<br>Rules<br>Logic)|vụ<br>/|1. Phân quyền thao tác trên thẻ công việc: Nhân viên<br>tư vấn chỉ có quyền kéo thả hoặc cập nhật trạng thái<br>đối với các phiếu được phân công trực tiếp cho mình.<br>Quản lý CSKH và Quản trị viên có quyền can thiệp,<br>chuyển trạng thái cho mọi phiếu trên bảng Kanban.<br>2. Quy tắc luân chuyển tiến độ một chiều: Tiến độ của<br>phiếu hỗ trợ bắt buộc phải đi theo trình tự tiến lên:<br>Chờ tiếp nhận → Đang xử lý → Đã giải quyết →<br>Đóng phiếu. Hệ thống không cho phép nhân viên tự ý<br>kéo lùi thẻ về các trạng thái trước đó.<br>3. Điều kiện hoàn tất phiếu: Để đưa một phiếu sang<br>trạng thái "Đã giải quyết", nhân viên bắt buộc phải<br>cung cấp tóm tắt kết quả xử lý với độ dài từ 10 đến<br>1.000 ký tự nhằm phục vụ lưu vết đối soát và đánh<br>giá chất lượng phục vụ.|



4. Điểm dừng đồng hồ cam kết dịch vụ: Ngay khi phiếu được ghi nhận sang trạng thái "Đã giải quyết", đồng hồ đếm ngược sẽ dừng lại. Mốc thời gian hoàn tất này là căn cứ duy nhất để xác định phiếu đó đạt chuẩn hay vi phạm cam kết thời gian xử lý. 

# **_Use case 4.4: Báo cáo thống kê hiệu suất_** 

|**Tên Use Case**|**Báo cáo thống kê hiệu suất**|
|---|---|
|Tác nhân|Quản lý CSKH, Quản trị viên|
|Điều kiện bắt đầu|1. Người dùng đã đăng nhập vào hệ thống bằng tài khoản<br>có vai trò Quản lý CSKH hoặc Quản trị viên.<br>2. Hệ thống đã có dữ liệu về các cuộc trò chuyện và các<br>phiếu hỗ trợ đã phát sinh trong quá trình vận hành.|
|Luồng<br>sự<br>kiện<br>chính (Lọc và xem<br>biểu đồ số liệu vận<br>hành tổng hợp)|1. Người dùng chọn mục "Báo cáo thống kê" trên thanh<br>điều hướng quản trị.<br>2. Hệ thống hiển thị màn hình bộ lọc gồm các trường<br>thông tin đầu vào với quy chuẩn kiểm thử cụ thể:<br>- Khoảng thời gian (Từ ngày - Đến ngày): Trường bắt<br>buộc; định dạng ngày chuẩn DD/MM/YYYY. Ràng buộc<br>biên:<br>T_bắt_đầu <= T_kết_thúc, T_kết_thúc <=<br>T_hiện_tại, và khoảng cách thời gian ΔT = T_kết_thúc -<br>T_bắt_đầu <= 365 ngày.|
||- Nhân viên phụ trách: Trường tùy chọn; chuỗi ký tự<br>chọn từ danh sách nhân viên hiện có hoặc mặc định "Tất<br>cả nhân viên".<br>- Mức độ ưu tiên: Trường tùy chọn; lọc theo một trong<br>các giá trị P1, P2, P3 hoặc mặc định "Tất cả các mức".|



- Danh mục sự cố: Trường tùy chọn; chọn một trong sáu danh mục sự cố hợp lệ hoặc mặc định "Tất cả danh mục". (Lưu ý: Người dùng có thể sử dụng các nút chọn nhanh khoảng thời gian có sẵn bằng cách thực hiện Luồng con A-1). 3. Người dùng thiết lập các tiêu chí lọc mong muốn và nhấn nút "Lọc dữ liệu". Nút bấm tạm thời chuyển sang trạng thái mờ kèm biểu tượng "Đang tải dữ liệu..." để tránh bấm lặp thao tác. 4. Hệ thống kiểm tra tính hợp lệ của khoảng thời gian đã nhập theo các quy chuẩn dữ liệu (định dạng DD/MM/YYYY, T_bắt_đầu <= T_kết_thúc, T_kết_thúc <= T_hiện_tại, và ΔT <= 365 ngày). Nếu vi phạm bất kỳ điều kiện nào, hệ thống thực hiện luồng rẽ nhánh E-1. 5. Nếu kết nối máy chủ bị gián đoạn khi đang truy xuất dữ liệu, hệ thống thực hiện luồng rẽ nhánh E-2. 6. Hệ thống tổng hợp toàn bộ các phiếu hỗ trợ phát sinh trong khoảng thời gian thỏa mãn điều kiện lọc. Nếu không có dữ liệu nào phát sinh, hệ thống thực hiện luồng rẽ nhánh E-3. 7. Hệ thống tính toán các chỉ số vận hành cốt lõi: - Tổng số phiếu phát sinh (N_tổng), số phiếu đã giải quyết (N_giải_quyết), số phiếu đang xử lý (N_đang_xử_lý), số phiếu vi phạm cam kết thời gian (N_vi_phạm). - Tỷ lệ vi phạm cam kết SLA: Công thức tính toán cụ thể: Tỷ lệ vi phạm (%) = (N_vi_phạm / N_tổng) * 100%. Nếu N_tổng = 0, Tỷ lệ vi phạm = 0%. - Tỷ lệ phân bổ cảm xúc của khách hàng (Tích cực, Bình thường, Tiêu cực nhẹ, Bức xúc cao). 8. Đầu ra: Hệ thống hiển thị kết quả gồm các khối số liệu tổng quan nổi bật ở trên cùng, biểu đồ tròn phân bổ mức độ cam kết xử lý và biểu đồ cột so sánh năng suất giải quyết giữa các nhân viên. Góc màn hình hiển thị nút 

||"Xuất báo cáo" (cho phép xuất dữ liệu ra tệp bảng tính<br>excel để lưu trữ).|
|---|---|
|Luồng con (A-1:<br>Chọn nhanh khoảng<br>thời gian thống kê)|1. Tại bước 2 của luồng chính, thay vì tự chọn từng ngày<br>trên lịch, người dùng bấm vào một trong các nút chọn<br>mốc thời gian nhanh gồm: "Hôm nay", "7 ngày qua", "30<br>ngày qua", hoặc "Tháng này".<br>2. Hệ thống tự động tính toán và điền chính xác giá trị<br>vào hai ô "Từ ngày" và "Đến ngày" theo định dạng<br>DD/MM/YYYY tương ứng, đảm bảo các ràng buộc<br>T_bắt_đầu <= T_kết_thúc, T_kết_thúc <= T_hiện_tại và<br>ΔT <= 365 ngày.<br>3. Người dùng kiểm tra lại và nhấn nút "Lọc dữ liệu" để<br>tiếp tục từ bước 3 của luồng chính.|
|Luồng rẽ nhánh|E-1: Khoảng thời gian lọc không hợp lệ<br>1. Hệ thống kiểm tra và phát hiện lỗi dữ liệu thời gian vi<br>phạm quy chuẩn (sai định dạng DD/MM/YYYY,<br>T_bắt_đầu > T_kết_thúc, T_kết_thúc > T_hiện_tại, hoặc<br>ΔT > 365 ngày).<br>2. Hệ thống làm sáng viền đỏ tại ô thời gian bị sai và<br>hiển thị câu thông báo lỗi cụ thể ngay dưới chân ô nhập<br>liệu (Ví dụ: "Ngày nhập không đúng định dạng<br>DD/MM/YYYY", "Ngày bắt đầu phải nhỏ hơn hoặc<br>bằng ngày kết thúc", "Ngày kết thúc không được vượt<br>quá ngày hiện tại", hoặc "Khoảng thời gian tra cứu tối đa<br>không vượt quá 365 ngày").<br>3. Hệ thống giữ nguyên nút "Lọc dữ liệu" ở trạng thái<br>mờ và giữ nguyên các giá trị bộ lọc đã chọn khác.<br>4. Người dùng điều chỉnh lại khoảng thời gian hợp lệ<br>theo chỉ dẫn và quay lại bước 3 của luồng chính.<br>E-2: Gián đoạn kết nối khi tải số liệu thống kê<br>1. Hệ thống không thể tải dữ liệu báo cáo do lỗi đường<br>truyền mạng hoặc máy chủ không phản hồi.<br>2. Hệ thống hiển thị hộp cảnh báo màu vàng cam ở giữa<br>khung báo cáo: "Không thể tải dữ liệu báo cáo do mất|



||kết nối. Vui lòng kiểm tra lại đường truyền và thử lại!"<br>kèm nút bấm "Thử lại".<br>3. Người dùng bấm "Thử lại", hệ thống gửi lại yêu cầu<br>truy xuất từ bước 3 của luồng chính.<br>E-3: Không có dữ liệu phát sinh trong khoảng thời gian<br>lọc<br>1. Trong khoảng thời gian người dùng chọn, hệ thống<br>không ghi nhận bất kỳ phiếu hỗ trợ hay lượt khiếu nại<br>nào phát sinh (N_tổng = 0).<br>2. Hệ thống tạm ẩn các biểu đồ phân tích, hiển thị hình<br>ảnh minh họa cùng dòng chữ thông báo: "Không có dữ<br>liệu phiếu hỗ trợ nào phát sinh trong khoảng thời gian đã<br>chọn".<br>3. Các ô số liệu tổng quan hiển thị giá trị mặc định<br>N_tổng = 0, N_giải_quyết = 0, N_đang_xử_lý = 0,<br>N_vi_phạm = 0 và Tỷ lệ vi phạm SLA = 0%.<br>4. Người dùng có thể chọn lại khoảng thời gian khác<br>rộng hơn để tiếp tục tra cứu.|
|---|---|
|Quy tắc Nghiệp vụ<br>(Business Rules /<br>Logic)|1. Phân quyền truy xuất số liệu: Báo cáo thống kê vận<br>hành chỉ được cung cấp cho tài khoản có vai trò Quản lý<br>CSKH hoặc Quản trị viên hệ thống. Nhân viên tư vấn<br>thông thường không có quyền truy cập vào màn hình này<br>để bảo mật dữ liệu hiệu suất của toàn chuỗi.<br>2. Phạm vi tính toán báo cáo: Một phiếu hỗ trợ được tính<br>vào báo cáo nếu thời điểm khởi tạo phiếu nằm trong<br>khoảng thời gian lọc (tính từ 00:00:00 của ngày bắt đầu<br>T_bắt_đầu đến 23:59:59 của ngày kết thúc T_kết_thúc).<br>Các phiếu bị hủy bỏ hoặc đánh dấu rác/trùng lặp sẽ bị<br>loại trừ.<br>3. Quy chuẩn tính tỷ lệ vi phạm cam kết SLA: Tỷ lệ vi<br>phạm được tính theo công thức Tỷ lệ vi phạm (%) =<br>(N_vi_phạm / N_tổng) * 100%, kết quả hiển thị theo<br>dạng phần trăm (%) và được làm tròn đến một chữ số<br>thập phân. Trường hợp N_tổng = 0 thì tỷ lệ mặc định<br>hiển thị là 0%.|



4. Tính khách quan của dữ liệu: Toàn bộ số liệu và biểu đồ trên màn hình báo cáo là dữ liệu chỉ xem (Read-only). Người dùng không được phép chỉnh sửa số liệu trực tiếp trên bảng thống kê để đảm bảo tính minh bạch và chính xác trong việc đánh giá nhân sự. 

