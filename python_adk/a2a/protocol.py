"""
Agent-to-Agent (A2A) Protocol - Triển khai giao thức giao tiếp giữa các agent

A2A Protocol định nghĩa cách các agent giao tiếp với nhau thông qua:
- Tasks: Đại diện cho các nhiệm vụ cần hoàn thành
- Messages: Giao tiếp giữa các agent
- Artifacts: Dữ liệu chia sẻ giữa các agent
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Trạng thái của Task"""
    CREATED = "created"
    SUBMITTED = "submitted"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"


class Role(str, Enum):
    """Vai trò trong cuộc trò chuyện"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class PartType(str, Enum):
    """Loại của Part trong Message và Artifact"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"


class Part(BaseModel):
    """Phần của một Message hoặc Artifact"""
    type: PartType = PartType.TEXT
    text: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class Message(BaseModel):
    """Tin nhắn trong A2A Protocol"""
    role: Role
    parts: List[Part] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_part(self, part: Part) -> 'Message':
        """Thêm một phần vào tin nhắn"""
        self.parts.append(part)
        return self


class Artifact(BaseModel):
    """Tạo phẩm trong A2A Protocol"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    parts: List[Part] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_part(self, part: Part) -> 'Artifact':
        """Thêm một phần vào tạo phẩm"""
        self.parts.append(part)
        return self


class Task(BaseModel):
    """Nhiệm vụ trong A2A Protocol"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED
    artifacts: List[Artifact] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    parent_task_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

    def update_status(self, status: TaskStatus, error: Optional[str] = None) -> 'Task':
        """Cập nhật trạng thái của Task"""
        self.status = status
        self.updated_at = datetime.now()
        if error:
            self.error = error
        return self

    def add_artifact(self, artifact: Artifact) -> 'Task':
        """Thêm Artifact vào Task"""
        self.artifacts.append(artifact)
        self.updated_at = datetime.now()
        return self


def generate_session_id() -> str:
    """Tạo ID ngẫu nhiên cho session"""
    return f"session-{uuid.uuid4()}" 