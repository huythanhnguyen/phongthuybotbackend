# Cấu Trúc Thư Mục - Phong Thủy Số (Kiến trúc Agent)

Dưới đây là cấu trúc thư mục được đề xuất cho dự án Phong Thủy Số dựa trên kiến trúc agent:

```
/phongthuybotbackend/
│
├── /agents/                          # Thư mục chứa tất cả các agent
│   ├── /root-agent/                  # Root Agent - điều phối chính
│   │   ├── index.js                  # Entry point cho Root Agent  
│   │   ├── agent-card.json           # Agent Card theo A2A Protocol
│   │   ├── router.js                 # Bộ định tuyến yêu cầu
│   │   └── /services/                # Các dịch vụ của Root Agent
│   │   
│   ├── /bat-cuc-linh-so/             # Agent phân tích phong thủy số học
│   │   ├── index.js                  # Entry point cho BatCucLinhSo Agent
│   │   ├── agent-card.json           # Agent Card theo A2A Protocol
│   │   └── /tools/                   # Các công cụ của agent
│   │       ├── phone-analysis.js     # Công cụ phân tích số điện thoại
│   │       ├── phone-recommend.js    # Công cụ đề xuất số điện thoại
│   │       ├── cccd-analysis.js      # Công cụ phân tích CCCD
│   │       ├── bank-account.js       # Công cụ phong thủy tài khoản ngân hàng
│   │       └── password.js           # Công cụ phong thủy mật khẩu
│   │   
│   ├── /payment/                     # Agent quản lý thanh toán
│   │   ├── index.js                  # Entry point cho Payment Agent
│   │   ├── agent-card.json           # Agent Card theo A2A Protocol
│   │   └── /tools/                   # Các công cụ của agent
│   │       ├── quota-check.js        # Công cụ kiểm tra quota
│   │       ├── payment-processing.js # Công cụ xử lý thanh toán
│   │       └── payment-history.js    # Công cụ quản lý lịch sử thanh toán
│   │   
│   ├── /user/                        # Agent quản lý người dùng
│   │   ├── index.js                  # Entry point cho User Agent
│   │   ├── agent-card.json           # Agent Card theo A2A Protocol
│   │   └── /tools/                   # Các công cụ của agent
│   │       ├── authentication.js     # Công cụ xác thực
│   │       ├── profile-management.js # Công cụ quản lý hồ sơ
│   │       └── history.js            # Công cụ quản lý lịch sử
│   │   
│   └── /chatbot/                     # Agent trò chuyện
│       ├── index.js                  # Entry point cho Chatbot Agent
│       ├── agent-card.json           # Agent Card theo A2A Protocol
│       └── /tools/                   # Các công cụ của agent
│           ├── llm.js                # Công cụ tương tác với LLM
│           ├── conversation-memory.js # Công cụ quản lý bộ nhớ hội thoại
│           └── agent-delegation.js   # Công cụ chuyển giao nhiệm vụ
│
├── /models/                          # Định nghĩa schema MongoDB
│   ├── User.js                       # Model người dùng
│   ├── Analysis.js                   # Model phân tích
│   ├── Payment.js                    # Model thanh toán
│   ├── Conversation.js               # Model hội thoại
│   └── AgentState.js                 # Model lưu trữ trạng thái agent
│
├── /api/                             # API Endpoints
│   ├── /v1/                          # API v1 (kiến trúc cũ)
│   │   ├── routes.js                 # Định nghĩa routes
│   │   └── /controllers/             # Controllers
│   │
│   └── /v2/                          # API v2 (kiến trúc agent)
│       ├── gateway.js                # API Gateway
│       ├── routes.js                 # Định nghĩa routes
│       └── /controllers/             # Controllers
│
├── /services/                        # Các dịch vụ dùng chung
│   ├── database.js                   # Kết nối cơ sở dữ liệu
│   ├── cache.js                      # Dịch vụ cache (Redis)
│   ├── logger.js                     # Dịch vụ ghi log
│   ├── gemini.js                     # Kết nối Google Gemini API
│   └── a2a-protocol.js               # Triển khai A2A Protocol
│
├── /tools/                           # Công cụ dùng chung giữa các agent
│   ├── bat-cuc-linh-so-helpers.js    # Helpers cho Bát Cực Linh Số
│   ├── agent-transfer.js             # Tool chuyển giao giữa các agent
│   └── jwt-auth.js                   # Tool xác thực JWT
│
├── /utils/                           # Các tiện ích
│   ├── constants.js                  # Hằng số
│   ├── validators.js                 # Kiểm tra đầu vào
│   ├── helpers.js                    # Hàm hỗ trợ
│   └── errorHandlers.js              # Xử lý lỗi
│
├── /config/                          # Cấu hình
│   ├── index.js                      # Cấu hình chính
│   ├── agent-manager.js              # Quản lý agent
│   └── env.js                        # Biến môi trường
│
├── /python/                          # Mã Python cho các agent AI
│   ├── /bat_cuc_linh_so/             # Phong thủy số học Python
│   │   ├── analysis.py               # Logic phân tích số
│   │   └── generator.py              # Sinh số theo phong thủy
│   │
│   └── /chatbot/                     # Chatbot AI Python
│       ├── llm_processor.py          # Xử lý LLM
│       └── conversation.py           # Quản lý hội thoại
│
├── /docs/                            # Tài liệu
│   ├── api.md                        # Tài liệu API
│   ├── agent-architecture.md         # Tài liệu kiến trúc agent
│   └── deployment.md                 # Hướng dẫn triển khai
│
├── /tests/                           # Kiểm thử
│   ├── /unit/                        # Unit tests
│   ├── /integration/                 # Integration tests
│   └── /e2e/                         # End-to-end tests
│
├── app.js                            # Entry point ứng dụng
├── server.js                         # Khởi động server
├── package.json                      # Cấu hình npm
├── package-lock.json                 # Lock file npm
└── .env                              # Biến môi trường
```

## Lưu ý về cấu trúc

### 1. Tổ chức theo Agent
- Mỗi agent được đặt trong thư mục riêng với đầy đủ tools cần thiết
- Mỗi agent đều có agent-card.json định nghĩa khả năng và giao diện tương tác
- Root Agent đóng vai trò trung tâm điều phối

### 2. Phân chia Node.js và Python
- Sử dụng Node.js cho backend API và các dịch vụ chính
- Sử dụng Python cho các thành phần AI và xử lý dữ liệu phức tạp
- Giao tiếp giữa Node.js và Python thông qua API hoặc message queue

### 3. Microservices
- Mỗi agent có thể được triển khai như một microservice riêng biệt
- Sử dụng API gateway để điều hướng yêu cầu đến agent phù hợp
- Hỗ trợ khả năng mở rộng và cân bằng tải

### 4. Tích hợp A2A Protocol
- Triển khai giao thức A2A cho giao tiếp giữa các agent
- Sử dụng Task, Message và Artifact cho trao đổi dữ liệu
- Hỗ trợ streaming và thông báo đẩy

### 5. Hỗ trợ phiên bản cũ và mới
- Duy trì cấu trúc API v1 cho tương thích ngược
- Phát triển API v2 cho kiến trúc agent mới
- Hỗ trợ di chuyển dần từ v1 sang v2 