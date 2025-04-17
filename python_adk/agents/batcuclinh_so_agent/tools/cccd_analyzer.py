"""
CCCD Analyzer Tool - Công cụ phân tích số CCCD/CMND theo Bát Cục Linh Số

Tool này phân tích số Căn cước công dân/Chứng minh nhân dân theo phương pháp Bát Cục Linh Số,
đưa ra ý nghĩa phong thủy và lời khuyên.
"""

import os
import logging
import re
import random
from typing import Dict, Any, List, Optional, Tuple

# Google ADK imports
from google_adk.core.tool import Tool
from google_adk.generators.llm import LLMGenerator


class CCCDAnalyzer(Tool):
    """Tool phân tích số CCCD/CMND theo Bát Cục Linh Số"""
    
    def __init__(self):
        """Khởi tạo CCCD Analyzer Tool"""
        super().__init__(
            name="cccd_analyzer",
            description="Phân tích số CCCD/CMND theo phương pháp Bát Cục Linh Số",
            parameters=[
                {
                    "name": "cccd_number",
                    "type": "string",
                    "description": "Số CCCD/CMND cần phân tích",
                    "required": True
                }
            ],
            returns={
                "type": "object",
                "description": "Kết quả phân tích số CCCD/CMND",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Trạng thái thành công"
                    },
                    "content": {
                        "type": "string",
                        "description": "Nội dung phân tích"
                    },
                    "cccd_number": {
                        "type": "string",
                        "description": "Số CCCD/CMND đã phân tích"
                    },
                    "info": {
                        "type": "object",
                        "description": "Thông tin được trích xuất từ CCCD/CMND",
                    },
                    "error": {
                        "type": "string",
                        "description": "Thông báo lỗi nếu có"
                    }
                }
            }
        )
        
        # Khởi tạo logger
        self.logger = logging.getLogger("CCCDAnalyzer")
        
        # Khởi tạo LLM Generator cho phân tích nâng cao
        model_name = os.environ.get("CCCD_ANALYZER_MODEL", "gemini-pro")
        self.generator = LLMGenerator(name="cccd-analyzer-generator", model=model_name)
        
        # Bảng mã tỉnh thành cho CCCD 12 số
        self.province_codes = {
            "001": "Hà Nội", "002": "Hà Giang", "004": "Cao Bằng", "006": "Bắc Kạn", 
            "008": "Tuyên Quang", "010": "Lào Cai", "011": "Điện Biên", "012": "Lai Châu", 
            "014": "Sơn La", "015": "Yên Bái", "017": "Hòa Bình", "019": "Thái Nguyên", 
            "020": "Lạng Sơn", "022": "Quảng Ninh", "024": "Bắc Giang", "025": "Phú Thọ", 
            "026": "Vĩnh Phúc", "027": "Bắc Ninh", "030": "Hải Dương", "031": "Hải Phòng", 
            "033": "Hưng Yên", "034": "Thái Bình", "035": "Hà Nam", "036": "Nam Định", 
            "037": "Ninh Bình", "038": "Thanh Hóa", "040": "Nghệ An", "042": "Hà Tĩnh", 
            "044": "Quảng Bình", "045": "Quảng Trị", "046": "Thừa Thiên Huế", "048": "Đà Nẵng", 
            "049": "Quảng Nam", "051": "Quảng Ngãi", "052": "Bình Định", "054": "Phú Yên", 
            "056": "Khánh Hòa", "058": "Ninh Thuận", "060": "Bình Thuận", "062": "Kon Tum", 
            "064": "Gia Lai", "066": "Đắk Lắk", "067": "Đắk Nông", "068": "Lâm Đồng", 
            "070": "Bình Phước", "072": "Tây Ninh", "074": "Bình Dương", "075": "Đồng Nai", 
            "077": "Bà Rịa - Vũng Tàu", "079": "Thành phố Hồ Chí Minh", "080": "Long An", 
            "082": "Tiền Giang", "083": "Bến Tre", "084": "Trà Vinh", "086": "Vĩnh Long", 
            "087": "Đồng Tháp", "089": "An Giang", "091": "Kiên Giang", "092": "Cần Thơ", 
            "093": "Hậu Giang", "094": "Sóc Trăng", "095": "Bạc Liêu", "096": "Cà Mau"
        }
        
        self.logger.info("CCCD Analyzer Tool đã được khởi tạo")
    
    def extract_cccd_number(self, text: str) -> Optional[str]:
        """Trích xuất số CCCD/CMND từ văn bản
        
        Args:
            text: Văn bản chứa số CCCD/CMND
            
        Returns:
            str: Số CCCD/CMND đã trích xuất hoặc None nếu không tìm thấy
        """
        # Mẫu regex cho CCCD (12 số) và CMND (9 hoặc 12 số)
        patterns = [
            r'\b\d{12}\b',  # CCCD - 12 số
            r'\b\d{9}\b'    # CMND - 9 số
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.replace(' ', '').replace('.', '').replace('-', ''))
            if matches:
                return matches[0]
        
        return None
    
    def is_valid_cccd(self, cccd_number: str) -> bool:
        """Kiểm tra tính hợp lệ của số CCCD/CMND
        
        Args:
            cccd_number: Số CCCD/CMND cần kiểm tra
            
        Returns:
            bool: True nếu hợp lệ, False nếu không
        """
        # Chuẩn hóa
        cccd = cccd_number.replace(' ', '').replace('.', '').replace('-', '')
        
        # Kiểm tra độ dài
        if len(cccd) == 12:
            # Kiểm tra mã tỉnh (3 số đầu tiên)
            province_code = cccd[:3]
            if province_code not in self.province_codes:
                return False
                
            # Kiểm tra mã giới tính và năm sinh (1 số tiếp theo)
            gender_code = int(cccd[3])
            if gender_code not in range(0, 10):
                return False
                
            # Kiểm tra các số còn lại
            if not cccd[4:].isdigit():
                return False
                
            return True
        elif len(cccd) == 9:
            # CMND 9 số - chỉ kiểm tra là số
            return cccd.isdigit()
        
        return False
    
    def extract_info_from_cccd(self, cccd_number: str) -> Dict[str, Any]:
        """Trích xuất thông tin từ số CCCD/CMND
        
        Args:
            cccd_number: Số CCCD/CMND cần trích xuất thông tin
            
        Returns:
            Dict[str, Any]: Thông tin được trích xuất
        """
        # Chuẩn hóa
        cccd = cccd_number.replace(' ', '').replace('.', '').replace('-', '')
        info = {"type": "unknown", "number": cccd}
        
        if len(cccd) == 12:
            info["type"] = "CCCD"
            
            # Trích xuất mã tỉnh
            province_code = cccd[:3]
            info["province_code"] = province_code
            info["province"] = self.province_codes.get(province_code, "Không xác định")
            
            # Trích xuất thông tin giới tính và năm sinh
            gender_year_code = int(cccd[3])
            century_mapping = {
                0: {"gender": "Nam", "century": "19"},
                1: {"gender": "Nữ", "century": "19"},
                2: {"gender": "Nam", "century": "20"},
                3: {"gender": "Nữ", "century": "20"},
                4: {"gender": "Nam", "century": "21"},
                5: {"gender": "Nữ", "century": "21"},
                6: {"gender": "Nam", "century": "unknown"},
                7: {"gender": "Nữ", "century": "unknown"},
                8: {"gender": "Nam", "century": "unknown"},
                9: {"gender": "Nữ", "century": "unknown"}
            }
            
            gender_info = century_mapping.get(gender_year_code, {"gender": "Không xác định", "century": "unknown"})
            info["gender"] = gender_info["gender"]
            
            # Trích xuất năm sinh (2 số tiếp theo)
            year_code = cccd[4:6]
            if gender_info["century"] != "unknown":
                info["birth_year"] = f"{gender_info['century']}{year_code}"
            else:
                info["birth_year"] = "Không xác định"
            
            # Mã ngẫu nhiên (6 số cuối)
            info["random_code"] = cccd[6:]
            
        elif len(cccd) == 9:
            info["type"] = "CMND"
            
            # CMND 9 số không có cấu trúc cố định để trích xuất thông tin
            # Nhưng có thể là mã tỉnh nếu đối chiếu với bảng mã
            # Tuy nhiên, vì không chắc chắn nên không trích xuất
            
        return info
    
    def calculate_total_value(self, cccd_number: str) -> int:
        """Tính tổng giá trị số học của số CCCD/CMND
        
        Args:
            cccd_number: Số CCCD/CMND cần tính toán
            
        Returns:
            int: Tổng giá trị
        """
        # Tính tổng tất cả các chữ số
        total = sum(int(digit) for digit in cccd_number if digit.isdigit())
        
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
    
    def find_special_pairs(self, cccd_number: str) -> Dict[str, List[Tuple[str, str]]]:
        """Tìm các cặp số đặc biệt trong CCCD/CMND
        
        Args:
            cccd_number: Số CCCD/CMND cần tìm cặp số
            
        Returns:
            Dict[str, List[Tuple[str, str]]]: Danh sách các cặp số đặc biệt theo loại
        """
        special_pairs = {
            "doubles": [],      # Cặp số giống nhau (11, 22, ...)
            "sequences": [],    # Cặp số liền kề tăng dần (12, 23, ...)
            "reverses": [],     # Cặp số liền kề đảo ngược (21, 32, ...)
            "good_numbers": []  # Cặp số tốt (68, 86, 19, 91, 28, 82, ...)
        }
        
        good_pairs = ["68", "86", "19", "91", "28", "82", "38", "83", "69", "96"]
        
        # Tìm các cặp số trong CCCD/CMND
        for i in range(len(cccd_number) - 1):
            pair = cccd_number[i:i+2]
            position = f"{i+1}-{i+2}"
            
            # Cặp số giống nhau
            if pair[0] == pair[1]:
                special_pairs["doubles"].append((position, pair))
            
            # Cặp số liền kề tăng dần
            if int(pair[1]) == int(pair[0]) + 1 or (pair[0] == '9' and pair[1] == '0'):
                special_pairs["sequences"].append((position, pair))
            
            # Cặp số liền kề đảo ngược
            if int(pair[0]) == int(pair[1]) + 1 or (pair[1] == '9' and pair[0] == '0'):
                special_pairs["reverses"].append((position, pair))
            
            # Cặp số tốt
            if pair in good_pairs:
                special_pairs["good_numbers"].append((position, pair))
        
        return special_pairs
    
    async def analyze(self, message: str) -> Dict[str, Any]:
        """Phân tích số CCCD/CMND từ tin nhắn
        
        Args:
            message: Nội dung tin nhắn chứa số CCCD/CMND
            
        Returns:
            Dict[str, Any]: Kết quả phân tích
        """
        # Trích xuất số CCCD/CMND từ tin nhắn
        cccd_number = self.extract_cccd_number(message)
        
        if not cccd_number:
            return {
                "success": False,
                "error": "Không tìm thấy số CCCD/CMND hợp lệ trong tin nhắn của bạn. CCCD có 12 số, CMND có 9 số.",
                "content": "Xin lỗi, tôi không tìm thấy số CCCD/CMND hợp lệ trong tin nhắn của bạn. CCCD có 12 số, CMND có 9 số."
            }
        
        # Kiểm tra tính hợp lệ
        if not self.is_valid_cccd(cccd_number):
            return {
                "success": False,
                "error": f"Số CCCD/CMND '{cccd_number}' không hợp lệ. Vui lòng kiểm tra lại.",
                "content": f"Số CCCD/CMND '{cccd_number}' không hợp lệ. Vui lòng kiểm tra lại."
            }
        
        # Trích xuất thông tin
        info = self.extract_info_from_cccd(cccd_number)
        
        # Tính tổng giá trị
        total_value = self.calculate_total_value(cccd_number)
        
        # Xác định ngũ hành
        element = self.get_element(total_value)
        
        # Tìm các cặp số đặc biệt
        special_pairs = self.find_special_pairs(cccd_number)
        
        # Chuẩn bị thông tin cho phân tích
        analysis_info = {
            "number": cccd_number,
            "type": info["type"],
            "total_value": total_value,
            "element": element,
            "info": info
        }
        
        # Phân tích số CCCD/CMND bằng LLM
        analysis_prompt = f"""
        Hãy phân tích số {info['type']} {cccd_number} theo phương pháp Bát Cục Linh Số với các thông tin sau:
        
        1. Tổng số (Lộ số): {total_value} - Ngũ hành: {element}
        """
        
        if info["type"] == "CCCD":
            analysis_prompt += f"""
        2. Thông tin cá nhân:
           - Tỉnh/Thành phố: {info['province']}
           - Giới tính: {info['gender']}
           - Năm sinh: {info['birth_year']}
           - Mã ngẫu nhiên: {info['random_code']}
        """
        
        analysis_prompt += f"""
        3. Các cặp số đặc biệt:
           - Cặp số giống nhau: {', '.join([f"{p[0]}({p[1]})" for p in special_pairs['doubles']]) if special_pairs['doubles'] else 'Không có'}
           - Cặp số liền kề tăng dần: {', '.join([f"{p[0]}({p[1]})" for p in special_pairs['sequences']]) if special_pairs['sequences'] else 'Không có'}
           - Cặp số liền kề đảo ngược: {', '.join([f"{p[0]}({p[1]})" for p in special_pairs['reverses']]) if special_pairs['reverses'] else 'Không có'}
           - Cặp số tốt: {', '.join([f"{p[0]}({p[1]})" for p in special_pairs['good_numbers']]) if special_pairs['good_numbers'] else 'Không có'}
        
        Phân tích chi tiết về:
        - Ý nghĩa tổng số và ngũ hành tương ứng
        - Ý nghĩa của các cặp số đặc biệt (nếu có)
        - Ý nghĩa của mã tỉnh và các thông tin cá nhân (nếu có)
        - Điểm mạnh và điểm yếu
        - Đánh giá tổng thể (tốt/trung bình/không tốt)
        - Lời khuyên hoặc gợi ý (nếu cần)
        
        Định dạng kết quả đẹp, dễ đọc với các tiêu đề và đoạn văn ngắn gọn.
        """
        
        try:
            response = await self.generator.generate(analysis_prompt)
            analysis_result = response.text
            
            return {
                "success": True,
                "cccd_number": cccd_number,
                "content": analysis_result,
                "info": info
            }
        except Exception as e:
            self.logger.error(f"Lỗi khi phân tích số CCCD/CMND: {str(e)}")
            
            # Trả về kết quả đơn giản nếu gặp lỗi
            basic_analysis = f"""
            Phân tích số {info['type']}: {cccd_number}
            
            Tổng số (Lộ số): {total_value}
            Ngũ hành: {element}
            """
            
            if info["type"] == "CCCD":
                basic_analysis += f"""
            Thông tin cá nhân:
            - Tỉnh/Thành phố: {info['province']}
            - Giới tính: {info['gender']}
            - Năm sinh: {info['birth_year']}
            - Mã ngẫu nhiên: {info['random_code']}
            """
            
            basic_analysis += """
            Vì gặp lỗi khi phân tích chi tiết, chỉ có thể cung cấp phân tích cơ bản.
            """
            
            return {
                "success": True,
                "cccd_number": cccd_number,
                "content": basic_analysis,
                "info": info,
                "error": str(e)
            }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Thực thi tool với tham số từ ADK
        
        Args:
            **kwargs: Tham số, bao gồm cccd_number
            
        Returns:
            Dict[str, Any]: Kết quả phân tích
        """
        cccd_number = kwargs.get("cccd_number", "")
        
        if not cccd_number:
            return {
                "success": False,
                "error": "Thiếu tham số cccd_number"
            }
        
        return await self.analyze(cccd_number) 