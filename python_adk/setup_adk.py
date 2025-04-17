"""
Script cài đặt Google ADK và các dependencies cần thiết
"""

import os
import sys
import subprocess

def main():
    print("==> Đang cài đặt Google ADK và các dependencies...")
    
    # Cài đặt dependencies cần thiết
    requirements = [
        "google-adk>=0.1.0",
        "google-generativeai>=0.3.0",
        "git+https://github.com/google/adk-python.git",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "python-multipart>=0.0.6"
    ]
    
    for req in requirements:
        print(f"==> Đang cài đặt {req}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        except subprocess.CalledProcessError as e:
            print(f"==> Lỗi khi cài đặt {req}: {e}")
            
    # Thiết lập PYTHONPATH
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    pythonpath = os.environ.get("PYTHONPATH", "")
    if parent_dir not in pythonpath:
        os.environ["PYTHONPATH"] = f"{pythonpath}:{parent_dir}" if pythonpath else parent_dir
        print(f"==> Đã thêm {parent_dir} vào PYTHONPATH")
    
    print("==> Cài đặt hoàn tất!")
    
if __name__ == "__main__":
    main() 