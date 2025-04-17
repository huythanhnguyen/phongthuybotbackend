# Python ADK Service for Phong Thủy Số

Dịch vụ ADK (Agent Development Kit) cho ứng dụng Phong Thủy Số, cung cấp các endpoints để phân tích số điện thoại, CCCD, mật khẩu và số tài khoản ngân hàng theo phương pháp Bát Cục Linh Số.

## Cấu trúc

- `main.py`: Module chính chứa các định nghĩa về API endpoints
- `asgi.py`: Entry point cho ASGI servers (như uvicorn, gunicorn, hypercorn)
- `agents/`: Thư mục chứa các agent chuyên biệt
- `a2a/`: Agent-to-agent communication utilities
- `mcp/`: Multi-component protocol

## Triển khai trên Render.com

Để triển khai thành công trên Render.com, cần lưu ý các điểm sau:

1. **Entry point**: Sử dụng `asgi.py` làm entry point, không sử dụng trực tiếp `main.py`
2. **Start command**: Đảm bảo lệnh khởi động như sau:
   ```
   cd /opt/render/project/src && uvicorn python_adk.asgi:application --host 0.0.0.0 --port $PORT
   ```
3. **Dependencies**: Đảm bảo `requirements.txt` chứa đầy đủ các dependencies và phiên bản cụ thể để tránh xung đột

## Xử lý lỗi "Could not import module 'main'"

Nếu gặp lỗi "Could not import module 'main'" khi triển khai trên Render.com, nguyên nhân có thể do:

1. **Đường dẫn không chính xác**: Đảm bảo lệnh khởi động đã cd vào thư mục gốc của project
2. **Import không đúng**: Kiểm tra cú pháp import trong `asgi.py` phải là `from python_adk.main import app` nếu bạn ở thư mục gốc, hoặc `from main import app` nếu bạn đã cd vào thư mục `python_adk`
3. **PYTHONPATH**: Đôi khi cần thêm thư mục gốc vào PYTHONPATH trước khi khởi động

## Phát triển cục bộ

```bash
cd python_adk
pip install -r requirements.txt
python main.py
```

Ứng dụng sẽ chạy tại `http://localhost:10000`

## API Documentation

Truy cập `http://localhost:10000/docs` hoặc `https://your-render-url/docs` để xem tài liệu API tự động tạo bởi Swagger UI. 