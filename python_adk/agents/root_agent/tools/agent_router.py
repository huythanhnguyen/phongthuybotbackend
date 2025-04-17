"""
Agent Router Tool - Công cụ chuyển hướng yêu cầu đến agent phù hợp

Tool này chuyển hướng yêu cầu từ Root Agent đến các Expert Agent
phù hợp dựa trên phân tích ý định và context.
"""

import logging
from typing import Dict, Any, List, Optional
from enum import Enum

# Google ADK imports
from adk.core.tool import Tool

# Local imports
from .intent_classifier import AgentType


class AgentRouter(Tool):
    """Tool chuyển hướng yêu cầu đến agent phù hợp"""
    
    def __init__(self):
        """Khởi tạo Agent Router Tool"""
        super().__init__(
            name="agent_router",
            description="Chuyển hướng yêu cầu đến agent phù hợp",
            parameters=[
                {
                    "name": "agent_type",
                    "type": "string",
                    "description": "Loại agent cần chuyển hướng đến",
                    "required": True
                },
                {
                    "name": "request",
                    "type": "string",
                    "description": "Nội dung yêu cầu cần chuyển hướng",
                    "required": True
                },
                {
                    "name": "session_id",
                    "type": "string",
                    "description": "ID của phiên trò chuyện",
                    "required": True
                },
                {
                    "name": "context",
                    "type": "object",
                    "description": "Context của cuộc trò chuyện",
                    "required": False
                }
            ],
            returns={
                "type": "object",
                "description": "Kết quả chuyển hướng yêu cầu",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Trạng thái thành công"
                    },
                    "agent_type": {
                        "type": "string",
                        "description": "Loại agent đã chuyển hướng đến"
                    },
                    "response": {
                        "type": "string",
                        "description": "Phản hồi từ agent (nếu có)"
                    },
                    "error": {
                        "type": "string",
                        "description": "Thông báo lỗi nếu có"
                    }
                }
            }
        )
        
        # Khởi tạo logger
        self.logger = logging.getLogger("AgentRouter")
        
        # Các agent đã đăng ký (sẽ được cập nhật bởi Root Agent)
        self.registered_agents = {}
    
    def register_agent(self, agent_type: str, agent: Any) -> None:
        """Đăng ký agent với router
        
        Args:
            agent_type: Loại agent
            agent: Instance của agent
        """
        self.registered_agents[agent_type] = agent
        self.logger.info(f"Đã đăng ký {agent_type} Agent với Router")
    
    async def route_request(self, agent_type: str, request: str, session_id: str, 
                           context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Chuyển hướng yêu cầu đến agent phù hợp
        
        Args:
            agent_type: Loại agent cần chuyển hướng đến
            request: Nội dung yêu cầu cần chuyển hướng
            session_id: ID của phiên trò chuyện
            context: Context của cuộc trò chuyện
            
        Returns:
            Dict[str, Any]: Kết quả của việc chuyển hướng
        """
        # Kiểm tra xem agent có được đăng ký không
        if agent_type not in self.registered_agents:
            return {
                "success": False,
                "error": f"Agent loại {agent_type} không được tìm thấy hoặc chưa được đăng ký"
            }
        
        try:
            self.logger.info(f"Đang chuyển hướng yêu cầu đến {agent_type} Agent")
            
            # Lấy agent từ danh sách đã đăng ký
            agent = self.registered_agents[agent_type]
            
            # Gọi agent xử lý yêu cầu
            result = await agent.process_request(request, session_id, context)
            
            return {
                "success": True,
                "agent_type": agent_type,
                "response": result.get("response", ""),
                "data": result
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi khi chuyển hướng yêu cầu đến {agent_type} Agent: {str(e)}")
            return {
                "success": False,
                "agent_type": agent_type,
                "error": f"Lỗi khi chuyển hướng yêu cầu: {str(e)}"
            }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Thực thi tool với tham số từ ADK
        
        Args:
            **kwargs: Tham số, bao gồm agent_type, request, session_id và context
            
        Returns:
            Dict[str, Any]: Kết quả của việc chuyển hướng
        """
        agent_type = kwargs.get("agent_type", "")
        request = kwargs.get("request", "")
        session_id = kwargs.get("session_id", "")
        context = kwargs.get("context", {})
        
        if not agent_type:
            return {
                "success": False,
                "error": "Thiếu tham số agent_type"
            }
        
        if not request:
            return {
                "success": False,
                "error": "Thiếu tham số request"
            }
        
        if not session_id:
            return {
                "success": False,
                "error": "Thiếu tham số session_id"
            }
        
        return await self.route_request(agent_type, request, session_id, context) 