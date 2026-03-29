#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AstrBot Extended Adapter
Extended functionality for AstrBot API including browser automation and plugin calling
"""

import json
import logging
from typing import Dict, Any, Optional, List

import aiohttp


class AstrBotExtended:
    """AstrBot扩展功能适配器 - 支持浏览器自动化和插件调用"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize AstrBot extended adapter"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get AstrBot configuration
        astrbot_config = config.get('hybrid_mode', {}).get('sender', {})
        self.api_key = astrbot_config.get('api_key', '')
        
        # Browser automation endpoints (Gull)
        self.gull_base_url = "http://localhost:6185"  # AstrBot default port
        
        # Plugin calling endpoints
        self.plugin_base_url = "http://localhost:6185/api/v1"
    
    async def send_message(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Send message via AstrBot API (basic functionality)"""
        return await self._call_astrbot_api(
            endpoint="/api/v1/im/message",
            payload={
                "umo": f"default:FriendMessage:{self.config['hybrid_mode']['sender']['target_qq']}",
                "message": message,
                "session_id": session_id or ""
            }
        )
    
    async def browser_execute(self, command: str, sandbox_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute browser automation command via Gull
        
        Args:
            command: Browser automation command (without 'agent-browser' prefix)
            sandbox_id: Optional sandbox ID for session persistence
        
        Returns:
            Execution result
        """
        payload = {"command": command}
        if sandbox_id:
            payload["sandbox_id"] = sandbox_id
        
        return await self._call_astrbot_api(
            endpoint="/gull/exec",
            payload=payload
        )
    
    async def browser_execute_batch(self, commands: List[str], sandbox_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute multiple browser commands in batch
        
        Args:
            commands: List of browser automation commands
            sandbox_id: Optional sandbox ID for session persistence
        
        Returns:
            Batch execution result
        """
        payload = {"commands": commands}
        if sandbox_id:
            payload["sandbox_id"] = sandbox_id
        
        return await self._call_astrbot_api(
            endpoint="/gull/exec_batch",
            payload=payload
        )
    
    async def call_plugin(self, plugin_name: str, function_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call AstrBot plugin function
        
        Args:
            plugin_name: Name of the plugin to call
            function_name: Function within the plugin
            parameters: Parameters for the function call
        
        Returns:
            Plugin execution result
        """
        return await self._call_astrbot_api(
            endpoint=f"/plugins/{plugin_name}/{function_name}",
            payload=parameters
        )
    
    async def get_available_plugins(self) -> Dict[str, Any]:
        """Get list of available AstrBot plugins"""
        return await self._call_astrbot_api(
            endpoint="/plugins/list"
        )
    
    async def create_sandbox(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Create a new browser automation sandbox"""
        payload = {}
        if name:
            payload["name"] = name
        
        return await self._call_astrbot_api(
            endpoint="/gull/sandbox/create",
            payload=payload
        )
    
    async def _call_astrbot_api(self, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make API call to AstrBot"""
        headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        url = f"{self.gull_base_url}{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                if payload:
                    async with session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        return await self._handle_response(response)
                else:
                    async with session.get(
                        url,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:
                        return await self._handle_response(response)
                        
        except Exception as e:
            self.logger.error(f"AstrBot API call failed: {e}")
            return {
                'status': 'error',
                'message': f'API call failed: {e}'
            }
    
    async def _handle_response(self, response) -> Dict[str, Any]:
        """Handle API response"""
        if response.status == 200:
            response_data = await response.json()
            return {
                'status': 'ok',
                'data': response_data,
                'status_code': response.status
            }
        else:
            error_text = await response.text()
            return {
                'status': 'error',
                'message': f'API request failed: {response.status}',
                'error_details': error_text,
                'status_code': response.status
            }
    
    # Browser automation utility methods
    async def navigate_to_url(self, url: str, sandbox_id: Optional[str] = None) -> Dict[str, Any]:
        """Navigate to URL in browser"""
        return await self.browser_execute(f"navigate {url}", sandbox_id)
    
    async def take_screenshot(self, sandbox_id: Optional[str] = None) -> Dict[str, Any]:
        """Take screenshot of current page"""
        return await self.browser_execute("screenshot", sandbox_id)
    
    async def extract_text(self, selector: str, sandbox_id: Optional[str] = None) -> Dict[str, Any]:
        """Extract text from page element"""
        return await self.browser_execute(f"extract-text {selector}", sandbox_id)
    
    async def click_element(self, selector: str, sandbox_id: Optional[str] = None) -> Dict[str, Any]:
        """Click on page element"""
        return await self.browser_execute(f"click {selector}", sandbox_id)
    
    async def fill_form(self, selector: str, value: str, sandbox_id: Optional[str] = None) -> Dict[str, Any]:
        """Fill form field"""
        return await self.browser_execute(f"fill {selector} {value}", sandbox_id)


# Example usage
async def example_extended_usage():
    """示例扩展用法"""
    from config.manager import ConfigManager
    
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    extended = AstrBotExtended(config)
    
    # 1. 发送消息 (基础功能)
    result = await extended.send_message("测试消息")
    print(f"消息发送结果: {result}")
    
    # 2. 浏览器自动化
    nav_result = await extended.navigate_to_url("https://example.com")
    print(f"浏览器导航结果: {nav_result}")
    
    # 3. 插件调用 (如果AstrBot支持)
    try:
        plugin_result = await extended.call_plugin(
            "browser-plugin",
            "screenshot",
            {"full_page": True}
        )
        print(f"插件调用结果: {plugin_result}")
    except Exception as e:
        print(f"插件调用失败 (可能不支持): {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_extended_usage())