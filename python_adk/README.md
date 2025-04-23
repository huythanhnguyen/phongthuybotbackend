# PhongThuyBot Backend - Google ADK

Hệ thống backend cho ứng dụng Phong Thủy Số dựa trên Google Agent Development Kit (ADK).

## Yêu cầu hệ thống

- Python 3.13+
- Các thư viện phụ thuộc trong file `requirements.txt`

## Cài đặt

### 1. Cài đặt Python 3.13

Đảm bảo bạn đã cài đặt Python 3.13 hoặc mới hơn. Kiểm tra phiên bản Python của bạn:

```bash
python --version
```

### 2. Tạo môi trường ảo (khuyến nghị)

```bash
python -m venv venv
source venv/bin/activate  # Trên Linux/MacOS
venv\Scripts\activate     # Trên Windows
```

### 3. Cài đặt các gói phụ thuộc

```bash
pip install -r requirements.txt
```

## Cấu hình

### 1. Tạo file .env

Tạo file `.env` với nội dung sau:

```env
# Server Configuration
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO

# API Security
API_KEY=dev_key
API_KEY_HEADER=X-API-Key

# Gemini API
GEMINI_API_KEY=your_google_api_key
DEFAULT_MODEL=gemini-1.5-pro

# ADK Configuration
SESSION_TTL=3600  # Session time-to-live in seconds
ROOT_AGENT_MODEL=gemini-pro
BATCUCLINH_SO_AGENT_MODEL=gemini-pro
```

Thay `your_google_api_key` bằng API key của Gemini của bạn.

## Chạy ứng dụng

### 1. Kiểm tra môi trường

Chạy công cụ kiểm tra để đảm bảo môi trường đã được cấu hình đúng:

```bash
python debug_tool.py
```

### 2. Chạy ứng dụng chính

```bash
python main.py
```

### 3. Chạy máy chủ web API

```bash
python asgi.py
```

## Cấu trúc dự án

```
python_adk/
├── adk/                   # Các tiện ích mở rộng cho ADK
├── agents/                # Định nghĩa các agent
│   ├── batcuclinh_so_agent/  # Agent phân tích phong thủy số
│   ├── payment_agent/     # Agent xử lý thanh toán
│   ├── root_agent/        # Agent chính điều phối
│   └── user_agent/        # Agent quản lý người dùng
├── constants/             # Các hằng số dùng chung
├── mcp/                   # Multi-Agent Communication Protocol
├── shared_libraries/      # Thư viện dùng chung
├── utils/                 # Tiện ích
├── main.py                # Điểm vào chính
├── asgi.py                # Máy chủ web API
└── requirements.txt       # Các dependency
```

## Lưu ý quan trọng về Python 3.13 và Google ADK

### 1. Thay đổi trong Google ADK phiên bản 0.2.0

Từ phiên bản 0.2.0, Google ADK đã thay đổi một số API và cách import:

- Sử dụng `from google.adk.tools import agent_tool_registry` và `from google.adk.tools.agent_tool import AgentTool` thay vì `from google.adk.tools.agent_tool import agent_tool, agent_tool_registry`
- Sử dụng decorator `@agent_tool_registry.register` thay vì `@agent_tool`
- Sử dụng phương thức `invoke()` thay vì `predict()` hoặc `run()`

### 2. Cách khắc phục lỗi phổ biến

Nếu gặp lỗi "cannot import name 'agent_tool' from 'google.adk.tools.agent_tool'", hãy kiểm tra:

1. Phiên bản Google ADK đã được cập nhật lên >=0.2.0
2. Thay đổi import và decorator trong mã nguồn:
   - `from google.adk.tools import agent_tool_registry`
   - `from google.adk.tools.agent_tool import AgentTool`
   - `@agent_tool_registry.register`

### 3. Module `imp` trong Python 3.13

Lỗi "ModuleNotFoundError: No module named 'imp'" trong Python 3.13 xảy ra do module `imp` đã bị xóa:

1. Đảm bảo dùng đúng phiên bản Google ADK tương thích với Python 3.13
2. Nếu sử dụng gcloud hoặc các công cụ khác, có thể cần cấu hình CLOUDSDK_PYTHON để trỏ về phiên bản Python khác

## Xử lý lỗi

Nếu bạn gặp các vấn đề khác, hãy xem file log tại `logs/app.log` để biết thêm chi tiết.

## Giấy phép

MIT 