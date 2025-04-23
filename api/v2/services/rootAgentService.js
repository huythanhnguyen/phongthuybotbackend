const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Cấu hình kết nối đến Python ADK
const PYTHON_ADK_URL = process.env.PYTHON_ADK_URL || 'http://localhost:10000';
const API_KEY = process.env.ADK_API_KEY || 'dev_key';

// Lưu trữ session
const sessions = {};

/**
 * Service quản lý Root Agent và điều phối tới các agents khác
 */
class RootAgentService {
  /**
   * Khởi tạo dịch vụ Root Agent
   */
  constructor() {
    console.log('🤖 Khởi tạo Root Agent Service');
    this.apiClient = axios.create({
      baseURL: PYTHON_ADK_URL,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
      }
    });
  }

  /**
   * Xử lý tin nhắn từ người dùng
   * @param {Object} params - Tham số xử lý
   * @param {string} params.message - Nội dung tin nhắn
   * @param {string} [params.sessionId] - ID phiên làm việc
   * @param {string} [params.userId] - ID người dùng
   * @param {Object} [params.metadata] - Metadata bổ sung
   * @returns {Promise<Object>} Kết quả xử lý
   */
  async processMessage({ message, sessionId, userId, metadata = {} }) {
    try {
      // Tạo ID phiên nếu chưa có
      if (!sessionId) {
        sessionId = uuidv4();
        console.log(`🆕 Tạo phiên mới: ${sessionId}`);
      }

      // Lưu thông tin phiên nếu chưa có
      if (!sessions[sessionId]) {
        sessions[sessionId] = {
          id: sessionId,
          userId,
          startTime: new Date(),
          history: [],
          metadata: { ...metadata }
        };
      }

      // Cập nhật lịch sử tin nhắn
      sessions[sessionId].history.push({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      });

      // Chuẩn bị request
      const requestBody = {
        message,
        session_id: sessionId,
        user_id: userId,
        metadata
      };

      // Gửi request đến Python ADK
      console.log(`📤 Gửi yêu cầu đến ADK: ${message.substring(0, 50)}...`);
      
      try {
        // Thử gọi API với timeout và retry
        const response = await this.apiClient.post('/chat', requestBody, {
          timeout: 30000, // Tăng timeout lên 30 giây
        });

        // Kiểm tra kết quả
        if (!response.data) {
          throw new Error('Không nhận được dữ liệu từ ADK');
        }

        // Lưu phản hồi vào lịch sử
        const responseContent = response.data.response || response.data.text || 'Không có phản hồi từ hệ thống';
        sessions[sessionId].history.push({
          role: 'assistant',
          content: responseContent,
          timestamp: new Date().toISOString(),
          agentType: response.data.agent_type || 'unknown'
        });

        return {
          sessionId,
          response: responseContent,
          agentType: response.data.agent_type || 'unknown',
          success: response.data.success !== false
        };
      } catch (apiError) {
        console.error('❌ Lỗi khi gọi API ADK:', apiError.message);
        
        // Thử gọi endpoint dự phòng /agent/stream
        if (apiError.code === 'ECONNREFUSED' || apiError.code === 'ENOTFOUND' || 
            apiError.response?.status === 500) {
          console.log('⚠️ Thử kết nối đến endpoint khác: /agent/stream');
          
          try {
            const fallbackResponse = await this.apiClient.post('/agent/stream', {
              text: message,
              sessionId: sessionId,
              userId: userId,
              metadata
            });
            
            if (fallbackResponse.data && (fallbackResponse.data.text || fallbackResponse.data.response)) {
              const responseText = fallbackResponse.data.text || fallbackResponse.data.response;
              
              // Lưu phản hồi vào lịch sử
              sessions[sessionId].history.push({
                role: 'assistant',
                content: responseText,
                timestamp: new Date().toISOString(),
                agentType: 'root' // Mặc định là root agent
              });
              
              return {
                sessionId,
                response: responseText,
                agentType: 'root',
                success: true
              };
            }
          } catch (fallbackError) {
            console.error('❌ Lỗi khi thử kết nối dự phòng:', fallbackError.message);
          }
        }
        
        // Nếu tất cả đều thất bại, dùng phương án dự phòng local
        console.log('⚠️ ADK không khả dụng, sử dụng phương án dự phòng local');
        return this._fallbackProcessing(message, sessionId);
      }
    } catch (error) {
      console.error('❌ Lỗi nghiêm trọng khi xử lý tin nhắn:', error);
      return {
        sessionId,
        response: "Đã xảy ra lỗi khi xử lý tin nhắn của bạn. Vui lòng thử lại sau.",
        agentType: "error",
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Xử lý tin nhắn dạng stream
   * @param {Object} params - Tham số xử lý
   * @param {string} params.message - Nội dung tin nhắn
   * @param {string} [params.sessionId] - ID phiên làm việc
   * @param {string} [params.userId] - ID người dùng
   * @param {Object} [params.metadata] - Metadata bổ sung
   * @param {Function} params.onChunk - Callback khi nhận được chunk dữ liệu
   * @param {Function} params.onComplete - Callback khi hoàn thành
   * @param {Function} params.onError - Callback khi có lỗi
   */
  async processMessageStream({ message, sessionId, userId, metadata = {}, onChunk, onComplete, onError }) {
    try {
      // Tạo ID phiên nếu chưa có
      if (!sessionId) {
        sessionId = uuidv4();
        console.log(`🆕 Tạo phiên mới: ${sessionId}`);
      }

      // Lưu thông tin phiên nếu chưa có
      if (!sessions[sessionId]) {
        sessions[sessionId] = {
          id: sessionId,
          userId,
          startTime: new Date(),
          history: [],
          metadata: { ...metadata }
        };
      }

      // Cập nhật lịch sử tin nhắn
      sessions[sessionId].history.push({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      });

      console.log(`📤 Gửi yêu cầu stream đến ADK: ${message.substring(0, 50)}...`);
      
      let useNonStreamingFallback = false;
      let streamError = null;
      
      // Thử các phương thức khác nhau để lấy phản hồi
      try {
        // Chuẩn bị request có stream
        const requestBody = {
          message,
          session_id: sessionId,
          user_id: userId,
          metadata,
          stream: true
        };
        
        // Gửi request đến Python ADK với stream
        const response = await this.apiClient.post('/chat/stream', requestBody, {
          responseType: 'stream',
          timeout: 30000 // Tăng timeout lên 30 giây
        });

        // Xử lý response dạng stream
        let fullContent = '';
        
        response.data.on('data', (chunk) => {
          const content = chunk.toString('utf8');
          
          // Phân tích dữ liệu theo định dạng SSE
          const lines = content.split('\n\n');
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.substring(6));
                
                if (data.type === 'chunk') {
                  fullContent += data.content;
                  onChunk(data);
                } else if (data.type === 'error') {
                  streamError = new Error(data.error || 'Unknown streaming error');
                  console.error('Stream error:', data.error);
                }
              } catch (e) {
                console.error('Lỗi khi xử lý chunk:', e);
              }
            }
          }
        });
        
        response.data.on('end', () => {
          // Kiểm tra nếu có lỗi hoặc không có nội dung
          if (streamError || !fullContent) {
            useNonStreamingFallback = true;
            return;
          }
          
          // Lưu phản hồi vào lịch sử
          sessions[sessionId].history.push({
            role: 'assistant',
            content: fullContent,
            timestamp: new Date().toISOString()
          });
          
          onComplete();
        });
        
        response.data.on('error', (err) => {
          console.error('Lỗi stream:', err);
          streamError = err;
          useNonStreamingFallback = true;
        });
        
        // Đợi một chút để xem có lỗi không
        await new Promise(resolve => setTimeout(resolve, 5000));
        
        // Nếu cần dùng fallback, thì break ra
        if (useNonStreamingFallback) {
          throw new Error('Stream không thành công, chuyển sang phương án dự phòng');
        }
        
      } catch (streamErr) {
        console.error('❌ Lỗi khi xử lý stream, thử phương án không stream:', streamErr.message);
        
        try {
          // Thử phương án không stream - gọi đến /agent/stream bình thường
          const fallbackResponse = await this.apiClient.post('/agent/stream', {
            text: message,
            sessionId,
            userId,
          }, { timeout: 30000 });
          
          if (fallbackResponse.data && fallbackResponse.data.text) {
            const responseText = fallbackResponse.data.text;
            
            // Giả lập stream bằng cách chia nhỏ phản hồi
            const chunks = this._splitTextIntoChunks(responseText);
            
            for (const chunk of chunks) {
              onChunk({
                type: 'chunk',
                content: chunk
              });
              
              // Tạm dừng một chút để giả lập stream
              await new Promise(resolve => setTimeout(resolve, 50));
            }
            
            // Lưu phản hồi vào lịch sử
            sessions[sessionId].history.push({
              role: 'assistant',
              content: responseText,
              timestamp: new Date().toISOString()
            });
            
            onComplete();
            return;
          } else {
            throw new Error('Không có dữ liệu từ fallback endpoint');
          }
        } catch (fallbackErr) {
          console.error('❌ Lỗi khi gọi fallback endpoint:', fallbackErr.message);
          
          // Cuối cùng thử phương án dự phòng local
          try {
            const result = await this._fallbackProcessing(message, sessionId);
            
            // Giả lập stream bằng cách chia nhỏ phản hồi
            const chunks = this._splitTextIntoChunks(result.response);
            
            for (const chunk of chunks) {
              onChunk({
                type: 'chunk',
                content: chunk
              });
              
              // Tạm dừng một chút để giả lập stream
              await new Promise(resolve => setTimeout(resolve, 50));
            }
            
            onComplete();
            return;
          } catch (localErr) {
            onError(new Error('Tất cả các phương án đều thất bại: ' + localErr.message));
          }
        }
      }
    } catch (error) {
      console.error('❌ Lỗi khi xử lý tin nhắn stream:', error);
      onError(error);
    }
  }

  /**
   * Gửi truy vấn trực tiếp đến một agent cụ thể
   * @param {Object} params - Tham số truy vấn
   * @param {string} params.agentType - Loại agent
   * @param {string} params.query - Nội dung truy vấn
   * @param {string} [params.sessionId] - ID phiên làm việc
   * @param {string} [params.userId] - ID người dùng
   * @param {Object} [params.metadata] - Metadata bổ sung
   * @returns {Promise<Object>} Kết quả truy vấn
   */
  async queryAgent({ agentType, query, sessionId, userId, metadata = {} }) {
    try {
      // Tạo ID phiên nếu chưa có
      if (!sessionId) {
        sessionId = uuidv4();
        console.log(`🆕 Tạo phiên mới cho truy vấn trực tiếp: ${sessionId}`);
      }

      // Chuẩn bị request
      const requestBody = {
        query,
        agent_type: agentType,
        session_id: sessionId,
        user_id: userId,
        metadata
      };

      // Gửi request đến Python ADK
      console.log(`📤 Gửi truy vấn trực tiếp đến agent ${agentType}: ${query.substring(0, 50)}...`);
      const response = await this.apiClient.post('/query', requestBody);

      // Kiểm tra kết quả
      if (!response.data || response.status !== 200) {
        throw new Error(`Không nhận được phản hồi từ agent ${agentType}`);
      }

      return {
        sessionId,
        response: response.data.response,
        agentType,
        success: response.data.success || true,
        data: response.data.data || {}
      };
    } catch (error) {
      console.error(`❌ Lỗi khi truy vấn agent ${agentType}:`, error);
      
      // Nếu API chưa chạy, sử dụng phương án dự phòng
      if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
        console.log('⚠️ ADK không khả dụng, sử dụng phương án dự phòng cho truy vấn trực tiếp');
        
        if (agentType === 'batcuclinh_so') {
          return {
            sessionId,
            response: `Đây là phản hồi dự phòng cho truy vấn "${query}" đến agent Bát Cục Linh Số. Python ADK chưa sẵn sàng.`,
            agentType,
            success: true
          };
        }
        
        return {
          sessionId,
          response: `Không thể kết nối đến agent ${agentType}. Python ADK chưa sẵn sàng.`,
          agentType,
          success: false
        };
      }
      
      throw error;
    }
  }

  /**
   * Xử lý dự phòng khi không thể kết nối tới Python ADK
   * @private
   * @param {string} message - Nội dung tin nhắn
   * @param {string} sessionId - ID phiên làm việc
   * @returns {Object} Kết quả xử lý dự phòng
   */
  _fallbackProcessing(message, sessionId) {
    console.log('🔄 Sử dụng xử lý dự phòng cho tin nhắn:', message.substring(0, 50));
    
    let response = '';
    let agentType = 'unknown';
    
    // Kiểm tra các từ khóa để xác định loại tin nhắn
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('số điện thoại') || 
        lowerMessage.includes('sđt') || 
        lowerMessage.match(/\d{10,11}/)) {
      // Phân tích số điện thoại
      response = 'Phân tích số điện thoại sẽ được thực hiện khi Python ADK sẵn sàng. Hiện tại dịch vụ này đang được khởi động.';
      agentType = 'batcuclinh_so';
    } else if (lowerMessage.includes('cccd') || 
              lowerMessage.includes('căn cước') || 
              lowerMessage.includes('cmnd') || 
              lowerMessage.match(/\d{9,12}/)) {
      // Phân tích CCCD
      response = 'Phân tích CCCD/CMND sẽ được thực hiện khi Python ADK sẵn sàng. Hiện tại dịch vụ này đang được khởi động.';
      agentType = 'batcuclinh_so';
    } else {
      // Mặc định
      response = 'Xin chào! Tôi là Phong Thủy Số Bot. Hiện tại dịch vụ phân tích đang được khởi động. Vui lòng thử lại sau ít phút, hoặc kiểm tra xem Python ADK đã được khởi động chưa.';
    }
    
    // Lưu phản hồi vào lịch sử nếu có session
    if (sessions[sessionId]) {
      sessions[sessionId].history.push({
        role: 'assistant',
        content: response,
        timestamp: new Date().toISOString(),
        agentType
      });
    }
    
    return {
      sessionId,
      response,
      agentType,
      success: true
    };
  }

  /**
   * Chia văn bản thành các chunks nhỏ hơn để giả lập stream
   * @private
   * @param {string} text - Văn bản cần chia
   * @param {number} [chunkSize=4] - Kích thước mỗi chunk (số từ)
   * @returns {string[]} Mảng các chunk
   */
  _splitTextIntoChunks(text, chunkSize = 4) {
    const words = text.split(' ');
    const chunks = [];
    
    for (let i = 0; i < words.length; i += chunkSize) {
      chunks.push(words.slice(i, i + chunkSize).join(' '));
    }
    
    return chunks;
  }
}

module.exports = new RootAgentService(); 