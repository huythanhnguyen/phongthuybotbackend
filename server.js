// server.js - Entry point cho Phong Thủy Số Backend

// Import dependencies
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const dotenv = require('dotenv');
const path = require('path');
const { connectDatabase } = require('./services/database');

// Load environment variables
dotenv.config();

// Create Express app
const app = express();

// Middleware
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? ['https://phongthuyso.onrender.com', 'https://bat-cuc-linh-so.phongthuyso.onrender.com']
    : 'http://localhost:5173',
  credentials: true
}));
app.use(morgan('dev'));

// Import routes
const batCucLinhSoRoutes = require('./api/v2/routes/bat-cuc-linh-so');

// Routes
app.use('/api/v2/bat-cuc-linh-so', batCucLinhSoRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'ok', message: 'Phong Thủy Số API is running' });
});

// Main API endpoint
app.get('/', (req, res) => {
  res.status(200).json({ 
    message: 'Chào mừng đến với Phong Thủy Số API v2',
    version: '2.0.0',
    status: process.env.NODE_ENV || 'development'
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: err.message || 'Đã xảy ra lỗi server',
    error: process.env.NODE_ENV === 'development' ? err : {}
  });
});

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
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Server đang chạy trên cổng ${PORT}`);
  console.log(`API có thể truy cập tại http://localhost:${PORT}`);
});

module.exports = app;