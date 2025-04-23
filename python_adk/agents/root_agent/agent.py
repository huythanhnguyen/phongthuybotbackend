"""
Root Agent Implementation

Triển khai RootAgent - Agent chính điều phối các agent chuyên biệt.
Kết hợp chức năng của BaseAgent và RootAgent để tránh xung đột.
"""

import abc
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Type, Union

# Import Agent từ google.adk.agents
from google.adk.agents import Agent as GeminiAgent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

# Định nghĩa agent_tool để tương thích với code hiện tại
# Sử dụng mẫu registry pattern thủ công
class AgentToolRegistry:
    _registry = {}
    
    @classmethod
    def register(cls, func):
        cls._registry[func.__name__] = func
        return func
    
    @classmethod
    def get_tool(cls, name):
        return cls._registry.get(name)

agent_tool_registry = AgentToolRegistry()
agent_tool = agent_tool_registry.register

# Tạo một annotate_type giả để xử lý vấn đề không tìm thấy module
def annotate_type(f):
    return f

from python_adk.shared_libraries.logger import get_logger
from python_adk.prompt import get_agent_prompt


class AgentType(str, Enum):
    """Các loại agent trong hệ thống"""
    ROOT = "root"
    BATCUCLINH_SO = "batcuclinh_so"
    PAYMENT = "payment"
    USER = "user"


class RootAgent:
    """
    Agent gốc kết hợp với chức năng của BaseAgent.
    Điều phối các agent chuyên biệt và cung cấp các chức năng cơ bản.
    """

    def __init__(self, name: str = "root_agent", model_name: str = "gemini-2.0-flash"):
        """
        Khởi tạo RootAgent
        
        Args:
            name (str): Tên của agent
            model_name (str): Tên model Gemini sử dụng cho agent
        """
        self.name = name
        self.model_name = model_name
        self.instruction = get_agent_prompt(AgentType.ROOT)
        
        # Khởi tạo agent thật từ Google ADK
        self._agent = GeminiAgent(
            name=name,
            model=model_name,
            instruction=self.instruction,
            generate_content_config=GenerateContentConfig(
                temperature=0.2,
                top_p=0.8,
            ),
            after_agent_callback=self._track_request
        )
        
        self.logger = get_logger(f"{self.__class__.__name__}", log_to_file=True)
        self.logger.info(f"Khởi tạo {self.name} với model {model_name}")
        
        # Các thuộc tính mở rộng 
        self.current_context: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        
        # Danh sách các agent con
        self.sub_agents = {}
        
        # Đăng ký các tools
        self._register_tools()
    
    def _track_request(self, agent_state, user_input, agent_response):
        """Callback để theo dõi yêu cầu và phản hồi"""
        self.logger.info(f"Đã nhận yêu cầu: {user_input}")
        self.logger.info(f"Đã phản hồi: {agent_response}")
        
        # Thêm vào lịch sử hội thoại
        self.add_to_history("user", user_input)
        self.add_to_history("assistant", agent_response)
        
        # Cập nhật agent_state nếu cần
        if "conversation_history" not in agent_state:
            agent_state["conversation_history"] = []
        
        agent_state["conversation_history"] = [
            {"role": entry["role"], "content": entry["content"]} 
            for entry in self.conversation_history
        ]
        
        return agent_state
    
    def _register_tools(self) -> None:
        """
        Đăng ký các tools cho Root Agent.
        """
        from python_adk.agents.root_agent.tools.intent_classifier import IntentClassifier
        from python_adk.agents.root_agent.tools.agent_router import AgentRouter
        from python_adk.agents.root_agent.tools.context_tracker import ContextTracker
        from python_adk.agents.root_agent.tools.conversation_manager import ConversationManager
        
        # Khởi tạo các tools
        self.intent_classifier = IntentClassifier()
        self.agent_router = AgentRouter()
        self.context_tracker = ContextTracker()
        self.conversation_manager = ConversationManager()
        
        # Đăng ký tools với agent
        self._agent.register_tool(self.intent_classifier)
        self._agent.register_tool(self.agent_router)
        self._agent.register_tool(self.context_tracker)
        self._agent.register_tool(self.conversation_manager)
    
    def register_agent(self, agent_type: AgentType, agent: Any) -> None:
        """
        Đăng ký một agent con với RootAgent
        
        Args:
            agent_type (AgentType): Loại agent
            agent (Any): Instance của agent
        """
        self.sub_agents[agent_type] = agent
        
        # Đăng ký agent với router
        if hasattr(self, 'agent_router'):
            self.agent_router.register_agent(agent_type, agent)
        
        self.logger.info(f"Đã đăng ký {agent_type} Agent")
    
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
    def invoke(self, user_message: str) -> str:
        """
        Xử lý tin nhắn từ người dùng, sử dụng GeminiAgent thực tế
        
        Args:
            user_message (str): Tin nhắn của người dùng
            
        Returns:
            str: Phản hồi của agent
        """
        self.logger.info(f"Nhận tin nhắn: {user_message}")
        
        # Sử dụng phương thức invoke từ agent thật
        try:
            response = self._agent.invoke(user_message)
        except Exception as e:
            self.logger.error(f"Lỗi khi gọi GeminiAgent.invoke: {e}")
            response = f"Đã xảy ra lỗi: {str(e)}"
        
        return response
    
    def process_message(self, user_message: str) -> str:
        """
        Xử lý tin nhắn và trả về phản hồi. Phương thức này
        được sử dụng bởi các agent khác khi gọi đến Root Agent.
        
        Args:
            user_message (str): Tin nhắn của người dùng
            
        Returns:
            str: Phản hồi của agent
        """
        return self.invoke(user_message)
    
    def run(self, user_message: str) -> str:
        """
        Tương tự invoke nhưng tên hàm tương thích với code cũ
        """
        return self.invoke(user_message)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


# Tạo instance của RootAgent để sử dụng ở nơi khác
root_agent = RootAgent() 