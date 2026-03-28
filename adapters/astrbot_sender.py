#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AstrBot Sender Adapter
Handles API communication with AstrBot for sending proactive messages
"""

import json
import logging
from typing import Dict, Any, Optional

import aiohttp


class AstrBotSender:
    """AstrBot消息发送适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize AstrBot sender"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get AstrBot configuration
        astrbot_config = config.get('hybrid_mode', {}).get('sender', {})
        self.api_url = astrbot_config.get('api_url', 'http://localhost:6185/api/v1/im/message')
        self.api_key = astrbot_config.get('api_key', '')
        self.target_qq = astrbot_config.get('target_qq', '')
        self.retry_count = astrbot_config.get('retry_count', 3)
        self.retry_delay = astrbot_config.get('retry_delay', 2)
    
    async def send_message(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Send message via AstrBot API"""
        self.logger.info(f"Sending message via AstrBot: {message[:50]}...")
        
        for attempt in range(self.retry_count):
            try:
                result = await self._send_api_request(message, session_id)
                
                if result.get('status') == 'ok':
                    self.logger.info("Message sent successfully")
                    return result
                else:
                    self.logger.warning(f"API returned error: {result}")
                    
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.retry_count - 1:
                    self.logger.info(f"Retrying in {self.retry_delay} seconds...")
                    await asyncio.sleep(self.retry_delay)
        
        return {'status': 'error', 'message': 'All retry attempts failed'}
    
    async def _send_api_request(self, message: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Send API request to AstrBot"""
        headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        # Determine target UMO based on session_id
        if session_id and session_id.startswith('group_'):
            group_id = session_id.replace('group_', '')
            umo = f"default:GroupMessage:{group_id}"
        else:
            # Default to friend message
            umo = f"default:FriendMessage:{self.target_qq}"
        
        payload = {
            "umo": umo,
            "message": message,
            "session_id": session_id or ""
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                
                if response.status == 200:
                    response_data = await response.json()
                    return {
                        'status': 'ok',
                        'data': response_data,
                        'umo': umo
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f'API request failed: {response.status}',
                        'status_code': response.status
                    }
    
    def validate_configuration(self) -> bool:
        """Validate AstrBot configuration"""
        if not self.api_key:
            self.logger.error("AstrBot API key not configured")
            return False
        
        if not self.target_qq:
            self.logger.error("Target QQ not configured")
            return False
        
        if not self.api_url:
            self.logger.error("API URL not configured")
            return False
        
        return True