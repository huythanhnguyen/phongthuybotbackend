"""
Entry point cho FastAPI server, cung cấp API endpoints để tương tác với các agents
"""

import os
import json
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
from dotenv import load_dotenv
import logging
from pydantic import BaseModel

# Tải biến môi trường
load_dotenv()

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Model cho request
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}
    stream: Optional[bool] = False

class QueryRequest(BaseModel):
    query: str
    agent_type: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

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

# Endpoint chat
@app.post("/chat")
async def chat(request: ChatRequest):
    """Xử lý tin nhắn chat từ user"""
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")
        
        # TODO: Implement actual agent processing logic here
        # Placeholder response
        response = {
            "success": True,
            "response": f"Phân tích: {request.message}",
            "agent_type": "batcuclinh_so",
            "session_id": request.session_id
        }
        
        return response
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint chat stream
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Xử lý tin nhắn chat từ user với response dạng stream"""
    try:
        logger.info(f"Received streaming chat request: {request.message[:50]}...")
        
        # Define the streaming response generator
        async def generate_stream():
            # Placeholder stream response - in a real implementation, this would
            # yield chunks as they become available from the agent
            chunks = [
                f"Phân tích tin nhắn",
                f" \"{request.message}\":",
                "\n\nĐây là",
                " phản hồi",
                " từ Python ADK",
                " dạng stream."
            ]
            
            for chunk in chunks:
                # Format each chunk as a server-sent event
                data = json.dumps({"type": "chunk", "content": chunk})
                yield f"data: {data}\n\n"
                
                # Simulate some processing time
                import asyncio
                await asyncio.sleep(0.1)
            
            # Send completion event
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            
        # Return a streaming response
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream"
        )
    except Exception as e:
        logger.error(f"Error processing streaming request: {str(e)}")
        # For streaming errors, we need to return them in the SSE format
        async def error_stream():
            error_data = json.dumps({"type": "error", "error": str(e)})
            yield f"data: {error_data}\n\n"
        
        return StreamingResponse(
            error_stream(),
            media_type="text/event-stream"
        )

# Endpoint query
@app.post("/query")
async def query(request: QueryRequest):
    """Xử lý truy vấn trực tiếp đến một agent cụ thể"""
    try:
        logger.info(f"Received query request for agent {request.agent_type}: {request.query[:50]}...")
        
        # TODO: Implement actual agent-specific processing logic here
        # Placeholder response
        response = {
            "success": True,
            "response": f"Phân tích từ agent {request.agent_type}: {request.query}",
            "agent_type": request.agent_type,
            "session_id": request.session_id
        }
        
        return response
    except Exception as e:
        logger.error(f"Error processing query request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Khởi động server khi chạy trực tiếp
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 