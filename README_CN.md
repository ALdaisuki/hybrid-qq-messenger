# Hybrid QQ Messenger 插件

> **混合架构的QQ消息解决方案** - 用NapCat收消息，用AstrBot发消息

## 这个插件是做什么的？

如果你想要让OpenClaw能够稳定地处理QQ消息，这个插件就是为你准备的。它把消息接收和发送分开处理：

- **NapCat负责收消息** - 通过WebSocket稳定接收QQ好友或群聊的消息
- **AstrBot负责发消息** - 通过API可靠地发送主动消息
- **OpenClaw处理对话** - 让AI自然地理解QQ消息并作出回应
- **两边互不影响** - 接收和发送分开，一个出问题不影响另一个

## 为什么需要混合架构？

以前用单一服务处理QQ消息有个问题：要么接收不稳定，要么发送不可靠。这个插件把两个服务结合起来：

```
NapCat收消息 → OpenClaw处理 → AstrBot发消息
```

这样即使NapCat偶尔断连，你还能通过AstrBot发消息；反过来，如果AstrBot出问题，收消息的功能还是正常的。

## 主要功能

- **双路径设计** - 收和发完全分开，避免单点故障
- **自然对话** - OpenClaw AI处理消息，不会机械响应
- **会话管理** - 自动跟踪对话上下文，超时自动清理
- **主动通知** - 可以通过AstrBot API发送主动消息
- **配置灵活** - JSON配置文件，支持热更新
- **技能集成** - 自动创建OpenClaw技能

## 你需要准备什么？

### 运行环境
- 已经安装并运行OpenClaw
- NapCat服务运行在端口3001
- AstrBot服务运行在端口6185
- Python 3.8或更高版本

### 必要信息
- AstrBot的API密钥
- 你的QQ号码（用于发送消息）
- 基本命令行操作能力

## 快速安装

### 1. 安装Python依赖
```bash
pip install websockets aiohttp
```

### 2. 复制插件
把整个 `hybrid-qq-messenger` 文件夹复制到你的OpenClaw插件目录：
```bash
cp -r hybrid-qq-messenger $OPENCLAW_HOME/plugins/
```

### 3. 配置OpenClaw
编辑 `openclaw.json`，在 `plugins` 部分添加：
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
        "你的OpenClaw插件路径"
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
      "whitelistUserIds": [YOUR_QQ_NUMBER_HERE],
      "renderMarkdownToPlain": true,
      "normalModeFlushIntervalMs": 1200,
      "normalModeFlushChars": 160
    }
  }
}
```

### 4. 配置插件
复制 `config.json` 并编辑里面的内容：
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
      "api_key": "YOUR_ASTRBOT_API_KEY_HERE",
      "target_qq": "YOUR_QQ_NUMBER_HERE",
      "enabled": true
    }
  }
}
```

### 5. 重启OpenClaw
```bash
openclaw gateway restart
```

## 怎么用这个插件？

### 发送主动消息
```python
from main import send_message

# 发一条简单消息
result = await send_message("这是一条主动消息")

# 发到特定会话
result = await send_message("会话特定消息", session_id="private_YOUR_QQ_NUMBER_HERE")

# 检查发送结果
if result.get('status') == 'ok':
    print("消息发送成功")
else:
    print(f"发送失败: {result.get('message')}")
```

### 完整控制插件
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

## 配置说明

### 接收端 (NapCat)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `napcat_ws_url` | NapCat WebSocket地址 | `ws://localhost:3001` |
| `enabled` | 是否启用接收端 | `true` |
| `auto_reconnect` | 连接断开时自动重连 | `true` |

### 发送端 (AstrBot)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `api_url` | AstrBot API地址 | `http://localhost:6185/api/v1/im/message` |
| `api_key` | AstrBot API密钥 | 必需 |
| `target_qq` | 默认目标QQ号码 | 必需 |
| `enabled` | 是否启用发送端 | `true` |

## 测试验证

### 检查安装
```bash
cd "你的插件路径"
python tests/check_installation.py
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

## 常见问题

**NapCat连接失败**
- 检查NapCat服务是否在运行
- 确认WebSocket URL和端口配置正确
- 验证OneBot配置

**AstrBot API错误**
- 检查API密钥是否正确
- 确认目标QQ号码配置
- 验证AstrBot服务是否可用

**插件不加载**
- 检查插件是否在allow列表中
- 确认插件路径正确
- 重启OpenClaw应用配置

## 项目结构

```
hybrid-qq-messenger/
├── core/           # 核心逻辑
│   └── plugin.py   # 主插件类
├── adapters/       # 外部服务适配器
│   ├── napcat_receiver.py  # NapCat接收器
│   └── astrbot_sender.py   # AstrBot发送器
├── services/       # 业务服务
│   └── session_manager.py  # 会话管理
├── config/         # 配置管理
│   └── manager.py  # 配置处理
├── models/         # 数据模型
│   └── message.py  # 消息模型
├── utils/          # 工具类
│   └── skill_manager.py    # 技能管理
├── tests/          # 测试
├── examples/       # 示例
└── docs/           # 文档
```

## 更多信息

- 📊 **[项目概览](PROJECT_OVERVIEW.md)** - 完整项目细节
- 🙏 **[致谢](ACKNOWLEDGEMENTS.md)** - 感谢框架和贡献者
- 📖 **[详细教程](docs/README_CN_DETAILED.md)** - 超详细安装指南

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**维护者**: OpenClaw社区  
**版本**: 1.0.0  
**状态**: 可以用了

## 社区支持

- 📖 **文档**: 完整的初学者教程
- 🔧 **工具**: 安装检查和测试脚本
- 🐛 **问题**: 报告Bug和请求功能
- 💡 **贡献**: 欢迎代码、文档和测试贡献