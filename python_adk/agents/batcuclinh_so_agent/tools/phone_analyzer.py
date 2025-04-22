"""
Phone Analyzer: Tool để phân tích số điện thoại theo phương pháp Bát Cục Linh Số
"""

import re
from typing import Dict, Any, List, Optional
# Sử dụng Google ADK FunctionTool thay vì Tool class tự định nghĩa
from google.adk.tools import FunctionTool, ToolContext
import os
from python_adk.constants.bat_tinh import BAT_TINH
from python_adk.constants.combinations import COMBINATIONS
from python_adk.constants.digit_meanings import DIGIT_MEANINGS
from python_adk.constants.response_factors import RESPONSE_FACTORS

def analyze_phone_number(phone_number: str, purpose: Optional[str] = None, tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    """Phân tích số điện thoại theo phương pháp Bát Cục Linh Số để xác định ý nghĩa phong thủy
    
    Sử dụng tool này khi người dùng yêu cầu phân tích số điện thoại theo phong thủy hoặc muốn biết ý nghĩa của số điện thoại.
    
    Args:
        phone_number: Số điện thoại cần phân tích. Có thể chứa các ký tự đặc biệt như dấu cách, dấu gạch ngang.
        purpose: Mục đích sử dụng số điện thoại (ví dụ: kinh doanh, cá nhân, tài lộc, tình cảm, sự nghiệp). Có thể bỏ trống.
        tool_context: Context của tool, được tự động truyền vào bởi ADK framework.
        
    Returns:
        Dict[str, Any]: Kết quả phân tích, bao gồm:
            - success (bool): Trạng thái thành công của việc phân tích
            - message (str): Thông báo lỗi nếu có
            - analysis (Dict): Kết quả phân tích chi tiết nếu thành công, bao gồm:
                - starSequence: Danh sách các ngôi sao được ánh xạ từ các cặp số
                - energyLevel: Mức năng lượng tổng hợp
                - balance: Sự cân bằng âm dương
                - starCombinations: Các tổ hợp sao liền kề
                - keyPositions: Các vị trí đặc biệt trong số điện thoại
    """
    # Chuẩn hóa số điện thoại
    normalized = _normalize_phone_number(phone_number)
    
    # Kiểm tra độ dài
    if len(normalized) < 9 or len(normalized) > 11:
        return {
            "success": False,
            "message": f"Số điện thoại không hợp lệ: {phone_number}"
        }
    
    # Phân tích số điện thoại theo Bát Cục Linh Số
    star_sequence = _map_to_star_sequence(normalized)
    
    # Tính năng lượng
    total_energy = sum(x["energyLevel"] for x in star_sequence)
    cat = sum(1 for x in star_sequence if x["nature"] == "Cát")
    hung = sum(1 for x in star_sequence if x["nature"] == "Hung")
    ratio = cat / (cat + hung) if (cat + hung) else 0
    balance = "Cân bằng" if abs(cat - hung) < 2 else ("Dương thịnh" if cat > hung else "Âm thịnh")
    energy_levels = {"total": total_energy, "cat": cat, "hung": hung, "ratio": ratio}
    
    # Tổ hợp sao liền kề
    combos = []
    for i in range(len(star_sequence) - 1):
        f = star_sequence[i]; s = star_sequence[i+1]
        key = f"{f['star']}_{s['star']}"
        comb = COMBINATIONS.get("STAR_PAIRS", {}).get(key, {})
        combos.append({
            "firstStar": {"name": f['name'], "nature": f['nature'], "originalPair": f['originalPair'], "energyLevel": f['energyLevel']},
            "secondStar": {"name": s['name'], "nature": s['nature'], "originalPair": s['originalPair'], "energyLevel": s['energyLevel']},
            "key": key,
            "description": comb.get("description", ""),
            "detailedDescription": comb.get("detailedDescription", []),
            "totalEnergy": f['energyLevel'] + s['energyLevel'],
            "isPositive": f['nature'] == "Cát" and s['nature'] == "Cát",
            "isNegative": f['nature'] == "Hung" and s['nature'] == "Hung",
            "position": f"{i+1}-{i+2}",
            "isLastPair": i == len(star_sequence) - 2
        })
    
    # Vị trí đặc biệt
    kp = {}
    ln = len(normalized)
    kp['lastDigit'] = {"value": normalized[-1], "meaning": DIGIT_MEANINGS.get("SINGLE_DIGIT_MEANINGS", {}).get(normalized[-1], ""), "position": "Vị trí cuối cùng"}
    if ln >= 3:
        d3 = normalized[-3]
        kp['thirdFromEnd'] = {"value": d3, "meaning": DIGIT_MEANINGS.get("THIRD_FROM_END_MEANINGS", {}).get(d3, ""), "position": "Vị trí thứ 3 từ cuối"}
    if ln >= 5:
        d5 = normalized[-5]
        kp['fifthFromEnd'] = {"value": d5, "meaning": DIGIT_MEANINGS.get("FIFTH_FROM_END_MEANINGS", {}).get(d5, ""), "position": "Vị trí thứ 5 từ cuối"}
    
    # Phân tích 3 số cuối
    last3 = normalized[-3:]
    p1, p2 = last3[:2], last3[1:]
    info1 = next((x for x in star_sequence if x['originalPair'] == p1), {})
    info2 = next((x for x in star_sequence if x['originalPair'] == p2), {})
    ck = f"{info1.get('star')}_{info2.get('star')}"
    cinfo = COMBINATIONS.get("STAR_PAIRS", {}).get(ck, {})
    last3analysis = {
        "lastThreeDigits": last3,
        "firstPair": {"pair": p1, "starInfo": info1},
        "secondPair": {"pair": p2, "starInfo": info2},
        "specialCombination": None,
        "starCombination": {"key": ck, "name": ck.replace("_"," + "), "description": cinfo.get("description",""), "detailedDescription": cinfo.get("detailedDescription",[])},
        "hasSpecialMeaning": True
    }
    
    # Phân tích mục đích sử dụng nếu có
    purpose_analysis = None
    if purpose:
        purpose_analysis = _analyze_purpose_compatibility(star_sequence, purpose)
    
    # Tạo kết quả phân tích
    analysis = {
        "result": {
            "starSequence": star_sequence, 
            "energyLevel": energy_levels, 
            "balance": balance, 
            "starCombinations": combos, 
            "keyCombinations": [], 
            "dangerousCombinations": [], 
            "keyPositions": kp, 
            "last3DigitsAnalysis": last3analysis, 
            "specialAttribute": "",
            "purposeAnalysis": purpose_analysis
        }
    }
    
    # Nếu có tool_context, lưu kết quả phân tích vào state
    if tool_context:
        tool_context.state["last_phone_analysis"] = {
            "number": normalized,
            "energy_level": energy_levels,
            "balance": balance
        }
    
    return {"success": True, "analysis": analysis}

def _normalize_phone_number(phone: str) -> str:
    """Chuẩn hóa số điện thoại về dạng không có ký tự đặc biệt"""
    # Bỏ tất cả các ký tự không phải số
    normalized = re.sub(r'[^0-9]', '', phone)
    
    # Chuyển +84 về 0
    if normalized.startswith("84") and len(normalized) > 9:
        normalized = "0" + normalized[2:]
        
    return normalized

def _get_star_level(energy: int) -> str:
    if energy >= 4:
        return "VERY_HIGH"
    elif energy == 3:
        return "HIGH"
    elif energy == 2:
        return "MEDIUM"
    return "LOW"

def _generate_pairs(digits: str) -> List[str]:
    pairs: List[str] = []
    i = 0
    while i < len(digits) - 1:
        if digits[i] in ("0", "5"):
            i += 1
            continue
        if digits[i+1] not in ("0", "5"):
            pairs.append(digits[i:i+2])
            i += 1
        else:
            j = i + 1
            group = digits[i]
            while j < len(digits) and digits[j] in ("0", "5"):
                group += digits[j]
                j += 1
            if j < len(digits):
                group += digits[j]
                j += 1
            pairs.append(group)
            i = j - 1
    # xử lý nhóm cuối
    if pairs:
        last = pairs[-1]
        if len(last) > 1 and last[0] not in ("0", "5") and all(c in ("0","5") for c in last[1:]):
            trailing = last[1:]
            pairs[-1] = last[0] + trailing
    return pairs

def _map_to_star_sequence(normalized: str) -> List[Dict[str, Any]]:
    pairs = _generate_pairs(normalized)
    zero_count = normalized.count("0")
    five_count = normalized.count("5")
    special_attr = ""
    special_effect = ""
    if zero_count:
        special_attr = "zero"
        special_effect = "Số 0 làm giảm năng lượng của các sao"
    if five_count:
        special_attr = f"{special_attr}_five" if special_attr else "five"
        msg = "Số 5 tăng cường năng lượng của các sao"
        special_effect = f"{special_effect}, {msg}" if special_effect else msg
    sequence: List[Dict[str,Any]] = []
    for pair in pairs:
        zeroes = pair.count("0")
        fives = pair.count("5")
        clean = "".join(d for d in pair if d not in ("0","5"))
        star_key, star_obj = None, None
        for k,v in BAT_TINH.items():
            if clean in v.get("numbers",[]):
                star_key, star_obj = k, v
                break
        base_energy = star_obj.get("energy", {}).get(clean, 1) if star_obj else 1
        energy_level = max(1, base_energy + fives - zeroes)
        level = _get_star_level(energy_level)
        response_factor = RESPONSE_FACTORS.get("STAR_RESPONSE_FACTORS", {}).get(star_key, 1)
        weighted = energy_level
        adjusted = weighted * response_factor
        sequence.append({
            "originalPair": pair,
            "mappedPair": clean,
            "star": star_key or "UNKNOWN",
            "name": star_obj.get("name", "") if star_obj else "",
            "nature": star_obj.get("nature", "") if star_obj else "",
            "level": level,
            "energyLevel": energy_level,
            "baseEnergyLevel": base_energy,
            "specialAttribute": special_attr,
            "specialEffect": special_effect,
            "detailedDescription": star_obj.get("detailedDescription", "") if star_obj else "",
            "description": star_obj.get("description", "") if star_obj else "",
            "isZeroVariant": zeroes > 0,
            "zeroCount": zeroes,
            "fiveCount": fives,
            "weightedEnergy": weighted,
            "responseFactor": response_factor,
            "adjustedEnergy": adjusted
        })
    return sequence

def _analyze_purpose_compatibility(star_sequence: List[Dict[str, Any]], purpose: str) -> Dict[str, Any]:
    """Phân tích độ phù hợp với mục đích sử dụng"""
    # Các mục đích phổ biến
    purposes = {
        "business": {
            "name": "Kinh doanh",
            "favorable_stars": ["THIEN_Y", "DIEN_NIEN"],
            "unfavorable_stars": ["TUYET_MENH", "NGU_QUY"]
        },
        "personal": {
            "name": "Cá nhân",
            "favorable_stars": ["SINH_KHI", "THIEN_Y"],
            "unfavorable_stars": ["HOA_HAI", "LUC_SAT"]
        },
        "wealth": {
            "name": "Tài lộc",
            "favorable_stars": ["THIEN_Y", "SINH_KHI"],
            "unfavorable_stars": ["TUYET_MENH", "HOA_HAI"]
        },
        "relationship": {
            "name": "Tình cảm",
            "favorable_stars": ["SINH_KHI", "THIEN_Y"],
            "unfavorable_stars": ["LUC_SAT", "NGU_QUY"]
        },
        "career": {
            "name": "Sự nghiệp",
            "favorable_stars": ["DIEN_NIEN", "SINH_KHI"],
            "unfavorable_stars": ["NGU_QUY", "TUYET_MENH"]
        }
    }
    
    # Đánh giá độ phù hợp với mục đích đã chọn
    selected_purpose = purposes.get(purpose)
    if not selected_purpose:
        return {
            "status": "error",
            "message": f"Mục đích '{purpose}' không được hỗ trợ"
        }
    
    favorable_count = 0
    unfavorable_count = 0
    
    for pair in star_sequence:
        if pair["star"] in selected_purpose["favorable_stars"]:
            favorable_count += 1
        if pair["star"] in selected_purpose["unfavorable_stars"]:
            unfavorable_count += 1
    
    # Tính điểm phù hợp (thang 10)
    compatibility_score = 5  # Mặc định trung bình
    if len(star_sequence) > 0:
        # Điểm cộng cho sao thuận lợi và trừ cho sao không thuận lợi
        compatibility_score += (favorable_count * 2 - unfavorable_count * 1.5) / len(star_sequence) * 5
        compatibility_score = min(10, max(1, round(compatibility_score)))
    
    # Đánh giá
    rating = ""
    if compatibility_score >= 9:
        rating = "★★★★★ (Rất tốt)"
    elif compatibility_score >= 7:
        rating = "★★★★☆ (Tốt)"
    elif compatibility_score >= 5:
        rating = "★★★☆☆ (Trung bình)"
    elif compatibility_score >= 3:
        rating = "★★☆☆☆ (Kém)"
    else:
        rating = "★☆☆☆☆ (Rất kém)"
    
    # Lời khuyên
    advice = ""
    if compatibility_score >= 8:
        advice = f"Số điện thoại này rất phù hợp cho mục đích {selected_purpose['name']}."
    elif compatibility_score >= 6:
        advice = f"Số điện thoại này phù hợp cho mục đích {selected_purpose['name']}."
    elif compatibility_score >= 4:
        advice = f"Số điện thoại này có thể sử dụng cho mục đích {selected_purpose['name']}, nhưng không lý tưởng."
    else:
        advice = f"Số điện thoại này không phù hợp cho mục đích {selected_purpose['name']}. Nên cân nhắc số khác."
    
    return {
        "purpose": selected_purpose["name"],
        "compatibility_score": compatibility_score,
        "rating": rating,
        "favorable_count": favorable_count,
        "unfavorable_count": unfavorable_count,
        "advice": advice
    }

# Tạo Function Tool thay vì class tự định nghĩa
phone_analyzer_tool = FunctionTool(func=analyze_phone_number) 