#!/usr/bin/env python3
"""Unified demo launcher for Showet combining all features.

This module provides:
- Demo search and discovery
- Streaming integration
- Collaboration across platforms
- CRT shader presets
- Playlist management
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path
from typing import Optional

from demo_database import DemoDatabase, get_db
from streaming import StreamConfig, StreamManager, StreamPlatform, setup_stream_key
from nostalgist_bridge import generate_nostalgist_config
from retro_effects import get_preset, CRT_PRESETS


class DemoLauncher:
    """Unified launcher for demoscene playback with all features."""

    def __init__(self):
        self.db = get_db()
        self.stream_manager = StreamManager()
        self.current_demo: Optional[dict] = None

    def search(self, query: str) -> list[dict]:
        """Search for demos."""
        return self.db.search_demos(query)

    def get_demo_info(self, pouet_id: int) -> dict:
        """Get demo metadata from Pouet."""
        url = f"http://api.pouet.net/v1/prod/?id={pouet_id}"
        try:
            response = urllib.request.urlopen(url, timeout=10)
            return json.loads(response.read().decode()).get("prod", {})
        except Exception as e:
            return {"error": str(e)}

    def get_crt_preset(self, platform: str) -> dict:
        """Get authentic CRT preset for platform."""
        return get_preset(platform)

    def launch(
        self,
        pouet_id: int,
        platform: str = None,
        stream_to: StreamPlatform = None,
        quality: str = "720p",
        fullscreen: bool = True,
        with_webcam: bool = False,
    ) -> None:
        """Launch a demo with optional streaming."""
        # Get demo info
        demo = self.get_demo_info(pouet_id)
        if "error" in demo:
            print(f"❌ Error fetching demo: {demo['error']}")
            return

        self.current_demo = demo
        
        # Determine platform if not specified
        if not platform:
            platforms = [p["slug"] for p in demo.get("platforms", {}).values()]
            platform = platforms[0] if platforms else None

        if not platform:
            print("❌ No platform found for this demo")
            return

        # Get CRT preset
        crt = self.get_crt_preset(platform)

        print(f"🚀 Launching: {demo.get('name', 'Unknown')}")
        print(f"🎯 Platform: {platform}")
        print(f"📺 CRT Preset: {crt.get('name', 'Default')}")

        # Setup streaming if requested
        if stream_to:
            stream_key = setup_stream_key(stream_to.value, "") or input(f"Enter {stream_to.value} stream key: ")
            config = StreamConfig(
                platform=stream_to,
                stream_key=stream_key,
                quality=quality,
                include_audio=True,
                include_webcam=with_webcam,
                overlay_text=f"{demo.get('name', 'Demo')} • {platform.upper()}",
            )
            self.stream_manager.configure(config)
            self.stream_manager.start(overlay_text=f"{demo.get('name', 'Demo')} • {platform.upper()}")

        # Record history
        self.db.add_history(pouet_id, platform)

    def create_streaming_playlist(self, name: str, platform: str, stream_to: StreamPlatform) -> str:
        """Create a playlist optimized for streaming a platform."""
        demos = self.db.search_by_platform(platform, limit=30)
        demo_ids = [d["id"] for d in demos]
        return self.db.create_playlist(name, demo_ids)

    def multi_stream_launch(
        self,
        pouet_id: int,
        platform_keys: list[tuple[str, str]],
        quality: str = "720p",
    ) -> None:
        """Launch demo stream to multiple platforms."""
        from rtmp_relay import RTMPRelay, MultiStreamConfig

        demo = self.get_demo_info(pouet_id)
        if "error" in demo:
            print(f"❌ Error: {demo['error']}")
            return

        # Determine platform
        platforms = [p["slug"] for p in demo.get("platforms", {}).values()]
        platform = (platforms[0] if platforms else "unknown").upper()

        targets = []
        for plat, key in platform_keys:
            if plat.lower() == "twitch":
                targets.append((StreamPlatform.TWITCH, key))
            elif plat.lower() == "youtube":
                targets.append((StreamPlatform.YOUTUBE, key))
            elif plat.lower() == "facebook":
                targets.append((StreamPlatform.FACEBOOK, key))

        config = MultiStreamConfig(
            targets=targets,
            quality=quality,
            overlay_text=f"{demo.get('name', 'Demo')} • {platform}",
        )

        relay = RTMPRelay()
        relay.configure(config)
        relay.start()

        print(f"📡 Streaming to {len(targets)} platforms!")


def main():
    parser = argparse.ArgumentParser(description="Showet unified demo launcher")
    parser.add_argument("--demo", type=int, help="Pouet.net demo ID")
    parser.add_argument("--search", help="Search query")
    parser.add_argument("--platform", help="Platform override")
    parser.add_argument("--stream", choices=["twitch", "youtube", "rtsp"], help="Stream to platform")
    parser.add_argument("--quality", default="720p", help="Stream quality")
    parser.add_argument("--webcam", action="store_true", help="Include webcam")
    parser.add_argument("--list-presets", action="store_true", help="List CRT presets")
    parser.add_argument("--favorites", action="store_true", help="List favorites")
    parser.add_argument("--history", action="store_true", help="Show history")
    parser.add_argument("--create-playlist", help="Create streaming playlist")
    args = parser.parse_args()

    launcher = DemoLauncher()

    if args.list_presets:
        print("📺 CRT Presets:")
        for slug, preset in CRT_PRESETS.items():
            print(f"  - {preset['name']}")
        return 0

    if args.favorites:
        favs = launcher.db.get_favorites()
        print("❤️ Favorites:")
        for demo_id, meta in favs.items():
            info = launcher.get_demo_info(demo_id)
            name = info.get("name", "Unknown")
            print(f"  - {demo_id}: {name} (tags: {meta.get('tags', [])})")
        return 0

    if args.history:
        hist = launcher.db.get_history()
        print("🕰️  History:")
        for entry in hist[:10]:
            info = launcher.get_demo_info(entry["pouet_id"])
            name = info.get("name", "Unknown")
            print(f"  - {entry['played_at'][:10]}: {name} ({entry['platform']})")
        return 0

    if args.search:
        results = launcher.search(args.search)
        print(f"🔎 Search results for '{args.search}':")
        for r in results[:10]:
            print(f"  - {r['id']}: {r['name']} ({r.get('type', '')})")
        return 0

    if args.demo:
        stream_platform = StreamPlatform(args.stream) if args.stream else None
        launcher.launch(
            pouet_id=args.demo,
            platform=args.platform,
            stream_to=stream_platform,
            quality=args.quality,
            with_webcam=args.webcam,
        )
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())