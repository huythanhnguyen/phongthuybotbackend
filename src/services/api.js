// Interceptors để xử lý response và lỗi
apiClient.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // Kiểm tra lỗi 401 Unauthorized
    if (error.response && error.response.status === 401) {
      // Tạo phiên ẩn danh thay vì đăng xuất và chuyển hướng
      const anonymousToken = `anonymous_${Date.now()}`
      localStorage.setItem('phone_analysis_token', anonymousToken)
      localStorage.setItem('phone_analysis_user', JSON.stringify({
        name: 'Người dùng ẩn danh',
        email: 'anonymous@user.com',
        role: 'user',
        isAnonymous: true
      }))
      
      // Reload trang để áp dụng token mới
      window.location.reload()
    }
    
    // Tạo thông báo lỗi
    const errorMessage = 
      (error.response && error.response.data && error.response.data.message) ||
      error.message ||
      'Đã xảy ra lỗi khi kết nối đến máy chủ'
    
    return Promise.reject(new Error(errorMessage))
  }
) 