# Hybrid QQ Messenger - 快速入门指南

## 🚀 5分钟快速安装

### 步骤1: 检查环境
确保你有：
- ✅ OpenClaw 运行环境
- ✅ NapCat 服务（端口3001）
- ✅ AstrBot API 密钥
- ✅ Python 3.8+

### 步骤2: 安装依赖
```bash
pip install websockets aiohttp
```

### 步骤3: 复制插件
将整个 `hybrid-qq-messenger` 目录复制到：
```
YOUR_OPENCLAW_PLUGINS_PATH_HERE
```

### 步骤4: 配置OpenClaw
编辑 `openclaw.json`，在 `plugins` 部分添加：
```json
"allow": [
  "hybrid-qq-messenger"
],
"load": {
  "paths": [
    "YOUR_PLUGIN_PATH_HERE"
  ]
},
"entries": {
  "hybrid-qq-messenger": {
    "enabled": true
  }
}
```

### 步骤5: 配置OneBot通道
在 `channels` 部分添加：
```json
"onebot": {
  "type": "forward-websocket",
  "host": "127.0.0.1",
  "port": 3001,
  "accessToken": "",
  "path": "/onebot/v11/ws",
  "requireMention": true,
  "whitelistUserIds": [YOUR_QQ_NUMBER_HERE],
  "renderMarkdownToPlain": true
}
```

### 步骤6: 配置插件
编辑 `config.json`，设置：
```json
{
  "hybrid_mode": {
    "receiver": {
      "napcat_ws_url": "ws://localhost:3001",
      "enabled": true
    },
    "sender": {
      "api_url": "http://localhost:6185/api/v1/im/message",
      "api_key": "你的API密钥",
      "target_qq": "你的QQ号码",
      "enabled": true
    }
  }
}
```

### 步骤7: 重启OpenClaw
```bash
openclaw gateway restart
```

### 步骤8: 测试功能
```bash
cd "YOUR_OPENCLAW_PATH\plugins\hybrid-qq-messenger"
python quick_test.py
```

## 🧪 测试消息发送

### 简单测试
```python
from main import send_message
import asyncio

async def test():
    result = await send_message("测试消息 - 功能正常")
    print("发送结果:", result)

asyncio.run(test())
```

### 完整测试
```bash
python test_system.py
```

## 🔧 常见问题速查

### Q: NapCat连接失败
**A:** 检查：
1. NapCat是否运行：`netstat -an | findstr :3001`
2. 配置中的 `message_post_format: array`

### Q: AstrBot API错误
**A:** 检查：
1. API密钥是否正确
2. 目标QQ号码配置
3. AstrBot服务状态

### Q: 插件不加载
**A:** 检查：
1. 插件是否在allow列表中
2. 插件路径是否正确
3. 重启OpenClaw

## 📞 获取帮助

如果遇到问题：
1. 查看详细文档：`README_CN.md`
2. 检查日志文件
3. 加入OpenClaw社区

---

**恭喜！** 你现在已经成功安装并配置了Hybrid QQ Messenger插件！

开始享受稳定可靠的QQ消息处理能力吧！ 🎉