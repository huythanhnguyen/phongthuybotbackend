/**
 * Payment API Routes
 * 
 * Các routes để quản lý thanh toán và gói dịch vụ
 */

const express = require('express');
const router = express.Router();
const axios = require('axios');
const config = require('../../../config');
const { authenticateToken } = require('../middleware/auth');

// Cấu hình ADK API service
const ADK_SERVICE_URL = config.ADK_SERVICE_URL || 'http://localhost:8000';

/**
 * @route   GET /api/v2/payment/plans
 * @desc    Lấy danh sách các gói dịch vụ
 * @access  Public
 */
router.get('/plans', async (req, res) => {
  try {
    // Gọi đến ADK service
    const response = await axios.get(`${ADK_SERVICE_URL}/api/payment/plans`);
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error fetching plans:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi lấy danh sách gói dịch vụ' });
  }
});

/**
 * @route   POST /api/v2/payment/create
 * @desc    Tạo yêu cầu thanh toán mới
 * @access  Private
 */
router.post('/create', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.user_id;
    const { plan_id } = req.body;
    
    // Validate input
    if (!plan_id) {
      return res.status(400).json({ success: false, message: 'Gói dịch vụ là bắt buộc' });
    }
    
    // Gọi đến ADK service
    const response = await axios.post(
      `${ADK_SERVICE_URL}/api/payment/create?user_id=${userId}`,
      { plan_id }
    );
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error creating payment:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi tạo yêu cầu thanh toán' });
  }
});

/**
 * @route   GET /api/v2/payment/verify/:paymentCode
 * @desc    Xác thực thanh toán
 * @access  Public
 */
router.get('/verify/:paymentCode', async (req, res) => {
  try {
    const paymentCode = req.params.paymentCode;
    
    // Validate input
    if (!paymentCode) {
      return res.status(400).json({ success: false, message: 'Mã thanh toán là bắt buộc' });
    }
    
    // Gọi đến ADK service
    const response = await axios.get(
      `${ADK_SERVICE_URL}/api/payment/verify/${paymentCode}`
    );
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error verifying payment:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi xác thực thanh toán' });
  }
});

/**
 * @route   GET /api/v2/payment/subscription
 * @desc    Kiểm tra thông tin gói dịch vụ của người dùng
 * @access  Private
 */
router.get('/subscription', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.user_id;
    
    // Gọi đến ADK service
    const response = await axios.get(
      `${ADK_SERVICE_URL}/api/payment/subscription/${userId}`
    );
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error checking subscription:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi kiểm tra gói dịch vụ' });
  }
});

/**
 * @route   GET /api/v2/payment/history
 * @desc    Lấy lịch sử thanh toán của người dùng
 * @access  Private
 */
router.get('/history', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.user_id;
    
    // Gọi đến ADK service
    const response = await axios.get(
      `${ADK_SERVICE_URL}/api/payment/history/${userId}`
    );
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error fetching payment history:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi lấy lịch sử thanh toán' });
  }
});

/**
 * @route   POST /api/v2/payment/cancel/:paymentCode
 * @desc    Hủy thanh toán
 * @access  Private
 */
router.post('/cancel/:paymentCode', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.user_id;
    const paymentCode = req.params.paymentCode;
    
    // Validate input
    if (!paymentCode) {
      return res.status(400).json({ success: false, message: 'Mã thanh toán là bắt buộc' });
    }
    
    // Gọi đến ADK service
    // Tạo query trực tiếp đến agent vì chưa có endpoint này
    const response = await axios.post(`${ADK_SERVICE_URL}/query`, {
      query: `cancel_payment ${paymentCode} ${userId}`,
      agent_type: 'payment',
      user_id: userId
    });
    
    return res.json({
      success: true,
      message: 'Hủy thanh toán thành công'
    });
  } catch (error) {
    console.error('Error canceling payment:', error.message);
    
    // Kiểm tra lỗi cụ thể từ ADK service
    if (error.response && error.response.data) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ success: false, message: 'Lỗi hủy thanh toán' });
  }
});

module.exports = router; 