#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AstrBot Adapter for Hybrid QQ Messenger
Complete implementation based on official AstrBot OpenAPI documentation
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import aiohttp


class AstrBotAdapter:
    """AstrBot适配器 - 基于官方OpenAPI文档的完整实现"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化AstrBot适配器"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 获取AstrBot配置
        astrbot_config = config.get('hybrid_mode', {}).get('sender', {})
        self.api_key = astrbot_config.get('api_key', '')
        self.base_url = "http://localhost:6185"
        self.target_qq = astrbot_config.get('target_qq', '')
        
    async def send_message(self, message: str) -> Dict[str, Any]:
        """
        发送纯文本消息
        
        Args:
            message: 消息内容
        
        Returns:
            发送结果
        """
        payload = {
            "umo": f"default:FriendMessage:{self.target_qq}",
            "message": message
        }
        
        return await self._call_astrbot_api(
            endpoint="/api/v1/im/message",
            method="POST",
            payload=payload
        )
    
    async def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        上传文件到AstrBot并获取attachment_id
        
        Args:
            file_path: 文件路径
        
        Returns:
            上传结果，包含attachment_id
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return {
                    'status': 'error',
                    'message': f'File not found: {file_path}'
                }
            
            # 读取文件内容
            with open(file_path_obj, 'rb') as f:
                file_content = f.read()
            
            # 准备multipart表单数据
            data = aiohttp.FormData()
            data.add_field('file', file_content, filename=file_path_obj.name)
            
            headers = {
                'X-API-Key': self.api_key
            }
            
            url = f"{self.base_url}/api/v1/file"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    return await self._handle_response(response)
                    
        except Exception as e:
            self.logger.error(f"File upload failed: {e}")
            return {
                'status': 'error',
                'message': f'File upload failed: {e}'
            }
    
    async def send_message_with_attachment(self, plain_text: str, attachment_id: str, 
                                        attachment_type: str = "file") -> Dict[str, Any]:
        """
        使用正确的消息段格式发送消息和附件
        
        Args:
            plain_text: 纯文本消息
            attachment_id: 附件ID
            attachment_type: 附件类型 (file, image, video, record)
        
        Returns:
            发送结果
        """
        # 根据AstrBot开发者文档的正确格式
        message_chain = [
            {
                "type": "plain",
                "text": plain_text
            },
            {
                "type": attachment_type,
                "attachment_id": attachment_id
            }
        ]
        
        payload = {
            "umo": f"default:FriendMessage:{self.target_qq}",
            "message": message_chain
        }
        
        return await self._call_astrbot_api(
            endpoint="/api/v1/im/message",
            method="POST",
            payload=payload
        )
    
    async def upload_and_send_file(self, file_path: str, message_text: str = "") -> Dict[str, Any]:
        """
        上传文件并发送消息（一体化操作）
        
        Args:
            file_path: 文件路径
            message_text: 伴随文件的消息文本
        
        Returns:
            综合结果
        """
        # 步骤1: 上传文件
        upload_result = await self.upload_file(file_path)
        
        if upload_result.get('status') != 'ok':
            return upload_result
        
        # 步骤2: 获取attachment_id
        upload_data = upload_result.get('data', {})
        inner_data = upload_data.get('data', {})
        attachment_id = inner_data.get('attachment_id')
        filename = inner_data.get('filename', Path(file_path).name)
        
        if not attachment_id:
            return {
                'status': 'error',
                'message': 'No attachment_id returned from upload'
            }
        
        # 步骤3: 确定附件类型
        file_ext = Path(file_path).suffix.lower()
        if file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            attachment_type = "image"
        elif file_ext in ['.mp3', '.wav', '.ogg']:
            attachment_type = "record"
        elif file_ext in ['.mp4', '.avi', '.mov']:
            attachment_type = "video"
        else:
            attachment_type = "file"
        
        # 步骤4: 发送消息
        final_message = message_text or f"File: {filename}"
        return await self.send_message_with_attachment(
            final_message,
            attachment_id,
            attachment_type
        )
    
    async def chat(self, message: str, username: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        发送聊天消息（支持流式响应）
        
        Args:
            message: 聊天消息内容
            username: 用户标识
            session_id: 可选会话ID
        
        Returns:
            聊天响应（SSE流式）
        """
        payload = {
            "message": message,
            "username": username
        }
        if session_id:
            payload["session_id"] = session_id
        
        return await self._call_astrbot_api(
            endpoint="/api/v1/chat",
            method="POST",
            payload=payload
        )
    
    async def get_chat_sessions(self, username: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """
        获取用户聊天会话列表
        
        Args:
            username: 用户标识
            page: 页码
            limit: 每页数量
        
        Returns:
            会话列表
        """
        params = {
            "username": username,
            "page": page,
            "limit": limit
        }
        
        return await self._call_astrbot_api(
            endpoint="/api/v1/chat/sessions",
            method="GET",
            params=params
        )
    
    async def list_bots(self) -> Dict[str, Any]:
        """获取机器人/平台ID列表"""
        return await self._call_astrbot_api(
            endpoint="/api/v1/im/bots",
            method="GET"
        )
    
    async def list_configs(self) -> Dict[str, Any]:
        """获取可用配置文件列表"""
        return await self._call_astrbot_api(
            endpoint="/api/v1/configs",
            method="GET"
        )
    
    async def _call_astrbot_api(self, endpoint: str, method: str = "GET", 
                               payload: Optional[Dict[str, Any]] = None,
                               params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """调用AstrBot API"""
        headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                if method.upper() == "GET":
                    async with session.get(
                        url,
                        headers=headers,
                        params=params,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:
                        return await self._handle_response(response)
                
                elif method.upper() == "POST":
                    async with session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        return await self._handle_response(response)
                
                else:
                    return {
                        'status': 'error',
                        'message': f'Unsupported HTTP method: {method}'
                    }
                        
        except Exception as e:
            self.logger.error(f"AstrBot API call failed: {e}")
            return {
                'status': 'error',
                'message': f'API call failed: {e}'
            }
    
    async def _handle_response(self, response) -> Dict[str, Any]:
        """处理API响应"""
        try:
            if response.status == 200:
                response_data = await response.json()
                return {
                    'status': 'ok',
                    'data': response_data,
                    'status_code': response.status
                }
            else:
                error_text = await response.text()
                return {
                    'status': 'error',
                    'message': f'API request failed: {response.status}',
                    'error_details': error_text,
                    'status_code': response.status
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Response processing failed: {e}',
                'status_code': response.status
            }