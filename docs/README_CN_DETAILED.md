# Hybrid QQ Messenger 插件 - 超详细教程

> **混合架构QQ消息插件** - 专为OpenClaw初学者设计的完整教程

## 🎯 这个插件是做什么的？

如果你想要让OpenClaw能够：
- 📱 **接收QQ消息** - 通过NapCat服务接收QQ好友或群聊的消息
- 📤 **发送QQ消息** - 通过AstrBot服务主动发送消息给QQ好友
- 🧠 **智能对话** - 让OpenClaw AI自然处理QQ对话
- 🔄 **稳定可靠** - 接收和发送分开，确保服务不中断

那么这个插件就是为你准备的！

## 🏗️ 架构原理（通俗解释）

想象一下这个插件就像一个聪明的邮局：

```
📮 接收邮箱 (NapCat) → 📦 处理中心 (插件) → 🤖 AI助手 (OpenClaw)
                              ↓
📤 发送邮箱 (AstrBot) → 📱 QQ好友
```

- **接收端**：NapCat就像你的QQ邮箱，专门接收消息
- **发送端**：AstrBot就像快递员，专门发送消息
- **插件**：就像邮局，负责协调接收和发送
- **AI**：就像聪明的助手，处理收到的消息

## 📋 安装前准备（检查清单）

### 必需的服务
- ✅ **OpenClaw** - 已经安装并可以正常运行
- ✅ **NapCat** - QQ机器人服务，运行在端口3001
- ✅ **AstrBot** - 消息发送服务，运行在端口6185

### 必需的信息
- 🔑 **AstrBot API密钥** - 从AstrBot服务获取
- 📱 **你的QQ号码** - 用于发送消息的目标
- 🖥️ **基本命令行操作** - 会使用终端/命令提示符

## 🚀 完整安装教程（一步一步来）

### 第一步：检查Python环境

打开终端（Windows按Win+R，输入cmd，按回车），运行：

```bash
python --version
```

应该显示 `Python 3.8` 或更高版本。如果没有，请先安装Python。

### 第二步：安装Python依赖

在终端中运行：

```bash
pip install websockets aiohttp
```

**这是什么？**
- `websockets` - 让插件能够连接NapCat的WebSocket
- `aiohttp` - 让插件能够调用AstrBot的API

### 第三步：复制插件文件

1. 找到你的OpenClaw安装目录（通常是 `YOUR_OPENCLAW_PATH`）
2. 进入 `plugins` 文件夹
3. 把整个 `hybrid-qq-messenger` 文件夹复制到这里

**最终路径应该是：**
```
YOUR_OPENCLAW_PATH\plugins\hybrid-qq-messenger\
```

### 第四步：配置NapCat（重要！）

找到你的NapCat配置文件，通常在：
```
napcat/config/onebot11_你的QQ号.json
```

用文本编辑器打开这个文件，确保包含以下内容：

```json
{
  "websocketClients": [
    {
      "host": "127.0.0.1",
      "port": 3001,
      "accessToken": "",
      "message_post_format": "array"
    }
  ]
}
```

**特别注意：** `message_post_format` 必须设置为 `"array"`，否则无法正确接收消息！

### 第五步：配置OpenClaw

找到OpenClaw配置文件：
```
YOUR_OPENCLAW_PATH\openclaw.json
```

用文本编辑器打开，找到 `plugins` 部分，添加以下配置：

```json
{
  "plugins": {
    "allow": [
      "memory-lancedb-pro",
      "google", 
      "openclaw-onebot",
      "hybrid-qq-messenger"  // 添加这一行
    ],
    "load": {
      "paths": [
        "YOUR_OPENCLAW_PATH\\\\plugins\\\\memory-lancedb-pro",
        "YOUR_OPENCLAW_PATH\\\\plugins\\\\hybrid-qq-messenger"  // 添加这一行
      ]
    },
    "entries": {
      "hybrid-qq-messenger": {
        "enabled": true  // 添加这一节
      }
    }
  }
}
```

然后在同一文件中找到 `channels` 部分，添加：

```json
{
  "channels": {
    "onebot": {
      "type": "forward-websocket",
      "host": "127.0.0.1",
      "port": 3001,
      "accessToken": "",
      "path": "/onebot/v11/ws",
      "requireMention": true,
      "whitelistUserIds": [YOUR_QQ_NUMBER_HERE],  // 改成你的QQ号
      "renderMarkdownToPlain": true,
      "normalModeFlushIntervalMs": 1200,
      "normalModeFlushChars": 160
    }
  }
}
```

### 第六步：配置插件

打开插件配置文件：
```
YOUR_OPENCLAW_PATH\plugins\hybrid-qq-messenger\config.json
```

修改为以下内容：

```json
{
  "hybrid_mode": {
    "receiver": {
      "type": "openclaw-onebot",
      "napcat_ws_url": "ws://localhost:3001",
      "enabled": true,
      "accessToken": "",
      "auto_reconnect": true,
      "reconnect_delay": 5
    },
    "sender": {
      "type": "astrbot-api",
      "api_url": "http://localhost:6185/api/v1/im/message",
      "api_key": "YOUR_ASTRBOT_API_KEY_HERE",  // 改成你的API密钥
      "enabled": true,
      "target_qq": "YOUR_QQ_NUMBER_HERE",  // 改成你的QQ号
      "retry_count": 3,
      "retry_delay": 2
    },
    "routing": {
      "auto_switch": true,
      "fallback_to_astrbot": true,
      "session_timeout": 300,
      "max_message_length": 1000
    },
    "enabled": true
  },
  "logging": {
    "level": "INFO",
    "file": "logs/hybrid-messenger.log",
    "max_size_mb": 10
  }
}
```

**重要修改：**
- `api_key`：改成你从AstrBot获取的真实API密钥
- `target_qq`：改成你的QQ号码（例如：YOUR_QQ_NUMBER_HERE）

### 第七步：重启OpenClaw

在终端中运行：

```bash
openclaw gateway restart
```

等待OpenClaw重新启动，这可能需要几秒钟。

## 🧪 验证安装（确保一切正常）

### 方法1：运行安装检查

打开终端，进入插件目录：

```bash
cd "YOUR_PLUGIN_PATH_HERE"
python check_installation.py
```

如果所有检查都显示 ✅，说明安装正确！

### 方法2：测试消息发送

在同一个目录下运行：

```bash
python -c "
import asyncio
from main import send_message

async def test():
    result = await send_message('测试消息 - 安装验证')
    print('发送结果:', result)

asyncio.run(test())
"
```

如果看到 `发送结果: {'status': 'ok'}`，说明消息发送成功！

### 方法3：测试完整功能

```bash
python test_system.py
```

这个脚本会测试所有组件，确保整个系统正常工作。

## 💡 如何使用插件

### 基本使用（自动模式）

插件启动后会自动工作：

1. **接收消息**：当QQ好友发送消息时，OpenClaw AI会自动处理
2. **智能回复**：AI基于对话上下文决定是否回复
3. **发送消息**：你可以通过代码主动发送消息

### 发送主动消息

创建一个Python文件 `send_message.py`：

```python
import asyncio
from main import send_message

async def main():
    # 发送简单消息
    result = await send_message("你好！这是一条测试消息")
    
    if result.get('status') == 'ok':
        print("🎉 消息发送成功！")
    else:
        print(f"❌ 发送失败: {result.get('message')}")

# 运行发送函数
asyncio.run(main())
```

保存后运行：
```bash
python send_message.py
```

### 发送到特定会话

如果你想要发送给特定的QQ好友或群聊：

```python
# 发送给特定好友（私聊）
result = await send_message("私聊消息", session_id="private_123456789")

# 发送到群聊
result = await send_message("群聊消息", session_id="group_987654321")
```

**session_id格式：**
- 私聊：`private_QQ号码`
- 群聊：`group_群号`

## 🔧 配置详解（每个参数的作用）

### 接收端配置

```json
"receiver": {
  "napcat_ws_url": "ws://localhost:3001",  // NapCat的WebSocket地址
  "enabled": true,                          // 是否启用接收功能
  "auto_reconnect": true,                   // 断开时自动重连
  "reconnect_delay": 5                      // 重连等待时间（秒）
}
```

### 发送端配置

```json
"sender": {
  "api_url": "http://localhost:6185/api/v1/im/message",  // AstrBot API地址
  "api_key": "你的API密钥",                    // AstrBot API密钥（必需）
  "target_qq": "你的QQ号",                      // 默认发送目标（必需）
  "enabled": true,                                      // 是否启用发送功能
  "retry_count": 3,                                     // 发送失败重试次数
  "retry_delay": 2                                      // 重试间隔（秒）
}
```

### 路由配置

```json
"routing": {
  "auto_switch": true,           // 自动切换接收和发送
  "fallback_to_astrbot": true,   // 接收失败时使用AstrBot发送
  "session_timeout": 300,        // 会话超时时间（5分钟）
  "max_message_length": 1000     // 最大消息长度
}
```

## 🚨 常见问题解决

### 问题1：NapCat连接失败

**症状：** 在OpenClaw日志中看到 "no config, service will not connect"

**解决步骤：**
1. 检查NapCat是否运行：
   ```bash
   netstat -an | findstr :3001
   ```
   应该看到 `LISTENING` 状态

2. 检查NapCat配置中的 `message_post_format` 是否为 `"array"`

3. 检查OpenClaw配置中的host和port是否正确

### 问题2：AstrBot API错误

**症状：** 发送消息时返回 "API请求失败: 405"

**解决步骤：**
1. 检查API密钥是否正确
2. 检查目标QQ号码配置
3. 检查AstrBot服务是否运行：
   ```bash
   curl -H "X-API-Key: 你的API密钥" http://localhost:6185/api/v1/im/status
   ```

### 问题3：插件不加载

**症状：** 在OpenClaw日志中看到 "plugin not found"

**解决步骤：**
1. 检查插件是否在 `allow` 列表中
2. 检查插件路径是否正确
3. 重启OpenClaw：`openclaw gateway restart`

### 问题4：消息发送成功但收不到

**解决步骤：**
1. 检查目标QQ号码是否正确
2. 检查AstrBot服务日志
3. 确认QQ客户端网络连接正常

## 📊 监控和日志

### 查看OpenClaw日志

```bash
openclaw logs
```

### 查看插件日志

插件日志文件在：
```
YOUR_OPENCLAW_PATH\plugins\hybrid-qq-messenger\logs\hybrid-messenger.log
```

### 检查服务状态

```bash
# 检查NapCat
netstat -an | findstr :3001

# 检查AstrBot  
curl -H "X-API-Key: 你的API密钥" http://localhost:6185/api/v1/im/status
```

## 🔄 高级功能

### 会话管理

插件会自动管理对话会话：
- 每个QQ好友或群聊都有独立的会话
- 会话5分钟无活动会自动清理
- 保持最近50条消息的历史记录

### 配置热更新

你可以在运行时更新配置：

```python
from config.manager import update_hybrid_config

new_config = {
    "hybrid_mode": {
        "sender": {
            "api_key": "新的API密钥"
        }
    }
}

update_hybrid_config(new_config)
```

### 错误重试机制

- WebSocket连接断开自动重连
- API发送失败自动重试（最多3次）
- 完善的异常处理和恢复

## 🎓 学习资源

### 下一步学习

1. **阅读代码**：查看 `examples/basic_usage.py` 学习更多用法
2. **理解架构**：阅读 `ARCHITECTURE.md` 了解技术原理
3. **故障排除**：保存本教程，遇到问题时参考

### 获取帮助

如果遇到问题：
1. 首先查看本教程的故障排除部分
2. 检查日志文件寻找错误信息
3. 加入OpenClaw社区寻求帮助

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**恭喜！** 🎉 你已经成功安装并配置了Hybrid QQ Messenger插件！

现在你可以：
- 🤖 让OpenClaw AI处理QQ消息
- 📤 主动发送消息给QQ好友
- 🔄 享受稳定可靠的消息服务

**维护者**: Plugin Author  
**版本**: 1.0.0  
**教程更新时间**: 2026-03-29