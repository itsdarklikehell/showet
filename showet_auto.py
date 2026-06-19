#!/usr/bin/env python3
"""Showet Auto - Automated demo discovery and playback.

Automatically finds and plays demos based on criteria like:
- Random trending demos
- Platform preference
- Demo type (intro, demo, 64k, etc.)
- Time-based rotation
"""

import argparse
import json
import random
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


def get_trending_demos(limit: int = 20) -> list[dict]:
    """Get trending demos from Pouet.net."""
    queries = ["trending", "demo", "intro", "64k", "4k", "pc", "amiga", "c64"]
    results = []

    for query in queries:
        try:
            url = f"http://api.pouet.net/v1/search/prod/?q={query}"
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode())

            for prod_id, prod in data.get("results", {}).items():
                if len(results) >= limit:
                    break
                results.append({
                    "id": int(prod_id),
                    "name": prod.get("name", "Unknown"),
                    "type": prod.get("type", ""),
                    "score": prod.get("score", 0),
                })
        except Exception:
            continue

    return results


def get_demo_by_platform(platform: str, limit: int = 20) -> list[dict]:
    """Get demos for a specific platform."""
    try:
        url = f"http://api.pouet.net/v1/search/prod/?platform={platform}"
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read().decode())

        results = []
        for prod_id, prod in list(data.get("results", {}).items())[:limit]:
            results.append({
                "id": int(prod_id),
                "name": prod.get("name", "Unknown"),
                "type": prod.get("type", ""),
            })
        return results
    except Exception:
        return []


def auto_play(
    mode: str = "trending",
    platform: str = None,
    count: int = 10,
    timeout: int = 300,
    loop_looped: bool = True,
) -> int:
    """
    Automatically play demos.

    Args:
        mode: "trending", "platform", "random", or "schedule"
        platform: Platform slug (for platform mode)
        count: Number of demos to play
        timeout: Seconds per demo
        loop_looped: Loop demos that are detected as looping

    Returns:
        Exit code
    """
    # Get demo list
    if mode == "trending":
        demos = get_trending_demos(limit=count * 2)
    elif mode == "platform" and platform:
        demos = get_demo_by_platform(platform, limit=count * 2)
    else:
        demos = get_trending_demos(limit=count * 2)

    if not demos:
        print("No demos found")
        return 1

    # Randomly select if we have more than needed
    selected = demos[:count] if len(demos) <= count else random.sample(demos, count)

    print(f"▶ Auto-playing {len(selected)} demos ({mode} mode)")

    for demo in selected:
        demo_id = demo["id"]
        demo_name = demo.get("name", "Unknown")
        demo_type = demo.get("type", "")

        print(f"\nDemo: {demo_name} (ID: {demo_id}, Type: {demo_type})")

        # Check if 64k/4k (typically loops)
        loops = 3 if loop_looped and ("64k" in demo_type.lower() or "4k" in demo_type.lower()) else 1

        # Run the demo
        try:
            result = subprocess.run(
                ["python3", "-m", "showet", str(demo_id)],
                timeout=timeout,
                cwd=Path(__file__).parent,
            )
        except subprocess.TimeoutExpired:
            print(f"  Demo timed out after {timeout}s")
            continue

    return 0


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Showet Auto - Automated demo discovery and playback",
    )
    parser.add_argument(
        "--mode",
        choices=["trending", "platform", "random", "schedule"],
        default="trending",
        help="Auto mode",
    )
    parser.add_argument("--platform", type=str, help="Platform for filtering")
    parser.add_argument(
        "--count", type=int, default=10, help="Number of demos to play"
    )
    parser.add_argument(
        "--timeout", type=int, default=300, help="Timeout per demo in seconds"
    )
    parser.add_argument(
        "--no-loop", action="store_true", help="Don't loop 64k/4k intros"
    )
    args = parser.parse_args()

    return auto_play(
        mode=args.mode,
        platform=args.platform,
        count=args.count,
        timeout=args.timeout,
        loop_looped=not args.no_loop,
    )


if __name__ == "__main__":
    raise SystemExit(main())