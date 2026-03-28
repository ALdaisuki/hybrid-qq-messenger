#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础使用示例 - Hybrid QQ Messenger插件使用示例
"""

import sys
import asyncio

# 添加插件路径
sys.path.insert(0, "..")

from core.plugin import HybridQQMessenger

async def example_basic_usage():
    """基础使用示例"""
    print("🎯 Hybrid QQ Messenger 基础使用示例")
    
    # 示例1: 发送简单消息
    print("\n1. 发送简单消息")
    plugin = HybridQQMessenger()
    
    result = await plugin.send_proactive_message("这是一条测试消息")
    print(f"发送结果: {result}")
    
    # 示例2: 发送到特定会话
    print("\n2. 发送到特定会话")
    result = await plugin.send_proactive_message(
        "这是一条会话特定消息",
        session_id="private_YOUR_QQ_NUMBER_HERE"
    )
    print(f"发送结果: {result}")
    
    # 示例3: 检查配置
    print("\n3. 检查配置")
    config = plugin.config_manager.load_config()
    print(f"接收端状态: {config['hybrid_mode']['receiver']['enabled']}")
    print(f"发送端状态: {config['hybrid_mode']['sender']['enabled']}")
    
    print("\n✅ 基础使用示例完成")

async def example_advanced_usage():
    """高级使用示例"""
    print("\n🎯 Hybrid QQ Messenger 高级使用示例")
    
    plugin = HybridQQMessenger()
    
    # 示例1: 批量发送消息
    print("\n1. 批量发送消息")
    messages = [
        "第一条测试消息",
        "第二条测试消息", 
        "第三条测试消息"
    ]
    
    for i, message in enumerate(messages, 1):
        result = await plugin.send_proactive_message(message)
        print(f"消息 {i} 发送结果: {result.get('status')}")
        await asyncio.sleep(1)  # 避免发送过快
    
    # 示例2: 处理发送结果
    print("\n2. 处理发送结果")
    results = []
    test_messages = ["成功消息", "另一条消息"]
    
    for msg in test_messages:
        result = await plugin.send_proactive_message(msg)
        results.append({
            'message': msg,
            'status': result.get('status'),
            'error': result.get('message')
        })
    
    # 分析结果
    success_count = sum(1 for r in results if r['status'] == 'ok')
    fail_count = len(results) - success_count
    
    print(f"成功: {success_count}, 失败: {fail_count}")
    
    for result in results:
        if result['status'] != 'ok':
            print(f"失败消息: {result['message']}, 错误: {result['error']}")
    
    print("\n✅ 高级使用示例完成")

if __name__ == "__main__":
    print("=" * 50)
    print("Hybrid QQ Messenger 使用示例")
    print("=" * 50)
    
    async def main():
        await example_basic_usage()
        await example_advanced_usage()
        
        print("\n" + "=" * 50)
        print("🎉 所有示例完成！")
        print("=" * 50)
    
    asyncio.run(main())