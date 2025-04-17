"""
Intent Classifier Tool - Công cụ phân loại ý định của người dùng

Tool này phân tích nội dung tin nhắn của người dùng để xác định 
agent phù hợp để xử lý yêu cầu.
"""

import os
import json
import logging
import re
from typing import Dict, Any, List, Optional
from enum import Enum

# Google ADK imports
from google_adk.core.tool import Tool


class AgentType(str, Enum):
    """Các loại agent được hỗ trợ trong hệ thống"""
    BAT_CUC_LINH_SO = "batcuclinh_so"
    PAYMENT = "payment"
    USER = "user"
    UNKNOWN = "unknown"


class IntentClassifier(Tool):
    """Tool phân loại ý định người dùng"""
    
    def __init__(self):
        """Khởi tạo Intent Classifier Tool"""
        super().__init__(
            name="intent_classifier",
            description="Phân tích nội dung tin nhắn để xác định agent phù hợp",
            parameters=[
                {
                    "name": "message",
                    "type": "string",
                    "description": "Nội dung tin nhắn cần phân tích",
                    "required": True
                }
            ],
            returns={
                "type": "object",
                "description": "Kết quả phân tích ý định",
                "properties": {
                    "agent_type": {
                        "type": "string",
                        "description": "Loại agent phù hợp"
                    },
                    "confidence": {
                        "type": "number",
                        "description": "Độ tin cậy của kết quả phân loại (0-1)"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Các từ khóa được nhận diện"
                    }
                }
            }
        )
        
        # Các pattern và từ khóa để phân loại
        self.patterns = {
            AgentType.BAT_CUC_LINH_SO: [
                r'số điện thoại',
                r'sđt',
                r'số đt',
                r'số cccd',
                r'căn cước',
                r'cmnd',
                r'cccd',
                r'tài khoản ngân hàng',
                r'số tài khoản',
                r'stk',
                r'mật khẩu',
                r'password',
                r'bát tinh',
                r'phong thủy số',
                r'bát cục linh số',
                r'phân tích số',
                r'\d{9,12}', # Mẫu số CCCD/CMND (9-12 chữ số)
                r'\d{10,11}' # Mẫu số điện thoại (10-11 chữ số)
            ],
            AgentType.PAYMENT: [
                r'thanh toán',
                r'payment',
                r'nâng cấp',
                r'upgrade',
                r'gói dịch vụ',
                r'plan',
                r'subscription',
                r'premium',
                r'mua',
                r'buy',
                r'giá',
                r'price',
                r'quota',
                r'hết lượt'
            ],
            AgentType.USER: [
                r'tài khoản',
                r'account',
                r'đăng ký',
                r'đăng nhập',
                r'login',
                r'signup',
                r'register',
                r'api key',
                r'api token',
                r'profile',
                r'hồ sơ',
                r'thông tin cá nhân'
            ]
        }
    
    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """Phân tích ý định dựa trên nội dung tin nhắn
        
        Args:
            message: Nội dung tin nhắn cần phân tích
            
        Returns:
            Dict[str, Any]: Kết quả phân tích gồm agent_type, confidence, keywords
        """
        # Chuyển tin nhắn sang chữ thường để dễ phân tích
        message_lower = message.lower()
        
        # Đếm số từ khóa match với mỗi loại agent
        matches = {agent_type: 0 for agent_type in AgentType}
        keywords = {agent_type: [] for agent_type in AgentType}
        
        # Kiểm tra các pattern
        for agent_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    matches[agent_type] += 1
                    keywords[agent_type].append(pattern)
        
        # Xác định agent có số lượng matches cao nhất
        max_matches = 0
        best_agent = AgentType.UNKNOWN
        
        for agent_type, count in matches.items():
            if count > max_matches:
                max_matches = count
                best_agent = agent_type
        
        # Tính độ tin cậy
        total_matches = sum(matches.values())
        confidence = max_matches / total_matches if total_matches > 0 else 0
        
        # Fallback về BatCucLinhSo nếu không xác định được
        if best_agent == AgentType.UNKNOWN or confidence < 0.3:
            best_agent = AgentType.BAT_CUC_LINH_SO
            confidence = 0.5
        
        return {
            "agent_type": best_agent,
            "confidence": confidence,
            "keywords": keywords[best_agent]
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Thực thi tool với tham số từ ADK
        
        Args:
            **kwargs: Tham số, bao gồm message
            
        Returns:
            Dict[str, Any]: Kết quả phân tích ý định
        """
        message = kwargs.get("message", "")
        return await self.analyze_intent(message) 