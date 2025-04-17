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
      cccdAnalysis: 'POST /api/v2/bat-cuc-linh-so/cccd'
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

    if (!type || !['phone', 'cccd'].includes(type)) {
      return res.status(400).json({
        success: false,
        message: 'Loại phân tích không hợp lệ. Vui lòng sử dụng "phone" hoặc "cccd"'
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

    // Phân tích số điện thoại
    const result = await batCucLinhSoService.analyzePhoneNumber(phoneNumber);

    // Trả về kết quả
    res.status(200).json({
      success: true,
      message: 'Phân tích số điện thoại thành công',
      result
    });
  } catch (error) {
    console.error('Lỗi khi phân tích số điện thoại:', error);
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

module.exports = router; 