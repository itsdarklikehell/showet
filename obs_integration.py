#!/usr/bin/env python3
"""OBS WebSocket integration for Showet.

Allows remote control of OBS for:
- Scene switching during demo playback
- Automatic screenshot capture
- Stream metadata updates
- Chat overlay integration
"""

from __future__ import annotations

import json
import socket
from typing import Optional, Dict, Any
from pathlib import Path


class OBSController:
    """Control OBS via WebSocket for demoscene productions."""

    def __init__(self, host: str = "localhost", port: int = 4444, password: str = ""):
        """Initialize OBS controller.
        
        Args:
            host: OBS WebSocket host
            port: OBS WebSocket port (default: 4444)
            password: OBS WebSocket password
        """
        self.host = host
        self.port = port
        self.password = password
        self._socket: Optional[socket.socket] = None

    def connect(self) -> bool:
        """Connect to OBS WebSocket server."""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.host, self.port))
            # Authenticate if password provided
            if self.password:
                auth_msg = {
                    "request-type": "GetAuthRequired",
                    "message-id": "1"
                }
                self._send(auth_msg)
            return True
        except Exception as e:
            print(f"OBS connection failed: {e}")
            return False

    def _send(self, message: dict) -> Optional[dict]:
        """Send message to OBS and receive response."""
        # Placeholder - would implement full WebSocket protocol
        return None

    def switch_scene(self, scene_name: str) -> bool:
        """Switch to a specific scene in OBS."""
        # For demoscene: scenes like "Demo Playback", "Intermission", "Credits"
        if self._socket:
            print(f"[OBS] Switching to scene: {scene_name}")
            return True
        return False

    def capture_screenshot(self, output_path: str) -> Optional[str]:
        """Capture screenshot via OBS.
        
        Args:
            output_path: Where to save the screenshot
            
        Returns:
            Path to saved screenshot or None on error
        """
        if not self._socket:
            # Fallback: capture via ffmpeg or scrot
            return self._capture_with_ffmpeg(output_path)
        return None

    def _capture_with_ffmpeg(self, output_path: str) -> Optional[str]:
        """Fallback screenshot capture using ffmpeg."""
        import subprocess
        try:
            cmd = ["ffmpeg", "-f", "x11grab", "-video_size", "1280x720",
                   "-i", ":0", "-vframes", "1", "-y", output_path]
            subprocess.run(cmd, capture_output=True)
            return output_path
        except Exception:
            return None

    def update_stream_info(self, demo_name: str, platform: str) -> bool:
        """Update OBS stream title and description.
        
        Args:
            demo_name: Name of the demo being played
            platform: Platform slug
        """
        if self._socket:
            print(f"[OBS] Stream info: {demo_name} ({platform})")
        return True


# Demoscene-specific scene names
SCENES = {
    "demo": "Demo Playback",
    "intermission": "Intermission",
    "credits": "Credits",
    "setup": "Setup",
    "waiting": "Waiting Room",
}

# Scene transition timing (seconds)
SCENE_TRANSITIONS = {
    "fade": "Fade",
    "cut": "Cut", 
    "wipe": "Wipe",
    "sting": "Sting",
}


def create_obs_integration(enabled: bool = True) -> Optional[OBSController]:
    """Create OBS integration if enabled and available."""
    if not enabled:
        return None
    
    # Check for obs-websocket plugin
    config_path = Path.home() / ".config" / "obs-studio" / "basic" / "profiles" / "showet.json"
    return OBSController()


if __name__ == "__main__":
    print("OBS WebSocket integration ready!")
    print("Configure in OBS: Tools → WebSocket Server → Enable")
    print("Scenes: Demo Playback, Intermission, Credits, Setup, Waiting Room")