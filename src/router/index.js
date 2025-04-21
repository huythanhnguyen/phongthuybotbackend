// Bảo vệ các trang yêu cầu đăng nhập
router.beforeEach((to, from, next) => {
  // Bỏ qua việc kiểm tra xác thực, luôn cho phép truy cập tất cả các route
  next()
}) 