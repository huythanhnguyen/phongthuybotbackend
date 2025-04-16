"""
Phone Analyzer Tool - Công cụ phân tích số điện thoại theo Bát Cục Linh Số

Tool này phân tích số điện thoại theo phương pháp Bát Cục Linh Số, đưa ra 
ý nghĩa phong thủy và lời khuyên.
"""

import re
import os
import logging
from typing import Dict, Any, List, Optional

# Google ADK imports
from adk.core.tool import Tool
from adk.generators.llm import LLMGenerator


class PhoneAnalyzer(Tool):
    """Tool phân tích số điện thoại theo Bát Cục Linh Số"""
    
    def __init__(self):
        """Khởi tạo Phone Analyzer Tool"""
        super().__init__(
            name="phone_analyzer",
            description="Phân tích số điện thoại theo phương pháp Bát Cục Linh Số",
            parameters=[
                {
                    "name": "phone_number",
                    "type": "string",
                    "description": "Số điện thoại cần phân tích",
                    "required": True
                }
            ],
            returns={
                "type": "object",
                "description": "Kết quả phân tích số điện thoại",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Trạng thái thành công"
                    },
                    "content": {
                        "type": "string",
                        "description": "Nội dung phân tích"
                    },
                    "phone_number": {
                        "type": "string",
                        "description": "Số điện thoại đã phân tích"
                    },
                    "error": {
                        "type": "string",
                        "description": "Thông báo lỗi nếu có"
                    }
                }
            }
        )
        
        # Khởi tạo logger
        self.logger = logging.getLogger("PhoneAnalyzer")
        
        # Khởi tạo LLM Generator cho phân tích nâng cao
        model_name = os.environ.get("PHONE_ANALYZER_MODEL", "gemini-pro")
        self.generator = LLMGenerator(name="phone-analyzer-generator", model=model_name)
        
        self.logger.info("Phone Analyzer Tool đã được khởi tạo")
    
    def extract_phone_number(self, text: str) -> Optional[str]:
        """Trích xuất số điện thoại từ văn bản
        
        Args:
            text: Văn bản chứa số điện thoại
            
        Returns:
            str: Số điện thoại đã trích xuất hoặc None nếu không tìm thấy
        """
        # Mẫu regex cho số điện thoại Việt Nam
        patterns = [
            r'0\d{9}',  # 10 chữ số, bắt đầu bằng 0
            r'0\d{8}',  # 9 chữ số, bắt đầu bằng 0
            r'\+84\d{9}',  # +84 và 9 chữ số
            r'84\d{9}'  # 84 và 9 chữ số
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.replace(' ', '').replace('.', '').replace('-', ''))
            if matches:
                return matches[0]
        
        return None
    
    def is_valid_phone_number(self, phone_number: str) -> bool:
        """Kiểm tra tính hợp lệ của số điện thoại Việt Nam
        
        Args:
            phone_number: Số điện thoại cần kiểm tra
            
        Returns:
            bool: True nếu hợp lệ, False nếu không
        """
        # Chuẩn hóa số điện thoại
        phone = phone_number.replace(' ', '').replace('.', '').replace('-', '')
        
        # Kiểm tra độ dài và tiền tố
        if re.match(r'^0\d{9}$', phone):  # 10 chữ số, bắt đầu bằng 0
            return True
        if re.match(r'^\+84\d{9}$', phone):  # +84 và 9 chữ số
            return True
        if re.match(r'^84\d{9}$', phone):  # 84 và 9 chữ số
            return True
        
        return False
    
    def normalize_phone_number(self, phone_number: str) -> str:
        """Chuẩn hóa số điện thoại về định dạng thống nhất
        
        Args:
            phone_number: Số điện thoại cần chuẩn hóa
            
        Returns:
            str: Số điện thoại đã chuẩn hóa
        """
        # Loại bỏ khoảng trắng, dấu chấm, dấu gạch ngang
        phone = phone_number.replace(' ', '').replace('.', '').replace('-', '')
        
        # Chuyển đổi từ +84/84 sang 0
        if phone.startswith('+84'):
            phone = '0' + phone[3:]
        elif phone.startswith('84') and len(phone) >= 10:
            phone = '0' + phone[2:]
        
        return phone
    
    def calculate_total_value(self, phone_number: str) -> int:
        """Tính tổng giá trị số học của số điện thoại
        
        Args:
            phone_number: Số điện thoại cần tính toán
            
        Returns:
            int: Tổng giá trị
        """
        # Tính tổng tất cả các chữ số
        total = sum(int(digit) for digit in phone_number if digit.isdigit())
        
        # Giảm xuống thành số có 1 chữ số
        while total > 9:
            total = sum(int(digit) for digit in str(total))
        
        return total
    
    def get_element(self, number: int) -> str:
        """Lấy ngũ hành tương ứng với số
        
        Args:
            number: Số cần xác định ngũ hành
            
        Returns:
            str: Ngũ hành (Kim, Mộc, Thủy, Hỏa, Thổ)
        """
        elements = {
            1: "Thủy",  # Thủy sinh Mộc
            2: "Thổ",   # Thổ sinh Kim
            3: "Mộc",   # Mộc sinh Hỏa
            4: "Kim",   # Kim sinh Thủy
            5: "Thổ",   # Trung tâm, Thổ
            6: "Kim",   # Kim sinh Thủy
            7: "Kim",   # Kim sinh Thủy
            8: "Thổ",   # Thổ sinh Kim
            9: "Hỏa",   # Hỏa sinh Thổ
            0: "Thủy"   # Thủy sinh Mộc
        }
        
        return elements.get(number, "Không xác định")
    
    def extract_pairs(self, phone_number: str) -> Dict[str, List[str]]:
        """Trích xuất các cặp số từ số điện thoại
        
        Args:
            phone_number: Số điện thoại cần trích xuất
            
        Returns:
            Dict[str, List[str]]: Từ điển các cặp số theo vị trí
        """
        pairs = {
            "first": [],   # Cặp số đầu
            "middle": [],  # Cặp số giữa
            "last": []     # Cặp số cuối
        }
        
        # Loại bỏ tiền tố 0 nếu có
        if phone_number.startswith('0'):
            phone = phone_number[1:]
        else:
            phone = phone_number
        
        # Trích xuất cặp số đầu (2 số đầu tiên)
        if len(phone) >= 2:
            pairs["first"].append(phone[:2])
        
        # Trích xuất cặp số giữa (2-3 số giữa)
        if len(phone) >= 5:
            middle_start = 2
            middle_end = len(phone) - 2
            middle_length = middle_end - middle_start
            
            if middle_length == 2:
                pairs["middle"].append(phone[middle_start:middle_end])
            elif middle_length >= 3:
                # Chia thành các cặp số
                for i in range(middle_start, middle_end - 1, 2):
                    if i + 1 < len(phone):
                        pairs["middle"].append(phone[i:i+2])
        
        # Trích xuất cặp số cuối (2 số cuối cùng)
        if len(phone) >= 2:
            pairs["last"].append(phone[-2:])
        
        return pairs
    
    async def analyze(self, message: str) -> Dict[str, Any]:
        """Phân tích số điện thoại từ tin nhắn
        
        Args:
            message: Nội dung tin nhắn chứa số điện thoại
            
        Returns:
            Dict[str, Any]: Kết quả phân tích
        """
        # Trích xuất số điện thoại từ tin nhắn
        phone_number = self.extract_phone_number(message)
        
        if not phone_number:
            return {
                "success": False,
                "error": "Không tìm thấy số điện thoại hợp lệ trong tin nhắn của bạn. Vui lòng cung cấp số điện thoại theo định dạng Việt Nam (VD: 0912345678).",
                "content": "Xin lỗi, tôi không tìm thấy số điện thoại hợp lệ trong tin nhắn của bạn. Vui lòng cung cấp số điện thoại theo định dạng Việt Nam (VD: 0912345678)."
            }
        
        # Kiểm tra tính hợp lệ
        if not self.is_valid_phone_number(phone_number):
            return {
                "success": False,
                "error": f"Số điện thoại '{phone_number}' không hợp lệ. Vui lòng cung cấp số điện thoại Việt Nam hợp lệ.",
                "content": f"Số điện thoại '{phone_number}' không hợp lệ. Vui lòng cung cấp số điện thoại Việt Nam hợp lệ."
            }
        
        # Chuẩn hóa số điện thoại
        normalized_phone = self.normalize_phone_number(phone_number)
        
        # Tính tổng giá trị
        total_value = self.calculate_total_value(normalized_phone)
        
        # Xác định ngũ hành
        element = self.get_element(total_value)
        
        # Trích xuất các cặp số
        pairs = self.extract_pairs(normalized_phone)
        
        # Phân tích số điện thoại bằng LLM
        analysis_prompt = f"""
        Hãy phân tích số điện thoại {normalized_phone} theo phương pháp Bát Cục Linh Số với các thông tin sau:
        
        1. Tổng số (Lộ số): {total_value} - Ngũ hành: {element}
        2. Cặp số đầu: {', '.join(pairs['first'])}
        3. Cặp số giữa: {', '.join(pairs['middle'])}
        4. Cặp số cuối: {', '.join(pairs['last'])}
        
        Phân tích chi tiết về:
        - Ý nghĩa tổng số và ngũ hành tương ứng
        - Ý nghĩa của từng cặp số (đầu, giữa, cuối)
        - Sự cân bằng âm dương (số chẵn/lẻ)
        - Quẻ chủ đạo và ý nghĩa
        - Điểm mạnh và điểm yếu
        - Đánh giá tổng thể (tốt/trung bình/không tốt)
        - Mức độ phù hợp với các mục đích: kinh doanh, sự nghiệp, tình duyên, tài chính
        
        Định dạng kết quả đẹp, dễ đọc với các tiêu đề và đoạn văn ngắn gọn.
        """
        
        try:
            response = await self.generator.generate(analysis_prompt)
            analysis_result = response.text
            
            return {
                "success": True,
                "phone_number": normalized_phone,
                "content": analysis_result
            }
        except Exception as e:
            self.logger.error(f"Lỗi khi phân tích số điện thoại: {str(e)}")
            
            # Trả về kết quả đơn giản nếu gặp lỗi
            basic_analysis = f"""
            Phân tích số điện thoại: {normalized_phone}
            
            Tổng số (Lộ số): {total_value}
            Ngũ hành: {element}
            
            Cặp số đầu: {', '.join(pairs['first'])}
            Cặp số giữa: {', '.join(pairs['middle'])}
            Cặp số cuối: {', '.join(pairs['last'])}
            
            Vì gặp lỗi khi phân tích chi tiết, chỉ có thể cung cấp phân tích cơ bản.
            """
            
            return {
                "success": True,
                "phone_number": normalized_phone,
                "content": basic_analysis,
                "error": str(e)
            }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Thực thi tool với tham số từ ADK
        
        Args:
            **kwargs: Tham số, bao gồm phone_number
            
        Returns:
            Dict[str, Any]: Kết quả phân tích
        """
        phone_number = kwargs.get("phone_number", "")
        
        if not phone_number:
            return {
                "success": False,
                "error": "Thiếu tham số phone_number"
            }
        
        return await self.analyze(phone_number) 