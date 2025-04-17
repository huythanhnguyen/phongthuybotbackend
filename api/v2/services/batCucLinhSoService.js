const axios = require('axios');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Cấu hình kết nối đến Python ADK
const PYTHON_ADK_URL = process.env.PYTHON_ADK_URL || 'http://localhost:8000';
const API_KEY = process.env.ADK_API_KEY || 'dev_key';

/**
 * Service phân tích số điện thoại, CCCD theo phương pháp Bát Cục Linh Số
 */
class BatCucLinhSoService {
  /**
   * Khởi tạo dịch vụ
   */
  constructor() {
    console.log('🔢 Khởi tạo Bát Cục Linh Số Service');
    this.apiClient = axios.create({
      baseURL: `${PYTHON_ADK_URL}/api`,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
      }
    });
  }

  /**
   * Phân tích số điện thoại
   * @param {string} phoneNumber - Số điện thoại cần phân tích
   * @returns {Object} Kết quả phân tích
   */
  async analyzePhoneNumber(phoneNumber) {
    try {
      console.log(`📞 Phân tích số điện thoại: ${phoneNumber}`);

      // Chuẩn hóa số điện thoại (bỏ các ký tự đặc biệt)
      const normalizedPhone = phoneNumber.replace(/[^0-9+]/g, '');
      
      try {
        // Gọi API từ Python ADK
        const response = await this.apiClient.post('/batcuclinh_so/phone', {
          phone_number: normalizedPhone
        });
        
        if (response.data && response.status === 200) {
          console.log('✅ Phân tích thành công từ Python ADK');
          return response.data;
        }
      } catch (error) {
        console.warn('⚠️ Không thể kết nối đến Python ADK:', error.message);
        console.log('🔄 Sử dụng phân tích dự phòng');
        // Tiếp tục với phân tích dự phòng
      }
      
      // Phân tích dự phòng nếu không thể kết nối đến Python ADK
      return this._fallbackPhoneAnalysis(normalizedPhone);
    } catch (error) {
      console.error('❌ Lỗi khi phân tích số điện thoại:', error);
      throw new Error(`Lỗi phân tích: ${error.message}`);
    }
  }

  /**
   * Phân tích CCCD/CMND
   * @param {string} cccdNumber - Số CCCD/CMND cần phân tích
   * @returns {Object} Kết quả phân tích
   */
  async analyzeCCCD(cccdNumber) {
    try {
      console.log(`🪪 Phân tích CCCD/CMND: ${cccdNumber}`);

      // Chuẩn hóa số CCCD (bỏ các ký tự đặc biệt)
      const normalizedCCCD = cccdNumber.replace(/[^0-9]/g, '');
      
      try {
        // Gọi API từ Python ADK
        const response = await this.apiClient.post('/batcuclinh_so/cccd', {
          cccd_number: normalizedCCCD
        });
        
        if (response.data && response.status === 200) {
          console.log('✅ Phân tích CCCD thành công từ Python ADK');
          return response.data;
        }
      } catch (error) {
        console.warn('⚠️ Không thể kết nối đến Python ADK:', error.message);
        console.log('🔄 Sử dụng phân tích CCCD dự phòng');
        // Tiếp tục với phân tích dự phòng
      }
      
      // Phân tích dự phòng nếu không thể kết nối đến Python ADK
      return this._fallbackCCCDAnalysis(normalizedCCCD);
    } catch (error) {
      console.error('❌ Lỗi khi phân tích CCCD/CMND:', error);
      throw new Error(`Lỗi phân tích: ${error.message}`);
    }
  }

  /**
   * Phân tích thông tin chung
   * @param {string} data - Dữ liệu cần phân tích
   * @param {string} type - Loại phân tích
   * @returns {Object} Kết quả phân tích
   */
  async analyze(data, type) {
    switch (type) {
      case 'phone':
        return await this.analyzePhoneNumber(data);
      case 'cccd':
        return await this.analyzeCCCD(data);
      default:
        throw new Error(`Loại phân tích không hỗ trợ: ${type}`);
    }
  }

  /**
   * Phân tích dự phòng cho số điện thoại
   * @private
   * @param {string} phoneNumber - Số điện thoại cần phân tích
   * @returns {Object} Kết quả phân tích dự phòng
   */
  _fallbackPhoneAnalysis(phoneNumber) {
    // Tính tổng các chữ số
    const sum = [...phoneNumber].reduce((total, digit) => {
      return total + (isNaN(parseInt(digit)) ? 0 : parseInt(digit));
    }, 0);
    
    // Rút gọn thành số có 1 chữ số
    let reducedSum = sum;
    while (reducedSum > 9) {
      reducedSum = [...reducedSum.toString()].reduce((total, digit) => {
        return total + parseInt(digit);
      }, 0);
    }
    
    // Xác định ngũ hành
    const element = this._getElement(reducedSum);
    
    // Phân tích cơ bản
    const analysis = `
    Phân tích số điện thoại: ${phoneNumber}
    
    Tổng giá trị: ${sum} (Rút gọn: ${reducedSum})
    Ngũ hành: ${element}
    
    Đây là kết quả phân tích dự phòng khi không thể kết nối đến Python ADK.
    Vui lòng thử lại sau khi hệ thống đã được khởi động đầy đủ.
    `;
    
    return {
      success: true,
      phoneNumber,
      totalValue: reducedSum,
      element,
      analysis
    };
  }
  
  /**
   * Phân tích dự phòng cho CCCD/CMND
   * @private
   * @param {string} cccdNumber - Số CCCD/CMND cần phân tích
   * @returns {Object} Kết quả phân tích dự phòng
   */
  _fallbackCCCDAnalysis(cccdNumber) {
    // Tính tổng các chữ số
    const sum = [...cccdNumber].reduce((total, digit) => {
      return total + parseInt(digit);
    }, 0);
    
    // Rút gọn thành số có 1 chữ số
    let reducedSum = sum;
    while (reducedSum > 9) {
      reducedSum = [...reducedSum.toString()].reduce((total, digit) => {
        return total + parseInt(digit);
      }, 0);
    }
    
    // Xác định ngũ hành
    const element = this._getElement(reducedSum);
    
    // Phân tích cơ bản
    let info = {};
    
    // Trích xuất thông tin từ CCCD 12 số
    if (cccdNumber.length === 12) {
      const provinceCode = cccdNumber.substring(0, 3);
      const genderCode = parseInt(cccdNumber[3]);
      const birthYear = cccdNumber.substring(4, 6);
      
      // Mapping giới tính và thế kỷ
      let gender = "Không xác định";
      let century = "xx";
      
      if (genderCode === 0 || genderCode === 2 || genderCode === 4 || genderCode === 6 || genderCode === 8) {
        gender = "Nam";
      } else if (genderCode === 1 || genderCode === 3 || genderCode === 5 || genderCode === 7 || genderCode === 9) {
        gender = "Nữ";
      }
      
      if (genderCode === 0 || genderCode === 1) {
        century = "19";
      } else if (genderCode === 2 || genderCode === 3) {
        century = "20";
      } else if (genderCode === 4 || genderCode === 5) {
        century = "21";
      }
      
      info = {
        type: "CCCD",
        provinceCode,
        gender,
        birthYear: `${century}${birthYear}`,
        randomCode: cccdNumber.substring(6)
      };
    } else if (cccdNumber.length === 9) {
      info = {
        type: "CMND",
        note: "CMND 9 số không có cấu trúc cố định để trích xuất thông tin chi tiết"
      };
    }
    
    const analysis = `
    Phân tích số ${info.type || "CCCD/CMND"}: ${cccdNumber}
    
    Tổng giá trị: ${sum} (Rút gọn: ${reducedSum})
    Ngũ hành: ${element}
    
    ${info.type === "CCCD" ? `
    Thông tin cá nhân:
    - Mã tỉnh: ${info.provinceCode}
    - Giới tính: ${info.gender}
    - Năm sinh: ${info.birthYear}
    - Mã ngẫu nhiên: ${info.randomCode}
    ` : ''}
    
    Đây là kết quả phân tích dự phòng khi không thể kết nối đến Python ADK.
    Vui lòng thử lại sau khi hệ thống đã được khởi động đầy đủ.
    `;
    
    return {
      success: true,
      cccdNumber,
      totalValue: reducedSum,
      element,
      info,
      analysis
    };
  }
  
  /**
   * Xác định ngũ hành từ số
   * @private
   * @param {number} number - Số cần xác định ngũ hành
   * @returns {string} Ngũ hành tương ứng
   */
  _getElement(number) {
    const elements = {
      1: "Thủy",
      2: "Thổ",
      3: "Mộc",
      4: "Kim",
      5: "Thổ",
      6: "Kim",
      7: "Kim",
      8: "Thổ",
      9: "Hỏa",
      0: "Thủy"
    };
    
    return elements[number] || "Không xác định";
  }
}

module.exports = new BatCucLinhSoService(); 