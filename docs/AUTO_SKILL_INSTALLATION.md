# 自动技能安装功能

## 概述

Hybrid QQ Messenger 插件包含一个自动技能安装系统，在插件启动时自动检测并创建相关的 OpenClaw 技能。

## 功能特性

### 自动检测机制

插件在初始化时会自动检查以下内容：

1. **技能目录存在性**: 检查 OpenClaw skills 目录是否存在
2. **技能文件状态**: 检查目标技能是否已存在
3. **自动创建**: 如果技能不存在，自动创建完整的技能目录结构

### 技能目录结构

```
skills/
└── hybrid_qq_messenger/
    ├── SKILL.md                    # 主技能文档
    ├── skill_config.json           # 技能配置文件
    └── examples/
        └── basic_usage.py          # 使用示例
```

## 技能内容

### 技能文档 (SKILL.md)

- **技能名称**: `hybrid-qq-messenger`
- **技能描述**: 混合架构QQ消息处理技能
- **使用场景**: QQ消息集成、主动通知、会话管理
- **配置说明**: 完整的服务配置指南
- **故障排除**: 常见问题和解决方案

### 配置文件 (skill_config.json)

```json
{
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
```

### 使用示例 (examples/basic_usage.py)

提供基础的使用示例代码，展示如何与插件交互。

## 实现机制

### 技能管理器 (utils/skill_manager.py)

```python
class SkillManager:
    """OpenClaw技能管理器"""
    
    def __init__(self, plugin_root: str):
        self.plugin_root = Path(plugin_root)
        self.skills_dir = self.plugin_root / "skills"
        self.target_skill_name = "hybrid_qq_messenger"
        self.source_skill_file = self.skills_dir / self.target_skill_name / "SKILL.md"
    
    def skill_exists(self) -> bool:
        """检查目标技能是否已存在"""
        
    def create_skill_directory(self) -> bool:
        """创建技能目录结构"""
    
    def initialize_skill(self) -> bool:
        """初始化技能 - 检查并创建技能目录"""
```

### 插件集成 (core/plugin.py)

```python
class HybridQQMessenger:
    def __init__(self, context=None):
        # 初始化技能
        self._initialize_skill()
    
    def _initialize_skill(self):
        """初始化插件技能"""
        skill_success = initialize_hybrid_qq_messenger_skill()
```

## 使用流程

### 自动安装流程

1. **插件启动**: OpenClaw 加载 Hybrid QQ Messenger 插件
2. **技能检测**: 插件自动检查技能目录状态
3. **目录创建**: 如果技能不存在，自动创建完整目录结构
4. **文件生成**: 生成技能文档、配置文件和示例
5. **状态报告**: 记录技能初始化结果

### 手动验证

用户可以通过以下方式验证技能安装：

```bash
# 检查技能目录
ls "J:\Alice\openclaw\skills\hybrid_qq_messenger"

# 验证技能内容
cat "J:\Alice\openclaw\skills\hybrid_qq_messenger\SKILL.md"
```

## 故障排除

### 常见问题

**技能目录创建失败**
- 检查 OpenClaw skills 目录权限
- 验证磁盘空间是否充足
- 确认路径配置正确

**技能文件缺失**
- 检查插件 skills 目录中的源文件
- 验证文件复制权限
- 重新启动插件触发重新安装

**技能初始化错误**
- 查看插件日志获取详细错误信息
- 检查 Python 环境依赖
- 确认技能管理器导入路径

### 日志信息

插件会在日志中记录技能初始化状态：

```
INFO: Hybrid QQ Messenger plugin initialized
INFO: Initializing Hybrid QQ Messenger skill...
INFO: Skill initialization completed
```

或

```
WARNING: Skill initialization failed, but plugin will continue
ERROR: Error during skill initialization: [具体错误信息]
```

## 设计优势

### 用户体验

- **零配置**: 用户无需手动创建技能文件
- **自动更新**: 插件更新时自动同步技能内容
- **一致性**: 确保技能文档与插件功能保持一致

### 维护便利

- **集中管理**: 技能文件与插件代码统一管理
- **版本控制**: 技能与插件版本同步更新
- **错误恢复**: 自动检测和修复技能文件问题

### 扩展性

- **模块化设计**: 技能管理器可独立使用
- **配置灵活**: 支持自定义技能内容和结构
- **多技能支持**: 可扩展支持多个相关技能

## 技术规范

### 兼容性

- **OpenClaw 版本**: 支持所有标准版本
- **Python 版本**: 3.8+
- **文件系统**: 支持 Windows/Linux/macOS

### 性能考虑

- **启动延迟**: 技能初始化在插件启动时异步执行
- **资源占用**: 技能文件占用磁盘空间极小
- **错误隔离**: 技能初始化失败不影响插件核心功能

---

**最后更新**: 2026-03-29  
**版本**: 1.0.0  
**状态**: 生产就绪