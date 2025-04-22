// server.js - Entry point cho Phong Thủy Số Backend

// Import dependencies
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const dotenv = require('dotenv');
const path = require('path');
const { connectDatabase } = require('./services/database');
const errorHandler = require('./api/v2/middleware/errorHandler');

// Load environment variables
dotenv.config();

// Create Express app
const app = express();

// Middleware
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Thiết lập CORS, cho phép cả API URL và Frontend URL trong production
const allowedOrigins = process.env.NODE_ENV === 'production'
  ? [
      'https://phongthuyso.onrender.com',
      'https://bat-cuc-linh-so.phongthuyso.onrender.com',
      'https://a2aphongthuyso-front.onrender.com'
    ]
  : ['*'];
app.use(
  cors({
    origin: (origin, callback) => {
      // cho phép yêu cầu không có origin (ví dụ từ curl hoặc server-side)
      if (!origin || allowedOrigins.includes(origin) || allowedOrigins.includes('*')) {
        callback(null, true);
      } else {
        callback(new Error(`Origin ${origin} không được phép bởi CORS`));
      }
    },
    credentials: true
  })
);

app.use(morgan('dev'));

// Import routes
const batCucLinhSoRoutes = require('./api/v2/routes/bat-cuc-linh-so');
const rootAgentRoutes = require('./api/v2/routes/root-agent');

// Routes
app.use('/api/v2/bat-cuc-linh-so', batCucLinhSoRoutes);
app.use('/api/v2/agent', rootAgentRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({ 
    status: 'ok', 
    message: 'Phong Thủy Số API is running',
    version: '2.0.0',
    adkEnabled: process.env.PYTHON_ADK_URL ? true : false 
  });
});

// Main API endpoint
app.get('/', (req, res) => {
  res.status(200).json({ 
    message: 'Chào mừng đến với Phong Thủy Số API v2',
    version: '2.0.0',
    status: process.env.NODE_ENV || 'development',
    endpoints: {
      agent: '/api/v2/agent',
      batCucLinhSo: '/api/v2/bat-cuc-linh-so',
      health: '/api/health'
    }
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: `Không tìm thấy endpoint: ${req.method} ${req.originalUrl}`
  });
});

// Error handling middleware
app.use(errorHandler);

// Thử kết nối database nhưng không dừng server nếu thất bại
try {
  connectDatabase().catch(err => {
    console.warn('⚠️ Lỗi kết nối đến MongoDB:', err.message);
    console.log('🔄 Server vẫn tiếp tục chạy mà không có kết nối database');
  });
} catch (error) {
  console.warn('⚠️ Không thể kết nối đến MongoDB:', error.message);
  console.log('🔄 Server vẫn tiếp tục chạy mà không có kết nối database');
}

// Start server
const PORT = process.env.PORT || 6000;
app.listen(PORT, () => {
  console.log(`Server đang chạy trên cổng ${PORT}`);
  console.log(`API có thể truy cập tại http://localhost:${PORT}`);
});

module.exports = app;