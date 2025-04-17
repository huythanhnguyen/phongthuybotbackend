"""
Context Tracker Tool - Công cụ theo dõi và duy trì context của cuộc trò chuyện

Tool này lưu trữ và quản lý context của cuộc trò chuyện để cung cấp 
thông tin liên tục giữa các lượt tương tác.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

# Google ADK imports
from google.adk.core.tool import Tool


class ContextTracker(Tool):
    """Tool theo dõi và duy trì context của cuộc trò chuyện"""
    
    def __init__(self):
        """Khởi tạo Context Tracker Tool"""
        super().__init__(
            name="context_tracker",
            description="Theo dõi và duy trì context của cuộc trò chuyện",
            parameters=[
                {
                    "name": "action",
                    "type": "string",
                    "description": "Hành động cần thực hiện: get_context, update_context, clear_context",
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
                    "description": "Dữ liệu context cần cập nhật (chỉ cần khi action=update_context)",
                    "required": False
                },
                {
                    "name": "key",
                    "type": "string",
                    "description": "Khóa của giá trị cần lấy (chỉ cần khi muốn lấy một giá trị cụ thể)",
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
        
        # Lưu trữ context của các phiên trò chuyện
        self.contexts: Dict[str, Dict[str, Any]] = {}
    
    def get_context(self, session_id: str, key: Optional[str] = None) -> Dict[str, Any]:
        """Lấy context của phiên trò chuyện
        
        Args:
            session_id: ID của phiên trò chuyện
            key: Khóa của giá trị cần lấy (nếu None, trả về toàn bộ context)
            
        Returns:
            Dict[str, Any]: Kết quả thao tác
        """
        if session_id not in self.contexts:
            return {
                "success": False,
                "error": f"Không tìm thấy context cho phiên với ID {session_id}"
            }
        
        if key is not None:
            if key in self.contexts[session_id]:
                return {
                    "success": True,
                    "data": {
                        key: self.contexts[session_id][key]
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Không tìm thấy khóa {key} trong context"
                }
        
        return {
            "success": True,
            "data": self.contexts[session_id]
        }
    
    def update_context(self, session_id: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cập nhật context của phiên trò chuyện
        
        Args:
            session_id: ID của phiên trò chuyện
            context_data: Dữ liệu context cần cập nhật
            
        Returns:
            Dict[str, Any]: Kết quả thao tác
        """
        if session_id not in self.contexts:
            self.contexts[session_id] = {}
        
        # Cập nhật context với dữ liệu mới
        self.contexts[session_id].update(context_data)
        
        # Cập nhật thời gian cập nhật cuối cùng
        self.contexts[session_id]["last_updated"] = datetime.now().isoformat()
        
        return {
            "success": True,
            "data": {
                "updated_keys": list(context_data.keys())
            }
        }
    
    def clear_context(self, session_id: str) -> Dict[str, Any]:
        """Xóa context của phiên trò chuyện
        
        Args:
            session_id: ID của phiên trò chuyện
            
        Returns:
            Dict[str, Any]: Kết quả thao tác
        """
        if session_id not in self.contexts:
            return {
                "success": False,
                "error": f"Không tìm thấy context cho phiên với ID {session_id}"
            }
        
        self.contexts[session_id] = {
            "last_updated": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "data": {
                "message": f"Đã xóa context cho phiên {session_id}"
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
        
        if action == "get_context":
            key = kwargs.get("key")
            return self.get_context(session_id, key)
        
        elif action == "update_context":
            context_data = kwargs.get("context_data", {})
            if not context_data:
                return {
                    "success": False,
                    "error": "Thiếu tham số context_data"
                }
            return self.update_context(session_id, context_data)
        
        elif action == "clear_context":
            return self.clear_context(session_id)
        
        else:
            return {
                "success": False,
                "error": f"Hành động không hợp lệ: {action}"
            }