# Tài liệu Yêu cầu Sản phẩm (PRD)
# Phong Thủy Số - Kiến trúc Agent

## 1. Tổng quan sản phẩm

### 1.1 Giới thiệu
Phong Thủy Số là một ứng dụng cung cấp dịch vụ phong thủy số học, giúp người dùng phân tích và tối ưu hóa các yếu tố số học trong cuộc sống hàng ngày như số điện thoại, CCCD, mật khẩu, và tài khoản ngân hàng dựa trên nguyên lý Bát Cực Linh Số và các nguyên tắc phong thủy truyền thống.

### 1.2 Mục tiêu
- Xây dựng nền tảng phong thủy số học tiên tiến dựa trên kiến trúc agent
- Cung cấp các dịch vụ phân tích và tư vấn phong thủy số học chính xác và hiệu quả
- Tạo ra trải nghiệm người dùng liền mạch và trực quan
- Xây dựng nền tảng có khả năng mở rộng và tích hợp các tính năng mới

### 1.3 Đối tượng người dùng
- Người quan tâm đến phong thủy và muốn áp dụng vào cuộc sống số
- Doanh nghiệp muốn tối ưu hóa các yếu tố số học trong thương hiệu
- Người dùng đang tìm kiếm số điện thoại, CCCD, hoặc tài khoản ngân hàng mới
- Người dùng muốn kiểm tra mức độ phong thủy của các số hiện tại

## 2. Kiến trúc hệ thống

### 2.1 Tổng quan kiến trúc
Hệ thống được thiết kế dựa trên kiến trúc agent, với một Root Agent điều phối và nhiều Specialized Agent xử lý các nhiệm vụ cụ thể. Kiến trúc này sẽ tuân theo các nguyên tắc của A2A Protocol và ADK framework.

### 2.2 Cấu trúc Agent

#### 2.2.1 Root Agent
- **Mục đích**: Điều phối các specialized agent và cung cấp giao diện tương tác thống nhất
- **Chức năng**:
  - Tiếp nhận và phân tích yêu cầu từ người dùng
  - Chuyển giao yêu cầu đến specialized agent phù hợp
  - Tổng hợp và trả về kết quả cho người dùng
  - Quản lý phiên làm việc và trạng thái hội thoại

#### 2.2.2 BatCucLinhSo Agent
- **Mục đích**: Phân tích và tư vấn phong thủy số học
- **Chức năng**:
  - Phân tích số điện thoại theo nguyên lý Bát Cực Linh Số
  - Đề xuất số điện thoại phù hợp với mục đích sử dụng
  - Phân tích 6 số cuối của CCCD
  - Phân tích và đề xuất số tài khoản ngân hàng
  - Tạo và đánh giá mật khẩu theo phong thủy
- **Tools**:
  - PhoneAnalysisTool: Phân tích số điện thoại
  - PhoneRecommendationTool: Đề xuất số điện thoại
  - CCCDAnalysisTool: Phân tích CCCD
  - BankAccountTool: Phân tích và đề xuất số tài khoản
  - PasswordTool: Tạo và đánh giá mật khẩu

#### 2.2.3 Payment Agent
- **Mục đích**: Quản lý thanh toán và gói dịch vụ
- **Chức năng**:
  - Kiểm tra quota người dùng
  - Xử lý giao dịch thanh toán
  - Quản lý các gói dịch vụ
  - Lưu trữ và hiển thị lịch sử thanh toán
- **Tools**:
  - QuotaCheckTool: Kiểm tra số câu hỏi còn lại
  - PaymentProcessingTool: Xử lý thanh toán
  - PaymentHistoryTool: Quản lý lịch sử thanh toán

#### 2.2.4 User Agent
- **Mục đích**: Quản lý thông tin và xác thực người dùng
- **Chức năng**:
  - Đăng ký và đăng nhập người dùng
  - Quản lý thông tin cá nhân
  - Đổi mật khẩu và khôi phục tài khoản
  - Lưu trữ lịch sử sử dụng dịch vụ
- **Tools**:
  - AuthenticationTool: Xác thực người dùng
  - ProfileManagementTool: Quản lý hồ sơ người dùng
  - HistoryTool: Quản lý lịch sử người dùng

#### 2.2.5 Chatbot Agent
- **Mục đích**: Hỗ trợ tương tác với người dùng qua hội thoại
- **Chức năng**:
  - Xử lý câu hỏi tự nhiên từ người dùng
  - Cung cấp thông tin về phong thủy số học
  - Hướng dẫn sử dụng các tính năng của hệ thống
  - Tương tác với các agent khác để trả lời câu hỏi phức tạp
- **Tools**:
  - LLMTool: Tương tác với mô hình ngôn ngữ lớn
  - ConversationMemoryTool: Quản lý bộ nhớ hội thoại
  - AgentDelegationTool: Chuyển giao nhiệm vụ cho agent khác

### 2.3 Luồng dữ liệu
1. Người dùng gửi yêu cầu đến hệ thống
2. Root Agent tiếp nhận và phân tích yêu cầu
3. Root Agent chuyển giao yêu cầu đến Specialized Agent phù hợp
4. Specialized Agent xử lý yêu cầu sử dụng các tools
5. Kết quả được trả về Root Agent
6. Root Agent trả kết quả cho người dùng

## 3. Các tính năng chi tiết

### 3.1 BatCucLinhSo Agent

#### 3.1.1 Phân tích số điện thoại
- **Mô tả**: Phân tích số điện thoại theo nguyên lý Bát Cực Linh Số
- **Input**: Số điện thoại (10 chữ số)
- **Output**: Phân tích chi tiết từng cặp số, ý nghĩa phong thủy, mức độ phù hợp
- **Yêu cầu kỹ thuật**:
  - Phân tích từng cặp số theo nguyên lý Bát Cực Linh Số
  - Xác định hung/cát tinh và mức độ ảnh hưởng
  - Tính tổng điểm phong thủy của số điện thoại
  - Đưa ra đánh giá tổng thể và khuyến nghị

#### 3.1.2 Đề xuất số điện thoại
- **Mô tả**: Đề xuất số điện thoại phù hợp với mục đích sử dụng
- **Input**: Mục đích sử dụng, các số yêu thích (không bắt buộc)
- **Output**: Danh sách số điện thoại đề xuất kèm phân tích
- **Yêu cầu kỹ thuật**:
  - Tạo thuật toán sinh số điện thoại theo mục đích
  - Đánh giá và xếp hạng các số được sinh ra
  - Lọc và đề xuất top 5-10 số phù hợp nhất

#### 3.1.3 Phân tích CCCD
- **Mô tả**: Phân tích 6 số cuối của CCCD theo quy tắc phong thủy
- **Input**: 6 số cuối của CCCD
- **Output**: Phân tích chi tiết ý nghĩa phong thủy
- **Yêu cầu kỹ thuật**:
  - Chuẩn hóa dãy số (xử lý số 0 theo quy tắc)
  - Tách số thành từng cặp và phân tích
  - Đánh giá tổng thể dựa trên Bát Cục Linh Số
  - Xác định các hung tinh và cát tinh
  - Phân tích tác động của từng cặp số
  - Phân tích tổ hợp các sao liền kề

#### 3.1.4 Phân tích và đề xuất số tài khoản ngân hàng
- **Mô tả**: Phân tích và đề xuất các cặp số cuối cho tài khoản ngân hàng
- **Input**: 
  - Số tài khoản (cho phân tích)
  - Mục đích sử dụng tài khoản, các số ưa thích (cho đề xuất)
- **Output**: 
  - Phân tích: Kết quả phân tích chi tiết các cặp số và ý nghĩa
  - Đề xuất: Danh sách các số tài khoản phù hợp với mục đích
- **Yêu cầu kỹ thuật**:
  - Phân tích 4 số cuối của tài khoản theo từng cặp số
  - Xác định các cặp số tốt cho từng mục đích sử dụng
  - Đánh giá tổng thể dựa trên tổng năng lượng
  - Đề xuất các cặp số phù hợp khi người dùng muốn chọn số
  - Hỗ trợ các mục đích: kinh doanh, cá nhân, đầu tư, tiết kiệm, sức khỏe

#### 3.1.5 Tạo và đánh giá mật khẩu
- **Mô tả**: Đánh giá mật khẩu hiện có theo phong thủy số học
- **Input**: Mật khẩu hiện tại
- **Output**: Kết quả đánh giá và gợi ý cải thiện
- **Yêu cầu kỹ thuật**:
  - Phân tích các cặp chữ số trong mật khẩu
  - Đánh giá tính an toàn của mật khẩu
  - Xác định các cặp số hung tinh cần tránh
  - Đưa ra gợi ý cải thiện mật khẩu về mặt phong thủy
  - Đảm bảo bảo mật mật khẩu trong quá trình xử lý

### 3.2 Payment Agent

#### 3.2.1 Kiểm tra quota
- **Mô tả**: Kiểm tra số câu hỏi còn lại của người dùng
- **Input**: User ID
- **Output**: Số câu hỏi còn lại, trạng thái gói dịch vụ
- **Yêu cầu kỹ thuật**:
  - Truy vấn cơ sở dữ liệu để lấy thông tin quota
  - Kiểm tra trạng thái gói dịch vụ hiện tại

#### 3.2.2 Xử lý thanh toán
- **Mô tả**: Xử lý giao dịch thanh toán cho các gói dịch vụ
- **Input**: User ID, gói dịch vụ, thông tin thanh toán
- **Output**: Kết quả giao dịch, số câu hỏi được cộng thêm
- **Yêu cầu kỹ thuật**:
  - Tích hợp với cổng thanh toán (VNPay, MoMo)
  - Xử lý webhook nhận kết quả thanh toán
  - Cập nhật quota người dùng sau khi thanh toán thành công

#### 3.2.3 Quản lý lịch sử thanh toán
- **Mô tả**: Lưu trữ và hiển thị lịch sử thanh toán của người dùng
- **Input**: User ID, khoảng thời gian (không bắt buộc)
- **Output**: Danh sách giao dịch thanh toán
- **Yêu cầu kỹ thuật**:
  - Lưu trữ thông tin giao dịch với đầy đủ metadata
  - Hỗ trợ lọc và sắp xếp lịch sử giao dịch

### 3.3 User Agent

#### 3.3.1 Xác thực người dùng
- **Mô tả**: Xử lý đăng ký, đăng nhập và quản lý phiên làm việc
- **Input**: Thông tin đăng nhập/đăng ký
- **Output**: Token xác thực, thông tin người dùng
- **Yêu cầu kỹ thuật**:
  - Triển khai JWT cho xác thực
  - Mã hóa mật khẩu an toàn
  - Quản lý phiên làm việc và token

#### 3.3.2 Quản lý hồ sơ người dùng
- **Mô tả**: Quản lý thông tin cá nhân của người dùng
- **Input**: User ID, thông tin cập nhật
- **Output**: Thông tin người dùng sau khi cập nhật
- **Yêu cầu kỹ thuật**:
  - Lưu trữ thông tin người dùng an toàn
  - Hỗ trợ các thao tác CRUD cơ bản

#### 3.3.3 Quản lý lịch sử người dùng
- **Mô tả**: Lưu trữ và hiển thị lịch sử sử dụng dịch vụ
- **Input**: User ID, loại dịch vụ (không bắt buộc)
- **Output**: Danh sách lịch sử sử dụng dịch vụ
- **Yêu cầu kỹ thuật**:
  - Lưu trữ lịch sử chi tiết theo từng loại dịch vụ
  - Hỗ trợ lọc và phân trang kết quả

### 3.4 Chatbot Agent

#### 3.4.1 Xử lý câu hỏi tự nhiên
- **Mô tả**: Xử lý câu hỏi từ người dùng bằng ngôn ngữ tự nhiên
- **Input**: Câu hỏi của người dùng
- **Output**: Câu trả lời, hướng dẫn, hoặc kết quả phân tích
- **Yêu cầu kỹ thuật**:
  - Tích hợp với Google Gemini API
  - Xử lý ngữ cảnh hội thoại
  - Trích xuất thông tin từ câu hỏi để chuyển giao cho các agent khác

## 4. Yêu cầu kỹ thuật

### 4.1 Yêu cầu hệ thống
- **Backend**:
  - Node.js cho API và các dịch vụ chính
  - Python cho các agent AI và xử lý dữ liệu
  - MongoDB cho lưu trữ dữ liệu
  - Redis cho cache và quản lý phiên
- **Kiến trúc**:
  - Microservices với các agent độc lập
  - RESTful API cho giao tiếp giữa frontend và backend
  - Pub/Sub pattern cho giao tiếp giữa các agent
  - A2A Protocol cho tương tác giữa các agent

### 4.2 Yêu cầu bảo mật
- Mã hóa dữ liệu nhạy cảm
- Xác thực JWT cho API
- Rate limiting và CSRF protection
- Sanitization đầu vào
- Logging và monitoring hệ thống

### 4.3 Khả năng mở rộng
- Microservices cho phép mở rộng độc lập từng thành phần
- Hỗ trợ thêm ngôn ngữ và mô hình AI mới
- Kiến trúc cho phép thêm specialized agent mới dễ dàng
- Hệ thống API mở cho phép tích hợp với bên thứ ba

## 5. Kế hoạch phát triển

### 5.1 MVP (Minimum Viable Product)
- Root Agent và BatCucLinhSo Agent
- Chức năng phân tích số điện thoại
- Chức năng phân tích CCCD
- Xác thực người dùng cơ bản
- Giao diện người dùng đơn giản

### 5.2 Phiên bản v1.0
- Thêm Payment Agent
- Tích hợp cổng thanh toán
- Cải thiện giao diện người dùng
- Thêm tính năng đề xuất số điện thoại và tài khoản ngân hàng
- Chatbot Agent cơ bản

### 5.3 Phiên bản v2.0
- Cải thiện trải nghiệm Chatbot Agent
- Thêm User Agent đầy đủ
- Tích hợp Social Login
- Trang quản trị cho admin
- Phân tích dữ liệu và dashboard
- API mở cho đối tác

## 6. Các chỉ số đo lường thành công

- Số lượng người dùng đăng ký
- Tỷ lệ chuyển đổi (người dùng miễn phí → trả phí)
- Độ chính xác của các phân tích phong thủy
- Tỷ lệ hoàn thành của các câu hỏi chatbot
- Thời gian phản hồi của hệ thống
- Tỷ lệ người dùng quay lại 