#!/usr/bin/env python3
"""Showet Demo Browser - List/search demos across pouet.net and scene.org."""

import sys
import subprocess
import json
from pathlib import Path


def search_pouet(query):
    """Search Pouet.net for demos."""
    try:
        result = subprocess.run(
            ["showet", "--search", query],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result.stdout)
    except Exception as e:
        print(f"Error searching Pouet: {e}")


def search_scene_org(query):
    """Search scene.org archives."""
    try:
        result = subprocess.run(
            ["scene-org", "--search", query],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result.stdout)
    except Exception as e:
        print(f"Error searching scene.org: {e}")


def list_platform_demos(platform):
    """List demos for a specific platform."""
    # Platform groups
    platform_groups = {
        "amiga": ["amiga", "commodore amiga"],
        "c64": ["c64", "commodore 64"],
        "dos": ["dos", "ms-dos", "pc"],
        "nes": ["nes", "famicom", "nintendo"],
        "snes": ["snes", "super famicom"],
        "megadrive": ["megadrive", "genesis", "sega"],
    }
    
    search_term = " ".join(platform_groups.get(platform.lower(), [platform]))
    print(f"🔍 Searching for {platform} demos...")
    
    # Use scene-org to search
    search_scene_org(search_term)


def show_hall_of_fame():
    """Display legendary demos."""
    hof = [
        {"name": "Second Reality", "group": "Future Crew", "year": 1993, "platform": "Amiga"},
        {"name": "Heaven Seven", "group": "Conspiracy", "year": 2003, "platform": "Amiga"},
        {"name": "Systematic", "group": "Farbrausch", "year": 2002, "platform": "DOS"},
        {"name": "Especially for You", "group": "Fairlight", "year": 2009, "platform": "C64"},
        {"name": "Bad Apple!!", "group": "ZUN", "year": 2007, "platform": "NES"},
    ]
    
    print("🏆 SHOWET HALL OF FAME")
    print("=" * 50)
    for demo in hof:
        print(f"  {demo['name']} by {demo['group']} ({demo['year']}) - {demo['platform']}")


def main():
    if len(sys.argv) < 2:
        print("🎮 Showet Demo Browser")
        print("\nUsage: showet-browser <command>")
        print("\nCommands:")
        print("  search <query>     - Search all sources")
        print("  pouet <query>      - Search Pouet.net")
        print("  scene <query>      - Search scene.org")
        print("  platform <name>    - Demo search for platform")
        print("  hof                - Show Hall of Fame")
        print("\nExamples:")
        print("  showet-browser platform commodore_64")
        print("  showet-browser hof")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "hof":
        show_hall_of_fame()
    elif cmd == "search" and len(sys.argv) > 2:
        search_pouet(sys.argv[2])
    elif cmd == "pouet" and len(sys.argv) > 2:
        search_pouet(sys.argv[2])
    elif cmd == "scene" and len(sys.argv) > 2:
        search_scene_org(sys.argv[2])
    elif cmd == "platform" and len(sys.argv) > 2:
        list_platform_demos(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()