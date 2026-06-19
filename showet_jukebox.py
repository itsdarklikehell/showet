#!/usr/bin/env python3
"""Showet Jukebox - Loop/shuffle/repeat demo playback with intelligent loop detection.

Intelligently plays demos from pouet.net, scene.org, and modarchive.org with loop detection
and configurable shuffle behavior. Looped demos (like 64k/4k intros) play up to 3 times in shuffle mode.
Supports all major demoscene sources with unified metadata handling.
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any, Optional

from showet_config import DEBUG, DEFAULT_TIMEOUT, DEFAULT_LOOP_LIMIT, LOOPED_KEYWORDS, CACHE_DIR
from scene_org_integration import SceneOrgClient
from modarchive_integration import ModArchiveAPI

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("showet.jukebox")

# Demo type mappings for loop detection
LOOPED_DEMO_TYPES = frozenset(["64k", "4k", "intro", "wild"])

# Demo type to estimated duration mapping (seconds)
DEMO_DURATION_ESTIMATES = {
    "64k": 180,
    "4k": 120,
    "intro": 90,
    "demo": 300,
    "diskmag": 600,
    "wild": 120,
    "zx_spectrum": 150,
    "commodore_64": 180,
    "amiga": 240,
    "nes": 60,
    "snes": 90,
    "dos": 200,
    "windows": 180,
}

# Module format to estimated duration
MODULE_DURATION_ESTIMATES = {
    "mod": 180,
    "s3m": 120,
    "xm": 150,
    "it": 200,
}


def get_demo_info(pouet_id: int) -> Optional[dict]:
    """Fetch demo metadata from Pouet.net.
    
    Args:
        pouet_id: Pouet.net production ID
        
    Returns:
        Demo metadata dict or None if fetch fails
    """
    try:
        url = f"http://api.pouet.net/v1/prod/?id={pouet_id}"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("prod")
    except Exception as e:
        logger.error("Failed to fetch demo %d: %s", pouet_id, e)
        return None


def get_scene_org_demo(demo_name: str) -> Optional[dict]:
    """Fetch demo metadata from scene.org.
    
    Args:
        demo_name: Demo filename or identifier on scene.org
        
    Returns:
        Demo metadata dict or None
    """
    client = SceneOrgClient()
    try:
        results = client.search_demos(demo_name)
        return results[0] if results else None
    except Exception as e:
        logger.error("Failed to fetch scene.org demo %s: %s", demo_name, e)
        return None


def is_looped_demo(demo_info: Optional[dict], source: str = "pouet") -> bool:
    """Detect if a demo loops based on metadata and type.
    
    Checks multiple sources:
    - Pouet.net: demo type (64k/4k intros) and tags
    - Scene.org: filename patterns and party context
    - ModArchive: module track characteristics
    
    Args:
        demo_info: Demo metadata dictionary
        source: Source identifier (pouet, scene_org, modarchive)
        
    Returns:
        True if demo is likely looped, False otherwise
    """
    if not demo_info:
        return False

    # Source-specific detection
    if source == "pouet":
        return _detect_pouet_loop(demo_info)
    elif source == "scene_org":
        return _detect_scene_org_loop(demo_info)
    elif source == "modarchive":
        return _detect_modarchive_loop(demo_info)
    
    return False


def _detect_pouet_loop(demo_info: dict) -> bool:
    """Detect loop status from Pouet.net metadata.
    
    Uses heuristics:
    - Demo type (64k/4k intros)
    - Tags/keywords (loop, looping)
    - Rating (high-rated intros often loop)
    - Rank position
    """
    # Rating heuristic: high-rated intros often loop
    rating = demo_info.get("rating", 0)
    demo_type = demo_info.get("type", "").lower()
    
    if rating and rating > 4.0 and "intro" in demo_type:
        return True
    
    # Check demo type (64k/4k intros)
    if any(t in demo_type for t in LOOPED_DEMO_TYPES):
        return True

    # Check tags/keywords
    tags = demo_info.get("tags", "")
    if tags:
        tags_lower = tags.lower()
        for keyword in LOOPED_KEYWORDS:
            if keyword in tags_lower:
                return True

    return False


def _detect_scene_org_loop(demo_info: dict) -> bool:
    """Detect loop status from scene.org demo.
    
    Scene.org demos loop detection based on:
    - Filename patterns (loop, endless, replay, forever)
    - Party context (certain parties favor looping intros)
    - Demo type indicators in path
    - File size heuristics (smaller files often loop)
    
    Returns:
        bool: True if likely looped
    """
    name = demo_info.get("name", "").lower()
    size = demo_info.get("size", 0)
    
    # Common loop-related patterns in filenames
    loop_patterns = ["loop", "replay", "forever", "endless", "continuous"]
    if any(p in name for p in loop_patterns):
        return True
    
    # Check for intros (often looping)
    if any(p in name for p in ["64k", "4k", "intro"]):
        return True
    
    # Size heuristic: very small demos (<5MB) often loop infinitely
    if size and size < 5 * 1024 * 1024:  # 5MB
        return True
    
    return False


def _detect_modarchive_loop(demo_info: dict) -> bool:
    """Detect if a music module is suitable for looping.
    
    Modules with longer durations or mix/remix patterns are good for looping.
    """
    name = demo_info.get("title", "").lower()
    
    # Common patterns for long tracks
    if any(p in name for p in ["medley", "mix", "megamix", "remix"]):
        return True
    
    return False


def estimate_demo_duration(demo_info: Optional[dict], source: str = "pouet") -> int:
    """Estimate demo duration based on type, platform, and metadata.
    
    Uses multiple heuristics:
    - Demo type (64k intros are typically 2-3 min)
    - Platform (C64 demos differ from PC demos)
    - File size (larger files often mean longer demos)
    - Ratings (higher rated demos often longer)
    
    Args:
        demo_info: Demo metadata dictionary
        source: Source identifier (pouet, scene_org, modarchive)
        
    Returns:
        Estimated duration in seconds
    """
    if not demo_info:
        return 180  # Default 3 minutes
    
    demo_type = ""
    platform = ""
    
    if source == "pouet":
        demo_type = demo_info.get("type", "").lower()
        # Try to extract platform from demo info
        platform_info = demo_info.get("platform", "")
        if platform_info:
            platform = platform_info.lower()
    elif source == "scene_org":
        # Extract from filename/path
        name = demo_info.get("name", "").lower()
        for p in DEMO_DURATION_ESTIMATES.keys():
            if p in name:
                platform = p
                break
    elif source == "modarchive":
        # Module duration based on format
        module_format = demo_info.get("format", "").lower()
        return MODULE_DURATION_ESTIMATES.get(module_format, 180)
    
    # Check type-based estimates first - but skip "demo" key which is too generic
    for demo_type_key, duration in DEMO_DURATION_ESTIMATES.items():
        if demo_type_key != "demo" and demo_type_key in demo_type:
            return duration
    
    # Check platform-based estimates - check platform before generic "demo" type
    for platform_key, duration in DEMO_DURATION_ESTIMATES.items():
        if platform_key in platform:
            return duration
    
    # Finally check for generic demo type
    if "demo" in demo_type:
        return DEMO_DURATION_ESTIMATES["demo"]
    
    return 180  # Default fallback


def generate_cross_source_playlist(
    pouet_ids: Optional[list[int]] = None,
    scene_org_names: Optional[list[str]] = None,
    modarchive_ids: Optional[list[int]] = None,
    platform: Optional[str] = None,
) -> list[dict]:
    """Generate a unified playlist from multiple sources.
    
    Args:
        pouet_ids: List of Pouet.net production IDs
        scene_org_names: List of scene.org demo filenames
        modarchive_ids: List of ModArchive module IDs
        platform: Optional platform filter
        
    Returns:
        List of unified demo metadata dictionaries
    """
    playlist = []
    
    # Fetch Pouet demos
    if pouet_ids:
        for pid in pouet_ids:
            demo_info = get_demo_info(pid)
            if demo_info:
                if platform and platform not in str(demo_info.get("platform", "")).lower():
                    continue
                playlist.append({
                    "id": pid,
                    "source": "pouet",
                    "title": demo_info.get("name", f"Pouet #{pid}"),
                    "type": demo_info.get("type", "demo"),
                    "loops": is_looped_demo(demo_info, "pouet"),
                    "duration": estimate_demo_duration(demo_info, "pouet"),
                    "platform": demo_info.get("platform", "unknown"),
                })
    
    # Fetch scene.org demos
    if scene_org_names:
        client = SceneOrgClient()
        for demo_name in scene_org_names:
            try:
                results = client.search_demos(demo_name)
                for result in results[:1]:  # Take first match
                    if platform and platform not in result.get("name", "").lower():
                        continue
                    playlist.append({
                        "id": result.get("url", demo_name),
                        "source": "scene_org",
                        "title": result.get("name", demo_name),
                        "type": "demo",
                        "loops": is_looped_demo(result, "scene_org"),
                        "duration": estimate_demo_duration(result, "scene_org"),
                        "platform": "unknown",
                    })
            except Exception as e:
                logger.warning("Could not fetch scene.org demo %s: %s", demo_name, e)
    
    # Fetch ModArchive modules
    if modarchive_ids:
        api = ModArchiveAPI()
        for mid in modarchive_ids:
            module = api.get_module(mid)
            if module:
                playlist.append({
                    "id": mid,
                    "source": "modarchive",
                    "title": module.get("title", f"Module #{mid}"),
                    "type": "module",
                    "format": module.get("format", "mod"),
                    "loops": is_looped_demo(module, "modarchive"),
                    "duration": estimate_demo_duration(module, "modarchive"),
                    "platform": "music",
                })
    
    return playlist


def print_playlist_summary(playlist: list[dict]) -> None:
    """Print a summary of the generated playlist.
    
    Args:
        playlist: List of demo metadata dictionaries
    """
    total_duration = sum(d["duration"] for d in playlist)
    looped_count = sum(1 for d in playlist if d.get("loops"))
    
    print(f"\n📋 Playlist Summary:")
    print(f"  Total demos: {len(playlist)}")
    print(f"  Looped demos: {looped_count}")
    print(f"  Estimated total duration: {total_duration // 60}m {total_duration % 60}s")
    
    # Group by source
    by_source = {}
    for d in playlist:
        src = d["source"]
        by_source[src] = by_source.get(src, 0) + 1
    
    print(f"  Sources: {', '.join(f'{k}({v})' for k, v in by_source.items())}")


def run_demo(pouet_id: int, timeout: int = DEFAULT_TIMEOUT) -> int:
    """Run a single demo and return its exit code.
    
    Args:
        pouet_id: Pouet.net production ID
        timeout: Maximum seconds to wait for demo completion
        
    Returns:
        Process exit code (0 for success)
    """
    try:
        result = subprocess.run(
            ["python3", "-m", "showet", str(pouet_id)],
            timeout=timeout,
            capture_output=True,
            cwd=Path(__file__).parent,
        )
        return result.returncode
    except subprocess.TimeoutExpired:
        logger.warning("Demo %d timed out after %ds", pouet_id, timeout)
        return -1
    except Exception as e:
        logger.error("Error running demo %d: %s", pouet_id, e)
        return -1


def play_demo_with_loops(pouet_id: int, loop_count: int, timeout: int) -> int:
    """Play a demo the specified number of times.
    
    Args:
        pouet_id: Pouet.net production ID
        loop_count: Number of times to loop the demo
        timeout: Maximum seconds per playback
        
    Returns:
        Exit code (0 for success)
    """
    logger.info("▶ Playing demo %d (%d loops)", pouet_id, loop_count)

    for loop in range(loop_count):
        if loop > 0:
            print(f"  Loop {loop + 1}/{loop_count}")
            logger.debug("Starting loop %d for demo %d", loop + 1, pouet_id)
        retcode = run_demo(pouet_id, timeout)
        if retcode != 0:
            break

    return 0


def jukebox_mode(
    demo_ids: list[int],
    mode: str = "shuffle",
    repeat: str = "all",
    loop_limit: int = DEFAULT_LOOP_LIMIT,
    timeout: int = DEFAULT_TIMEOUT,
    source: str = "pouet",
) -> int:
    """Run demos in jukebox mode.

    Args:
        demo_ids: List of demo IDs (Pouet IDs or scene.org demo names)
        mode: "shuffle", "random", or "sequential"
        repeat: "all", "one", or "none"
        loop_limit: Max loops for looped demos in shuffle mode
        timeout: Max seconds per demo loop
        source: Source of demo IDs (pouet, scene_org, modarchive)

    Returns:
        Exit code
    """
    if not demo_ids:
        print("No demos specified")
        return 1

    import random
    
    # Get demo metadata for loop detection
    demo_loop_status = {}
    for pid in demo_ids:
        demo_info = get_demo_info(pid) if source == "pouet" else None
        demo_loop_status[pid] = is_looped_demo(demo_info, source) if demo_info else False

    # Determine playback order
    if mode == "random":
        ids_to_play = demo_ids.copy()
        random.shuffle(ids_to_play)
    elif mode == "shuffle":
        # Shuffle with loop detection
        ids_to_play = demo_ids.copy()
        random.shuffle(ids_to_play)
    else:
        ids_to_play = demo_ids.copy()

    # Play demos
    played = set()
    for pid in ids_to_play:
        if pid in played and repeat == "none":
            continue
        played.add(pid)

        # Determine loop count
        # Looped demos play up to loop_limit times in shuffle
        # Non-looping demos play once
        if mode == "shuffle" and demo_loop_status.get(pid, False):
            loops = min(loop_limit, 3)  # Cap at 3 for shuffle
        else:
            loops = 1

        play_demo_with_loops(pid, loops, timeout)

        # Handle repeat "one"
        if repeat == "one":
            # Stay on this demo - loop continuously
            print(f"🔁 Repeating demo {pid} forever...")
            logger.info("Entering repeat-one mode for demo %d", pid)
            while True:
                play_demo_with_loops(pid, loops, timeout)

    return 0


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Showet Jukebox - Continuous demo playback with loop/shuffle/repeat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--ids", type=int, nargs="+", help="Pouet.net demo IDs to play")
    parser.add_argument(
        "--source",
        choices=["pouet", "scene_org", "modarchive"],
        default="pouet",
        help="Source for demo IDs",
    )
    parser.add_argument(
        "--mode",
        choices=["shuffle", "random", "sequential"],
        default="shuffle",
        help="Playback mode (default: shuffle)",
    )
    parser.add_argument(
        "--repeat",
        choices=["all", "one", "none"],
        default="all",
        help="Repeat mode (default: all)",
    )
    parser.add_argument(
        "--loops",
        type=int,
        default=3,
        help="Loop limit for looped demos (default: 3)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Max seconds per demo (default: 300)",
    )
    parser.add_argument("--platform", type=str, help="Filter by platform slug")
    # Cross-source playlist options
    parser.add_argument("--scene-org-names", type=str, nargs="+", help="Scene.org demo filenames")
    parser.add_argument("--modarchive-ids", type=int, nargs="+", help="ModArchive module IDs")
    parser.add_argument("--generate-playlist", action="store_true", help="Generate and display playlist without playing")
    args = parser.parse_args()

    if args.generate_playlist:
        playlist = generate_cross_source_playlist(
            pouet_ids=args.ids,
            scene_org_names=args.scene_org_names,
            modarchive_ids=args.modarchive_ids,
            platform=args.platform,
        )
        print_playlist_summary(playlist)
        return 0

    if not args.ids and not args.scene_org_names and not args.modarchive_ids:
        print("Usage: showet-jukebox --ids ID1 ID2 ... [options]")
        print("\nOptions:")
        print("  --ids ID1 ID2 ...                 Pouet.net demo IDs to play")
        print("  --scene-org-names NAME1 NAME2 ...   Scene.org demo filenames")
        print("  --modarchive-ids ID1 ID2 ...        ModArchive module IDs")
        print("  --generate-playlist                 Show playlist summary without playing")
        print("  --source pouet|scene_org|modarchive Demo ID source")
        print("  --mode shuffle|random|sequential    Playback order")
        print("  --repeat all|one|none             Repeat mode")
        print("  --loops N                         Loop count for looped demos (default: 3)")
        print("  --timeout N                       Per-demo timeout in seconds")
        print("  --platform SLUG                   Filter by platform")
        return 1

    return jukebox_mode(
        demo_ids=args.ids or [],
        mode=args.mode,
        repeat=args.repeat,
        loop_limit=args.loops,
        timeout=args.timeout,
        source=args.source,
    )


if __name__ == "__main__":
    raise SystemExit(main())