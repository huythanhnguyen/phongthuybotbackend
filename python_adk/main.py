"""
Main Entry Point

Điểm vào chính của ứng dụng Phong Thủy Số.
"""

import os
import sys
import argparse
import logging
from typing import Dict, Optional

from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI

# Import the root agent instance directly
from python_adk.agents import root_agent
from python_adk.shared_libraries.logger import get_logger

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Phong Thủy Số API",
    description="API cho ứng dụng phân tích phong thủy số học",
    version="0.1.0"
)

def configure_logging():
    """Cấu hình logging cho ứng dụng"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # Cấu hình cơ bản cho logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "app.log")),
            logging.StreamHandler(sys.stdout)
        ]
    )


def configure_gemini(api_key: Optional[str] = None):
    """
    Cấu hình Gemini API
    
    Args:
        api_key (Optional[str]): API key cho Gemini, nếu không cung cấp sẽ lấy từ môi trường
    """
    # Lấy API key từ môi trường nếu không được cung cấp
    if not api_key:
        # Ưu tiên lấy từ GOOGLE_API_KEY
        api_key = os.getenv("GOOGLE_API_KEY")
        
        # Nếu không tìm thấy, thử lấy từ GEMINI_API_KEY
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")
        
    if not api_key:
        raise ValueError("Không tìm thấy API key. Vui lòng cung cấp GOOGLE_API_KEY hoặc GEMINI_API_KEY trong môi trường hoặc trực tiếp.")
    
    # Cấu hình Gemini
    genai.configure(api_key=api_key)


def run_interactive_shell(model_name: str):
    """
    Chạy shell tương tác với agent
    
    Args:
        model_name (str): Tên model Gemini sử dụng
    """
    logger = get_logger("InteractiveShell")
    logger.info(f"Khởi động shell tương tác với model {model_name}")
    
    # Sử dụng root_agent đã được khởi tạo
    # Lưu ý: model_name từ command line hiện không được sử dụng để cấu hình lại root_agent
    # Nếu cần cấu hình model động, cần cơ chế khác.
    
    print("\n===== Phong Thủy Số - Interactive Shell =====")
    print("Nhập 'exit' hoặc 'quit' để thoát\n")
    
    while True:
        try:
            # Nhận input từ người dùng
            user_input = input("\nBạn: ")
            
            # Kiểm tra thoát
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Tạm biệt!")
                break
            
            # Xử lý input với Root Agent (instance đã import)
            # Lưu ý: Phương thức 'run' không tồn tại trên GeminiAgent, sử dụng 'invoke'
            # Xử lý input với Root Agent
            response = root_agent.invoke(user_input)
            
            # Hiển thị phản hồi
            print(f"\nPhong Thủy Số: {response}")
            
        except KeyboardInterrupt:
            print("\nTạm biệt!")
            break
        except Exception as e:
            logger.error(f"Lỗi: {e}")
            print(f"\nCó lỗi xảy ra: {e}")


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Phong Thủy Số - Ứng dụng phân tích phong thủy số học")
    
    parser.add_argument(
        "--model", 
        type=str, 
        default="gemini-1.5-pro",
        help="Model Gemini sử dụng (mặc định: gemini-1.5-pro)"
    )
    
    parser.add_argument(
        "--api-key", 
        type=str, 
        help="Google API key cho Gemini (nếu không cung cấp, sẽ lấy từ GOOGLE_API_KEY hoặc GEMINI_API_KEY trong môi trường)"
    )
    
    return parser.parse_args()


def main():
    """Main entry point của ứng dụng"""
    # Load environment variables
    load_dotenv()
    
    # Cấu hình logging
    configure_logging()
    
    # Parse command line arguments
    args = parse_arguments()
    
    try:
        # Cấu hình Gemini
        configure_gemini(api_key=args.api_key)
        
        # Chạy shell tương tác
        run_interactive_shell(model_name=args.model)
        
    except Exception as e:
        logging.error(f"Lỗi khi khởi động ứng dụng: {e}")
        print(f"Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

@app.get("/health")
async def health_check():
    """
    Endpoint kiểm tra trạng thái hoạt động của ứng dụng.
    Sử dụng bởi Docker healthcheck.
    """
    return {"status": "healthy", "version": "0.1.0"} 
