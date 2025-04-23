"""
Context Tracker Tool - Công cụ theo dõi ngữ cảnh hội thoại

Tool này quản lý và theo dõi ngữ cảnh (context) của cuộc trò chuyện,
lưu trữ và truy xuất thông tin quan trọng giữa các lượt tương tác.
"""

from typing import Dict, Any, List, Optional
import time
import json
import logging

# Google ADK imports
from google.adk.tools import FunctionTool


class ContextTracker(FunctionTool):
    """Tool theo dõi ngữ cảnh hội thoại"""
    
    def __init__(self):
        """Khởi tạo Context Tracker Tool"""
        super().__init__(
            name="context_tracker",
            description="Theo dõi ngữ cảnh (context) của cuộc trò chuyện",
            parameters=[
                {
                    "name": "action",
                    "type": "string",
                    "description": "Hành động cần thực hiện: update, get, clear",
                    "required": True
                },
                {
                    "name": "session_id",
                    "type": "string",
                    "description": "ID của phiên trò chuyện",
                    "required": True
                },
                {
                    "name": "context_data",
                    "type": "object",
                    "description": "Dữ liệu context cần cập nhật (chỉ cần khi action=update)",
                    "required": False
                },
                {
                    "name": "key",
                    "type": "string",
                    "description": "Khóa cụ thể trong context cần lấy (chỉ cần khi action=get)",
                    "required": False
                }
            ],
            returns={
                "type": "object",
                "description": "Kết quả của hành động",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Trạng thái thành công"
                    },
                    "context": {
                        "type": "object",
                        "description": "Dữ liệu context"
                    },
                    "error": {
                        "type": "string",
                        "description": "Thông báo lỗi nếu có"
                    }
                }
            }
        )
        
        # Lưu trữ context theo session
        self.contexts = {}
        self.logger = logging.getLogger("ContextTracker")
    
    async def update_context(self, session_id: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cập nhật context cho một phiên
        
        Args:
            session_id: ID của phiên trò chuyện
            context_data: Dữ liệu context cần cập nhật
            
        Returns:
            Dict[str, Any]: Kết quả cập nhật
        """
        # Khởi tạo context cho session nếu chưa có
        if session_id not in self.contexts:
            self.contexts[session_id] = {
                "last_updated": time.time()
            }
        
        # Cập nhật context với dữ liệu mới
        self.contexts[session_id].update(context_data)
        self.contexts[session_id]["last_updated"] = time.time()
        
        self.logger.debug(f"Cập nhật context cho session {session_id}")
        
        return {
            "success": True,
            "context": self.contexts[session_id]
        }
    
    async def get_context(self, session_id: str, key: Optional[str] = None) -> Dict[str, Any]:
        """Lấy context của một phiên
        
        Args:
            session_id: ID của phiên trò chuyện
            key: Khóa cụ thể trong context cần lấy (optional)
            
        Returns:
            Dict[str, Any]: Context
        """
        # Kiểm tra xem session có tồn tại không
        if session_id not in self.contexts:
            return {
                "success": True,
                "context": {}
            }
        
        # Lấy toàn bộ context hoặc giá trị cụ thể
        if key:
            value = self.contexts[session_id].get(key)
            return {
                "success": True,
                "context": {key: value}
            }
        else:
            return {
                "success": True,
                "context": self.contexts[session_id]
            }
    
    async def clear_context(self, session_id: str) -> Dict[str, Any]:
        """Xóa context của một phiên
        
        Args:
            session_id: ID của phiên trò chuyện
            
        Returns:
            Dict[str, Any]: Kết quả xóa
        """
        # Xóa context
        if session_id in self.contexts:
            self.contexts[session_id] = {
                "last_updated": time.time()
            }
        
        return {
            "success": True,
            "context": {}
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Thực thi tool với tham số từ ADK
        
        Args:
            **kwargs: Tham số
            
        Returns:
            Dict[str, Any]: Kết quả của hành động
        """
        action = kwargs.get("action")
        session_id = kwargs.get("session_id")
        
        if not action:
            return {
                "success": False,
                "error": "Thiếu tham số action"
            }
        
        if not session_id:
            return {
                "success": False,
                "error": "Thiếu tham số session_id"
            }
        
        # Thực hiện hành động tương ứng
        if action == "update":
            context_data = kwargs.get("context_data")
            if not context_data:
                return {
                    "success": False,
                    "error": "Thiếu tham số context_data cho hành động update"
                }
            return await self.update_context(session_id, context_data)
        
        elif action == "get":
            key = kwargs.get("key")
            return await self.get_context(session_id, key)
        
        elif action == "clear":
            return await self.clear_context(session_id)
        
        else:
            return {
                "success": False,
                "error": f"Hành động không hợp lệ: {action}"
            }