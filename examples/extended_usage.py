#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extended Usage Example for Hybrid QQ Messenger
演示AstrBot扩展功能的使用方法 - 浏览器自动化和插件调用
"""

import asyncio
import sys
from pathlib import Path

# Add plugin path
plugin_dir = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_dir))

from adapters.astrbot_extended import AstrBotExtended
from config.manager import ConfigManager


async def example_browser_automation():
    """浏览器自动化示例"""
    print("🚀 AstrBot 浏览器自动化示例")
    print("=" * 50)
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    extended = AstrBotExtended(config)
    
    try:
        # 1. 创建浏览器沙盒
        print("\n1. 创建浏览器沙盒...")
        sandbox_result = await extended.create_sandbox("test-sandbox")
        print(f"沙盒创建结果: {sandbox_result}")
        
        sandbox_id = None
        if sandbox_result.get('status') == 'ok' and sandbox_result.get('data'):
            sandbox_id = sandbox_result['data'].get('sandbox_id')
            print(f"沙盒ID: {sandbox_id}")
        
        # 2. 导航到网页
        print("\n2. 导航到网页...")
        nav_result = await extended.navigate_to_url("https://www.example.com", sandbox_id)
        print(f"导航结果: {nav_result}")
        
        # 3. 截图
        print("\n3. 截图...")
        screenshot_result = await extended.take_screenshot(sandbox_id)
        print(f"截图结果: {screenshot_result}")
        
        # 4. 提取页面文本
        print("\n4. 提取页面文本...")
        text_result = await extended.extract_text("h1", sandbox_id)
        print(f"文本提取结果: {text_result}")
        
        print("\n✅ 浏览器自动化示例完成")
        
    except Exception as e:
        print(f"❌ 浏览器自动化失败: {e}")


async def example_plugin_integration():
    """插件集成示例"""
    print("\n🔌 AstrBot 插件集成示例")
    print("=" * 50)
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    extended = AstrBotExtended(config)
    
    try:
        # 1. 获取可用插件列表
        print("\n1. 获取插件列表...")
        plugins_result = await extended.get_available_plugins()
        print(f"插件列表结果: {plugins_result}")
        
        # 2. 尝试调用插件 (如果支持)
        print("\n2. 尝试调用插件...")
        try:
            plugin_result = await extended.call_plugin(
                "weather",  # 假设有天气插件
                "get_weather",
                {"city": "Beijing"}
            )
            print(f"插件调用结果: {plugin_result}")
        except Exception as e:
            print(f"⚠️ 插件调用失败 (可能AstrBot不支持): {e}")
        
        print("\n✅ 插件集成示例完成")
        
    except Exception as e:
        print(f"❌ 插件集成失败: {e}")


async def example_hybrid_workflow():
    """混合工作流示例 - 结合消息发送和浏览器自动化"""
    print("\n🔄 混合工作流示例")
    print("=" * 50)
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    extended = AstrBotExtended(config)
    
    try:
        # 1. 发送开始通知
        print("\n1. 发送开始通知...")
        start_msg = "🔍 开始浏览器自动化任务..."
        msg_result = await extended.send_message(start_msg)
        print(f"消息发送结果: {msg_result}")
        
        # 2. 执行浏览器自动化
        print("\n2. 执行浏览器自动化...")
        nav_result = await extended.navigate_to_url("https://httpbin.org/json")
        print(f"导航结果: {nav_result}")
        
        # 3. 提取数据
        print("\n3. 提取数据...")
        extract_result = await extended.extract_text("pre", None)
        print(f"数据提取结果: {extract_result}")
        
        # 4. 发送结果通知
        print("\n4. 发送结果通知...")
        if extract_result.get('status') == 'ok':
            end_msg = "✅ 自动化任务完成，数据已提取"
        else:
            end_msg = "❌ 自动化任务失败"
        
        end_result = await extended.send_message(end_msg)
        print(f"结果通知发送结果: {end_result}")
        
        print("\n✅ 混合工作流示例完成")
        
    except Exception as e:
        print(f"❌ 混合工作流失败: {e}")


async def main():
    """主函数"""
    print("🎯 AstrBot 扩展功能使用示例")
    print("=" * 50)
    
    # 检查AstrBot配置
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    if not config['hybrid_mode']['sender']['api_key']:
        print("⚠️ 请先配置AstrBot API密钥")
        return
    
    # 运行示例
    await example_browser_automation()
    await example_plugin_integration()
    await example_hybrid_workflow()
    
    print("\n" + "=" * 50)
    print("🎉 所有扩展功能示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())