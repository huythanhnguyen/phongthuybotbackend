"""
Entry point cho FastAPI server, cung cấp API endpoints để tương tác với các agents
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel

# Tải biến môi trường
load_dotenv()

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Root Agent
from python_adk.agents.root_agent import RootAgent, AgentType

# Specialized Agents
from python_adk.agents.batcuclinh_so_agent import BatCucLinhSoAgent
from python_adk.agents.auth_agent import AuthAgent

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

# Khởi tạo và đăng ký các agents
root_agent = RootAgent()
batcuclinh_so_agent = BatCucLinhSoAgent()
auth_agent = AuthAgent()

# Đăng ký các agents với Root Agent
root_agent.register_expert_agent(AgentType.BAT_CUC_LINH_SO, batcuclinh_so_agent)
root_agent.register_expert_agent("auth", auth_agent)  # Đăng ký auth agent

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
        
        # Xử lý yêu cầu bằng Root Agent
        response = await root_agent.process_request(
            user_request=request.message,
            session_id=request.session_id,
            user_id=request.user_id,
            metadata=request.metadata
        )
        
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
        
        # Lấy agent type
        agent_type = request.agent_type
        if agent_type.lower() == "batcuclinh_so":
            agent_type = AgentType.BAT_CUC_LINH_SO
        
        # Tạo context để gọi Root Agent
        context = {
            "session_id": request.session_id,
            "user_id": request.user_id,
            "metadata": {
                "query": request.query,
                **request.metadata
            }
        }
        
        # Thực hiện truy vấn thông qua Root Agent
        response = await root_agent.process_request(
            user_request=request.query,
            session_id=request.session_id,
            user_id=request.user_id,
            metadata={
                "agent_type": agent_type,
                **request.metadata
            }
        )
        
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
        
        # Kiểm tra độ dài số CCCD
        if not cccd.isdigit() or (len(cccd) != 9 and len(cccd) != 12):
            return {
                "success": False,
                "message": "Số CCCD/CMND không hợp lệ. Vui lòng nhập 9 số (CMND) hoặc 12 số (CCCD)."
            }
        
        # Tính tổng các chữ số
        sum_value = sum(int(digit) for digit in cccd)
        
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
        
        # Phân tích thông tin từ CCCD (chỉ áp dụng cho CCCD 12 số)
        info = {}
        if len(cccd) == 12:
            # Mã tỉnh/thành phố (3 số đầu)
            province_code = cccd[:3]
            province_map = {
                "001": "Hà Nội", "002": "Hà Giang", "004": "Cao Bằng",
                "006": "Bắc Kạn", "008": "Tuyên Quang", "010": "Lào Cai",
                "011": "Điện Biên", "012": "Lai Châu", "014": "Sơn La",
                "015": "Yên Bái", "017": "Hòa Bình", "019": "Thái Nguyên",
                "020": "Lạng Sơn", "022": "Quảng Ninh", "024": "Bắc Giang",
                "025": "Phú Thọ", "026": "Vĩnh Phúc", "027": "Bắc Ninh",
                "030": "Hải Dương", "031": "Hải Phòng", "033": "Hưng Yên",
                "034": "Thái Bình", "035": "Hà Nam", "036": "Nam Định",
                "037": "Ninh Bình", "038": "Thanh Hóa", "040": "Nghệ An",
                "042": "Hà Tĩnh", "044": "Quảng Bình", "045": "Quảng Trị",
                "046": "Thừa Thiên Huế", "048": "Đà Nẵng", "049": "Quảng Nam",
                "051": "Quảng Ngãi", "052": "Bình Định", "054": "Phú Yên",
                "056": "Khánh Hòa", "058": "Ninh Thuận", "060": "Bình Thuận",
                "062": "Kon Tum", "064": "Gia Lai", "066": "Đắk Lắk",
                "067": "Đắk Nông", "068": "Lâm Đồng", "070": "Bình Phước",
                "072": "Tây Ninh", "074": "Bình Dương", "075": "Đồng Nai",
                "077": "Bà Rịa - Vũng Tàu", "079": "Hồ Chí Minh", "080": "Long An",
                "082": "Tiền Giang", "083": "Bến Tre", "084": "Trà Vinh",
                "086": "Vĩnh Long", "087": "Đồng Tháp", "089": "An Giang",
                "091": "Kiên Giang", "092": "Cần Thơ", "093": "Hậu Giang",
                "094": "Sóc Trăng", "095": "Bạc Liêu", "096": "Cà Mau"
            }
            info["province"] = province_map.get(province_code, "Không xác định")
            
            # Mã giới tính và năm sinh (1 số tiếp theo)
            gender_year_code = int(cccd[3])
            if gender_year_code == 0:
                info["gender"] = "Nam"
                info["birth_year"] = "19" + cccd[4:6]
            elif gender_year_code == 1:
                info["gender"] = "Nữ"
                info["birth_year"] = "19" + cccd[4:6]
            elif gender_year_code == 2:
                info["gender"] = "Nam"
                info["birth_year"] = "20" + cccd[4:6]
            elif gender_year_code == 3:
                info["gender"] = "Nữ"
                info["birth_year"] = "20" + cccd[4:6]
            elif gender_year_code == 4:
                info["gender"] = "Nam"
                info["birth_year"] = "21" + cccd[4:6]
            elif gender_year_code == 5:
                info["gender"] = "Nữ"
                info["birth_year"] = "21" + cccd[4:6]
            else:
                info["gender"] = "Không xác định"
                info["birth_year"] = "Không xác định"
            
            # Mã số ngẫu nhiên
            info["random_code"] = cccd[6:]
        
        return {
            "success": True,
            "cccd_number": cccd,
            "totalValue": reduced_sum,
            "element": element,
            "info": info,
            "content": f"""
            Phân tích số CCCD: {cccd}
            
            Tổng số (Lộ số): {reduced_sum} - Ngũ hành: {element}
            
            {f"Thông tin cá nhân:" if info else ""}
            {f"- Tỉnh/Thành phố: {info.get('province')}" if info.get('province') else ""}
            {f"- Giới tính: {info.get('gender')}" if info.get('gender') else ""}
            {f"- Năm sinh: {info.get('birth_year')}" if info.get('birth_year') else ""}
            {f"- Mã ngẫu nhiên: {info.get('random_code')}" if info.get('random_code') else ""}
            
            Đây là kết quả phân tích từ Python ADK.
            """
        }
    except Exception as e:
        logger.error(f"Error analyzing CCCD: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Khởi động server khi chạy trực tiếp
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 