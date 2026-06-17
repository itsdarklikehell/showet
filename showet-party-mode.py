#!/usr/bin/env python3
"""
Showet Party Mode Server
WebSocket server for synchronized demo playback across multiple devices
"""

import asyncio
import json
from websockets.server import serve
from datetime import datetime
from typing import Dict, Set

class PartyModeServer:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.clients: Dict[str, Set[str]] = {}
    
    async def register_client(self, session_id: str, client_id: str):
        if session_id not in self.clients:
            self.clients[session_id] = set()
        self.clients[session_id].add(client_id)
    
    async def unregister_client(self, session_id: str, client_id: str):
        if session_id in self.clients:
            self.clients[session_id].discard(client_id)
            if not self.clients[session_id]:
                del self.clients[session_id]
    
    async def handle_message(self, session_id: str, client_id: str, data: dict):
        msg_type = data.get('type')
        
        if msg_type == 'join':
            await self.register_client(session_id, client_id)
            await self.broadcast_session_info(session_id)
        
        elif msg_type == 'launch_demo':
            # Broadcast demo launch to all clients
            await self.broadcast(session_id, {
                'type': 'demo_launch',
                'demo_id': data.get('demo_id'),
                'demo_name': data.get('demo_name'),
                'timestamp': datetime.now().isoformat(),
                'host': client_id
            })
        
        elif msg_type == 'playback_sync':
            # Synchronize playback state
            await self.broadcast(session_id, {
                'type': 'playback_state',
                'state': data.get('state'),
                'time': data.get('time'),
                'demo_id': data.get('demo_id')
            })
        
        elif msg_type == 'chat':
            await self.broadcast(session_id, {
                'type': 'chat',
                'message': data.get('message'),
                'sender': data.get('sender', client_id[:8])
            })
    
    async def broadcast(self, session_id: str, message: dict):
        if session_id not in self.clients:
            return
        msg_str = json.dumps(message)
        # In real implementation, send to all connected clients
        print(f"[PartyMode] Broadcasting to {session_id}: {message.get('type')}")
    
    async def broadcast_session_info(self, session_id: str):
        await self.broadcast(session_id, {
            'type': 'session_info',
            'session': {
                'id': session_id,
                'participant_count': len(self.clients.get(session_id, set())),
                'created_at': datetime.now().isoformat()
            }
        })

# CLI for starting party mode
if __name__ == "__main__":
    import sys
    print("🎉 Showet Party Mode Server")
    print("Usage: python3 showet-party-mode.py <port>")
    print("Example: python3 showet-party-mode.py 8765")
    sys.exit(0)