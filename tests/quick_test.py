#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试 - 验证基本功能
"""

import sys
import asyncio

# Add current directory to path
sys.path.insert(0, '.')

async def quick_test():
    try:
        # Import plugin
        from core.plugin import HybridQQMessenger
        
        # Initialize plugin
        plugin = HybridQQMessenger()
        print("✅ Plugin initialization successful")
        
        # Test configuration
        config = plugin.config_manager.load_config()
        print("✅ Configuration loading successful")
        
        # Test adapters
        if hasattr(plugin, 'napcat_receiver') and hasattr(plugin, 'astrbot_sender'):
            print("✅ Adapters initialization successful")
        else:
            print("❌ Adapters initialization failed")
            return
        
        # Test services
        if hasattr(plugin, 'session_manager'):
            print("✅ Services initialization successful")
        else:
            print("❌ Services initialization failed")
            return
        
        print("🎉 All basic tests passed!")
        print("\nHybrid QQ Messenger is ready for integration!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test())