import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '../services/authService'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  // State
  const currentUser = ref(null)
  const token = ref(localStorage.getItem('phone_analysis_token') || null)
  
  // Getters
  const isAuthenticated = computed(() => true) // Luôn trả về true
  
  // ... existing code ...
  
  function loadUserFromStorage() {
    try {
      const userStr = localStorage.getItem('phone_analysis_user')
      if (userStr) {
        currentUser.value = JSON.parse(userStr)
      } else {
        // Nếu không có user trong storage, tạo một user ẩn danh
        currentUser.value = {
          name: 'Khách truy cập',
          email: 'guest@example.com',
          role: 'user',
          isAnonymous: true
        }
        localStorage.setItem('phone_analysis_user', JSON.stringify(currentUser.value))
      }
    } catch (error) {
      console.error('Error loading user from storage:', error)
    }
  }
  
  // Hàm đảm bảo luôn có phiên xác thực
  async function ensureAuthenticated() {
    if (!token.value) {
      const response = await authService.autoAuthenticate()
      if (response.success) {
        token.value = response.token || `anonymous_${Date.now()}`
        currentUser.value = response.user || {
          name: 'Khách truy cập',
          email: 'guest@example.com',
          role: 'user',
          isAnonymous: true
        }
        
        localStorage.setItem('phone_analysis_token', token.value)
        localStorage.setItem('phone_analysis_user', JSON.stringify(currentUser.value))
      }
    }
    return true
  }
  
  // Gọi loadUserFromStorage ngay khi tạo store
  loadUserFromStorage()
  
  // Đảm bảo luôn có phiên xác thực
  ensureAuthenticated()

  return {
    currentUser,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    ensureAuthenticated
  }
}) 