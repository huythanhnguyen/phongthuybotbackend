"""
Model Context Protocol (MCP) Server

MCP Server quản lý tài nguyên, templates và cấu hình cho các agent:
- Templates: Các mẫu prompt cho agents
- Parameters: Cấu hình cho các mô hình LLM
- Resources: Tài nguyên dùng chung (dữ liệu phân tích, hướng dẫn, v.v.)
"""

import os
import json
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

# Định nghĩa các models cho MCP

class TemplateParam(BaseModel):
    """Parameter trong template prompt"""
    name: str
    description: str
    default_value: Optional[Any] = None
    required: bool = False


class Template(BaseModel):
    """Template cho prompt"""
    id: str
    name: str
    description: str
    content: str
    parameters: List[TemplateParam] = Field(default_factory=list)
    version: str = "1.0.0"
    created_at: str
    updated_at: str


class ModelParameter(BaseModel):
    """Tham số cấu hình cho model"""
    name: str
    value: Any
    description: str


class ModelConfig(BaseModel):
    """Cấu hình cho model"""
    id: str
    name: str
    description: str
    model: str  # Tên model (gemini-pro, gemini-pro-vision, v.v.)
    parameters: List[ModelParameter] = Field(default_factory=list)
    version: str = "1.0.0"
    created_at: str
    updated_at: str


class Resource(BaseModel):
    """Tài nguyên dùng chung"""
    id: str
    name: str
    description: str
    content: Any
    type: str  # json, text, binary, v.v.
    version: str = "1.0.0"
    created_at: str
    updated_at: str


class MCPServer:
    """MCP Server triển khai"""
    
    def __init__(self, data_dir: str = None):
        """Khởi tạo MCP Server
        
        Args:
            data_dir: Thư mục lưu trữ dữ liệu. Mặc định là "./mcp_data"
        """
        self.data_dir = data_dir or "./mcp_data"
        self.templates: Dict[str, Template] = {}
        self.model_configs: Dict[str, ModelConfig] = {}
        self.resources: Dict[str, Resource] = {}
        
        # Tạo thư mục dữ liệu nếu chưa tồn tại
        os.makedirs(os.path.join(self.data_dir, "templates"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "model_configs"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "resources"), exist_ok=True)
        
        # Load dữ liệu từ disk
        self._load_data()
    
    def _load_data(self):
        """Load dữ liệu từ disk"""
        self._load_templates()
        self._load_model_configs()
        self._load_resources()
    
    def _load_templates(self):
        """Load templates từ disk"""
        templates_dir = os.path.join(self.data_dir, "templates")
        for filename in os.listdir(templates_dir):
            if filename.endswith(".json"):
                with open(os.path.join(templates_dir, filename), 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    template = Template(**template_data)
                    self.templates[template.id] = template
    
    def _load_model_configs(self):
        """Load model configs từ disk"""
        configs_dir = os.path.join(self.data_dir, "model_configs")
        for filename in os.listdir(configs_dir):
            if filename.endswith(".json"):
                with open(os.path.join(configs_dir, filename), 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    config = ModelConfig(**config_data)
                    self.model_configs[config.id] = config
    
    def _load_resources(self):
        """Load resources từ disk"""
        resources_dir = os.path.join(self.data_dir, "resources")
        for filename in os.listdir(resources_dir):
            if filename.endswith(".json"):
                with open(os.path.join(resources_dir, filename), 'r', encoding='utf-8') as f:
                    resource_data = json.load(f)
                    resource = Resource(**resource_data)
                    self.resources[resource.id] = resource
    
    def get_template(self, template_id: str) -> Optional[Template]:
        """Lấy template theo ID
        
        Args:
            template_id: ID của template
            
        Returns:
            Template nếu tìm thấy, None nếu không tồn tại
        """
        return self.templates.get(template_id)
    
    def get_model_config(self, config_id: str) -> Optional[ModelConfig]:
        """Lấy model config theo ID
        
        Args:
            config_id: ID của model config
            
        Returns:
            ModelConfig nếu tìm thấy, None nếu không tồn tại
        """
        return self.model_configs.get(config_id)
    
    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """Lấy resource theo ID
        
        Args:
            resource_id: ID của resource
            
        Returns:
            Resource nếu tìm thấy, None nếu không tồn tại
        """
        return self.resources.get(resource_id)


# Singleton instance of MCPServer
mcp_server = MCPServer() 