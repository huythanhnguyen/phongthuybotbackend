# Phong Thủy Số - Agent-based System

Hệ thống phân tích phong thủy số học sử dụng kiến trúc Multi-Agent dựa trên Google ADK.

## Giới thiệu

Phong Thủy Số là một ứng dụng cung cấp dịch vụ phân tích phong thủy số học, giúp người dùng phân tích và tối ưu hóa các yếu tố số học trong cuộc sống hàng ngày như số điện thoại, CCCD, mật khẩu, và tài khoản ngân hàng dựa trên nguyên lý Bát Cực Linh Số và các nguyên tắc phong thủy truyền thống.

## Yêu cầu Hệ thống

- Python 3.13+
- Google ADK
- Gemini API key

## Cài đặt

### 1. Cài đặt môi trường

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt môi trường
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate

# Cài đặt các dependencies
pip install -e .
```

### 2. Cấu hình API Key

Tạo file `.env` với nội dung:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Sử dụng

### Chạy ứng dụng trong chế độ tương tác

```bash
python -m python_adk.main
```

Các tùy chọn:
- `--model`: Chọn model Gemini (mặc định: gemini-1.5-pro)
- `--api-key`: Cung cấp Gemini API key (nếu không muốn sử dụng từ .env)

Ví dụ:
```bash
python -m python_adk.main --model gemini-1.5-flash
```

## Kiến trúc Hệ thống

Hệ thống sử dụng kiến trúc Multi-Agent với các thành phần chính:

### 1. Root Agent
- Điều phối yêu cầu đến các agent chuyên biệt
- Phân tích ý định người dùng
- Đảm bảo trải nghiệm liền mạch và nhất quán

### 2. BatCucLinhSo Agent
- Phân tích số điện thoại theo Bát Cực Linh Số
- Phân tích 6 số cuối CCCD
- Đề xuất số điện thoại theo mục đích sử dụng
- Phân tích và đề xuất số tài khoản ngân hàng
- Tạo và đánh giá mật khẩu theo phong thủy

### 3. Payment Agent
- Quản lý quota người dùng
- Xử lý thanh toán và nâng cấp gói dịch vụ
- Quản lý lịch sử thanh toán

### 4. User Agent
- Quản lý thông tin người dùng
- Xác thực đăng nhập/đăng ký
- Quản lý hồ sơ người dùng
- Lưu trữ lịch sử sử dụng dịch vụ

## Đóng góp

Vui lòng tạo issue hoặc pull request nếu bạn muốn đóng góp cho dự án.

## Giấy phép

Apache License 2.0 