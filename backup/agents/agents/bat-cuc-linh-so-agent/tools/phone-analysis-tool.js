// agents/bat-cuc-linh-so-agent/tools/phone-analysis-tool.js - Công cụ phân tích số điện thoại

const { ADKClient } = require('@adk/node-client');
const { generateUniqueId } = require('../../../utils/id-generator');
const User = require('../../../models/user.model');

// Cấu hình ADK Client
const adkClient = new ADKClient({
  apiKey: process.env.ADK_API_KEY,
  baseUrl: process.env.ADK_BASE_URL || 'https://api.adk.io'
});

/**
 * Kiểm tra định dạng số điện thoại Việt Nam
 * @param {string} phoneNumber - Số điện thoại cần kiểm tra
 * @returns {boolean} Kết quả kiểm tra
 */
function isValidVietnamesePhoneNumber(phoneNumber) {
  // Loại bỏ khoảng trắng, dấu gạch ngang, và dấu ngoặc
  const cleaned = phoneNumber.replace(/[\s\-()]/g, '');
  
  // Định dạng số điện thoại Việt Nam (10 hoặc 11 số)
  // - Bắt đầu bằng 0, sau đó là 3/5/7/8/9
  // - Hoặc bắt đầu bằng +84, sau đó là 3/5/7/8/9
  const regex = /^(0|\+84)([3-9][0-9]{8,9})$/;
  
  return regex.test(cleaned);
}

/**
 * Trích xuất số điện thoại từ văn bản
 * @param {string} text - Văn bản chứa số điện thoại
 * @returns {string|null} Số điện thoại đã trích xuất hoặc null nếu không tìm thấy
 */
function extractPhoneNumber(text) {
  // Tìm số điện thoại trong văn bản
  const phoneRegex = /0[3-9][0-9]{8,9}|(\+84|84)[3-9][0-9]{8,9}/g;
  const matches = text.match(phoneRegex);
  
  if (matches && matches.length > 0) {
    // Trả về số điện thoại đầu tiên tìm thấy
    return matches[0];
  }
  
  return null;
}

/**
 * Phân tích phong thủy số điện thoại
 * @param {string} phoneNumber - Số điện thoại cần phân tích
 * @returns {Object} Kết quả phân tích
 */
async function analyzePhoneNumber(phoneNumber) {
  try {
    // Nếu số điện thoại không hợp lệ, trả về lỗi
    if (!isValidVietnamesePhoneNumber(phoneNumber)) {
      return {
        success: false,
        error: 'Số điện thoại không hợp lệ. Vui lòng nhập số điện thoại Việt Nam (10-11 số, bắt đầu bằng 0).'
      };
    }
    
    // Định dạng chuẩn hóa số điện thoại
    const cleanedPhone = phoneNumber.replace(/[\s\-()]/g, '');
    
    // Gửi yêu cầu đến ADK
    const response = await adkClient.query({
      messages: [
        {
          role: 'user',
          content: `Phân tích phong thủy số điện thoại ${cleanedPhone} theo học thuyết Bát Cục Linh Số. Hãy đánh giá số này về:
1. Quẻ chủ đạo
2. Ngũ hành
3. Sự cân bằng âm dương
4. Điểm mạnh
5. Điểm yếu
6. Đánh giá tổng thể (tốt/trung bình/không tốt)
7. Mức độ phù hợp với các mục đích: kinh doanh, sự nghiệp, tình duyên, tài chính

Hãy phân tích chi tiết, cụ thể và chính xác. Định dạng đẹp, dễ đọc.`
        }
      ]
    });
    
    // Xử lý kết quả từ ADK
    if (response && response.candidates && response.candidates.length > 0) {
      const content = response.candidates[0].content;
      
      return {
        success: true,
        phoneNumber: cleanedPhone,
        content: content,
        id: generateUniqueId()
      };
    } else {
      throw new Error('Không nhận được phản hồi hợp lệ từ dịch vụ phân tích');
    }
  } catch (error) {
    console.error('❌ Lỗi phân tích số điện thoại:', error);
    return {
      success: false,
      error: error.message || 'Đã xảy ra lỗi khi phân tích số điện thoại. Vui lòng thử lại sau.'
    };
  }
}

/**
 * Xử lý yêu cầu phân tích số điện thoại
 * @param {string} message - Tin nhắn chứa yêu cầu phân tích
 * @param {Object} context - Ngữ cảnh của yêu cầu
 * @returns {Object} Kết quả phân tích
 */
async function process(message, context = {}) {
  try {
    // Trích xuất số điện thoại từ tin nhắn
    const phoneNumber = extractPhoneNumber(message) || message.match(/\d{10,11}/)?.[0];
    
    if (!phoneNumber) {
      return {
        success: false,
        content: 'Xin lỗi, tôi không tìm thấy số điện thoại trong yêu cầu của bạn. Vui lòng cung cấp một số điện thoại Việt Nam hợp lệ (10-11 số, bắt đầu bằng 0).'
      };
    }
    
    // Kiểm tra xem người dùng có đủ lượt phân tích không (nếu có thông tin người dùng)
    if (context.userId) {
      const user = await User.findById(context.userId);
      
      if (user && !user.hasRemainingQuestions()) {
        return {
          success: false,
          content: 'Bạn đã hết lượt phân tích. Vui lòng nâng cấp gói dịch vụ để tiếp tục sử dụng.'
        };
      }
      
      // Giảm số lượt phân tích nếu người dùng tồn tại
      if (user) {
        user.decrementRemainingQuestions();
        await user.save();
      }
    }
    
    // Phân tích số điện thoại
    const result = await analyzePhoneNumber(phoneNumber);
    
    if (!result.success) {
      return {
        success: false,
        content: result.error
      };
    }
    
    return {
      success: true,
      content: result.content,
      phoneNumber: result.phoneNumber,
      id: result.id
    };
  } catch (error) {
    console.error('❌ Lỗi xử lý yêu cầu phân tích số điện thoại:', error);
    return {
      success: false,
      content: 'Đã xảy ra lỗi khi xử lý yêu cầu. Vui lòng thử lại sau.'
    };
  }
}

module.exports = {
  process,
  analyzePhoneNumber,
  isValidVietnamesePhoneNumber,
  extractPhoneNumber
}; 