"""
Payment Agent Implementation

Triển khai PaymentAgent - Agent xử lý thanh toán.
"""

from typing import Any, Dict

from google.adk.agents import Agent as GeminiAgent
from python_adk.agents.root_agent.agent import AgentType
from python_adk.prompt import get_agent_prompt

# Tạo một agent giả đơn giản để khắc phục lỗi import
class PaymentAgent:
    """
    Payment Agent - Agent giả đơn giản để xử lý thanh toán
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash", name: str = "payment_agent"):
        """
        Khởi tạo Payment Agent
        
        Args:
            model_name (str): Tên model sử dụng cho agent
            name (str): Tên của agent
        """
        self.name = name
        self.model_name = model_name
        self.instruction = get_agent_prompt(AgentType.PAYMENT)
        
        # Khởi tạo agent thật từ Google ADK
        self._agent = GeminiAgent(
            name=name,
            model=model_name,
            instruction=self.instruction
        )

    def invoke(self, user_message: str) -> str:
        """
        Xử lý tin nhắn từ người dùng
        
        Args:
            user_message (str): Tin nhắn của người dùng
            
        Returns:
            str: Phản hồi của agent
        """
        return "Tính năng thanh toán chưa được triển khai."

# Tạo instance của PaymentAgent
payment_agent = PaymentAgent() 