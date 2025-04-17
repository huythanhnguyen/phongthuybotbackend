"""
Payment Processor Tool

Tool xử lý các giao dịch thanh toán và nâng cấp tài khoản.
"""

import os
import json
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import uuid

from adk.core.tool import tool
from pymongo import MongoClient
from pymongo.collection import Collection

# Kết nối MongoDB
client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017"))
db = client[os.environ.get("MONGODB_NAME", "phongthuybotdb")]
payments_collection = db["payments"]
users_collection = db["users"]

class PaymentProcessor:
    """Tool xử lý thanh toán"""
    
    def __init__(self):
        """Khởi tạo Payment Processor"""
        self.logger = logging.getLogger("PaymentProcessor")
        
        # Thiết lập các gói dịch vụ
        self.plans = {
            "basic": {
                "name": "Gói Cơ Bản",
                "price": 99000,  # VND
                "duration": 30,  # Ngày
                "daily_limit": 30,
                "monthly_limit": 300,
                "features": ["Phân tích số điện thoại", "Phân tích CCCD"]
            },
            "premium": {
                "name": "Gói Cao Cấp",
                "price": 199000,  # VND
                "duration": 30,  # Ngày
                "daily_limit": 100,
                "monthly_limit": 1000,
                "features": ["Phân tích số điện thoại", "Phân tích CCCD", "Phân tích STK ngân hàng", "Phân tích mật khẩu"]
            },
            "business": {
                "name": "Gói Doanh Nghiệp",
                "price": 499000,  # VND
                "duration": 30,  # Ngày
                "daily_limit": 500,
                "monthly_limit": 5000,
                "features": ["Tất cả tính năng", "API Access", "Hỗ trợ ưu tiên"]
            }
        }
    
    @tool
    async def get_plans(self) -> Dict[str, Any]:
        """Lấy danh sách các gói dịch vụ
        
        Returns:
            Dict[str, Any]: Danh sách gói dịch vụ
        """
        return {
            "success": True,
            "plans": self.plans
        }
    
    @tool
    async def create_payment(self, user_id: str, plan_id: str) -> Dict[str, Any]:
        """Tạo yêu cầu thanh toán mới
        
        Args:
            user_id: ID người dùng
            plan_id: ID gói dịch vụ (basic, premium, business)
            
        Returns:
            Dict[str, Any]: Thông tin thanh toán
        """
        try:
            # Kiểm tra gói dịch vụ
            if plan_id not in self.plans:
                return {
                    "success": False,
                    "message": "Gói dịch vụ không hợp lệ"
                }
            
            # Lấy thông tin gói
            plan = self.plans[plan_id]
            
            # Tạo mã thanh toán
            payment_code = f"PTB{uuid.uuid4().hex[:8].upper()}"
            
            # Thời gian hết hạn thanh toán (24 giờ)
            expires_at = datetime.utcnow() + timedelta(hours=24)
            
            # Tạo document thanh toán
            payment_doc = {
                "payment_code": payment_code,
                "user_id": user_id,
                "plan_id": plan_id,
                "amount": plan["price"],
                "status": "pending",  # pending, completed, canceled
                "created_at": datetime.utcnow(),
                "expires_at": expires_at,
                "completed_at": None
            }
            
            # Lưu vào database
            result = payments_collection.insert_one(payment_doc)
            
            return {
                "success": True,
                "payment_id": str(result.inserted_id),
                "payment_code": payment_code,
                "amount": plan["price"],
                "plan_name": plan["name"],
                "expires_at": expires_at.isoformat(),
                "payment_methods": {
                    "bank_transfer": {
                        "account_number": "1234567890",
                        "bank_name": "Vietcombank",
                        "account_name": "PHONG THUY SO",
                        "message": payment_code
                    },
                    "momo": {
                        "phone": "0987654321",
                        "name": "PHONG THUY SO",
                        "message": payment_code
                    }
                }
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi tạo thanh toán: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def verify_payment(self, payment_code: str) -> Dict[str, Any]:
        """Xác thực thanh toán
        
        Args:
            payment_code: Mã thanh toán
            
        Returns:
            Dict[str, Any]: Kết quả xác thực
        """
        try:
            # Tìm thanh toán
            payment = payments_collection.find_one({"payment_code": payment_code})
            if not payment:
                return {
                    "success": False,
                    "message": "Không tìm thấy thanh toán"
                }
            
            # Kiểm tra trạng thái
            if payment["status"] == "completed":
                return {
                    "success": True,
                    "status": "completed",
                    "message": "Thanh toán đã được xác nhận trước đó"
                }
            
            if payment["status"] == "canceled":
                return {
                    "success": False,
                    "status": "canceled",
                    "message": "Thanh toán đã bị hủy"
                }
            
            # Kiểm tra hết hạn
            if payment["expires_at"] < datetime.utcnow():
                # Cập nhật trạng thái hủy
                payments_collection.update_one(
                    {"_id": payment["_id"]},
                    {"$set": {"status": "canceled"}}
                )
                
                return {
                    "success": False,
                    "status": "expired",
                    "message": "Thanh toán đã hết hạn"
                }
            
            # Mô phỏng xác thực thanh toán
            # Trong thực tế, cần kiểm tra với cổng thanh toán
            
            # Cập nhật trạng thái
            payments_collection.update_one(
                {"_id": payment["_id"]},
                {
                    "$set": {
                        "status": "completed",
                        "completed_at": datetime.utcnow()
                    }
                }
            )
            
            # Nâng cấp tài khoản người dùng
            await self._upgrade_user_subscription(payment["user_id"], payment["plan_id"])
            
            return {
                "success": True,
                "status": "completed",
                "message": "Thanh toán đã được xác nhận"
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi xác thực thanh toán: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def get_payment_history(self, user_id: str) -> Dict[str, Any]:
        """Lấy lịch sử thanh toán của người dùng
        
        Args:
            user_id: ID người dùng
            
        Returns:
            Dict[str, Any]: Lịch sử thanh toán
        """
        try:
            # Tìm tất cả thanh toán của người dùng
            payments = list(payments_collection.find({"user_id": user_id}))
            
            # Format lại kết quả
            formatted_payments = []
            for payment in payments:
                formatted_payment = {
                    "payment_id": str(payment["_id"]),
                    "payment_code": payment["payment_code"],
                    "plan_id": payment["plan_id"],
                    "plan_name": self.plans[payment["plan_id"]]["name"] if payment["plan_id"] in self.plans else "Unknown",
                    "amount": payment["amount"],
                    "status": payment["status"],
                    "created_at": payment["created_at"].isoformat()
                }
                
                if payment["completed_at"]:
                    formatted_payment["completed_at"] = payment["completed_at"].isoformat()
                
                formatted_payments.append(formatted_payment)
            
            return {
                "success": True,
                "payments": formatted_payments
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi lấy lịch sử thanh toán: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def cancel_payment(self, payment_code: str, user_id: str) -> Dict[str, Any]:
        """Hủy thanh toán
        
        Args:
            payment_code: Mã thanh toán
            user_id: ID người dùng (để xác thực quyền)
            
        Returns:
            Dict[str, Any]: Kết quả hủy
        """
        try:
            # Tìm thanh toán
            payment = payments_collection.find_one({"payment_code": payment_code})
            if not payment:
                return {
                    "success": False,
                    "message": "Không tìm thấy thanh toán"
                }
            
            # Kiểm tra quyền sở hữu
            if payment["user_id"] != user_id:
                return {
                    "success": False,
                    "message": "Bạn không có quyền hủy thanh toán này"
                }
            
            # Kiểm tra trạng thái
            if payment["status"] != "pending":
                return {
                    "success": False,
                    "message": f"Không thể hủy thanh toán với trạng thái {payment['status']}"
                }
            
            # Cập nhật trạng thái
            payments_collection.update_one(
                {"_id": payment["_id"]},
                {"$set": {"status": "canceled"}}
            )
            
            return {
                "success": True,
                "message": "Thanh toán đã được hủy"
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi hủy thanh toán: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    @tool
    async def check_subscription(self, user_id: str) -> Dict[str, Any]:
        """Kiểm tra thông tin gói dịch vụ của người dùng
        
        Args:
            user_id: ID người dùng
            
        Returns:
            Dict[str, Any]: Thông tin gói dịch vụ
        """
        try:
            # Tìm người dùng
            user = users_collection.find_one({"_id": user_id})
            if not user:
                return {
                    "success": False,
                    "message": "Không tìm thấy người dùng"
                }
            
            # Lấy thông tin gói dịch vụ
            subscription = user.get("subscription", {
                "plan": "free",
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=30),
                "auto_renew": False
            })
            
            # Kiểm tra hết hạn
            is_active = True
            if "end_date" in subscription and isinstance(subscription["end_date"], datetime):
                is_active = subscription["end_date"] > datetime.utcnow()
            
            # Thông tin quota
            quota = user.get("quota", {
                "daily_limit": 10,
                "monthly_limit": 100,
                "used_today": 0,
                "used_month": 0,
                "reset_date": datetime.utcnow() + timedelta(days=1)
            })
            
            # Lấy thông tin gói
            plan_details = self.plans.get(subscription["plan"]) if subscription["plan"] in self.plans else {
                "name": "Gói Miễn Phí",
                "features": ["Giới hạn tính năng", "Giới hạn số lượng truy vấn"]
            }
            
            return {
                "success": True,
                "subscription": {
                    "plan": subscription["plan"],
                    "plan_name": plan_details.get("name", "Unknown"),
                    "start_date": subscription["start_date"].isoformat() if isinstance(subscription["start_date"], datetime) else subscription["start_date"],
                    "end_date": subscription["end_date"].isoformat() if isinstance(subscription["end_date"], datetime) else subscription["end_date"],
                    "is_active": is_active,
                    "auto_renew": subscription.get("auto_renew", False),
                    "features": plan_details.get("features", [])
                },
                "quota": {
                    "daily_limit": quota.get("daily_limit", 10),
                    "monthly_limit": quota.get("monthly_limit", 100),
                    "used_today": quota.get("used_today", 0),
                    "used_month": quota.get("used_month", 0),
                    "remaining_today": quota.get("daily_limit", 10) - quota.get("used_today", 0),
                    "remaining_month": quota.get("monthly_limit", 100) - quota.get("used_month", 0)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi kiểm tra gói dịch vụ: {str(e)}")
            return {
                "success": False,
                "message": f"Đã xảy ra lỗi: {str(e)}"
            }
    
    async def _upgrade_user_subscription(self, user_id: str, plan_id: str) -> None:
        """Nâng cấp gói dịch vụ của người dùng
        
        Args:
            user_id: ID người dùng
            plan_id: ID gói dịch vụ
        """
        try:
            # Lấy thông tin gói
            plan = self.plans[plan_id]
            
            # Tính thời gian hết hạn mới
            start_date = datetime.utcnow()
            end_date = start_date + timedelta(days=plan["duration"])
            
            # Cập nhật thông tin người dùng
            users_collection.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "subscription": {
                            "plan": plan_id,
                            "start_date": start_date,
                            "end_date": end_date,
                            "auto_renew": False
                        },
                        "quota": {
                            "daily_limit": plan["daily_limit"],
                            "monthly_limit": plan["monthly_limit"],
                            "used_today": 0,
                            "used_month": 0,
                            "reset_date": datetime.utcnow() + timedelta(days=1)
                        }
                    }
                }
            )
            
        except Exception as e:
            self.logger.error(f"Lỗi nâng cấp gói dịch vụ: {str(e)}")
            raise 