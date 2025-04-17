// agents/bat-cuc-linh-so-agent/tools/cccd-analysis-tool.js - Công cụ phân tích số CCCD

const { ADKClient } = require('@adk/node-client');
const { generateUniqueId } = require('../../../utils/id-generator');
const User = require('../../../models/user.model');

// Cấu hình ADK Client
const adkClient = new ADKClient({
  apiKey: process.env.ADK_API_KEY,
  baseUrl: process.env.ADK_BASE_URL || 'https://api.adk.io'
});

/**
 * Kiểm tra định dạng số căn cước công dân Việt Nam
 * @param {string} cccd - Số CCCD cần kiểm tra
 * @returns {boolean} Kết quả kiểm tra
 */
function isValidCCCD(cccd) {
  // Loại bỏ khoảng trắng
  const cleaned = cccd.replace(/\s/g, '');
  
  // CCCD mới có 12 số
  // CMND cũ có 9 số
  return /^\d{9}$|^\d{12}$/.test(cleaned);
}

/**
 * Trích xuất số CCCD từ văn bản
 * @param {string} text - Văn bản chứa số CCCD
 * @returns {string|null} Số CCCD đã trích xuất hoặc null nếu không tìm thấy
 */
function extractCCCD(text) {
  // Tìm số CCCD trong văn bản
  const cccdRegex = /\b\d{9}\b|\b\d{12}\b/g;
  const matches = text.match(cccdRegex);
  
  if (matches && matches.length > 0) {
    // Trả về số CCCD đầu tiên tìm thấy
    return matches[0];
  }
  
  return null;
}

/**
 * Phân tích phong thủy số CCCD
 * @param {string} cccd - Số CCCD cần phân tích
 * @returns {Object} Kết quả phân tích
 */
async function analyzeCCCD(cccd) {
  try {
    // Nếu số CCCD không hợp lệ, trả về lỗi
    if (!isValidCCCD(cccd)) {
      return {
        success: false,
        error: 'Số CCCD/CMND không hợp lệ. Vui lòng nhập số CMND (9 số) hoặc CCCD (12 số).'
      };
    }
    
    // Định dạng chuẩn hóa số CCCD
    const cleanedCCCD = cccd.replace(/\s/g, '');
    
    // Gửi yêu cầu đến ADK
    const response = await adkClient.query({
      messages: [
        {
          role: 'user',
          content: `Phân tích phong thủy số căn cước công dân/CMND ${cleanedCCCD} theo học thuyết Bát Cục Linh Số. Hãy đánh giá về:
1. Ý nghĩa các số cấu thành
2. Ngũ hành
3. Sự cân bằng âm dương
4. Điểm mạnh
5. Điểm yếu
6. Đánh giá tổng thể (tốt/trung bình/không tốt)
7. Những lưu ý đặc biệt

Hãy phân tích chi tiết, cụ thể và chính xác. Định dạng đẹp, dễ đọc.`
        }
      ]
    });
    
    // Xử lý kết quả từ ADK
    if (response && response.candidates && response.candidates.length > 0) {
      const content = response.candidates[0].content;
      
      return {
        success: true,
        cccd: cleanedCCCD,
        content: content,
        id: generateUniqueId()
      };
    } else {
      throw new Error('Không nhận được phản hồi hợp lệ từ dịch vụ phân tích');
    }
  } catch (error) {
    console.error('❌ Lỗi phân tích số CCCD:', error);
    return {
      success: false,
      error: error.message || 'Đã xảy ra lỗi khi phân tích số CCCD. Vui lòng thử lại sau.'
    };
  }
}

/**
 * Xử lý yêu cầu phân tích số CCCD
 * @param {string} message - Tin nhắn chứa yêu cầu phân tích
 * @param {Object} context - Ngữ cảnh của yêu cầu
 * @returns {Object} Kết quả phân tích
 */
async function process(message, context = {}) {
  try {
    // Trích xuất số CCCD từ tin nhắn
    const cccd = extractCCCD(message) || message.match(/\d{9,12}/)?.[0];
    
    if (!cccd) {
      return {
        success: false,
        content: 'Xin lỗi, tôi không tìm thấy số CCCD/CMND trong yêu cầu của bạn. Vui lòng cung cấp số CMND (9 số) hoặc CCCD (12 số).'
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
    
    // Phân tích số CCCD
    const result = await analyzeCCCD(cccd);
    
    if (!result.success) {
      return {
        success: false,
        content: result.error
      };
    }
    
    return {
      success: true,
      content: result.content,
      cccd: result.cccd,
      id: result.id
    };
  } catch (error) {
    console.error('❌ Lỗi xử lý yêu cầu phân tích số CCCD:', error);
    return {
      success: false,
      content: 'Đã xảy ra lỗi khi xử lý yêu cầu. Vui lòng thử lại sau.'
    };
  }
}

module.exports = {
  process,
  analyzeCCCD,
  isValidCCCD,
  extractCCCD
}; 