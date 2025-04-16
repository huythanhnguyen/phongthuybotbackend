// models/user.model.js - Model người dùng

const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

// Schema API Key
const apiKeySchema = new mongoose.Schema({
  key: {
    type: String,
    required: true,
    unique: true
  },
  name: {
    type: String,
    required: true
  },
  isActive: {
    type: Boolean,
    default: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  lastUsed: {
    type: Date,
    default: null
  },
  usageCount: {
    type: Number,
    default: 0
  },
  usageLimit: {
    type: Number,
    default: 100
  },
  permissions: {
    type: [String],
    default: ['phoneAnalysis', 'cccdAnalysis', 'bankAccountAnalysis', 'passwordAnalysis']
  }
});

// Schema người dùng
const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Vui lòng nhập tên'],
    trim: true
  },
  email: {
    type: String,
    required: [true, 'Vui lòng nhập email'],
    unique: true,
    trim: true,
    lowercase: true,
    match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Email không hợp lệ']
  },
  password: {
    type: String,
    required: [true, 'Vui lòng nhập mật khẩu'],
    minlength: [6, 'Mật khẩu phải có ít nhất 6 ký tự'],
    select: false
  },
  phone: {
    type: String,
    trim: true
  },
  isAdmin: {
    type: Boolean,
    default: false
  },
  isActive: {
    type: Boolean,
    default: true
  },
  remainingQuestions: {
    type: Number,
    default: 3
  },
  apiKeys: [apiKeySchema],
  analysisHistory: [
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Analysis'
    }
  ],
  createdAt: {
    type: Date,
    default: Date.now
  },
  lastLoginAt: {
    type: Date,
    default: null
  }
}, {
  timestamps: true
});

// Hash mật khẩu trước khi lưu
userSchema.pre('save', async function(next) {
  // Chỉ hash mật khẩu nếu nó được thay đổi
  if (!this.isModified('password')) {
    return next();
  }
  
  try {
    // Tạo salt
    const salt = await bcrypt.genSalt(10);
    
    // Hash mật khẩu với salt
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Tạo API key mới cho người dùng
userSchema.methods.createApiKey = function(name, permissions = []) {
  // Tạo key ngẫu nhiên
  const key = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  
  // Tạo API key mới
  const apiKey = {
    key,
    name: name || `API Key ${this.apiKeys.length + 1}`,
    isActive: true,
    createdAt: new Date(),
    permissions: permissions.length > 0 ? permissions : ['phoneAnalysis', 'cccdAnalysis', 'bankAccountAnalysis', 'passwordAnalysis']
  };
  
  // Thêm vào danh sách API keys
  this.apiKeys.push(apiKey);
  
  return apiKey;
};

// So sánh mật khẩu đã nhập với mật khẩu trong database
userSchema.methods.matchPassword = async function(enteredPassword) {
  return await bcrypt.compare(enteredPassword, this.password);
};

// Kiểm tra xem người dùng còn đủ số lượt phân tích không
userSchema.methods.hasRemainingQuestions = function() {
  return this.remainingQuestions > 0;
};

// Giảm số lượt phân tích còn lại
userSchema.methods.decrementRemainingQuestions = function() {
  if (this.remainingQuestions > 0) {
    this.remainingQuestions -= 1;
  }
  
  return this.remainingQuestions;
};

// Tạo model từ schema
const User = mongoose.model('User', userSchema);

module.exports = User; 