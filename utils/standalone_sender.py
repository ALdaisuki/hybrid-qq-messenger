#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone message sender for Hybrid QQ Messenger
Can be used from any session without plugin context
"""

import asyncio
import sys
from pathlib import Path

# Add plugin path
plugin_dir = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_dir))

from adapters.astrbot_adapter import AstrBotAdapter
from config.manager import ConfigManager


async def send_qq_message(message: str, target_qq: str = None) -> dict:
    """
    Send QQ message from any session (standalone function)
    
    Args:
        message: Message content to send
        target_qq: Optional target QQ number (uses config if not provided)
    
    Returns:
        Send result dictionary
    """
    try:
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Override target QQ if provided
        if target_qq:
            config['hybrid_mode']['sender']['target_qq'] = target_qq
        
        # Create AstrBot adapter
        astrbot = AstrBotAdapter(config)
        
        # Send message
        result = await astrbot.send_message(message)
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Standalone send failed: {str(e)}'
        }


async def send_qq_file(file_path: str, message_text: str = "", target_qq: str = None) -> dict:
    """
    Send QQ file from any session (standalone function)
    
    Args:
        file_path: Path to file to send
        message_text: Optional message text to accompany file
        target_qq: Optional target QQ number
    
    Returns:
        Send result dictionary
    """
    try:
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Override target QQ if provided
        if target_qq:
            config['hybrid_mode']['sender']['target_qq'] = target_qq
        
        # Create AstrBot adapter
        astrbot = AstrBotAdapter(config)
        
        # Upload and send file
        result = await astrbot.upload_and_send_file(file_path, message_text)
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Standalone file send failed: {str(e)}'
        }


# Convenience sync functions
def send_message_sync(message: str, target_qq: str = None) -> dict:
    """Synchronous wrapper for send_qq_message"""
    return asyncio.run(send_qq_message(message, target_qq))


def send_file_sync(file_path: str, message_text: str = "", target_qq: str = None) -> dict:
    """Synchronous wrapper for send_qq_file"""
    return asyncio.run(send_qq_file(file_path, message_text, target_qq))


# Example usage
if __name__ == "__main__":
    # Test standalone sending
    result = send_message_sync("Test from standalone sender")
    print(f"Standalone send result: {result}")