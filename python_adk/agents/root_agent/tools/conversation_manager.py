"""
Conversation Manager Tool - Công cụ quản lý luồng trò chuyện

Tool này quản lý luồng trò chuyện, lưu trữ lịch sử và cung cấp 
các chức năng tương tác với lịch sử trò chuyện.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import time

# Google ADK imports
from google_adk.core.tool import Tool


class ConversationManager(Tool):
    """Tool quản lý luồng trò chuyện"""
    
    def __init__(self):
        """Khởi tạo Conversation Manager Tool"""
        super().__init__(
            name="conversation_manager",
            description="Quản lý lịch sử và luồng trò chuyện",
            parameters=[
                {
                    "name": "action",
                    "type": "string",
                    "description": "Hành động cần thực hiện: add_message, get_history, clear_history",
                    "required": True
                },
                {
                    "name": "session_id",
                    "type": "string",
                    "description": "ID của phiên trò chuyện",
                    "required": True
                },
                {
                    "name": "message",
                    "type": "object",
                    "description": "Tin nhắn cần thêm vào lịch sử (chỉ cần khi action=add_message)",
                    "required": False
                },
                {
                    "name": "limit",
                    "type": "integer",
                    "description": "Số lượng tin nhắn tối đa trả về (chỉ cần khi action=get_history)",
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
                    "data": {
                        "type": "object",
                        "description": "Dữ liệu kết quả"
                    },
                    "error": {
                        "type": "string",
                        "description": "Thông báo lỗi nếu có"
                    }
                }
            }
        )
        
        # Lưu trữ lịch sử trò chuyện
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
    
    def add_message(self, session_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Thêm tin nhắn vào lịch sử
        
        Args:
            session_id: ID của phiên trò chuyện
            message: Tin nhắn cần thêm
            
        Returns:
            Dict[str, Any]: Kết quả thao tác
        """
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        # Thêm timestamp nếu chưa có
        if "timestamp" not in message:
            message["timestamp"] = time.time()
        
        self.conversations[session_id].append(message)
        
        return {
            "success": True,
            "data": {
                "message_count": len(self.conversations[session_id])
            }
        }
    
    def get_history(self, session_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Lấy lịch sử trò chuyện
        
        Args:
            session_id: ID của phiên trò chuyện
            limit: Số lượng tin nhắn tối đa trả về
            
        Returns:
            Dict[str, Any]: Kết quả thao tác
        """
        if session_id not in self.conversations:
            return {
                "success": False,
                "error": f"Không tìm thấy phiên trò chuyện với ID {session_id}"
            }
        
        history = self.conversations[session_id]
        
        if limit is not None and limit > 0:
            history = history[-limit:]
        
        return {
            "success": True,
            "data": {
                "history": history,
                "message_count": len(history)
            }
        }
    
    def clear_history(self, session_id: str) -> Dict[str, Any]:
        """Xóa lịch sử trò chuyện
        
        Args:
            session_id: ID của phiên trò chuyện
            
        Returns:
            Dict[str, Any]: Kết quả thao tác
        """
        if session_id not in self.conversations:
            return {
                "success": False,
                "error": f"Không tìm thấy phiên trò chuyện với ID {session_id}"
            }
        
        self.conversations[session_id] = []
        
        return {
            "success": True,
            "data": {
                "message_count": 0
            }
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Thực thi tool với tham số từ ADK
        
        Args:
            **kwargs: Tham số, bao gồm action, session_id và các tham số khác
            
        Returns:
            Dict[str, Any]: Kết quả của hành động
        """
        action = kwargs.get("action", "")
        session_id = kwargs.get("session_id", "")
        
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
        
        if action == "add_message":
            message = kwargs.get("message", {})
            if not message:
                return {
                    "success": False,
                    "error": "Thiếu tham số message"
                }
            return self.add_message(session_id, message)
        
        elif action == "get_history":
            limit = kwargs.get("limit")
            return self.get_history(session_id, limit)
        
        elif action == "clear_history":
            return self.clear_history(session_id)
        
        else:
            return {
                "success": False,
                "error": f"Hành động không hợp lệ: {action}"
            } 