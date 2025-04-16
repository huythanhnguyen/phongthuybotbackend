# Kế hoạch Triển khai Phong Thủy Số trên Render.com

## 1. Tổng quan kiến trúc

### 1.1. Kiến trúc tổng thể
- **Frontend**: Vue.js SPA với nhiều landing page
- **Backend**: Node.js API với kiến trúc Agent-based
- **Triển khai**: Render.com Web Services và API Services

### 1.2. Phân chia dịch vụ
- **Phong Thủy Số Frontend**: Web Service trên Render.com
- **Phong Thủy Số Backend API**: API Service trên Render.com
- **Landing Pages**: Static Sites trên Render.com

## 2. Triển khai Frontend

### 2.1. Ứng dụng chính (Vue SPA)

#### 2.1.1. Cấu hình Render.com
```yaml
# render.yaml cho Frontend
services:
  - type: web
    name: phong-thuy-so-frontend
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./dist
    pullRequestPreviewsEnabled: true
    headers:
      - path: /*
        name: Cache-Control
        value: max-age=0, must-revalidate
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    envVars:
      - key: VITE_API_BASE_URL
        value: https://api-phong-thuy-so.onrender.com
      - key: VITE_ADK_BASE_URL
        value: https://adk-backend.onrender.com
```

#### 2.1.2. Tái sử dụng giao diện ADK
- Tích hợp `AppView.vue` từ ADK framework
- Tùy chỉnh theme và các component phù hợp với thương hiệu Phong Thủy Số
- Giữ nguyên luồng UI và UX chính của ADK

#### 2.1.3. Tùy chỉnh giao diện Chat
```vue
<!-- components/chat/ChatInterface.vue -->
<template>
  <div class="chat-container">
    <chat-header :agent="currentAgent" />
    
    <!-- Hỗ trợ đa phương tiện -->
    <chat-messages :messages="messages" />
    
    <chat-input 
      @send-message="sendMessage"
      @upload-file="uploadFile"
      @record-voice="recordVoice"
      :supports-voice="true"
      :supports-files="true"
      :supports-images="true"
      :supports-video="true"
      :supports-pdf="true"
    />
  </div>
</template>
```

### 2.2. Landing Pages

#### 2.2.1. Cấu trúc Landing Pages
- **BatCucLinhSo Landing**: `/landing/bat-cuc-linh-so`
- **Tương lai**: Các landing page cho các agent khác

#### 2.2.2. Cấu hình Render.com cho Landing Pages
```yaml
# render.yaml cho Landing Pages
services:
  - type: web
    name: bat-cuc-linh-so-landing
    env: static
    buildCommand: npm install && npm run build:landing-bat-cuc
    staticPublishPath: ./dist/landing/bat-cuc-linh-so
    domain: bat-cuc-linh-so.phongthuyso.vn
```

### 2.3. API Key Management UI

```vue
<!-- components/developer/ApiKeyManager.vue -->
<template>
  <div class="api-key-container">
    <h2>Quản lý API Keys</h2>
    
    <!-- Hiển thị API keys hiện có -->
    <api-key-list :keys="apiKeys" @revoke="revokeKey" />
    
    <!-- Form tạo API key mới -->
    <api-key-create-form @create="createNewKey" />
    
    <!-- Hướng dẫn sử dụng API -->
    <api-usage-guide />
  </div>
</template>
```

## 3. Triển khai Backend

### 3.1. Kiến trúc Agent

#### 3.1.1. Root Agent
- Gateway cho tất cả các tương tác
- Phân tích yêu cầu và điều hướng đến Expert Agents

#### 3.1.2. Expert Agents
- **BatCucLinhSo Agent**: Phân tích phong thủy số
- **ChatAgent**: Xử lý trò chuyện thông thường
- **FinanceAgent**: Tư vấn tài chính phong thủy
- **LifestyleAgent**: Tư vấn lối sống theo phong thủy

### 3.2. Cấu hình Render.com cho Backend

```yaml
# render.yaml cho Backend
services:
  - type: web
    name: phong-thuy-so-api
    env: node
    buildCommand: npm install
    startCommand: node server.js
    healthCheckPath: /api/health
    envVars:
      - key: NODE_ENV
        value: production
      - key: MONGODB_URI
        sync: false
      - key: JWT_SECRET
        sync: false
      - key: ADK_API_KEY
        sync: false
      - key: GEMINI_API_KEY
        sync: false
```

### 3.3. Hỗ trợ Đa phương tiện

#### 3.3.1. Xử lý Tệp và Hình ảnh
```javascript
// agents/root-agent/multimedia-processor.js
class MultimediaProcessor {
  async processImage(imageBuffer) {
    // Phân tích hình ảnh sử dụng ADK Vision API
    return await adkVisionApi.analyze(imageBuffer);
  }
  
  async processDocument(documentBuffer, mimeType) {
    // Trích xuất văn bản từ PDF/Docs
    return await adkDocumentApi.extractText(documentBuffer, mimeType);
  }
  
  async processAudio(audioBuffer) {
    // Chuyển speech-to-text
    return await adkSpeechApi.transcribe(audioBuffer);
  }
  
  async processVideo(videoBuffer) {
    // Trích xuất frames và audio
    return await adkVideoApi.analyze(videoBuffer);
  }
}
```

### 3.4. API Key Management

```javascript
// api/v1/routes/developer.js
const router = express.Router();
const { authenticate } = require('../middleware/auth');
const apiKeyController = require('../controllers/apiKeyController');

router.get('/api-keys', authenticate, apiKeyController.listApiKeys);
router.post('/api-keys', authenticate, apiKeyController.createApiKey);
router.delete('/api-keys/:id', authenticate, apiKeyController.revokeApiKey);
router.get('/api-usage/:keyId', authenticate, apiKeyController.getApiUsage);

module.exports = router;
```

## 4. Tích hợp ADK

### 4.1. Frontend

#### 4.1.1. Tích hợp ADK Components
```javascript
// main.js
import { createApp } from 'vue';
import App from './App.vue';
import { ADKProvider, ADKComponents } from '@adk/vue-components';

const app = createApp(App);

app.use(ADKProvider, {
  apiKey: import.meta.env.VITE_ADK_API_KEY,
  baseUrl: import.meta.env.VITE_ADK_BASE_URL
});

app.use(ADKComponents);
app.mount('#app');
```

#### 4.1.2. Tùy chỉnh giao diện ADK
```scss
// assets/scss/adk-overrides.scss
:root {
  --adk-primary-color: #4f46e5;
  --adk-secondary-color: #f59e0b;
  --adk-text-color: #1f2937;
  --adk-background-color: #f9fafb;
  --adk-border-radius: 0.5rem;
}

.adk-chat-container {
  max-width: 1200px;
  margin: 0 auto;
  
  .adk-message-bubble {
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  }
}
```

### 4.2. Backend

#### 4.2.1. Tích hợp ADK Agents API
```javascript
// config/adk-config.js
const { ADKClient } = require('@adk/node-client');

const adkClient = new ADKClient({
  apiKey: process.env.ADK_API_KEY,
  baseUrl: process.env.ADK_BASE_URL
});

module.exports = {
  adkClient,
  agentConfig: {
    rootAgent: {
      name: 'PhongThuySoRoot',
      capabilities: ['routing', 'user-context', 'multimedia']
    },
    expertAgents: {
      batCucLinhSo: {
        name: 'BatCucLinhSo',
        capabilities: ['phone-analysis', 'cccd-analysis', 'bank-account', 'password']
      },
      chatAgent: {
        name: 'PhongThuyChat',
        capabilities: ['conversation', 'feng-shui-knowledge']
      }
      // Thêm các expert agents khác
    }
  }
};
```

## 5. Landing Pages

### 5.1. Cấu trúc giao diện Landing

```
/landing/
├── /bat-cuc-linh-so/
│   ├── index.html
│   ├── assets/
│   │   ├── components/
│   │   │   ├── Hero.vue
│   │   │   ├── Features.vue
│   │   │   ├── Testimonials.vue
│   │   │   ├── Pricing.vue
│   │   │   └── CTASection.vue
│   │   └── styles/
├── /shared/
│   ├── components/
│   ├── styles/
│   └── utils/
└── /future-landing-pages/
    └── ...
```

### 5.2. Xây dựng và triển khai

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  plugins: [vue()],
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        batCucLinhSo: resolve(__dirname, 'landing/bat-cuc-linh-so/index.html'),
        // Thêm các landing page khác trong tương lai
      }
    }
  }
});
```

## 6. API Embedding cho Website Khách hàng

### 6.1. JavaScript SDK

```javascript
// public/sdk/phong-thuy-so-sdk.js
(function(global) {
  class PhongThuySoWidget {
    constructor(options) {
      this.apiKey = options.apiKey;
      this.targetElement = options.targetElement;
      this.theme = options.theme || 'light';
      this.defaultAgent = options.defaultAgent || 'bat-cuc-linh-so';
      
      this.init();
    }
    
    init() {
      // Tạo iframe hoặc elements
      this.createWidgetDOM();
      // Thiết lập listeners
      this.setupEventListeners();
    }
    
    createWidgetDOM() {
      // Tạo widget UI
    }
    
    setupEventListeners() {
      // Xử lý sự kiện
    }
    
    // Phương thức API
    sendMessage(message) {
      // Gửi tin nhắn đến backend
    }
    
    uploadFile(file) {
      // Upload file
    }
  }
  
  global.PhongThuySo = {
    createWidget: function(options) {
      return new PhongThuySoWidget(options);
    }
  };
})(window);
```

### 6.2. HTML Embedding

```html
<!-- Cách nhúng trên website khách hàng -->
<div id="phong-thuy-so-widget"></div>

<script src="https://phongthuyso.vn/sdk/phong-thuy-so-sdk.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    PhongThuySo.createWidget({
      apiKey: 'YOUR_API_KEY',
      targetElement: '#phong-thuy-so-widget',
      theme: 'dark',
      defaultAgent: 'bat-cuc-linh-so'
    });
  });
</script>
```

## 7. Kế hoạch Triển khai

### 7.1. Giai đoạn 1: Chuẩn bị (1-2 tuần)
- Thiết lập dự án trên Render.com
- Tạo repository và CI/CD
- Thiết lập môi trường phát triển

### 7.2. Giai đoạn 2: Core Features (3-4 tuần)
- Triển khai Root Agent và BatCucLinhSo Agent
- Xây dựng giao diện chính với ADK
- Triển khai landing page BatCucLinhSo

### 7.3. Giai đoạn 3: Đa phương tiện (2-3 tuần)
- Triển khai tính năng nhận dạng giọng nói
- Triển khai tính năng xử lý hình ảnh
- Triển khai tính năng xử lý tài liệu và video

### 7.4. Giai đoạn 4: Developer API (2 tuần)
- Xây dựng hệ thống quản lý API key
- Phát triển JavaScript SDK
- Viết tài liệu API

### 7.5. Giai đoạn 5: Tối ưu hóa và Mở rộng (liên tục)
- Thêm Expert Agents mới
- Tạo thêm landing pages
- Tối ưu hóa hiệu suất

## 8. Quản lý cấu hình Render.com

### 8.1. Environment Variables
- **Frontend**:
  - `VITE_API_BASE_URL`
  - `VITE_ADK_BASE_URL`
  - `VITE_ADK_API_KEY`

- **Backend**:
  - `NODE_ENV`
  - `MONGODB_URI`
  - `JWT_SECRET`
  - `ADK_API_KEY`
  - `GEMINI_API_KEY`

### 8.2. Render.com Blueprint

Tập tin `render.yaml` đầy đủ cho toàn bộ dự án:

```yaml
services:
  # Frontend SPA
  - type: web
    name: phong-thuy-so-frontend
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    envVars:
      - key: VITE_API_BASE_URL
        value: https://api-phong-thuy-so.onrender.com
        
  # Landing Page: BatCucLinhSo
  - type: web
    name: bat-cuc-linh-so-landing
    env: static
    buildCommand: npm install && npm run build:landing-bat-cuc
    staticPublishPath: ./dist/landing/bat-cuc-linh-so
    domain: bat-cuc-linh-so.phongthuyso.vn
    
  # Backend API
  - type: web
    name: phong-thuy-so-api
    env: node
    buildCommand: npm install
    startCommand: node server.js
    healthCheckPath: /api/health
    envVars:
      - key: NODE_ENV
        value: production
      - key: MONGODB_URI
        sync: false
      - key: JWT_SECRET
        sync: false
      - key: ADK_API_KEY
        sync: false
      - key: GEMINI_API_KEY
        sync: false
        
  # Database (Optional, có thể sử dụng MongoDB Atlas)
  - type: pserv
    name: phong-thuy-so-mongodb
    env: docker
    dockerfilePath: ./deployment/Dockerfile.mongodb
    disk:
      name: mongodb-data
      mountPath: /data/db
      sizeGB: 10
```

## 9. Kết luận

Kế hoạch triển khai này đưa ra một lộ trình rõ ràng để xây dựng và triển khai dự án Phong Thủy Số trên nền tảng Render.com. Phương pháp tiếp cận này cho phép:

1. **Tích hợp liền mạch** với ADK để tận dụng các tính năng sẵn có
2. **Mở rộng dễ dàng** với nhiều landing page và expert agents
3. **Hỗ trợ đa phương tiện** đầy đủ (văn bản, hình ảnh, âm thanh, video, PDF)
4. **API mở** cho phép khách hàng tích hợp dịch vụ vào website của họ
5. **Triển khai đơn giản** thông qua Render.com với cấu hình "Infrastructure as Code"

Với kiến trúc agent-based này, hệ thống có thể dễ dàng mở rộng thêm các chuyên gia trong tương lai mà không cần thay đổi kiến trúc cốt lõi. 