#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试技能初始化功能
"""

import sys
import asyncio
from pathlib import Path

# Add plugin path
plugin_dir = Path(__file__).parent
sys.path.insert(0, str(plugin_dir))

from utils.skill_manager import initialize_hybrid_qq_messenger_skill, SkillManager

def test_skill_initialization():
    """测试技能初始化"""
    print("测试技能初始化功能...")
    
    # 测试技能管理器
    skill_manager = SkillManager(str(plugin_dir))
    
    # 获取技能信息
    info = skill_manager.get_skill_info()
    print("\n技能信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # 检查技能是否存在
    exists = skill_manager.skill_exists()
    print(f"\n技能存在状态: {exists}")
    
    # 初始化技能
    print("\n初始化技能...")
    success = initialize_hybrid_qq_messenger_skill()
    print(f"初始化结果: {success}")
    
    return success

if __name__ == "__main__":
    success = test_skill_initialization()
    
    if success:
        print("\n✅ 技能初始化测试通过!")
    else:
        print("\n❌ 技能初始化测试失败!")
    
    print("\n检查技能目录内容:")
    skills_dir = Path("YOUR_OPENCLAW_PATH/skills/hybrid_qq_messenger")
    if skills_dir.exists():
        for item in skills_dir.rglob("*"):
            if item.is_file():
                print(f"  📄 {item.relative_to(skills_dir)}")
            elif item.is_dir():
                print(f"  📁 {item.relative_to(skills_dir)}")
    else:
        print("  技能目录不存在")