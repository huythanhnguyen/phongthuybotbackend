// agents/root-agent/index.js - Root Agent điều phối yêu cầu đến các agent chuyên biệt

const { Task, Message, Artifact } = require('../../services/a2a-protocol');
const { generateUniqueId, generateSessionId } = require('../../utils/id-generator');

class RootAgent {
  constructor() {
    this.expertAgents = {};
    this.state = {
      sessions: {}
    };
  }

  /**
   * Đăng ký Expert Agent với Root Agent
   * @param {string} agentName - Tên của Expert Agent
   * @param {Object} agent - Instance của Expert Agent
   */
  registerExpertAgent(agentName, agent) {
    this.expertAgents[agentName] = agent;
    console.log(`🔗 Đã kết nối Root Agent với ${agentName} Agent`);
  }

  /**
   * Phân tích yêu cầu để xác định Expert Agent phù hợp
   * @param {string} request - Yêu cầu từ người dùng
   * @returns {string} Tên của Expert Agent
   */
  analyzeRequest(request) {
    const lowerRequest = request.toLowerCase();
    
    // Kiểm tra yêu cầu phân tích số điện thoại, CCCD, tài khoản ngân hàng, mật khẩu
    if (lowerRequest.includes('số điện thoại') || 
        lowerRequest.includes('số đt') ||
        lowerRequest.includes('sđt') ||
        lowerRequest.includes('cccd') || 
        lowerRequest.includes('căn cước') ||
        lowerRequest.includes('tài khoản ngân hàng') ||
        lowerRequest.includes('mật khẩu')) {
      return 'batCucLinhSo';
    }
    
    // Mặc định sử dụng BatCucLinhSo Agent (vì hiện tại chỉ có một Expert Agent)
    return 'batCucLinhSo';
  }

  /**
   * Xử lý yêu cầu từ người dùng
   * @param {string} request - Yêu cầu từ người dùng
   * @param {Object} context - Ngữ cảnh của yêu cầu
   * @returns {Object} Kết quả xử lý
   */
  async processRequest(request, context = {}) {
    // Tạo Task theo A2A Protocol
    const task = new Task({
      id: generateUniqueId(),
      sessionId: context.sessionId || generateSessionId(),
      status: { state: 'submitted' }
    });
    
    // Tạo Message từ yêu cầu người dùng
    const message = new Message({
      role: 'user',
      parts: [{ type: 'text', text: request }]
    });
    
    // Lưu context vào session
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
      content: request,
      timestamp: new Date()
    });
    
    // Phân tích yêu cầu để xác định Expert Agent phù hợp
    const targetAgent = this.analyzeRequest(request);
    
    // Kiểm tra xem Expert Agent có tồn tại không
    if (!this.expertAgents[targetAgent]) {
      return this.handleError('Agent không khả dụng', task);
    }
    
    try {
      // Chuyển Task đến Expert Agent
      console.log(`🔄 Root Agent chuyển yêu cầu đến ${targetAgent} Agent`);
      const result = await this.expertAgents[targetAgent].processTask(task, message, context);
      
      // Cập nhật trạng thái Task
      task.status = { state: 'completed' };
      task.artifacts = result.artifacts || [];
      
      // Thêm phản hồi vào lịch sử
      this.state.sessions[task.sessionId].history.push({
        type: 'response',
        content: result,
        timestamp: new Date()
      });
      
      return this.formatResponse(task);
    } catch (error) {
      console.error('Lỗi xử lý yêu cầu:', error);
      return this.handleError(error.message, task);
    }
  }

  /**
   * Xử lý yêu cầu với streaming response
   * @param {string} request - Yêu cầu từ người dùng
   * @param {Object} context - Ngữ cảnh của yêu cầu
   * @returns {EventEmitter} Stream events với dữ liệu phản hồi
   */
  processRequestStream(request, context = {}) {
    const EventEmitter = require('events');
    const stream = new EventEmitter();
    
    // Xử lý yêu cầu bất đồng bộ
    this.processRequest(request, context)
      .then(result => {
        // Giả lập streaming bằng cách chia nhỏ phản hồi
        if (result.results && result.results.length > 0) {
          const text = result.results[0].content;
          const chunks = this.splitTextIntoChunks(text, 20);
          
          let index = 0;
          const interval = setInterval(() => {
            if (index < chunks.length) {
              stream.emit('data', {
                type: 'chunk',
                content: chunks[index],
                index: index,
                total: chunks.length
              });
              index++;
            } else {
              clearInterval(interval);
              stream.emit('data', {
                type: 'complete',
                taskId: result.taskId,
                sessionId: result.sessionId
              });
              stream.emit('end');
            }
          }, 100);
        } else {
          stream.emit('data', result);
          stream.emit('end');
        }
      })
      .catch(error => {
        stream.emit('data', { error: error.message });
        stream.emit('end');
      });
    
    // Thêm phương thức để hủy stream
    stream.cancel = () => {
      stream.removeAllListeners();
    };
    
    return stream;
  }

  /**
   * Chia văn bản thành các đoạn nhỏ
   * @param {string} text - Văn bản cần chia
   * @param {number} size - Số từ mỗi đoạn
   * @returns {Array} Mảng các đoạn văn bản
   */
  splitTextIntoChunks(text, size = 20) {
    const words = text.split(' ');
    const chunks = [];
    
    for (let i = 0; i < words.length; i += size) {
      chunks.push(words.slice(i, i + size).join(' '));
    }
    
    return chunks;
  }

  /**
   * Định dạng phản hồi từ Task
   * @param {Task} task - Task A2A
   * @returns {Object} Phản hồi đã định dạng
   */
  formatResponse(task) {
    return {
      success: true,
      taskId: task.id,
      sessionId: task.sessionId,
      status: task.status.state,
      results: task.artifacts.map(artifact => ({
        type: artifact.parts[0].type,
        content: artifact.parts[0].type === 'text' 
          ? artifact.parts[0].text 
          : artifact.parts[0]
      }))
    };
  }

  /**
   * Xử lý lỗi và trả về phản hồi lỗi
   * @param {string} errorMessage - Thông báo lỗi
   * @param {Task} task - Task A2A
   * @returns {Object} Phản hồi lỗi
   */
  handleError(errorMessage, task) {
    task.status = { state: 'error' };
    task.artifacts = [
      new Artifact({
        parts: [{ 
          type: 'text', 
          text: `Rất tiếc, đã xảy ra lỗi: ${errorMessage}. Vui lòng thử lại sau.` 
        }]
      })
    ];
    
    return this.formatResponse(task);
  }
}

module.exports = new RootAgent(); 