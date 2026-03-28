#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装检查脚本 - 验证Hybrid QQ Messenger安装是否正确
"""

import sys
import os
import json
from pathlib import Path

def check_installation():
    """检查安装状态"""
    print("🔍 检查 Hybrid QQ Messenger 安装状态...")
    
    # 检查1: 插件目录
    print("\n1. 检查插件目录...")
    plugin_dir = Path(__file__).parent
    if plugin_dir.exists():
        print("✅ 插件目录存在")
    else:
        print("❌ 插件目录不存在")
        return False
    
    # 检查2: 必需文件
    print("\n2. 检查必需文件...")
    required_files = [
        "main.py",
        "config.json", 
        "openclaw.plugin.json",
        "core/plugin.py",
        "adapters/napcat_receiver.py",
        "adapters/astrbot_sender.py"
    ]
    
    all_files_exist = True
    for file in required_files:
        file_path = plugin_dir / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} 缺失")
            all_files_exist = False
    
    if not all_files_exist:
        return False
    
    # 检查3: 配置文件
    print("\n3. 检查配置文件...")
    config_path = plugin_dir / "config.json"
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查关键配置
            hybrid_config = config.get('hybrid_mode', {})
            receiver_enabled = hybrid_config.get('receiver', {}).get('enabled', False)
            sender_enabled = hybrid_config.get('sender', {}).get('enabled', False)
            
            print(f"✅ 接收端启用: {receiver_enabled}")
            print(f"✅ 发送端启用: {sender_enabled}")
            
            # 检查API密钥
            api_key = hybrid_config.get('sender', {}).get('api_key', '')
            if api_key:
                print("✅ API密钥已配置")
            else:
                print("⚠️ API密钥未配置")
                
        except Exception as e:
            print(f"❌ 配置文件解析错误: {e}")
            return False
    else:
        print("❌ 配置文件不存在")
        return False
    
    # 检查4: OpenClaw配置
    print("\n4. 检查OpenClaw配置...")
    openclaw_dir = plugin_dir.parent.parent
    openclaw_config_path = openclaw_dir / "openclaw.json"
    
    if openclaw_config_path.exists():
        try:
            with open(openclaw_config_path, 'r', encoding='utf-8') as f:
                openclaw_config = json.load(f)
            
            # 检查插件配置
            plugins_config = openclaw_config.get('plugins', {})
            allow_list = plugins_config.get('allow', [])
            
            if 'hybrid-qq-messenger' in allow_list:
                print("✅ 插件在allow列表中")
            else:
                print("❌ 插件不在allow列表中")
                return False
            
            # 检查OneBot配置
            onebot_config = openclaw_config.get('channels', {}).get('onebot', {})
            if onebot_config:
                print("✅ OneBot配置存在")
                print(f"   - 主机: {onebot_config.get('host')}")
                print(f"   - 端口: {onebot_config.get('port')}")
            else:
                print("❌ OneBot配置缺失")
                return False
                
        except Exception as e:
            print(f"❌ OpenClaw配置解析错误: {e}")
            return False
    else:
        print("❌ OpenClaw配置文件不存在")
        return False
    
    # 检查5: Python依赖
    print("\n5. 检查Python依赖...")
    try:
        import websockets
        print("✅ websockets 已安装")
    except ImportError:
        print("❌ websockets 未安装 - 运行: pip install websockets")
        return False
    
    try:
        import aiohttp
        print("✅ aiohttp 已安装")
    except ImportError:
        print("❌ aiohttp 未安装 - 运行: pip install aiohttp")
        return False
    
    print("\n🎉 所有检查通过！")
    print("\n下一步:")
    print("1. 重启OpenClaw: openclaw gateway restart")
    print("2. 测试功能: python quick_test.py")
    print("3. 发送测试消息")
    
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("Hybrid QQ Messenger 安装检查")
    print("=" * 50)
    
    success = check_installation()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 安装检查通过！插件已准备就绪。")
    else:
        print("❌ 安装检查失败。请查看上面的错误信息并修复。")
    print("=" * 50)

if __name__ == "__main__":
    main()