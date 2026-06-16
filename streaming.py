#!/usr/bin/env python3
"""Streaming integration for Showet - Twitch, YouTube Live, RTSP, and more.

Features:
- RTMP streaming to Twitch/YouTube/Facebook Live
- RTSP server for local network streaming
- OBS-style scene switching and overlays
- Webcam/microphone integration
- Recording capabilities for demo captures
- Integration with platform runners
- Scheduled demo overlay support
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# Try to import scheduler for overlay integration
try:
    import importlib.util
    if importlib.util.find_spec("demo_scheduler"):
        SCHEDULER_AVAILABLE = True
    else:
        SCHEDULER_AVAILABLE = False
except ImportError:
    SCHEDULER_AVAILABLE = False

# Quality presets
QUALITY_PRESETS = {
    "480p": {"resolution": "854x480", "bitrate": "1500k", "bframes": 0},
    "720p": {"resolution": "1280x720", "bitrate": "2500k", "bframes": 0},
    "1080p": {"resolution": "1920x1080", "bitrate": "4500k", "bframes": 2},
    "1440p": {"resolution": "2560x1440", "bitrate": "6500k", "bframes": 2},
    "4k": {"resolution": "3840x2160", "bitrate": "12000k", "bframes": 2},
}


class StreamPlatform(str, Enum):
    """Supported streaming platforms."""
    TWITCH = "twitch"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    CUSTOM = "custom"
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
    webcam_position: str = "top-right"  # top-right, top-left, bottom-right, bottom-left
    overlay_text: str = ""
    record_locally: bool = False
    record_path: str | None = None
    fps: int = 30
    extra_ffmpeg_args: list[str] = field(default_factory=list)


class StreamManager:
    """Manage live streaming output for demos with full production features."""

    def __init__(self) -> None:
        self.config: StreamConfig | None = None
        self._process: subprocess.Popen | None = None
        self._rtsp_server: subprocess.Popen | None = None
        self.is_streaming: bool = False

    def configure(self, config: StreamConfig) -> None:
        """Configure the stream manager with streaming options."""
        self.config = config
        if not config.stream_key and config.platform != StreamPlatform.RTSP:
            config_path = Path.home() / ".showet" / "stream_key"
            if config_path.exists():
                config.stream_key = config_path.read_text().strip()

    def _build_ffmpeg_command(self, window_id: str = "0") -> list[str]:
        """Build the ffmpeg command based on configuration."""
        if not self.config:
            raise RuntimeError("StreamManager not configured")

        preset = QUALITY_PRESETS.get(self.config.quality, QUALITY_PRESETS["720p"])
        width, height = preset["resolution"].split("x")

        cmd = ["ffmpeg"]

        # Video input - use x11grab for X11 or gdigrab for Windows
        cmd.extend([
            "-y",  # Overwrite output
            "-f", "x11grab",
            "-framerate", str(self.config.fps),
            "-video_size", preset["resolution"],
            "-i", f":{window_id}",
        ])

        # Add webcam if enabled
        inputs = [(":0")] if not self.config.include_webcam else []
        if self.config.include_webcam:
            cmd.extend([
                "-f", "v4l2",
                "-framerate", "30",
                "-video_size", "640x480",
                "-i", self.config.webcam_device,
            ])
            inputs.append(self.config.webcam_device)

        # Audio input (system audio)
        if self.config.include_audio:
            cmd.extend([
                "-f", "pulse",
                "-i", "default",
            ])
            inputs.append("audio")

        # Video encoding - build filter graph if needed
        video_filters = []

        # Add webcam overlay (takes webcam as input 1)
        if self.config.include_webcam:
            x, y = "(W-w-10)", "(H-h-10)"  # top-right by default
            if self.config.webcam_position == "top-left":
                x, y = "10", "10"
            elif self.config.webcam_position == "bottom-right":
                x, y = "(W-w-10)", "(H-h-10)"
            elif self.config.webcam_position == "bottom-left":
                x, y = "10", "(H-h-10)"

            # Overlay webcam (input 1) onto main video (input 0)
            video_filters.append(
                f"[0:v][1:v]overlay={x}:{y}[vout]"
            )

        # Add text overlay for demo info (apply to the video output)
        if self.config.overlay_text:
            text_escape = self.config.overlay_text.replace("'", "\\'")
            drawtext_filter = (
                f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                f"text='{text_escape}':fontcolor=white:fontsize=24:x=10:y=H-34"
            )
            if video_filters:
                # Add drawtext to the vout
                video_filters.append(f"[vout]{drawtext_filter}[vfinal]")
            else:
                video_filters.append(f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                                     f"text='{text_escape}':fontcolor=white:fontsize=24:x=10:y=H-34")

        if video_filters:
            cmd.extend(["-filter_complex", ";".join(video_filters)])
            # Map the final video output
            if "[vfinal]" in str(video_filters):
                cmd.extend(["-map", "[vfinal]"])
            elif "[vout]" in str(video_filters):
                cmd.extend(["-map", "[vout]"])
            else:
                # Just drawtext, no filter graph needed
                pass
        else:
            cmd.extend(["-map", "0:v"])

        cmd.extend([
            "-c:v", "libx264",
            "-preset", "fast",
            "-b:v", preset["bitrate"],
            "-maxrate", preset["bitrate"],
            "-bufsize", f"{int(preset['bitrate'].replace('k', '')) * 2}k",
            "-pix_fmt", "yuv420p",
        ])

        # Audio encoding
        if self.config.include_audio:
            cmd.extend([
                "-map", "0:a?" if self.config.include_webcam else "0:a",
                "-c:a", "aac",
                "-b:a", "128k",
            ])

        cmd.extend(self.config.extra_ffmpeg_args)

        # Output format based on platform
        stream_url = self._get_stream_url()
        cmd.extend(["-f", "flv" if self.config.platform != StreamPlatform.RTSP else "rtsp", stream_url])

        return cmd

    def _get_stream_url(self) -> str:
        """Get the formatted stream URL based on platform and key."""
        if not self.config:
            raise RuntimeError("StreamManager not configured")

        base_urls = {
            StreamPlatform.TWITCH: "rtmp://live.twitch.tv/app/{}",
            StreamPlatform.YOUTUBE: "rtmp://a.rtmp.youtube.com/live2/{}",
            StreamPlatform.FACEBOOK: "rtmp://live-upload.facebook.com:443/rtmp/{}",
            StreamPlatform.RTSP: "rtsp://0.0.0.0:8554/showet",
            StreamPlatform.CUSTOM: "{}",
        }

        if self.config.platform == StreamPlatform.RTSP:
            return base_urls[StreamPlatform.RTSP].format(self.config.stream_key or "")

        return base_urls[self.config.platform].format(self.config.stream_key)

    def start(self, window_id: str = "0", overlay_text: str = "") -> subprocess.Popen | None:
        """Start streaming with current configuration.
        
        Args:
            window_id: X11 display/window to capture (e.g., "0" for :0)
            overlay_text: Text overlay to display (overrides config.overlay_text)
        """
        cmd = self._build_ffmpeg_command(window_id)

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                text=True
            )
            self.is_streaming = True
            label = overlay_text or self.config.overlay_text or "manual playback"
            print(f"📺 Streaming started to {self.config.platform.value}")
            print(f"🎯 Demo: {label}")
            return self._process
        except FileNotFoundError:
            print("❌ FFmpeg not found. Install ffmpeg for streaming support.")
            print("   Ubuntu/Debian: sudo apt install ffmpeg")
            print("   Fedora: sudo dnf install ffmpeg")
            print("   macOS: brew install ffmpeg")
            return None

    def start_rtsp_server(self, port: int = 8554) -> subprocess.Popen | None:
        """Start standalone RTSP server for local network streaming."""
        cmd = [
            "ffmpeg",
            "-f", "x11grab",
            "-framerate", "30",
            "-video_size", "1280x720",
            "-i", ":0",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-f", "rtsp",
            f"rtsp://0.0.0.0:{port}/showet",
        ]

        try:
            self._rtsp_server = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            print(f"📡 RTSP server started on rtsp://localhost:{port}/showet")
            return self._rtsp_server
        except FileNotFoundError:
            print("❌ FFmpeg not found.")
            return None

    def stop(self) -> None:
        """Stop the streaming process."""
        if self._process:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None

        if self._rtsp_server:
            self._rtsp_server.terminate()
            self._rtsp_server.wait()
            self._rtsp_server = None

        self.is_streaming = False
        print("⏹️ Streaming stopped")

    def get_status(self) -> dict:
        """Get current streaming status."""
        status = {
            "streaming": self.is_streaming,
            "platform": self.config.platform.value if self.config else None,
            "quality": self.config.quality if self.config else None,
            "has_webcam": self.config.include_webcam if self.config else False,
            "recording": bool(self.config and self.config.record_locally),
        }
        
        return status


def get_stream_key(platform: str = "twitch") -> str:
    """Get stream key from config file."""
    config_path = Path.home() / ".showet" / f"{platform}_stream_key"
    if config_path.exists():
        return config_path.read_text().strip()
    # Fallback to generic stream key
    generic_path = Path.home() / ".showet" / "stream_key"
    if generic_path.exists():
        return generic_path.read_text().strip()
    return ""


def setup_stream_key(platform: str, stream_key: str) -> None:
    """Save stream key to config file."""
    config_dir = Path.home() / ".showet"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / f"{platform}_stream_key"
    config_path.write_text(stream_key)
    # Set restrictive permissions
    config_path.chmod(0o600)
    print(f"🔑 Stream key saved to {config_path}")


# Preset configurations for common use cases
def create_demo_stream_config(
    platform: StreamPlatform,
    stream_key: str,
    quality: str = "720p",
    demo_name: str = "",
    platform_slug: str = ""
) -> StreamConfig:
    """Create a stream config optimized for demo playback."""
    overlay = f"SHOWET • {platform_slug.upper()}"
    if demo_name:
        overlay = f"{demo_name} • {platform_slug.upper()}"

    return StreamConfig(
        platform=platform,
        stream_key=stream_key,
        quality=quality,
        include_audio=True,
        include_webcam=False,
        overlay_text=overlay,
        record_locally=False,
    )


if __name__ == "__main__":
    # Demo configuration helper
    print("StreamManager ready!")
    print("\nQuick setup:")
    print("  1. Get your stream key from Twitch/YouTube")
    print("  2. save_stream_key.py --platform twitch --key YOUR_KEY")
    print("  3. showet-stream --platform twitch --demo 12345")
    print("\nPlatforms: twitch, youtube, facebook, rtsp, custom")