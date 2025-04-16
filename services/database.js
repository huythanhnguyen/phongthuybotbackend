// services/database.js - Kết nối và quản lý database

const mongoose = require('mongoose');

/**
 * Kết nối đến MongoDB
 */
const connectDatabase = async () => {
  try {
    const mongoURI = process.env.MONGODB_URI || 'mongodb://localhost:27017/phong_thuy_so';
    
    // Cấu hình kết nối
    const options = {
      // Loại bỏ các option đã được deprecated
      serverSelectionTimeoutMS: 5000, // Thời gian timeout cho quá trình chọn server
      connectTimeoutMS: 10000, // Thời gian timeout kết nối
    };

    // Thực hiện kết nối
    await mongoose.connect(mongoURI, options);
    
    console.log('✅ Kết nối thành công đến MongoDB');
    
    // Xử lý sự kiện mất kết nối
    mongoose.connection.on('error', (err) => {
      console.error('❌ Lỗi kết nối MongoDB:', err);
    });

    mongoose.connection.on('disconnected', () => {
      console.warn('⚠️ Mất kết nối đến MongoDB, đang thử kết nối lại...');
    });

    // Xử lý khi Node.js process kết thúc
    process.on('SIGINT', async () => {
      try {
        await mongoose.connection.close();
        console.log('📝 Đóng kết nối MongoDB do ứng dụng kết thúc');
        process.exit(0);
      } catch (err) {
        console.error('❌ Lỗi khi đóng kết nối MongoDB:', err);
        process.exit(1);
      }
    });
    
    return mongoose.connection;
  } catch (error) {
    console.error('❌ Lỗi kết nối đến MongoDB:', error.message);
    // Không thoát quy trình, chỉ throw lỗi để xử lý ở nơi gọi
    throw error;
  }
};

module.exports = { connectDatabase }; 