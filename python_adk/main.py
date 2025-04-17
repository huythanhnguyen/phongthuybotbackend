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

# Agents
from python_adk.agents.root_agent import RootAgent, AgentType
from python_adk.agents.batcuclinh_so_agent import BatCucLinhSoAgent
from python_adk.agents.user_agent import UserAgent
from python_adk.agents.payment_agent import PaymentAgent

# Tải biến môi trường
load_dotenv()

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Khởi tạo các agents
root_agent = RootAgent()
batcuclinh_so_agent = BatCucLinhSoAgent()
user_agent = UserAgent()
payment_agent = PaymentAgent()

# Đăng ký các expert agents với Root Agent
root_agent.register_expert_agent(AgentType.BAT_CUC_LINH_SO, batcuclinh_so_agent)
root_agent.register_expert_agent(AgentType.USER, user_agent)
root_agent.register_expert_agent(AgentType.PAYMENT, payment_agent)

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

# User and Payment models
class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class ApiKeyRequest(BaseModel):
    name: str
    expiry_days: Optional[int] = None
    quota: Optional[int] = None

class PaymentRequest(BaseModel):
    plan_id: str

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
        
        # Gọi Root Agent xử lý
        result = await root_agent.process_request(
            request.message,
            request.session_id,
            request.user_id,
            request.metadata
        )
        
        return result
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
            # TODO: Implement actual streaming from agent
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
        
        # Map agent_type to actual agent
        agent_map = {
            "batcuclinh_so": batcuclinh_so_agent,
            "user": user_agent,
            "payment": payment_agent
        }
        
        agent = agent_map.get(request.agent_type)
        if not agent:
            raise HTTPException(status_code=400, detail=f"Unknown agent type: {request.agent_type}")
        
        # Create task and message
        from python_adk.a2a.protocol import Task, Message, Part, Role, PartType, TaskStatus
        task = Task(session_id=request.session_id or "direct-query", status=TaskStatus.SUBMITTED)
        message = Message(role=Role.USER, parts=[Part(type=PartType.TEXT, text=request.query)])
        
        # Call agent directly
        result = await agent.process_task(task, message, {
            "user_id": request.user_id,
            "metadata": request.metadata
        })
        
        # Extract response
        response_text = ""
        if result["artifacts"] and len(result["artifacts"]) > 0:
            artifact = result["artifacts"][0]
            if artifact.parts and len(artifact.parts) > 0:
                response_text = artifact.parts[0].text
        
        return {
            "success": True,
            "response": response_text,
            "agent_type": request.agent_type,
            "session_id": request.session_id
        }
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
                "province_code": province_code,
                "gender": gender,
                "birth_year": f"{century}{birth_year}"
            }
        
        return {
            "success": True,
            "cccdNumber": cccd,
            "totalValue": reduced_sum,
            "element": element,
            "info": info,
            "analysis": f"""
            Phân tích số CCCD {cccd}:
            
            Tổng giá trị: {sum_value} (Rút gọn: {reduced_sum})
            Ngũ hành: {element}
            
            Thông tin: {json.dumps(info, ensure_ascii=False)}
            
            Đây là kết quả phân tích từ Python ADK.
            """
        }
    except Exception as e:
        logger.error(f"Error analyzing CCCD number: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# User Agent API Endpoints
@app.post("/api/user/register")
async def register(request: RegisterRequest):
    """Đăng ký người dùng mới"""
    try:
        logger.info(f"Received register request for email: {request.email}")
        result = await user_agent.register_user(
            request.email, 
            request.password, 
            request.name, 
            request.phone
        )
        return result
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/login")
async def login(request: LoginRequest):
    """Đăng nhập người dùng"""
    try:
        logger.info(f"Received login request for email: {request.email}")
        result = await user_agent.login_user(request.email, request.password)
        return result
    except Exception as e:
        logger.error(f"Error logging in user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/info")
async def user_info(user_id: str):
    """Lấy thông tin người dùng"""
    try:
        logger.info(f"Received user info request for user ID: {user_id}")
        result = await user_agent.account_manager.get_user_info(user_id)
        return result
    except Exception as e:
        logger.error(f"Error getting user info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/apikey")
async def create_api_key(request: ApiKeyRequest, user_id: str):
    """Tạo API key mới"""
    try:
        logger.info(f"Received API key creation request for user ID: {user_id}")
        result = await user_agent.generate_api_key(
            user_id, 
            request.name, 
            request.expiry_days, 
            request.quota
        )
        return result
    except Exception as e:
        logger.error(f"Error creating API key: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/apikey")
async def get_api_keys(user_id: str):
    """Lấy danh sách API keys của người dùng"""
    try:
        logger.info(f"Received API keys request for user ID: {user_id}")
        result = await user_agent.api_key_generator.get_api_keys(user_id)
        return result
    except Exception as e:
        logger.error(f"Error getting API keys: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/user/apikey/{key_id}")
async def revoke_api_key(key_id: str, user_id: str):
    """Thu hồi API key"""
    try:
        logger.info(f"Received API key revocation request for key ID: {key_id}")
        result = await user_agent.api_key_generator.revoke_api_key(key_id, user_id)
        return result
    except Exception as e:
        logger.error(f"Error revoking API key: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Payment Agent API Endpoints
@app.get("/api/payment/plans")
async def get_plans():
    """Lấy danh sách các gói dịch vụ"""
    try:
        logger.info("Received plans request")
        result = await payment_agent.get_plans()
        return result
    except Exception as e:
        logger.error(f"Error getting plans: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/payment/create")
async def create_payment(request: PaymentRequest, user_id: str):
    """Tạo yêu cầu thanh toán mới"""
    try:
        logger.info(f"Received payment creation request for user ID: {user_id}")
        result = await payment_agent.create_payment(user_id, request.plan_id)
        return result
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/payment/verify/{payment_code}")
async def verify_payment(payment_code: str):
    """Xác thực thanh toán"""
    try:
        logger.info(f"Received payment verification request for code: {payment_code}")
        result = await payment_agent.verify_payment(payment_code)
        return result
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/payment/subscription/{user_id}")
async def check_subscription(user_id: str):
    """Kiểm tra thông tin gói dịch vụ của người dùng"""
    try:
        logger.info(f"Received subscription check request for user ID: {user_id}")
        result = await payment_agent.check_subscription(user_id)
        return result
    except Exception as e:
        logger.error(f"Error checking subscription: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/payment/history/{user_id}")
async def payment_history(user_id: str):
    """Lấy lịch sử thanh toán của người dùng"""
    try:
        logger.info(f"Received payment history request for user ID: {user_id}")
        result = await payment_agent.payment_processor.get_payment_history(user_id)
        return result
    except Exception as e:
        logger.error(f"Error getting payment history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Lấy port từ biến môi trường hoặc mặc định 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Khởi động uvicorn server
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 