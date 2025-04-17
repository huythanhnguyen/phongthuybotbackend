#!/bin/bash

echo "==> Cài đặt các dependencies"
pip install -r python_adk/requirements.txt

echo "==> Cài đặt trực tiếp Google ADK"
pip install google-adk google-generativeai
pip install git+https://github.com/google/adk-python.git

echo "==> Thiết lập biến môi trường"
export PYTHONPATH=$PYTHONPATH:$(pwd)
export LOG_LEVEL=INFO
export API_KEY=dev_key
export API_KEY_HEADER=X-API-Key
export DEFAULT_MODEL=gemini-pro
export ROOT_AGENT_MODEL=gemini-pro
export BATCUCLINH_SO_AGENT_MODEL=gemini-pro

echo "==> Kiểm tra cài đặt"
python -c "import adk; print('ADK đã được cài đặt thành công!')" || echo "Lỗi: Không thể import adk"

echo "==> Chạy ứng dụng"
uvicorn python_adk.asgi:application --host 0.0.0.0 --port 10000 