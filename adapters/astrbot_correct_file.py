#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AstrBot Correct File Adapter
Based on official developer documentation
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import aiohttp


class AstrBotCorrectFile:
    """AstrBot正确文件发送适配器 - 基于官方开发者文档"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize correct file AstrBot adapter"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get AstrBot configuration
        astrbot_config = config.get('hybrid_mode', {}).get('sender', {})
        self.api_key = astrbot_config.get('api_key', '')
        self.base_url = "http://localhost:6185"
        
    async def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        Upload file to AstrBot and get attachment_id
        
        Args:
            file_path: Path to file to upload
        
        Returns:
            Upload result with attachment_id
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return {
                    'status': 'error',
                    'message': f'File not found: {file_path}'
                }
            
            # Read file content
            with open(file_path_obj, 'rb') as f:
                file_content = f.read()
            
            # Prepare multipart form data
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
        Send message with attachment using correct message chain format
        
        Args:
            plain_text: Plain text message
            attachment_id: Attachment ID from upload_file
            attachment_type: Type of attachment (file, image, video, record)
        
        Returns:
            Send result
        """
        # Correct message format according to AstrBot documentation
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
            "umo": f"default:FriendMessage:{self.config['hybrid_mode']['sender']['target_qq']}",
            "message": message_chain
        }
        
        return await self._call_astrbot_api(
            endpoint="/api/v1/im/message",
            method="POST",
            payload=payload
        )
    
    async def send_image_with_text(self, text: str, attachment_id: str) -> Dict[str, Any]:
        """Send image with text"""
        return await self.send_message_with_attachment(text, attachment_id, "image")
    
    async def send_file_with_text(self, text: str, attachment_id: str) -> Dict[str, Any]:
        """Send file with text"""
        return await self.send_message_with_attachment(text, attachment_id, "file")
    
    async def upload_and_send_file(self, file_path: str, message_text: str = "") -> Dict[str, Any]:
        """
        Upload file and send message in one operation with correct format
        
        Args:
            file_path: Path to file to upload
            message_text: Message text to accompany the file
        
        Returns:
            Combined result
        """
        # Step 1: Upload file
        upload_result = await self.upload_file(file_path)
        
        if upload_result.get('status') != 'ok':
            return upload_result
        
        # Step 2: Get attachment_id
        upload_data = upload_result.get('data', {})
        inner_data = upload_data.get('data', {})
        attachment_id = inner_data.get('attachment_id')
        filename = inner_data.get('filename', Path(file_path).name)
        
        if not attachment_id:
            return {
                'status': 'error',
                'message': 'No attachment_id returned from upload'
            }
        
        # Step 3: Determine attachment type
        file_ext = Path(file_path).suffix.lower()
        if file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            attachment_type = "image"
        elif file_ext in ['.mp3', '.wav', '.ogg']:
            attachment_type = "record"
        elif file_ext in ['.mp4', '.avi', '.mov']:
            attachment_type = "video"
        else:
            attachment_type = "file"
        
        # Step 4: Send message with correct format
        final_message = message_text or f"文件: {filename}"
        return await self.send_message_with_attachment(
            final_message,
            attachment_id,
            attachment_type
        )
    
    async def _call_astrbot_api(self, endpoint: str, method: str = "GET", 
                               payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make API call to AstrBot"""
        headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                if method.upper() == "POST":
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


# Example usage
async def example_correct_file():
    """示例正确文件用法"""
    from config.manager import ConfigManager
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    correct_file = AstrBotCorrectFile(config)
    
    # Create test file
    test_file_path = "correct_test.txt"
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write("这是使用正确格式发送的测试文件")
    
    # Upload and send with correct format
    result = await correct_file.upload_and_send_file(
        test_file_path,
        "✅ 使用正确消息段格式发送的文件"
    )
    
    print(f"正确格式文件发送结果: {result}")
    
    # Clean up
    import os
    if os.path.exists(test_file_path):
        os.remove(test_file_path)


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_correct_file())