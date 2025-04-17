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

class PhoneRequest(BaseModel):
    phone_number: str

class CCCDRequest(BaseModel):
    cccd_number: str

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

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Phong Thủy Số ADK Service is running", "version": "0.1.0"}

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

# Bát Cục Linh Số - Phone Analysis Endpoint
@app.post("/api/batcuclinh_so/phone")
async def analyze_phone(request: PhoneRequest):
    """Phân tích số điện thoại theo phương pháp Bát Cục Linh Số"""
    try:
        logger.info(f"Received phone analysis request: {request.phone_number}")
        
        # Chuẩn hóa số điện thoại
        phone = request.phone_number.replace('+84', '0').strip()
        
        # Tính tổng các chữ số
        sum_value = sum(int(digit) for digit in phone if digit.isdigit())
        
        # Rút gọn tổng thành số có 1 chữ số
        reduced_sum = sum_value
        while reduced_sum > 9:
            reduced_sum = sum(int(digit) for digit in str(reduced_sum))
        
        # Xác định ngũ hành
        element_map = {
            1: "Kim", 2: "Thủy", 3: "Mộc", 
            4: "Mộc", 5: "Thổ", 6: "Kim",
            7: "Kim", 8: "Thổ", 9: "Hỏa"
        }
        element = element_map.get(reduced_sum, "Không xác định")
        
        # TODO: Implement more detailed analysis logic here
        
        return {
            "success": True,
            "phoneNumber": phone,
            "totalValue": reduced_sum,
            "element": element,
            "analysis": f"""
            Phân tích số điện thoại {phone}:
            
            Tổng giá trị: {sum_value} (Rút gọn: {reduced_sum})
            Ngũ hành: {element}
            
            Đây là kết quả phân tích từ Python ADK.
            """
        }
    except Exception as e:
        logger.error(f"Error analyzing phone number: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Bát Cục Linh Số - CCCD Analysis Endpoint
@app.post("/api/batcuclinh_so/cccd")
async def analyze_cccd(request: CCCDRequest):
    """Phân tích CCCD/CMND theo phương pháp Bát Cục Linh Số"""
    try:
        logger.info(f"Received CCCD analysis request: {request.cccd_number}")
        
        # Chuẩn hóa số CCCD
        cccd = request.cccd_number.strip()
        
        # Tính tổng các chữ số
        sum_value = sum(int(digit) for digit in cccd if digit.isdigit())
        
        # Rút gọn tổng thành số có 1 chữ số
        reduced_sum = sum_value
        while reduced_sum > 9:
            reduced_sum = sum(int(digit) for digit in str(reduced_sum))
        
        # Xác định ngũ hành
        element_map = {
            1: "Kim", 2: "Thủy", 3: "Mộc", 
            4: "Mộc", 5: "Thổ", 6: "Kim",
            7: "Kim", 8: "Thổ", 9: "Hỏa"
        }
        element = element_map.get(reduced_sum, "Không xác định")
        
        # Phân tích thông tin CCCD
        info = {}
        if len(cccd) == 12:  # CCCD 12 số
            province_code = int(cccd[:3])
            gender_code = int(cccd[3])
            birth_year = cccd[4:6]
            
            # Xác định giới tính và thế kỷ sinh
            gender = "Nam" if gender_code % 2 == 0 else "Nữ"
            century = "19"  # Mặc định thế kỷ 20
            
            if gender_code in [0, 1]:
                century = "19"
            elif gender_code in [2, 3]:
                century = "20"
            elif gender_code in [4, 5]:
                century = "21"
            
            info = {
                "type": "CCCD",
                "provinceCode": province_code,
                "gender": gender,
                "birthYear": f"{century}{birth_year}",
                "randomCode": cccd[6:]
            }
        elif len(cccd) == 9:  # CMND 9 số
            info = {
                "type": "CMND",
                "note": "CMND 9 số không có cấu trúc cố định để trích xuất thông tin chi tiết"
            }
        
        # TODO: Implement more detailed analysis logic here
        
        return {
            "success": True,
            "cccdNumber": cccd,
            "totalValue": reduced_sum,
            "element": element,
            "info": info,
            "analysis": f"""
            Phân tích số {info.get('type', 'CCCD/CMND')}: {cccd}
            
            Tổng giá trị: {sum_value} (Rút gọn: {reduced_sum})
            Ngũ hành: {element}
            
            {f"Thông tin cá nhân:" if info.get('type') == 'CCCD' else ''}
            {f"- Mã tỉnh: {info.get('provinceCode')}" if info.get('type') == 'CCCD' else ''}
            {f"- Giới tính: {info.get('gender')}" if info.get('type') == 'CCCD' else ''}
            {f"- Năm sinh: {info.get('birthYear')}" if info.get('type') == 'CCCD' else ''}
            {f"- Mã ngẫu nhiên: {info.get('randomCode')}" if info.get('type') == 'CCCD' else ''}
            
            Đây là kết quả phân tích từ Python ADK.
            """
        }
    except Exception as e:
        logger.error(f"Error analyzing CCCD/CMND: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Khởi động server khi chạy trực tiếp
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
else:
    # Khi được import bởi uvicorn, sử dụng app object
    pass 