# API Troubleshooting Guide

## Vấn đề hiện tại

Ứng dụng hiện tại đang gặp lỗi 500 khi gọi từ frontend đến API `/agent/chat`. Những lỗi chính bao gồm:

```
phongthuybotbackend.onrender.com/api/v2/agent/chat:1 Failed to load resource: the server responded with a status of 500 ()
index-6cfca9c1.js:612 API Error [post] /agent/chat: Object
index-6cfca9c1.js:612 Error creating new session: Error: Đã xảy ra lỗi khi xử lý tin nhắn
```

## Nguyên nhân và giải pháp

Sau khi phân tích cả NodeJS API Gateway và Python ADK backend, chúng tôi đã xác định và khắc phục các vấn đề sau:

### 1. Lỗi xử lý HTTP exception trong FastAPI

**Vấn đề:** Python ADK trả về HTTP Exception 500 thay vì JSON response, khiến client frontend không thể xử lý.

**Giải pháp:** Cập nhật các endpoint trong `python_adk/main.py` để trả về JSON response thay vì raise Exception.

### 2. Vấn đề phiên bản thư viện

**Vấn đề:** Có sự không tương thích giữa các phiên bản của `google-adk` và `google-generativeai`.

**Giải pháp:** Cố định phiên bản cụ thể trong `requirements.txt`:
- `google-adk==0.2.0`
- `google-generativeai==0.4.0`

### 3. Xử lý lỗi không đầy đủ trong Node.js API Gateway

**Vấn đề:** API Gateway không xử lý đúng các lỗi từ Python ADK.

**Giải pháp:** Cải thiện xử lý lỗi trong `rootAgentService.js` bằng cách:
- Thêm retry logic
- Fallback đến các endpoint khác nhau
- Trả về phản hồi thân thiện với người dùng thay vì lỗi kỹ thuật

### 4. Vấn đề session_id vs sessionId

**Vấn đề:** Không nhất quán giữa `session_id` và `sessionId` trong các API.

**Giải pháp:** Cập nhật các endpoint để hỗ trợ cả hai format.

## Kiểm tra và triển khai

1. **Kiểm tra môi trường local:**
   ```
   # Khởi động API Gateway (NodeJS)
   node server.js
   
   # Khởi động Python ADK (terminal khác)
   cd python_adk
   python main.py
   ```

2. **Kiểm tra endpoint:**
   ```
   curl -X POST http://localhost:6000/api/v2/agent/chat
   ```

3. **Triển khai:**
   - Đảm bảo file `.env` được cấu hình đúng
   - Triển khai lên Render.com

## Biến môi trường cần thiết

Tạo file `.env` trong thư mục gốc dự án và một file `.env` khác trong thư mục `python_adk/` với nội dung sau:

**Root .env:**
```
PORT=6000
NODE_ENV=development
PYTHON_ADK_URL=http://localhost:10000
ADK_API_KEY=dev_key
```

**python_adk/.env:**
```
PORT=10000
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
ADK_API_KEY=dev_key
DEBUG=True
```

## Các bước bảo trì trong tương lai

1. Luôn đảm bảo phiên bản của các thư viện Google ADK và Gemini AI được cố định
2. Thử nghiệm cả Node.js gateway và Python ADK trước khi triển khai
3. Kiểm tra logs từ cả hai service để tìm lỗi
4. Nếu cần, có thể sử dụng fallback xử lý tin nhắn trong `rootAgentService.js` để tạm thời phục vụ người dùng khi có sự cố với Python ADK

## Cấu trúc API hiện tại

1. Frontend gọi đến `/api/v2/agent/chat` (Node.js Gateway)
2. Node.js Gateway chuyển tiếp đến Python ADK qua `/chat` hoặc `/agent/chat`
3. Python ADK xử lý tin nhắn và trả về kết quả

Thiết kế này cho phép:
- Khả năng mở rộng cao
- Tách biệt giữa API Gateway và xử lý AI
- Fallback tới xử lý tin nhắn local khi cần thiết 