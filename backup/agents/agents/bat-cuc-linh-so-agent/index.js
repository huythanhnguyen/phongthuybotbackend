// agents/bat-cuc-linh-so-agent/index.js - Expert Agent phân tích phong thủy số

const { Task, Message, Artifact } = require('../../services/a2a-protocol');
const { generateUniqueId } = require('../../utils/id-generator');
const batCucLinhSoService = require('./services/bat-cuc-linh-so-service');
const phoneAnalysisTool = require('./tools/phone-analysis-tool');
const cccdAnalysisTool = require('./tools/cccd-analysis-tool');
const bankAccountTool = require('./tools/bank-account-tool');
const passwordTool = require('./tools/password-tool');

class BatCucLinhSoAgent {
  constructor() {
    this.tools = {
      phoneAnalysis: phoneAnalysisTool,
      cccdAnalysis: cccdAnalysisTool,
      bankAccountAnalysis: bankAccountTool,
      passwordAnalysis: passwordTool
    };

    this.state = {
      sessions: {}
    };
  }

  /**
   * Xác định công cụ phù hợp dựa trên nội dung tin nhắn
   * @param {string} message - Nội dung tin nhắn
   * @returns {string} Tên công cụ phù hợp
   */
  determineTool(message) {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('số điện thoại') || 
        lowerMessage.includes('số đt') || 
        lowerMessage.includes('sđt') ||
        lowerMessage.match(/\d{10,11}/)) { // Kiểm tra có số điện thoại không
      return 'phoneAnalysis';
    }
    
    if (lowerMessage.includes('cccd') || 
        lowerMessage.includes('căn cước') || 
        lowerMessage.includes('cmnd') ||
        lowerMessage.match(/\d{9,12}/)) { // Kiểm tra có số CCCD/CMND không
      return 'cccdAnalysis';
    }
    
    if (lowerMessage.includes('tài khoản ngân hàng') || 
        lowerMessage.includes('số tài khoản') || 
        lowerMessage.includes('stk') ||
        lowerMessage.includes('thẻ ngân hàng')) {
      return 'bankAccountAnalysis';
    }
    
    if (lowerMessage.includes('mật khẩu') || 
        lowerMessage.includes('password') || 
        lowerMessage.includes('pass')) {
      return 'passwordAnalysis';
    }
    
    // Mặc định sử dụng phân tích số điện thoại
    return 'phoneAnalysis';
  }

  /**
   * Xử lý task từ Root Agent
   * @param {Task} task - Task A2A
   * @param {Message} message - Tin nhắn từ người dùng
   * @param {Object} context - Ngữ cảnh của yêu cầu
   * @returns {Object} Kết quả xử lý
   */
  async processTask(task, message, context = {}) {
    console.log(`🔍 BatCucLinhSo đang xử lý yêu cầu: ${message.parts[0].text}`);
    
    try {
      // Lưu session nếu chưa có
      if (!this.state.sessions[task.sessionId]) {
        this.state.sessions[task.sessionId] = {
          userId: context.userId,
          history: [],
          createdAt: new Date()
        };
      }
      
      // Thêm tin nhắn vào lịch sử
      this.state.sessions[task.sessionId].history.push({
        type: 'request',
        content: message.parts[0].text,
        timestamp: new Date()
      });
      
      // Xác định công cụ phù hợp
      const toolName = this.determineTool(message.parts[0].text);
      
      // Xử lý yêu cầu bằng công cụ tương ứng
      const result = await this.tools[toolName].process(message.parts[0].text, context);
      
      // Tạo artifacts từ kết quả
      const artifact = new Artifact({
        type: 'response',
        parts: [{ type: 'text', text: result.content }]
      });
      
      // Thêm phản hồi vào lịch sử
      this.state.sessions[task.sessionId].history.push({
        type: 'response',
        content: result.content,
        timestamp: new Date(),
        toolUsed: toolName
      });
      
      // Cập nhật trạng thái task
      task.updateStatus('completed');
      task.addArtifact(artifact);
      
      return {
        taskId: task.id,
        status: task.status,
        artifacts: task.artifacts
      };
    } catch (error) {
      console.error('❌ Lỗi xử lý BatCucLinhSo:', error);
      
      // Tạo artifact lỗi
      const errorArtifact = new Artifact({
        type: 'error',
        parts: [{ 
          type: 'text', 
          text: `Rất tiếc, đã xảy ra lỗi khi phân tích: ${error.message}. Vui lòng thử lại với nội dung khác.` 
        }]
      });
      
      // Cập nhật trạng thái task
      task.updateStatus('error', { error: error.message });
      task.addArtifact(errorArtifact);
      
      return {
        taskId: task.id,
        status: task.status,
        artifacts: task.artifacts
      };
    }
  }

  /**
   * Lấy lịch sử phân tích của người dùng
   * @param {string} userId - ID của người dùng
   * @returns {Array} Lịch sử phân tích
   */
  getUserHistory(userId) {
    const userSessions = Object.values(this.state.sessions)
      .filter(session => session.userId === userId)
      .sort((a, b) => b.createdAt - a.createdAt);
    
    const history = [];
    
    userSessions.forEach(session => {
      session.history.forEach(item => {
        if (item.type === 'response' && item.toolUsed) {
          history.push({
            content: item.content,
            timestamp: item.timestamp,
            toolUsed: item.toolUsed
          });
        }
      });
    });
    
    return history;
  }
}

module.exports = new BatCucLinhSoAgent(); 