#!/usr/bin/env python3
"""Streaming integration for Showet - Twitch, YouTube Live, RTSP.

Features:
- RTMP streaming to Twitch/YouTube
- RTSP server for local network streaming
- Recording capabilities for demo captures
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


class StreamManager:
    """Manage live streaming output for demos."""

    def __init__(self) -> None:
        self.stream_url: Optional[str] = None
        self.platform: str = "twitch"
        self.quality: str = "720p"
        self._process: subprocess.Popen | None = None

    def setup_rtmp(self, stream_url: str, platform: str = "twitch", quality: str = "720p") -> None:
        """Configure RTMP streaming to Twitch/YouTube."""
        self.stream_url = stream_url
        self.platform = platform
        self.quality = quality

    def start_stream(self, window_id: str = "0") -> Optional[subprocess.Popen]:
        """Start streaming using ffmpeg."""
        if not self.stream_url:
            print("No stream URL configured")
            return None

        # FFmpeg command for RTMP streaming
        # Captures screen/window and streams to RTMP endpoint
        cmd = [
            "ffmpeg",
            "-f", "x11grab",
            "-r", "30",
            "-s", "1280x720",
            "-i", f":{window_id}",
            "-c:v", "libx264",
            "-preset", "fast",
            "-b:v", "2500k",
            "-maxrate", "2500k",
            "-bufsize", "5000k",
            "-pix_fmt", "yuv420p",
            "-f", "flv",
            self.stream_url
        ]

        try:
            self._process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(f"📺 Streaming started to {self.platform}: {self.stream_url[:20]}...")
            return self._process
        except FileNotFoundError:
            print("❌ FFmpeg not found. Install ffmpeg for streaming support.")
            return None

    def start_rtsp_server(self, port: int = 8554) -> Optional[subprocess.Popen]:
        """Start an RTSP server for local network streaming."""
        cmd = [
            "ffmpeg",
            "-f", "x11grab",
            "-r", "30",
            "-s", "1280x720",
            "-i", ":0",
            "-c:v", "libx264",
            "-f", "rtsp",
            f"rtsp://0.0.0.0:{port}/demo"
        ]

        try:
            self._process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(f"📡 RTSP server started on port {port}")
            return self._process
        except FileNotFoundError:
            print("❌ FFmpeg not found.")
            return None

    def stop_stream(self) -> None:
        """Stop the streaming process."""
        if self._process:
            self._process.terminate()
            self._process.wait()
            self._process = None
            print("⏹️ Streaming stopped")


def get_twitch_stream_key() -> str:
    """Get Twitch stream key from config or prompt."""
    config_path = Path.home() / ".showet" / "stream_key"
    if config_path.exists():
        return config_path.read_text().strip()
    return ""


def format_twitch_url(stream_key: str) -> str:
    """Format Twitch ingest URL."""
    return f"rtmp://live.twitch.tv/app/{stream_key}"


def format_youtube_url(stream_key: str) -> str:
    """Format YouTube Live ingest URL."""
    return f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"


if __name__ == "__main__":
    # Example usage
    streamer = StreamManager()
    print("StreamManager ready - configure with stream URL for live demo streaming!")
    print("Twitch: rtmp://live.twitch.tv/app/YOUR_STREAM_KEY")
    print("YouTube: rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY")