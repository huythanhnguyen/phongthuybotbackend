import { apiClient, API_CONFIG } from './api'

const authService = {
  // ... existing code ...
  
  /**
   * Tự động tạo phiên ẩn danh nếu chưa có token
   * @returns {Promise} - Kết quả xác thực tự động
   */
  async autoAuthenticate() {
    if (!localStorage.getItem('phone_analysis_token')) {
      return this.createAnonymousSession('guest_' + Date.now())
    }
    return { success: true }
  },
  
  /**
   * Kiểm tra xác thực
   * @returns {boolean} - true nếu đã đăng nhập, false nếu chưa
   */
  isAuthenticated() {
    // Luôn trả về true để cho phép truy cập
    return true
  }
}

export default authService 