const axios = require('axios');
const dotenv = require('dotenv');
const fs = require('fs');
const path = require('path');

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
    
    // Khởi tạo logger
    this.setupLogger();
    
    this.apiClient = axios.create({
      baseURL: baseURL,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
      },
      timeout: 10000, // 10 second timeout
      maxRedirects: 3,
      retry: 2, // Thử lại 2 lần nếu gặp lỗi
      retryDelay: 1000 // Chờ 1 giây trước khi thử lại
    });
    
    // Thêm interceptor để tự động thử lại khi gặp lỗi
    this.apiClient.interceptors.response.use(undefined, async (err) => {
      const { config } = err;
      if (!config || !config.retry) {
        return Promise.reject(err);
      }
      
      // Giảm số lần retry còn lại
      config.retry -= 1;
      
      if (config.retry === 0) {
        return Promise.reject(err);
      }
      
      // Tạo promise delay
      const delayRetry = new Promise(resolve => {
        setTimeout(resolve, config.retryDelay || 1000);
      });
      
      // Thử lại sau khi delay
      await delayRetry;
      console.log('🔄 Đang thử lại kết nối đến Python ADK...');
      this.log('info', `Đang thử lại kết nối đến Python ADK: ${config.url}`);
      return this.apiClient(config);
    });
  }
  
  /**
   * Thiết lập logger
   */
  setupLogger() {
    try {
      const logDir = path.join(__dirname, '../../../logs');
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
      this.logPath = path.join(logDir, 'adk-connection.log');
      this.log('info', '🔢 Khởi tạo Bát Cục Linh Số Service');
    } catch (error) {
      console.error('❌ Không thể thiết lập logger:', error);
    }
  }
  
  /**
   * Ghi log
   * @param {string} level - Cấp độ log (info, warn, error)
   * @param {string} message - Thông báo log
   */
  log(level, message) {
    if (!this.logPath) return;
    
    try {
      const timestamp = new Date().toISOString();
      const logEntry = `[${timestamp}] [${level.toUpperCase()}] ${message}\n`;
      fs.appendFileSync(this.logPath, logEntry);
    } catch (error) {
      console.error('❌ Lỗi khi ghi log:', error);
    }
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