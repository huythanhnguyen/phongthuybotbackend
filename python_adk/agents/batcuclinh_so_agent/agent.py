"""
BatCucLinhSo Agent - Phân tích số điện thoại, CCCD, số tài khoản theo Bát Cục Linh Số

BatCucLinhSo Agent là expert agent chuyên biệt, phân tích các dãy số
theo phương pháp Bát Cục Linh Số.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
import re

# Google ADK imports
from google_adk.core.agent import Agent
from google_adk.core.agent_builder import AgentBuilder
from google_adk.generators.llm import LLMGenerator
from google_adk.managers.context import ContextManager

# A2A Protocol imports
from python_adk.a2a.protocol import Task, Message, Artifact, Part, TaskStatus, Role, PartType

# Local tools imports
from .tools.phone_analyzer import PhoneAnalyzer
from .tools.cccd_analyzer import CCCDAnalyzer


class AnalysisType:
    """Các loại phân tích được hỗ trợ"""
    PHONE = "phone"
    CCCD = "cccd"
    BANK_ACCOUNT = "bank_account"
    PASSWORD = "password"
    UNKNOWN = "unknown"


class BatCucLinhSoAgent:
    """BatCucLinhSo Agent chuyên phân tích số điện thoại, CCCD, STK ngân hàng"""
    
    def __init__(self):
        """Khởi tạo BatCucLinhSo Agent"""
        # Khởi tạo logger
        self.logger = logging.getLogger("BatCucLinhSoAgent")
        
        # Khởi tạo các tools
        self.phone_analyzer = PhoneAnalyzer()
        self.cccd_analyzer = CCCDAnalyzer()
        # TODO: Thêm các công cụ phân tích khác (bank_account, password)
        
        # State lưu trữ sessions
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        # Khởi tạo agent với Google ADK
        model_name = os.environ.get("BATCUCLINH_SO_AGENT_MODEL", "gemini-pro")
        self.agent: Agent = self._build_agent(model_name)
        
        self.logger.info("BatCucLinhSo Agent đã được khởi tạo")
    
    def _build_agent(self, model_name: str) -> Agent:
        """Xây dựng agent sử dụng Google ADK
        
        Args:
            model_name: Tên của model LLM
            
        Returns:
            Agent: Agent được xây dựng
        """
        # Đọc hệ thống prompt từ file
        system_prompt = self._load_system_prompt()
        
        # Tạo generator cho agent
        generator = LLMGenerator(name="batcuclinh-so-generator", model=model_name)
        
        # Xây dựng agent
        agent = (
            AgentBuilder(name="batcuclinh-so-agent")
            .with_system_prompt(system_prompt)
            .with_generator(generator)
            .with_tools([
                self.phone_analyzer,
                self.cccd_analyzer
                # TODO: Thêm các công cụ khác
            ])
            .build()
        )
        
        return agent
    
    def _load_system_prompt(self) -> str:
        """Đọc hệ thống prompt từ file
        
        Returns:
            str: Nội dung prompt
        """
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            # Fallback prompt nếu không tìm thấy file
            return """
            Bạn là BatCucLinhSo Agent, chuyên gia phân tích số điện thoại, CCCD, STK ngân hàng 
            theo phương pháp Bát Cục Linh Số. Nhiệm vụ của bạn là phân tích các con số mà người dùng cung cấp,
            đưa ra ý nghĩa và lời khuyên dựa trên phong thủy số học.
            
            Bạn cần phân tích các yếu tố:
            1. Tổng số
            2. Các cặp số có ý nghĩa
            3. Mức độ cân bằng âm dương
            4. Ngũ hành
            5. Quẻ chủ đạo
            6. Điểm mạnh và điểm yếu
            7. Mức độ phù hợp với các mục đích khác nhau
            
            Hãy sử dụng các tools chuyên biệt để phân tích chính xác và đưa ra kết luận dễ hiểu.
            """
    
    def _determine_analysis_type(self, message: str) -> str:
        """Xác định loại phân tích dựa trên nội dung tin nhắn
        
        Args:
            message: Nội dung tin nhắn
            
        Returns:
            str: Loại phân tích
        """
        message_lower = message.lower()
        
        # Kiểm tra số điện thoại
        phone_patterns = [
            r'số điện thoại', r'sđt', r'số đt',
            r'0\d{9}', r'0\d{8}', r'\+84\d{9}'
        ]
        for pattern in phone_patterns:
            if re.search(pattern, message_lower):
                return AnalysisType.PHONE
        
        # Kiểm tra CCCD/CMND
        cccd_patterns = [
            r'căn cước', r'cccd', r'cmnd', r'chứng minh',
            r'\d{9}', r'\d{12}'
        ]
        for pattern in cccd_patterns:
            if re.search(pattern, message_lower):
                return AnalysisType.CCCD
        
        # Kiểm tra STK ngân hàng
        bank_patterns = [
            r'tài khoản ngân hàng', r'stk', r'số tài khoản'
        ]
        for pattern in bank_patterns:
            if re.search(pattern, message_lower):
                return AnalysisType.BANK_ACCOUNT
        
        # Kiểm tra mật khẩu
        password_patterns = [
            r'mật khẩu', r'password', r'pass'
        ]
        for pattern in password_patterns:
            if re.search(pattern, message_lower):
                return AnalysisType.PASSWORD
        
        # Mặc định: phân tích số điện thoại (phổ biến nhất)
        return AnalysisType.PHONE
    
    async def process_task(self, task: Task, message: Message, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Xử lý task từ Root Agent
        
        Args:
            task: Task cần xử lý
            message: Tin nhắn từ người dùng
            context: Context bổ sung
            
        Returns:
            Dict[str, Any]: Kết quả xử lý
        """
        self.logger.info(f"BatCucLinhSo Agent đang xử lý task {task.id}")
        
        try:
            # Lưu session nếu chưa có
            if task.session_id not in self.sessions:
                self.sessions[task.session_id] = {
                    "user_id": context.get("user_id") if context else None,
                    "history": [],
                    "current_analysis": None
                }
            
            # Thêm tin nhắn vào lịch sử
            message_text = message.parts[0].text if message.parts else ""
            self.sessions[task.session_id]["history"].append({
                "role": message.role,
                "content": message_text,
                "timestamp": task.created_at.isoformat()
            })
            
            # Xác định loại phân tích
            analysis_type = self._determine_analysis_type(message_text)
            self.sessions[task.session_id]["current_analysis"] = analysis_type
            
            # Cập nhật trạng thái task
            task.update_status(TaskStatus.RUNNING)
            
            # Phân tích dựa trên loại
            if analysis_type == AnalysisType.PHONE:
                result = await self.phone_analyzer.analyze(message_text)
            elif analysis_type == AnalysisType.CCCD:
                result = await self.cccd_analyzer.analyze(message_text)
            elif analysis_type == AnalysisType.BANK_ACCOUNT:
                # TODO: Triển khai bank_account_analyzer
                result = {
                    "success": False,
                    "content": "Phân tích số tài khoản ngân hàng chưa được triển khai. Vui lòng thử lại sau."
                }
            elif analysis_type == AnalysisType.PASSWORD:
                # TODO: Triển khai password_analyzer
                result = {
                    "success": False,
                    "content": "Phân tích mật khẩu chưa được triển khai. Vui lòng thử lại sau."
                }
            else:
                result = {
                    "success": False,
                    "content": "Không thể xác định loại phân tích. Vui lòng cung cấp số điện thoại, CCCD, số tài khoản hoặc mật khẩu cần phân tích."
                }
            
            # Tạo artifact từ kết quả
            content = result.get("content", "Không có kết quả phân tích")
            artifact = Artifact(
                type="response",
                parts=[Part(type=PartType.TEXT, text=content)]
            )
            
            # Cập nhật task với artifact
            task.add_artifact(artifact)
            
            # Cập nhật trạng thái task
            status = TaskStatus.COMPLETED if result.get("success", False) else TaskStatus.ERROR
            task.update_status(status)
            
            # Thêm phản hồi vào lịch sử
            self.sessions[task.session_id]["history"].append({
                "role": "assistant",
                "content": content,
                "analysis_type": analysis_type,
                "timestamp": task.updated_at.isoformat()
            })
            
            return {
                "taskId": task.id,
                "status": task.status,
                "artifacts": task.artifacts
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi xử lý BatCucLinhSo: {str(e)}")
            
            # Tạo artifact lỗi
            error_artifact = Artifact(
                type="error",
                parts=[Part(type=PartType.TEXT, text=f"Rất tiếc, đã xảy ra lỗi khi phân tích: {str(e)}. Vui lòng thử lại với nội dung khác.")]
            )
            
            # Cập nhật task với artifact lỗi
            task.update_status(TaskStatus.ERROR, str(e))
            task.add_artifact(error_artifact)
            
            return {
                "taskId": task.id,
                "status": task.status,
                "artifacts": task.artifacts
            }
    
    async def process_request(self, user_request: str, session_id: Optional[str] = None, 
                             context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Xử lý yêu cầu trực tiếp từ người dùng
        
        Args:
            user_request: Yêu cầu của người dùng
            session_id: ID của phiên làm việc
            context: Context bổ sung
            
        Returns:
            Dict[str, Any]: Kết quả xử lý
        """
        # Tạo Task và Message
        task = Task(session_id=session_id)
        message = Message(role=Role.USER, parts=[Part(type=PartType.TEXT, text=user_request)])
        
        # Xử lý task
        result = await self.process_task(task, message, context)
        
        # Trích xuất phản hồi
        response = ""
        if result["artifacts"] and len(result["artifacts"]) > 0:
            artifact = result["artifacts"][0]
            if artifact.parts and len(artifact.parts) > 0:
                response = artifact.parts[0].text
        
        return {
            "success": task.status == TaskStatus.COMPLETED,
            "response": response,
            "task_id": task.id,
            "session_id": session_id,
            "analysis_type": self.sessions[session_id]["current_analysis"] if session_id in self.sessions else None
        }