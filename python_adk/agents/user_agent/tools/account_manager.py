"""
Account Manager Tool

Tool quản lý tài khoản người dùng, bao gồm đăng ký, đăng nhập, và cập nhật thông tin.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from google.adk.core.tool import tool
import jwt
import bcrypt
from pymongo import MongoClient
from pymongo.collection import Collection

# Kết nối MongoDB
client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017"))
db = client[os.environ.get("MONGODB_NAME", "phongthuybotdb")]
users_collection = db["users"]

class AccountManager:
    """Tool quản lý tài khoản người dùng"""
    
    def __init__(self):
        """Khởi tạo Account Manager"""
        self.logger = logging.getLogger("AccountManager")
        self.jwt_secret = os.environ.get("JWT_SECRET", "default_jwt_secret")
        self.token_expiry = int(os.environ.get("TOKEN_EXPIRY", "86400"))  # 24 giờ
    
    @tool
    async def register_user(self, email: str, password: str, name: str = None, phone: str = None) -> Dict[str, Any]:
        """Đăng ký người dùng mới
        
        Args:
            email: Email người dùng
            password: Mật khẩu
            name: Tên người dùng (tùy chọn)
            phone: Số điện thoại (tùy chọn)
            
        Returns:
            Dict[str, Any]: Kết quả đăng ký
        """
        try:
            # Kiểm tra email đã tồn tại
            existing_user = users_collection.find_one({"email": email})
            if existing_user:
                return {
                    "success": False,
                    "message": "Email đã được sử dụng. Vui lòng chọn email khác."
                }
            
            # Hash mật khẩu
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Tạo người dùng mới
            new_user = {
                "email": email,
                "password": hashed_password,
                "name": name,
                "phone": phone,
                "role": "user",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "quota": {
                    "daily_limit": 10,
                    "monthly_limit": 100,
                    "used_today": 0,
                    "used_month": 0,
                    "reset_date": datetime.utcnow() + timedelta(days=1)
                },
                "subscription": {
                    "plan": "free",
                    "start_date": datetime.utcnow(),
                    "end_date": datetime.utcnow() + timedelta(days=30),
                    "auto_renew": False
                }
            }
            
            result = users_collection.insert_one(new_user)
            
            # Tạo token
            token = self._generate_token(str(result.inserted_id), email, "user")
            
            return {
                "success": True,
                "message": "Đăng ký thành công",
                "user_id": str(result.inserted_id),
                "token": token
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi đăng ký: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Đăng nhập người dùng
        
        Args:
            email: Email người dùng
            password: Mật khẩu
            
        Returns:
            Dict[str, Any]: Kết quả đăng nhập
        """
        try:
            # Tìm người dùng
            user = users_collection.find_one({"email": email})
            if not user:
                return {
                    "success": False,
                    "message": "Email hoặc mật khẩu không chính xác"
                }
            
            # Kiểm tra mật khẩu
            if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                return {
                    "success": False,
                    "message": "Email hoặc mật khẩu không chính xác"
                }
            
            # Tạo token
            token = self._generate_token(str(user["_id"]), user["email"], user["role"])
            
            return {
                "success": True,
                "message": "Đăng nhập thành công",
                "user_id": str(user["_id"]),
                "token": token,
                "user": {
                    "email": user["email"],
                    "name": user.get("name"),
                    "role": user["role"],
                    "subscription": user.get("subscription")
                }
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi đăng nhập: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def update_profile(self, user_id: str, name: str = None, phone: str = None, 
                           email: str = None, password: str = None) -> Dict[str, Any]:
        """Cập nhật thông tin người dùng
        
        Args:
            user_id: ID người dùng
            name: Tên người dùng (tùy chọn)
            phone: Số điện thoại (tùy chọn)
            email: Email mới (tùy chọn)
            password: Mật khẩu mới (tùy chọn)
            
        Returns:
            Dict[str, Any]: Kết quả cập nhật
        """
        try:
            # Tạo dict cập nhật
            update_data = {"updated_at": datetime.utcnow()}
            
            if name:
                update_data["name"] = name
            if phone:
                update_data["phone"] = phone
            if email:
                # Kiểm tra email mới đã tồn tại
                existing_user = users_collection.find_one({"email": email, "_id": {"$ne": user_id}})
                if existing_user:
                    return {
                        "success": False,
                        "message": "Email đã được sử dụng. Vui lòng chọn email khác."
                    }
                update_data["email"] = email
            if password:
                # Hash mật khẩu mới
                update_data["password"] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Cập nhật thông tin
            result = users_collection.update_one({"_id": user_id}, {"$set": update_data})
            
            if result.modified_count == 0:
                return {
                    "success": False,
                    "message": "Không tìm thấy người dùng hoặc không có thông tin nào được cập nhật"
                }
            
            return {
                "success": True,
                "message": "Cập nhật thông tin thành công"
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi cập nhật thông tin: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Lấy thông tin người dùng
        
        Args:
            user_id: ID người dùng
            
        Returns:
            Dict[str, Any]: Thông tin người dùng
        """
        try:
            user = users_collection.find_one({"_id": user_id})
            if not user:
                return {
                    "success": False,
                    "message": "Không tìm thấy người dùng"
                }
            
            # Loại bỏ mật khẩu trước khi trả về
            user.pop("password", None)
            
            return {
                "success": True,
                "user": {
                    "email": user["email"],
                    "name": user.get("name"),
                    "phone": user.get("phone"),
                    "role": user["role"],
                    "created_at": user["created_at"].isoformat(),
                    "quota": user.get("quota"),
                    "subscription": user.get("subscription")
                }
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi lấy thông tin người dùng: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Xác thực token
        
        Args:
            token: JWT token
            
        Returns:
            Dict[str, Any]: Kết quả xác thực
        """
        try:
            # Giải mã token
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            
            return {
                "success": True,
                "user_id": payload["user_id"],
                "email": payload["email"],
                "role": payload["role"]
            }
            
        except jwt.ExpiredSignatureError:
            return {
                "success": False,
                "message": "Token đã hết hạn"
            }
        except jwt.InvalidTokenError:
            return {
                "success": False,
                "message": "Token không hợp lệ"
            }
    
    def _generate_token(self, user_id: str, email: str, role: str) -> str:
        """Tạo JWT token
        
        Args:
            user_id: ID người dùng
            email: Email người dùng
            role: Vai trò người dùng
            
        Returns:
            str: JWT token
        """
        payload = {
            "user_id": user_id,
            "email": email,
            "role": role,
            "exp": datetime.utcnow() + timedelta(seconds=self.token_expiry)
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256") 