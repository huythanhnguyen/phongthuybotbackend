# ADK và A2A Protocol - Tài liệu tham khảo

## 1. Tổng quan về ADK (Agent Development Kit)

Agent Development Kit (ADK) là một framework mã nguồn mở dùng để phát triển và triển khai AI Agent. ADK có thể được sử dụng với các LLM phổ biến và công cụ AI sinh thành mã nguồn mở, và được thiết kế với trọng tâm là tích hợp chặt chẽ với hệ sinh thái Google và mô hình Gemini.

### Đặc điểm chính của ADK:
- **Orchestration linh hoạt**: Định nghĩa quy trình bằng các workflow agent (Sequential, Parallel, Loop)
- **Kiến trúc Multi-Agent**: Xây dựng ứng dụng mô-đun và có khả năng mở rộng
- **Hệ sinh thái Tool phong phú**: Trang bị agent với nhiều khả năng khác nhau
- **Sẵn sàng triển khai**: Đóng gói và triển khai agent ở bất kỳ đâu
- **Đánh giá tích hợp**: Đánh giá có hệ thống hiệu suất của agent

### Các loại Agent trong ADK:
1. **LLM Agents**: Sử dụng LLM để thực hiện nhiệm vụ
2. **Workflow Agents**:
   - Sequential Agents: Thực hiện các bước tuần tự
   - Loop Agents: Lặp lại quá trình cho đến khi đạt điều kiện
   - Parallel Agents: Thực hiện nhiều nhiệm vụ đồng thời
3. **Custom Agents**: Agents tùy chỉnh theo nhu cầu riêng
4. **Multi-agent systems**: Hệ thống nhiều agent phối hợp

### Các Tools trong ADK:
- Function tools
- Built-in tools
- Third party tools
- Google Cloud tools
- MCP tools
- OpenAPI tools

### Chức năng chuyển giao nhiệm vụ:
ADK hỗ trợ khả năng chuyển giao nhiệm vụ giữa các agent:
```python
google.adk.tools.transfer_to_agent(agent_name, tool_context)
```
Hàm này cho phép chuyển câu hỏi/nhiệm vụ sang một agent khác.

## 2. A2A Protocol (Agent-to-Agent Protocol)

A2A là một giao thức mở cho phép khả năng tương tác giữa các Agent, thu hẹp khoảng cách giữa các hệ thống agent không đồng nhất.

### Nguyên tắc chính:
- **Đơn giản**: Tái sử dụng các tiêu chuẩn hiện có
- **Sẵn sàng cho doanh nghiệp**: Xác thực, Bảo mật, Quyền riêng tư, Theo dõi, Giám sát
- **Bất đồng bộ đầu tiên**: Hỗ trợ tác vụ (rất) dài và human-in-the-loop
- **Không phụ thuộc phương thức**: text, audio/video, forms, iframe, v.v.
- **Thực thi không minh bạch**: Các agent không cần chia sẻ suy nghĩ, kế hoạch hoặc công cụ

### Các thành phần chính trong A2A:

#### 1. Actors (Tác nhân):
- **User**: Người dùng cuối (con người hoặc dịch vụ)
- **Client**: Thực thể yêu cầu hành động từ một agent thay mặt cho người dùng
- **Remote Agent (Server)**: Agent "blackbox" đóng vai trò là máy chủ A2A

#### 2. Agent Card:
Mỗi Remote Agent hỗ trợ A2A phải xuất bản một Agent Card mô tả khả năng/kỹ năng và cơ chế xác thực của agent.

#### 3. Các đối tượng cốt lõi:
- **Task**: Cho phép Client và Remote Agent đạt được kết quả cụ thể
- **Artifact**: Kết quả được tạo ra bởi Agent
- **Message**: Nội dung không phải Artifact (suy nghĩ, ngữ cảnh, hướng dẫn...)
- **Part**: Một phần nội dung hoàn chỉnh được trao đổi

#### 4. Phương thức liên lạc:
- Sử dụng HTTP làm phương tiện truyền tải
- Sử dụng JSON-RPC 2.0 làm định dạng trao đổi dữ liệu
- Hỗ trợ streaming qua SSE
- Hỗ trợ thông báo đẩy cho các tác vụ dài

## 3. Tích hợp MCP và A2A

Model Capability Protocol (MCP) là một API tiêu chuẩn cho phép ứng dụng tương tác với các mô hình AI thông qua các khả năng cụ thể. MCP có thể được tích hợp với A2A để tạo ra một hệ sinh thái agent hoàn chỉnh.

### Lợi ích của tích hợp MCP và A2A:
- Khả năng tương tác giữa các agent với các mô hình AI khác nhau
- Tiêu chuẩn hóa việc xác thực và ủy quyền
- Hỗ trợ doanh nghiệp với các tính năng bảo mật và giám sát
- Khả năng mở rộng và linh hoạt

## 4. Hướng dẫn thiết kế hệ thống Agent

### Cấu trúc thư mục khuyến nghị:
```
/project-root
  /agents
    /root-agent          # Agent chính điều phối
    /specialized-agents  # Các agent chuyên biệt
      /bat-cuc-linh-so
      /payment
      /user-management
  /tools                 # Các công cụ dùng chung
  /models                # Định nghĩa dữ liệu
  /services              # Dịch vụ chia sẻ
  /api                   # API endpoints
  /config                # Cấu hình
  /utils                 # Tiện ích
```

### Quy trình xây dựng Agent:
1. Xác định nhiệm vụ và phạm vi của agent
2. Chọn loại agent phù hợp (LLM, Workflow, Custom)
3. Xác định các công cụ cần thiết
4. Triển khai logic agent
5. Kiểm thử và đánh giá
6. Triển khai và giám sát

### Các mẫu Agent điển hình:
- Root Agent: Điều phối các agent khác
- Specialized Agent: Thực hiện nhiệm vụ cụ thể
- Tool-using Agent: Sử dụng các công cụ để hoàn thành nhiệm vụ
- Memory-enhanced Agent: Lưu trữ và sử dụng bộ nhớ

### Các phương pháp giao tiếp giữa các Agent:
- Direct transfer: Chuyển giao trực tiếp nhiệm vụ
- Task delegation: Ủy thác nhiệm vụ
- Collaborative problem-solving: Giải quyết vấn đề cộng tác
- Information sharing: Chia sẻ thông tin 