# Phong Thủy Số - Backend API

Backend API cho dự án "Phong Thủy Số" sử dụng kiến trúc Agent-based để phân tích số điện thoại, CCCD và các dữ liệu số học khác.

## Cài đặt

### Yêu cầu

- Node.js (v14 trở lên)
- MongoDB (tùy chọn)
- Python 3.9+ (cho ADK)

### Cài đặt Node.js Backend

```bash
# Clone repository
git clone https://github.com/youruser/phongthuybotbackend.git
cd phongthuybotbackend

# Cài đặt dependencies
npm install

# Tạo file .env
cp .env.example .env
# Sửa file .env để phù hợp với môi trường

# Chạy server
npm run dev
```

### Cài đặt Python ADK (Agent Development Kit)

```bash
# Di chuyển vào thư mục Python ADK
cd python_adk

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env
cp .env.example .env
# Sửa file .env để phù hợp với môi trường

# Chạy Python ADK
python main.py
```

## Kiến trúc Agent

### Root Agent

Root Agent đóng vai trò điều phối, nhận yêu cầu từ người dùng và chuyển hướng đến agent chuyên biệt thích hợp.

### Bát Cục Linh Số Agent

Agent chuyên phân tích số điện thoại, CCCD/CMND, STK ngân hàng, mật khẩu theo phương pháp Bát Cục Linh Số.

## API Endpoints

### Root Agent

```
GET /api/v2/agent
POST /api/v2/agent/chat
POST /api/v2/agent/stream
POST /api/v2/agent/query
```

### Bát Cục Linh Số

```
GET /api/v2/bat-cuc-linh-so
POST /api/v2/bat-cuc-linh-so/analyze
POST /api/v2/bat-cuc-linh-so/phone
POST /api/v2/bat-cuc-linh-so/cccd
```

## Ví dụ sử dụng API

### Phân tích số điện thoại

```bash
curl -X POST http://localhost:5000/api/v2/bat-cuc-linh-so/phone \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "0987654321"}'
```

### Gửi tin nhắn đến Root Agent

```bash
curl -X POST http://localhost:5000/api/v2/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Phân tích số điện thoại 0987654321", "sessionId": "session123"}'
```

### Truy vấn trực tiếp đến Bát Cục Linh Số Agent

```bash
curl -X POST http://localhost:5000/api/v2/agent/query \
  -H "Content-Type: application/json" \
  -d '{"agentType": "batcuclinh_so", "query": "Phân tích số CCCD 012345678901"}'
```

## Chức năng dự phòng (Fallback)

API được thiết kế để hoạt động ngay cả khi Python ADK chưa khởi động. Khi Python ADK không khả dụng, hệ thống sẽ sử dụng chức năng dự phòng trong Node.js để cung cấp kết quả cơ bản.

## Cấu trúc thư mục

```
/
├── api/               # API endpoints
│   ├── middleware/    # Middleware chung
│   └── v2/            # API v2
│       ├── middleware/# Middleware API v2
│       ├── routes/    # Route handlers 
│       └── services/  # Business logic
├── services/          # Core services
├── python_adk/        # Python Agent Development Kit
│   ├── agents/        # Agent definitions
│   ├── a2a/           # Agent-to-Agent protocol
│   └── utils/         # Utility modules
└── config/            # Configuration 