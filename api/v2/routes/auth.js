const express = require('express');
const router = express.Router();
const rootAgentService = require('../services/rootAgentService');

/**
 * @route   GET /api/v2/auth
 * @desc    Thông tin về API Authentication
 * @access  Public
 */
router.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'Phong Thủy Số - Auth API',
    version: '2.0.0',
    endpoints: {
      login: 'POST /api/v2/auth/login',
      register: 'POST /api/v2/auth/register',
      logout: 'POST /api/v2/auth/logout',
      me: 'GET /api/v2/auth/me',
      changePassword: 'POST /api/v2/auth/change-password'
    }
  });
});

/**
 * @route   POST /api/v2/auth/login
 * @desc    Đăng nhập người dùng
 * @access  Public
 */
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    if (!email || !password) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp email và mật khẩu'
      });
    }

    // Gọi Root Agent để xử lý đăng nhập
    const result = await rootAgentService.queryAgent({
      agentType: 'auth',
      query: 'login',
      metadata: { email, password }
    });

    if (!result.success) {
      return res.status(401).json({
        success: false,
        message: result.message || 'Đăng nhập không thành công'
      });
    }

    res.status(200).json({
      success: true,
      message: 'Đăng nhập thành công',
      token: result.token,
      user: result.user
    });
  } catch (error) {
    console.error('Lỗi khi đăng nhập:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi đăng nhập',
      error: error.message
    });
  }
});

/**
 * @route   POST /api/v2/auth/register
 * @desc    Đăng ký người dùng mới
 * @access  Public
 */
router.post('/register', async (req, res) => {
  try {
    const { name, email, password } = req.body;
    
    if (!name || !email || !password) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp đầy đủ thông tin đăng ký'
      });
    }

    // Gọi Root Agent để xử lý đăng ký
    const result = await rootAgentService.queryAgent({
      agentType: 'auth',
      query: 'register',
      metadata: { name, email, password }
    });

    if (!result.success) {
      return res.status(400).json({
        success: false,
        message: result.message || 'Đăng ký không thành công'
      });
    }

    res.status(201).json({
      success: true,
      message: 'Đăng ký thành công',
      token: result.token,
      user: result.user
    });
  } catch (error) {
    console.error('Lỗi khi đăng ký:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi đăng ký',
      error: error.message
    });
  }
});

/**
 * @route   POST /api/v2/auth/logout
 * @desc    Đăng xuất người dùng
 * @access  Public
 */
router.post('/logout', async (req, res) => {
  try {
    // Lấy token từ header
    const token = req.headers.authorization?.split(' ')[1];
    
    // Gọi Root Agent để xử lý đăng xuất
    const result = await rootAgentService.queryAgent({
      agentType: 'auth',
      query: 'logout',
      metadata: { token }
    });

    res.status(200).json({
      success: true,
      message: 'Đăng xuất thành công'
    });
  } catch (error) {
    console.error('Lỗi khi đăng xuất:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi đăng xuất',
      error: error.message
    });
  }
});

/**
 * @route   GET /api/v2/auth/me
 * @desc    Lấy thông tin người dùng hiện tại
 * @access  Private
 */
router.get('/me', async (req, res) => {
  try {
    // Lấy token từ header
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'Không tìm thấy token, yêu cầu xác thực'
      });
    }

    // Gọi Root Agent để xác thực token
    const result = await rootAgentService.queryAgent({
      agentType: 'auth',
      query: 'verify_token',
      metadata: { token }
    });

    if (!result.success) {
      return res.status(401).json({
        success: false,
        message: 'Token không hợp lệ hoặc đã hết hạn'
      });
    }

    res.status(200).json({
      success: true,
      user: result.user
    });
  } catch (error) {
    console.error('Lỗi khi xác thực người dùng:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi xác thực người dùng',
      error: error.message
    });
  }
});

/**
 * @route   POST /api/v2/auth/change-password
 * @desc    Thay đổi mật khẩu người dùng
 * @access  Private
 */
router.post('/change-password', async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body;
    
    if (!currentPassword || !newPassword) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp mật khẩu hiện tại và mật khẩu mới'
      });
    }

    // Lấy token từ header
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'Không tìm thấy token, yêu cầu xác thực'
      });
    }

    // Gọi Root Agent để thay đổi mật khẩu
    const result = await rootAgentService.queryAgent({
      agentType: 'auth',
      query: 'change_password',
      metadata: { token, currentPassword, newPassword }
    });

    if (!result.success) {
      return res.status(400).json({
        success: false,
        message: result.message || 'Không thể thay đổi mật khẩu'
      });
    }

    res.status(200).json({
      success: true,
      message: 'Thay đổi mật khẩu thành công'
    });
  } catch (error) {
    console.error('Lỗi khi thay đổi mật khẩu:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi thay đổi mật khẩu',
      error: error.message
    });
  }
});

module.exports = router; 