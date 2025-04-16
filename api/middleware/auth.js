// api/middleware/auth.js - Middleware xác thực người dùng

const jwt = require('jsonwebtoken');
const User = require('../../models/user.model');

/**
 * Middleware xác thực người dùng bằng JWT
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 * @param {Function} next - Next middleware function
 */
const authenticate = async (req, res, next) => {
  try {
    // Lấy token từ header
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        success: false,
        message: 'Không tìm thấy token xác thực'
      });
    }
    
    const token = authHeader.split(' ')[1];
    
    // Giải mã token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Tìm người dùng theo ID
    const user = await User.findById(decoded.id).select('-password');
    
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Token không hợp lệ hoặc người dùng không tồn tại'
      });
    }
    
    // Lưu thông tin người dùng vào request
    req.user = user;
    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({
        success: false,
        message: 'Token không hợp lệ'
      });
    }
    
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        success: false,
        message: 'Token đã hết hạn'
      });
    }
    
    console.error('❌ Lỗi xác thực:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi server'
    });
  }
};

/**
 * Middleware kiểm tra quyền Admin
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 * @param {Function} next - Next middleware function
 */
const isAdmin = (req, res, next) => {
  // Middleware authenticate phải được gọi trước
  if (!req.user) {
    return res.status(401).json({
      success: false,
      message: 'Không tìm thấy thông tin người dùng'
    });
  }
  
  if (!req.user.isAdmin) {
    return res.status(403).json({
      success: false,
      message: 'Bạn không có quyền thực hiện hành động này'
    });
  }
  
  next();
};

/**
 * Middleware xác thực API key
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 * @param {Function} next - Next middleware function
 */
const authenticateApiKey = async (req, res, next) => {
  try {
    // Lấy API key từ header hoặc query parameter
    const apiKey = req.headers['x-api-key'] || req.query.api_key;
    
    if (!apiKey) {
      return res.status(401).json({
        success: false,
        message: 'Không tìm thấy API key'
      });
    }
    
    // Tìm người dùng theo API key
    const user = await User.findOne({
      'apiKeys.key': apiKey,
      'apiKeys.isActive': true
    });
    
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'API key không hợp lệ hoặc đã bị vô hiệu hóa'
      });
    }
    
    // Lưu thông tin người dùng vào request
    req.user = user;
    req.apiKey = apiKey;
    
    // Cập nhật thông tin sử dụng API key
    const apiKeyObj = user.apiKeys.find(k => k.key === apiKey);
    apiKeyObj.lastUsed = new Date();
    apiKeyObj.usageCount += 1;
    
    await user.save();
    
    next();
  } catch (error) {
    console.error('❌ Lỗi xác thực API key:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi server'
    });
  }
};

/**
 * Middleware xác thực thông qua JWT hoặc API key
 * @param {Object} req - Request object
 * @param {Object} res - Response object
 * @param {Function} next - Next middleware function
 */
const authenticateAny = async (req, res, next) => {
  try {
    // Kiểm tra API key trước
    const apiKey = req.headers['x-api-key'] || req.query.api_key;
    
    if (apiKey) {
      // Tìm người dùng theo API key
      const user = await User.findOne({
        'apiKeys.key': apiKey,
        'apiKeys.isActive': true
      });
      
      if (user) {
        // Lưu thông tin người dùng vào request
        req.user = user;
        req.apiKey = apiKey;
        
        // Cập nhật thông tin sử dụng API key
        const apiKeyObj = user.apiKeys.find(k => k.key === apiKey);
        apiKeyObj.lastUsed = new Date();
        apiKeyObj.usageCount += 1;
        
        await user.save();
        
        return next();
      }
    }
    
    // Nếu không có API key hoặc API key không hợp lệ, thử JWT
    const authHeader = req.headers.authorization;
    
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.split(' ')[1];
      
      // Giải mã token
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      
      // Tìm người dùng theo ID
      const user = await User.findById(decoded.id).select('-password');
      
      if (user) {
        // Lưu thông tin người dùng vào request
        req.user = user;
        return next();
      }
    }
    
    // Nếu không có API key và JWT, hoặc cả hai đều không hợp lệ
    res.status(401).json({
      success: false,
      message: 'Vui lòng cung cấp token hoặc API key hợp lệ'
    });
  } catch (error) {
    console.error('❌ Lỗi xác thực:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi server'
    });
  }
};

// Export middlewares
module.exports = {
  authenticate,
  isAdmin,
  authenticateApiKey,
  authenticateAny
}; 