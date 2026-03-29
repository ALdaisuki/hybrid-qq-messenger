#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive AstrBot API Test
测试AstrBot所有可用API端点的完整示例
"""

import asyncio
import sys
from pathlib import Path

# Add plugin path
plugin_dir = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_dir))

from adapters.astrbot_comprehensive import AstrBotComprehensive
from config.manager import ConfigManager


async def test_all_endpoints():
    """测试所有AstrBot API端点"""
    print("🚀 AstrBot 完整API功能测试")
    print("=" * 60)
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    comprehensive = AstrBotComprehensive(config)
    
    # 检查配置
    if not config['hybrid_mode']['sender']['api_key']:
        print("❌ 请先配置AstrBot API密钥")
        return
    
    try:
        # 1. 测试消息发送
        print("\n1. 📤 测试消息发送...")
        msg_result = await comprehensive.send_message("🔍 AstrBot API功能测试消息")
        print(f"   状态: {'✅ 成功' if msg_result.get('status') == 'ok' else '❌ 失败'}")
        print(f"   详情: {msg_result}")
        
        # 2. 测试聊天功能
        print("\n2. 💬 测试聊天功能...")
        chat_result = await comprehensive.chat("你好，请介绍一下你自己", "test_user_001")
        print(f"   状态: {'✅ 成功' if chat_result.get('status') == 'ok' else '❌ 失败'}")
        if chat_result.get('status') == 'ok':
            print(f"   响应类型: {chat_result['data'].get('content_type', 'N/A')}")
        
        # 3. 测试聊天会话
        print("\n3. 📋 测试聊天会话...")
        sessions_result = await comprehensive.get_chat_sessions("test_user_001")
        print(f"   状态: {'✅ 成功' if sessions_result.get('status') == 'ok' else '❌ 失败'}")
        
        # 4. 测试机器人列表
        print("\n4. 🤖 测试机器人列表...")
        bots_result = await comprehensive.list_bots()
        print(f"   状态: {'✅ 成功' if bots_result.get('status') == 'ok' else '❌ 失败'}")
        if bots_result.get('status') == 'ok':
            print(f"   平台数量: {len(bots_result['data']) if isinstance(bots_result['data'], list) else 'N/A'}")
        
        # 5. 测试配置列表
        print("\n5. ⚙️ 测试配置列表...")
        configs_result = await comprehensive.list_configs()
        print(f"   状态: {'✅ 成功' if configs_result.get('status') == 'ok' else '❌ 失败'}")
        
        # 6. 测试仓库信息
        print("\n6. 📦 测试仓库信息...")
        repo_result = await comprehensive.get_repo_info()
        print(f"   状态: {'✅ 成功' if repo_result.get('status') == 'ok' else '❌ 失败'}")
        if repo_result.get('status') == 'ok':
            repo_data = repo_result.get('data', {})
            print(f"   仓库名: {repo_data.get('name', 'N/A')}")
            print(f"   星标数: {repo_data.get('stargazers_count', 'N/A')}")
        
        # 总结
        print("\n" + "=" * 60)
        print("📊 测试总结:")
        print(f"   总测试项: 6")
        print(f"   成功项: {sum(1 for r in [msg_result, chat_result, sessions_result, bots_result, configs_result, repo_result] if r.get('status') == 'ok')}")
        print(f"   失败项: {sum(1 for r in [msg_result, chat_result, sessions_result, bots_result, configs_result, repo_result] if r.get('status') == 'error')}")
        
    except Exception as e:
        print(f"\n💥 测试过程中出现错误: {e}")


async def test_advanced_features():
    """测试高级功能"""
    print("\n🔬 AstrBot 高级功能测试")
    print("=" * 60)
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    comprehensive = AstrBotComprehensive(config)
    
    try:
        # 1. 测试会话管理
        print("\n1. 🗂️ 测试会话管理...")
        for i in range(3):
            session_result = await comprehensive.chat(
                f"这是第{i+1}条测试消息", 
                "advanced_user",
                session_id=f"session_{i}"
            )
            print(f"   会话{i+1}: {'✅' if session_result.get('status') == 'ok' else '❌'}")
        
        # 2. 获取会话列表
        print("\n2. 📋 获取会话列表...")
        advanced_sessions = await comprehensive.get_chat_sessions("advanced_user", page=1, limit=10)
        print(f"   状态: {'✅ 成功' if advanced_sessions.get('status') == 'ok' else '❌ 失败'}")
        
        print("\n✅ 高级功能测试完成")
        
    except Exception as e:
        print(f"\n❌ 高级功能测试失败: {e}")


async def main():
    """主函数"""
    print("🎯 AstrBot 完整API功能测试套件")
    print("=" * 60)
    
    # 运行基础测试
    await test_all_endpoints()
    
    # 运行高级测试
    await test_advanced_features()
    
    print("\n" + "=" * 60)
    print("🎉 所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())