# Phong Thủy Số - Tích hợp Full Stack (Frontend + Backend)

## 1. Tổng quan hệ thống

Phong Thủy Số là một ứng dụng full stack gồm hai phần chính:

1. **Frontend**: Ứng dụng Vue.js với giao diện người dùng hiện đại
2. **Backend**: API sử dụng kiến trúc Agent dựa trên Node.js (API) và Python (AI/ML)

Tài liệu này mô tả cách tích hợp hai thành phần này để tạo ra một hệ thống hoàn chỉnh.

## 2. Cấu trúc thư mục

```
/phong-thuy-so/
├── /frontend/                              # Frontend Vue.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── /public/                            # Tài nguyên tĩnh
│   └── /src/
│       ├── App.vue                         # Component gốc
│       ├── main.js                         # Entry point
│       ├── /assets/                        # CSS, hình ảnh
│       ├── /components/                    # Các component
│       │   ├── /analysis/                  # Component phân tích
│       │   ├── /auth/                      # Component xác thực
│       │   ├── /chat/                      # Component chatbot
│       │   └── /layout/                    # Component layout
│       ├── /router/                        # Vue Router
│       ├── /services/                      # Các service gọi API
│       │   ├── api.js                      # Cấu hình axios
│       │   ├── analysisService.js          # Dịch vụ phân tích
│       │   └── authService.js              # Dịch vụ xác thực
│       ├── /stores/                        # Pinia stores
│       │   ├── analysis.js
│       │   ├── auth.js
│       │   └── chat.js
│       └── /views/                         # Các trang
│           ├── AppView.vue                 # Trang ứng dụng chính
│           ├── HomeView.vue                # Trang chủ
│           ├── LoginView.vue               # Trang đăng nhập
│           └── /guides/                    # Trang hướng dẫn
│
├── /backend/                               # Backend API
│   ├── app.js                              # Entry point
│   ├── server.js                           # Server startup
│   ├── package.json
│   ├── /agents/                            # Thư mục chứa các agent
│   │   ├── /root-agent/                    # Root Agent
│   │   ├── /bat-cuc-linh-so/               # Agent phân tích số
│   │   ├── /payment/                       # Agent thanh toán
│   │   ├── /user/                          # Agent người dùng
│   │   └── /chatbot/                       # Agent chatbot
│   ├── /api/                               # API endpoints
│   │   ├── /v1/                            # API cũ
│   │   └── /v2/                            # API mới (agent-based)
│   ├── /models/                            # MongoDB models
│   ├── /services/                          # Các dịch vụ chung
│   ├── /tools/                             # Công cụ dùng chung
│   ├── /utils/                             # Tiện ích
│   ├── /config/                            # Cấu hình
│   ├── /python/                            # Mã Python
│   │   ├── /bat_cuc_linh_so/
│   │   └── /chatbot/
│   ├── /docs/                              # Tài liệu API
│   └── /tests/                             # Kiểm thử
└── /deployment/                            # Cấu hình triển khai
    ├── docker-compose.yml
    ├── Dockerfile.frontend
    ├── Dockerfile.backend
    └── /nginx/                             # Cấu hình Nginx
```

## 3. Tích hợp Frontend-Backend

### 3.1 Điểm kết nối

Frontend và Backend tương tác qua API RESTful với các endpoint chính sau:

#### API v1 (Tương thích ngược)
- `/api/auth/*`: Xác thực người dùng
- `/api/analysis/*`: Phân tích số điện thoại
- `/api/payments/*`: Thanh toán
- `/api/users/*`: Quản lý người dùng

#### API v2 (Kiến trúc Agent)
- `/api/v2/agent/root`: Điểm vào cho Root Agent
- `/api/v2/agent/bat-cuc-linh-so`: API cho BatCucLinhSo Agent
- `/api/v2/agent/payment`: API cho Payment Agent
- `/api/v2/agent/user`: API cho User Agent
- `/api/v2/agent/chatbot`: API cho Chatbot Agent
- `/api/v2/gateway`: API Gateway để điều hướng yêu cầu

### 3.2 Chiến lược di chuyển

1. **Giai đoạn 1**: Di chuyển từng phần backend sang kiến trúc Agent
   - Giữ nguyên API v1 cho frontend hiện tại
   - Triển khai API v2 song song
   - Chuyển hướng nội bộ từ v1 sang v2

2. **Giai đoạn 2**: Cập nhật frontend để sử dụng API v2
   - Cập nhật các service trong `src/services/`
   - Cập nhật các store để làm việc với kiến trúc mới
   - Bổ sung các component mới cho tính năng mới

3. **Giai đoạn 3**: Hoàn thiện tích hợp
   - Xóa các endpoint cũ
   - Tối ưu hóa giao tiếp

## 4. Chi tiết kết nối Frontend-Backend

### 4.1 API Service (Frontend)

```javascript
// frontend/src/services/api.js
import axios from 'axios'

// Cấu hình chung
const API_VERSION = 'v2'  // Có thể chuyển đổi giữa v1 và v2
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://api.phongthuyso.vn/api'
  : 'http://localhost:3000/api'

// Tạo gateway service để giao tiếp với API Gateway
export const gatewayService = axios.create({
  baseURL: `${API_BASE_URL}/${API_VERSION}/gateway`,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Tạo các agent service riêng biệt
export const rootAgentService = axios.create({
  baseURL: `${API_BASE_URL}/${API_VERSION}/agent/root`,
  timeout: 15000
})

export const batCucLinhSoService = axios.create({
  baseURL: `${API_BASE_URL}/${API_VERSION}/agent/bat-cuc-linh-so`,
  timeout: 20000
})

export const paymentService = axios.create({
  baseURL: `${API_BASE_URL}/${API_VERSION}/agent/payment`,
  timeout: 15000
})

export const userService = axios.create({
  baseURL: `${API_BASE_URL}/${API_VERSION}/agent/user`,
  timeout: 15000
})

export const chatbotService = axios.create({
  baseURL: `${API_BASE_URL}/${API_VERSION}/agent/chatbot`,
  timeout: 30000
})

// Token interceptor chung
const addAuthInterceptor = (serviceInstance) => {
  serviceInstance.interceptors.request.use(
    config => {
      const token = localStorage.getItem('phone_analysis_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    error => Promise.reject(error)
  )
}

// Thêm interceptor vào tất cả các service
[gatewayService, rootAgentService, batCucLinhSoService,
 paymentService, userService, chatbotService].forEach(addAuthInterceptor)
```

### 4.2 Agent Gateway (Backend)

```javascript
// backend/api/v2/gateway.js
const express = require('express')
const router = express.Router()
const rootAgent = require('../../agents/root-agent')

// API Gateway nhận tất cả các yêu cầu và phân phối tới các agent
router.post('/request', async (req, res) => {
  try {
    const { request, context } = req.body
    
    // Gửi yêu cầu đến Root Agent để phân tích và điều hướng
    const result = await rootAgent.processRequest(request, {
      ...context,
      userId: req.user?.id
    })
    
    // Trả về kết quả
    res.json(result)
  } catch (error) {
    res.status(500).json({
      success: false,
      message: error.message || 'Lỗi server'
    })
  }
})

// Streaming API để hỗ trợ SSE (Server-Sent Events)
router.post('/stream', (req, res) => {
  // Cấu hình SSE
  res.setHeader('Content-Type', 'text/event-stream')
  res.setHeader('Cache-Control', 'no-cache')
  res.setHeader('Connection', 'keep-alive')
  
  // Xử lý yêu cầu streaming
  const { request, context } = req.body
  const stream = rootAgent.processRequestStream(request, {
    ...context,
    userId: req.user?.id
  })
  
  // Gửi dữ liệu khi có cập nhật
  stream.on('data', (data) => {
    res.write(`data: ${JSON.stringify(data)}\n\n`)
  })
  
  // Đóng kết nối khi hoàn thành
  stream.on('end', () => {
    res.write('data: {"event": "end"}\n\n')
    res.end()
  })
  
  // Xử lý khi client ngắt kết nối
  req.on('close', () => {
    stream.cancel()
  })
})

module.exports = router
```

### 4.3 Frontend Store cho Agent (Pinia)

```javascript
// frontend/src/stores/agent.js
import { defineStore } from 'pinia'
import { gatewayService } from '../services/api'

export const useAgentStore = defineStore('agent', {
  state: () => ({
    activeAgent: 'root',
    conversations: {},
    isProcessing: false,
    currentResult: null,
    error: null
  }),
  
  actions: {
    // Gửi yêu cầu đến Agent Gateway
    async sendRequest(request, context = {}) {
      this.isProcessing = true
      this.error = null
      
      try {
        const response = await gatewayService.post('/request', {
          request,
          context: {
            ...context,
            agent: this.activeAgent
          }
        })
        
        this.currentResult = response.data
        
        // Lưu vào lịch sử hội thoại
        if (!this.conversations[this.activeAgent]) {
          this.conversations[this.activeAgent] = []
        }
        
        this.conversations[this.activeAgent].push({
          type: 'request',
          content: request,
          timestamp: new Date()
        })
        
        this.conversations[this.activeAgent].push({
          type: 'response',
          content: response.data,
          timestamp: new Date()
        })
        
        return response.data
      } catch (error) {
        this.error = error.message || 'Lỗi không xác định'
        throw error
      } finally {
        this.isProcessing = false
      }
    },
    
    // Thiết lập agent hiện tại
    setActiveAgent(agentName) {
      this.activeAgent = agentName
    },
    
    // Xóa lịch sử hội thoại
    clearConversation(agentName = null) {
      if (agentName) {
        this.conversations[agentName] = []
      } else {
        this.conversations[this.activeAgent] = []
      }
    }
  }
})
```

## 5. Tương tác giữa các Agent

### 5.1 Mô hình tương tác A2A trong Backend

```javascript
// backend/agents/root-agent/index.js
const { Task, Message, Artifact } = require('../../services/a2a-protocol')
const batCucLinhSoAgent = require('../bat-cuc-linh-so')
const paymentAgent = require('../payment')
const userAgent = require('../user')
const chatbotAgent = require('../chatbot')

class RootAgent {
  async processRequest(request, context) {
    // Tạo Task theo A2A Protocol
    const task = new Task({
      id: generateUniqueId(),
      sessionId: context.sessionId || generateSessionId(),
      status: { state: 'submitted' }
    })
    
    // Tạo Message từ yêu cầu người dùng
    const message = new Message({
      role: 'user',
      parts: [{ type: 'text', text: request }]
    })
    
    // Phân tích yêu cầu để xác định Agent phù hợp
    const targetAgent = this.analyzeRequest(request)
    
    // Chuyển Task đến Agent chuyên biệt
    let result
    
    switch (targetAgent) {
      case 'batCucLinhSo':
        result = await batCucLinhSoAgent.processTask(task, message, context)
        break
      case 'payment':
        result = await paymentAgent.processTask(task, message, context)
        break
      case 'user':
        result = await userAgent.processTask(task, message, context)
        break
      case 'chatbot':
        result = await chatbotAgent.processTask(task, message, context)
        break
      default:
        // Xử lý bởi Chatbot nếu không xác định được
        result = await chatbotAgent.processTask(task, message, context)
    }
    
    // Cập nhật trạng thái Task
    task.status = { state: 'completed' }
    task.artifacts = result.artifacts || []
    
    return this.formatResponse(task)
  }
  
  analyzeRequest(request) {
    // Logic phân tích yêu cầu để xác định Agent phù hợp
    const lowerRequest = request.toLowerCase()
    
    if (lowerRequest.includes('số điện thoại') || 
        lowerRequest.includes('cccd') || 
        lowerRequest.includes('tài khoản ngân hàng') ||
        lowerRequest.includes('mật khẩu')) {
      return 'batCucLinhSo'
    }
    
    if (lowerRequest.includes('thanh toán') || 
        lowerRequest.includes('nạp tiền') || 
        lowerRequest.includes('gói dịch vụ')) {
      return 'payment'
    }
    
    if (lowerRequest.includes('tài khoản') || 
        lowerRequest.includes('đăng nhập') || 
        lowerRequest.includes('đăng ký') ||
        lowerRequest.includes('đổi mật khẩu')) {
      return 'user'
    }
    
    // Mặc định sử dụng Chatbot
    return 'chatbot'
  }
  
  formatResponse(task) {
    // Chuyển đổi từ Task sang định dạng phản hồi
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
    }
  }
}

module.exports = new RootAgent()
```

### 5.2 Kích hoạt Agent từ Frontend

```vue
<!-- frontend/src/components/chat/AgentSelector.vue -->
<template>
  <div class="agent-selector">
    <div class="title">Chọn Agent</div>
    <div class="agents">
      <button 
        v-for="agent in availableAgents" 
        :key="agent.id"
        :class="{ active: currentAgent === agent.id }"
        @click="selectAgent(agent.id)"
      >
        <font-awesome-icon :icon="agent.icon" />
        <span>{{ agent.name }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAgentStore } from '../../stores/agent'

const agentStore = useAgentStore()

const availableAgents = [
  { id: 'batCucLinhSo', name: 'Phong Thủy Số', icon: 'mobile-alt' },
  { id: 'payment', name: 'Thanh Toán', icon: 'credit-card' },
  { id: 'user', name: 'Tài Khoản', icon: 'user' },
  { id: 'chatbot', name: 'Trò Chuyện', icon: 'comment' }
]

const currentAgent = computed(() => agentStore.activeAgent)

const selectAgent = (agentId) => {
  agentStore.setActiveAgent(agentId)
}
</script>
```

## 6. Quy trình phát triển và triển khai

### 6.1 Môi trường phát triển

#### Môi trường Frontend
- Sử dụng Vite cho phát triển nhanh
- Hot Module Replacement (HMR)
- Cấu hình proxy đến backend

```javascript
// frontend/vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'robots.txt', 'img/*.svg'],
      manifest: {
        name: 'Phong Thủy Số',
        short_name: 'PhongThuySo',
        theme_color: '#4f46e5',
        start_url: '/',
        display: 'standalone',
        background_color: '#ffffff',
        icons: [
          // Các icon PWA
        ]
      }
    })
  ],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    }
  }
})
```

#### Môi trường Backend
- Nodemon cho phát triển
- Cấu hình CORS
- Hỗ trợ Python subprocess

```javascript
// backend/app.js
const express = require('express')
const cors = require('cors')
const morgan = require('morgan')
const { connectDatabase } = require('./services/database')
const agentManager = require('./config/agent-manager')

const app = express()

// Middleware
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? ['https://phongthuyso.vn', 'https://www.phongthuyso.vn'] 
    : 'http://localhost:5173',
  credentials: true
}))
app.use(express.json())
app.use(morgan('dev'))

// Khởi tạo agents
agentManager.initializeAgents()

// API routes
app.use('/api/v1', require('./api/v1/routes'))
app.use('/api/v2/gateway', require('./api/v2/gateway'))
app.use('/api/v2/agent/root', require('./api/v2/controllers/rootAgent'))
app.use('/api/v2/agent/bat-cuc-linh-so', require('./api/v2/controllers/batCucLinhSoAgent'))
app.use('/api/v2/agent/payment', require('./api/v2/controllers/paymentAgent'))
app.use('/api/v2/agent/user', require('./api/v2/controllers/userAgent'))
app.use('/api/v2/agent/chatbot', require('./api/v2/controllers/chatbotAgent'))

// Kết nối database
connectDatabase()

module.exports = app
```

### 6.2 Triển khai

Cấu hình triển khai với Docker và Nginx:

```yaml
# deployment/docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ../frontend
      dockerfile: ../deployment/Dockerfile.frontend
    restart: always
    depends_on:
      - backend
    networks:
      - app-network

  backend:
    build:
      context: ../backend
      dockerfile: ../deployment/Dockerfile.backend
    restart: always
    environment:
      - NODE_ENV=production
      - PORT=3000
      - MONGO_URI=${MONGO_URI}
      - JWT_SECRET=${JWT_SECRET}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - mongodb
      - redis
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - frontend
      - backend
    networks:
      - app-network

  mongodb:
    image: mongo:latest
    restart: always
    volumes:
      - mongo-data:/data/db
    networks:
      - app-network

  redis:
    image: redis:alpine
    restart: always
    volumes:
      - redis-data:/data
    networks:
      - app-network

volumes:
  mongo-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

## 7. Bảo mật và hiệu suất

### 7.1 Bảo mật

- **JWT Authentication**: Sử dụng cho xác thực người dùng
- **HTTPS**: SSL/TLS cho mọi kết nối
- **Input Validation**: Kiểm tra đầu vào từ frontend và backend
- **Rate Limiting**: Giới hạn số lượng yêu cầu API
- **CORS**: Cấu hình chặt chẽ với whitelist domain
- **Helmet**: Bảo vệ HTTP header

### 7.2 Hiệu suất

- **Caching**: Redis cho cache API và session
- **Lazy Loading**: Tải component theo nhu cầu
- **API Optimization**: Giảm thiểu dữ liệu truyền tải
- **CDN**: Sử dụng CDN cho tài nguyên tĩnh
- **Compression**: Nén dữ liệu truyền tải

## 8. Theo dõi và báo cáo lỗi

- **Logging**: Winston và Morgan cho backend, browser console cho frontend
- **Error Tracking**: Sentry hoặc LogRocket
- **Analytics**: Google Analytics hoặc Matomo
- **Performance Monitoring**: New Relic hoặc Datadog

## 9. Kế hoạch nâng cấp

### 9.1 Kế hoạch ngắn hạn (1-3 tháng)
- Chuyển đổi backend hiện tại sang kiến trúc Agent
- Cập nhật frontend để tương thích với API mới
- Tối ưu hóa tốc độ tải trang và phản hồi API

### 9.2 Kế hoạch trung hạn (3-6 tháng)
- Phát triển thêm các Agent mới
- Cải thiện thuật toán phân tích phong thủy
- Tích hợp thanh toán thực tế (VNPay, MoMo)

### 9.3 Kế hoạch dài hạn (6-12 tháng)
- Phát triển ứng dụng di động (React Native)
- Tích hợp trí tuệ nhân tạo nâng cao
- Mở rộng sang các thị trường quốc tế 