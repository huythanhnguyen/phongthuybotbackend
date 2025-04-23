import os
import subprocess
import sys

# Kiểm tra và cài đặt các phụ thuộc nếu cần
def install_dependencies():
    print("Kiểm tra và cài đặt các phụ thuộc...")
    try:
        import pip
        with open('requirements.txt', 'r') as file:
            packages = file.readlines()
        for package in packages:
            package = package.strip()
            if package and not package.startswith('#'):
                try:
                    __import__(package.split('==')[0].replace('-', '_'))
                except ImportError:
                    print(f"Cài đặt {package}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Lỗi khi cài đặt phụ thuộc: {e}")
        sys.exit(1)

# Chạy ứng dụng FastAPI
def run_app():
    print("Khởi động ứng dụng FastAPI...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, "main.py", "--model", "gemini-1.5-pro"])

if __name__ == "__main__":
    install_dependencies()
    run_app() 