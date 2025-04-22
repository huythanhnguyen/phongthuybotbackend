"""
MCP - Module chính cho các chức năng phân tích và quản lý tài nguyên

Module này chứa các hàm và công cụ chung được sử dụng
trong các chức năng phân tích của Phong Thủy Số, cũng như
các thành phần quản lý tài nguyên và cấu hình cho các agents.
"""

# Import từ server.py - Quản lý tài nguyên và cấu hình
from .server import (
    TemplateParam,
    Template,
    ModelParameter,
    ModelConfig,
    Resource,
    MCPServer,
    mcp_server
)

# Import từ common.py - Các hàm tiện ích chung
from .common import (
    extract_digits,
    calculate_energy_number,
    get_five_element,
    get_energy_meaning,
    is_lucky_number,
    is_unlucky_number
)

__all__ = [
    # Server components
    'TemplateParam',
    'Template',
    'ModelParameter',
    'ModelConfig',
    'Resource',
    'MCPServer',
    'mcp_server',
    
    # Common utilities
    'extract_digits',
    'calculate_energy_number',
    'get_five_element',
    'get_energy_meaning',
    'is_lucky_number',
    'is_unlucky_number'
] 