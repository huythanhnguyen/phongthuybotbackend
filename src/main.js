import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import authService from './services/authService'

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(createPinia())
app.use(router)

// Tự động xác thực trước khi mount ứng dụng
authService.autoAuthenticate().then(() => {
  app.mount('#app')
}) 