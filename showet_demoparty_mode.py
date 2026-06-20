#!/usr/bin/env python3
"""Showet Demoparty Mode - Watch all demos from a specific demoparty.

Fetches all compo entries from a demoparty and plays them in sequence.
Supports pouet.net party search and scene.org archive integration.
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Optional

from showet_config import DEFAULT_TIMEOUT, CACHE_DIR
from scene_org_integration import SceneOrgClient
from showet_jukebox import generate_cross_source_playlist

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("showet.demoparty")

# Known demoparty keywords on scene.org
PARTY_KEYWORDS = {
    "assembly": "assembly",
    "revision": "revision",
    "breakpoint": "breakpoint",
    "forever": "forever",
    "x": "x-party",
    "the_party": "the_party",
}

# Compo categories by party
COMPO_CATEGORIES = [
    "64k_intro",
    "4k_intro",
    "combined_demo",
    "oldschool_demo",
    "newschool_demo",
    "graphics",
    "music",
]


def search_party_demos(party_name: str, year: Optional[str] = None) -> list[dict]:
    """Search for demos from a specific demoparty.
    
    Args:
        party_name: Name of the demoparty (assembly, revision, etc.)
        year: Optional year filter
        
    Returns:
        List of demo metadata
    """
    client = SceneOrgClient()
    demos = []
    
    # Build search pattern
    search_pattern = party_name
    if year:
        search_pattern = f"{party_name}_{year}"
    
    try:
        results = client.search_demos(search_pattern)
        for result in results[:50]:  # Limit to 50
            demos.append({
                "name": result.get("name", "Unknown"),
                "url": result.get("url", ""),
                "size": result.get("size", 0),
                "source": "scene_org",
            })
    except Exception as e:
        logger.warning("Scene.org search failed: %s", e)
    
    # Also search Pouet for party productions
    try:
        pouet_results = search_pouet_party(party_name, year)
        demos.extend(pouet_results[:20])
    except Exception as e:
        logger.warning("Pouet search failed: %s", e)
    
    return demos


def search_pouet_party(party_name: str, year: Optional[str] = None) -> list[dict]:
    """Search Pouet.net for party productions.
    
    Args:
        party_name: Party name
        year: Optional year
        
    Returns:
        List of demo metadata
    """
    demos = []
    
    # Pouet has a prods endpoint we can search
    url = f"http://api.pouet.net/v1/prod/?search={party_name}"
    if year:
        url += f"&year={year}"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Showet/3.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            for prod in data.get("prods", [])[:20]:
                demos.append({
                    "id": prod.get("id"),
                    "name": prod.get("name", "Unknown"),
                    "type": prod.get("type", ""),
                    "source": "pouet",
                    "party": prod.get("party", party_name),
                })
    except Exception as e:
        logger.debug("Pouet API error: %s", e)
    
    return demos


def demoparty_watch(
    party_name: str,
    year: Optional[str] = None,
    category: Optional[str] = None,
    sequential: bool = True,
    loop_repeat: bool = False,
) -> int:
    """Watch all demos from a demoparty.
    
    Args:
        party_name: Name of the demoparty
        year: Optional year (defaults to latest)
        category: Optional compo category filter
        sequential: Play in order (True) or shuffle (False)
        loop_repeat: Loop repeat mode
        
    Returns:
        Number of demos found
    """
    demos = search_party_demos(party_name, year)
    
    if not demos:
        print(f"No demos found for {party_name}")
        return 0
    
    print(f"\n🎮 {party_name.upper()} Demoparty Mode")
    print(f"Found {len(demos)} demos\n")
    
    # Separate Pouet and scene.org IDs
    pouet_ids = [d["id"] for d in demos if d.get("source") == "pouet" and d.get("id")]
    scene_names = [d["name"] for d in demos if d.get("source") == "scene_org"]
    
    # Generate playlist summary
    playlist = generate_cross_source_playlist(
        pouet_ids=pouet_ids,
        scene_org_names=scene_names,
    )
    
    # Print the lineup
    for i, demo in enumerate(playlist, 1):
        loops = "🔄" if demo.get("loops") else "▶"
        print(f"  {i:2}. {loops} {demo.get('title', 'Unknown')}")
    
    print()
    
    # Launch jukebox with these demos
    mode = "sequential" if sequential else "shuffle"
    repeat = "one" if loop_repeat else "none"
    
    jukebox_cmd = [
        "showet-jukebox",
        "--source", "mixed",
    ]
    
    if pouet_ids:
        jukebox_cmd.extend(["--ids"] + pouet_ids)
    
    if scene_names:
        jukebox_cmd.extend(["--scene-org-names"] + scene_names)
    
    jukebox_cmd.extend([
        "--mode", mode,
        "--repeat", repeat,
    ])
    
    print("Starting playback...")
    try:
        subprocess.run(jukebox_cmd, cwd=Path(__file__).parent)
    except Exception as e:
        logger.error("Failed to start jukebox: %s", e)
    
    return len(demos)


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Showet Demoparty Mode - Watch all demos from a party",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("party", nargs="?", help="Demoparty name (assembly, revision, breakpoint)")
    parser.add_argument("--year", "-y", help="Year (e.g., 2024)")
    parser.add_argument("--category", "-c", help="Compo category filter")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle order instead of sequential")
    parser.add_argument("--loop-repeat", action="store_true", help="Loop repeat mode")
    parser.add_argument("--list-parties", action="store_true", help="List known demoparties")
    args = parser.parse_args()

    if args.list_parties:
        print("Known demoparties:")
        for name in PARTY_KEYWORDS.keys():
            print(f"  - {name}")
        return 0

    if not args.party:
        print("Usage: showet-demoparty <party> [options]")
        print("\nKnown parties: assembly, revision, breakpoint, forever, x")
        parser.print_help()
        return 1

    party_name = args.party.lower()
    if party_name in PARTY_KEYWORDS:
        party_name = PARTY_KEYWORDS[party_name]
    
    return demoparty_watch(
        party_name=party_name,
        year=args.year,
        category=args.category,
        sequential=not args.shuffle,
        loop_repeat=args.loop_repeat,
    )


if __name__ == "__main__":
    raise SystemExit(main())