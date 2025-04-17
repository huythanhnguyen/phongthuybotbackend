/**
 * User API Routes
 * 
 * Các routes để quản lý tài khoản người dùng và API keys
 */

const express = require('express');
const router = express.Router();
const axios = require('axios');
const config = require('../../../config');
const { authenticateToken } = require('../middleware/auth');

// Cấu hình ADK API service
const ADK_SERVICE_URL = config.ADK_SERVICE_URL || 'http://localhost:8000';

/**
 * @route   POST /api/v2/user/register
 * @desc    Đăng ký người dùng mới
 * @access  Public
 */
router.post('/register', async (req, res) => {
  try {
    const { email, password, name, phone } = req.body;
    
    // Validate input
    if (!email || !password) {
      return res.status(400).json({ success: false, message: 'Email và mật khẩu là bắt buộc' });
    }
    
    // Gọi đến ADK service
    const response = await axios.post(`${ADK_SERVICE_URL}/api/user/register`, {
      email,
      password,
      name,
      phone
    });
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error in user registration:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi đăng ký tài khoản' });
  }
});

/**
 * @route   POST /api/v2/user/login
 * @desc    Đăng nhập người dùng
 * @access  Public
 */
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Validate input
    if (!email || !password) {
      return res.status(400).json({ success: false, message: 'Email và mật khẩu là bắt buộc' });
    }
    
    // Gọi đến ADK service
    const response = await axios.post(`${ADK_SERVICE_URL}/api/user/login`, {
      email,
      password
    });
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error in user login:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi đăng nhập' });
  }
});

/**
 * @route   GET /api/v2/user/info
 * @desc    Lấy thông tin người dùng
 * @access  Private
 */
router.get('/info', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.user_id;
    
    // Gọi đến ADK service
    const response = await axios.get(`${ADK_SERVICE_URL}/api/user/info?user_id=${userId}`);
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error fetching user info:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi lấy thông tin người dùng' });
  }
});

/**
 * @route   POST /api/v2/user/apikey
 * @desc    Tạo API key mới
 * @access  Private
 */
router.post('/apikey', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.user_id;
    const { name, expiry_days, quota } = req.body;
    
    // Validate input
    if (!name) {
      return res.status(400).json({ success: false, message: 'Tên API key là bắt buộc' });
    }
    
    // Gọi đến ADK service
    const response = await axios.post(
      `${ADK_SERVICE_URL}/api/user/apikey?user_id=${userId}`,
      { name, expiry_days, quota }
    );
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error creating API key:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi tạo API key' });
  }
});

/**
 * @route   GET /api/v2/user/apikey
 * @desc    Lấy danh sách API keys
 * @access  Private
 */
router.get('/apikey', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.user_id;
    
    // Gọi đến ADK service
    const response = await axios.get(`${ADK_SERVICE_URL}/api/user/apikey?user_id=${userId}`);
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error fetching API keys:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi lấy danh sách API keys' });
  }
});

/**
 * @route   DELETE /api/v2/user/apikey/:keyId
 * @desc    Thu hồi API key
 * @access  Private
 */
router.delete('/apikey/:keyId', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.user_id;
    const keyId = req.params.keyId;
    
    // Gọi đến ADK service
    const response = await axios.delete(
      `${ADK_SERVICE_URL}/api/user/apikey/${keyId}?user_id=${userId}`
    );
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error revoking API key:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi thu hồi API key' });
  }
});

/**
 * @route   PUT /api/v2/user/profile
 * @desc    Cập nhật thông tin profile
 * @access  Private
 */
router.put('/profile', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.user_id;
    const { name, phone, email, password } = req.body;
    
    // Gọi đến ADK service
    // Tạo query trực tiếp đến agent vì chưa có endpoint này
    const response = await axios.post(`${ADK_SERVICE_URL}/query`, {
      query: `update_profile ${JSON.stringify({ 
        user_id: userId, 
        name, 
        phone, 
        email, 
        password 
      })}`,
      agent_type: 'user',
      user_id: userId
    });
    
    return res.json({
      success: true,
      message: 'Cập nhật thông tin thành công'
    });
  } catch (error) {
    console.error('Error updating profile:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi cập nhật thông tin' });
  }
});

module.exports = router; 