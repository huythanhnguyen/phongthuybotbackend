const express = require('express');
const router = express.Router();
const batCucLinhSoService = require('../services/batCucLinhSoService');

/**
 * @route   GET /api/v2/bat-cuc-linh-so
 * @desc    Thông tin về API Bát Cục Linh Số
 * @access  Public
 */
router.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'API Bát Cục Linh Số v2.0',
    endpoints: {
      analyze: 'POST /api/v2/bat-cuc-linh-so/analyze',
      phoneAnalysis: 'POST /api/v2/bat-cuc-linh-so/phone',
      cccdAnalysis: 'POST /api/v2/bat-cuc-linh-so/cccd',
      passwordAnalysis: 'POST /api/v2/bat-cuc-linh-so/password',
      bankAccountAnalysis: 'POST /api/v2/bat-cuc-linh-so/bank-account',
      bankAccountSuggestion: 'POST /api/v2/bat-cuc-linh-so/suggest-bank-account'
    }
  });
});

/**
 * @route   POST /api/v2/bat-cuc-linh-so/analyze
 * @desc    Phân tích thông tin theo Bát Cục Linh Số
 * @access  Public
 */
router.post('/analyze', async (req, res) => {
  try {
    const { data, type } = req.body;
    
    if (!data) {
      return res.status(400).json({
        success: false,
        message: 'Thiếu dữ liệu để phân tích'
      });
    }

    if (!type || !['phone', 'cccd', 'password', 'bank_account'].includes(type)) {
      return res.status(400).json({
        success: false,
        message: 'Loại phân tích không hợp lệ. Vui lòng sử dụng "phone", "cccd", "password" hoặc "bank_account"'
      });
    }

    // Phân tích dữ liệu
    const result = await batCucLinhSoService.analyze(data, type);

    res.status(200).json({
      success: true,
      message: 'Phân tích thành công',
      type,
      result
    });
  } catch (error) {
    console.error('Lỗi khi phân tích:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi phân tích',
      error: error.message
    });
  }
});

/**
 * @route   POST /api/v2/bat-cuc-linh-so/phone
 * @desc    Phân tích số điện thoại theo Bát Cục Linh Số
 * @access  Public
 */
router.post('/phone', async (req, res) => {
  try {
    const { phoneNumber } = req.body;
    
    if (!phoneNumber) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp số điện thoại'
      });
    }

    // Kiểm tra định dạng số điện thoại
    const phoneRegex = /^(0|\+84)([0-9]{9,10})$/;
    if (!phoneRegex.test(phoneNumber)) {
      return res.status(400).json({
        success: false,
        message: 'Số điện thoại không hợp lệ, vui lòng cung cấp số điện thoại Việt Nam'
      });
    }

    try {
      // Phân tích số điện thoại
      const result = await batCucLinhSoService.analyzePhoneNumber(phoneNumber);
      
      // Kiểm tra nếu kết quả là fallback
      if (result && result.message && result.message.includes('Không kết nối được')) {
        // Trả về kết quả fallback với status 206 (Partial Content)
        return res.status(206).json({
          success: true,
          partial: true,
          message: 'Phân tích cơ bản số điện thoại thành công (chế độ offline)',
          result
        });
      }
      
      // Trả về kết quả đầy đủ
      res.status(200).json({
        success: true,
        message: 'Phân tích số điện thoại thành công',
        result
      });
    } catch (analysisError) {
      console.error('⚠️ Lỗi khi phân tích số điện thoại:', analysisError);
      
      // Kiểm tra nếu là lỗi kết nối
      if (analysisError.message && analysisError.message.includes('kết nối')) {
        return res.status(503).json({
          success: false,
          message: 'Dịch vụ phân tích tạm thời không khả dụng',
          error: analysisError.message
        });
      }
      
      // Lỗi khác
      throw analysisError;
    }
  } catch (error) {
    console.error('❌ Lỗi khi phân tích số điện thoại:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi phân tích số điện thoại',
      error: error.message
    });
  }
});

/**
 * @route   POST /api/v2/bat-cuc-linh-so/cccd
 * @desc    Phân tích CCCD/CMND theo Bát Cục Linh Số
 * @access  Public
 */
router.post('/cccd', async (req, res) => {
  try {
    const { cccdNumber } = req.body;
    
    if (!cccdNumber) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp số CCCD/CMND'
      });
    }

    // Chuẩn hóa số CCCD
    const normalizedCCCD = cccdNumber.replace(/[^0-9]/g, '');

    // Kiểm tra độ dài số CCCD/CMND
    if (normalizedCCCD.length !== 9 && normalizedCCCD.length !== 12) {
      return res.status(400).json({
        success: false,
        message: 'Số CCCD/CMND không hợp lệ, vui lòng cung cấp CMND 9 số hoặc CCCD 12 số'
      });
    }

    // Phân tích CCCD/CMND
    const result = await batCucLinhSoService.analyzeCCCD(normalizedCCCD);

    // Trả về kết quả
    res.status(200).json({
      success: true,
      message: 'Phân tích CCCD/CMND thành công',
      result
    });
  } catch (error) {
    console.error('Lỗi khi phân tích CCCD/CMND:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi phân tích CCCD/CMND',
      error: error.message
    });
  }
});

/**
 * @route   POST /api/v2/bat-cuc-linh-so/password
 * @desc    Phân tích mật khẩu theo Bát Cục Linh Số
 * @access  Public
 */
router.post('/password', async (req, res) => {
  try {
    const { password } = req.body;
    
    if (!password) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp mật khẩu để phân tích'
      });
    }

    // Kiểm tra độ dài mật khẩu
    if (password.length < 6) {
      return res.status(400).json({
        success: false,
        message: 'Mật khẩu quá ngắn, vui lòng cung cấp mật khẩu ít nhất 6 ký tự'
      });
    }

    // Phân tích mật khẩu
    const result = await batCucLinhSoService.analyzePassword(password);

    // Trả về kết quả
    res.status(200).json({
      success: true,
      message: 'Phân tích mật khẩu thành công',
      result
    });
  } catch (error) {
    console.error('Lỗi khi phân tích mật khẩu:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi phân tích mật khẩu',
      error: error.message
    });
  }
});

/**
 * @route   POST /api/v2/bat-cuc-linh-so/bank-account
 * @desc    Phân tích số tài khoản ngân hàng theo Bát Cục Linh Số
 * @access  Public
 */
router.post('/bank-account', async (req, res) => {
  try {
    const { accountNumber } = req.body;
    
    if (!accountNumber) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp số tài khoản ngân hàng'
      });
    }

    // Chuẩn hóa số tài khoản
    const normalizedAccount = accountNumber.replace(/[^0-9]/g, '');

    // Kiểm tra độ dài số tài khoản
    if (normalizedAccount.length < 6) {
      return res.status(400).json({
        success: false,
        message: 'Số tài khoản không hợp lệ, vui lòng cung cấp số tài khoản hợp lệ'
      });
    }

    // Phân tích số tài khoản
    const result = await batCucLinhSoService.analyzeBankAccount(normalizedAccount);

    // Trả về kết quả
    res.status(200).json({
      success: true,
      message: 'Phân tích số tài khoản thành công',
      result
    });
  } catch (error) {
    console.error('Lỗi khi phân tích số tài khoản:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi phân tích số tài khoản',
      error: error.message
    });
  }
});

/**
 * @route   POST /api/v2/bat-cuc-linh-so/suggest-bank-account
 * @desc    Gợi ý số tài khoản ngân hàng theo Bát Cục Linh Số
 * @access  Public
 */
router.post('/suggest-bank-account', async (req, res) => {
  try {
    const { purpose, preferredDigits } = req.body;
    
    if (!purpose) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp mục đích sử dụng tài khoản'
      });
    }

    // Kiểm tra mục đích
    const validPurposes = ['business', 'personal', 'investment', 'saving', 'health'];
    if (!validPurposes.includes(purpose)) {
      return res.status(400).json({
        success: false,
        message: `Mục đích không hợp lệ. Vui lòng sử dụng một trong các giá trị: ${validPurposes.join(', ')}`
      });
    }

    // Gợi ý số tài khoản
    const result = await batCucLinhSoService.suggestBankAccountNumbers(purpose, preferredDigits || []);

    // Trả về kết quả
    res.status(200).json({
      success: true,
      message: 'Gợi ý số tài khoản thành công',
      result
    });
  } catch (error) {
    console.error('Lỗi khi gợi ý số tài khoản:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi gợi ý số tài khoản',
      error: error.message
    });
  }
});

module.exports = router; 