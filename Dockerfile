FROM python:3.11-slim

WORKDIR /app

# Cài đặt các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Sao chép các file cần thiết
COPY python_adk/requirements.txt ./python_adk/
COPY python_adk/ ./python_adk/

# Cài đặt các dependencies Python
RUN pip install --no-cache-dir -r python_adk/requirements.txt
RUN pip install --no-cache-dir google-adk google-generativeai
RUN pip install --no-cache-dir git+https://github.com/google/adk-python.git

# Thiết lập biến môi trường
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO
ENV API_KEY=production_key
ENV API_KEY_HEADER=X-API-Key
ENV DEFAULT_MODEL=gemini-pro
ENV ROOT_AGENT_MODEL=gemini-pro
ENV BATCUCLINH_SO_AGENT_MODEL=gemini-pro

# Kiểm tra cài đặt
RUN python -c "import adk; print('ADK đã được cài đặt thành công!')"

# Mở cổng
EXPOSE 10000

# Lệnh khởi động
CMD ["uvicorn", "python_adk.asgi:application", "--host", "0.0.0.0", "--port", "10000"] 