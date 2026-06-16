#!/usr/bin/env python3
"""Showet streaming CLI - Stream demos to Twitch/YouTube/RTSP with overlays.

Usage:
    showet-stream --platform twitch --demo 12345
    showet-stream --platform youtube --quality 1080p --overlay "MyStream"
    showet-stream --rtsp --port 8554
    showet-stream --save-key twitch --key YOUR_STREAM_KEY
"""

import argparse
import os
import signal
import sys
from pathlib import Path

from streaming import (
    StreamConfig,
    StreamManager,
    StreamPlatform,
    setup_stream_key,
    get_stream_key,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Showet live streaming with demo overlay support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  showet-stream --platform twitch --demo 12345
  showet-stream --platform youtube --quality 1080p --demo 12345
  showet-stream --rtsp --port 8554 --fullscreen
  showet-stream --save-key twitch --key YOUR_KEY
  showet-stream --platform twitch --webcam --demo 12345

Supported platforms: twitch, youtube, facebook, custom, rtsp
Quality options: 480p, 720p, 1080p, 1440p, 4k
        """
    )
    parser.add_argument("--platform", choices=["twitch", "youtube", "facebook", "custom", "rtsp"],
                        default="twitch", help="Streaming platform")
    parser.add_argument("--stream-key", help="Stream key (or set SHOWET_STREAM_KEY env var)")
    parser.add_argument("--demo", type=int, help="Pouet.net demo ID to stream")
    parser.add_argument("--quality", default="720p",
                        choices=["480p", "720p", "1080p", "1440p", "4k"],
                        help="Stream quality")
    parser.add_argument("--overlay", default="", help="Overlay text on stream")
    parser.add_argument("--webcam", action="store_true", help="Include webcam overlay")
    parser.add_argument("--no-audio", action="store_true", help="Disable audio capture")
    parser.add_argument("--rtsp", action="store_true", help="Use RTSP server instead of RTMP")
    parser.add_argument("--rtsp-port", type=int, default=8554, help="RTSP port (default: 8554)")
    parser.add_argument("--save-key", choices=["twitch", "youtube", "facebook", "custom"],
                        help="Save stream key to config")
    parser.add_argument("--key", help="Stream key (used with --save-key)")
    parser.add_argument("--record", action="store_true", help="Record stream locally")
    parser.add_argument("--record-path", help="Path for local recording")
    parser.add_argument("--fullscreen", action="store_true", help="Stream in fullscreen mode")
    return parser.parse_args()


def main():
    args = parse_args()

    # Handle save-key option
    if args.save_key and args.key:
        setup_stream_key(args.save_key, args.key)
        return 0

    # Determine platform
    if args.rtsp:
        platform = StreamPlatform.RTSP
        stream_key = ""
    else:
        platform = StreamPlatform(args.platform)
        stream_key = args.stream_key or os.environ.get("SHOWET_STREAM_KEY", "")
        if not stream_key and not args.rtsp:
            stream_key = get_stream_key(args.platform)

    if not stream_key and platform != StreamPlatform.RTSP:
        print("❌ No stream key provided.")
        print("💡 Set SHOWET_STREAM_KEY env var, use --stream-key, or --save-key to store")
        return 1

    # Create config
    config = StreamConfig(
        platform=platform,
        stream_key=stream_key,
        quality=args.quality,
        include_audio=not args.no_audio,
        include_webcam=args.webcam,
        overlay_text=args.overlay,
        record_locally=args.record,
        record_path=args.record_path,
    )

    # Setup signal handler for graceful exit
    manager = StreamManager()
    manager.configure(config)

    def signal_handler(sig, frame):
        print("\n🛑 Stopping stream...")
        manager.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start appropriate stream type
    if args.rtsp:
        print("📡 Starting RTSP server...")
        manager.start_rtsp_server(port=args.rtsp_port)
        print("Press Ctrl+C to stop streaming...")
        try:
            if manager._rtsp_server:
                manager._rtsp_server.wait()
        except KeyboardInterrupt:
            pass
        manager.stop()
    else:
        # Launch the demo and stream it
        if args.demo:
            print(f"🎮 Fetching demo {args.demo}...")
            # Import and run the demo
            import showet
            from showet import create_platform_runners, run_production, build_arg_parser

            # Create custom args for the specific demo
            import argparse
            demo_ns = argparse.Namespace(
                pouetid=args.demo,
                platforms=False,
                random=False,
                fullscreen=args.fullscreen,
                audio=not args.no_audio,
                core=None
            )
            runners = create_platform_runners()

            # Get demo info for overlay
            try:
                import urllib.request
                import json
                url = f"http://api.pouet.net/v1/prod/?id={args.demo}"
                data = json.loads(urllib.request.urlopen(url).read().decode())
                demo_name = data.get("prod", {}).get("name", "")
                if demo_name and not args.overlay:
                    config.overlay_text = f"{demo_name}"
            except Exception as e:
                print(f"Note: Could not fetch demo info: {e}")

            print(f"🚀 Starting {args.platform} stream at {args.quality} quality...")
            manager.start(overlay_text=config.overlay_text)

            # Run the demo (will stream while running)
            try:
                result = run_production(demo_ns, runners)
            except KeyboardInterrupt:
                print("\n🛑 Stopping stream...")
            finally:
                manager.stop()
        else:
            # Manual streaming mode
            print(f"🚀 Starting {args.platform} stream at {args.quality} quality...")
            print("Press Ctrl+C to stop streaming...")
            manager.start(overlay_text=args.overlay)
            try:
                if manager._process:
                    manager._process.wait()
            except KeyboardInterrupt:
                manager.stop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())