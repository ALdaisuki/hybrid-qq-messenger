# Hybrid QQ Messenger Plugin

> **Hybrid Architecture for QQ Messaging** - Complete solution for OpenClaw QQ integration

## 🎯 Quick Overview

This plugin enables OpenClaw to:
- 📱 **Receive QQ Messages** via NapCat WebSocket
- 📤 **Send QQ Messages** via AstrBot API
- 🧠 **Process Conversations** naturally with OpenClaw AI
- 🔄 **Reliable Architecture** with separate receive/send paths

## 📚 Documentation

### 📖 Documentation Index
- 🔗 **[Documentation Index](docs/INDEX.md)** - Complete documentation catalog and learning paths

### For Beginners
- 📖 **[Complete Beginner's Guide](docs/README_DETAILED.md)** - Step-by-step installation and usage
- 🚀 **[Quick Start Guide](docs/QUICK_START.md)** - 5-minute installation
- 🔍 **[Installation Check](check_installation.py)** - Verify your setup

### For Chinese Users
- 📖 **[中文详细教程](docs/README_CN_DETAILED.md)** - 完整的中文安装和使用指南
- 🚀 **[快速入门](docs/QUICK_START.md)** - 5分钟快速安装

### Technical Documentation
- 🏗️ **[Architecture](docs/ARCHITECTURE.md)** - Technical design and principles
- 🎯 **[Skill Definition](SKILL.md)** - OpenClaw skill configuration
- 📊 **[Status Report](docs/STATUS_REPORT.md)** - Current system status

## 🚀 Quick Installation

### 1. Install Dependencies
```bash
pip install websockets aiohttp
```

### 2. Copy Plugin
Copy the `hybrid-qq-messenger` folder to your OpenClaw plugins directory.

### 3. Configure Services
- **NapCat**: Ensure WebSocket running on port 3001
- **AstrBot**: Configure API key and target QQ

### 4. Verify Installation
```bash
cd "J:\Alice\openclaw\plugins\hybrid-qq-messenger"
python check_installation.py
```

## 💡 Quick Usage

### Send Messages
```python
from main import send_message

# Send simple message
result = await send_message("Hello from OpenClaw!")

# Send to specific session
result = await send_message("Session message", session_id="private_123456789")
```

## 📁 Project Structure

```
hybrid-qq-messenger/
├── core/           # Core business logic
├── adapters/       # External service adapters
├── services/       # Business services
├── config/         # Configuration management
├── models/         # Data models
├── examples/       # Usage examples
├── tests/          # Test suite
└── docs/           # Documentation files
```

## 🔧 Key Features

- **Dual-Path Architecture** - Separate receiving and sending
- **Natural Conversation** - AI processes messages naturally
- **Session Management** - Intelligent conversation tracking
- **Reliable Delivery** - Retry mechanisms and error handling
- **Configuration Driven** - Flexible JSON configuration

## 📞 Support

### Getting Help
1. Check the **[detailed documentation](docs/README_DETAILED.md)**
2. Run the **[installation check](check_installation.py)**
3. Join the OpenClaw community

### Common Issues
- **Connection Problems**: Check service status and configuration
- **API Errors**: Verify API keys and target QQ numbers
- **Plugin Loading**: Check OpenClaw configuration

## 🏗️ Project Overview

- 📊 **[Project Overview](PROJECT_OVERVIEW.md)** - Complete project structure and technical details
- 🙏 **[Acknowledgements](ACKNOWLEDGEMENTS.md)** - Thanks to frameworks and contributors

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

**Maintainer**: Alice  
**Version**: 1.0.0  
**Status**: Production Ready

## 🤝 Community & Support

- 📖 **Documentation**: Complete beginner-friendly tutorials
- 🔧 **Tools**: Installation check and testing scripts
- 🐛 **Issues**: Report bugs and request features
- 💡 **Contributions**: Welcome code, docs, and testing contributions