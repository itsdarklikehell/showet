#!/usr/bin/env python3
"""Showet streaming CLI - Stream demos to Twitch/YouTube/RTSP.

Usage:
    showet-stream --platform twitch --demo 12345
    showet-stream --rtsp --port 8554
"""

import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Showet live streaming")
    parser.add_argument("--platform", choices=["twitch", "youtube", "rtsp"], default="twitch")
    parser.add_argument("--stream-key", help="Stream key (or set SHOWET_STREAM_KEY env var)")
    parser.add_argument("--rtsp", action="store_true", help="Use RTSP server instead of RTMP")
    parser.add_argument("--port", type=int, default=8554, help="RTSP port (default: 8554)")
    parser.add_argument("--demo", type=int, help="Pouet.net demo ID to stream")
    parser.add_argument("--quality", default="720p", help="Stream quality (480p/720p/1080p)")
    return parser.parse_args()


def main():
    args = parse_args()
    
    stream_key = args.stream_key or os.environ.get("SHOWET_STREAM_KEY", "")
    
    if args.rtsp:
        from streaming import StreamManager
        streamer = StreamManager()
        streamer.start_rtsp_server(port=args.port)
    elif args.platform == "twitch" and stream_key:
        from streaming import StreamManager, format_twitch_url
        streamer = StreamManager()
        streamer.setup_rtmp(format_twitch_url(stream_key), "twitch", args.quality)
        streamer.start_stream()
    elif args.platform == "youtube" and stream_key:
        from streaming import StreamManager, format_youtube_url
        streamer = StreamManager()
        streamer.setup_rtmp(format_youtube_url(stream_key), "youtube", args.quality)
        streamer.start_stream()
    else:
        print("❌ No stream key provided. Set SHOWET_STREAM_KEY environment variable or use --stream-key")
        print("💡 Tip: Add 'export SHOWET_STREAM_KEY=your_key' to ~/.bashrc")
        return 1
    
    print(f"🎮 Demo: {args.demo or 'manual playback'}")
    print("Press Ctrl+C to stop streaming...")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())