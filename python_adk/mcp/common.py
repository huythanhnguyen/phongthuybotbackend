"""
Các hàm tiện ích chung được sử dụng trong nhiều module
"""

import re
from typing import Dict, Any, List, Optional

def extract_digits(text: str) -> str:
    """
    Trích xuất các chữ số từ một chuỗi.
    
    Args:
        text (str): Chuỗi cần xử lý
        
    Returns:
        str: Chuỗi chỉ chứa các chữ số
    """
    if not text:
        return ""
    
    return ''.join(filter(str.isdigit, text))

def calculate_energy_number(digits: str) -> int:
    """
    Tính toán số năng lượng dựa trên tổng các chữ số.
    
    Args:
        digits (str): Chuỗi chữ số
        
    Returns:
        int: Số năng lượng (1-9)
    """
    if not digits:
        return 0
    
    # Tính tổng các chữ số
    digit_sum = sum(int(d) for d in digits)
    
    # Rút gọn thành một chữ số (1-9)
    return digit_sum % 9 or 9

def get_five_element(number: int) -> str:
    """
    Xác định ngũ hành dựa trên số.
    
    Args:
        number (int): Số cần xác định ngũ hành
        
    Returns:
        str: Tên ngũ hành
    """
    five_elements_map = {
        1: "Thủy",
        2: "Thổ",
        3: "Mộc",
        4: "Kim",
        5: "Thổ",
        6: "Kim",
        7: "Thủy",
        8: "Mộc",
        9: "Hỏa"
    }
    
    return five_elements_map.get(number, "Không xác định")

def get_energy_meaning(number: int) -> str:
    """
    Lấy ý nghĩa của số năng lượng.
    
    Args:
        number (int): Số năng lượng (1-9)
        
    Returns:
        str: Ý nghĩa của số năng lượng
    """
    energy_meanings = {
        1: "Chủ động, sáng tạo, khởi đầu mới, độc lập",
        2: "Hợp tác, cân bằng, kiên nhẫn, bền bỉ",
        3: "Phát triển, mở rộng, linh hoạt, sáng tạo",
        4: "Ổn định, chắc chắn, kỷ luật, xây dựng",
        5: "Thay đổi, linh hoạt, tự do, phiêu lưu",
        6: "Hài hòa, trách nhiệm, phụng sự, cống hiến",
        7: "Phân tích, chiêm nghiệm, trí tuệ, tâm linh",
        8: "Thịnh vượng, quyền lực, thành tựu, vật chất",
        9: "Hoàn thành, viên mãn, lý tưởng, nhân đạo"
    }
    
    return energy_meanings.get(number, "Không xác định")

def is_lucky_number(number: str) -> bool:
    """
    Kiểm tra một số có phải là số may mắn không.
    
    Args:
        number (str): Số cần kiểm tra
        
    Returns:
        bool: True nếu là số may mắn, False nếu không
    """
    lucky_numbers = ['6', '8', '9']
    return number in lucky_numbers

def is_unlucky_number(number: str) -> bool:
    """
    Kiểm tra một số có phải là số không may mắn không.
    
    Args:
        number (str): Số cần kiểm tra
        
    Returns:
        bool: True nếu là số không may mắn, False nếu không
    """
    unlucky_numbers = ['4', '7']
    return number in unlucky_numbers 