/**
 * Middleware xử lý lỗi cho API v2
 */

/**
 * Xử lý lỗi từ API request
 * @param {Error} err - Lỗi xảy ra
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next middleware function
 */
const errorHandler = (err, req, res, next) => {
  console.error('Error:', err);

  // Xác định mã lỗi HTTP
  let statusCode = err.statusCode || 500;

  // Xác định thông báo lỗi
  let message = err.message || 'Đã xảy ra lỗi trên server';

  // Định dạng và trả về phản hồi lỗi
  res.status(statusCode).json({
    success: false,
    error: {
      message,
      stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
    }
  });
};

module.exports = errorHandler; 