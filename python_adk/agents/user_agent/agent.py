"""
User Agent Implementation

Triển khai UserAgent - Agent quản lý thông tin người dùng.
"""

from typing import Any, Dict

from python_adk.agents.base_agent import BaseAgent
from python_adk.agents.root_agent.agent import AgentType
from python_adk.prompt import get_agent_prompt

# Tạo một agent kế thừa từ BaseAgent
class UserAgent(BaseAgent):
    """
    User Agent - Agent quản lý thông tin người dùng
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash", name: str = "user_agent"):
        """
        Khởi tạo User Agent
        
        Args:
            model_name (str): Tên model sử dụng cho agent
            name (str): Tên của agent
        """
        # Lấy prompt làm instruction
        instruction = get_agent_prompt(AgentType.USER)
        
        # Gọi constructor của BaseAgent
        super().__init__(
            name=name,
            model_name=model_name,
            instruction=instruction
        )
    
    def _register_tools(self) -> None:
        """Đăng ký các tools cho User Agent"""
        # Chưa có tools đặc thù cho user
        pass

# Tạo instance của UserAgent
user_agent = UserAgent() 