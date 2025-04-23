#!/usr/bin/env python
"""
Debug Tool - Công cụ kiểm tra môi trường Python và các cấu hình

Công cụ này giúp kiểm tra:
1. Phiên bản Python
2. Các gói thư viện đã cài đặt và phiên bản
3. Cấu trúc import của Google ADK
4. Các biến môi trường cần thiết
"""

import sys
import os
import pkg_resources
import subprocess
import importlib.util
from typing import Dict, List, Optional, Tuple

# Định nghĩa các màu để in ra console
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(title: str) -> None:
    """In tiêu đề được định dạng đẹp"""
    width = 80
    print(f"\n{BOLD}{BLUE}{'=' * width}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * ((width - len(title)) // 2)} {title} {'=' * ((width - len(title)) // 2)}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * width}{RESET}\n")

def check_python_version() -> str:
    """Kiểm tra phiên bản Python"""
    version = sys.version.split()[0]
    return version

def check_package_installed(package_name: str) -> Tuple[bool, Optional[str]]:
    """Kiểm tra xem gói đã được cài đặt hay chưa và phiên bản của nó"""
    try:
        package = pkg_resources.get_distribution(package_name)
        return True, package.version
    except pkg_resources.DistributionNotFound:
        return False, None

def check_critical_packages() -> Dict[str, Dict[str, any]]:
    """Kiểm tra các gói quan trọng đã được cài đặt chưa"""
    packages = {
        "google-generativeai": {"installed": False, "version": None, "min_version": "0.2.0"},
        "google-adk": {"installed": False, "version": None, "min_version": "0.2.0"},
        "fastapi": {"installed": False, "version": None, "min_version": "0.89.0"},
        "pydantic": {"installed": False, "version": None, "min_version": "2.0.0"},
        "python-dotenv": {"installed": False, "version": None, "min_version": "0.21.0"},
        "uvicorn": {"installed": False, "version": None, "min_version": "0.20.0"}
    }
    
    for package_name in packages:
        installed, version = check_package_installed(package_name)
        packages[package_name]["installed"] = installed
        packages[package_name]["version"] = version
        
        # Kiểm tra phiên bản tối thiểu
        if installed and version:
            min_version = packages[package_name]["min_version"]
            packages[package_name]["is_minimum_version"] = pkg_resources.parse_version(version) >= pkg_resources.parse_version(min_version)
        else:
            packages[package_name]["is_minimum_version"] = False
    
    return packages

def check_google_adk_modules() -> Dict[str, Dict[str, bool]]:
    """Kiểm tra các module Google ADK"""
    modules = {
        "Google ADK": {
            "import": False,
            "tools": False,
            "type_inference": False,
            "agent_tools": False
        }
    }
    
    # Kiểm tra import google.adk
    try:
        import google.adk
        modules["Google ADK"]["import"] = True
        
        # Kiểm tra các module con
        try:
            # Kiểm tra API mới (từ v0.2.0 trở lên)
            from google.adk.tools.agent_tool import AgentTool
            from google.adk.tools import agent_tool_registry
            modules["Google ADK"]["tools"] = True
        except ImportError:
            # Thử kiểm tra API cũ
            try:
                from google.adk.tools.agent_tool import agent_tool, agent_tool_registry
                modules["Google ADK"]["tools"] = True
                modules["Google ADK"]["old_api"] = True
            except ImportError:
                modules["Google ADK"]["old_api"] = False
        
        try:
            from google.adk.type_inference import annotate_type
            modules["Google ADK"]["type_inference"] = True
        except ImportError:
            pass
            
    except ImportError:
        pass
    
    return modules

def check_environment_variables() -> Dict[str, bool]:
    """Kiểm tra các biến môi trường cần thiết"""
    env_vars = {
        "GEMINI_API_KEY": False,
        "PORT": False,
        "HOST": False,
    }
    
    for var in env_vars:
        if os.environ.get(var):
            env_vars[var] = True
    
    return env_vars

def check_imp_module_status() -> Dict[str, bool]:
    """Kiểm tra tình trạng của module 'imp' đã bị loại bỏ trong Python 3.13"""
    status = {
        "exists": False,
        "error_message": None
    }
    
    try:
        import imp
        status["exists"] = True
    except ImportError as e:
        status["error_message"] = str(e)
    
    return status

def check_deprecated_modules() -> Dict[str, Dict[str, any]]:
    """Kiểm tra các module đã bị loại bỏ trong Python 3.13"""
    deprecated_modules = {
        "imp": check_imp_module_status()
    }
    
    return deprecated_modules

def main():
    """Hàm chính thực hiện kiểm tra và hiển thị kết quả"""
    print_header("Công cụ kiểm tra môi trường Python và Google ADK")
    
    # Kiểm tra phiên bản Python
    python_version = check_python_version()
    print(f"{BOLD}Phiên bản Python:{RESET} {BLUE}{python_version}{RESET}")
    if python_version.startswith("3.13"):
        print(f"{YELLOW}Phát hiện Python 3.13 - Một số module cũ có thể đã bị loại bỏ{RESET}")
    
    # Kiểm tra các gói quan trọng
    print_header("Kiểm tra các gói quan trọng")
    packages = check_critical_packages()
    all_packages_installed = True
    
    for package_name, package_info in packages.items():
        if package_info["installed"]:
            version_info = f"{GREEN}{package_info['version']}{RESET}"
            if not package_info["is_minimum_version"]:
                version_info = f"{YELLOW}{package_info['version']} (Cần >= {package_info['min_version']}){RESET}"
                all_packages_installed = False
            print(f"{BOLD}{package_name}:{RESET} {version_info}")
        else:
            print(f"{BOLD}{package_name}:{RESET} {RED}Chưa cài đặt{RESET}")
            all_packages_installed = False
    
    # Kiểm tra module Google ADK  
    print_header("Kiểm tra cấu trúc Google ADK")
    adk_modules = check_google_adk_modules()
    all_adk_modules_ok = True
    
    for module_name, module_status in adk_modules.items():
        print(f"{BOLD}{module_name}:{RESET}")
        for submodule, status in module_status.items():
            if submodule == "old_api":
                if status:
                    print(f"  - {submodule}: {YELLOW}Sử dụng API cũ, nên nâng cấp lên v0.2.0+{RESET}")
                continue
                
            status_text = f"{GREEN}OK{RESET}" if status else f"{RED}Lỗi{RESET}"
            print(f"  - {submodule}: {status_text}")
            if not status:
                all_adk_modules_ok = False
    
    # Kiểm tra các module bị loại bỏ trong Python 3.13
    print_header("Kiểm tra tương thích Python 3.13")
    deprecated = check_deprecated_modules()
    
    for module_name, status in deprecated.items():
        if status["exists"]:
            print(f"{BOLD}{module_name}:{RESET} {GREEN}Có thể import{RESET}")
        else:
            print(f"{BOLD}{module_name}:{RESET} {RED}Không thể import{RESET}")
            if status["error_message"]:
                print(f"  - Lỗi: {RED}{status['error_message']}{RESET}")
                print(f"  - {YELLOW}Module này đã bị loại bỏ trong Python 3.13, cần thay đổi mã nguồn{RESET}")
    
    # Kiểm tra các biến môi trường
    print_header("Kiểm tra biến môi trường")
    env_vars = check_environment_variables()
    all_env_vars_set = True
    
    for var_name, is_set in env_vars.items():
        status_text = f"{GREEN}Đã cài đặt{RESET}" if is_set else f"{RED}Chưa cài đặt{RESET}"
        print(f"{BOLD}{var_name}:{RESET} {status_text}")
        if not is_set:
            all_env_vars_set = False
    
    # Kiểm tra cách import Google ADK với API mới
    print_header("Ví dụ về cách import Google ADK đúng")
    print(f"{CYAN}# API mới (Google ADK >= 0.2.0, Python 3.13+){RESET}")
    print(f"{CYAN}from google.adk.tools.agent_tool import AgentTool{RESET}")
    print(f"{CYAN}from google.adk.tools import agent_tool_registry{RESET}")
    print(f"{CYAN}from google.adk.type_inference import annotate_type{RESET}")
    print(f"{CYAN}{RESET}")
    print(f"{CYAN}@agent_tool_registry.register{RESET}")
    print(f"{CYAN}@annotate_type{RESET}")
    print(f"{CYAN}def my_tool(param1: str) -> str:{RESET}")
    print(f"{CYAN}    return f\"Tool output: {{param1}}\"{RESET}")
    
    # Tổng kết
    print_header("Tóm tắt kiểm tra")
    summary_ok = all_packages_installed and all_adk_modules_ok and all_env_vars_set
    
    if summary_ok:
        print(f"{GREEN}✓ Tất cả kiểm tra đều thành công. Môi trường đã sẵn sàng!{RESET}")
    else:
        print(f"{YELLOW}⚠ Phát hiện một số vấn đề cần giải quyết trước khi chạy ứng dụng.{RESET}")
        
        if not all_packages_installed:
            print(f"{YELLOW}- Một số gói thư viện cần được cài đặt hoặc nâng cấp.{RESET}")
        
        if not all_adk_modules_ok:
            print(f"{YELLOW}- Một số module Google ADK không thể import được.{RESET}")
            if adk_modules["Google ADK"].get("old_api", False):
                print(f"{YELLOW}  → Bạn đang sử dụng API cũ, hãy nâng cấp lên v0.2.0+ và sửa cách import.{RESET}")
        
        if not all_env_vars_set:
            print(f"{YELLOW}- Một số biến môi trường cần được cài đặt trong file .env.{RESET}")
        
        if python_version.startswith("3.13") and "imp" in deprecated and not deprecated["imp"]["exists"]:
            print(f"{YELLOW}- Python 3.13 không còn hỗ trợ module 'imp', cần cập nhật mã nguồn.{RESET}")
            print(f"{YELLOW}  → Xem các lưu ý trong README.md.{RESET}")

if __name__ == "__main__":
    main() 