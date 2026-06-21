"""CLI module for Showet v4.0.

Unified command-line interface for demo running, streaming, and jukebox modes.
"""

from __future__ import annotations

import argparse
import sys


def create_main_parser() -> argparse.ArgumentParser:
    """Create main argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="showet",
        description="Showet v4.0 - The definitive demoscene demo-runner",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a demo by ID or path")
    run_parser.add_argument("source", help="Pouet.net ID or file path")
    run_parser.add_argument("--fullscreen", "-f", action="store_true")

    # Jukebox command
    jb_parser = subparsers.add_parser("jukebox", help="Continuous demo playback")
    jb_parser.add_argument("--ids", type=int, nargs="+", help="Demo IDs to play")
    jb_parser.add_argument("--shuffle", action="store_true", default=True)
    jb_parser.add_argument("--loops", type=int, default=3, help="Max loops per demo")

    # Stream command
    stream_parser = subparsers.add_parser("stream", help="Stream demos to platforms")
    stream_parser.add_argument("--platform", choices=["twitch", "youtube", "rtsp"], default="rtsp")
    stream_parser.add_argument("--demo", type=int, help="Demo ID to stream")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for Showet CLI."""
    parser = create_main_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        from showet.core.executor import execute_demo
        try:
            demo_id = int(args.source)
            # Would need to fetch and run demo
        except ValueError:
            return execute_demo(args.source, fullscreen=args.fullscreen)
    elif args.command == "jukebox":
        from showet.core.jukebox import jukebox_mode
        if args.ids:
            return jukebox_mode(demo_ids=args.ids, loop_limit=args.loops)
    elif args.command == "stream":
        from showet.utils.stream_manager import StreamManager, StreamConfig, StreamPlatform
        # Stream setup
    else:
        parser.print_help()
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())