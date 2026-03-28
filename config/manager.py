#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Manager
Handles plugin configuration loading, validation, and updates
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


class ConfigManager:
    """Configuration management class"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize config manager"""
        if config_path is None:
            self.config_path = Path(__file__).parent.parent / "config.json"
        else:
            self.config_path = Path(config_path)
        
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("Config file not found, using default config")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            return self.get_default_config()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Save configuration to file"""
        if config is not None:
            self.config = config
        
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            self.logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            return False
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "hybrid_mode": {
                "receiver": {
                    "type": "openclaw-onebot",
                    "napcat_ws_url": "ws://localhost:3001",
                    "enabled": True,
                    "access_token": "",
                    "auto_reconnect": True,
                    "reconnect_delay": 5
                },
                "sender": {
                    "type": "astrbot-api",
                    "api_url": "http://localhost:6185/api/v1/im/message",
                    "api_key": "",
                    "enabled": True,
                    "target_qq": "",
                    "retry_count": 3,
                    "retry_delay": 2
                },
                "routing": {
                    "auto_switch": True,
                    "fallback_to_astrbot": True,
                    "session_timeout": 300,
                    "max_message_length": 1000
                },
                "enabled": True
            },
            "logging": {
                "level": "INFO",
                "file": "logs/hybrid-messenger.log",
                "max_size_mb": 10
            }
        }
    
    def update_config(self, new_config: Dict[str, Any]) -> bool:
        """Update configuration with new values"""
        # Deep merge config
        self._deep_merge(self.config, new_config)
        return self.save_config()
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Deep merge two dictionaries"""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def validate_config(self, config: Optional[Dict[str, Any]] = None) -> Tuple[bool, list]:
        """Validate configuration"""
        if config is None:
            config = self.config
        
        errors = []
        
        # Check required fields
        if not config.get('hybrid_mode', {}).get('receiver', {}).get('napcat_ws_url'):
            errors.append("Missing napcat_ws_url in receiver config")
        
        sender_config = config.get('hybrid_mode', {}).get('sender', {})
        if not sender_config.get('api_key'):
            errors.append("Missing api_key in sender config")
        if not sender_config.get('target_qq'):
            errors.append("Missing target_qq in sender config")
        
        return len(errors) == 0, errors


# Global functions for easy access
def get_hybrid_config() -> Dict[str, Any]:
    """Get current hybrid configuration"""
    manager = ConfigManager()
    return manager.config


def update_hybrid_config(new_config: Dict[str, Any]) -> bool:
    """Update hybrid configuration"""
    manager = ConfigManager()
    return manager.update_config(new_config)


def validate_hybrid_config(config: Optional[Dict[str, Any]] = None) -> Tuple[bool, list]:
    """Validate hybrid configuration"""
    manager = ConfigManager()
    return manager.validate_config(config)