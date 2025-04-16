const express = require('express');
const router = express.Router();

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
      phoneAnalysis: 'POST /api/v2/bat-cuc-linh-so/phone-analysis'
    }
  });
});

/**
 * @route   POST /api/v2/bat-cuc-linh-so/analyze
 * @desc    Phân tích thông tin theo Bát Cục Linh Số
 * @access  Public
 */
router.post('/analyze', (req, res) => {
  try {
    const { data, type } = req.body;
    
    if (!data) {
      return res.status(400).json({
        success: false,
        message: 'Thiếu dữ liệu để phân tích'
      });
    }

    // Tạm thời trả về kết quả giả lập
    res.status(200).json({
      success: true,
      message: 'Phân tích thành công',
      type: type || 'general',
      result: {
        data: data,
        analysis: `Đây là kết quả phân tích mẫu cho ${data}. Sẽ được kết nối với Python ADK sau.`,
        summary: 'Kết quả phân tích mẫu'
      }
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
 * @route   POST /api/v2/bat-cuc-linh-so/phone-analysis
 * @desc    Phân tích số điện thoại theo Bát Cục Linh Số
 * @access  Public
 */
router.post('/phone-analysis', (req, res) => {
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

    // Tạm thời trả về kết quả giả lập
    res.status(200).json({
      success: true,
      message: 'Phân tích số điện thoại thành công',
      result: {
        phoneNumber: phoneNumber,
        analysis: `Đây là kết quả phân tích mẫu cho số điện thoại ${phoneNumber}. Sẽ được kết nối với Python ADK sau.`,
        summary: 'Số điện thoại có năng lượng tốt',
        score: 8.5
      }
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

module.exports = router; 