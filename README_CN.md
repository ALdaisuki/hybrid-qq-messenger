# Hybrid QQ Messenger 插件

> **混合架构QQ消息插件** - 基于NapCat的稳定消息接收和AstrBot的可靠消息推送

## 概述

Hybrid QQ Messenger 是一个专为 OpenClaw 设计的插件，采用混合架构实现稳定可靠的QQ消息处理。

### 核心功能
- **NapCat集成**: 通过 OneBot v11 WebSocket 协议接收QQ消息
- **AstrBot集成**: 通过 REST API 发送主动消息
- **混合架构**: 接收和发送路径分离，确保服务可靠性

## 架构设计

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   NapCat QQ     │────│  OpenClaw 插件   │────│   OpenClaw AI   │
│   (接收端)      │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              │
                              ▼
┌─────────────────┐    ┌──────────────────┐
│   AstrBot API   │◄───│  主动消息发送    │
│   (发送端)      │    │                  │
└─────────────────┘    └──────────────────┘
```

### 技术特性

- **双路径架构**: 接收和发送路径完全分离，避免单点故障
- **自然对话处理**: 消息由 OpenClaw AI 自然处理，不强制响应
- **会话管理**: 智能会话跟踪和自动超时处理
- **主动消息推送**: 通过 AstrBot API 可靠推送主动消息
- **配置驱动**: 灵活的 JSON 配置，支持运行时更新
- **自动技能安装**: 插件启动时自动检测并创建相关技能

## 前置要求

### 环境要求
- OpenClaw 运行环境
- NapCat 服务（已配置并运行）
- AstrBot API 访问权限和凭据
- Python 3.8+ 环境

### 服务要求
- **NapCat**: 运行在端口 3001 的 WebSocket 服务
- **AstrBot**: 运行在端口 6185 的 API 服务

## 安装指南

### 步骤1: 安装依赖

```bash
pip install websockets aiohttp
```

### 步骤2: 复制插件

将插件目录复制到 OpenClaw 插件目录：

```bash
cp -r hybrid-qq-messenger $OPENCLAW_HOME/plugins/
```

### 步骤3: 配置 OpenClaw

编辑 `openclaw.json`，添加以下配置：

```json
{
  "plugins": {
    "allow": [
      "memory-lancedb-pro",
      "google", 
      "openclaw-onebot",
      "hybrid-qq-messenger"
    ],
    "load": {
      "paths": [
        "YOUR_OPENCLAW_PLUGINS_PATH"
      ]
    },
    "entries": {
      "hybrid-qq-messenger": {
        "enabled": true
      }
    }
  },
  "channels": {
    "onebot": {
      "type": "forward-websocket",
      "host": "127.0.0.1",
      "port": 3001,
      "accessToken": "",
      "path": "/onebot/v11/ws",
      "requireMention": true,
      "whitelistUserIds": [YOUR_QQ_NUMBER],
      "renderMarkdownToPlain": true,
      "normalModeFlushIntervalMs": 1200,
      "normalModeFlushChars": 160
    }
  }
}
```

### 步骤4: 配置插件

编辑 `config.json`：

```json
{
  "hybrid_mode": {
    "receiver": {
      "napcat_ws_url": "ws://localhost:3001",
      "enabled": true,
      "auto_reconnect": true
    },
    "sender": {
      "api_url": "http://localhost:6185/api/v1/im/message",
      "api_key": "YOUR_ASTRBOT_API_KEY",
      "target_qq": "YOUR_QQ_NUMBER",
      "enabled": true
    }
  }
}
```

### 步骤5: 重启 OpenClaw

```bash
openclaw gateway restart
```

## 使用方法

### 发送主动消息

```python
from main import send_message

# 发送简单消息
result = await send_message("这是一条主动消息")

# 发送到特定会话
result = await send_message("会话特定消息", session_id="private_YOUR_QQ_NUMBER")

# 检查发送结果
if result.get('status') == 'ok':
    print("消息发送成功")
else:
    print(f"发送失败: {result.get('message')}")
```

### 完整插件控制

```python
from core.plugin import HybridQQMessenger

# 创建插件实例
plugin = HybridQQMessenger(context)

# 启动插件
await plugin.start()

# 发送主动消息
result = await plugin.send_proactive_message("测试消息")

# 停止插件
await plugin.stop()
```

## 配置详解

### 接收端配置 (NapCat)

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `napcat_ws_url` | 字符串 | `ws://localhost:3001` | NapCat WebSocket地址 |
| `enabled` | 布尔值 | `true` | 是否启用接收端 |
| `auto_reconnect` | 布尔值 | `true` | 连接断开时自动重连 |

### 发送端配置 (AstrBot)

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `api_url` | 字符串 | `http://localhost:6185/api/v1/im/message` | AstrBot API地址 |
| `api_key` | 字符串 | - | AstrBot API密钥（必需） |
| `target_qq` | 字符串 | - | 默认目标QQ号码（必需） |
| `enabled` | 布尔值 | `true` | 是否启用发送端 |

## 测试验证

### 测试插件功能

```bash
cd "YOUR_PLUGIN_PATH"
python tests/quick_test.py
```

### 测试消息发送

```bash
python -c "
import asyncio
from main import send_message

async def test():
    result = await send_message('测试消息 - 功能验证')
    print('发送结果:', result)

asyncio.run(test())
"
```

## 故障排除

### 常见问题

**NapCat连接失败**
- 检查NapCat服务是否运行
- 验证WebSocket URL和端口配置
- 确认OneBot配置正确

**AstrBot API错误**
- 验证API密钥是否正确
- 检查目标QQ号码配置
- 确认AstrBot服务可用

**插件不加载**
- 检查插件是否在allow列表中
- 验证插件路径是否正确
- 重启OpenClaw应用配置

## 项目结构

```
hybrid-qq-messenger/
├── core/                    # 核心业务逻辑
│   └── plugin.py           # 主插件类和生命周期管理
├── adapters/               # 外部服务适配器
│   ├── napcat_receiver.py  # NapCat WebSocket接收器
│   └── astrbot_sender.py   # AstrBot API发送器
├── services/               # 业务服务层
│   └── session_manager.py  # 会话管理和状态跟踪
├── config/                 # 配置管理
│   └── manager.py          # 配置加载、验证、更新
├── models/                 # 数据模型
│   └── message.py          # 消息、会话、结果数据模型
├── utils/                  # 工具类
│   └── skill_manager.py    # 技能管理器
├── tests/                  # 测试套件
├── examples/               # 使用示例
└── docs/                   # 详细文档
```

## 项目概览

- 📊 **[项目概览](PROJECT_OVERVIEW.md)** - 完整项目结构和技术细节
- 🙏 **[致谢文档](ACKNOWLEDGEMENTS.md)** - 感谢框架和贡献者
- 📖 **[详细教程](docs/README_CN_DETAILED.md)** - 超详细中文安装教程
- 🔧 **[AstrBot API参考](docs/ASTRBOT_API_REFERENCE.md)** - 完整的API使用指南

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**维护者**: OpenClaw Community  
**版本**: 1.0.0  
**状态**: 生产就绪

## 社区与支持

- 📖 **文档**: 完整的初学者友好教程
- 🔧 **工具**: 安装检查和测试脚本
- 🐛 **问题**: 报告Bug和请求功能
- 💡 **贡献**: 欢迎代码、文档和测试贡献