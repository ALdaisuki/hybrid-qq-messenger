# Hybrid QQ Messenger Plugin - Complete Beginner's Guide

> **Hybrid Architecture QQ Messaging Plugin** - Complete tutorial designed for OpenClaw beginners

## 🎯 What Does This Plugin Do?

If you want OpenClaw to be able to:
- 📱 **Receive QQ Messages** - Receive messages from QQ friends or groups via NapCat service
- 📤 **Send QQ Messages** - Proactively send messages to QQ friends via AstrBot service
- 🧠 **Smart Conversations** - Let OpenClaw AI naturally handle QQ conversations
- 🔄 **Stable & Reliable** - Separate receiving and sending paths to ensure uninterrupted service

Then this plugin is for you!

## 🏗️ Architecture Explained (Simple Terms)

Think of this plugin like a smart post office:

```
📮 Receiving Mailbox (NapCat) → 📦 Processing Center (Plugin) → 🤖 AI Assistant (OpenClaw)
                                            ↓
📤 Sending Mailbox (AstrBot) → 📱 QQ Friends
```

- **Receiver**: NapCat is like your QQ mailbox, specifically for receiving messages
- **Sender**: AstrBot is like a courier, specifically for sending messages
- **Plugin**: Like a post office, coordinating receiving and sending
- **AI**: Like a smart assistant, processing received messages

## 📋 Pre-installation Checklist

### Required Services
- ✅ **OpenClaw** - Installed and running normally
- ✅ **NapCat** - QQ bot service, running on port 3001
- ✅ **AstrBot** - Message sending service, running on port 6185

### Required Information
- 🔑 **AstrBot API Key** - Obtained from AstrBot service
- 📱 **Your QQ Number** - Target for sending messages
- 🖥️ **Basic Command Line Skills** - Know how to use terminal/command prompt

## 🚀 Complete Installation Tutorial (Step by Step)

### Step 1: Check Python Environment

Open terminal (Windows: Win+R, type cmd, press Enter), run:

```bash
python --version
```

Should show `Python 3.8` or higher. If not, install Python first.

### Step 2: Install Python Dependencies

In terminal, run:

```bash
pip install websockets aiohttp
```

**What is this?**
- `websockets` - Allows plugin to connect to NapCat's WebSocket
- `aiohttp` - Allows plugin to call AstrBot's API

### Step 3: Copy Plugin Files

1. Find your OpenClaw installation directory (usually `YOUR_OPENCLAW_PATH`)
2. Go to `plugins` folder
3. Copy the entire `hybrid-qq-messenger` folder here

**Final path should be:**
```
YOUR_OPENCLAW_PATH\plugins\hybrid-qq-messenger\
```

### Step 4: Configure NapCat (Important!)

Find your NapCat configuration file, usually at:
```
napcat/config/onebot11_your_qq_number.json
```

Open this file with a text editor, make sure it contains:

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

**Special Note:** `message_post_format` must be set to `"array"`, otherwise messages won't be received correctly!

### Step 5: Configure OpenClaw

Find OpenClaw configuration file:
```
YOUR_OPENCLAW_PATH\openclaw.json
```

Open with text editor, find `plugins` section, add this configuration:

```json
{
  "plugins": {
    "allow": [
      "memory-lancedb-pro",
      "google", 
      "openclaw-onebot",
      "hybrid-qq-messenger"  // Add this line
    ],
    "load": {
      "paths": [
        "YOUR_OPENCLAW_PATH\\\\plugins\\\\memory-lancedb-pro",
        "YOUR_OPENCLAW_PATH\\\\plugins\\\\hybrid-qq-messenger"  // Add this line
      ]
    },
    "entries": {
      "hybrid-qq-messenger": {
        "enabled": true  // Add this section
      }
    }
  }
}
```

Then in the same file, find `channels` section, add:

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
      "whitelistUserIds": [YOUR_QQ_NUMBER_HERE],  // Change to your QQ number
      "renderMarkdownToPlain": true,
      "normalModeFlushIntervalMs": 1200,
      "normalModeFlushChars": 160
    }
  }
}
```

### Step 6: Configure Plugin

Open plugin configuration file:
```
YOUR_OPENCLAW_PATH\plugins\hybrid-qq-messenger\config.json
```

Modify to this content:

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
      "api_key": "YOUR_ASTRBOT_API_KEY_HERE",  // Change to your real API key
      "enabled": true,
      "target_qq": "YOUR_QQ_NUMBER_HERE",  // Change to your QQ number
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

**Important Changes:**
- `api_key`: Change to your real API key from AstrBot
- `target_qq`: Change to your QQ number (e.g., YOUR_QQ_NUMBER_HERE)

### Step 7: Restart OpenClaw

In terminal, run:

```bash
openclaw gateway restart
```

Wait for OpenClaw to restart, this may take a few seconds.

## 🧪 Verify Installation (Make Sure Everything Works)

### Method 1: Run Installation Check

Open terminal, go to plugin directory:

```bash
cd "YOUR_PLUGIN_PATH_HERE"
python check_installation.py
```

If all checks show ✅, installation is correct!

### Method 2: Test Message Sending

In the same directory, run:

```bash
python -c "
import asyncio
from main import send_message

async def test():
    result = await send_message('Test message - Installation verification')
    print('Send result:', result)

asyncio.run(test())
"
```

If you see `Send result: {'status': 'ok'}`, message sent successfully!

### Method 3: Test Complete Functionality

```bash
python test_system.py
```

This script tests all components to ensure the entire system works properly.

## 💡 How to Use the Plugin

### Basic Usage (Automatic Mode)

After plugin starts, it works automatically:

1. **Receive Messages**: When QQ friends send messages, OpenClaw AI automatically processes them
2. **Smart Replies**: AI decides whether to reply based on conversation context
3. **Send Messages**: You can proactively send messages through code

### Send Proactive Messages

Create a Python file `send_message.py`:

```python
import asyncio
from main import send_message

async def main():
    # Send simple message
    result = await send_message("Hello! This is a test message")
    
    if result.get('status') == 'ok':
        print("🎉 Message sent successfully!")
    else:
        print(f"❌ Send failed: {result.get('message')}")

# Run send function
asyncio.run(main())
```

Save and run:
```bash
python send_message.py
```

### Send to Specific Sessions

If you want to send to specific QQ friends or groups:

```python
# Send to specific friend (private chat)
result = await send_message("Private message", session_id="private_123456789")

# Send to group chat
result = await send_message("Group message", session_id="group_987654321")
```

**session_id format:**
- Private chat: `private_QQ_number`
- Group chat: `group_group_number`

## 🔧 Configuration Details (What Each Parameter Does)

### Receiver Configuration

```json
"receiver": {
  "napcat_ws_url": "ws://localhost:3001",  // NapCat WebSocket address
  "enabled": true,                          // Enable receiving function
  "auto_reconnect": true,                   // Auto reconnect when disconnected
  "reconnect_delay": 5                      // Reconnect wait time (seconds)
}
```

### Sender Configuration

```json
"sender": {
  "api_url": "http://localhost:6185/api/v1/im/message",  // AstrBot API address
  "api_key": "your-api-key",                 // AstrBot API key (required)
  "target_qq": "your-qq-number",             // Default send target (required)
  "enabled": true,                                      // Enable sending function
  "retry_count": 3,                                     // Send failure retry count
  "retry_delay": 2                                      // Retry interval (seconds)
}
```

### Routing Configuration

```json
"routing": {
  "auto_switch": true,           // Auto switch between receive and send
  "fallback_to_astrbot": true,   // Use AstrBot for sending when receive fails
  "session_timeout": 300,        // Session timeout time (5 minutes)
  "max_message_length": 1000     // Maximum message length
}
```

## 🚨 Common Problem Solving

### Problem 1: NapCat Connection Failure

**Symptoms:** See "no config, service will not connect" in OpenClaw logs

**Solution Steps:**
1. Check if NapCat is running:
   ```bash
   netstat -an | findstr :3001
   ```
   Should see `LISTENING` status

2. Check if `message_post_format` in NapCat config is `"array"`

3. Check if host and port in OpenClaw configuration are correct

### Problem 2: AstrBot API Error

**Symptoms:** Returns "API request failed: 405" when sending messages

**Solution Steps:**
1. Check if API key is correct
2. Check target QQ number configuration
3. Check if AstrBot service is running:
   ```bash
   curl -H "X-API-Key: your-api-key" http://localhost:6185/api/v1/im/status
   ```

### Problem 3: Plugin Not Loading

**Symptoms:** See "plugin not found" in OpenClaw logs

**Solution Steps:**
1. Check if plugin is in `allow` list
2. Check if plugin path is correct
3. Restart OpenClaw: `openclaw gateway restart`

### Problem 4: Message Sent Successfully But Not Received

**Solution Steps:**
1. Check if target QQ number is correct
2. Check AstrBot service logs
3. Confirm QQ client network connection is normal

## 📊 Monitoring and Logs

### View OpenClaw Logs

```bash
openclaw logs
```

### View Plugin Logs

Plugin log file at:
```
YOUR_OPENCLAW_PATH\plugins\hybrid-qq-messenger\logs\hybrid-messenger.log
```

### Check Service Status

```bash
# Check NapCat
netstat -an | findstr :3001

# Check AstrBot  
curl -H "X-API-Key: your-api-key" http://localhost:6185/api/v1/im/status
```

## 🔄 Advanced Features

### Session Management

Plugin automatically manages conversation sessions:
- Each QQ friend or group has independent session
- Sessions automatically cleaned after 5 minutes of inactivity
- Maintains history of last 50 messages

### Configuration Hot Updates

You can update configuration at runtime:

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

### Error Retry Mechanism

- WebSocket connection auto-reconnects when disconnected
- API send failures auto-retry (up to 3 times)
- Comprehensive exception handling and recovery

## 🎓 Learning Resources

### Next Steps to Learn

1. **Read Code**: Check `examples/basic_usage.py` to learn more usage
2. **Understand Architecture**: Read `ARCHITECTURE.md` to understand technical principles
3. **Troubleshooting**: Save this tutorial for reference when encountering problems

### Getting Help

If you encounter problems:
1. First check the troubleshooting section of this tutorial
2. Check log files for error information
3. Join OpenClaw community for help

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

**Congratulations!** 🎉 You have successfully installed and configured the Hybrid QQ Messenger plugin!

Now you can:
- 🤖 Let OpenClaw AI handle QQ messages
- 📤 Proactively send messages to QQ friends
- 🔄 Enjoy stable and reliable messaging service

**Maintainer**: Plugin Author  
**Version**: 1.0.0  
**Tutorial Update Time**: 2026-03-29