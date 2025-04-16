// utils/id-generator.js - Các hàm tạo ID duy nhất

/**
 * Tạo ID duy nhất kết hợp giữa timestamp và chuỗi ngẫu nhiên
 * @returns {string} ID duy nhất
 */
function generateUniqueId() {
  return Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
}

/**
 * Tạo Session ID theo định dạng UUID v4
 * @returns {string} UUID v4
 */
function generateSessionId() {
  // Triển khai UUID v4 đơn giản
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

/**
 * Tạo Task ID với tiền tố
 * @param {string} prefix - Tiền tố cho Task ID
 * @returns {string} Task ID với tiền tố
 */
function generateTaskId(prefix = 'task') {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
}

/**
 * Kiểm tra xem ID có đúng định dạng UUID v4 không
 * @param {string} id - ID cần kiểm tra
 * @returns {boolean} Kết quả kiểm tra
 */
function isValidUUID(id) {
  const regex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return regex.test(id);
}

module.exports = {
  generateUniqueId,
  generateSessionId,
  generateTaskId,
  isValidUUID
}; 