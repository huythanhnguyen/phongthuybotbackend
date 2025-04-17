const express = require('express');
const router = express.Router();
const rootAgentService = require('../services/rootAgentService');

/**
 * @route   GET /api/v2/agent
 * @desc    Thông tin về API Root Agent
 * @access  Public
 */
router.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'Phong Thủy Số - Root Agent API',
    version: '2.0.0',
    endpoints: {
      chat: 'POST /api/v2/agent/chat',
      stream: 'POST /api/v2/agent/stream',
      query: 'POST /api/v2/agent/query'
    }
  });
});

/**
 * @route   POST /api/v2/agent/chat
 * @desc    Gửi tin nhắn đến Root Agent và nhận phản hồi
 * @access  Public
 */
router.post('/chat', async (req, res) => {
  try {
    const { message, sessionId, userId, metadata } = req.body;
    
    if (!message) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp nội dung tin nhắn'
      });
    }

    // Gọi Root Agent để xử lý tin nhắn
    const result = await rootAgentService.processMessage({
      message,
      sessionId,
      userId,
      metadata
    });

    res.status(200).json({
      success: true,
      message: 'Xử lý tin nhắn thành công',
      result
    });
  } catch (error) {
    console.error('Lỗi khi xử lý tin nhắn:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi xử lý tin nhắn',
      error: error.message
    });
  }
});

/**
 * @route   POST /api/v2/agent/stream
 * @desc    Gửi tin nhắn đến Root Agent và nhận phản hồi dạng stream
 * @access  Public
 */
router.post('/stream', async (req, res) => {
  try {
    const { message, sessionId, userId, metadata } = req.body;
    
    if (!message) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp nội dung tin nhắn'
      });
    }

    // Thiết lập header cho streaming response
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    // Gọi Root Agent với callback để xử lý stream
    await rootAgentService.processMessageStream({
      message,
      sessionId,
      userId,
      metadata,
      onChunk: (chunk) => {
        res.write(`data: ${JSON.stringify(chunk)}\n\n`);
      },
      onComplete: () => {
        res.write(`data: ${JSON.stringify({ type: 'complete' })}\n\n`);
        res.end();
      },
      onError: (error) => {
        res.write(`data: ${JSON.stringify({ type: 'error', error: error.message })}\n\n`);
        res.end();
      }
    });
  } catch (error) {
    console.error('Lỗi khi xử lý stream:', error);
    res.write(`data: ${JSON.stringify({ type: 'error', error: error.message })}\n\n`);
    res.end();
  }
});

/**
 * @route   POST /api/v2/agent/query
 * @desc    Gửi truy vấn trực tiếp đến một agent cụ thể
 * @access  Public
 */
router.post('/query', async (req, res) => {
  try {
    const { agentType, query, sessionId, userId, metadata } = req.body;
    
    if (!query) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp nội dung truy vấn'
      });
    }

    if (!agentType) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng cung cấp loại agent'
      });
    }

    // Gọi trực tiếp đến agent cụ thể
    const result = await rootAgentService.queryAgent({
      agentType,
      query,
      sessionId,
      userId,
      metadata
    });

    res.status(200).json({
      success: true,
      message: 'Truy vấn thành công',
      result
    });
  } catch (error) {
    console.error('Lỗi khi truy vấn agent:', error);
    res.status(500).json({
      success: false,
      message: 'Đã xảy ra lỗi khi truy vấn agent',
      error: error.message
    });
  }
});

module.exports = router; 