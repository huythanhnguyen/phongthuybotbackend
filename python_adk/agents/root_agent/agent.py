"""
Root Agent - Điều phối các yêu cầu đến các agent chuyên biệt

Root Agent đóng vai trò như một điều phối viên chính, phân tích ý định 
của người dùng và chuyển hướng đến các agent chuyên biệt.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from enum import Enum

# Google ADK imports
from google.adk.agents import Agent
from google.adk.agents import Builder as AgentBuilder
from google.adk.models.lite_llm import LiteLlm as LLMGenerator
from google.adk.contexts import ContextManager

# A2A Protocol imports
from python_adk.a2a.protocol import Task, Message, Artifact, Part, TaskStatus, Role, PartType

# Local imports
from .tools.intent_classifier import IntentClassifier
from .tools.conversation_manager import ConversationManager
from .tools.context_tracker import ContextTracker
from .tools.agent_router import AgentRouter


class AgentType(str, Enum):
    """Các loại agent được hỗ trợ trong hệ thống"""
    BAT_CUC_LINH_SO = "batcuclinh_so"
    PAYMENT = "payment"
    USER = "user"
    AUTH = "auth"
    UNKNOWN = "unknown"


class RootAgent:
    """Root Agent điều phối yêu cầu đến các agent chuyên biệt"""

    def __init__(self):
        """Khởi tạo Root Agent"""
        # Khởi tạo logger
        self.logger = logging.getLogger("RootAgent")
        
        # Khởi tạo các tools
        self.intent_classifier = IntentClassifier()
        self.conversation_manager = ConversationManager()
        self.context_tracker = ContextTracker()
        self.agent_router = AgentRouter()
        
        # State lưu trữ sessions
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        # Khởi tạo agent với Google ADK
        model_name = os.environ.get("ROOT_AGENT_MODEL", "gemini-pro")
        self.agent: Agent = self._build_agent(model_name)
        
        # Các expert agents được đăng ký
        self.expert_agents = {}
        
        self.logger.info("Root Agent đã được khởi tạo")
    
    def _build_agent(self, model_name: str) -> Agent:
        """Xây dựng agent sử dụng Google ADK
        
        Args:
            model_name: Tên của model LLM
            
        Returns:
            Agent: Agent được xây dựng
        """
        # Đọc hệ thống prompt từ file
        system_prompt = self._load_system_prompt()
        
        # Tạo generator cho agent
        generator = LLMGenerator(name="root-generator", model=model_name)
        
        # Xây dựng agent
        agent = (
            AgentBuilder(name="root-agent")
            .with_system_prompt(system_prompt)
            .with_generator(generator)
            .with_tools([
                self.intent_classifier,
                self.conversation_manager,
                self.context_tracker,
                self.agent_router
            ])
            .build()
        )
        
        return agent
    
    def _load_system_prompt(self) -> str:
        """Đọc hệ thống prompt từ file
        
        Returns:
            str: Nội dung prompt
        """
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            # Fallback prompt nếu không tìm thấy file
            return """
            Bạn là Root Agent cho hệ thống Phong Thủy Số, có nhiệm vụ điều phối yêu cầu 
            của người dùng đến các agent chuyên biệt. Dựa vào nội dung của tin nhắn, 
            bạn cần phân tích ý định người dùng và chuyển đến agent phù hợp.
            
            Các agent chuyên biệt bao gồm:
            - BatCucLinhSo Agent: Phân tích số điện thoại, CCCD, STK ngân hàng theo phương pháp Bát Cục Linh Số
            - Payment Agent: Xử lý các giao dịch thanh toán
            - User Agent: Quản lý thông tin người dùng và API keys
            
            Hãy xác định agent phù hợp dựa trên nội dung tin nhắn và chuyển yêu cầu đến agent đó.
            """
    
    def register_expert_agent(self, agent_type: AgentType, agent: Any) -> None:
        """Đăng ký Expert Agent với Root Agent
        
        Args:
            agent_type: Loại agent
            agent: Instance của Expert Agent
        """
        self.expert_agents[agent_type] = agent
        self.logger.info(f"Đã đăng ký {agent_type} Agent")
    
    async def process_request(self, user_request: str, session_id: Optional[str] = None, 
                             user_id: Optional[str] = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Xử lý yêu cầu từ người dùng
        
        Args:
            user_request: Yêu cầu của người dùng
            session_id: ID của phiên làm việc
            user_id: ID của người dùng
            metadata: Metadata bổ sung
            
        Returns:
            Dict[str, Any]: Kết quả xử lý
        """
        # Khởi tạo session nếu chưa có
        if not session_id or session_id not in self.sessions:
            session_id = f"session-{len(self.sessions) + 1}"
            self.sessions[session_id] = {
                "user_id": user_id,
                "history": [],
                "context": {},
                "metadata": metadata or {},
                "current_agent": None
            }
        
        # Tạo Task và Message theo A2A Protocol
        task = Task(session_id=session_id, status=TaskStatus.SUBMITTED)
        message = Message(role=Role.USER, parts=[Part(type=PartType.TEXT, text=user_request)])
        
        # Thêm yêu cầu vào lịch sử
        self.sessions[session_id]["history"].append({
            "role": "user",
            "content": user_request,
            "timestamp": task.created_at.isoformat()
        })
        
        try:
            # Phân tích ý định của người dùng
            intent_result = await self.intent_classifier.analyze_intent(user_request)
            agent_type = intent_result["agent_type"]
            
            # Cập nhật context
            self.context_tracker.update_context(self.sessions[session_id]["context"], user_request, intent_result)
            
            # Kiểm tra xem có expert agent phù hợp không
            if agent_type not in self.expert_agents:
                return self._handle_error("Không tìm thấy agent phù hợp", task)
            
            # Cập nhật thông tin agent hiện tại
            self.sessions[session_id]["current_agent"] = agent_type
            
            # Chuyển yêu cầu đến expert agent
            self.logger.info(f"Chuyển yêu cầu đến {agent_type} Agent")
            expert_agent = self.expert_agents[agent_type]
            
            # Cập nhật trạng thái task
            task.update_status(TaskStatus.RUNNING)
            
            # Gọi expert agent xử lý task
            result = await expert_agent.process_task(task, message, {
                "user_id": user_id,
                "context": self.sessions[session_id]["context"],
                "metadata": metadata
            })
            
            # Thêm phản hồi vào lịch sử
            response_text = ""
            if result["artifacts"] and len(result["artifacts"]) > 0:
                artifact = result["artifacts"][0]
                if artifact.parts and len(artifact.parts) > 0:
                    response_text = artifact.parts[0].text
            
            self.sessions[session_id]["history"].append({
                "role": "assistant",
                "content": response_text,
                "timestamp": task.updated_at.isoformat()
            })
            
            # Trả về kết quả
            return {
                "success": True,
                "task_id": task.id,
                "session_id": session_id,
                "response": response_text,
                "agent_type": agent_type
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi xử lý yêu cầu: {str(e)}")
            return self._handle_error(str(e), task)
    
    def _handle_error(self, error_message: str, task: Task) -> Dict[str, Any]:
        """Xử lý lỗi và trả về phản hồi lỗi
        
        Args:
            error_message: Thông báo lỗi
            task: Task A2A
            
        Returns:
            Dict[str, Any]: Phản hồi lỗi
        """
        task.update_status(TaskStatus.ERROR, error_message)
        
        error_artifact = Artifact(
            type="error",
            parts=[Part(type=PartType.TEXT, text=f"Rất tiếc, đã xảy ra lỗi: {error_message}. Vui lòng thử lại sau.")]
        )
        
        task.add_artifact(error_artifact)
        
        return {
            "success": False,
            "task_id": task.id,
            "session_id": task.session_id,
            "error": error_message,
            "response": f"Rất tiếc, đã xảy ra lỗi: {error_message}. Vui lòng thử lại sau."
        } 