#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hybrid QQ Messenger Plugin Entry Point
OpenClaw plugin for hybrid QQ messaging with NapCat reception and AstrBot sending
"""

import sys
import asyncio
from pathlib import Path

# Add plugin path
plugin_dir = Path(__file__).parent
sys.path.insert(0, str(plugin_dir))

# Import from core module
from core.plugin import (
    HybridQQMessenger,
    plugin_start,
    plugin_stop,
    send_message
)

# Import skill manager
from utils.skill_manager import initialize_hybrid_qq_messenger_skill


async def main():
    """Standalone plugin execution"""
    # Set console encoding
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Initialize skill on plugin start
    print("🔍 初始化 Hybrid QQ Messenger 技能...")
    skill_success = initialize_hybrid_qq_messenger_skill()
    
    if skill_success:
        print("✅ 技能初始化完成")
    else:
        print("⚠️ 技能初始化失败，但插件将继续运行")
    
    # Create plugin instance
    plugin = HybridQQMessenger()
    
    try:
        await plugin.start()
        
        # Keep running
        print("Hybrid messenger plugin running, press Ctrl+C to stop...")
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\nReceived stop signal...")
        await plugin.stop()
        print("Hybrid messenger plugin stopped")


if __name__ == "__main__":
    asyncio.run(main())


# OpenClaw plugin interface functions
__all__ = [
    'HybridQQMessenger',
    'plugin_start',
    'plugin_stop', 
    'send_message'
]