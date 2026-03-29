#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean Example for Hybrid QQ Messenger
Example usage without any personal data
"""

import asyncio
import os
from pathlib import Path

# Add plugin path to Python path
plugin_dir = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(plugin_dir))

from adapters.astrbot_adapter import AstrBotAdapter
from config.manager import ConfigManager


async def example_usage():
    """
    Example usage of Hybrid QQ Messenger
    
    This example demonstrates how to use the plugin without any personal data.
    Replace YOUR_API_KEY_HERE and YOUR_QQ_NUMBER_HERE with your actual values.
    """
    
    print("🚀 Hybrid QQ Messenger - Clean Example")
    print("=" * 50)
    
    # Load configuration (you need to configure this first)
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    # Initialize AstrBot adapter
    astrbot = AstrBotAdapter(config)
    
    # Example 1: Send text message
    print("\n1. Sending text message...")
    try:
        result = await astrbot.send_message("Hello from Hybrid QQ Messenger!")
        if result.get('status') == 'ok':
            print("✅ Text message sent successfully!")
        else:
            print(f"❌ Text message failed: {result.get('message')}")
    except Exception as e:
        print(f"❌ Text message error: {e}")
    
    # Example 2: Upload and send file
    print("\n2. Uploading and sending file...")
    try:
        # Create a temporary test file
        test_file = "example_test.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("This is a test file from Hybrid QQ Messenger example.")
        
        result = await astrbot.upload_and_send_file(
            test_file,
            "Test file from clean example"
        )
        
        if result.get('status') == 'ok':
            print("✅ File uploaded and sent successfully!")
        else:
            print(f"❌ File upload/send failed: {result.get('message')}")
        
        # Clean up temporary file
        if os.path.exists(test_file):
            os.remove(test_file)
            
    except Exception as e:
        print(f"❌ File upload/send error: {e}")
    
    # Example 3: Chat functionality
    print("\n3. Testing chat functionality...")
    try:
        result = await astrbot.chat("Hello, please introduce yourself", "example_user")
        if result.get('status') == 'ok':
            print("✅ Chat functionality working!")
        else:
            print(f"❌ Chat failed: {result.get('message')}")
    except Exception as e:
        print(f"❌ Chat error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Clean example completed!")


if __name__ == "__main__":
    asyncio.run(example_usage())