# Cấu trúc thư mục dự án Phong Thủy Số

Dự án Phong Thủy Số được tổ chức thành hai phần chính:
1. **Backend Node.js**: Đảm nhiệm vai trò API Gateway, kết nối database, và xử lý business logic
2. **Backend Python**: Sử dụng Google ADK để triển khai kiến trúc đa tác tử (multi-agent)

```
phong_thuy_so/
│
├── node_backend/                   # Backend Node.js
│   ├── server.js                   # Entry point của Node.js server
│   ├── config/                     # Cấu hình ứng dụng
│   │   ├── database.js             # Cấu hình database
│   │   ├── auth.js                 # Cấu hình authentication
│   │   └── environments/           # Cấu hình môi trường (dev, prod)
│   │
│   ├── api/                        # API Gateway
│   │   ├── middleware/             # Middleware cho API
│   │   └── v1/                     # API routes phiên bản v1
│   │       └── routes/             # Định nghĩa các routes
│   │           ├── auth.routes.js
│   │           ├── analysis.routes.js
│   │           └── payment.routes.js
│   │
│   ├── api/v2/                     # API routes phiên bản v2 (ADK)
│   │   ├── routes/
│   │   │   ├── chat.routes.js      # Endpoint cho chat với agents
│   │   │   ├── upload.routes.js    # Endpoint cho upload files
│   │   │   ├── user.routes.js      # Endpoint quản lý user
│   │   │   ├── payment.routes.js   # Endpoint thanh toán
│   │   │   └── apikeys.routes.js   # Endpoint quản lý API keys
│   │   │
│   │   └── middleware/
│   │       ├── auth.middleware.js  # Xác thực
│   │       ├── quota.middleware.js # Quản lý quota
│   │       └── streaming.middleware.js # Hỗ trợ SSE
│   │
│   ├── controllers/                # Xử lý logic request/response
│   │   ├── auth.controller.js
│   │   ├── analysis.controller.js
│   │   └── payment.controller.js
│   │
│   ├── models/                     # Mô hình dữ liệu
│   │   ├── user.model.js
│   │   ├── analysis.model.js
│   │   └── payment.model.js
│   │
│   ├── services/                   # Business logic
│   │   ├── database.js             # Kết nối database
│   │   ├── analysisService.js      # Logic phân tích
│   │   ├── geminiService.js        # Tích hợp với Google Gemini
│   │   ├── a2a-protocol.js         # Định nghĩa A2A Protocol
│   │   └── agents/                 # Tích hợp với agents
│   │       ├── rootAgent.js        # Kết nối với Root Agent
│   │       ├── batCucLinhSoAgent.js # Kết nối với BatCucLinhSo Agent
│   │       ├── paymentAgent.js     # Kết nối với Payment Agent
│   │       └── userAgent.js        # Kết nối với User Agent
│   │
│   └── utils/                      # Tiện ích
│       ├── logger.js               # Logging
│       ├── validators.js           # Xác thực input
│       └── formatters.js           # Format dữ liệu
│
├── python_adk/                     # Backend Python với Google ADK
│   ├── main.py                     # Entry point cho FastAPI server
│   ├── config/                     # Cấu hình
│   │   ├── config.py               # Cấu hình chung
│   │   └── logging.py              # Cấu hình logging
│   │
│   ├── endpoints/                  # FastAPI endpoints
│   │   ├── chat.py                 # Endpoint xử lý chat
│   │   ├── tasks.py                # Endpoint quản lý tasks
│   │   └── webhooks.py             # Webhooks cho events
│   │
│   ├── agents/                     # Định nghĩa agents
│   │   ├── root_agent/             # Root Agent
│   │   │   ├── agent.py            # Định nghĩa Root Agent
│   │   │   ├── prompts.py          # Prompts cho Root Agent
│   │   │   └── tools/              # Tools cho Root Agent
│   │   │       ├── intent_classifier.py
│   │   │       ├── conversation_manager.py
│   │   │       ├── context_tracker.py
│   │   │       └── agent_router.py
│   │   │
│   │   ├── batcuclinh_so_agent/    # BatCucLinhSo Agent
│   │   │   ├── agent.py            # Định nghĩa BatCucLinhSo Agent
│   │   │   ├── prompts.py          # Prompts cho BatCucLinhSo Agent
│   │   │   └── tools/              # Tools cho BatCucLinhSo Agent
│   │   │       ├── phone_analyzer.py
│   │   │       ├── cccd_analyzer.py
│   │   │       ├── bank_account_analyzer.py
│   │   │       ├── password_analyzer.py
│   │   │       └── recommendation_engine.py
│   │   │
│   │   ├── payment_agent/          # Payment Agent
│   │   │   ├── agent.py            # Định nghĩa Payment Agent
│   │   │   ├── prompts.py          # Prompts cho Payment Agent
│   │   │   └── tools/              # Tools cho Payment Agent
│   │   │       ├── payment_processor.py
│   │   │       ├── subscription_manager.py
│   │   │       ├── quota_checker.py
│   │   │       └── notification_sender.py
│   │   │
│   │   └── user_agent/             # User Agent
│   │       ├── agent.py            # Định nghĩa User Agent
│   │       ├── prompts.py          # Prompts cho User Agent
│   │       └── tools/              # Tools cho User Agent
│   │           ├── account_manager.py
│   │           ├── apikey_generator.py
│   │           ├── history_tracker.py
│   │           └── preference_manager.py
│   │
│   ├── a2a/                        # Agent-to-Agent Protocol
│   │   ├── protocol.py             # Định nghĩa A2A Protocol
│   │   ├── task.py                 # Quản lý tasks
│   │   ├── message.py              # Quản lý messages
│   │   └── artifact.py             # Quản lý artifacts
│   │
│   ├── mcp/                        # Model Context Protocol
│   │   ├── server.py               # MCP Server
│   │   ├── templates.py            # Quản lý templates
│   │   ├── parameters.py           # Quản lý parameters
│   │   └── resources.py            # Quản lý resources
│   │
│   ├── session/                    # Session Management
│   │   ├── base.py                 # Base SessionService
│   │   ├── memory_session.py       # InMemorySessionService
│   │   └── mongo_session.py        # MongoDBSessionService
│   │
│   ├── callbacks/                  # Callbacks cho events
│   │   ├── task_callbacks.py       # Callbacks cho tasks
│   │   ├── message_callbacks.py    # Callbacks cho messages
│   │   └── error_callbacks.py      # Callbacks cho errors
│   │
│   └── utils/                      # Tiện ích
│       ├── logging_utils.py        # Logging utilities
│       ├── validation.py           # Xác thực dữ liệu
│       └── metrics.py              # Metrics tracking
│
├── frontend/                       # Frontend (Vue.js)
│   ├── public/                     # Static assets
│   └── src/                        # Source code
│       ├── assets/                 # Assets
│       ├── components/             # Vue components
│   │   └── views/                  # Vue views
│   │       ├── router/                 # Vue Router
│   │       ├── store/                  # Vuex/Pinia store
│   │       ├── services/               # API services
│   │       ├── utils/                  # Tiện ích
│   │       ├── App.vue                 # Root component
│   │       └── main.js                 # Entry point
│   │
│   ├── kubernetes/                     # Kubernetes configs
│   │   ├── node-backend/               # Node.js service configs
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   │
│   │   ├── python-adk/                 # Python ADK service configs
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   │
│   │   ├── mongodb/                    # MongoDB configs
│   │   │   ├── statefulset.yaml
│   │   │   └── service.yaml
│   │   │
│   │   └── ingress.yaml                # Ingress config
│   │
│   ├── docker/                         # Docker configs
│   │   ├── node-backend/               # Node.js Docker
│   │   │   └── Dockerfile
│   │   │
│   │   ├── python-adk/                 # Python ADK Docker
│   │   │   └── Dockerfile
│   │   │
│   │   └── docker-compose.yml          # Docker Compose config
│   │
│   ├── PRD/                            # Documentation
│   │   ├── structure.md                # Cấu trúc thư mục (file này)
│   │   ├── tasklog.md                  # Nhật ký công việc
│   │   ├── implementation_plan.md      # Kế hoạch triển khai
│   │   ├── multiAgentPrd.md            # PRD cho kiến trúc đa tác tử
│   │   └── api_docs.md                 # Tài liệu API
│   │
│   ├── tests/                          # Tests
│   │   ├── node_backend/               # Tests cho Node.js backend
│   │   │   ├── unit/                   # Unit tests
│   │   │   └── integration/            # Integration tests
│   │   │
│   │   └── python_adk/                 # Tests cho Python ADK
│   │       ├── unit/                   # Unit tests
│   │       └── integration/            # Integration tests
│   │
│   ├── .gitignore                      # Git ignore file
│   │
│   └── README.md                       # Readme
│       └── package.json                # Node.js package
└── requirements.txt                # Python requirements
```

## Kiến trúc Agents sử dụng Google ADK

Google Agent Development Kit (ADK) được tích hợp vào dự án để xây dựng hệ thống đa tác tử thông minh. Kiến trúc này gồm các thành phần chính:

### 1. Agents

- **Root Agent**: Điều phối viên chính, nhận input từ người dùng, phân loại và chuyển hướng đến các agent chuyên biệt
- **BatCucLinhSo Agent**: Chuyên phân tích số điện thoại, CCCD, STK ngân hàng theo phương pháp Bát Cục Linh Số
- **Payment Agent**: Xử lý các giao dịch thanh toán và quản lý quota người dùng
- **User Agent**: Quản lý thông tin người dùng và API keys

### 2. Agent-to-Agent (A2A) Protocol

A2A Protocol cho phép các agent giao tiếp với nhau một cách chuẩn hóa thông qua:

- **Tasks**: Đại diện cho các nhiệm vụ cần hoàn thành
- **Messages**: Giao tiếp giữa các agent
- **Artifacts**: Dữ liệu chia sẻ giữa các agent

### 3. Model Context Protocol (MCP)

MCP quản lý tài nguyên và cấu hình cho các agent:

- **Templates**: Các mẫu prompt cho agents
- **Parameters**: Cấu hình cho các mô hình LLM
- **Resources**: Tài nguyên dùng chung (dữ liệu phân tích, hướng dẫn, v.v.)

### 4. API Gateway

API Gateway đóng vai trò trung gian giữa frontend và hệ thống agents, cung cấp:

- **Authentication & Authorization**: Xác thực và phân quyền
- **Quota Management**: Quản lý hạn mức sử dụng
- **Request Routing**: Chuyển hướng requests đến các endpoints thích hợp
- **Response Streaming**: Hỗ trợ Server-Sent Events (SSE)
- **Error Handling**: Xử lý lỗi thống nhất

### 5. Session Management

Hệ thống quản lý session để duy trì context giữa các tương tác:

- **InMemorySessionService**: Dùng cho môi trường phát triển
- **MongoDBSessionService**: Dùng cho môi trường production

## Chiến lược triển khai

Dự án hỗ trợ nhiều phương thức triển khai:

1. **Docker & Docker Compose**: Cho môi trường phát triển
   ```
   docker-compose up --build
   ```

2. **Kubernetes**: Cho môi trường production
   ```
   kubectl apply -f kubernetes/
   ```

3. **Google Cloud Run**: Cho triển khai serverless
   ```
   gcloud run deploy node-backend --source ./node_backend
   gcloud run deploy python-adk --source ./python_adk
   ```

4. **Local Development**: Cho phát triển cục bộ
   ```
   # Terminal 1: Node.js backend
   cd node_backend
   npm install
   npm run dev
   
   # Terminal 2: Python ADK
   cd python_adk
   pip install -r requirements.txt
   uvicorn main:app --reload
   ``` 