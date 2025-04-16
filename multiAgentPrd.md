Tài liệu Yêu cầu Sản phẩm (PRD)
Phong Thủy Số - Kiến trúc Multi-Agent
1. Tổng quan sản phẩm
1.1 Giới thiệu
Phong Thủy Số là một nền tảng cung cấp dịch vụ phong thủy số học, giúp người dùng phân tích và tối ưu hóa các yếu tố số học trong cuộc sống hàng ngày. Phiên bản mới sẽ được xây dựng dựa trên kiến trúc multi-agent, cho phép mở rộng các expert agent và khả năng mua credit của người dùng để truy cập vào các dịch vụ khác nhau.
1.2 Mục tiêu

Xây dựng nền tảng phong thủy số học tiên tiến dựa trên kiến trúc multi-agent với ADK
Cung cấp các dịch vụ phân tích và tư vấn phong thủy số học chính xác và hiệu quả
Phát triển hệ thống quản lý credit và API key cho người dùng
Tạo ra trải nghiệm người dùng liền mạch và trực quan
Xây dựng nền tảng có khả năng mở rộng và tích hợp các expert agent mới

1.3 Đối tượng người dùng

Người quan tâm đến phong thủy và muốn áp dụng vào cuộc sống số
Doanh nghiệp muốn tối ưu hóa các yếu tố số học trong thương hiệu
Nhà phát triển muốn tích hợp dịch vụ phong thủy số vào ứng dụng của họ qua API
Chuyên gia phong thủy cung cấp dịch vụ tư vấn thông qua nền tảng

2. Kiến trúc hệ thống
2.1 Tổng quan kiến trúc
Hệ thống được thiết kế dựa trên kiến trúc multi-agent, với một Root Agent điều phối và nhiều Expert Agent (như Bát Cực Linh Số, Tử Vi, Thần Số Học) xử lý các nhiệm vụ chuyên biệt. Kiến trúc này sẽ tuân theo các nguyên tắc của ADK và tích hợp A2A Protocol để giao tiếp giữa các agent.
Hệ thống sẽ được phân tách thành hai thành phần backend chính:

Node.js API Gateway: Xử lý tương tác với frontend, quản lý users, thanh toán, và định tuyến yêu cầu đến Agent Service
Python Agents Service: Triển khai ADK Python để xử lý logic phong thủy số học và tương tác giữa các agent

2.2 Cấu trúc Agent
2.2.1 Root Agent

Mục đích: Điều phối các expert agent và cung cấp giao diện tương tác thống nhất
Chức năng:

Tiếp nhận và phân tích yêu cầu từ người dùng
Chuyển giao yêu cầu đến expert agent phù hợp
Tổng hợp và trả về kết quả cho người dùng
Quản lý phiên làm việc và trạng thái hội thoại
Xác thực người dùng và quản lý API key



2.2.2 BatCucLinhSo Expert Agent

Mục đích: Phân tích và tư vấn phong thủy số học theo Bát Cực Linh Số
Chức năng:

Phân tích số điện thoại theo nguyên lý Bát Cực Linh Số
Đề xuất số điện thoại phù hợp với mục đích sử dụng
Phân tích 6 số cuối của CCCD
Phân tích và đề xuất số tài khoản ngân hàng
Tạo và đánh giá mật khẩu theo phong thủy



2.2.3 Phong Thủy Expert Agent (Dự kiến phát triển)

Mục đích: Phân tích và tư vấn phong thủy tổng quát
Chức năng:

Phân tích mệnh ngũ hành và tương sinh tương khắc
Đánh giá và tư vấn về hướng nhà, vị trí làm việc
Gợi ý màu sắc và vật phẩm phong thủy
Tư vấn cải thiện phong thủy cho các không gian



2.2.4 Tử Vi Expert Agent (Dự kiến phát triển)

Mục đích: Phân tích và tư vấn tử vi
Chức năng:

Lập và giải lá số tử vi
Dự báo vận hạn theo chu kỳ
Tư vấn định hướng sự nghiệp, tình duyên, tài lộc



2.2.5 Thần Số Học Expert Agent (Dự kiến phát triển)

Mục đích: Phân tích và tư vấn thần số học
Chức năng:

Tính toán các con số chủ đạo dựa trên ngày sinh
Phân tích ý nghĩa các con số
Đề xuất hành động phù hợp với các con số



2.2.6 Credit Management Agent

Mục đích: Quản lý credit của người dùng
Chức năng:

Kiểm tra số credit hiện có của người dùng
Xử lý giao dịch nạp credit
Trừ credit khi người dùng sử dụng dịch vụ
Lưu trữ và hiển thị lịch sử giao dịch



2.2.7 API Management Agent

Mục đích: Quản lý API key và quyền truy cập
Chức năng:

Tạo và quản lý API key cho người dùng
Xác thực và phân quyền truy cập API
Giám sát sử dụng API và đảm bảo tuân thủ hạn mức
Thu thập số liệu sử dụng API cho báo cáo và lập hóa đơn



2.3 Luồng dữ liệu

Người dùng hoặc ứng dụng client gửi yêu cầu đến Node.js API Gateway
API Gateway xác thực người dùng và kiểm tra credit/API key
API Gateway chuyển tiếp yêu cầu đến Python Agents Service
Root Agent phân tích yêu cầu và xác định Expert Agent phù hợp
Root Agent chuyển giao yêu cầu đến Expert Agent
Expert Agent xử lý yêu cầu và gửi kết quả lại Root Agent
Root Agent có thể tổng hợp kết quả từ nhiều Expert Agent nếu cần
Python Agents Service trả kết quả về API Gateway
API Gateway trừ credit của người dùng dựa trên dịch vụ đã sử dụng
API Gateway trả kết quả cho người dùng

2.4 Tương tác giữa các Agent và Services

Giữa Node.js API Gateway và Python Agents Service: REST API hoặc gRPC
Giữa các agent trong Python Agents Service: ADK và A2A Protocol
Truy cập database: Cả hai service đều truy cập vào cùng MongoDB database
Quản lý session và cache: Redis được sử dụng cho cả hai service

3. Hệ thống quản lý credit và API
3.1 Mô hình credit

Credit: Đơn vị thanh toán nội bộ của hệ thống
Gói credit:

Gói Cơ bản: 100 credit (100,000 VND)
Gói Tiêu chuẩn: 300 credit (270,000 VND - tiết kiệm 10%)
Gói Premium: 1000 credit (800,000 VND - tiết kiệm 20%)
Gói Doanh nghiệp: Tùy chỉnh theo nhu cầu


Chi phí sử dụng:

Phân tích số điện thoại: 5 credit
Đề xuất số điện thoại: 10 credit
Phân tích CCCD: 5 credit
Phân tích tài khoản ngân hàng: 5 credit
Tạo mật khẩu: 3 credit
Phân tích phong thủy tổng quát: 15 credit
Lập và giải lá số tử vi: 20 credit
Phân tích thần số học: 10 credit



3.2 API Management

Cấp độ API:

Free: 50 lượt gọi/ngày, không hỗ trợ các dịch vụ cao cấp
Basic: 1000 lượt gọi/ngày, hỗ trợ các dịch vụ cơ bản
Pro: 10,000 lượt gọi/ngày, hỗ trợ tất cả dịch vụ
Enterprise: Không giới hạn, SLA riêng


API Key Management:

Tạo và quản lý nhiều API key với các quyền khác nhau
Theo dõi sử dụng theo từng API key
Hạn chế truy cập theo IP hoặc domain
Thiết lập hạn mức sử dụng tùy chỉnh



3.3 Thanh toán và lập hóa đơn

Phương thức thanh toán:

Thanh toán trực tuyến (Visa, MasterCard, PayOS)
Ví điện tử (MoMo, ZaloPay, VNPay)
Chuyển khoản ngân hàng


Hệ thống lập hóa đơn:

Xuất hóa đơn tự động sau khi thanh toán
Theo dõi lịch sử giao dịch
Báo cáo sử dụng hàng tháng
Tự động gia hạn cho các gói đăng ký



4. Tech Stack
4.1 Frontend

Framework: Vue.js 3 (Composition API)
State Management: Pinia
UI Components: Vuetify 3 hoặc Tailwind CSS + HeadlessUI
Routing: Vue Router
API Client: Axios
Testing: Vitest, Cypress
Build Tool: Vite

4.2 Backend (Node.js API Gateway)

Runtime: Node.js (v18+)
Framework: Express.js với TypeScript
Database: MongoDB cho dữ liệu người dùng và giao dịch
Cache & Session: Redis
Authentication: JWT, OAuth2
API Documentation: Swagger/OpenAPI
Payment Integration: PayOS SDK
Testing: Jest, SuperTest

4.3 Agent Service (Python)

Runtime: Python 3.9+
Agent Framework: Google ADK (Agent Development Kit)
API Framework: FastAPI
Dependency Management: Poetry hoặc Pip
Database Clients: PyMongo, Redis-py
Communication: HTTP/REST hoặc gRPC
Testing: Pytest
LLM Integration: Google Gemini API

4.4 AI/ML

LLM: Google Gemini API (primary), OpenAI API (backup)
Vector Database: Pinecone hoặc Milvus cho RAG
Embedding Models: Sentence Transformers

4.5 DevOps & Infrastructure

CI/CD: GitHub Actions/GitLab CI
Containerization: Docker, Kubernetes
Cloud Provider: Render.com (ưu tiên), GCP hoặc Firebase
Monitoring: Prometheus, Grafana
Logging: ELK Stack hoặc GCP Operations Suite
Serverless: Cloud Functions/Cloud Run cho một số microservices

5. Cấu trúc thư mục
Dự án sẽ được tổ chức theo mô hình monorepo nhưng tách biệt rõ các thành phần:
/phong-thuy-so/               # Root repository
├── frontend/                 # Vue.js frontend
├── backend/                  # Node.js API Gateway
├── agents/                   # Python ADK Agents
│   ├── phong_thuy_so/        
│   │   ├── root_agent/       # Root Agent
│   │   ├── expert_agents/    # Các Expert Agent
│   │   │   ├── bat_cuc_linh_so/
│   │   │   └── ... 
│   │   ├── api/              # FastAPI layer
│   │   └── main.py           # Entry point
├── deploy/                   # Deployment configs
└── docs/                     # Documentation
6. Yêu cầu chức năng
6.1 Quản lý người dùng

Đăng ký, đăng nhập và quản lý thông tin cá nhân
Xác thực hai yếu tố
Quản lý phiên làm việc
Phân quyền người dùng (thông thường, premium, admin)
Đồng bộ hóa dữ liệu giữa các thiết bị

6.2 Quản lý credit

Mua và nạp credit
Xem số dư credit
Theo dõi lịch sử sử dụng credit
Thiết lập ngưỡng cảnh báo khi credit thấp
Tự động gia hạn credit theo đăng ký

6.3 Quản lý API key

Tạo mới API key
Quản lý quyền truy cập của từng API key
Theo dõi sử dụng API theo key
Thiết lập hạn mức sử dụng
Vô hiệu hóa hoặc xóa API key

6.4 Tương tác Expert Agents

Gửi yêu cầu đến các expert agent
Xem kết quả phân tích
Lưu và quản lý lịch sử phân tích
Tải xuống báo cáo phân tích (PDF, DOC)
Chia sẻ kết quả phân tích qua email hoặc mạng xã hội

6.5 Quản lý Dashboard

Dashboard tổng quan cho người dùng
Báo cáo sử dụng dịch vụ
Thống kê chi tiêu
Đề xuất dịch vụ phù hợp
Thông báo và cập nhật

6.6 Tích hợp và API

Tài liệu API đầy đủ
Môi trường sandbox để thử nghiệm
Webhooks cho các sự kiện
SDK cho các ngôn ngữ phổ biến (JavaScript, Python, PHP)
Ví dụ tích hợp

7. Yêu cầu phi chức năng
7.1 Hiệu suất

Thời gian phản hồi API < 500ms (không bao gồm xử lý LLM)
Xử lý đồng thời tối thiểu 1000 yêu cầu/phút
Khả năng mở rộng theo chiều ngang
Tối ưu hóa cache cho các truy vấn phổ biến
Thời gian khởi động dịch vụ < 30 giây

7.2 Bảo mật

Mã hóa dữ liệu nhạy cảm tại rest và in transit
Tuân thủ GDPR và CCPA
Xác thực và phân quyền mạnh mẽ
Bảo vệ chống tấn công CSRF, XSS và injection
Quét lỗ hổng bảo mật tự động

7.3 Độ tin cậy

Uptime 99.9%
Cơ chế fallback khi dịch vụ LLM không khả dụng
Hệ thống sao lưu dữ liệu tự động
Giám sát và cảnh báo chủ động
Khôi phục sau thảm họa

7.4 Khả năng mở rộng

Kiến trúc modular cho phép thêm expert agent mới
API versioning để đảm bảo tương thích ngược
Khả năng xử lý tăng đột biến lưu lượng truy cập
Tự động mở rộng theo tải

7.5 Khả năng truy xuất

Nhật ký đầy đủ cho tất cả các giao dịch
Theo dõi đường dẫn xử lý giữa các agent
Metrics chi tiết cho mục đích lập hóa đơn và phân tích
Audit trails cho các hoạt động quản trị

8. Triển khai hạ tầng
8.1 Cấu hình Render.com (Ưu tiên)

Frontend: Static Site
API Gateway: Web Service (Node.js)
Agents Service: Web Service (Python)
Database: MongoDB Atlas (External)
Cache: Redis Service (Render.com)

8.2 Tích hợp PayOS

Xử lý qua Node.js API Gateway
Workflow:

Frontend gửi yêu cầu mua credit
Backend tạo giao dịch trong PayOS
Người dùng được chuyển hướng đến cổng thanh toán
PayOS gửi webhook khi thanh toán hoàn tất
Backend cập nhật credit người dùng



8.3 Môi trường phát triển

Local: Docker Compose cho toàn bộ stack
CI/CD: Tự động triển khai từ GitHub đến Render.com
Testing: Unit tests, integration tests, E2E tests
Monitoring: Render.com metrics, custom logging

9. Kế hoạch phát triển
9.1 Giai đoạn 1: MVP (3 tháng)

Chuyển đổi kiến trúc hiện tại sang mô hình multi-agent với ADK Python
Tích hợp Node.js API Gateway với Python Agents Service
Xây dựng Root Agent và BatCucLinhSo Expert Agent
Xây dựng hệ thống quản lý credit cơ bản với PayOS
Phát triển giao diện người dùng mới
Triển khai hệ thống xác thực và quản lý phiên làm việc

9.2 Giai đoạn 2: Mở rộng dịch vụ (3 tháng)

Phát triển thêm Phong Thủy Expert Agent
Nâng cấp hệ thống quản lý credit và thanh toán
Phát triển API Management và hệ thống API key
Cải thiện giao diện người dùng và trải nghiệm người dùng
Phát triển SDK JavaScript

9.3 Giai đoạn 3: Tối ưu hóa và mở rộng (6 tháng)

Phát triển thêm Tử Vi và Thần Số Học Expert Agent
Xây dựng hệ thống analytics và báo cáo
Tối ưu hóa hiệu suất và khả năng mở rộng
Phát triển các SDK bổ sung (Python, PHP)
Tích hợp với các nền tảng bên thứ ba (CRM, ERP)

9.4 Giai đoạn 4: Enterprise và AI nâng cao (6 tháng)

Phát triển tính năng dành cho doanh nghiệp
Nâng cao khả năng AI với fine-tuning models
Xây dựng marketplace cho các expert agent bên thứ ba
Tối ưu hóa trải nghiệm di động và đa thiết bị
Mở rộng ra thị trường quốc tế

10. Metrics và KPIs
10.1 Metrics kinh doanh

Tổng doanh thu hàng tháng
Số lượng người dùng đăng ký mới
Tỷ lệ chuyển đổi (free → paid)
Giá trị vòng đời khách hàng (CLV)
Chi phí thu hút khách hàng (CAC)

10.2 Metrics sản phẩm

Thời gian sử dụng trung bình
Tỷ lệ giữ chân người dùng
Số lượng phân tích được thực hiện
Phân bố sử dụng giữa các expert agent
Tỷ lệ thành công của các phân tích

10.3 Metrics kỹ thuật

Thời gian phản hồi API
Uptime của dịch vụ
Tỷ lệ lỗi
Thời gian giải quyết sự cố
Mức sử dụng tài nguyên

11. Rủi ro và Giảm thiểu
11.1 Rủi ro kỹ thuật

Hiệu suất LLM không ổn định: Triển khai hàng đợi và cơ chế fallback
Tích hợp ADK Python phức tạp: Lập kế hoạch POC và đào tạo đội ngũ
Giao tiếp giữa Node.js và Python: Xây dựng lớp API ổn định với thử nghiệm kỹ lưỡng
Vấn đề mở rộng: Thiết kế cho khả năng mở rộng từ đầu, sử dụng kiến trúc microservices

11.2 Rủi ro kinh doanh

Khó khăn trong việc định giá credit: Thực hiện A/B testing và điều chỉnh dựa trên phản hồi
Cạnh tranh thị trường: Tập trung vào tính năng độc đáo và chất lượng dịch vụ
Chấp nhận của người dùng: Thu thập phản hồi sớm và thường xuyên từ người dùng

12. Phụ lục
12.1 Tài liệu tham khảo

Google ADK Python Documentation
A2A Protocol Specification
Model Context Protocol (MCP)
Vue.js Documentation
FastAPI Documentation
MongoDB Documentation

12.2 Giải thích thuật ngữ

ADK: Agent Development Kit, bộ công cụ phát triển agent của Google
A2A Protocol: Agent-to-Agent Protocol, giao thức giao tiếp giữa các agent
Expert Agent: Agent chuyên biệt xử lý một lĩnh vực cụ thể
Credit: Đơn vị thanh toán nội bộ của hệ thống
API Key: Khóa xác thực để truy cập API
