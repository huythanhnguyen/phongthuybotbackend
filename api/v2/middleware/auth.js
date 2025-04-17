/**
 * Authentication Middleware
 * 
 * Middleware để xác thực người dùng qua JWT token
 */

const axios = require('axios');
const config = require('../../../config');

// Cấu hình ADK API service
const ADK_SERVICE_URL = config.ADK_SERVICE_URL || 'http://localhost:8000';

/**
 * Middleware để xác thực JWT token
 * 
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
exports.authenticateToken = async (req, res, next) => {
  try {
    // Lấy token từ header
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
    
    if (!token) {
      return res.status(401).json({ success: false, message: 'Không tìm thấy token xác thực' });
    }
    
    // Xác thực token thông qua ADK service
    const response = await axios.post(`${ADK_SERVICE_URL}/query`, {
      query: `verify_token ${token}`,
      agent_type: 'user'
    });
    
    if (!response.data.success) {
      return res.status(403).json({ success: false, message: 'Token không hợp lệ hoặc đã hết hạn' });
    }
    
    // Lưu thông tin user vào request
    req.user = {
      user_id: response.data.response.user_id,
      email: response.data.response.email,
      role: response.data.response.role
    };
    
    next();
  } catch (error) {
    console.error('Error authenticating token:', error.message);
    return res.status(403).json({ success: false, message: 'Lỗi xác thực token' });
  }
};

/**
 * Middleware để xác thực API key
 * 
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
exports.authenticateApiKey = async (req, res, next) => {
  try {
    // Lấy API key từ header
    const apiKey = req.headers['x-api-key'];
    
    if (!apiKey) {
      return res.status(401).json({ success: false, message: 'Không tìm thấy API key' });
    }
    
    // Xác thực API key thông qua ADK service
    const response = await axios.post(`${ADK_SERVICE_URL}/query`, {
      query: `verify_api_key ${apiKey}`,
      agent_type: 'user'
    });
    
    if (!response.data.success) {
      return res.status(403).json({ success: false, message: 'API key không hợp lệ hoặc đã hết hạn' });
    }
    
    // Lưu thông tin user vào request
    req.user = {
      user_id: response.data.response.user_id,
      remaining_quota: response.data.response.remaining_quota
    };
    
    next();
  } catch (error) {
    console.error('Error authenticating API key:', error.message);
    return res.status(403).json({ success: false, message: 'Lỗi xác thực API key' });
  }
}; 