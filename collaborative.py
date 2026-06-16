#!/usr/bin/env python3
"""WebRTC signaling server for collaborative demo sessions.

Allows multiple users to watch demos together in sync, with optional
live streaming integration for broadcasting to Twitch/YouTube.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Optional

# Simple in-memory session store (would use Redis in production)
SESSIONS: dict[str, dict] = {}


def create_session(platform: str, demo_id: Optional[int] = None, stream_to: Optional[str] = None) -> str:
    """Create a new collaborative session.
    
    Args:
        platform: Platform slug for the demo (e.g., 'commodore_64')
        demo_id: Pouet.net demo ID
        stream_to: Optional streaming platform ('twitch', 'youtube', 'rtsp')
    
    Returns:
        Session ID for joining
    """
    session_id = str(uuid.uuid4())[:8]
    
    SESSIONS[session_id] = {
        "platform": platform,
        "demo_id": demo_id,
        "host": None,
        "peers": [],
        "stream_to": stream_to,
        "created": str(Path.home()),
        "playback_state": "idle"
    }
    
    return session_id


def join_session(session_id: str, client_id: str) -> dict:
    """Join an existing session."""
    session = SESSIONS.get(session_id)
    if not session:
        return {"error": "Session not found"}
    
    session["peers"].append(client_id)
    return {
        "session": session,
        "websocket_url": f"wss://showet.live/ws/{session_id}"
    }


def update_playback(session_id: str, state: str, time: float = 0) -> dict:
    """Update playback state for all peers."""
    session = SESSIONS.get(session_id)
    if not session:
        return {"error": "Session not found"}
    
    session["playback_state"] = state
    session["playback_time"] = time
    
    # In real implementation, broadcast via WebSocket
    return {"status": "updated", "state": state}


def get_session(session_id: str) -> Optional[dict]:
    """Get session details."""
    return SESSIONS.get(session_id)


def get_session_with_stream_info(session_id: str) -> Optional[dict]:
    """Get session info including stream status."""
    session = SESSIONS.get(session_id)
    if session and session.get("stream_to"):
        session["stream_available"] = True
    return session


# Generate session HTML for easy joining
def generate_session_html(session_id: str, with_stream: bool = False, spectator_mode: bool = False) -> str:
    """Generate HTML snippet for joining a collaborative session.
    
    Args:
        session_id: Session to join
        with_stream: Include streaming integration
        spectator_mode: Add chat overlay for spectators
    """
    stream_js = ""
    if with_stream:
        stream_js = '''
<script>
// Check if session has active stream
const ws = new WebSocket("wss://showet.live/ws/${session_id}");
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "stream_status" && data.active) {
        console.log("Live stream available at:", data.stream_url);
    }
};
</script>
'''
    
    chat_overlay = ""
    if spectator_mode:
        chat_overlay = '''
<div style="position:fixed;bottom:20px;left:20px;background:rgba(0,0,0,0.8);padding:10px;border:1px solid #ff6b00;border-radius:5px;">
  <div id="chat-messages" style="max-height:200px;overflow-y:auto;color:white;font-size:12px;"></div>
  <input id="chat-input" type="text" placeholder="Type chat..." style="width:100%;margin-top:5px;">
</div>
<script>
document.getElementById('chat-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const msg = e.target.value;
        if (msg) {
            // Send chat message via WebSocket
            ws.send(JSON.stringify({type: 'chat', message: msg}));
            e.target.value = '';
        }
    }
});
</script>
'''
    
    return f'''
<div id="showet-session-{session_id}">
  <script>
// WebSocket connection for collaborative demo watching
const ws = new WebSocket("wss://showet.live/ws/{session_id}");
ws.onmessage = (event) => {{
    const data = JSON.parse(event.data);
    if (data.type === "playback_state") {{
        // Sync playback across all peers
        console.log("Sync:", data.state);
    }}
    if (data.type === "chat") {{
        // Display chat messages
        const chat = document.getElementById('chat-messages');
        if (chat) {{
            const p = document.createElement('p');
            p.textContent = data.message;
            chat.appendChild(p);
        }}
    }}
}};
</script>
{stream_js}
{chat_overlay}
</div>
'''


if __name__ == "__main__":
    # Demo
    session = create_session("commodore_64", 12345)
    print(f"Created session: {session}")
    print(f"Join at: https://showet.live/session/{session}")