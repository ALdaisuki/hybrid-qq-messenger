#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Management Service
Handles conversation session state and context tracking
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional
from collections import defaultdict


class SessionManager:
    """会话管理服务"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize session manager"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get session configuration
        routing_config = config.get('hybrid_mode', {}).get('routing', {})
        self.session_timeout = routing_config.get('session_timeout', 300)  # 5 minutes
        self.max_message_length = routing_config.get('max_message_length', 1000)
        
        # Session storage
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timestamps: Dict[str, float] = {}
        
        # Start cleanup task
        self.cleanup_task = asyncio.create_task(self._cleanup_expired_sessions())
    
    async def update_session(self, session_id: str, message_data: Dict[str, Any]):
        """Update session with new message"""
        try:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'messages': [],
                    'user_id': message_data.get('user_id'),
                    'group_id': message_data.get('group_id'),
                    'message_type': message_data.get('message_type'),
                    'created_at': time.time(),
                    'last_activity': time.time()
                }
            
            # Add message to session
            self.sessions[session_id]['messages'].append({
                'content': message_data.get('content', ''),
                'timestamp': message_data.get('timestamp', time.time()),
                'message_id': message_data.get('message_id')
            })
            
            # Update last activity
            self.sessions[session_id]['last_activity'] = time.time()
            self.session_timestamps[session_id] = time.time()
            
            # Limit message history
            max_messages = 50  # Keep last 50 messages
            if len(self.sessions[session_id]['messages']) > max_messages:
                self.sessions[session_id]['messages'] = self.sessions[session_id]['messages'][-max_messages:]
            
            self.logger.debug(f"Session {session_id} updated")
            
        except Exception as e:
            self.logger.error(f"Error updating session {session_id}: {e}")
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        session = self.sessions.get(session_id)
        
        if session and time.time() - session['last_activity'] <= self.session_timeout:
            # Update last activity
            session['last_activity'] = time.time()
            return session
        
        return None
    
    async def get_session_context(self, session_id: str, max_messages: int = 10) -> str:
        """Get conversation context for session"""
        session = await self.get_session(session_id)
        
        if not session:
            return ""
        
        # Get recent messages
        recent_messages = session['messages'][-max_messages:]
        
        # Build context string
        context_lines = []
        for msg in recent_messages:
            context_lines.append(f"User: {msg['content']}")
        
        return "\n".join(context_lines)
    
    async def end_session(self, session_id: str):
        """End session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_timestamps:
            del self.session_timestamps[session_id]
        
        self.logger.info(f"Session {session_id} ended")
    
    async def _cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        while True:
            try:
                current_time = time.time()
                expired_sessions = []
                
                for session_id, session in self.sessions.items():
                    if current_time - session['last_activity'] > self.session_timeout:
                        expired_sessions.append(session_id)
                
                for session_id in expired_sessions:
                    await self.end_session(session_id)
                
                if expired_sessions:
                    self.logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
                
                # Wait before next cleanup
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in session cleanup: {e}")
                await asyncio.sleep(60)
    
    async def stop(self):
        """Stop session manager"""
        self.cleanup_task.cancel()
        try:
            await self.cleanup_task
        except asyncio.CancelledError:
            pass
        
        self.logger.info("Session manager stopped")