"""
Main entry point for the Phong Thủy Số API
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import os
from dotenv import load_dotenv

# Import Google ADK components
from google.adk.agents import LlmAgent, BaseAgent
from google.adk.tools import FunctionTool

# Import local components
from python_adk.agents.batcuclinh_so_agent.agent import BatCucLinhSoAgent
from python_adk.agents.batcuclinh_so_agent.tools.phone_analyzer import phone_analyzer_tool, phone_analyzer
from python_adk.agents.batcuclinh_so_agent.tools.cccd_analyzer import cccd_analyzer_tool, cccd_analyzer
from python_adk.agents.batcuclinh_so_agent.tools.password_analyzer import password_analyzer_tool, password_analyzer
from python_adk.agents.batcuclinh_so_agent.tools.bank_account_analyzer import bank_account_analyzer_tool, bank_account_analyzer
from python_adk.agents.batcuclinh_so_agent.tools.bank_account_suggester import bank_account_suggester_tool, bank_account_suggester

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("API_KEY", "render_production_key")
API_KEY_HEADER = os.getenv("API_KEY_HEADER", "X-API-Key")

# Initialize FastAPI app
app = FastAPI(
    title="Phong Thủy Số API",
    description="API for analyzing phone numbers and CCCD numbers using Bát Cục Linh Số method",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
agent = BatCucLinhSoAgent(
    name="bat_cuc_linh_so_agent",
    description="Agent for analyzing phone numbers and CCCD numbers using Bát Cục Linh Số method",
    tools=[
        phone_analyzer_tool, 
        cccd_analyzer_tool,
        password_analyzer_tool,
        bank_account_analyzer_tool,
        bank_account_suggester_tool
    ]
)

# API Key middleware
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    # Skip API key check for health check and documentation
    if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)
    
    # Check API key
    api_key = request.headers.get(API_KEY_HEADER)
    if not api_key or api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid API key"}
        )
    
    return await call_next(request)

# Define request models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PhoneAnalysisRequest(BaseModel):
    phone_number: str
    purpose: Optional[str] = None

class CCCDAnalysisRequest(BaseModel):
    cccd_number: str

class PasswordAnalysisRequest(BaseModel):
    password: str

class BankAccountAnalysisRequest(BaseModel):
    account_number: str

class BankAccountSuggestionRequest(BaseModel):
    bank_code: str
    prefix: Optional[str] = None
    length: Optional[int] = None
    purpose: str = "personal"

# Define response models
class ChatResponse(BaseModel):
    success: bool
    message: str
    response: str
    agent_type: str

class AnalysisResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = None

# API endpoints
@app.get("/")
async def root():
    return {
        "name": "Phong Thủy Số API",
        "version": "1.0.0",
        "description": "API for analyzing phone numbers and CCCD numbers using Bát Cục Linh Số method"
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Process the message using the agent
        response = await agent.process_message(request.message)
        return {
            "success": True,
            "message": "Message processed successfully",
            "response": response,
            "agent_type": "bat_cuc_linh_so_agent"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/phone")
async def analyze_phone(request: PhoneAnalysisRequest):
    try:
        result = phone_analyzer(
            phone_number=request.phone_number,
            purpose=request.purpose
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/cccd")
async def analyze_cccd(request: CCCDAnalysisRequest):
    try:
        result = cccd_analyzer(
            cccd_number=request.cccd_number
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/password")
async def analyze_password(request: PasswordAnalysisRequest):
    try:
        result = password_analyzer(
            password=request.password
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/bank-account")
async def analyze_bank_account(request: BankAccountAnalysisRequest):
    try:
        result = bank_account_analyzer(
            account_number=request.account_number
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/suggest/bank-account")
async def suggest_bank_account(request: BankAccountSuggestionRequest):
    try:
        result = bank_account_suggester(
            bank_code=request.bank_code,
            prefix=request.prefix,
            length=request.length,
            purpose=request.purpose
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the server
if __name__ == "__main__":
    # Sử dụng biến môi trường PORT nếu có, mặc định là 5000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port) 
