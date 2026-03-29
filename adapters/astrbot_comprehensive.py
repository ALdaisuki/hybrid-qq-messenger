#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AstrBot Comprehensive Adapter
Complete AstrBot API functionality based on OpenAPI documentation
"""

import json
import logging
from typing import Dict, Any, Optional, List

import aiohttp


class AstrBotComprehensive:
    """AstrBot完整功能适配器 - 基于官方OpenAPI文档"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize comprehensive AstrBot adapter"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get AstrBot configuration
        astrbot_config = config.get('hybrid_mode', {}).get('sender', {})
        self.api_key = astrbot_config.get('api_key', '')
        self.base_url = "http://localhost:6185"
        
    async def send_message(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Send message via AstrBot API"""
        return await self._call_astrbot_api(
            endpoint="/api/v1/im/message",
            method="POST",
            payload={
                "umo": f"default:FriendMessage:{self.config['hybrid_mode']['sender']['target_qq']}",
                "message": message,
                "session_id": session_id or ""
            }
        )
    
    async def chat(self, message: str, username: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Send chat message with streaming support
        
        Args:
            message: Chat message content
            username: User identifier
            session_id: Optional session ID (auto-generated if omitted)
        
        Returns:
            Chat response with Server-Sent Events support
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
        Get chat sessions for user with pagination
        
        Args:
            username: User identifier
            page: Page number (default: 1)
            limit: Items per page (default: 20)
        
        Returns:
            List of chat sessions
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
    
    async def upload_file(self, file_path: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload file to knowledge base
        
        Args:
            file_path: Path to file to upload
            description: Optional file description
        
        Returns:
            Upload result
        """
        # Note: This would require multipart form data implementation
        # For now, return placeholder
        return {
            'status': 'info',
            'message': 'File upload requires multipart form data implementation'
        }
    
    async def list_bots(self) -> Dict[str, Any]:
        """List available bot/platform IDs"""
        return await self._call_astrbot_api(
            endpoint="/api/v1/im/bots",
            method="GET"
        )
    
    async def list_configs(self) -> Dict[str, Any]:
        """List available configuration files"""
        return await self._call_astrbot_api(
            endpoint="/api/v1/configs",
            method="GET"
        )
    
    async def get_repo_info(self) -> Dict[str, Any]:
        """Get AstrBot repository information"""
        return await self._call_astrbot_api(
            endpoint="/api/v1/github/repo-info",
            method="GET"
        )
    
    async def _call_astrbot_api(self, endpoint: str, method: str = "GET", 
                               payload: Optional[Dict[str, Any]] = None,
                               params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make API call to AstrBot"""
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
        """Handle API response"""
        try:
            if response.status == 200:
                # Check content type
                content_type = response.headers.get('Content-Type', '')
                
                if 'application/json' in content_type:
                    response_data = await response.json()
                    return {
                        'status': 'ok',
                        'data': response_data,
                        'status_code': response.status
                    }
                else:
                    # Handle non-JSON responses (like SSE streaming)
                    text_response = await response.text()
                    return {
                        'status': 'ok',
                        'data': {
                            'content_type': content_type,
                            'text': text_response
                        },
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


# Example usage
async def example_comprehensive_usage():
    """示例完整功能用法"""
    from config.manager import ConfigManager
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    comprehensive = AstrBotComprehensive(config)
    
    # 1. 发送消息
    result = await comprehensive.send_message("测试消息")
    print(f"消息发送结果: {result}")
    
    # 2. 聊天功能
    chat_result = await comprehensive.chat("你好", "test_user")
    print(f"聊天结果: {chat_result}")
    
    # 3. 获取聊天会话
    sessions_result = await comprehensive.get_chat_sessions("test_user")
    print(f"会话列表: {sessions_result}")
    
    # 4. 获取机器人列表
    bots_result = await comprehensive.list_bots()
    print(f"机器人列表: {bots_result}")
    
    # 5. 获取配置列表
    configs_result = await comprehensive.list_configs()
    print(f"配置列表: {configs_result}")
    
    # 6. 获取仓库信息
    repo_result = await comprehensive.get_repo_info()
    print(f"仓库信息: {repo_result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_comprehensive_usage())