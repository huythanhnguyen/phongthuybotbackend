# API Documentation - Phong Thủy Số

## Tổng quan

API của Phong Thủy Số v2.0 cung cấp các endpoints để phân tích số điện thoại, CCCD/CMND, mật khẩu và số tài khoản ngân hàng theo phương pháp Bát Cục Linh Số. Hệ thống được xây dựng với kiến trúc agent-based sử dụng Google Agent Development Kit (ADK), bao gồm Root Agent điều phối và các Expert Agent chuyên biệt.

**Base URL:**
- Development: `http://localhost:5000` (Node.js Gateway)
- ADK Service: `http://localhost:10000` (Python ADK)
- Production: `https://phongthuybotbackend.onrender.com`

## Kiến trúc hệ thống

Hệ thống sử dụng kiến trúc hai lớp:

1. **API Gateway (Node.js)**: Xử lý yêu cầu từ client, chuyển tiếp tới Python ADK Service
2. **ADK Service (Python)**: Triển khai các agents và logic phân tích sử dụng Google ADK

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

Gửi tin nhắn đến Root Agent và nhận phản hồi. Root Agent sẽ tự động phân tích ý định người dùng và chuyển hướng đến agent chuyên biệt.

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
    "cccdAnalysis": "POST /api/v2/bat-cuc-linh-so/cccd",
    "passwordAnalysis": "POST /api/v2/bat-cuc-linh-so/password",
    "bankAccountAnalysis": "POST /api/v2/bat-cuc-linh-so/bank-account",
    "bankAccountSuggestion": "POST /api/v2/bat-cuc-linh-so/suggest-bank-account"
  }
}
```

#### POST /api/v2/bat-cuc-linh-so/analyze

Phân tích thông tin chung theo Bát Cục Linh Số.

**Request Body:**

```json
{
  "data": "0987654321",
  "type": "phone" // Một trong "phone", "cccd", "password", "bank_account"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Phân tích thành công",
  "type": "phone",
  "result": {
    // Kết quả phân tích tùy theo type
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
    "success": true,
    "phoneNumber": "0987654321",
    "normalized": "0987654321",
    "analysis": {
      "original_number": "0987654321",
      "normalized_number": "0987654321",
      "pairs": ["09", "98", "87", "76", "65", "54", "43", "32", "21"],
      "pairs_analysis": [
        {
          "pair": "09",
          "star": "Thiên Y hóa hung",
          "description": "Thiên Y có số 0: Năng lượng yếu hoặc biến chất",
          "energy": 1,
          "nature": "Cát hóa hung"
        },
        // ... các cặp số khác
      ],
      "energy_balance": {
        "total_score": 6,
        "average_energy": 2.2,
        "cats_count": 3,
        "hungs_count": 4,
        "yin_yang_balance": "Âm thịnh (nhiều hung tinh)",
        "rating": "★★★☆☆ (Trung bình)"
      },
      "purpose_compatibility": {
        "business": {
          "name": "Kinh doanh",
          "score": 5,
          "rating": "★★★☆☆ (Trung bình)",
          "favorable_count": 1,
          "unfavorable_count": 2
        },
        // ... các mục đích khác
      },
      "advice": "Số điện thoại này có năng lượng trung bình. Số điện thoại này phù hợp nhất cho mục đích Tình cảm. Số có nhiều hung tinh, cần chú ý đến các mặt tiêu cực có thể xảy ra."
    }
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
    "success": true,
    "cccd_number": "012345678901",
    "content": "Phân tích số CCCD: 012345678901\n\nTổng số (Lộ số): 3 - Ngũ hành: Mộc\n\nThông tin cá nhân:\n- Tỉnh/Thành phố: Hà Nội\n- Giới tính: Nữ\n- Năm sinh: 2001\n- Mã ngẫu nhiên: 45678901\n\nCác cặp số đặc biệt:\n- Cặp số giống nhau: Không có\n- Cặp số liền kề tăng dần: 1-2(12), 2-3(23), 3-4(34), 4-5(45), 5-6(56), 6-7(67), 7-8(78), 8-9(89), 9-10(90)\n- Cặp số liền kề đảo ngược: Không có\n- Cặp số tốt: 3-4(34), 6-7(67), 8-9(89)\n\nĐiểm mạnh:\n- Nhiều cặp số tăng dần liên tiếp thể hiện sự phát triển thuận lợi\n- Mộc mạnh, thích hợp cho sáng tạo và phát triển cá nhân\n- Có nhiều cặp số tốt mang lại may mắn trong học tập và sự nghiệp\n\nĐiểm yếu:\n- Một số cặp số thiếu cân bằng, có thể gây ra bất ổn trong các mối quan hệ\n- Thiếu yếu tố Kim và Thủy\n\nĐánh giá tổng thể: Tốt (7/10)\nSố CCCD này mang nhiều năng lượng tích cực, đặc biệt thuận lợi cho học tập, sáng tạo và sự phát triển. Người sở hữu số này có thể gặp thuận lợi trong sự nghiệp nghệ thuật, giáo dục hoặc các ngành cần sự sáng tạo.\n\nLời khuyên: Phát huy các điểm mạnh về sáng tạo và học tập, đồng thời cần chú ý cân bằng trong các mối quan hệ cá nhân.",
    "info": {
      "type": "CCCD",
      "province": "Hà Nội",
      "gender": "Nữ",
      "birth_year": "2001",
      "random_code": "45678901"
    }
  }
}
```

#### POST /api/v2/bat-cuc-linh-so/password

Phân tích mật khẩu theo Bát Cục Linh Số và đưa ra lời khuyên về cả phong thủy lẫn bảo mật.

**Request Body:**

```json
{
  "password": "MyP@ssw0rd123"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Phân tích mật khẩu thành công",
  "result": {
    "success": true,
    "password": "************",
    "hasDigits": true,
    "analysis": {
      "numerology": {
        "digitPairs": ["01", "12", "23"],
        "stars": ["Thiên Y hóa hung", "Tuyệt Mệnh", "Họa Hại"],
        "energy_balance": {
          "total_score": 4,
          "nature": "Hung tinh chiếm ưu thế"
        }
      },
      "security": {
        "strength": "Mạnh",
        "score": 8,
        "features": ["Độ dài tốt", "Có chữ thường", "Có chữ in hoa", "Có số", "Có ký tự đặc biệt"]
      },
      "recommendation": "Mật khẩu có độ bảo mật tốt nhưng có năng lượng phong thủy không thuận lợi. Nên thay đổi cặp số '23' thành '28' hoặc '82' để cải thiện năng lượng mà không làm giảm tính bảo mật."
    }
  }
}
```

#### POST /api/v2/bat-cuc-linh-so/bank-account

Phân tích số tài khoản ngân hàng theo Bát Cục Linh Số.

**Request Body:**

```json
{
  "accountNumber": "1903246813574"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Phân tích số tài khoản thành công",
  "result": {
    "success": true,
    "accountNumber": "1903246813574",
    "analysis": {
      "total_value": 4,
      "element": "Kim",
      "pairs": ["19", "90", "03", "32", "24", "46", "68", "81", "13", "35", "57", "74"],
      "pairs_analysis": [
        {
          "pair": "19",
          "star": "Diên Niên",
          "description": "Năng lực chuyên nghiệp, công việc",
          "energy": 4,
          "nature": "Cát"
        },
        // ... các cặp số khác
      ],
      "purpose_rating": {
        "business": "★★★★☆ (Tốt)",
        "investment": "★★★★★ (Rất tốt)",
        "saving": "★★★★☆ (Tốt)",
        "personal": "★★★☆☆ (Trung bình)"
      },
      "recommendation": "Số tài khoản này rất phù hợp cho mục đích đầu tư và kinh doanh. Đặc biệt thuận lợi cho tăng trưởng và phát triển tài chính dài hạn."
    }
  }
}
```

#### POST /api/v2/bat-cuc-linh-so/suggest-bank-account

Gợi ý số tài khoản ngân hàng phù hợp với mục đích sử dụng.

**Request Body:**

```json
{
  "purpose": "business", // "business", "investment", "saving", "personal", "health"
  "preferredDigits": ["6", "8", "9"] // optional
}
```

**Response:**

```json
{
  "success": true,
  "message": "Gợi ý số tài khoản thành công",
  "result": {
    "success": true,
    "purpose": "business",
    "preferredDigits": ["6", "8", "9"],
    "recommendations": [
      {
        "lastFourDigits": "6868",
        "stars": "Thiên Y",
        "energyLevel": 4,
        "description": "Rất thích hợp cho kinh doanh, mang lại tài lộc và phát triển"
      },
      {
        "lastFourDigits": "8691",
        "stars": "Thiên Y + Diên Niên",
        "energyLevel": 3.5,
        "description": "Kết hợp tài lộc và năng lực chuyên nghiệp"
      },
      // ... các gợi ý khác
    ]
  }
}
```

## Python ADK API Endpoints

Dưới đây là các endpoints được cung cấp trực tiếp bởi Python ADK Service. Các endpoints này được sử dụng nội bộ bởi API Gateway (Node.js).

### Root Endpoint

#### GET /

Lấy thông tin tổng quan về Python ADK Service.

**Response:**

```json
{
  "name": "Phong Thủy Số API",
  "version": "1.0.0",
  "description": "API for analyzing phone numbers and CCCD numbers using Bát Cục Linh Số method"
}
```

### Health Check

#### GET /health

Kiểm tra trạng thái hoạt động của Python ADK Service.

**Response:**

```json
{
  "status": "healthy"
}
```

### Phone Analysis API

#### POST /analyze/phone

Phân tích số điện thoại theo phương pháp Bát Cục Linh Số.

**Request Body:**

```json
{
  "phone_number": "0987654321",
  "purpose": "business" // optional
}
```

**Response:**

```json
{
  "phone_number": "0987654321",
  "network_code": "098",
  "subscriber_number": "7654321",
  "analysis": [
    {
      "number": "09",
      "tinh": "THIEN_Y",
      "name": "Thiên Y",
      "description": "May mắn, tài lộc, phú quý",
      "energy": {...},
      "position": "Rất tốt",
      "nature": "Cát"
    },
    // ... các cặp số khác
  ],
  "combinations": [
    {
      "numbers": "09-87",
      "combination": "THIEN_Y_SINH_KHI",
      "description": "Quý nhân mang tài lộc",
      "detailed_description": "Khi Sinh Khí kết hợp với Thiên Y, tạo thành tổ hợp mạnh về quý nhân và tài lộc..."
    },
    // ... các tổ hợp khác
  ],
  "purpose": "business"
}
```

### CCCD Analysis API

#### POST /analyze/cccd

Phân tích số CCCD theo phương pháp Bát Cục Linh Số.

**Request Body:**

```json
{
  "cccd_number": "012345678901"
}
```

**Response:**

```json
{
  "cccd_number": "012345678901",
  "birth_date": {
    "year": 2001,
    "month": 2,
    "day": 3
  },
  "last_four": "8901",
  "analysis": [
    {
      "number": "01",
      "tinh": "SINH_KHI",
      "name": "Sinh Khí",
      "description": "Quý nhân, may mắn, thuận lợi",
      "energy": {...},
      "position": "Rất tốt",
      "nature": "Cát"
    },
    // ... các cặp số khác
  ],
  "combinations": [
    {
      "numbers": "01-23",
      "combination": "SINH_KHI_DIEN_NIEN",
      "description": "Quý nhân giúp sự nghiệp",
      "detailed_description": "Khi Sinh Khí kết hợp với Diên Niên, tạo thành tổ hợp mạnh về quý nhân và sự nghiệp..."
    },
    // ... các tổ hợp khác
  ]
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
│   ├── middleware/       # Middleware
│   └── v2/               # API version 2
│       ├── routes/       # Định nghĩa routes
│       │   ├── root-agent.js     # Routes cho Root Agent
│       │   └── bat-cuc-linh-so.js # Routes cho Bát Cục Linh Số
│       └── services/     # Business logic
├── constants/            # Các hằng số
├── config/               # Cấu hình
├── python_adk/           # Python ADK integration
│   ├── agents/           # Agent implementations
│   │   ├── root_agent/   # Root Agent xử lý điều phối
│   │   └── batcuclinh_so_agent/ # Agent phân tích Bát Cục Linh Số
│   │       ├── tools/    # Công cụ phân tích (PhoneAnalyzer, CCCDAnalyzer)
│   │       └── prompts/  # Prompts và hướng dẫn cho agent
│   ├── constants/        # Các hằng số Python
│   └── main.py           # FastAPI entry point
├── services/             # Shared services
├── .env.example          # Template cho biến môi trường
├── server.js             # Entry point
└── package.json          # Node.js dependencies
```

## Quản lý Phiên (Sessions)

Hệ thống hỗ trợ quản lý phiên để duy trì cuộc hội thoại:

- Mỗi phiên được định danh bởi một `sessionId` duy nhất
- Nếu không cung cấp `sessionId`, hệ thống sẽ tự động tạo ID mới
- Lịch sử hội thoại được lưu trữ trong bộ nhớ của ADK agent

Cấu trúc dữ liệu phiên trong ADK:
```json
{
  "session_id": "unique-session-id",
  "history": [
    {
      "role": "user",
      "content": "Phân tích số điện thoại 0987654321",
      "timestamp": "2023-06-15T14:30:00Z"
    },
    {
      "role": "assistant",
      "content": "Phân tích số điện thoại 0987654321: ...",
      "analysis_type": "phone",
      "timestamp": "2023-06-15T14:30:05Z"
    }
  ],
  "current_analysis": "phone",
  "last_updated": "2023-06-15T14:30:05Z"
}
```

## Phát triển Tương lai

1. **Chứng thực (Authentication):** Triển khai hệ thống chứng thực JWT
2. **Database Persistence:** Lưu trữ phiên và lịch sử phân tích vào MongoDB 
3. **Mở rộng Agent:** Thêm các agents phân tích phong thủy theo Tứ Trụ, Kinh Dịch
4. **Hệ thống subscription:** Triển khai hệ thống thanh toán và quản lý gói dịch vụ
5. **Mobile app:** Phát triển ứng dụng di động tích hợp với API
6. **Tích hợp Multi-modal:** Hỗ trợ phân tích qua hình ảnh (scan CCCD, scan số điện thoại)
