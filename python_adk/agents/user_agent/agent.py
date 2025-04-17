"""
User Agent - Quản lý tài khoản người dùng

User Agent đóng vai trò quản lý thông tin người dùng, bao gồm đăng ký, 
đăng nhập, cập nhật profile, và quản lý API keys.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

# Google ADK imports
from adk.core.agent import Agent
from adk.core.agent_builder import AgentBuilder
from adk.generators.llm import LLMGenerator
from adk.managers.context import ContextManager

# A2A Protocol imports
from python_adk.a2a.protocol import Task, Message, Artifact, Part, TaskStatus, Role, PartType

# Tools imports
from .tools.account_manager import AccountManager
from .tools.api_key_generator import ApiKeyGenerator


class UserAgent:
    """User Agent quản lý tài khoản người dùng"""

    def __init__(self):
        """Khởi tạo User Agent"""
        # Khởi tạo logger
        self.logger = logging.getLogger("UserAgent")
        
        # Khởi tạo các tools
        self.account_manager = AccountManager()
        self.api_key_generator = ApiKeyGenerator()
        
        # Khởi tạo agent với Google ADK
        model_name = os.environ.get("USER_AGENT_MODEL", "gemini-pro")
        self.agent: Agent = self._build_agent(model_name)
        
        self.logger.info("User Agent đã được khởi tạo")
    
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
        generator = LLMGenerator(name="user-generator", model=model_name)
        
        # Xây dựng agent
        agent = (
            AgentBuilder(name="user-agent")
            .with_system_prompt(system_prompt)
            .with_generator(generator)
            .with_tools([
                self.account_manager,
                self.api_key_generator
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
            Bạn là User Agent cho hệ thống Phong Thủy Số, có nhiệm vụ quản lý thông tin người dùng.
            Bạn có thể xử lý các yêu cầu về đăng ký, đăng nhập, cập nhật thông tin, và quản lý API keys.
            
            Hãy sử dụng các công cụ có sẵn để thực hiện các nhiệm vụ này một cách chính xác và hiệu quả.
            Tương tác với người dùng bằng cách trả lời các yêu cầu liên quan đến tài khoản của họ.
            
            Đảm bảo tính bảo mật và chính xác khi xử lý thông tin người dùng.
            """
    
    async def process_task(self, task: Task, message: Message, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Xử lý task từ Root Agent
        
        Args:
            task: Task theo A2A Protocol
            message: Message chứa yêu cầu của người dùng
            context: Context bổ sung
            
        Returns:
            Dict[str, Any]: Kết quả xử lý
        """
        try:
            # Extract nội dung yêu cầu
            user_request = message.parts[0].text if message.parts else ""
            self.logger.info(f"Nhận yêu cầu: {user_request}")
            
            # Parse context
            user_id = context.get("user_id") if context else None
            metadata = context.get("metadata", {}) if context else {}
            
            # Tạo prompt từ yêu cầu và context
            prompt = self._create_prompt(user_request, user_id, metadata)
            
            # Gọi agent xử lý
            response = await self.agent.generate(prompt)
            response_text = response.text
            
            # Cập nhật trạng thái task
            task.update_status(TaskStatus.COMPLETED)
            
            # Tạo artifact chứa kết quả
            result_artifact = Artifact(
                type="result",
                parts=[Part(type=PartType.TEXT, text=response_text)]
            )
            
            # Thêm artifact vào task
            task.add_artifact(result_artifact)
            
            return {
                "success": True,
                "task": task,
                "artifacts": [result_artifact]
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi xử lý task: {str(e)}")
            
            # Cập nhật trạng thái task lỗi
            task.update_status(TaskStatus.ERROR, str(e))
            
            # Tạo artifact chứa thông báo lỗi
            error_artifact = Artifact(
                type="error",
                parts=[Part(type=PartType.TEXT, text=f"Đã xảy ra lỗi: {str(e)}")]
            )
            
            # Thêm artifact vào task
            task.add_artifact(error_artifact)
            
            return {
                "success": False,
                "task": task,
                "artifacts": [error_artifact]
            }
    
    def _create_prompt(self, user_request: str, user_id: Optional[str], metadata: Dict[str, Any]) -> str:
        """Tạo prompt từ yêu cầu và context
        
        Args:
            user_request: Yêu cầu của người dùng
            user_id: ID người dùng
            metadata: Metadata bổ sung
            
        Returns:
            str: Prompt hoàn chỉnh
        """
        prompt_parts = [
            f"Yêu cầu của người dùng: {user_request}",
            ""
        ]
        
        # Thêm thông tin về người dùng nếu có
        if user_id:
            prompt_parts.append(f"ID người dùng: {user_id}")
        
        # Thêm các thông tin quan trọng từ metadata
        if metadata:
            if "token" in metadata:
                prompt_parts.append("Người dùng đã đăng nhập")
            if "api_key" in metadata:
                prompt_parts.append(f"API key: {metadata['api_key']}")
            if "action" in metadata:
                prompt_parts.append(f"Hành động: {metadata['action']}")
        
        return "\n".join(prompt_parts)
    
    async def register_user(self, email: str, password: str, name: str = None, phone: str = None) -> Dict[str, Any]:
        """API Helper: Đăng ký người dùng mới
        
        Args:
            email: Email người dùng
            password: Mật khẩu
            name: Tên người dùng (tùy chọn)
            phone: Số điện thoại (tùy chọn)
            
        Returns:
            Dict[str, Any]: Kết quả đăng ký
        """
        return await self.account_manager.register_user(email, password, name, phone)
    
    async def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """API Helper: Đăng nhập người dùng
        
        Args:
            email: Email người dùng
            password: Mật khẩu
            
        Returns:
            Dict[str, Any]: Kết quả đăng nhập
        """
        return await self.account_manager.login_user(email, password)
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """API Helper: Xác thực token
        
        Args:
            token: JWT token
            
        Returns:
            Dict[str, Any]: Kết quả xác thực
        """
        return await self.account_manager.verify_token(token)
    
    async def generate_api_key(self, user_id: str, name: str, expiry_days: int = None, quota: int = None) -> Dict[str, Any]:
        """API Helper: Tạo API key mới
        
        Args:
            user_id: ID người dùng
            name: Tên API key
            expiry_days: Số ngày hết hạn (tùy chọn)
            quota: Hạn mức sử dụng (tùy chọn)
            
        Returns:
            Dict[str, Any]: Thông tin API key mới
        """
        return await self.api_key_generator.generate_api_key(user_id, name, expiry_days, quota) 