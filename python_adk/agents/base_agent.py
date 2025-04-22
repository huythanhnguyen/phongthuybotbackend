"""
Base Agent Module

Module cung cấp lớp cơ sở cho tất cả các agent trong hệ thống.
"""

import abc
from typing import Any, Dict, List, Optional, Set, Type, Union

from google.adk.agents import Agent as GeminiAgent
from google.adk.tools.agent_tool import agent_tool_registry
from google.adk.type_inference import annotate_type

from python_adk.shared_libraries.logger import get_logger


class BaseAgent(GeminiAgent):
    """
    Lớp cơ sở cho tất cả các agent trong hệ thống Phong Thủy Số
    """

    def __init__(self, system_prompt: str, model_name: str = "gemini-1.5-pro"):
        """
        Khởi tạo BaseAgent
        
        Args:
            system_prompt (str): System prompt cho agent
            model_name (str): Tên model Gemini sử dụng cho agent
        """
        super().__init__(system_prompt=system_prompt, model=model_name)
        
        self.logger = get_logger(f"{self.__class__.__name__}", log_to_file=True)
        self.logger.info(f"Khởi tạo {self.__class__.__name__} với model {model_name}")
        
        # Các thuộc tính mở rộng 
        self.current_context: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        
        # Đăng ký các tools
        self._register_tools()
    
    @abc.abstractmethod
    def _register_tools(self) -> None:
        """
        Đăng ký các tools cho agent.
        Cần được override trong các lớp con.
        """
        pass
    
    def update_context(self, key: str, value: Any) -> None:
        """
        Cập nhật context của agent
        
        Args:
            key (str): Khóa của context
            value (Any): Giá trị cần lưu
        """
        self.current_context[key] = value
        self.logger.debug(f"Cập nhật context: {key} = {value}")
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Lấy giá trị từ context
        
        Args:
            key (str): Khóa cần lấy
            default (Any, optional): Giá trị mặc định nếu không tìm thấy
            
        Returns:
            Any: Giá trị tương ứng với khóa hoặc giá trị mặc định
        """
        return self.current_context.get(key, default)
    
    def add_to_history(self, role: str, content: str) -> None:
        """
        Thêm một message vào lịch sử hội thoại
        
        Args:
            role (str): Vai trò của người gửi ('user' hoặc 'assistant')
            content (str): Nội dung tin nhắn
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def clear_history(self) -> None:
        """Xóa lịch sử hội thoại"""
        self.conversation_history = []
        self.logger.info("Đã xóa lịch sử hội thoại")
    
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
        
        # Sử dụng phương thức predict của parent class (GeminiAgent)
        response = super().predict(user_message)
        
        self.add_to_history("assistant", response)
        self.logger.info(f"Phản hồi: {response}")
        
        return response
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}" 