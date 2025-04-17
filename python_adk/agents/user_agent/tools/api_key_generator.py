"""
API Key Generator Tool

Tool tạo và quản lý API keys cho người dùng.
"""

import os
import logging
import secrets
import string
from typing import Dict, Any, List
from datetime import datetime, timedelta

from google.adk.core.tool import tool
from pymongo import MongoClient
from pymongo.collection import Collection

# Kết nối MongoDB
client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017"))
db = client[os.environ.get("MONGODB_NAME", "phongthuybotdb")]
apikeys_collection = db["apikeys"]

class ApiKeyGenerator:
    """Tool tạo và quản lý API keys"""
    
    def __init__(self):
        """Khởi tạo API Key Generator"""
        self.logger = logging.getLogger("ApiKeyGenerator")
        self.key_length = int(os.environ.get("API_KEY_LENGTH", "32"))
        self.default_expiry_days = int(os.environ.get("API_KEY_EXPIRY_DAYS", "90"))
    
    @tool
    async def generate_api_key(self, user_id: str, name: str, 
                             expiry_days: int = None, quota: int = None) -> Dict[str, Any]:
        """Tạo API key mới
        
        Args:
            user_id: ID người dùng
            name: Tên API key
            expiry_days: Số ngày hết hạn (tùy chọn)
            quota: Hạn mức sử dụng (tùy chọn)
            
        Returns:
            Dict[str, Any]: Thông tin API key mới
        """
        try:
            # Tạo API key mới
            api_key = self._generate_random_key()
            
            # Tính ngày hết hạn
            expiry_days = expiry_days or self.default_expiry_days
            expiry_date = datetime.utcnow() + timedelta(days=expiry_days)
            
            # Tạo document API key
            api_key_doc = {
                "user_id": user_id,
                "name": name,
                "key": api_key,
                "quota": quota or 100,
                "used": 0,
                "created_at": datetime.utcnow(),
                "expires_at": expiry_date,
                "last_used": None,
                "status": "active"
            }
            
            # Lưu vào database
            result = apikeys_collection.insert_one(api_key_doc)
            
            return {
                "success": True,
                "message": "API key đã được tạo thành công",
                "api_key": api_key,
                "id": str(result.inserted_id),
                "expires_at": expiry_date.isoformat(),
                "quota": quota or 100
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi tạo API key: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def get_api_keys(self, user_id: str) -> Dict[str, Any]:
        """Lấy danh sách API keys của người dùng
        
        Args:
            user_id: ID người dùng
            
        Returns:
            Dict[str, Any]: Danh sách API keys
        """
        try:
            # Tìm tất cả API keys của người dùng
            api_keys = list(apikeys_collection.find({"user_id": user_id}))
            
            # Ẩn thông tin key đầy đủ
            for key in api_keys:
                key["_id"] = str(key["_id"])
                # Chỉ hiển thị 8 ký tự đầu và 4 ký tự cuối
                if len(key["key"]) > 12:
                    key["key"] = f"{key['key'][:8]}...{key['key'][-4:]}"
                key["created_at"] = key["created_at"].isoformat()
                key["expires_at"] = key["expires_at"].isoformat()
                if key["last_used"]:
                    key["last_used"] = key["last_used"].isoformat()
            
            return {
                "success": True,
                "api_keys": api_keys
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi lấy danh sách API keys: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def revoke_api_key(self, api_key_id: str, user_id: str) -> Dict[str, Any]:
        """Thu hồi API key
        
        Args:
            api_key_id: ID của API key
            user_id: ID người dùng (để xác thực quyền)
            
        Returns:
            Dict[str, Any]: Kết quả thu hồi
        """
        try:
            # Kiểm tra quyền sở hữu
            api_key = apikeys_collection.find_one({"_id": api_key_id})
            if not api_key:
                return {
                    "success": False,
                    "message": "Không tìm thấy API key"
                }
            
            if api_key["user_id"] != user_id:
                return {
                    "success": False,
                    "message": "Bạn không có quyền thu hồi API key này"
                }
            
            # Cập nhật trạng thái
            result = apikeys_collection.update_one(
                {"_id": api_key_id},
                {"$set": {"status": "revoked", "updated_at": datetime.utcnow()}}
            )
            
            if result.modified_count == 0:
                return {
                    "success": False,
                    "message": "Không thể thu hồi API key"
                }
            
            return {
                "success": True,
                "message": "API key đã bị thu hồi"
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi thu hồi API key: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def verify_api_key(self, api_key: str) -> Dict[str, Any]:
        """Xác thực API key
        
        Args:
            api_key: API key cần xác thực
            
        Returns:
            Dict[str, Any]: Kết quả xác thực
        """
        try:
            # Tìm API key
            key_doc = apikeys_collection.find_one({"key": api_key, "status": "active"})
            if not key_doc:
                return {
                    "success": False,
                    "message": "API key không hợp lệ hoặc đã bị thu hồi"
                }
            
            # Kiểm tra hết hạn
            if key_doc["expires_at"] < datetime.utcnow():
                return {
                    "success": False,
                    "message": "API key đã hết hạn"
                }
            
            # Kiểm tra quota
            if key_doc["used"] >= key_doc["quota"]:
                return {
                    "success": False,
                    "message": "API key đã vượt quá hạn mức sử dụng"
                }
            
            # Cập nhật thông tin sử dụng
            apikeys_collection.update_one(
                {"_id": key_doc["_id"]},
                {
                    "$inc": {"used": 1},
                    "$set": {"last_used": datetime.utcnow()}
                }
            )
            
            return {
                "success": True,
                "user_id": key_doc["user_id"],
                "remaining_quota": key_doc["quota"] - key_doc["used"] - 1
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi xác thực API key: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    def _generate_random_key(self) -> str:
        """Tạo chuỗi ngẫu nhiên làm API key
        
        Returns:
            str: API key ngẫu nhiên
        """
        # Tạo chuỗi ngẫu nhiên với các ký tự an toàn
        alphabet = string.ascii_letters + string.digits
        api_key = ''.join(secrets.choice(alphabet) for _ in range(self.key_length))
        
        # Thêm tiền tố để dễ nhận biết
        return f"ptb_{api_key}" 