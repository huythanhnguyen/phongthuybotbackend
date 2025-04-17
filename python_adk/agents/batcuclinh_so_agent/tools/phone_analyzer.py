"""
Phone Analyzer: Tool để phân tích số điện thoại theo phương pháp Bát Cục Linh Số
"""

import re
from typing import Dict, Any, List, Optional
from adk.core.tool import Tool

class PhoneAnalyzer(Tool):
    """Tool phân tích số điện thoại theo phương pháp Bát Cục Linh Số"""
    
    def __init__(self):
        """Khởi tạo Phone Analyzer Tool"""
        super().__init__(
            name="phone_analyzer",
            description="Phân tích số điện thoại theo phương pháp Bát Cục Linh Số để xác định ý nghĩa phong thủy",
            parameters=["phone_number", "purpose"],
            required_params=["phone_number"]
        )
        
        # Khởi tạo dữ liệu Bát Cục Linh Số
        self._init_bat_cuc_linh_so_data()
    
    def _init_bat_cuc_linh_so_data(self):
        """Khởi tạo dữ liệu về các sao và cặp số trong Bát Cục Linh Số"""
        # 4 Cát Tinh (Sao Tốt)
        self.SINH_KHI = {
            "name": "Sinh Khí",
            "description": "Vui vẻ, quý nhân, dẫn đạo lực",
            "numbers": ["14", "41", "67", "76", "39", "93", "28", "82"],
            "energy": {
                "14": 4, "41": 4,  # Mức năng lượng cao nhất
                "67": 3, "76": 3,  # Mức năng lượng cao
                "39": 2, "93": 2,  # Mức năng lượng trung bình
                "28": 1, "82": 1   # Mức năng lượng thấp
            },
            "nature": "Cát"  # Auspicious
        }
        
        self.THIEN_Y = {
            "name": "Thiên Y",
            "description": "Tiền tài, tình cảm, hồi báo",
            "numbers": ["13", "31", "68", "86", "49", "94", "27", "72"],
            "energy": {
                "13": 4, "31": 4,  # Mức năng lượng cao nhất
                "68": 3, "86": 3,  # Mức năng lượng cao
                "49": 2, "94": 2,  # Mức năng lượng trung bình
                "27": 1, "72": 1   # Mức năng lượng thấp
            },
            "nature": "Cát"  # Auspicious
        }
        
        self.DIEN_NIEN = {
            "name": "Diên Niên",
            "description": "Năng lực chuyên nghiệp, công việc",
            "numbers": ["19", "91", "78", "87", "34", "43", "26", "62"],
            "energy": {
                "19": 4, "91": 4,  # Mức năng lượng cao nhất
                "78": 3, "87": 3,  # Mức năng lượng cao
                "34": 2, "43": 2,  # Mức năng lượng trung bình
                "26": 1, "62": 1   # Mức năng lượng thấp
            },
            "nature": "Cát"  # Auspicious
        }
        
        self.PHUC_VI = {
            "name": "Phục Vị",
            "description": "Chịu đựng, khó thay đổi",
            "numbers": ["11", "22", "33", "44", "66", "77", "88", "99"],
            "energy": {
                "11": 4, "22": 4, "33": 1, "44": 1,
                "66": 2, "77": 2, "88": 3, "99": 3
            },
            "nature": "Cát/Hung"  # Can be both auspicious or inauspicious
        }
        
        # 4 Hung Tinh (Sao Xấu)
        self.HOA_HAI = {
            "name": "Họa Hại",
            "description": "Khẩu tài, chi tiêu lớn, thị phi",
            "numbers": ["17", "71", "89", "98", "46", "64", "23", "32"],
            "energy": {
                "17": 4, "71": 4,  # Mức năng lượng cao nhất
                "89": 3, "98": 3,  # Mức năng lượng cao
                "46": 2, "64": 2,  # Mức năng lượng trung bình
                "23": 1, "32": 1   # Mức năng lượng thấp
            },
            "nature": "Hung"  # Inauspicious
        }
        
        self.LUC_SAT = {
            "name": "Lục Sát",
            "description": "Giao tế, phục vụ, cửa hàng, nữ nhân",
            "numbers": ["16", "61", "47", "74", "38", "83", "92", "29"],
            "energy": {
                "16": 4, "61": 4,  # Mức năng lượng cao nhất
                "47": 3, "74": 3,  # Mức năng lượng cao
                "38": 2, "83": 2,  # Mức năng lượng trung bình
                "92": 1, "29": 1   # Mức năng lượng thấp
            },
            "nature": "Hung"  # Inauspicious
        }
        
        self.NGU_QUY = {
            "name": "Ngũ Quỷ",
            "description": "Trí óc, biến động, không ổn định, tư duy",
            "numbers": ["18", "81", "79", "97", "36", "63", "24", "42"],
            "energy": {
                "18": 4, "81": 4,  # Mức năng lượng cao nhất
                "79": 3, "97": 3,  # Mức năng lượng cao
                "36": 2, "63": 2,  # Mức năng lượng trung bình
                "24": 1, "42": 1   # Mức năng lượng thấp
            },
            "nature": "Hung"  # Inauspicious
        }
        
        self.TUYET_MENH = {
            "name": "Tuyệt Mệnh",
            "description": "Dốc sức, đầu tư, hành động, phá tài",
            "numbers": ["12", "21", "69", "96", "84", "48", "73", "37"],
            "energy": {
                "12": 4, "21": 4,  # Mức năng lượng cao nhất
                "69": 3, "96": 3,  # Mức năng lượng cao
                "84": 2, "48": 2,  # Mức năng lượng trung bình
                "73": 1, "37": 1   # Mức năng lượng thấp
            },
            "nature": "Hung"  # Inauspicious
        }
        
        # Tất cả các sao
        self.ALL_STARS = [
            self.SINH_KHI, self.THIEN_Y, self.DIEN_NIEN, self.PHUC_VI,
            self.HOA_HAI, self.LUC_SAT, self.NGU_QUY, self.TUYET_MENH
        ]
        
        # Mapping từ cặp số đến sao
        self.number_to_star = {}
        for star in self.ALL_STARS:
            for number in star["numbers"]:
                self.number_to_star[number] = {
                    "name": star["name"],
                    "description": star["description"],
                    "energy": star["energy"].get(number, 3),
                    "nature": star["nature"]
                }
    
    def _normalize_phone_number(self, phone: str) -> str:
        """Chuẩn hóa số điện thoại về dạng không có ký tự đặc biệt"""
        # Bỏ tất cả các ký tự không phải số
        normalized = re.sub(r'[^0-9]', '', phone)
        
        # Chuyển +84 về 0
        if normalized.startswith("84") and len(normalized) > 9:
            normalized = "0" + normalized[2:]
            
        return normalized
    
    def _get_overlapping_pairs(self, number: str) -> List[str]:
        """Tạo các cặp số chồng lấp từ số điện thoại"""
        pairs = []
        for i in range(len(number) - 1):
            pairs.append(number[i:i+2])
        return pairs
    
    def _get_star_for_pair(self, pair: str) -> Dict[str, Any]:
        """Xác định sao tương ứng với cặp số"""
        if pair in self.number_to_star:
            return self.number_to_star[pair]
        
        # Xử lý cặp số có chứa số 0
        if "0" in pair:
            original_star = None
            
            # Thay 0 bằng số khác và kiểm tra
            for replacement in "123456789":
                test_pair = pair.replace("0", replacement)
                if test_pair in self.number_to_star:
                    original_star = self.number_to_star[test_pair]
                    break
            
            if original_star:
                # Sao có số 0 thường bị biến chất (hóa hung)
                return {
                    "name": f"{original_star['name']} hóa hung",
                    "description": f"{original_star['name']} có số 0: Năng lượng yếu hoặc biến chất",
                    "energy": max(1, original_star["energy"] - 1),  # Giảm năng lượng
                    "nature": "Cát hóa hung" if original_star["nature"] == "Cát" else "Hung"
                }
        
        # Sao không xác định
        return {
            "name": "Không xác định",
            "description": "Cặp số không thuộc Bát Cục Linh Số",
            "energy": 1,
            "nature": "Không xác định"
        }
    
    def _analyze_energy_balance(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Phân tích sự cân bằng năng lượng trong số điện thoại"""
        pairs_analysis = analysis_result["pairs_analysis"]
        
        # Đếm số lượng sao cát/hung và tính tổng năng lượng
        total_energy = 0
        cats_count = 0
        hungs_count = 0
        
        for pair in pairs_analysis:
            total_energy += pair["energy"]
            if pair["nature"] == "Cát":
                cats_count += 1
            elif pair["nature"] == "Hung":
                hungs_count += 1
        
        # Tính số điểm tổng hợp (thang điểm 10)
        average_energy = total_energy / len(pairs_analysis) if pairs_analysis else 0
        total_score = min(10, max(1, round((average_energy / 4 * 6) + (cats_count / len(pairs_analysis) * 4)))) if pairs_analysis else 5
        
        # Đánh giá cân bằng âm dương
        yin_yang_balance = "Cân bằng"
        if cats_count > 2 * hungs_count:
            yin_yang_balance = "Dương thịnh (nhiều cát tinh)"
        elif hungs_count > 2 * cats_count:
            yin_yang_balance = "Âm thịnh (nhiều hung tinh)"
        
        return {
            "total_score": total_score,
            "average_energy": round(average_energy, 1),
            "cats_count": cats_count,
            "hungs_count": hungs_count,
            "yin_yang_balance": yin_yang_balance,
            "rating": self._get_rating(total_score)
        }
    
    def _get_rating(self, score: int) -> str:
        """Chuyển điểm thành đánh giá sao"""
        if score >= 9:
            return "★★★★★ (Rất tốt)"
        elif score >= 7:
            return "★★★★☆ (Tốt)"
        elif score >= 5:
            return "★★★☆☆ (Trung bình)"
        elif score >= 3:
            return "★★☆☆☆ (Kém)"
        else:
            return "★☆☆☆☆ (Rất kém)"
    
    def _analyze_purpose_compatibility(self, analysis_result: Dict[str, Any], purpose: Optional[str] = None) -> Dict[str, Any]:
        """Phân tích độ phù hợp với mục đích sử dụng"""
        pairs_analysis = analysis_result["pairs_analysis"]
        
        # Các mục đích phổ biến
        purposes = {
            "business": {
                "name": "Kinh doanh",
                "favorable_stars": ["Thiên Y", "Diên Niên"],
                "unfavorable_stars": ["Tuyệt Mệnh", "Ngũ Quỷ"]
            },
            "personal": {
                "name": "Cá nhân",
                "favorable_stars": ["Sinh Khí", "Thiên Y"],
                "unfavorable_stars": ["Họa Hại", "Lục Sát"]
            },
            "wealth": {
                "name": "Tài lộc",
                "favorable_stars": ["Thiên Y", "Sinh Khí"],
                "unfavorable_stars": ["Tuyệt Mệnh", "Họa Hại"]
            },
            "relationship": {
                "name": "Tình cảm",
                "favorable_stars": ["Sinh Khí", "Thiên Y"],
                "unfavorable_stars": ["Lục Sát", "Ngũ Quỷ"]
            },
            "career": {
                "name": "Sự nghiệp",
                "favorable_stars": ["Diên Niên", "Sinh Khí"],
                "unfavorable_stars": ["Ngũ Quỷ", "Tuyệt Mệnh"]
            }
        }
        
        # Đánh giá độ phù hợp với từng mục đích
        purpose_compatibility = {}
        for p_key, p_data in purposes.items():
            favorable_count = 0
            unfavorable_count = 0
            
            for pair in pairs_analysis:
                if pair["star"] in p_data["favorable_stars"]:
                    favorable_count += 1
                if pair["star"] in p_data["unfavorable_stars"]:
                    unfavorable_count += 1
            
            # Tính điểm phù hợp (thang 10)
            compatibility_score = 5  # Mặc định trung bình
            if len(pairs_analysis) > 0:
                # Điểm cộng cho sao thuận lợi và trừ cho sao không thuận lợi
                compatibility_score += (favorable_count * 2 - unfavorable_count * 1.5) / len(pairs_analysis) * 5
                compatibility_score = min(10, max(1, round(compatibility_score)))
            
            purpose_compatibility[p_key] = {
                "name": p_data["name"],
                "score": compatibility_score,
                "rating": self._get_rating(compatibility_score),
                "favorable_count": favorable_count,
                "unfavorable_count": unfavorable_count
            }
        
        # Nếu có mục đích cụ thể, đưa ra lời khuyên chi tiết
        specific_advice = ""
        if purpose and purpose in purposes:
            p_data = purpose_compatibility[purpose]
            specific_advice = f"Số điện thoại này "
            
            if p_data["score"] >= 8:
                specific_advice += f"rất phù hợp cho mục đích {p_data['name']}."
            elif p_data["score"] >= 6:
                specific_advice += f"phù hợp cho mục đích {p_data['name']}."
            elif p_data["score"] >= 4:
                specific_advice += f"có thể sử dụng cho mục đích {p_data['name']}, nhưng không lý tưởng."
            else:
                specific_advice += f"không phù hợp cho mục đích {p_data['name']}. Nên cân nhắc số khác."
        
        # Xác định mục đích phù hợp nhất
        best_purpose = max(purpose_compatibility.items(), key=lambda x: x[1]["score"])
        best_purpose_advice = f"Số điện thoại này phù hợp nhất cho mục đích {best_purpose[1]['name']}."
        
        return {
            "purpose_compatibility": purpose_compatibility,
            "best_purpose": {
                "key": best_purpose[0],
                "name": best_purpose[1]["name"],
                "score": best_purpose[1]["score"]
            },
            "specific_advice": specific_advice if purpose else best_purpose_advice
        }
    
    def _get_overall_advice(self, analysis_result: Dict[str, Any]) -> str:
        """Tạo lời khuyên tổng thể dựa trên kết quả phân tích"""
        energy_balance = analysis_result["energy_balance"]
        purpose_compat = analysis_result["purpose_compatibility"]
        
        advice = ""
        
        # Lời khuyên dựa trên điểm số tổng thể
        if energy_balance["total_score"] >= 8:
            advice += "Số điện thoại này có năng lượng rất tốt. "
        elif energy_balance["total_score"] >= 6:
            advice += "Số điện thoại này có năng lượng khá tốt. "
        elif energy_balance["total_score"] >= 4:
            advice += "Số điện thoại này có năng lượng trung bình. "
        else:
            advice += "Số điện thoại này có năng lượng không tốt. Nên cân nhắc thay đổi. "
        
        # Thêm lời khuyên về mục đích sử dụng
        advice += purpose_compat["specific_advice"]
        
        # Lời khuyên dựa trên sự cân bằng âm dương
        if energy_balance["yin_yang_balance"] != "Cân bằng":
            if energy_balance["yin_yang_balance"] == "Dương thịnh (nhiều cát tinh)":
                advice += " Số có nhiều cát tinh, mang lại may mắn và thuận lợi."
            else:
                advice += " Số có nhiều hung tinh, cần chú ý đến các mặt tiêu cực có thể xảy ra."
        
        return advice
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi phân tích số điện thoại theo phương pháp Bát Cục Linh Số"""
        phone_number = params.get("phone_number")
        purpose = params.get("purpose")
        
        if not phone_number:
            return {
                "success": False,
                "message": "Thiếu số điện thoại để phân tích"
            }
        
        # Chuẩn hóa số điện thoại
        normalized_phone = self._normalize_phone_number(phone_number)
        
        # Nếu số không hợp lệ
        if len(normalized_phone) < 9 or len(normalized_phone) > 11:
            return {
                "success": False,
                "message": f"Số điện thoại không hợp lệ: {phone_number}"
            }
        
        # Lấy các cặp số chồng lấp
        pairs = self._get_overlapping_pairs(normalized_phone)
        
        # Phân tích từng cặp số
        pairs_analysis = []
        for pair in pairs:
            star_info = self._get_star_for_pair(pair)
            pairs_analysis.append({
                "pair": pair,
                "star": star_info["name"],
                "description": star_info["description"],
                "energy": star_info["energy"],
                "nature": star_info["nature"]
            })
        
        # Cấu trúc kết quả phân tích
        analysis_result = {
            "original_number": phone_number,
            "normalized_number": normalized_phone,
            "pairs": pairs,
            "pairs_analysis": pairs_analysis
        }
        
        # Phân tích cân bằng năng lượng
        energy_balance = self._analyze_energy_balance(analysis_result)
        analysis_result["energy_balance"] = energy_balance
        
        # Phân tích độ phù hợp với mục đích
        purpose_compatibility = self._analyze_purpose_compatibility(analysis_result, purpose)
        analysis_result["purpose_compatibility"] = purpose_compatibility
        
        # Tạo lời khuyên tổng thể
        overall_advice = self._get_overall_advice(analysis_result)
        analysis_result["advice"] = overall_advice
        
        return {
            "success": True,
            "phoneNumber": phone_number,
            "normalized": normalized_phone,
            "analysis": analysis_result
        } 