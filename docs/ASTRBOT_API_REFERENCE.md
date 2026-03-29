# AstrBot API 参考文档

## 概述

AstrBot是一个支持API Key认证的QQ机器人框架，从v4.18.0开始提供HTTP API接口。本插件使用AstrBot API进行消息发送。

## 认证方式

### API Key生成

1. 打开AstrBot WebUI
2. 进入设置界面
3. 创建新的API密钥

### 认证头

支持两种认证方式：

```http
# 方式1: X-API-Key头
X-API-Key: YOUR_ASTRBOT_API_KEY_HERE

# 方式2: Bearer Token
Authorization: Bearer YOUR_ASTRBOT_API_KEY_HERE
```

## 消息发送端点

### 基本信息

- **URL**: `http://localhost:6185/api/v1/im/message`
- **方法**: POST
- **内容类型**: `application/json`

### 请求格式

```json
{
  "umo": "default:FriendMessage:YOUR_QQ_NUMBER_HERE",
  "message": "消息内容",
  "session_id": "optional_session_identifier"
}
```

### UMO格式说明

UMO (Universal Message Object) 用于指定消息类型和目标：

| 消息类型 | UMO格式 | 说明 |
|----------|---------|------|
| 好友消息 | `default:FriendMessage:QQ_NUMBER` | 发送给指定QQ好友 |
| 群组消息 | `default:GroupMessage:GROUP_ID` | 发送到指定QQ群 |
| 临时消息 | `default:TempMessage:GROUP_ID` | 发送临时消息 |

### 响应格式

```json
{
  "status": "ok",
  "data": {
    "status": "ok",
    "message": null,
    "data": {}
  },
  "umo": "default:FriendMessage:YOUR_QQ_NUMBER_HERE"
}
```

## 错误处理

### 常见错误状态

- **401 Unauthorized**: API密钥无效或缺失
- **400 Bad Request**: 请求格式错误
- **404 Not Found**: 端点不存在
- **500 Internal Server Error**: AstrBot服务内部错误

### 错误响应示例

```json
{
  "status": "error",
  "message": "API request failed: 401"
}
```

## 使用示例

### cURL示例

```bash
# 使用X-API-Key头
curl -X POST \
  http://localhost:6185/api/v1/im/message \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: YOUR_ASTRBOT_API_KEY_HERE' \
  -d '{
    "umo": "default:FriendMessage:YOUR_QQ_NUMBER_HERE",
    "message": "Hello from AstrBot API"
  }'

# 使用Bearer Token
curl -X POST \
  http://localhost:6185/api/v1/im/message \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_ASTRBOT_API_KEY_HERE' \
  -d '{
    "umo": "default:FriendMessage:YOUR_QQ_NUMBER_HERE",
    "message": "Hello from AstrBot API"
  }'
```

### Python示例

```python
import aiohttp
import asyncio

async def send_astrbot_message():
    headers = {
        'X-API-Key': 'YOUR_ASTRBOT_API_KEY_HERE',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "umo": "default:FriendMessage:YOUR_QQ_NUMBER_HERE",
        "message": "测试消息"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:6185/api/v1/im/message',
            headers=headers,
            json=payload
        ) as response:
            if response.status == 200:
                result = await response.json()
                print(f"发送成功: {result}")
            else:
                print(f"发送失败: {response.status}")

# 运行示例
asyncio.run(send_astrbot_message())
```

## 配置说明

### 插件配置

在 `config.json` 中的发送器配置：

```json
{
  "hybrid_mode": {
    "sender": {
      "type": "astrbot-api",
      "api_url": "http://localhost:6185/api/v1/im/message",
      "api_key": "YOUR_ASTRBOT_API_KEY_HERE",
      "target_qq": "YOUR_QQ_NUMBER_HERE",
      "enabled": true,
      "retry_count": 3,
      "retry_delay": 2
    }
  }
}
```

## 最佳实践

### 安全性

- **保护API密钥**: 不要在代码中硬编码API密钥
- **使用环境变量**: 通过环境变量传递敏感信息
- **最小权限**: 仅授予必要的API权限

### 性能

- **连接池**: 复用HTTP连接
- **超时设置**: 设置合理的请求超时
- **重试机制**: 实现指数退避重试

### 错误处理

- **重试策略**: 对临时性错误进行重试
- **降级方案**: 准备备用消息发送方案
- **监控告警**: 监控API可用性和性能

## 故障排除

### 连接问题

- **检查服务状态**: 确认AstrBot服务正在运行
- **验证端口**: 确认6185端口可访问
- **检查防火墙**: 确保防火墙未阻止连接

### 认证问题

- **验证API密钥**: 确认密钥正确且未过期
- **检查权限**: 确认API密钥有发送消息权限
- **测试连接**: 使用cURL测试基本连接

### 消息发送问题

- **验证UMO格式**: 确认UMO格式正确
- **检查目标QQ**: 确认目标QQ号有效
- **查看日志**: 检查AstrBot服务日志

---

**参考文档**: 
- [AstrBot官方文档](https://docs.astrbot.app/)
- [OpenAPI规范](https://docs.astrbot.app/scalar.html)

**版本**: 1.0.0  
**最后更新**: 2026-03-29