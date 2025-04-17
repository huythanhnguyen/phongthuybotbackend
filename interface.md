# API Documentation - Phong Thủy Số

## Tổng quan

API của Phong Thủy Số v2.0 cung cấp các endpoints để phân tích số điện thoại, CCCD và các thông tin khác theo phương pháp Bát Cục Linh Số. Hệ thống được xây dựng với kiến trúc agent-based, bao gồm Root Agent điều phối và các Expert Agent chuyên biệt.

**Base URL:**
- Development: `http://localhost:5000`
- Production: `https://phongthuybotbackend.onrender.com`

## Authentication

Hiện tại, API chưa yêu cầu xác thực. Xác thực sẽ được bổ sung trong các phiên bản tiếp theo.

## Định dạng Response

Tất cả các API endpoints đều trả về dữ liệu dưới dạng JSON với định dạng:

```json
{
  "success": boolean,
  "message": string,
  "result": object
}
```

Khi gặp lỗi:

```json
{
  "success": false,
  "message": string,
  "error": string
}
```

## API Endpoints

### Health Check

#### GET /api/health

Kiểm tra trạng thái hoạt động của API.

**Response:**

```json
{
  "status": "ok",
  "message": "Phong Thủy Số API is running",
  "version": "2.0.0",
  "adkEnabled": true
}
```

### Thông tin chung

#### GET /

Lấy thông tin tổng quan về API.

**Response:**

```json
{
  "message": "Chào mừng đến với Phong Thủy Số API v2",
  "version": "2.0.0",
  "status": "production",
  "endpoints": {
    "agent": "/api/v2/agent",
    "batCucLinhSo": "/api/v2/bat-cuc-linh-so",
    "health": "/api/health"
  }
}
```

### Root Agent API

#### GET /api/v2/agent

Lấy thông tin về API Root Agent.

**Response:**

```json
{
  "success": true,
  "message": "Phong Thủy Số - Root Agent API",
  "version": "2.0.0",
  "endpoints": {
    "chat": "POST /api/v2/agent/chat",
    "stream": "POST /api/v2/agent/stream",
    "query": "POST /api/v2/agent/query"
  }
}
```

#### POST /api/v2/agent/chat

Gửi tin nhắn đến Root Agent và nhận phản hồi.

**Request Body:**

```json
{
  "message": "Phân tích số điện thoại 0987654321",
  "sessionId": "session123", // optional
  "userId": "user456", // optional
  "metadata": {} // optional
}
```

**Response:**

```json
{
  "success": true,
  "message": "Xử lý tin nhắn thành công",
  "result": {
    "sessionId": "session123",
    "response": "Phân tích số điện thoại 0987654321:\n\nTổng số: 5 (Ngũ hành: Thổ)\nCác cặp số...",
    "agentType": "batcuclinh_so",
    "success": true
  }
}
```

#### POST /api/v2/agent/stream

Gửi tin nhắn đến Root Agent và nhận phản hồi dạng stream (Server-Sent Events).

**Request Body:**

```json
{
  "message": "Phân tích số điện thoại 0987654321",
  "sessionId": "session123", // optional
  "userId": "user456", // optional
  "metadata": {} // optional
}
```

**Response:**

Phản hồi dạng Server-Sent Events (SSE):

```
data: {"type":"chunk","content":"Phân tích số điện thoại"}
data: {"type":"chunk","content":" 0987654321:"}
data: {"type":"chunk","content":"\n\nTổng số: 5"}
...
data: {"type":"complete"}
```

#### POST /api/v2/agent/query

Gửi truy vấn trực tiếp đến một agent cụ thể.

**Request Body:**

```json
{
  "agentType": "batcuclinh_so",
  "query": "Phân tích số CCCD 012345678901",
  "sessionId": "session123", // optional
  "userId": "user456", // optional
  "metadata": {} // optional
}
```

**Response:**

```json
{
  "success": true,
  "message": "Truy vấn thành công",
  "result": {
    "sessionId": "session123",
    "response": "Phân tích số CCCD 012345678901:\n\nTổng số: 3 (Ngũ hành: Mộc)\nThông tin...",
    "agentType": "batcuclinh_so",
    "success": true
  }
}
```

### Bát Cục Linh Số API

#### GET /api/v2/bat-cuc-linh-so

Lấy thông tin về API Bát Cục Linh Số.

**Response:**

```json
{
  "success": true,
  "message": "API Bát Cục Linh Số v2.0",
  "endpoints": {
    "analyze": "POST /api/v2/bat-cuc-linh-so/analyze",
    "phoneAnalysis": "POST /api/v2/bat-cuc-linh-so/phone",
    "cccdAnalysis": "POST /api/v2/bat-cuc-linh-so/cccd"
  }
}
```

#### POST /api/v2/bat-cuc-linh-so/analyze

Phân tích thông tin chung theo Bát Cục Linh Số.

**Request Body:**

```json
{
  "data": "0987654321",
  "type": "phone" // "phone" hoặc "cccd"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Phân tích thành công",
  "type": "phone",
  "result": {
    "phoneNumber": "0987654321",
    "totalValue": 5,
    "element": "Thổ",
    "analysis": "Phân tích chi tiết...",
    "success": true
  }
}
```

#### POST /api/v2/bat-cuc-linh-so/phone

Phân tích số điện thoại theo Bát Cục Linh Số.

**Request Body:**

```json
{
  "phoneNumber": "0987654321"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Phân tích số điện thoại thành công",
  "result": {
    "phoneNumber": "0987654321",
    "totalValue": 5,
    "element": "Thổ",
    "analysis": "Phân tích chi tiết...",
    "success": true
  }
}
```

#### POST /api/v2/bat-cuc-linh-so/cccd

Phân tích CCCD/CMND theo Bát Cục Linh Số.

**Request Body:**

```json
{
  "cccdNumber": "012345678901"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Phân tích CCCD/CMND thành công",
  "result": {
    "cccdNumber": "012345678901",
    "totalValue": 3,
    "element": "Mộc",
    "info": {
      "type": "CCCD",
      "provinceCode": "012",
      "gender": "Nam",
      "birthYear": "2001",
      "randomCode": "345678"
    },
    "analysis": "Phân tích chi tiết...",
    "success": true
  }
}
```

## Sử dụng Streaming API trong Frontend

### JavaScript/Vue.js

```javascript
async function streamChatResponse(message, sessionId) {
  try {
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

    // Tạo reader từ response body
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = '';
    
    // Xử lý stream
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      // Decode và xử lý từng chunk
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n\n');
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.substring(6));
            
            if (data.type === 'chunk') {
              fullText += data.content;
              // Cập nhật UI với nội dung mới
              updateChatUI(fullText);
            } else if (data.type === 'complete') {
              // Xử lý khi stream hoàn tất
              finalizeChatUI(fullText);
            } else if (data.type === 'error') {
              // Xử lý lỗi
              handleStreamError(data.error);
            }
          } catch (e) {
            console.error('Error parsing SSE data:', e);
          }
        }
      }
    }
  } catch (error) {
    console.error('Error with streaming request:', error);
  }
}
```

## Deployment

### Server đã được triển khai lên Render.com

API đã được triển khai tại:
- **Production URL:** `https://phongthuybotbackend.onrender.com`

### Cấu hình hệ thống

Server được cấu hình với:
- **Node.js runtime:** v18.x
- **Python ADK:** v3.10+
- **Database:** MongoDB Atlas (tùy chọn)

### Cấu trúc Dự án

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

## Fallback Mechanism

API được thiết kế để vẫn hoạt động khi Python ADK chưa khởi động. Trong trường hợp này, Node.js backend sẽ xử lý các yêu cầu và trả về kết quả phân tích cơ bản.

### Các tính năng dự phòng

- **Phân tích số điện thoại:** Tính toán tổng số, rút gọn, và xác định ngũ hành
- **Phân tích CCCD:** Tính toán tổng số, rút gọn, ngũ hành, và trích xuất thông tin cơ bản từ CCCD 12 số

## Quản lý Phiên (Sessions)

Hệ thống hỗ trợ quản lý phiên để duy trì cuộc hội thoại:

- Mỗi phiên được định danh bởi một `sessionId` duy nhất
- Nếu không cung cấp `sessionId`, hệ thống sẽ tự động tạo ID mới
- Lịch sử hội thoại được lưu trữ tạm thời trong bộ nhớ server

## Hạn chế & Phát triển Tương lai

1. **Chứng thực (Authentication):** Hiện tại chưa có hệ thống chứng thực, sẽ bổ sung trong phiên bản tiếp theo
2. **Database:** Hỗ trợ lưu trữ dữ liệu vào MongoDB (cần cấu hình trong `.env`)
3. **Mở rộng Agent:** Thêm các chuyên gia phong thủy khác
4. **Tích hợp LLM:** Cải thiện khả năng phân tích với các mô hình ngôn ngữ lớn
