#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NapCat Receiver Adapter
Handles WebSocket connection to NapCat for receiving QQ messages
"""

import asyncio
import json
import logging
from typing import Optional, Callable, Dict, Any

import websockets


class NapCatReceiver:
    """NapCat消息接收适配器"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize NapCat receiver"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get NapCat configuration
        napcat_config = config.get('hybrid_mode', {}).get('receiver', {})
        self.ws_url = napcat_config.get('napcat_ws_url', 'ws://localhost:3001')
        self.reconnect_delay = napcat_config.get('reconnect_delay', 5)
        self.auto_reconnect = napcat_config.get('auto_reconnect', True)
        
        self.message_callback: Optional[Callable] = None
        self.is_running = False
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
    
    def set_message_callback(self, callback: Callable):
        """Set message processing callback"""
        self.message_callback = callback
    
    async def start(self):
        """Start NapCat receiver"""
        self.is_running = True
        self.logger.info(f"Starting NapCat receiver, connecting to: {self.ws_url}")
        
        while self.is_running:
            try:
                await self._connect_and_listen()
            except Exception as e:
                self.logger.error(f"NapCat connection error: {e}")
                
                if self.is_running and self.auto_reconnect:
                    self.logger.info(f"Reconnecting in {self.reconnect_delay} seconds...")
                    await asyncio.sleep(self.reconnect_delay)
    
    async def _connect_and_listen(self):
        """Connect and listen to NapCat WebSocket"""
        async with websockets.connect(self.ws_url) as websocket:
            self.websocket = websocket
            self.logger.info("NapCat WebSocket connection established")
            
            # Send connection success notification
            await self._send_connection_success()
            
            # Listen for messages
            async for message in websocket:
                if not self.is_running:
                    break
                    
                await self._handle_websocket_message(message)
    
    async def _handle_websocket_message(self, message: str):
        """Handle WebSocket message"""
        try:
            message_data = json.loads(message)
            
            # Filter out QQ message events
            if self._is_qq_message(message_data):
                await self._process_qq_message(message_data)
                
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {e}")
        except Exception as e:
            self.logger.error(f"Error handling WebSocket message: {e}")
    
    def _is_qq_message(self, message_data: Dict[str, Any]) -> bool:
        """Check if message is a QQ message event"""
        post_type = message_data.get('post_type')
        message_type = message_data.get('message_type')
        
        # Filter message events
        return post_type == 'message' and message_type in ['private', 'group']
    
    async def _process_qq_message(self, message_data: Dict[str, Any]):
        """Process QQ message"""
        try:
            # Extract message information
            qq_message = {
                'post_type': message_data.get('post_type'),
                'message_type': message_data.get('message_type'),
                'sub_type': message_data.get('sub_type'),
                'message_id': message_data.get('message_id'),
                'user_id': message_data.get('user_id'),
                'group_id': message_data.get('group_id'),
                'content': message_data.get('message', ''),
                'raw_message': message_data.get('raw_message', ''),
                'session_id': self._get_session_id(message_data),
                'timestamp': message_data.get('time')
            }
            
            self.logger.debug(f"Processing QQ message: {qq_message['content'][:50]}...")
            
            # Call message processing callback
            if self.message_callback:
                await self.message_callback(qq_message)
                
        except Exception as e:
            self.logger.error(f"Error processing QQ message: {e}")
    
    def _get_session_id(self, message_data: Dict[str, Any]) -> str:
        """Generate session ID from message data"""
        message_type = message_data.get('message_type')
        
        if message_type == 'private':
            return f"private_{message_data.get('user_id')}"
        elif message_type == 'group':
            return f"group_{message_data.get('group_id')}"
        else:
            return "unknown"
    
    async def _send_connection_success(self):
        """Send connection success notification"""
        try:
            if self.websocket:
                success_msg = {
                    "action": "send_private_msg",
                    "params": {
                        "user_id": self.config.get('admin_qq'),
                        "message": "NapCat receiver connected successfully"
                    }
                }
                await self.websocket.send(json.dumps(success_msg))
        except Exception as e:
            self.logger.error(f"Error sending connection success notification: {e}")
    
    async def stop(self):
        """Stop NapCat receiver"""
        self.is_running = False
        self.logger.info("Stopping NapCat receiver")
        
        if self.websocket:
            await self.websocket.close()