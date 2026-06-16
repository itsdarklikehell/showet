#!/usr/bin/env python3
"""RTMP relay for multi-platform streaming.

Stream to multiple platforms simultaneously (Twitch, YouTube, Facebook).
Uses FFmpeg tee muxer or separate processes.

Demoscene feature: Broadcast your demo party releases everywhere at once!
"""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List

from streaming import StreamConfig, StreamPlatform, StreamManager, QUALITY_PRESETS


class RelayMode(str, Enum):
    """How to relay streams."""
    TEE = "tee"       # Single FFmpeg with tee muxer
    MULTI = "multi"   # Separate FFmpeg processes


@dataclass
class MultiStreamConfig:
    """Configuration for streaming to multiple platforms."""
    targets: List[tuple[StreamPlatform, str]] = field(default_factory=list)  # [(platform, key), ...]
    quality: str = "720p"
    include_audio: bool = True
    include_webcam: bool = False
    overlay_text: str = ""
    mode: RelayMode = RelayMode.TEE


class RTMPRelay:
    """Stream to multiple platforms simultaneously."""

    def __init__(self) -> None:
        self.config: Optional[MultiStreamConfig] = None
        self._processes: List[subprocess.Popen] = []
        self.is_relaying: bool = False

    def configure(self, config: MultiStreamConfig) -> None:
        """Configure the relay."""
        self.config = config

    def add_target(self, platform: StreamPlatform, stream_key: str) -> None:
        """Add a streaming target."""
        if self.config:
            self.config.targets.append((platform, stream_key))

    def _build_tee_command(self, window_id: str = "0") -> list[str]:
        """Build FFmpeg command using tee muxer for multi-streaming."""
        if not self.config or not self.config.targets:
            raise RuntimeError("No targets configured")

        preset = QUALITY_PRESETS.get(self.config.quality, QUALITY_PRESETS["720p"])
        width, height = preset["resolution"].split("x")

        cmd = ["ffmpeg", "-y", "-f", "x11grab", "-video_size", preset["resolution"],
               "-framerate", "30", "-i", f":{window_id}"]

        # Build tee output URL
        tee_parts = []
        for platform, key in self.config.targets:
            if platform == StreamPlatform.TWITCH:
                tee_parts.append(f"[f=flv]rtmp://live.twitch.tv/app/{key}")
            elif platform == StreamPlatform.YOUTUBE:
                tee_parts.append(f"[f=flv]rtmp://a.rtmp.youtube.com/live2/{key}")
            elif platform == StreamPlatform.FACEBOOK:
                tee_parts.append(f"[f=flv]rtmp://live-upload.facebook.com:443/rtmp/{key}")

        # Add encoding and tee output
        cmd.extend([
            "-c:v", "libx264", "-preset", "fast", "-b:v", preset["bitrate"],
            "-f", "tee", "-map", "0:v", 
            f"[{'|'.join(tee_parts)}]"
        ])

        return cmd

    def start(self, window_id: str = "0") -> bool:
        """Start relaying to all configured platforms."""
        if not self.config or not self.config.targets:
            print("❌ No streaming targets configured")
            return False

        if self.config.mode == RelayMode.MULTI:
            return self._start_multi(window_id)
        else:
            return self._start_tee(window_id)

    def _start_multi(self, window_id: str) -> bool:
        """Start separate FFmpeg processes for each target."""
        preset = QUALITY_PRESETS.get(self.config.quality, QUALITY_PRESETS["720p"])

        for platform, key in self.config.targets:
            try:
                config = StreamConfig(
                    platform=platform,
                    stream_key=key,
                    quality=self.config.quality,
                    include_audio=self.config.include_audio,
                    include_webcam=self.config.include_webcam,
                    overlay_text=self.config.overlay_text,
                )
                manager = StreamManager()
                manager.configure(config)
                proc = manager.start(window_id)
                if proc:
                    self._processes.append(proc)
                    print(f"📡 Started stream to {platform.value}")
            except Exception as e:
                print(f"❌ Failed to start {platform.value}: {e}")

        self.is_relaying = len(self._processes) > 0
        return self.is_relaying

    def _start_tee(self, window_id: str) -> bool:
        """Start single FFmpeg with tee muxer (not fully implemented)."""
        print("⚠️ Tee mode not yet implemented, falling back to multi-process")
        return self._start_multi(window_id)

    def stop(self) -> None:
        """Stop all relay processes."""
        for proc in self._processes:
            proc.terminate()
        self._processes.clear()
        self.is_relaying = False
        print("⏹️ All streams stopped")


def multi_stream_demo(demo_id: int, platforms_keys: List[tuple[str, str]], quality: str = "720p"):
    """Convenience function to stream demo to multiple platforms.
    
    Args:
        demo_id: Pouet.net demo ID
        platforms_keys: List of (platform, stream_key) tuples
        quality: Stream quality
    """
    relay = RTMPRelay()
    config = MultiStreamConfig(targets=[], quality=quality, overlay_text=f"Demo {demo_id}")
    relay.configure(config)

    for platform, key in platforms_keys:
        if platform.lower() == "twitch":
            relay.add_target(StreamPlatform.TWITCH, key)
        elif platform.lower() == "youtube":
            relay.add_target(StreamPlatform.YOUTUBE, key)
        elif platform.lower() == "facebook":
            relay.add_target(StreamPlatform.FACEBOOK, key)

    return relay.start()


if __name__ == "__main__":
    print("📡 RTMP Relay ready!")
    print("\nUsage:")
    print("  relay = RTMPRelay()")
    print("  config = MultiStreamConfig(targets=[(StreamPlatform.TWITCH, 'key')], quality='720p')")
    print("  relay.configure(config)")
    print("  relay.start()")
    print("\nOr use the convenience function:")
    print('  multi_stream_demo(12345, [("twitch", "key1"), ("youtube", "key2")])')


def main() -> None:
    """CLI entry point for RTMP relay."""
    import sys
    if len(sys.argv) < 2:
        print("📡 Showet RTMP Relay")
        print("Usage: showet-relay --platforms twitch,youtube --keys KEY1,KEY2 --demo 12345")
        return

    print("RTMP relay CLI - configure in code or via showet-launcher --multi-stream")