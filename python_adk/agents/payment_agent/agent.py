"""
Payment Agent - Xử lý thanh toán và quản lý gói dịch vụ

Payment Agent đóng vai trò xử lý các giao dịch thanh toán, nâng cấp tài khoản,
và kiểm tra quota.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

# Google ADK imports
from google.adk.core.agent import Agent
from google.adk.core.agent_builder import AgentBuilder
from google.adk.generators.llm import LLMGenerator
from google.adk.managers.context import ContextManager

# A2A Protocol imports
from python_adk.a2a.protocol import Task, Message, Artifact, Part, TaskStatus, Role, PartType

# Tools imports
from .tools.payment_processor import PaymentProcessor


class PaymentAgent:
    """Payment Agent xử lý thanh toán và quản lý gói dịch vụ"""

    def __init__(self):
        """Khởi tạo Payment Agent"""
        # Khởi tạo logger
        self.logger = logging.getLogger("PaymentAgent")
        
        # Khởi tạo các tools
        self.payment_processor = PaymentProcessor()
        
        # Khởi tạo agent với Google ADK
        model_name = os.environ.get("PAYMENT_AGENT_MODEL", "gemini-pro")
        self.agent: Agent = self._build_agent(model_name)
        
        self.logger.info("Payment Agent đã được khởi tạo")
    
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
        generator = LLMGenerator(name="payment-generator", model=model_name)
        
        # Xây dựng agent
        agent = (
            AgentBuilder(name="payment-agent")
            .with_system_prompt(system_prompt)
            .with_generator(generator)
            .with_tools([
                self.payment_processor
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
            Bạn là Payment Agent cho hệ thống Phong Thủy Số, có nhiệm vụ xử lý thanh toán và quản lý gói dịch vụ.
            Bạn có thể xử lý các yêu cầu về tạo thanh toán, xác thực thanh toán, kiểm tra gói dịch vụ, và lịch sử thanh toán.
            
            Hãy sử dụng các công cụ có sẵn để thực hiện các nhiệm vụ này một cách chính xác và hiệu quả.
            Tương tác với người dùng bằng cách trả lời các yêu cầu liên quan đến thanh toán và gói dịch vụ.
            
            Đảm bảo tính minh bạch và chính xác khi xử lý thông tin thanh toán.
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
            if "payment_code" in metadata:
                prompt_parts.append(f"Mã thanh toán: {metadata['payment_code']}")
            if "plan_id" in metadata:
                prompt_parts.append(f"Gói dịch vụ: {metadata['plan_id']}")
            if "action" in metadata:
                prompt_parts.append(f"Hành động: {metadata['action']}")
        
        return "\n".join(prompt_parts)
    
    async def get_plans(self) -> Dict[str, Any]:
        """API Helper: Lấy danh sách các gói dịch vụ
        
        Returns:
            Dict[str, Any]: Danh sách gói dịch vụ
        """
        return await self.payment_processor.get_plans()
    
    async def create_payment(self, user_id: str, plan_id: str) -> Dict[str, Any]:
        """API Helper: Tạo yêu cầu thanh toán mới
        
        Args:
            user_id: ID người dùng
            plan_id: ID gói dịch vụ
            
        Returns:
            Dict[str, Any]: Thông tin thanh toán
        """
        return await self.payment_processor.create_payment(user_id, plan_id)
    
    async def verify_payment(self, payment_code: str) -> Dict[str, Any]:
        """API Helper: Xác thực thanh toán
        
        Args:
            payment_code: Mã thanh toán
            
        Returns:
            Dict[str, Any]: Kết quả xác thực
        """
        return await self.payment_processor.verify_payment(payment_code)
    
    async def check_subscription(self, user_id: str) -> Dict[str, Any]:
        """API Helper: Kiểm tra thông tin gói dịch vụ của người dùng
        
        Args:
            user_id: ID người dùng
            
        Returns:
            Dict[str, Any]: Thông tin gói dịch vụ
        """
        return await self.payment_processor.check_subscription(user_id) 