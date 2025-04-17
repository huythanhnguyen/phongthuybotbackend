# Kế hoạch triển khai Phong Thủy Số trên Render

## Tổng quan

Dự án "Phong Thủy Số" bao gồm hai thành phần chính cần triển khai:

1. **Node.js Backend** - Cung cấp API endpoints, xử lý requests, và kết nối với cơ sở dữ liệu
2. **Python ADK Service** - Cung cấp các agent và công cụ phân tích sử dụng Google Agent Development Kit

Kế hoạch này mô tả cách triển khai cả hai thành phần trên Render.com.

## Chuẩn bị môi trường

### 1. Tạo tài khoản Render

- Đăng ký tài khoản tại [Render](https://render.com)
- Kết nối GitHub repository của dự án
- Thiết lập phương thức thanh toán (nếu cần)

### 2. Chuẩn bị repository

- Đảm bảo repository chứa cả hai thành phần (Node.js và Python ADK)
- Tạo file `render.yaml` để cấu hình triển khai
- Tạo file `requirements.txt` cho Python ADK
- Cập nhật `package.json` để bao gồm các dependencies cần thiết (như `uuid`)

## Triển khai Node.js Backend

### Cấu hình Web Service

**Thông số cơ bản:**
- **Name**: `phongthuybotbackend`
- **Environment**: `Node.js`
- **Region**: `Singapore (Southeast Asia)`
- **Branch**: `main`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm start`
- **Plan**: `Starter ($7/month)` hoặc Free Plan (cho giai đoạn phát triển)

**Cấu hình Node.js:**
- Node version: 16.x hoặc mới hơn

**Biến môi trường:**
```
NODE_ENV=production
PORT=10000
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/phongthuybotdb
PYTHON_ADK_URL=https://phongthuybotadk.onrender.com
ADK_API_KEY=<secret_key>
JWT_SECRET=<your_secret_key>
JWT_EXPIRE=30d
CLIENT_URL=https://phongthuyso.onrender.com
GEMINI_API_KEY=<your_gemini_api_key>
```

### Cài đặt dependencies

Đảm bảo `package.json` bao gồm các dependencies sau:
```json
{
  "dependencies": {
    "axios": "^1.6.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "express": "^4.18.2",
    "jsonwebtoken": "^9.0.2",
    "mongoose": "^8.0.1",
    "morgan": "^1.10.0",
    "uuid": "^9.0.1"
  },
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "build": "echo 'Build completed'"
  }
}
```

## Triển khai Python ADK Service

### Cấu hình Web Service

**Thông số cơ bản:**
- **Name**: `phongthuybotadk`
- **Environment**: `Python 3`
- **Region**: `Singapore (Southeast Asia)`
- **Branch**: `main`
- **Build Command**: `pip install -r python_adk/requirements.txt`
- **Start Command**: `cd python_adk && python main.py`
- **Plan**: `Starter ($7/month)` hoặc Free Plan (cho giai đoạn phát triển)

**Cấu hình Python:**
- Python version: 3.9 hoặc mới hơn

**Biến môi trường:**
```
PORT=10000
HOST=0.0.0.0
LOG_LEVEL=INFO
API_KEY=<same_as_ADK_API_KEY_in_Node.js>
API_KEY_HEADER=X-API-Key
GOOGLE_API_KEY=<your_gemini_api_key>
DEFAULT_MODEL=gemini-pro
ROOT_AGENT_MODEL=gemini-pro
BATCUCLINH_SO_AGENT_MODEL=gemini-pro
PHONE_ANALYZER_MODEL=gemini-pro
CCCD_ANALYZER_MODEL=gemini-pro
```

### Cài đặt Python dependencies

Đảm bảo `python_adk/requirements.txt` bao gồm các dependencies sau:
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.4.2
google-generativeai==0.3.1
adk==0.2.5
requests==2.31.0
python-dotenv==1.0.0
pytest==7.4.3
```

## Tạo file render.yaml

Tạo file `render.yaml` tại thư mục gốc của repository với nội dung sau:

```yaml
services:
  # Node.js Backend
  - type: web
    name: phongthuybotbackend
    env: node
    region: singapore
    plan: starter
    buildCommand: npm install
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 10000
      - key: MONGODB_URI
        sync: false
      - key: PYTHON_ADK_URL
        value: https://phongthuybotadk.onrender.com
      - key: ADK_API_KEY
        sync: false
      - key: JWT_SECRET
        sync: false
      - key: JWT_EXPIRE
        value: 30d
      - key: CLIENT_URL
        value: https://phongthuyso.onrender.com
      - key: GEMINI_API_KEY
        sync: false

  # Python ADK Service
  - type: web
    name: phongthuybotadk
    env: python
    region: singapore
    plan: starter
    buildCommand: pip install -r python_adk/requirements.txt
    startCommand: cd python_adk && python main.py
    envVars:
      - key: PORT
        value: 10000
      - key: HOST
        value: 0.0.0.0
      - key: LOG_LEVEL
        value: INFO
      - key: API_KEY
        sync: false
      - key: API_KEY_HEADER
        value: X-API-Key
      - key: GOOGLE_API_KEY
        sync: false
      - key: DEFAULT_MODEL
        value: gemini-pro
      - key: ROOT_AGENT_MODEL
        value: gemini-pro
      - key: BATCUCLINH_SO_AGENT_MODEL
        value: gemini-pro
```

## Bước triển khai

1. **Đẩy code lên GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Thiết lập trên Render**:
   - Đăng nhập vào tài khoản Render
   - Chọn "New" > "Blueprint"
   - Chọn repository từ GitHub
   - Render sẽ tự động phát hiện file render.yaml và đề xuất thiết lập
   - Xem xét cấu hình và thiết lập các biến môi trường mật

3. **Triển khai và kiểm tra**:
   - Nhấn "Apply" để bắt đầu quá trình triển khai
   - Kiểm tra logs để đảm bảo không có lỗi trong quá trình triển khai
   - Thử nghiệm API endpoints sau khi triển khai hoàn tất

## Quản lý và giám sát

### Cấu hình Autoscaling (tuỳ chọn)

Nếu muốn tự động điều chỉnh tài nguyên dựa trên lưu lượng:

- Đi đến mục "Settings" của service
- Chọn "Autoscaling"
- Thiết lập các thông số như min/max instances

### Giám sát

Sử dụng tính năng giám sát tích hợp của Render:

- **Metrics**: Theo dõi CPU, RAM, và Network usage
- **Logs**: Kiểm tra logs realtime
- **Alerts**: Thiết lập cảnh báo cho các sự cố

### Cập nhật

Để cập nhật các dịch vụ:

1. Đẩy các thay đổi lên GitHub
2. Render sẽ tự động phát hiện và triển khai lại (nếu cấu hình Auto Deploy)

## Khắc phục sự cố

### Lỗi Node.js

- **Cannot find module 'uuid'**: Chạy `npm install uuid` và đảm bảo nó được thêm vào package.json
- **EADDRINUSE**: Đảm bảo port không bị conflict, Render thường sử dụng PORT environment variable
- **MongoDB connection errors**: Kiểm tra MONGODB_URI và đảm bảo mạng cho phép kết nối

### Lỗi Python ADK

- **ModuleNotFoundError**: Đảm bảo tất cả dependencies được liệt kê trong requirements.txt
- **ImportError**: Kiểm tra cấu trúc import và đường dẫn tương đối
- **API Key errors**: Đảm bảo GOOGLE_API_KEY được thiết lập đúng

## Tham khảo

- [Render Docs - Web Services](https://render.com/docs/web-services)
- [Render Docs - Environment Variables](https://render.com/docs/environment-variables)
- [Render Docs - YAML Configuration](https://render.com/docs/yaml-spec)
- [Render Docs - Python Services](https://render.com/docs/python)
- [Render Docs - Node.js Services](https://render.com/docs/node-js) 