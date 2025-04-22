const axios = require('axios');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Cấu hình kết nối đến Python ADK
const PROD_ADK_URL = 'https://phongthuybotadk.onrender.com';
const DEV_ADK_URL = process.env.PYTHON_ADK_URL || 'http://localhost:8000';
const API_KEY = process.env.ADK_API_KEY || 'dev_key';
const NODE_ENV = process.env.NODE_ENV || 'development';

/**
 * Service phân tích số điện thoại, CCCD theo phương pháp Bát Cục Linh Số
 */
class BatCucLinhSoService {
  /**
   * Khởi tạo dịch vụ
   */
  constructor() {
    console.log('🔢 Khởi tạo Bát Cục Linh Số Service');
    const baseURL = NODE_ENV === 'production' ? PROD_ADK_URL : DEV_ADK_URL;
    console.log(`🔗 Kết nối đến Python ADK: ${baseURL}`);
    
    this.apiClient = axios.create({
      baseURL: baseURL,
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
      
      // Gọi API từ Python ADK
      const response = await this.apiClient.post('/analyze/phone', {
        phone_number: normalizedPhone
      });
      
      if (response.data && response.status === 200) {
        console.log('✅ Phân tích thành công từ Python ADK');
        return response.data;
      }
      
      throw new Error('Không nhận được phản hồi hợp lệ từ Python ADK');
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
      
      // Gọi API từ Python ADK
      const response = await this.apiClient.post('/analyze/cccd', {
        cccd_number: normalizedCCCD
      });
      
      if (response.data && response.status === 200) {
        console.log('✅ Phân tích CCCD thành công từ Python ADK');
        return response.data;
      }
      
      throw new Error('Không nhận được phản hồi hợp lệ từ Python ADK');
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
   * Phân tích mật khẩu theo phong thủy
   * @param {string} password - Mật khẩu cần phân tích
   * @returns {Object} Kết quả phân tích mật khẩu theo phong thủy
   */
  async analyzePassword(password) {
    try {
      console.log(`🔐 Phân tích mật khẩu theo phong thủy`);
      
      // Gọi API từ Python ADK
      const response = await this.apiClient.post('/analyze/password', {
        password: password
      });
      
      if (response.data && response.status === 200) {
        console.log('✅ Phân tích mật khẩu thành công từ Python ADK');
        return response.data;
      }
      
      throw new Error('Không nhận được phản hồi hợp lệ từ Python ADK');
    } catch (error) {
      console.error('❌ Lỗi khi phân tích mật khẩu:', error);
      throw new Error(`Lỗi phân tích: ${error.message}`);
    }
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
      
      // Gọi API từ Python ADK
      const response = await this.apiClient.post('/analyze/bank-account', {
        account_number: normalizedAccount
      });
      
      if (response.data && response.status === 200) {
        console.log('✅ Phân tích số tài khoản thành công từ Python ADK');
        return response.data;
      }
      
      throw new Error('Không nhận được phản hồi hợp lệ từ Python ADK');
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
      
      // Gọi API từ Python ADK
      const response = await this.apiClient.post('/suggest/bank-account', {
        purpose: purpose,
        preferred_digits: preferredDigits
      });
      
      if (response.data && response.status === 200) {
        console.log('✅ Gợi ý số tài khoản thành công từ Python ADK');
        return response.data;
      }
      
      throw new Error('Không nhận được phản hồi hợp lệ từ Python ADK');
    } catch (error) {
      console.error('❌ Lỗi khi gợi ý số tài khoản ngân hàng:', error);
      throw new Error(`Lỗi gợi ý: ${error.message}`);
    }
  }
}

module.exports = new BatCucLinhSoService(); 