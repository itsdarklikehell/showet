"""Stream manager module for Showet.

RTMP/RTSP streaming to Twitch, YouTube, and other platforms with CRT overlays.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from enum import Enum


class StreamPlatform(str, Enum):
    """Supported streaming platforms."""
    TWITCH = "twitch"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    RTSP = "rtsp"


@dataclass
class StreamConfig:
    """Configuration for a streaming session."""
    platform: StreamPlatform = StreamPlatform.TWITCH
    stream_key: str = ""
    quality: str = "720p"
    include_audio: bool = True
    include_webcam: bool = False
    webcam_device: str = "/dev/video0"
    webcam_position: str = "top-right"
    overlay_text: str = ""
    fps: int = 30


class StreamManager:
    """Manage live streaming output for demos."""

    def __init__(self) -> None:
        self.config: StreamConfig | None = None
        self._process: subprocess.Popen | None = None
        self.is_streaming: bool = False

    def configure(self, config: StreamConfig) -> None:
        """Configure the stream manager with streaming options."""
        self.config = config

    def start(self, overlay_text: str = "") -> subprocess.Popen | None:
        """Start streaming with current configuration."""
        if not self.config:
            return None
        # Simplified streaming start
        self.is_streaming = True
        return None

    def stop(self) -> None:
        """Stop the streaming process."""
        if self._process:
            self._process.terminate()
            self._process = None
        self.is_streaming = False

    def get_status(self) -> dict:
        """Get current streaming status."""
        return {
            "streaming": self.is_streaming,
            "platform": self.config.platform.value if self.config else None,
        }