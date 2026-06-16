#!/usr/bin/env python3
"""Save stream keys to showet configuration.

Usage:
    save_stream_key.py --platform twitch --key YOUR_STREAM_KEY
    save_stream_key.py --platform youtube --key YOUR_STREAM_KEY
"""

import argparse
from streaming import setup_stream_key


def main():
    parser = argparse.ArgumentParser(description="Save stream key to showet config")
    parser.add_argument("--platform", required=True, 
                        choices=["twitch", "youtube", "facebook", "custom"])
    parser.add_argument("--key", required=True, help="Stream key to save")
    args = parser.parse_args()
    
    setup_stream_key(args.platform, args.key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())