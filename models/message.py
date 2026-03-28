#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Message Models
Data models for message handling and serialization
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class QQMessage:
    """QQ消息数据模型"""
    post_type: str
    message_type: str
    sub_type: str
    message_id: int
    user_id: int
    group_id: Optional[int]
    content: str
    raw_message: str
    session_id: str
    timestamp: int
    
    @classmethod
    def from_onebot_data(cls, data: Dict[str, Any]) -> 'QQMessage':
        """从OneBot数据创建QQMessage实例"""
        return cls(
            post_type=data.get('post_type', ''),
            message_type=data.get('message_type', ''),
            sub_type=data.get('sub_type', ''),
            message_id=data.get('message_id', 0),
            user_id=data.get('user_id', 0),
            group_id=data.get('group_id'),
            content=data.get('message', ''),
            raw_message=data.get('raw_message', ''),
            session_id=cls._generate_session_id(data),
            timestamp=data.get('time', 0)
        )
    
    @staticmethod
    def _generate_session_id(data: Dict[str, Any]) -> str:
        """生成会话ID"""
        message_type = data.get('message_type')
        
        if message_type == 'private':
            return f"private_{data.get('user_id')}"
        elif message_type == 'group':
            return f"group_{data.get('group_id')}"
        else:
            return "unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'post_type': self.post_type,
            'message_type': self.message_type,
            'sub_type': self.sub_type,
            'message_id': self.message_id,
            'user_id': self.user_id,
            'group_id': self.group_id,
            'content': self.content,
            'raw_message': self.raw_message,
            'session_id': self.session_id,
            'timestamp': self.timestamp
        }


@dataclass
class Session:
    """会话数据模型"""
    session_id: str
    user_id: int
    group_id: Optional[int]
    message_type: str
    messages: list
    created_at: float
    last_activity: float
    
    def is_expired(self, timeout: int = 300) -> bool:
        """检查会话是否过期"""
        return (time.time() - self.last_activity) > timeout
    
    def add_message(self, message: Dict[str, Any]):
        """添加消息到会话"""
        self.messages.append(message)
        self.last_activity = time.time()
    
    def get_recent_messages(self, count: int = 10) -> list:
        """获取最近的消息"""
        return self.messages[-count:] if self.messages else []


@dataclass
class SendResult:
    """发送结果数据模型"""
    status: str  # 'ok', 'error'
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    status_code: Optional[int] = None
    
    @classmethod
    def success(cls, data: Optional[Dict[str, Any]] = None) -> 'SendResult':
        """创建成功结果"""
        return cls(status='ok', data=data)
    
    @classmethod
    def error(cls, message: str, status_code: Optional[int] = None) -> 'SendResult':
        """创建错误结果"""
        return cls(status='error', message=message, status_code=status_code)
    
    def is_success(self) -> bool:
        """检查是否成功"""
        return self.status == 'ok'