// services/a2a-protocol.js - Triển khai A2A Protocol

/**
 * Lớp Task - Đại diện cho một nhiệm vụ trong A2A Protocol
 */
class Task {
  constructor(params = {}) {
    this.id = params.id || generateUniqueId();
    this.sessionId = params.sessionId || null;
    this.status = params.status || { state: 'created' };
    this.artifacts = params.artifacts || [];
    this.createdAt = params.createdAt || new Date();
    this.updatedAt = params.updatedAt || new Date();
    this.parentTaskId = params.parentTaskId || null;
    this.metadata = params.metadata || {};
  }

  /**
   * Cập nhật trạng thái của Task
   * @param {string} state - Trạng thái mới
   * @param {Object} metadata - Metadata bổ sung
   */
  updateStatus(state, metadata = {}) {
    this.status = { state, ...metadata };
    this.updatedAt = new Date();
    return this;
  }

  /**
   * Thêm Artifact vào Task
   * @param {Artifact} artifact - Artifact để thêm vào
   */
  addArtifact(artifact) {
    this.artifacts.push(artifact);
    this.updatedAt = new Date();
    return this;
  }

  /**
   * Chuyển đổi Task thành JSON
   * @returns {Object} Biểu diễn JSON của Task
   */
  toJSON() {
    return {
      id: this.id,
      sessionId: this.sessionId,
      status: this.status,
      artifacts: this.artifacts.map(artifact => artifact.toJSON()),
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      parentTaskId: this.parentTaskId,
      metadata: this.metadata
    };
  }
}

/**
 * Lớp Message - Đại diện cho một tin nhắn trong A2A Protocol
 */
class Message {
  constructor(params = {}) {
    this.role = params.role || 'user'; // 'user', 'assistant', 'system'
    this.parts = params.parts || [];
    this.createdAt = params.createdAt || new Date();
    this.metadata = params.metadata || {};
  }

  /**
   * Thêm một phần vào tin nhắn
   * @param {Object} part - Phần để thêm vào
   */
  addPart(part) {
    this.parts.push(part);
    return this;
  }

  /**
   * Chuyển đổi Message thành JSON
   * @returns {Object} Biểu diễn JSON của Message
   */
  toJSON() {
    return {
      role: this.role,
      parts: this.parts,
      createdAt: this.createdAt,
      metadata: this.metadata
    };
  }
}

/**
 * Lớp Artifact - Đại diện cho một tạo phẩm trong A2A Protocol
 */
class Artifact {
  constructor(params = {}) {
    this.type = params.type || 'message';
    this.parts = params.parts || [];
    this.createdAt = params.createdAt || new Date();
    this.metadata = params.metadata || {};
  }

  /**
   * Thêm một phần vào tạo phẩm
   * @param {Object} part - Phần để thêm vào
   */
  addPart(part) {
    this.parts.push(part);
    return this;
  }

  /**
   * Chuyển đổi Artifact thành JSON
   * @returns {Object} Biểu diễn JSON của Artifact
   */
  toJSON() {
    return {
      type: this.type,
      parts: this.parts,
      createdAt: this.createdAt,
      metadata: this.metadata
    };
  }
}

/**
 * Hàm tạo ID ngẫu nhiên
 * @returns {string} ID ngẫu nhiên
 */
function generateUniqueId() {
  return Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
}

module.exports = {
  Task,
  Message,
  Artifact
}; 