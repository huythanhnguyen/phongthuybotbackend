"""
Root Agent Implementation

Triển khai RootAgent - Agent chính điều phối các agent chuyên biệt.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from google.adk.agent_tools import agent_tool, agent_tool_registry
from google.adk.type_inference import annotate_type

from python_adk.agents.base_agent import BaseAgent
from python_adk.prompt import get_agent_prompt
from python_adk.shared_libraries.logger import get_logger


class AgentType(str, Enum):
    """Các loại agent trong hệ thống"""
    ROOT = "root"
    BATCUCLINH_SO = "batcuclinh_so"
    PAYMENT = "payment"
    USER = "user"


class RootAgent(BaseAgent):
    """
    Root Agent - Agent chính điều phối các yêu cầu đến các agent chuyên biệt
    """
    
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        """
        Khởi tạo Root Agent
        
        Args:
            model_name (str): Tên model sử dụng cho agent
        """
        system_prompt = get_agent_prompt(AgentType.ROOT)
        super().__init__(system_prompt=system_prompt, model_name=model_name)
        
        self.logger = get_logger("RootAgent", log_to_file=True)
        self.agent_registry = {}  # Sẽ được điền bởi AgentRegistry
    
    def _register_tools(self) -> None:
        """Đăng ký các tools cho Root Agent"""
        agent_tool_registry.register(self.intent_classifier)
        agent_tool_registry.register(self.delegate_to_agent)
    
    def register_agent(self, agent_type: AgentType, agent_instance: BaseAgent) -> None:
        """
        Đăng ký một agent vào registry
        
        Args:
            agent_type (AgentType): Loại agent
            agent_instance (BaseAgent): Instance của agent
        """
        self.agent_registry[agent_type] = agent_instance
        self.logger.info(f"Đã đăng ký agent: {agent_type}")
    
    @agent_tool
    @annotate_type
    def intent_classifier(self, user_message: str) -> AgentType:
        """
        Phân loại ý định của người dùng để xác định agent phù hợp
        
        Args:
            user_message (str): Tin nhắn của người dùng
            
        Returns:
            AgentType: Loại agent phù hợp với ý định của người dùng
        """
        # Sử dụng từ khóa để phân loại sơ bộ
        message_lower = user_message.lower()
        
        # Xác định agent phù hợp dựa trên từ khóa
        if any(keyword in message_lower for keyword in ["số điện thoại", "cccd", "tài khoản", "mật khẩu", "phân tích", "đề xuất", "bát cực"]):
            return AgentType.BATCUCLINH_SO
        
        elif any(keyword in message_lower for keyword in ["gói", "thanh toán", "nâng cấp", "quota", "giá", "phí", "mua"]):
            return AgentType.PAYMENT
        
        elif any(keyword in message_lower for keyword in ["đăng ký", "đăng nhập", "tài khoản", "thông tin", "cá nhân", "hồ sơ"]):
            return AgentType.USER
            
        # Mặc định là RootAgent xử lý
        return AgentType.ROOT
    
    @agent_tool
    @annotate_type
    def delegate_to_agent(self, agent_type: AgentType, user_message: str) -> str:
        """
        Chuyển giao yêu cầu đến agent chuyên biệt
        
        Args:
            agent_type (AgentType): Loại agent cần chuyển giao
            user_message (str): Tin nhắn của người dùng
            
        Returns:
            str: Phản hồi từ agent
        """
        if agent_type not in self.agent_registry:
            self.logger.error(f"Không tìm thấy agent: {agent_type}")
            return f"Xin lỗi, tôi không thể xử lý yêu cầu này vì không tìm thấy agent {agent_type}."
        
        agent = self.agent_registry[agent_type]
        self.logger.info(f"Chuyển giao yêu cầu đến {agent_type}: {user_message}")
        
        # Bao gồm context trong tin nhắn nếu cần
        response = agent.run(user_message)
        
        return response
    
    @annotate_type
    def run(self, user_message: str) -> str:
        """
        Xử lý tin nhắn từ người dùng
        
        Args:
            user_message (str): Tin nhắn của người dùng
            
        Returns:
            str: Phản hồi của agent
        """
        self.logger.info(f"Nhận tin nhắn: {user_message}")
        self.add_to_history("user", user_message)
        
        # Sử dụng phương thức predict của parent class (BaseAgent -> GeminiAgent)
        response = super(BaseAgent, self).predict(user_message)
        
        self.add_to_history("assistant", response)
        self.logger.info(f"Phản hồi: {response}")
        
        return response 