---
name: hybrid-qq-messenger
description: |
  Hybrid QQ消息插件 - 结合NapCat接收和AstrBot发送的混合架构
  提供稳定的QQ消息接收和可靠的主动消息推送功能
  专为个人AI助手和开发者工具场景设计，适合OpenClaw初学者使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Exec
  - Process
  - Message
  - Browser
metadata:
  trigger: QQ消息处理、主动消息发送、混合消息架构、NapCat、AstrBot、QQ机器人
  category: messaging
  version: 1.0.0
  author: Alice
  status: production-ready
  dependencies:
    - websockets
    - aiohttp
  difficulty: beginner
  estimated-setup-time: 15分钟
---

# Hybrid QQ Messenger Skill

## 🎯 技能概述

本技能提供完整的QQ消息处理能力，采用分离架构确保最高可靠性：

- **接收端**: 通过NapCat + OneBot v11 WebSocket接收QQ消息
- **发送端**: 通过AstrBot REST API发送主动消息
- **会话管理**: 智能会话跟踪和上下文管理
- **自然对话**: OpenClaw AI处理消息，保持自然对话流程

## 🏗️ 技术架构

### 核心设计原则

1. **分离架构**: 接收和发送路径完全独立，避免单点故障
2. **自然处理**: 接收的消息由OpenClaw AI自然处理，不强制响应
3. **可靠发送**: 主动消息通过AstrBot API可靠推送
4. **配置驱动**: JSON配置支持实时调整和灵活部署

### 消息处理流程

```
接收路径: NapCat → WebSocket → OpenClaw AI (自然对话)
发送路径: Plugin → AstrBot API → QQ消息推送
```

## 📋 使用场景

### 个人AI助手
- **智能对话**: 接收用户QQ消息并由OpenClaw AI智能回复
- **主动通知**: 发送提醒、更新和重要通知
- **会话管理**: 保持对话上下文和用户状态

### 开发者工具
- **系统监控**: 监控系统状态并发送通知
- **调试支持**: 发送调试信息和状态报告
- **工作流集成**: 集成到开发工作流中

## 🔧 配置说明

### NapCat配置要求

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

### 插件配置 (`config.json`)

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
      "api_key": "your-api-key",
      "target_qq": "123456789",
      "enabled": true
    }
  }
}
```

## 💡 使用方法

### 发送主动消息

```python
from main import send_message

# 发送主动消息
result = await send_message("这是一条主动消息")

# 发送到特定会话
result = await send_message("会话特定消息", session_id="private_3364897325")

# 检查发送结果
if result.get('status') == 'ok':
    print("消息发送成功")
else:
    print(f"发送失败: {result.get('message')}")
```

### 获取插件状态

```python
from core.plugin import HybridQQMessenger

# 创建插件实例
plugin = HybridQQMessenger()

# 检查配置状态
config = plugin.config_manager.load_config()
print(f"接收端启用: {config['hybrid_mode']['receiver']['enabled']}")
print(f"发送端启用: {config['hybrid_mode']['sender']['enabled']}")
```

## 🚨 故障排除

### 常见问题

**接收端连接失败**
- 检查NapCat服务是否正常运行
- 验证WebSocket URL和端口配置
- 确认OneBot配置中的 `message_post_format: array`

**发送端API错误**
- 验证AstrBot API密钥是否正确
- 检查目标QQ号码配置
- 确认AstrBot服务可用性

**插件加载失败**
- 检查OpenClaw插件配置
- 验证依赖包是否安装
- 查看OpenClaw系统日志

### 日志分析

插件提供详细的日志输出：

- **INFO级别**: 连接状态、消息处理、会话更新
- **DEBUG级别**: 详细的消息处理流程
- **ERROR级别**: 连接错误、API失败、配置问题

## 🔄 会话管理

### 会话生命周期

1. **创建**: 收到第一条消息时自动创建会话
2. **更新**: 每次新消息更新会话活动时间
3. **超时**: 5分钟无活动自动清理会话
4. **清理**: 定期清理过期会话释放资源

### 会话上下文

插件维护最近50条消息的历史记录，为OpenClaw AI提供对话上下文。

## 📊 性能特性

- **连接重试**: 自动重连机制确保服务连续性
- **消息重试**: 发送失败时自动重试(最多3次)
- **会话优化**: 智能会话管理避免内存泄漏
- **错误处理**: 完善的异常处理和恢复机制

## 🔮 扩展能力

### 自定义适配器

插件采用适配器模式，支持扩展新的消息平台：

```python
from adapters.base import MessageAdapter

class CustomAdapter(MessageAdapter):
    async def send_message(self, message: str, session_id: str = None):
        # 自定义发送逻辑
        pass
```

### 配置热更新

支持运行时配置更新：

```python
from config.manager import update_hybrid_config

new_config = {
    "hybrid_mode": {
        "sender": {
            "api_key": "new-api-key"
        }
    }
}

update_hybrid_config(new_config)
```

## 🎓 初学者指南

### 快速开始步骤

1. **安装依赖**: `pip install websockets aiohttp`
2. **复制插件**: 将插件目录复制到OpenClaw插件目录
3. **配置NapCat**: 确保NapCat运行在端口3001
4. **配置AstrBot**: 获取API密钥并配置目标QQ
5. **重启OpenClaw**: 应用配置更改
6. **测试发送**: 使用示例代码测试消息发送

### 验证安装

运行以下命令验证安装：

```bash
cd "J:\Alice\openclaw\plugins\hybrid-qq-messenger"
python quick_test.py
```

### 第一次使用

1. 发送测试消息确认功能正常
2. 通过QQ向机器人发送消息测试接收
3. 检查日志确认无错误信息
4. 开始正常使用

---

**注意**: 本技能需要NapCat和AstrBot服务正常运行。请确保相关服务已正确配置和启动。

**版本**: 1.0.0  
**状态**: 生产就绪  
**难度**: 初学者友好  
**最后更新**: 2026-03-29