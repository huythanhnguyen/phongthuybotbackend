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
      case 'password':
        return await this.analyzePassword(data);
      case 'bank_account':
        return await this.analyzeBankAccount(data);
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
    // Lấy 6 số cuối của CCCD để phân tích phong thủy
    const lastSix = cccdNumber.slice(-6);
    
    // Chuẩn hóa chuỗi số (xử lý số 0 và 5)
    const normalized = this._normalizeCccdSequence(lastSix);
    
    // Tách thành các cặp số chồng lấp
    const pairs = this._splitIntoOverlappingPairs(normalized);
    
    // Cấu trúc dữ liệu phân tích
    const analysisData = {
      pairsAnalysis: [],       // Phân tích từng cặp số
      combinationsAnalysis: [], // Phân tích tổ hợp các sao liền kề
      summary: ''              // Tóm tắt tổng quan
    };
    
    // Kiểm tra xem có thể tạo được cặp số không
    if (pairs.length === 0) {
      analysisData.summary = `Không thể tạo cặp số nào từ chuỗi chuẩn hóa '${normalized}' để phân tích.`;
      if (normalized.length < 2) {
        analysisData.summary += ` (Chuỗi chuẩn hóa quá ngắn).`;
      } else {
        analysisData.summary += ` (Kiểm tra lại logic chuẩn hóa).`;
      }
    } else {
      // Phân tích từng cặp số
      pairs.forEach((pair, index) => {
        const starInfo = this._getStarInfoForPair(pair);
        analysisData.pairsAnalysis.push({
          pairNumber: index + 1,
          digits: pair,
          starKey: starInfo.key,
          star: starInfo.name,
          meaning: starInfo.description,
          nature: starInfo.nature,
          energyLevel: starInfo.energy
        });
      });
      
      // Phân tích tổ hợp các sao liền kề (nếu có nhiều hơn 1 cặp)
      if (analysisData.pairsAnalysis.length > 1) {
        for (let i = 0; i < analysisData.pairsAnalysis.length - 1; i++) {
          const star1Info = analysisData.pairsAnalysis[i];
          const star2Info = analysisData.pairsAnalysis[i + 1];
          
          if (star1Info.starKey !== "UNKNOWN" && star2Info.starKey !== "UNKNOWN") {
            const combinationInfo = this._getStarCombinationInfo(star1Info.starKey, star2Info.starKey);
            if (combinationInfo) {
              analysisData.combinationsAnalysis.push({
                combinationNumber: i + 1,
                stars: `${star1Info.star} (${star1Info.digits}) + ${star2Info.star} (${star2Info.digits})`,
                meaning: combinationInfo.description,
                details: combinationInfo.detailedDescription
              });
            }
          }
        }
      }
      
      // Tạo tóm tắt
      const starSequence = analysisData.pairsAnalysis.map(p => p.star).join(' -> ');
      analysisData.summary = `Phân tích dựa trên chuỗi số chuẩn hóa '${normalized}' (${pairs.length} cặp số, ${analysisData.combinationsAnalysis.length} kết hợp). Chuỗi sao: ${starSequence}.`;
      
      if (pairs.length < 5 && lastSix.includes('5')) {
        analysisData.summary += ` (Lưu ý: Số cặp số ít hơn 5 do có số 5 trong 6 số cuối).`;
      }
    }
    
    // Trích xuất thông tin từ cấu trúc CCCD (tương tự phần cũ)
    let info = {};
    
    if (cccdNumber.length === 12) {
      const provinceCode = cccdNumber.substring(0, 3);
      const genderCode = parseInt(cccdNumber[3]);
      const birthYear = cccdNumber.substring(4, 6);
      
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
    
    return {
      success: true,
      originalNumber: cccdNumber,
      lastSixDigits: lastSix,
      normalizedSequence: normalized,
      pairs: pairs,
      analysis: {
        individualPairs: analysisData.pairsAnalysis,
        starCombinations: analysisData.combinationsAnalysis,
        overallSummary: analysisData.summary
      },
      info
    };
  }
  
  /**
   * Chuẩn hóa chuỗi số CCCD theo quy tắc:
   * 1. Số 0: Thay thế bằng số liền trước khác 0 (hoặc số cuối cùng của chuỗi gốc nếu không có)
   * 2. Số 5: Loại bỏ khỏi chuỗi
   * @param {string} digits - Chuỗi 6 số cuối của CCCD
   * @returns {string} Chuỗi số đã chuẩn hóa (có thể ngắn hơn 6 số)
   */
  _normalizeCccdSequence(digits) {
    let processedDigits = digits.split('');
    const lastOriginalDigit = digits[digits.length - 1]; // Lưu số cuối cùng của chuỗi gốc
    
    // Bước 1: Xử lý số 0
    for (let i = 0; i < processedDigits.length; i++) {
      if (processedDigits[i] === '0') {
        let j = i - 1;
        while (j >= 0 && processedDigits[j] === '0') {
          j--;
        }
        // Sử dụng số khác 0 đã tìm được, hoặc số cuối cùng nếu không tìm thấy
        processedDigits[i] = (j >= 0) ? processedDigits[j] : lastOriginalDigit;
      }
    }
    
    // Bước 2: Loại bỏ số 5
    const normalized = processedDigits.filter(digit => digit !== '5').join('');
    
    return normalized;
  }
  
  /**
   * Tách chuỗi số đã chuẩn hóa thành các cặp số chồng lấp
   * @param {string} sequence - Chuỗi số đã chuẩn hóa
   * @returns {string[]} Mảng các cặp số chồng lấp
   */
  _splitIntoOverlappingPairs(sequence) {
    const pairs = [];
    if (!sequence || sequence.length < 2) {
      return pairs; // Không thể tạo cặp
    }
    for (let i = 0; i < sequence.length - 1; i++) {
      pairs.push(sequence.substring(i, i + 2));
    }
    return pairs;
  }
  
  /**
   * Lấy thông tin sao cho một cặp số
   * @param {string} pair - Cặp số cần phân tích
   * @returns {Object} Thông tin sao tương ứng
   */
  _getStarInfoForPair(pair) {
    // Require tại đây để tránh circular dependency
    const BAT_TINH = require('../../../constants/batTinh');
    
    for (const starKey in BAT_TINH) {
      if (starKey.includes('_ZERO') || starKey.includes('_FIVE')) {
        continue;
      }
      const starData = BAT_TINH[starKey];
      if (starData.numbers && starData.numbers.includes(pair)) {
        return {
          key: starKey,
          name: starData.name,
          description: starData.description,
          nature: starData.nature,
          energy: starData.energy[pair] || 3 // Mặc định là 3 nếu không có thông tin
        };
      }
    }
    
    return {
      key: "UNKNOWN",
      name: "Không xác định",
      description: "Không có thông tin",
      nature: "Không xác định",
      energy: 1
    };
  }
  
  /**
   * Lấy thông tin tổ hợp hai sao liền kề
   * @param {string} starKey1 - Khóa của sao thứ nhất
   * @param {string} starKey2 - Khóa của sao thứ hai
   * @returns {Object|null} Thông tin tổ hợp hai sao
   */
  _getStarCombinationInfo(starKey1, starKey2) {
    // Require tại đây để tránh circular dependency
    const COMBINATIONS = require('../../../constants/combinations');
    
    const combinationKey = `${starKey1}_${starKey2}`;
    if (COMBINATIONS.STAR_PAIRS && COMBINATIONS.STAR_PAIRS[combinationKey]) {
      const comboData = COMBINATIONS.STAR_PAIRS[combinationKey];
      return {
        combination: `${starKey1} - ${starKey2}`,
        description: comboData.description,
        detailedDescription: comboData.detailedDescription || []
      };
    }
    return null;
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

  /**
   * Phân tích mật khẩu theo phong thủy
   * @param {string} password - Mật khẩu cần phân tích
   * @returns {Object} Kết quả phân tích mật khẩu theo phong thủy
   */
  async analyzePassword(password) {
    try {
      console.log(`🔐 Phân tích mật khẩu theo phong thủy`);
      
      try {
        // Gọi API từ Python ADK
        const response = await this.apiClient.post('/batcuclinh_so/password', {
          password: password
        });
        
        if (response.data && response.status === 200) {
          console.log('✅ Phân tích mật khẩu thành công từ Python ADK');
          return response.data;
        }
      } catch (error) {
        console.warn('⚠️ Không thể kết nối đến Python ADK:', error.message);
        console.log('🔄 Sử dụng phân tích mật khẩu dự phòng');
        // Tiếp tục với phân tích dự phòng
      }
      
      // Phân tích dự phòng nếu không thể kết nối đến Python ADK
      return this._fallbackPasswordAnalysis(password);
    } catch (error) {
      console.error('❌ Lỗi khi phân tích mật khẩu:', error);
      throw new Error(`Lỗi phân tích: ${error.message}`);
    }
  }

  /**
   * Phân tích dự phòng cho mật khẩu
   * @private
   * @param {string} password - Mật khẩu cần phân tích
   * @returns {Object} Kết quả phân tích dự phòng
   */
  _fallbackPasswordAnalysis(password) {
    // Trích xuất các số từ mật khẩu
    const numbers = password.replace(/[^0-9]/g, '');
    
    // Nếu không có số, trả về kết quả mặc định
    if (!numbers || numbers.length === 0) {
      return {
        success: true,
        password: password.replace(/./g, '*'), // Che mật khẩu bằng dấu *
        hasDigits: false,
        analysis: {
          summary: 'Mật khẩu không chứa số để phân tích theo Bát Cục Linh Số.',
          recommendation: 'Cân nhắc thêm các số có ý nghĩa phong thủy tốt vào mật khẩu.'
        },
        securityLevel: this._assessPasswordStrength(password)
      };
    }
    
    // Tìm các cặp số liền kề trong mật khẩu
    const pairs = this._findDigitPairsInPassword(password);
    
    // Cấu trúc dữ liệu phân tích
    const analysisData = {
      digitalPresence: `Mật khẩu chứa ${numbers.length} chữ số (${numbers.length / password.length * 100}%).`,
      pairsAnalysis: [],       // Phân tích từng cặp số
      badCombinations: [],     // Các kết hợp hung tinh
      goodCombinations: [],    // Các kết hợp cát tinh
      recommendation: ''       // Đề xuất cải thiện
    };
    
    // Phân tích từng cặp số
    let hasNegativeStar = false;
    
    pairs.forEach(pair => {
      const starInfo = this._getStarInfoForPair(pair.digits);
      const pairAnalysis = {
        position: `${pair.startIndex}-${pair.startIndex + 1}`,
        digits: pair.digits,
        starKey: starInfo.key,
        star: starInfo.name,
        nature: starInfo.nature
      };
      
      analysisData.pairsAnalysis.push(pairAnalysis);
      
      // Kiểm tra hung/cát tinh
      if (starInfo.nature === 'Hung tinh') {
        hasNegativeStar = true;
        analysisData.badCombinations.push(`${starInfo.name} (${pair.digits}) tại vị trí ${pair.startIndex+1}`);
      } else if (starInfo.nature === 'Cát tinh') {
        analysisData.goodCombinations.push(`${starInfo.name} (${pair.digits}) tại vị trí ${pair.startIndex+1}`);
      }
    });
    
    // Tạo đề xuất cải thiện
    if (hasNegativeStar) {
      analysisData.recommendation = 'Nên thay đổi các cặp số hung tinh bằng các cặp số cát tinh để cải thiện năng lượng.';
    } else if (analysisData.pairsAnalysis.length === 0) {
      analysisData.recommendation = 'Thêm các cặp số có ý nghĩa tốt theo Bát Cục Linh Số để tăng cường năng lượng.';
    } else {
      analysisData.recommendation = 'Mật khẩu có năng lượng tốt về mặt số học.';
    }
    
    // Tóm tắt
    let summary = '';
    if (analysisData.badCombinations.length > 0) {
      summary += `Phát hiện ${analysisData.badCombinations.length} cặp số hung tinh. `;
    }
    if (analysisData.goodCombinations.length > 0) {
      summary += `Phát hiện ${analysisData.goodCombinations.length} cặp số cát tinh. `;
    }
    summary += analysisData.recommendation;
    
    return {
      success: true,
      password: password.replace(/./g, '*'), // Che mật khẩu bằng dấu *
      hasDigits: true,
      digitCount: numbers.length,
      digitPairs: pairs.length,
      analysis: {
        details: analysisData,
        summary: summary
      },
      securityLevel: this._assessPasswordStrength(password)
    };
  }
  
  /**
   * Tìm các cặp số liền kề trong mật khẩu
   * @private
   * @param {string} password - Mật khẩu cần phân tích
   * @returns {Array} Mảng các cặp số liền kề và vị trí của chúng
   */
  _findDigitPairsInPassword(password) {
    const pairs = [];
    
    for (let i = 0; i < password.length - 1; i++) {
      const char1 = password[i];
      const char2 = password[i + 1];
      
      // Kiểm tra nếu cả hai ký tự là số
      if (/^\d$/.test(char1) && /^\d$/.test(char2)) {
        pairs.push({
          startIndex: i,
          digits: char1 + char2
        });
      }
    }
    
    return pairs;
  }
  
  /**
   * Đánh giá độ mạnh của mật khẩu
   * @private
   * @param {string} password - Mật khẩu cần đánh giá
   * @returns {Object} Thông tin về độ mạnh của mật khẩu
   */
  _assessPasswordStrength(password) {
    let strength = 0;
    let feedback = [];
    
    // Kiểm tra độ dài
    if (password.length < 8) {
      feedback.push('Mật khẩu quá ngắn');
    } else if (password.length >= 12) {
      strength += 2;
    } else {
      strength += 1;
    }
    
    // Kiểm tra chữ thường
    if (/[a-z]/.test(password)) {
      strength += 1;
    } else {
      feedback.push('Nên thêm chữ cái thường');
    }
    
    // Kiểm tra chữ hoa
    if (/[A-Z]/.test(password)) {
      strength += 1;
    } else {
      feedback.push('Nên thêm chữ cái hoa');
    }
    
    // Kiểm tra số
    if (/\d/.test(password)) {
      strength += 1;
    } else {
      feedback.push('Nên thêm chữ số');
    }
    
    // Kiểm tra ký tự đặc biệt
    if (/[^A-Za-z0-9]/.test(password)) {
      strength += 1;
    } else {
      feedback.push('Nên thêm ký tự đặc biệt');
    }
    
    // Xác định mức độ an toàn
    let level = 'Yếu';
    if (strength >= 5) {
      level = 'Rất mạnh';
    } else if (strength >= 4) {
      level = 'Mạnh';
    } else if (strength >= 3) {
      level = 'Trung bình';
    }
    
    return {
      level,
      score: strength,
      feedback: feedback
    };
  }

  /**
   * Phân tích số tài khoản ngân hàng
   * @param {string} accountNumber - Số tài khoản ngân hàng cần phân tích
   * @returns {Object} Kết quả phân tích
   */
  async analyzeBankAccount(accountNumber) {
    try {
      console.log(`🏦 Phân tích số tài khoản ngân hàng: ${accountNumber}`);

      // Chuẩn hóa số tài khoản (bỏ các ký tự đặc biệt)
      const normalizedAccount = accountNumber.replace(/[^0-9]/g, '');
      
      try {
        // Gọi API từ Python ADK
        const response = await this.apiClient.post('/batcuclinh_so/bank_account', {
          account_number: normalizedAccount
        });
        
        if (response.data && response.status === 200) {
          console.log('✅ Phân tích số tài khoản thành công từ Python ADK');
          return response.data;
        }
      } catch (error) {
        console.warn('⚠️ Không thể kết nối đến Python ADK:', error.message);
        console.log('🔄 Sử dụng phân tích dự phòng');
        // Tiếp tục với phân tích dự phòng
      }
      
      // Phân tích dự phòng nếu không thể kết nối đến Python ADK
      return this._fallbackBankAccountAnalysis(normalizedAccount);
    } catch (error) {
      console.error('❌ Lỗi khi phân tích số tài khoản ngân hàng:', error);
      throw new Error(`Lỗi phân tích: ${error.message}`);
    }
  }

  /**
   * Tạo gợi ý số tài khoản ngân hàng
   * @param {string} purpose - Mục đích của tài khoản (business, personal, investment, saving)
   * @param {Array} preferredDigits - Các chữ số ưa thích (không bắt buộc)
   * @returns {Object} Các gợi ý số tài khoản
   */
  async suggestBankAccountNumbers(purpose, preferredDigits = []) {
    try {
      console.log(`🏦 Gợi ý số tài khoản ngân hàng cho mục đích: ${purpose}`);
      
      try {
        // Gọi API từ Python ADK
        const response = await this.apiClient.post('/batcuclinh_so/suggest_bank_account', {
          purpose: purpose,
          preferred_digits: preferredDigits
        });
        
        if (response.data && response.status === 200) {
          console.log('✅ Gợi ý số tài khoản thành công từ Python ADK');
          return response.data;
        }
      } catch (error) {
        console.warn('⚠️ Không thể kết nối đến Python ADK:', error.message);
        console.log('🔄 Sử dụng gợi ý dự phòng');
        // Tiếp tục với gợi ý dự phòng
      }
      
      // Gợi ý dự phòng nếu không thể kết nối đến Python ADK
      return this._fallbackBankAccountSuggestion(purpose, preferredDigits);
    } catch (error) {
      console.error('❌ Lỗi khi gợi ý số tài khoản ngân hàng:', error);
      throw new Error(`Lỗi gợi ý: ${error.message}`);
    }
  }

  /**
   * Phân tích dự phòng cho số tài khoản ngân hàng
   * @private
   * @param {string} accountNumber - Số tài khoản ngân hàng cần phân tích
   * @returns {Object} Kết quả phân tích dự phòng
   */
  _fallbackBankAccountAnalysis(accountNumber) {
    // Lấy 4 số cuối của tài khoản
    const lastFour = accountNumber.slice(-4);
    
    // Tạo các cặp số từ 4 số cuối
    const pairs = [];
    if (lastFour.length >= 2) {
      pairs.push(lastFour.substring(0, 2));
      
      if (lastFour.length >= 3) {
        pairs.push(lastFour.substring(1, 3));
        
        if (lastFour.length >= 4) {
          pairs.push(lastFour.substring(2, 4));
        }
      }
    }
    
    // Cấu trúc dữ liệu phân tích
    const analysisData = {
      pairsAnalysis: [],       // Phân tích từng cặp số
      favorableFor: [],        // Thuận lợi cho mục đích nào
      overallRating: 0,        // Đánh giá tổng thể (1-10)
      summary: ''              // Tóm tắt tổng quan
    };
    
    let totalEnergy = 0;
    let pairsCount = 0;
    
    // Phân tích từng cặp số
    pairs.forEach((pair, index) => {
      const starInfo = this._getStarInfoForPair(pair);
      const pairAnalysis = {
        pairNumber: index + 1,
        digits: pair,
        starKey: starInfo.key,
        star: starInfo.name,
        meaning: starInfo.description,
        nature: starInfo.nature,
        energyLevel: starInfo.energy
      };
      
      analysisData.pairsAnalysis.push(pairAnalysis);
      
      // Cộng dồn năng lượng cho đánh giá tổng thể
      if (starInfo.nature === 'Cát tinh') {
        totalEnergy += starInfo.energy;
        pairsCount++;
        
        // Xác định mục đích phù hợp
        if (starInfo.key === 'THIEN_GIAI' || starInfo.key === 'THIEN_Y') {
          if (!analysisData.favorableFor.includes('health')) {
            analysisData.favorableFor.push('health');
          }
        }
        
        if (starInfo.key === 'THIEN_TAI' || starInfo.key === 'THIEN_Y') {
          if (!analysisData.favorableFor.includes('wealth')) {
            analysisData.favorableFor.push('wealth');
          }
        }
        
        if (starInfo.key === 'THIEN_MAN' || starInfo.key === 'THIEN_HAU') {
          if (!analysisData.favorableFor.includes('happiness')) {
            analysisData.favorableFor.push('happiness');
          }
        }
        
        if (starInfo.key === 'THIEN_LO' || starInfo.key === 'THIEN_TAI') {
          if (!analysisData.favorableFor.includes('business')) {
            analysisData.favorableFor.push('business');
          }
        }
      } else if (starInfo.nature === 'Hung tinh') {
        totalEnergy -= starInfo.energy;
        pairsCount++;
      }
    });
    
    // Tính đánh giá tổng thể
    if (pairsCount > 0) {
      const averageEnergy = totalEnergy / pairsCount;
      
      // Chuyển đổi sang thang điểm 10
      analysisData.overallRating = Math.min(10, Math.max(1, Math.round(5 + averageEnergy)));
      
      // Tạo tóm tắt
      if (analysisData.overallRating >= 8) {
        analysisData.summary = 'Số tài khoản ngân hàng có năng lượng rất tốt. Phù hợp cho mục đích: ' + 
          (analysisData.favorableFor.length > 0 ? analysisData.favorableFor.join(', ') : 'tích lũy tài chính chung');
      } else if (analysisData.overallRating >= 5) {
        analysisData.summary = 'Số tài khoản ngân hàng có năng lượng trung bình.';
      } else {
        analysisData.summary = 'Số tài khoản ngân hàng có năng lượng không thuận lợi. Nên cân nhắc thay đổi.';
      }
    } else {
      analysisData.overallRating = 5;
      analysisData.summary = 'Không thể phân tích số tài khoản do không có cặp số phù hợp.';
    }
    
    return {
      success: true,
      accountNumber: accountNumber,
      lastFourDigits: lastFour,
      pairs: pairs,
      analysis: analysisData
    };
  }
  
  /**
   * Gợi ý dự phòng cho số tài khoản ngân hàng
   * @private
   * @param {string} purpose - Mục đích của tài khoản
   * @param {Array} preferredDigits - Các chữ số ưa thích
   * @returns {Object} Kết quả gợi ý dự phòng
   */
  _fallbackBankAccountSuggestion(purpose, preferredDigits = []) {
    console.log(`Tạo gợi ý số tài khoản cho mục đích: ${purpose}`);
    
    // Xác định các sao phù hợp với mục đích
    let targetStars = [];
    
    switch (purpose.toLowerCase()) {
      case 'business':
        // Thích hợp cho kinh doanh
        targetStars = ['THIEN_LO', 'THIEN_TAI', 'THIEN_HOA'];
        break;
      case 'investment':
        // Thích hợp cho đầu tư
        targetStars = ['THIEN_TAI', 'THIEN_PHUC', 'THIEN_LINH'];
        break;
      case 'saving':
        // Thích hợp cho tiết kiệm
        targetStars = ['THIEN_TAI', 'THIEN_THU', 'THIEN_NGUYET'];
        break;
      case 'health':
        // Thích hợp cho sức khỏe
        targetStars = ['THIEN_Y', 'THIEN_GIAI', 'THIEN_NGUYET'];
        break;
      default:
        // Personal - chung chung
        targetStars = ['THIEN_TAI', 'THIEN_Y', 'THIEN_MAN'];
        break;
    }
    
    // Lấy các cặp số tương ứng với các sao mục tiêu
    const suitablePairs = this._getSuitableDigitPairs(targetStars, preferredDigits);
    
    // Tạo đề xuất
    const recommendations = [];
    
    // Tạo các tổ hợp cặp số cuối từ hai cặp số
    for (let i = 0; i < Math.min(suitablePairs.length, 10); i++) {
      const firstPair = suitablePairs[i];
      
      for (let j = 0; j < Math.min(suitablePairs.length, 10); j++) {
        if (i !== j) {
          const secondPair = suitablePairs[j];
          
          // Kết hợp để tạo 4 số cuối
          if (secondPair.digits[0] === firstPair.digits[1]) {
            // Nếu chữ số đầu của cặp thứ hai trùng với chữ số cuối của cặp đầu tiên
            // thì tạo thành một dãy 3 số liên tục
            const lastFour = firstPair.digits + secondPair.digits[1];
            
            recommendations.push({
              lastFourDigits: lastFour,
              stars: `${firstPair.star} + ${secondPair.star}`,
              energyLevel: (firstPair.energyLevel + secondPair.energyLevel) / 2,
              description: `Kết hợp ${firstPair.star} (${firstPair.digits}) và ${secondPair.star} (${secondPair.digits})`
            });
          }
          
          // Nếu đã đủ 5 đề xuất thì dừng
          if (recommendations.length >= 5) {
            break;
          }
        }
      }
      
      // Nếu đã đủ 5 đề xuất thì dừng
      if (recommendations.length >= 5) {
        break;
      }
    }
    
    // Nếu chưa đủ đề xuất, thêm các cặp riêng lẻ
    if (recommendations.length < 5) {
      for (let i = 0; i < Math.min(suitablePairs.length, 5 - recommendations.length); i++) {
        const pair = suitablePairs[i];
        
        // Tạo số cuối bằng cách lặp lại cặp số
        recommendations.push({
          lastFourDigits: pair.digits + pair.digits,
          stars: `${pair.star} (kép)`,
          energyLevel: pair.energyLevel,
          description: `${pair.star} (${pair.digits}) lặp lại để tăng cường năng lượng`
        });
      }
    }
    
    // Sắp xếp theo mức năng lượng
    recommendations.sort((a, b) => b.energyLevel - a.energyLevel);
    
    return {
      success: true,
      purpose: purpose,
      preferredDigits: preferredDigits,
      recommendations: recommendations,
      note: 'Đây là đề xuất dự phòng. Vui lòng thử lại khi Python ADK sẵn sàng để có kết quả chính xác hơn.'
    };
  }
  
  /**
   * Lấy các cặp số phù hợp với các sao được chỉ định
   * @private
   * @param {Array} targetStars - Các sao mục tiêu
   * @param {Array} preferredDigits - Các chữ số ưa thích (không bắt buộc)
   * @returns {Array} Mảng các cặp số phù hợp và thông tin của chúng
   */
  _getSuitableDigitPairs(targetStars, preferredDigits = []) {
    // Require tại đây để tránh circular dependency
    const BAT_TINH = require('../../../constants/batTinh');
    
    const result = [];
    
    // Duyệt qua các sao mục tiêu
    for (const starKey of targetStars) {
      if (BAT_TINH[starKey]) {
        const starData = BAT_TINH[starKey];
        
        // Duyệt qua các cặp số của sao này
        if (starData.numbers && Array.isArray(starData.numbers)) {
          for (const pair of starData.numbers) {
            // Kiểm tra nếu cặp số chứa các chữ số ưa thích
            const containsPreferred = preferredDigits.length === 0 ||
              preferredDigits.some(d => pair.includes(d));
            
            if (containsPreferred) {
              result.push({
                digits: pair,
                star: starData.name,
                starKey: starKey,
                nature: starData.nature,
                energyLevel: starData.energy[pair] || 3
              });
            }
          }
        }
      }
    }
    
    // Sắp xếp theo mức năng lượng
    result.sort((a, b) => b.energyLevel - a.energyLevel);
    
    return result;
  }
}

module.exports = new BatCucLinhSoService(); 