"""
Entry point cho FastAPI server, cung cấp API endpoints để tương tác với các agents
"""

import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import logging

# Tải biến môi trường
load_dotenv()

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Khởi tạo FastAPI app
app = FastAPI(
    title="Phong Thủy Số ADK Service",
    description="API service cho Phong Thủy Số sử dụng Google ADK",
    version="0.1.0",
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Thay bằng domain thực tế trong production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Kiểm tra trạng thái hoạt động của service"""
    return {"status": "ok", "service": "Phong Thủy Số ADK Service"}

# Endpoint chat cơ bản (sẽ được mở rộng sau)
@app.post("/chat")
async def chat():
    """Endpoint chat tạm thời, sẽ được triển khai đầy đủ sau"""
    return {"message": "Chat endpoint coming soon"}

# Khởi động server khi chạy trực tiếp
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 