#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NapCat Receiver Adapter for Hybrid QQ Messenger
Handles message reception from NapCat via OpenClaw OneBot plugin
"""

import logging
from typing import Dict, Any, Callable, Optional

import asyncio


class NapCatReceiver:
    """NapCat接收器适配器 - 处理来自NapCat的消息接收"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化NapCat接收器"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 获取NapCat配置
        napcat_config = config.get('hybrid_mode', {}).get('receiver', {})
        self.ws_url = napcat_config.get('napcat_ws_url', 'ws://localhost:3001')
        self.access_token = napcat_config.get('access_token', '')
        self.auto_reconnect = napcat_config.get('auto_reconnect', True)
        self.reconnect_delay = napcat_config.get('reconnect_delay', 5)
        
        # 消息处理器
        self.message_handler: Optional[Callable] = None
        
    async def start_listening(self, message_handler: Callable):
        """
        开始监听消息（实际由OpenClaw OneBot插件处理）
        
        Args:
            message_handler: 消息处理回调函数
        """
        self.message_handler = message_handler
        self.logger.info(f"NapCat receiver initialized with WS URL: {self.ws_url}")
        
        # 注意：实际的消息接收由OpenClaw OneBot插件处理
        # 这里主要是配置和状态管理
        return True
    
    async def handle_incoming_message(self, message_data: Dict[str, Any]) -> bool:
        """
        处理接收到的消息
        
        Args:
            message_data: 接收到的消息数据
            
        Returns:
            处理是否成功
        """
        try:
            if self.message_handler:
                # 调用消息处理器
                await self.message_handler(message_data)
                return True
            else:
                self.logger.warning("No message handler set")
                return False
                
        except Exception as e:
            self.logger.error(f"Error handling incoming message: {e}")
            return False
    
    async def stop_listening(self):
        """停止监听消息"""
        self.logger.info("NapCat receiver stopped")
        return True