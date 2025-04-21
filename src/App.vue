<template>
  <div id="app">
    <router-view />
    
    <!-- PWA update notification -->
    <div v-if="needRefresh" class="pwa-update-notification">
      <div class="pwa-update-content">
        <p><strong>Có phiên bản mới!</strong></p>
        <p>Vui lòng cập nhật để trải nghiệm các tính năng mới nhất.</p>
        <div class="pwa-button-group">
          <button @click="updateServiceWorker()" class="pwa-update-button">Cập nhật</button>
          <button @click="closeNotification()" class="pwa-close-button">Sau này</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { registerSW } from 'virtual:pwa-register'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
const needRefresh = ref(false)
const updateServiceWorker = registerSW({
  onNeedRefresh() {
    needRefresh.value = true
  },
  onOfflineReady() {
    console.log('Ứng dụng đã sẵn sàng sử dụng offline')
  }
})

onMounted(async () => {
  // Đảm bảo người dùng luôn được xác thực khi khởi động ứng dụng
  await authStore.ensureAuthenticated()
})

const closeNotification = () => {
  needRefresh.value = false
}
</script> 