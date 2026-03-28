#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能管理器 - 自动检测和创建OpenClaw技能
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional


class SkillManager:
    """OpenClaw技能管理器"""
    
    def __init__(self, plugin_root: str):
        """
        初始化技能管理器
        
        Args:
            plugin_root: 插件根目录路径
        """
        self.plugin_root = Path(plugin_root)
        self.skills_dir = self.plugin_root.parent.parent / "skills"
        self.target_skill_name = "hybrid_qq_messenger"
        self.source_skill_file = self.plugin_root / "SKILL.md"
        
    def skill_exists(self) -> bool:
        """
        检查目标技能是否已存在
        
        Returns:
            bool: 技能是否存在
        """
        target_skill_path = self.skills_dir / self.target_skill_name / "SKILL.md"
        return target_skill_path.exists()
    
    def create_skill_directory(self) -> bool:
        """
        创建技能目录结构
        
        Returns:
            bool: 创建是否成功
        """
        try:
            # 创建技能目录
            skill_dir = self.skills_dir / self.target_skill_name
            skill_dir.mkdir(parents=True, exist_ok=True)
            
            # 复制SKILL.md文件
            if self.source_skill_file.exists():
                shutil.copy2(self.source_skill_file, skill_dir / "SKILL.md")
                print(f"已复制技能文件到: {skill_dir / 'SKILL.md'}")
            else:
                print(f"源技能文件不存在: {self.source_skill_file}")
                return False
            
            # 创建技能配置文件
            self._create_skill_config(skill_dir)
            
            # 创建技能示例文件
            self._create_skill_examples(skill_dir)
            
            print(f"技能目录创建成功: {skill_dir}")
            return True
            
        except Exception as e:
            print(f"创建技能目录失败: {e}")
            return False
    
    def _create_skill_config(self, skill_dir: Path) -> None:
        """
        创建技能配置文件
        
        Args:
            skill_dir: 技能目录路径
        """
        config_content = {
            "skill_info": {
                "name": "hybrid_qq_messenger",
                "display_name": "Hybrid QQ Messenger",
                "description": "混合架构QQ消息处理技能",
                "version": "1.0.0",
                "author": "Alice",
                "category": "messaging",
                "tags": ["qq", "messaging", "napcat", "astrbot"]
            },
            "dependencies": {
                "python": ["websockets", "aiohttp"],
                "services": ["napcat", "astrbot"]
            },
            "configuration": {
                "napcat_ws_url": "ws://localhost:3001",
                "astrbot_api_url": "http://localhost:6185/api/v1/im/message",
                "target_qq": "YOUR_QQ_NUMBER_HERE"
            }
        }
        
        config_file = skill_dir / "skill_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_content, f, ensure_ascii=False, indent=2)
        
        print(f"已创建技能配置文件: {config_file}")
    
    def _create_skill_examples(self, skill_dir: Path) -> None:
        """
        创建技能示例文件
        
        Args:
            skill_dir: 技能目录路径
        """
        examples_dir = skill_dir / "examples"
        examples_dir.mkdir(exist_ok=True)
        
        # 创建基础使用示例
        basic_example = examples_dir / "basic_usage.py"
        basic_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hybrid QQ Messenger 基础使用示例
"""

import asyncio

async def example_send_message():
    """发送消息示例"""
    # 注意：这个示例需要在OpenClaw环境中运行
    # 实际使用时，消息发送功能由插件自动处理
    
    print("🎯 Hybrid QQ Messenger 使用说明")
    print("1. 插件启动后自动处理QQ消息")
    print("2. 通过NapCat接收消息")
    print("3. 通过AstrBot发送消息")
    print("4. OpenClaw AI自然处理对话")
    
    # 在实际OpenClaw环境中，可以通过以下方式发送消息：
    # from main import send_message
    # result = await send_message("这是一条测试消息")

if __name__ == "__main__":
    asyncio.run(example_send_message())
'''
        
        with open(basic_example, 'w', encoding='utf-8') as f:
            f.write(basic_content)
        
        print(f"已创建技能示例文件: {basic_example}")
    
    def initialize_skill(self) -> bool:
        """
        初始化技能 - 检查并创建技能目录
        
        Returns:
            bool: 初始化是否成功
        """
        print("检查技能目录状态...")
        
        # 检查技能目录是否存在
        if not self.skills_dir.exists():
            print(f"OpenClaw技能目录不存在: {self.skills_dir}")
            return False
        
        # 检查目标技能是否已存在
        if self.skill_exists():
            print(f"技能已存在: {self.target_skill_name}")
            return True
        
        # 创建技能目录
        print(f"创建新技能: {self.target_skill_name}")
        return self.create_skill_directory()
    
    def get_skill_info(self) -> Dict[str, Any]:
        """
        获取技能信息
        
        Returns:
            Dict[str, Any]: 技能信息
        """
        return {
            "skill_name": self.target_skill_name,
            "skill_path": str(self.skills_dir / self.target_skill_name),
            "exists": self.skill_exists(),
            "source_file": str(self.source_skill_file),
            "skills_directory": str(self.skills_dir)
        }


def initialize_hybrid_qq_messenger_skill() -> bool:
    """
    初始化Hybrid QQ Messenger技能
    
    Returns:
        bool: 初始化是否成功
    """
    # 获取插件根目录
    plugin_root = Path(__file__).parent.parent
    
    # 创建技能管理器
    skill_manager = SkillManager(str(plugin_root))
    
    # 初始化技能
    return skill_manager.initialize_skill()


if __name__ == "__main__":
    # 测试技能管理器
    success = initialize_hybrid_qq_messenger_skill()
    
    if success:
        print("技能初始化完成!")
    else:
        print("技能初始化失败!")
    
    # 显示技能信息
    plugin_root = Path(__file__).parent.parent
    skill_manager = SkillManager(str(plugin_root))
    info = skill_manager.get_skill_info()
    print(f"\n技能信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")