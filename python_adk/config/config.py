"""
Configuration Manager - Quản lý cấu hình của hệ thống

Module này chứa các lớp và phương thức liên quan đến cấu hình hệ thống,
đọc từ biến môi trường và file cấu hình.
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional


class AppConfig:
    """Quản lý cấu hình của ứng dụng"""
    
    def __init__(self, env_file: Optional[str] = None):
        """Khởi tạo cấu hình từ file môi trường
        
        Args:
            env_file: Đường dẫn đến file môi trường (.env)
        """
        # Load biến môi trường
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        # API settings
        self.api_key = os.getenv("API_KEY", "render_production_key")
        self.api_key_header = os.getenv("API_KEY_HEADER", "X-API-Key")
        self.port = int(os.getenv("PORT", 10000))
        
        # LLM settings
        self.use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0") == "1"
        self.api_key_genai = os.getenv("GOOGLE_API_KEY", None)
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", None)
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        # Agent settings
        self.root_agent_model = os.getenv("ROOT_AGENT_MODEL", "gemini-pro")
        self.specialist_agent_model = os.getenv("SPECIALIST_AGENT_MODEL", "gemini-pro")
        
        # Session settings
        self.session_ttl = int(os.getenv("SESSION_TTL", 3600))  # 1 hour in seconds
        self.session_store_type = os.getenv("SESSION_STORE_TYPE", "memory")
        self.session_redis_url = os.getenv("SESSION_REDIS_URL", None)
        
        # Database settings
        self.mongo_uri = os.getenv("MONGO_URI", None)
        self.mongo_db_name = os.getenv("MONGO_DB_NAME", "phongthuybot")
        
        # Logging settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Initialize other configurations
        self._init_configs()
    
    def _init_configs(self):
        """Khởi tạo cấu hình bổ sung"""
        # Cài đặt LLM
        self.llm_config = {
            "use_vertex": self.use_vertex,
            "api_key": self.api_key_genai,
            "project_id": self.project_id,
            "location": self.location
        }
        
        # Cài đặt session
        self.session_config = {
            "ttl": self.session_ttl,
            "store_type": self.session_store_type,
            "redis_url": self.session_redis_url
        }
        
        # Cài đặt database
        self.db_config = {
            "mongo_uri": self.mongo_uri,
            "db_name": self.mongo_db_name
        }
    
    def get_agent_config(self, agent_type: str) -> Dict[str, Any]:
        """Lấy cấu hình cho một loại agent cụ thể
        
        Args:
            agent_type: Loại agent (root, phone, cccd, ...)
            
        Returns:
            Dict[str, Any]: Cấu hình của agent
        """
        # Cấu hình chung cho tất cả các agent
        base_config = {
            "model": self.specialist_agent_model,
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 40,
            "llm_config": self.llm_config
        }
        
        # Cấu hình riêng cho từng loại agent
        if agent_type == "root":
            base_config["model"] = self.root_agent_model
            base_config["temperature"] = 0.1
        
        return base_config
    
    def __str__(self) -> str:
        """Biểu diễn chuỗi của cấu hình"""
        return f"AppConfig(api_key={'*'*8}, use_vertex={self.use_vertex}, session_store={self.session_store_type})" 