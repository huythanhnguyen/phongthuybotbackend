"""
Session Manager - Quản lý các phiên làm việc

Module này chứa các lớp và phương thức để quản lý phiên làm việc với người dùng,
lưu trữ và khôi phục trạng thái của phiên.
"""

import uuid
import time
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

# ADK imports
from google.adk.state import SessionState

logger = logging.getLogger(__name__)


class Session:
    """Đại diện cho một phiên làm việc với người dùng"""
    
    def __init__(
        self, 
        session_id: Optional[str] = None, 
        user_id: Optional[str] = None,
        state: Optional[SessionState] = None
    ):
        """Khởi tạo một phiên mới
        
        Args:
            session_id: ID của phiên, nếu không có sẽ tạo ID mới
            user_id: ID của người dùng
            state: Trạng thái phiên, nếu không có sẽ tạo mới
        """
        self.session_id = session_id or f"session-{uuid.uuid4()}"
        self.user_id = user_id
        self.state = state or SessionState()
        self.created_at = datetime.now()
        self.last_updated = self.created_at
        self.messages = []
    
    def update_timestamp(self):
        """Cập nhật thời gian sửa đổi cuối cùng"""
        self.last_updated = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi phiên thành dictionary để lưu trữ
        
        Returns:
            Dict[str, Any]: Dictionary đại diện cho phiên
        """
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "messages": self.messages
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        """Tạo phiên từ dictionary
        
        Args:
            data: Dictionary chứa dữ liệu phiên
            
        Returns:
            Session: Đối tượng phiên mới
        """
        session = cls(
            session_id=data.get("session_id"),
            user_id=data.get("user_id")
        )
        
        # Khôi phục timestamps
        if "created_at" in data:
            session.created_at = datetime.fromisoformat(data["created_at"])
        if "last_updated" in data:
            session.last_updated = datetime.fromisoformat(data["last_updated"])
        
        # Khôi phục messages
        session.messages = data.get("messages", [])
        
        return session


class SessionManager:
    """Quản lý các phiên làm việc"""
    
    def __init__(self, ttl: int = 3600, store_type: str = "memory"):
        """Khởi tạo Session Manager
        
        Args:
            ttl: Time-to-live cho phiên (giây)
            store_type: Loại lưu trữ ("memory", "redis", "mongo")
        """
        self.ttl = ttl
        self.store_type = store_type
        self.sessions = {}  # Lưu trữ trong bộ nhớ
        
        logger.info(f"Khởi tạo SessionManager với store_type={store_type}, ttl={ttl}s")
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Lấy phiên theo ID
        
        Args:
            session_id: ID của phiên cần lấy
            
        Returns:
            Session: Phiên tìm thấy hoặc None
        """
        if not session_id:
            return None
        
        if session_id in self.sessions:
            # Kiểm tra xem phiên đã hết hạn chưa
            session = self.sessions[session_id]
            if self._is_expired(session):
                logger.info(f"Phiên {session_id} đã hết hạn, xóa phiên")
                self.delete_session(session_id)
                return None
            return session
        
        return None
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> Session:
        """Lấy phiên nếu tồn tại, nếu không tạo phiên mới
        
        Args:
            session_id: ID của phiên cần lấy
            
        Returns:
            Session: Phiên hiện có hoặc mới
        """
        if session_id:
            session = self.get_session(session_id)
            if session:
                return session
        
        # Tạo phiên mới
        session = Session(session_id)
        self.save_session(session)
        logger.info(f"Tạo phiên mới với ID {session.session_id}")
        
        return session
    
    def save_session(self, session: Session) -> bool:
        """Lưu phiên vào kho lưu trữ
        
        Args:
            session: Phiên cần lưu
            
        Returns:
            bool: True nếu lưu thành công
        """
        session.update_timestamp()
        self.sessions[session.session_id] = session
        logger.debug(f"Đã lưu phiên {session.session_id}")
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """Xóa phiên khỏi kho lưu trữ
        
        Args:
            session_id: ID của phiên cần xóa
            
        Returns:
            bool: True nếu xóa thành công
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Đã xóa phiên {session_id}")
            return True
        
        logger.warning(f"Không tìm thấy phiên {session_id} để xóa")
        return False
    
    def list_sessions(self, user_id: Optional[str] = None) -> List[Session]:
        """Liệt kê tất cả các phiên
        
        Args:
            user_id: Nếu có, chỉ liệt kê phiên của người dùng cụ thể
            
        Returns:
            List[Session]: Danh sách các phiên
        """
        sessions = []
        for session in self.sessions.values():
            if user_id and session.user_id != user_id:
                continue
            
            if not self._is_expired(session):
                sessions.append(session)
        
        return sessions
    
    def cleanup_expired_sessions(self) -> int:
        """Xóa các phiên đã hết hạn
        
        Returns:
            int: Số phiên đã xóa
        """
        expired_sessions = []
        for session_id, session in self.sessions.items():
            if self._is_expired(session):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.delete_session(session_id)
        
        logger.info(f"Đã xóa {len(expired_sessions)} phiên hết hạn")
        return len(expired_sessions)
    
    def _is_expired(self, session: Session) -> bool:
        """Kiểm tra xem phiên đã hết hạn chưa
        
        Args:
            session: Phiên cần kiểm tra
            
        Returns:
            bool: True nếu phiên đã hết hạn
        """
        elapsed = (datetime.now() - session.last_updated).total_seconds()
        return elapsed > self.ttl 