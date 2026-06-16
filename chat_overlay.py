#!/usr/bin/env python3
"""Demo chat overlay system for Showet.

Provides:
- Twitch/YouTube chat overlay
- Hall of fame ticker
- Party countdown display
- Custom message overlay
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Chat overlay templates
OVERLAY_TEMPLATES = {
    "twitch": {
        "position": "bottom-left",
        "background": "rgba(0,0,0,0.7)",
        "font": "'Courier New', monospace",
        "color": "#ff6b00",
        "border": "#9146FF",
    },
    "youtube": {
        "position": "bottom-right",
        "background": "rgba(255,255,255,0.1)",
        "font": "'Roboto', sans-serif",
        "color": "#FF0000",
        "border": "#FF0000",
    }
}


def generate_chat_overlay_html(platform: str = "twitch", with_hall_of_fame: bool = True) -> str:
    """Generate chat overlay HTML for streaming.
    
    Args:
        platform: Streaming platform (twitch/youtube)
        with_hall_of_fame: Show hall of fame ticker
    
    Returns:
        HTML/CSS for chat overlay
    """
    template = OVERLAY_TEMPLATES.get(platform, OVERLAY_TEMPLATES["twitch"])
    
    # Hall of fame randomizer
    hof_js = ""
    if with_hall_of_fame:
        from demo_spotlight import HALL_OF_FAME
        hof_items = ", ".join([f'"{d["name"]}"' for d in HALL_OF_FAME[:5]])
        hof_js = f'''
<script>
const hallOfFame = [{hof_items}];
let hofIndex = 0;
setInterval(() => {{
    document.getElementById('hof-ticker').textContent = '🏆 ' + hallOfFame[hofIndex];
    hofIndex = (hofIndex + 1) % hallOfFame.length;
}}, 8000);
</script>
'''
    
    return f'''
<div id="showet-chat-overlay" style="
    position: fixed;
    {template['position'].replace('-', ' ')};
    bottom: 20px; {'left: 20px;' if 'left' in template['position'] else 'right: 20px;'};
    background: {template['background']};
    padding: 10px 15px;
    border-radius: 5px;
    border: 2px solid {template['border']};
    font-family: {template['font']};
    color: {template['color']};
    max-width: 350px;
    z-index: 9999;
">
    <div id="chat-header" style="font-weight: bold; margin-bottom: 5px;">
        💬 Showet Chat
    </div>
    <div id="chat-messages" style="font-size: 12px; max-height: 200px; overflow-y: auto;"></div>
    <div id="hof-ticker" style="font-size: 11px; margin-top: 8px; opacity: 0.8;"></div>
    <input id="chat-input" type="text" placeholder="Type your comment..." 
           style="width: 100%; margin-top: 5px; background: #111; border: 1px solid {template['border']}; color: white;">
{hof_js}
</div>
<script>
// Chat WebSocket integration
const chatWs = new WebSocket("wss://showet.live/chat");
chatWs.onmessage = (event) => {{
    const data = JSON.parse(event.data);
    const chat = document.getElementById('chat-messages');
    const msg = document.createElement('div');
    msg.style.margin = '2px 0';
    msg.textContent = '<strong>' + data.user + '</strong>: ' + data.message;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}};
</script>
'''


def generate_simple_ticker(messages: list[str], duration: int = 30) -> str:
    """Generate a simple scrolling ticker overlay.
    
    Args:
        messages: List of messages to show
        duration: Seconds to show each message
    
    Returns:
        HTML for ticker overlay
    """
    msgs = ", ".join([f'"{m}"' for m in messages])
    return f'''
<div id="showet-ticker" style="
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,0.8);
    padding: 8px 20px;
    border-radius: 20px;
    border: 2px solid #ff6b00;
    color: #ff6b00;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    z-index: 9999;
">
    <span id="ticker-message"></span>
</div>
<script>
const tickerMsgs = [{msgs}];
let tickerIdx = 0;
setInterval(() => {{
    document.getElementById('ticker-message').textContent = tickerMsgs[tickerIdx];
    tickerIdx = (tickerIdx + 1) % tickerMsgs.length;
}}, {duration * 1000});
</script>
'''


def add_demo_info_overlay(demo_id: int) -> str:
    """Add demo info overlay for streaming.
    
    Args:
        demo_id: Pouet.net demo ID
    
    Returns:
        HTML for demo info overlay
    """
    try:
        import urllib.request
        url = f"http://api.pouet.net/v1/prod/?id={demo_id}"
        data = json.loads(urllib.request.urlopen(url, timeout=5).read().decode())
        prod = data.get("prod", {})
        
        name = prod.get("name", "Unknown")
        group = ", ".join([g.get("name", "") for g in prod.get("groups", [])[:2]])
        party = prod.get("party", {}).get("name", "")
        year = prod.get("year", "")
        
        return f'''
<div id="demo-info-overlay" style="
    position: fixed;
    top: 20px;
    right: 20px;
    background: rgba(0,0,0,0.85);
    padding: 15px;
    border-radius: 5px;
    border: 2px solid #ff6b00;
    color: white;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    z-index: 9998;
">
    <div style="color: #ff6b00; font-weight: bold;">🎬 NOW PLAYING</div>
    <div style="margin-top: 5px;">{name}</div>
    <div style="font-size: 12px; opacity: 0.8;">by {group}</div>
    <div style="font-size: 11px; margin-top: 3px;">{party} {year}</div>
</div>
'''
    except Exception:
        return ""


if __name__ == "__main__":
    print("Chat overlay templates:")
    for name in OVERLAY_TEMPLATES:
        print(f"  - {name}")
    print("\nAdd to streaming output for enhanced viewer experience!")


def main() -> None:
    """CLI entry point."""
    import sys
    platform = sys.argv[1] if len(sys.argv) > 1 else "twitch"
    html = generate_chat_overlay_html(platform)
    print(f"Chat overlay HTML for {platform}:")
    print(html[:200] + "...")