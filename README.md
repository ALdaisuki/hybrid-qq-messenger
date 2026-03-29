# Hybrid QQ Messenger Plugin

[![OpenClaw Plugin](https://img.shields.io/badge/OpenClaw-Plugin-blue)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A hybrid architecture QQ messaging plugin for OpenClaw that combines the stability of NapCat for message reception with the reliability of AstrBot for proactive message sending.

## 🎯 Features

- **Hybrid Architecture**: Separate message reception (NapCat) and sending (AstrBot) for maximum reliability
- **File Support**: Send text files, images, audio, and video attachments
- **Smart Conversations**: Natural AI-powered QQ conversations
- **Session Management**: Automatic session creation and cleanup
- **Error Recovery**: Automatic reconnection and retry mechanisms
- **Skill Integration**: Automatic skill installation for seamless OpenClaw integration

## 🏗️ Architecture

```
NapCat (WebSocket) → OpenClaw AI → AstrBot (REST API)
     ↑                                   ↓
Message Reception                   Proactive Sending
```

## 📋 Requirements

- **OpenClaw**: Latest version with plugin support
- **NapCat**: Running on port 3001 with OneBot v11 support
- **AstrBot**: Running on port 6185 with API key enabled
- **Python**: 3.8+ with aiohttp library

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/hybrid-qq-messenger.git
cd hybrid-qq-messenger
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure OpenClaw
Add to your `openclaw.json`:

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

### 4. Configure Plugin
Edit `config.json`:

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

### 5. Restart OpenClaw
```bash
# Restart OpenClaw to load the plugin
openclaw restart
```

## 💡 Usage

### In OpenClaw Environment
```python
from main import send_message

# Send text message
await send_message("Hello from Hybrid QQ Messenger!")

# Send file (automatically handles upload and attachment)
await send_message_with_file("Check this file!", "path/to/file.txt")
```

### Command Line Testing
```bash
# Test basic functionality
python tests/quick_test.py

# Test complete system
python tests/test_system.py

# Check installation
python tests/check_installation.py
```

## 📁 Project Structure

```
hybrid-qq-messenger/
├── adapters/           # Message adapters (NapCat, AstrBot)
├── config/            # Configuration management
├── core/              # Core plugin logic
├── docs/              # Comprehensive documentation
├── examples/          # Usage examples
├── models/            # Data models
├── services/          # Background services
├── skills/            # OpenClaw skill integration
├── tests/             # Test suite
├── utils/             # Utility functions
├── config.json        # Plugin configuration
├── main.py           # Plugin entry point
├── openclaw.plugin.json  # OpenClaw plugin manifest
└── README.md         # This file
```

## 🧪 Testing

### Quick Test
```bash
python tests/quick_test.py
```

### Full System Test
```bash
python tests/test_system.py
```

### Installation Check
```bash
python tests/check_installation.py
```

## 📚 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get started quickly
- **[Detailed Tutorial](docs/README_DETAILED.md)** - Complete setup guide
- **[Architecture Overview](docs/ARCHITECTURE.md)** - Technical deep dive
- **[AstrBot API Reference](docs/ASTRBOT_API_REFERENCE.md)** - Complete API documentation
- **[Extended Features](docs/EXTENDED_FEATURES.md)** - Advanced capabilities

## 🔧 Troubleshooting

### Common Issues

**NapCat Connection Failed**
- Verify NapCat is running on port 3001
- Check WebSocket URL in config.json
- Ensure OneBot v11 compatibility

**AstrBot API Errors**
- Validate API key permissions
- Check target QQ number format
- Verify AstrBot service status

**Plugin Not Loading**
- Confirm plugin path in openclaw.json
- Check OpenClaw logs for errors
- Verify Python dependencies

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [OpenClaw](https://openclaw.ai) - The amazing AI assistant platform
- [NapCat](https://napcat.org) - Reliable QQ robot framework
- [AstrBot](https://astrbot.app) - Powerful AI chatbot platform
- [OneBot](https://onebot.dev) - Universal bot protocol

---

**Note**: Replace `YOUR_USERNAME`, `YOUR_OPENCLAW_PATH`, `YOUR_ASTRBOT_API_KEY_HERE`, and `YOUR_QQ_NUMBER_HERE` with your actual values before deployment.