// server/controllers/authController.js
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const config = require('../config/env');

// Helper: Tạo JWT token
const generateToken = (id) => {
  return jwt.sign({ id }, config.JWT_SECRET, {
    expiresIn: config.JWT_EXPIRES
  });
};

// Đăng ký người dùng mới
exports.register = async (req, res) => {
  try {
    const { name, email, password, phoneNumber } = req.body;

    // Kiểm tra email đã tồn tại
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({
        success: false,
        message: 'Email đã được sử dụng'
      });
    }

    // Tạo người dùng mới với remainingQuestions và isPremium
    const user = await User.create({
      name,
      email,
      password,
      phoneNumber,
      remainingQuestions: config.TRIAL_QUESTIONS,
      isPremium: false
    });

    // Tạo token
    const token = generateToken(user._id);

    res.status(201).json({
      success: true,
      token,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        phoneNumber: user.phoneNumber,
        role: user.role,
        remainingQuestions: user.remainingQuestions,
        isPremium: user.isPremium
      }
    });
  } catch (error) {
    console.error('Register error:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi đăng ký tài khoản',
      error: error.message
    });
  }
};

// Đăng nhập
exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;

    // Kiểm tra email và password
    if (!email || !password) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp email và mật khẩu'
      });
    }

    // Tìm người dùng và bao gồm trường password
    const user = await User.findOne({ email }).select('+password');

    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Email hoặc mật khẩu không chính xác'
      });
    }

    // Kiểm tra mật khẩu
    const isMatch = await user.matchPassword(password);

    if (!isMatch) {
      return res.status(401).json({
        success: false,
        message: 'Email hoặc mật khẩu không chính xác'
      });
    }

    // Cập nhật thời gian đăng nhập
    await user.updateLastLogin();

    // Tạo token
    const token = generateToken(user._id);

    res.json({
      success: true,
      token,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        phoneNumber: user.phoneNumber,
        role: user.role,
        remainingQuestions: user.remainingQuestions,
        isPremium: user.isPremium
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi đăng nhập',
      error: error.message
    });
  }
};

// Lấy thông tin người dùng hiện tại
exports.getCurrentUser = async (req, res) => {
  try {
    const user = req.user;

    res.json({
      success: true,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        phoneNumber: user.phoneNumber,
        role: user.role,
        createdAt: user.createdAt,
        lastLogin: user.lastLogin,
        remainingQuestions: user.remainingQuestions,
        isPremium: user.isPremium
      }
    });
  } catch (error) {
    console.error('Get current user error:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi lấy thông tin người dùng',
      error: error.message
    });
  }
};

// Xác thực token
exports.verifyToken = async (req, res) => {
  try {
    // Middleware authenticate đã kiểm tra và giải mã token rồi
    // và đã đặt thông tin user vào req.user
    res.json({
      valid: true,
      user: {
        id: req.user._id,
        name: req.user.name,
        email: req.user.email,
        phoneNumber: req.user.phoneNumber,
        role: req.user.role,
        createdAt: req.user.createdAt,
        lastLogin: req.user.lastLogin,
        remainingQuestions: req.user.remainingQuestions,
        isPremium: req.user.isPremium
      }
    });
  } catch (error) {
    console.error('Verify token error:', error);
    res.status(500).json({
      valid: false,
      message: 'Lỗi khi xác thực token',
      error: error.message
    });
  }
};

// Đổi mật khẩu
exports.changePassword = async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body;
    const userId = req.user.id;

    // Lấy người dùng với mật khẩu
    const user = await User.findById(userId).select('+password');

    // Kiểm tra mật khẩu hiện tại
    const isMatch = await user.matchPassword(currentPassword);

    if (!isMatch) {
      return res.status(401).json({
        success: false,
        message: 'Mật khẩu hiện tại không chính xác'
      });
    }

    // Cập nhật mật khẩu mới
    user.password = newPassword;
    await user.save();

    res.json({
      success: true,
      message: 'Đổi mật khẩu thành công'
    });
  } catch (error) {
    console.error('Change password error:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi đổi mật khẩu',
      error: error.message
    });
  }
};

// Quên mật khẩu - yêu cầu đặt lại
exports.forgotPassword = async (req, res) => {
  try {
    const { email } = req.body;

    // Tìm người dùng 
    const user = await User.findOne({ email });

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'Không tìm thấy người dùng với email này'
      });
    }

    // Tạo token đặt lại mật khẩu (trong thực tế sẽ gửi email)
    const resetToken = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });

    // Ở đây sẽ thêm code gửi email với link đặt lại mật khẩu
    // Trong phiên bản demo này, chúng ta trả về token trực tiếp

    res.json({
      success: true,
      message: 'Vui lòng kiểm tra email để đặt lại mật khẩu',
      resetToken // Chỉ trả về trong môi trường phát triển
    });
  } catch (error) {
    console.error('Forgot password error:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi xử lý yêu cầu đặt lại mật khẩu',
      error: error.message
    });
  }
};

// Đặt lại mật khẩu với token
exports.resetPassword = async (req, res) => {
  try {
    const { token, newPassword } = req.body;

    // Xác thực token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const userId = decoded.id;

    // Tìm và cập nhật người dùng
    const user = await User.findById(userId);

    if (!user) {
      return res.status(400).json({
        success: false,
        message: 'Token không hợp lệ hoặc đã hết hạn'
      });
    }

    // Cập nhật mật khẩu
    user.password = newPassword;
    await user.save();

    res.json({
      success: true,
      message: 'Đặt lại mật khẩu thành công'
    });
  } catch (error) {
    console.error('Reset password error:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi đặt lại mật khẩu',
      error: error.message
    });
  }
};

// Đăng xuất người dùng
exports.logout = async (req, res) => {
  try {
    // Lấy thông tin user từ middleware authenticate
    const userId = req.user._id;
    
    // Ghi log đăng xuất
    console.log(`User ${userId} logged out at ${new Date()}`);
    
    // Trả về phản hồi thành công
    res.status(200).json({
      success: true,
      message: 'Đăng xuất thành công'
    });
    
    // Lưu ý: JWT token vẫn có hiệu lực cho đến khi hết hạn
    // Việc "logout" chỉ xảy ra ở phía client khi họ xóa token
  } catch (error) {
    console.error('Logout error:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi đăng xuất',
      error: error.message
    });
  }
};