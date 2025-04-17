"""
Auth Agent - Xử lý xác thực và quản lý tài khoản người dùng

Auth Agent đóng vai trò xử lý các yêu cầu liên quan đến xác thực, 
đăng ký, đăng nhập và quản lý tài khoản người dùng.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
import datetime
import uuid
import jwt
from passlib.hash import bcrypt

# Google ADK imports
from adk.core.agent import Agent
from adk.core.agent_builder import AgentBuilder
from adk.generators.llm import LLMGenerator
from adk.managers.context import ContextManager

# A2A Protocol imports
from python_adk.a2a.protocol import Task, Message, Artifact, Part, TaskStatus, Role, PartType

class AuthAgent:
    """Auth Agent xử lý các yêu cầu liên quan đến xác thực"""

    def __init__(self):
        """Khởi tạo Auth Agent"""
        # Khởi tạo logger
        self.logger = logging.getLogger("AuthAgent")
        
        # State lưu trữ users (trong bộ nhớ tạm thời)
        # Trong triển khai thực tế, sử dụng database
        self.users: Dict[str, Any] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        # Khóa bí mật để ký JWT
        self.secret_key = os.environ.get("JWT_SECRET", "phongthuyso_secret_key")
        
        # Thời gian hết hạn token (mặc định 24 giờ)
        self.token_expiry = int(os.environ.get("TOKEN_EXPIRY", 86400))
        
        self.logger.info("Auth Agent đã được khởi tạo")
    
    async def process_task(self, task: Task, message: Message, context: Dict[str, Any]) -> Dict[str, Any]:
        """Xử lý task từ Root Agent
        
        Args:
            task: Task A2A
            message: Message A2A
            context: Thông tin ngữ cảnh
            
        Returns:
            Dict[str, Any]: Kết quả xử lý
        """
        try:
            # Lấy loại query từ context
            query_type = context.get("metadata", {}).get("query_type", "")
            
            # Phân tích nội dung truy vấn để xác định hành động cần thực hiện
            action = self._determine_action(query_type, context)
            
            # Thực hiện hành động tương ứng
            result = await self._execute_action(action, context)
            
            # Cập nhật trạng thái task và tạo artifact
            task.update_status(TaskStatus.COMPLETED)
            
            response_text = result.get("message", "Xử lý thành công")
            artifact = Artifact(
                type="response",
                parts=[Part(type=PartType.TEXT, text=response_text)]
            )
            
            task.add_artifact(artifact)
            
            # Bổ sung metadata vào kết quả
            result.update({
                "success": True,
                "task_id": task.id,
                "response": response_text
            })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Lỗi xử lý task: {str(e)}")
            return self._handle_error(str(e), task)
    
    def _determine_action(self, query_type: str, context: Dict[str, Any]) -> str:
        """Xác định hành động cần thực hiện dựa trên truy vấn
        
        Args:
            query_type: Loại truy vấn từ metadata
            context: Thông tin ngữ cảnh
            
        Returns:
            str: Tên hành động cần thực hiện
        """
        # Nếu metadata đã chỉ định query, sử dụng nó
        if query_type in ["login", "register", "logout", "verify_token", "change_password"]:
            return query_type
        
        # Nếu không, phân tích từ nội dung truy vấn
        query = context.get("metadata", {}).get("query", "")
        
        if "đăng nhập" in query.lower() or "login" in query.lower():
            return "login"
        elif "đăng ký" in query.lower() or "register" in query.lower():
            return "register"
        elif "đăng xuất" in query.lower() or "logout" in query.lower():
            return "logout"
        elif "token" in query.lower() or "xác thực" in query.lower():
            return "verify_token"
        elif "đổi mật khẩu" in query.lower() or "change password" in query.lower():
            return "change_password"
        
        # Mặc định
        return "unknown"
    
    async def _execute_action(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Thực hiện hành động xác định
        
        Args:
            action: Tên hành động
            context: Thông tin ngữ cảnh
            
        Returns:
            Dict[str, Any]: Kết quả hành động
        """
        metadata = context.get("metadata", {})
        
        if action == "login":
            return await self._login(metadata.get("email", ""), metadata.get("password", ""))
        elif action == "register":
            return await self._register(
                metadata.get("name", ""), 
                metadata.get("email", ""), 
                metadata.get("password", "")
            )
        elif action == "logout":
            return await self._logout(metadata.get("token", ""))
        elif action == "verify_token":
            return await self._verify_token(metadata.get("token", ""))
        elif action == "change_password":
            return await self._change_password(
                metadata.get("token", ""),
                metadata.get("currentPassword", ""),
                metadata.get("newPassword", "")
            )
        else:
            return {
                "success": False,
                "message": "Không xác định được hành động cần thực hiện"
            }
    
    async def _login(self, email: str, password: str) -> Dict[str, Any]:
        """Đăng nhập người dùng
        
        Args:
            email: Email đăng nhập
            password: Mật khẩu
            
        Returns:
            Dict[str, Any]: Kết quả đăng nhập
        """
        if not email or not password:
            return {
                "success": False,
                "message": "Vui lòng cung cấp email và mật khẩu"
            }
        
        # Kiểm tra user trong "database"
        user_key = email.lower()
        if user_key not in self.users:
            # Trong triển khai thật, cần xử lý bảo mật hơn để không xác nhận email tồn tại
            return {
                "success": False,
                "message": "Email hoặc mật khẩu không chính xác"
            }
        
        user = self.users[user_key]
        
        # Kiểm tra mật khẩu
        if not bcrypt.verify(password, user["password_hash"]):
            return {
                "success": False,
                "message": "Email hoặc mật khẩu không chính xác"
            }
        
        # Tạo token JWT
        token = self._generate_token(user)
        
        # Thêm session
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "user_id": user["id"],
            "created_at": datetime.datetime.now().isoformat(),
            "last_activity": datetime.datetime.now().isoformat()
        }
        
        # Lọc thông tin người dùng (không trả về password_hash)
        user_info = {k: v for k, v in user.items() if k != "password_hash"}
        
        return {
            "success": True,
            "message": "Đăng nhập thành công",
            "token": token,
            "user": user_info,
            "sessionId": session_id
        }
    
    async def _register(self, name: str, email: str, password: str) -> Dict[str, Any]:
        """Đăng ký người dùng mới
        
        Args:
            name: Tên người dùng
            email: Email
            password: Mật khẩu
            
        Returns:
            Dict[str, Any]: Kết quả đăng ký
        """
        if not name or not email or not password:
            return {
                "success": False,
                "message": "Vui lòng cung cấp đầy đủ thông tin đăng ký"
            }
        
        # Kiểm tra email đã tồn tại chưa
        user_key = email.lower()
        if user_key in self.users:
            return {
                "success": False,
                "message": "Email đã được đăng ký"
            }
        
        # Tạo user mới
        user_id = str(uuid.uuid4())
        
        # Hash mật khẩu
        password_hash = bcrypt.hash(password)
        
        # Lưu user
        self.users[user_key] = {
            "id": user_id,
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.datetime.now().isoformat(),
            "role": "user"
        }
        
        # Tạo token JWT
        token = self._generate_token(self.users[user_key])
        
        # Thêm session
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.datetime.now().isoformat(),
            "last_activity": datetime.datetime.now().isoformat()
        }
        
        # Lọc thông tin người dùng (không trả về password_hash)
        user_info = {k: v for k, v in self.users[user_key].items() if k != "password_hash"}
        
        return {
            "success": True,
            "message": "Đăng ký thành công",
            "token": token,
            "user": user_info,
            "sessionId": session_id
        }
    
    async def _logout(self, token: str) -> Dict[str, Any]:
        """Đăng xuất người dùng
        
        Args:
            token: JWT token
            
        Returns:
            Dict[str, Any]: Kết quả đăng xuất
        """
        if not token:
            return {
                "success": True,
                "message": "Đăng xuất thành công"
            }
        
        # Giải mã token để lấy thông tin
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            
            # Xóa các session của user
            session_to_remove = []
            for session_id, session in self.sessions.items():
                if session["user_id"] == user_id:
                    session_to_remove.append(session_id)
            
            for session_id in session_to_remove:
                self.sessions.pop(session_id, None)
                
        except jwt.PyJWTError:
            # Không báo lỗi nếu token không hợp lệ
            pass
        
        return {
            "success": True,
            "message": "Đăng xuất thành công"
        }
    
    async def _verify_token(self, token: str) -> Dict[str, Any]:
        """Xác thực token JWT
        
        Args:
            token: JWT token
            
        Returns:
            Dict[str, Any]: Kết quả xác thực
        """
        if not token:
            return {
                "success": False,
                "message": "Không tìm thấy token"
            }
        
        # Kiểm tra token anonymous
        if token.startswith("anonymous_"):
            session_id = token.replace("anonymous_", "")
            return {
                "success": True,
                "message": "Phiên ẩn danh hợp lệ",
                "user": {
                    "id": f"anonymous_{session_id}",
                    "name": "Người dùng ẩn danh",
                    "email": "anonymous@user.com",
                    "role": "anonymous",
                    "isAnonymous": True,
                    "created_at": datetime.datetime.now().isoformat()
                }
            }
        
        # Giải mã token
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Kiểm tra hết hạn
            now = datetime.datetime.now().timestamp()
            if now > payload.get("exp", 0):
                return {
                    "success": False,
                    "message": "Token đã hết hạn"
                }
            
            # Lấy thông tin user
            user_id = payload.get("user_id")
            user = None
            
            # Tìm user từ ID
            for _, u in self.users.items():
                if u["id"] == user_id:
                    user = u
                    break
            
            if not user:
                return {
                    "success": False,
                    "message": "Không tìm thấy thông tin người dùng"
                }
            
            # Lọc thông tin người dùng (không trả về password_hash)
            user_info = {k: v for k, v in user.items() if k != "password_hash"}
            
            return {
                "success": True,
                "message": "Token hợp lệ",
                "user": user_info
            }
            
        except jwt.PyJWTError as e:
            return {
                "success": False,
                "message": f"Token không hợp lệ: {str(e)}"
            }
    
    async def _change_password(self, token: str, current_password: str, new_password: str) -> Dict[str, Any]:
        """Thay đổi mật khẩu người dùng
        
        Args:
            token: JWT token
            current_password: Mật khẩu hiện tại
            new_password: Mật khẩu mới
            
        Returns:
            Dict[str, Any]: Kết quả thay đổi mật khẩu
        """
        if not token or not current_password or not new_password:
            return {
                "success": False,
                "message": "Thiếu thông tin cần thiết"
            }
        
        # Giải mã token
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            
            # Tìm user từ ID
            user = None
            user_key = None
            
            for email, u in self.users.items():
                if u["id"] == user_id:
                    user = u
                    user_key = email
                    break
            
            if not user or not user_key:
                return {
                    "success": False,
                    "message": "Không tìm thấy thông tin người dùng"
                }
            
            # Kiểm tra mật khẩu hiện tại
            if not bcrypt.verify(current_password, user["password_hash"]):
                return {
                    "success": False,
                    "message": "Mật khẩu hiện tại không chính xác"
                }
            
            # Cập nhật mật khẩu mới
            self.users[user_key]["password_hash"] = bcrypt.hash(new_password)
            
            return {
                "success": True,
                "message": "Thay đổi mật khẩu thành công"
            }
            
        except jwt.PyJWTError as e:
            return {
                "success": False,
                "message": f"Token không hợp lệ: {str(e)}"
            }
    
    def _generate_token(self, user: Dict[str, Any]) -> str:
        """Tạo JWT token
        
        Args:
            user: Thông tin người dùng
            
        Returns:
            str: JWT token
        """
        now = datetime.datetime.now()
        
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "iat": now.timestamp(),
            "exp": (now + datetime.timedelta(seconds=self.token_expiry)).timestamp()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token
    
    def _handle_error(self, error_message: str, task: Task) -> Dict[str, Any]:
        """Xử lý lỗi và trả về phản hồi lỗi
        
        Args:
            error_message: Thông báo lỗi
            task: Task A2A
            
        Returns:
            Dict[str, Any]: Phản hồi lỗi
        """
        task.update_status(TaskStatus.ERROR, error_message)
        
        error_artifact = Artifact(
            type="error",
            parts=[Part(type=PartType.TEXT, text=f"Rất tiếc, đã xảy ra lỗi: {error_message}. Vui lòng thử lại sau.")]
        )
        
        task.add_artifact(error_artifact)
        
        return {
            "success": False,
            "task_id": task.id,
            "session_id": task.session_id,
            "error": error_message,
            "response": f"Rất tiếc, đã xảy ra lỗi: {error_message}. Vui lòng thử lại sau."
        } 