# 扩展功能文档

## 概述

Hybrid QQ Messenger 插件现在支持 AstrBot 的扩展功能，包括浏览器自动化和插件调用能力。

## 浏览器自动化 (Gull)

AstrBot 使用 "Gull" 组件提供容器化的浏览器自动化运行时。

### 核心端点

- **`/gull/exec`** - 执行单个浏览器命令
- **`/gull/exec_batch`** - 批量执行浏览器命令
- **`/gull/sandbox/create`** - 创建浏览器沙盒

### 支持的命令

```python
# 导航
await extended.navigate_to_url("https://example.com")

# 截图
await extended.take_screenshot()

# 元素操作
await extended.click_element("button.submit")
await extended.fill_form("input.name", "Alice")

# 数据提取
await extended.extract_text("h1.title")
```

### 沙盒管理

浏览器自动化支持沙盒隔离：

```python
# 创建沙盒
sandbox_result = await extended.create_sandbox("my-sandbox")
sandbox_id = sandbox_result['data']['sandbox_id']

# 在沙盒中执行命令
await extended.navigate_to_url("https://example.com", sandbox_id)
```

## 插件调用

### 获取插件列表

```python
plugins_result = await extended.get_available_plugins()
```

### 调用插件函数

```python
# 调用天气插件
result = await extended.call_plugin(
    "weather",
    "get_weather", 
    {"city": "Beijing"}
)

# 调用翻译插件
result = await extended.call_plugin(
    "translator",
    "translate_text",
    {"text": "Hello", "target_lang": "zh"}
)
```

## 配置要求

### AstrBot 版本

- **最低版本**: v4.18.0+
- **推荐版本**: 最新稳定版

### 服务要求

- AstrBot 服务运行在端口 6185
- 启用 API Key 认证
- 安装并启用相关插件

## 使用示例

### 基础浏览器自动化

```python
from adapters.astrbot_extended import AstrBotExtended
from config.manager import ConfigManager

config_manager = ConfigManager()
config = config_manager.load_config()
extended = AstrBotExtended(config)

# 导航并截图
await extended.navigate_to_url("https://example.com")
await extended.take_screenshot()
```

### 混合工作流

```python
# 1. 发送开始通知
await extended.send_message("开始自动化任务...")

# 2. 执行浏览器自动化
await extended.navigate_to_url("https://target-site.com")
data = await extended.extract_text(".content")

# 3. 发送结果
await extended.send_message(f"任务完成，获取数据: {data}")
```

### 批量操作

```python
# 批量执行命令
commands = [
    "navigate https://example.com",
    "wait 2000",
    "screenshot",
    "extract-text h1"
]

result = await extended.browser_execute_batch(commands)
```

## 错误处理

### 常见错误

- **连接失败**: AstrBot 服务未启动
- **认证失败**: API Key 无效
- **端点不存在**: 功能未启用或版本不支持
- **命令执行失败**: 浏览器操作错误

### 错误响应格式

```json
{
  "status": "error",
  "message": "错误描述",
  "error_details": "详细错误信息",
  "status_code": 404
}
```

## 最佳实践

### 性能优化

- **复用沙盒**: 在相同会话中复用沙盒 ID
- **批量操作**: 使用 `exec_batch` 减少请求次数
- **合理超时**: 设置适当的命令执行超时

### 错误恢复

- **重试机制**: 对临时性错误进行重试
- **降级策略**: 准备备用方案
- **状态检查**: 定期检查服务状态

### 安全性

- **沙盒隔离**: 使用沙盒进行任务隔离
- **权限控制**: 限制敏感操作
- **输入验证**: 验证所有用户输入

## 故障排除

### 浏览器自动化问题

**命令执行失败**
- 检查命令语法是否正确
- 验证页面元素选择器
- 确认页面加载完成

**沙盒创建失败**
- 检查 Gull 服务状态
- 验证沙盒名称唯一性
- 确认系统资源充足

### 插件调用问题

**插件不存在**
- 确认插件已安装并启用
- 检查插件名称拼写
- 验证 AstrBot 插件目录

**函数调用失败**
- 检查函数参数格式
- 验证插件权限设置
- 查看插件日志输出

### 连接问题

**API 连接失败**
- 确认 AstrBot 服务运行状态
- 检查防火墙和网络设置
- 验证端口 6185 可访问

---

**相关文档**:
- [AstrBot API 参考](ASTRBOT_API_REFERENCE.md)
- [快速开始指南](QUICK_START.md)
- [架构设计](ARCHITECTURE.md)

**版本**: 1.0.0  
**最后更新**: 2026-03-29