#!/usr/bin/env python3
"""WebRTC signaling server for collaborative demo sessions.

Allows multiple users to watch demos together in sync.
"""

import json
import uuid
from pathlib import Path
from typing import Optional

# Simple in-memory session store (would use Redis in production)
SESSIONS: dict[str, dict] = {}


def create_session(platform: str, demo_id: Optional[int] = None) -> str:
    """Create a new collaborative session."""
    session_id = str(uuid.uuid4())[:8]
    
    SESSIONS[session_id] = {
        "platform": platform,
        "demo_id": demo_id,
        "host": None,
        "peers": [],
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


# Generate session HTML for easy joining
def generate_session_html(session_id: str) -> str:
    return f'''
<script>
// WebSocket connection for collaborative demo watching
const ws = new WebSocket("wss://showet.live/ws/{session_id}");
ws.onmessage = (event) => {{
    const data = JSON.parse(event.data);
    if (data.type === "playback_state") {{
        // Sync playback across all peers
        console.log("Sync:", data.state);
    }}
}};
</script>
'''