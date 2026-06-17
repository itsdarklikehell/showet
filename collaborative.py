# Collaborative session server - join and watch demos together
from __future__ import annotations

import json
import uuid
import asyncio
import websockets
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, parse_qs

# In-memory session store with WebSocket connections
SESSIONS: dict[str, dict] = {}
WEBSOCKET_CONNECTIONS: dict[str, list] = {}  # session_id -> [websocket_connections]


def create_session(platform: str, demo_id: Optional[int] = None, stream_to: Optional[str] = None,
                   session_name: str = "Demo Session") -> str:
    """Create a new collaborative session.
    
    Args:
        platform: Platform slug for the demo (e.g., 'commodore_64')
        demo_id: Pouet.net demo ID
        stream_to: Optional streaming platform ('twitch', 'youtube', 'rtsp')
        session_name: Human-readable session name
    
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
        "created": datetime.now().isoformat(),
        "playback_state": "idle",
        "playback_time": 0,
        "session_name": session_name,
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


def list_sessions() -> list[dict]:
    """List all active sessions."""
    return [{
        "id": sid,
        "platform": s["platform"],
        "demo_id": s.get("demo_id"),
        "session_name": s.get("session_name", "Demo Session"),
        "peers": len(s["peers"]),
    } for sid, s in SESSIONS.items()]


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


class CollaborativeHandler(SimpleHTTPRequestHandler):
    """HTTP handler for collaborative session management."""

    def __init__(self, *args, **kwargs):
        self.project_root = Path(__file__).parent
        super().__init__(*args, directory=str(self.project_root), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/api/sessions":
            self._handle_list_sessions()
        elif parsed.path.startswith("/api/session/"):
            session_id = parsed.path.split("/")[3]
            self._handle_get_session(session_id)
        elif parsed.path == "/session/" or parsed.path.startswith("/session/"):
            session_id = parsed.path.split("/")[2] if "/" in parsed.path else None
            if session_id:
                self._handle_session_page(session_id)
            else:
                self.send_error(404, "Session not specified")
        else:
            super().do_GET()

    def _handle_list_sessions(self):
        sessions = list_sessions()
        self.send_json_response({"sessions": sessions})

    def _handle_get_session(self, session_id: str):
        session = get_session(session_id)
        if session:
            self.send_json_response(session)
        else:
            self.send_error(404, "Session not found")

    def _handle_session_page(self, session_id: str):
        session = get_session(session_id)
        if not session:
            self.send_error(404, "Session not found")
            return
        
        html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Showet Session - {session.get('session_name', session_id)}</title>
    <script src="https://cdn.jsdelivr.net/npm/nostalgist@latest/dist/nostalgist.min.js"></script>
    <script src="collaborative.js"></script>
</head>
<body style="background:#111;color:white;font-family:Courier New,monospace;">
    <h1>📺 Showet Session: {session.get('session_name', session_id)}</h1>
    {generate_session_html(session_id, with_stream=True, spectator_mode=True)}
</body>
</html>
'''
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def send_json_response(self, data: dict, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


async def broadcast_to_session(session_id: str, message: dict):
    """Broadcast message to all WebSocket connections in a session."""
    if session_id in WEBSOCKET_CONNECTIONS:
        connections = WEBSOCKET_CONNECTIONS[session_id][:]
        for ws in connections:
            try:
                await ws.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                WEBSOCKET_CONNECTIONS[session_id].remove(ws)


async def register_connection(session_id: str, websocket):
    """Register a WebSocket connection for a session."""
    if session_id not in WEBSOCKET_CONNECTIONS:
        WEBSOCKET_CONNECTIONS[session_id] = []
    WEBSOCKET_CONNECTIONS[session_id].append(websocket)


async def unregister_connection(session_id: str, websocket):
    """Unregister a WebSocket connection for a session."""
    if session_id in WEBSOCKET_CONNECTIONS:
        WEBSOCKET_CONNECTIONS[session_id].remove(websocket)


# WebSocket handler for real-time communication
async def websocket_handler(websocket, path):
    """Handle WebSocket connections for collaborative sessions."""
    try:
        # Extract session ID from path
        session_id = path.split("/")[-1]
        
        # Register connection
        await register_connection(session_id, websocket)
        
        # Send initial state
        session = get_session(session_id)
        if session:
            await websocket.send(json.dumps({
                "type": "session_info",
                "session": session
            }))
        
        # Listen for messages
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("type") == "playback_state":
                    update_playback(session_id, data.get("state", "unknown"), data.get("time", 0))
                    await broadcast_to_session(session_id, data)
                elif data.get("type") == "chat":
                    await broadcast_to_session(session_id, data)
                elif data.get("type") == "join":
                    join_session(data.get("session_id"), data.get("client_id"))
            except json.JSONDecodeError:
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await unregister_connection(session_id, websocket)


def start_websocket_server(port: int = 8765):
    """Start WebSocket server for real-time collaboration."""
    async def run():
        print(f"🤝 WebSocket server on ws://localhost:{port}")
        async with websockets.serve(websocket_handler, "0.0.0.0", port):
            await asyncio.Future()  # run forever
    
    asyncio.run(run())


def main(port: int = 8766):
    """Start collaborative session server."""
    print(f"🤝 Showet Collaborative Server on http://localhost:{port}")
    print("Create sessions: POST /api/create?platform=c64&demo_id=12345")
    server = HTTPServer(("0.0.0.0", port), CollaborativeHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")


if __name__ == "__main__":
    main()