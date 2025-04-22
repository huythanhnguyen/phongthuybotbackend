"""
Main entry point for the Phong Thủy Số API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

# Load environment variables
load_dotenv()

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
    tools=[phone_analyzer_tool, cccd_analyzer_tool]
)

# Define request models
class PhoneAnalysisRequest(BaseModel):
    phone_number: str
    purpose: Optional[str] = None

class CCCDAnalysisRequest(BaseModel):
    cccd_number: str

# Define response models
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

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the server
if __name__ == "__main__":
    # Sử dụng biến môi trường PORT nếu có, mặc định là 5000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port) 
