# Phong Thủy Số - Backend API

Phong Thủy Số Backend API là hệ thống cung cấp các endpoint phân tích số điện thoại, CCCD/CMND theo phương pháp Bát Cục Linh Số, sử dụng kiến trúc agent-based.

## Deployed API

API đã được triển khai tại:
- **Production URL:** https://phongthuybotbackend.onrender.com

## API Status

Bạn có thể kiểm tra trạng thái hoạt động của API tại:
- https://phongthuybotbackend.onrender.com/api/health

## Kiến trúc

Backend được xây dựng với hai thành phần chính:

1. **Node.js Server**: Xử lý các HTTP requests, routing, và phân tích dự phòng nếu Python ADK chưa khởi động.

2. **Python ADK**: Phần xử lý phân tích chuyên sâu, dựa trên kiến trúc Google Agent Development Kit, giao tiếp với Node.js server qua REST API.

## Tính năng chính

- **Root Agent API**: Xử lý tin nhắn đầu vào, định tuyến tới các expert agents
- **Bát Cục Linh Số API**: Phân tích số điện thoại và CCCD/CMND
- **Streaming API**: Hỗ trợ phản hồi dạng stream cho trải nghiệm người dùng mượt mà
- **Fallback Mechanism**: Vẫn hoạt động khi Python ADK chưa khởi động
- **Session Management**: Lưu trữ và quản lý phiên hội thoại

## API Documentation

Chi tiết về các endpoints và cách sử dụng API có thể tìm thấy trong file [interface.md](./interface.md).

## Cấu trúc dự án

```
phongthuybotbackend/
├── api/                  # API routes và controllers
│   └── v2/               # API version 2
│       ├── controllers/  # Logic xử lý request
│       ├── middleware/   # Middleware
│       ├── routes/       # Định nghĩa routes
│       └── services/     # Business logic
├── constants/            # Các hằng số
├── config/               # Cấu hình
├── python_adk/           # Python ADK integration
│   ├── a2a/              # Agent-to-agent communication
│   ├── agents/           # Agent implementations
│   ├── mcp/              # Multi-component protocol
│   └── main.py           # FastAPI entry point
├── services/             # Shared services
├── .env.example          # Template cho biến môi trường
├── server.js             # Entry point
└── package.json          # Node.js dependencies
```

## Development Setup

```bash
# Cài đặt dependencies
npm install

# Tạo file .env từ template
cp .env.example .env

# Khởi động server
npm start
```

## Python ADK Setup

```bash
# Đi đến thư mục Python ADK
cd python_adk

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env từ template
cp .env.example .env

# Khởi động Python ADK
python main.py
```

## Kết nối Frontend

Frontend có thể kết nối đến API theo các cách:

1. **Regular API Calls**: Sử dụng phương thức fetch hoặc axios
2. **Streaming**: Sử dụng Server-Sent Events (SSE)

Ví dụ streaming với JavaScript:

```javascript
async function streamChatResponse(message, sessionId) {
  const response = await fetch('https://phongthuybotbackend.onrender.com/api/v2/agent/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      sessionId,
    }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    // Xử lý chunk dữ liệu
    // ...
  }
}
```

## Deployment

API được triển khai trên Render.com với các cấu hình:
- Node.js web service
- Auto-deploy từ GitHub repository
- Environment variables được cấu hình trong Render Dashboard

## Testing

Sử dụng script test-api.js để kiểm tra các endpoints:

```bash
node test-api.js
```