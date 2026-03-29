# Hybrid QQ Messenger 插件

[![OpenClaw插件](https://img.shields.io/badge/OpenClaw-插件-blue)](https://openclaw.ai)
[![许可证](https://img.shields.io/badge/许可证-MIT-green)](LICENSE)

一个混合架构的QQ消息插件，为OpenClaw提供稳定的消息接收（NapCat）和可靠的主动消息发送（AstrBot）功能。

## 🎯 功能特性

- **混合架构**: 分离消息接收（NapCat）和发送（AstrBot），确保最大可靠性
- **文件支持**: 发送文本文件、图片、音频和视频附件
- **智能对话**: 基于AI的自然QQ对话处理
- **会话管理**: 自动会话创建和清理
- **错误恢复**: 自动重连和重试机制
- **技能集成**: 自动技能安装，无缝OpenClaw集成

## 🏗️ 架构设计

```
NapCat (WebSocket) → OpenClaw AI → AstrBot (REST API)
     ↑                                   ↓
消息接收                           主动发送
```

## 📋 系统要求

- **OpenClaw**: 最新版本，支持插件
- **NapCat**: 运行在端口3001，支持OneBot v11
- **AstrBot**: 运行在端口6185，启用API密钥
- **Python**: 3.8+，需要aiohttp库

## 🚀 安装指南

### 1. 克隆仓库
```bash
git clone https://github.com/YOUR_USERNAME/hybrid-qq-messenger.git
cd hybrid-qq-messenger
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置OpenClaw
在`openclaw.json`中添加：

```json
{
  "plugins": {
    "load": {
      "paths": [
        "YOUR_OPENCLAW_PATH/plugins/hybrid-qq-messenger"
      ]
    },
    "entries": {
      "hybrid-qq-messenger": {
        "enabled": true
      }
    }
  }
}
```

### 4. 配置插件
编辑`config.json`：

```json
{
  "hybrid_mode": {
    "receiver": {
      "napcat_ws_url": "ws://localhost:3001",
      "enabled": true
    },
    "sender": {
      "api_key": "YOUR_ASTRBOT_API_KEY_HERE",
      "target_qq": "YOUR_QQ_NUMBER_HERE",
      "enabled": true
    }
  }
}
```

### 5. 重启OpenClaw
```bash
# 重启OpenClaw加载插件
openclaw restart
```

## 💡 使用方法

### 在OpenClaw环境中
```python
from main import send_message

# 发送文本消息
await send_message("来自Hybrid QQ Messenger的消息！")

# 发送文件（自动处理上传和附件）
await send_message_with_file("查看此文件！", "path/to/file.txt")
```

### 命令行测试
```bash
# 测试基础功能
python tests/quick_test.py

# 测试完整系统
python tests/test_system.py

# 检查安装
python tests/check_installation.py
```

## 📁 项目结构

```
hybrid-qq-messenger/
├── adapters/           # 消息适配器（NapCat, AstrBot）
├── config/            # 配置管理
├── core/              # 核心插件逻辑
├── docs/              # 完整文档
├── examples/          # 使用示例
├── models/            # 数据模型
├── services/          # 后台服务
├── skills/            # OpenClaw技能集成
├── tests/             # 测试套件
├── utils/             # 工具函数
├── config.json        # 插件配置
├── main.py           # 插件入口点
├── openclaw.plugin.json  # OpenClaw插件清单
└── README_CN.md       # 本文件
```

## 🧪 测试验证

### 快速测试
```bash
python tests/quick_test.py
```

### 完整系统测试
```bash
python tests/test_system.py
```

### 安装检查
```bash
python tests/check_installation.py
```

## 📚 文档资源

- **[快速开始指南](docs/QUICK_START.md)** - 快速上手
- **[详细教程](docs/README_CN_DETAILED.md)** - 完整设置指南
- **[架构概述](docs/ARCHITECTURE.md)** - 技术深度解析
- **[AstrBot API参考](docs/ASTRBOT_API_REFERENCE.md)** - 完整API文档
- **[扩展功能](docs/EXTENDED_FEATURES.md)** - 高级功能

## 🔧 故障排除

### 常见问题

**NapCat连接失败**
- 验证NapCat是否运行在端口3001
- 检查config.json中的WebSocket URL
- 确保OneBot v11兼容性

**AstrBot API错误**
- 验证API密钥权限
- 检查目标QQ号码格式
- 验证AstrBot服务状态

**插件未加载**
- 确认openclaw.json中的插件路径
- 检查OpenClaw日志中的错误
- 验证Python依赖

## 🤝 贡献指南

欢迎贡献！请按以下步骤操作：

1. Fork仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - 出色的AI助手平台
- [NapCat](https://napcat.org) - 可靠的QQ机器人框架
- [AstrBot](https://astrbot.app) - 强大的AI聊天机器人平台
- [OneBot](https://onebot.dev) - 通用机器人协议

---

**注意**: 请将`YOUR_USERNAME`、`YOUR_OPENCLAW_PATH`、`YOUR_ASTRBOT_API_KEY_HERE`和`YOUR_QQ_NUMBER_HERE`替换为您的实际值后再部署。