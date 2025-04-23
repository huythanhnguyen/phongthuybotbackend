"""
Base Agent Module

Module cung cấp lớp cơ sở cho tất cả các agent trong hệ thống.
Lớp này dựa trên RootAgent nhưng chỉ chứa các phương thức cần thiết cho các agent khác.
"""

import abc
from typing import Any, Dict, List, Optional, Set, Type, Union, Callable

# Bỏ import không cần thiết và gây lỗi
# from python_adk.agents.root_agent.agent import agent_tool_registry, agent_tool, annotate_type

# Import Agent từ google.adk.agents
from google.adk.agents import Agent as GeminiAgent
from google.genai.types import GenerateContentConfig # Thêm import nếu cần

from python_adk.shared_libraries.logger import get_logger


class BaseAgent:
    """
    Lớp cơ sở cho tất cả các agent chuyên biệt trong hệ thống Phong Thủy Số.
    Bao bọc GeminiAgent và cung cấp các phương thức tiện ích.
    """

    def __init__(
        self,
        name: str,
        model_name: str = "gemini-2.0-flash",
        instruction: str = None,
        tools: Optional[List[Callable]] = None, # Thêm tham số tools
        generate_content_config: Optional[GenerateContentConfig] = None,
        after_agent_callback: Optional[Callable] = None
    ):
        """
        Khởi tạo BaseAgent
        
        Args:
            name (str): Tên của agent
            model_name (str): Tên model Gemini sử dụng cho agent
            instruction (str): Instruction cho agent
            tools (Optional[List[Callable]]): Danh sách các tool cho agent
            generate_content_config (Optional[GenerateContentConfig]): Cấu hình generation
            after_agent_callback (Optional[Callable]): Callback sau mỗi lượt agent
        """
        self.name = name
        self.model_name = model_name
        self.instruction = instruction
        self.tools = tools or []
        
        # Khởi tạo agent thật từ Google ADK
        self._agent = GeminiAgent(
            name=name,
            model=model_name,
            instruction=instruction,
            tools=self.tools, # Truyền tools vào GeminiAgent
            generate_content_config=generate_content_config, # Truyền config
            after_agent_callback=after_agent_callback # Truyền callback
        )
        
        self.logger = get_logger(f"{self.__class__.__name__}", log_to_file=True)
        self.logger.info(f"Khởi tạo {self.name} với model {model_name} và {len(self.tools)} tools")
        
        # Các thuộc tính mở rộng 
        self.current_context: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
    
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
    
    def process_message(self, user_message: str) -> str:
        """
        Xử lý tin nhắn từ người dùng, sử dụng GeminiAgent thực tế
        
        Args:
            user_message (str): Tin nhắn của người dùng
            
        Returns:
            str: Phản hồi của agent
        """
        self.logger.info(f"Nhận tin nhắn: {user_message}")
        self.add_to_history("user", user_message)
        
        # Sử dụng phương thức invoke từ agent thật
        try:
            response = self._agent.invoke(user_message)
        except Exception as e:
            self.logger.error(f"Lỗi khi gọi GeminiAgent.invoke: {e}")
            response = f"Đã xảy ra lỗi: {str(e)}"
        
        self.add_to_history("assistant", response)
        self.logger.info(f"Phản hồi: {response}")
        
        return response
    
    def invoke(self, user_message: str) -> str:
        """
        Cách gọi thay thế cho process_message
        """
        return self.process_message(user_message)
    
    def run(self, user_message: str) -> str:
        """
        Tương tự invoke nhưng tên hàm tương thích với code cũ
        """
        return self.invoke(user_message)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}" 