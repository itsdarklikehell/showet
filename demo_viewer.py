#!/usr/bin/env python3
"""Demo metadata viewer and formatter for Showet.

Provides rich information display for demoscene productions.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path
from typing import Optional, Dict, Any


def fetch_demo_metadata(pouet_id: int) -> Optional[Dict[str, Any]]:
    """Fetch complete demo metadata from Pouet.net.
    
    Args:
        pouet_id: Pouet.net production ID
    
    Returns:
        Demo metadata dict or None on error
    """
    url = f"http://api.pouet.net/v1/prod/?id={pouet_id}"
    try:
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read().decode())
        return data.get("prod")
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return None


def format_demo_info(demo: Dict[str, Any]) -> str:
    """Format demo information for display.
    
    Args:
        demo: Demo metadata dict
    
    Returns:
        Formatted string for terminal display
    """
    lines = []
    lines.append(f"🎵 {demo.get('name', 'Unknown')}")
    lines.append("═" * 50)
    
    # Byline
    if demo.get("groups"):
        by = ", ".join(g.get("name", "") for g in demo["groups"])
        if by:
            lines.append(f"👥 By: {by}")
    
    # Type and year
    demo_type = demo.get("type", "Unknown")
    lines.append(f"📋 Type: {demo_type}")
    
    # Platform support
    platforms = demo.get("platforms", {})
    if platforms:
        platform_names = [p.get("name", "") for p in platforms.values()]
        lines.append(f"💻 Platforms: {', '.join(platform_names[:3])}")
        if len(platform_names) > 3:
            lines.append(f"              ... and {len(platform_names) - 3} more")
    
    # Party info
    if demo.get("party"):
        party = demo["party"].get("name", "")
        year = demo.get("year", "")
        if party:
            lines.append(f"🏆 Party: {party} {year}")
    
    # Scores
    if demo.get("score"):
        lines.append(f"⭐ Score: {demo['score']}")
    
    # Tags
    tags = demo.get("tags", [])
    if tags:
        tag_names = [t.get("name", "") for t in tags][:5]
        lines.append(f"🔖 Tags: {', '.join(tag_names)}")
    
    # Release date
    if demo.get("release_date"):
        lines.append(f"📅 Released: {demo['release_date']}")
    
    # Download info
    download = demo.get("download", "")
    if download:
        lines.append(f"📥 Download: {download[:60]}...")
    
    return "\n".join(lines)


def display_demo_info(pouet_id: int, with_crt: bool = True) -> str:
    """Display demo info with optional CRT styling.
    
    Args:
        pouet_id: Pouet.net production ID
        with_crt: Add CRT-style formatting
    
    Returns:
        Formatted demo info string
    """
    demo = fetch_demo_metadata(pouet_id)
    if not demo:
        return f"❌ Could not fetch demo {pouet_id}"
    
    info = format_demo_info(demo)
    
    if with_crt:
        # Add CRT-style borders
        lines = info.split("\n")
        width = max(len(line) for line in lines)
        top = "╔" + "═" * (width + 2) + "╗"
        bottom = "╚" + "═" * (width + 2) + "╝"
        bordered = [top]
        for line in lines:
            bordered.append(f"║ {line.ljust(width)} ║")
        bordered.append(bottom)
        return "\n".join(bordered)
    
    return info


def generate_stream_overlay(demo_id: int) -> str:
    """Generate overlay text for streaming.
    
    Args:
        demo_id: Pouet.net production ID
    
    Returns:
        Overlay text string
    """
    demo = fetch_demo_metadata(demo_id)
    if not demo:
        return "Showet Demo Runner"
    
    name = demo.get("name", "Unknown")
    platforms = demo.get("platforms", {})
    platform = list(platforms.values())[0].get("slug", "") if platforms else ""
    
    return f"{name} • {platform.upper()}" if platform else name


if __name__ == "__main__":
    def main():
        import sys
        parser = argparse.ArgumentParser(description="Showet demo metadata viewer")
        parser.add_argument("--overlay", action="store_true", help="Output streaming overlay text only")
        parser.add_argument("--demo-id", type=int, required=True, help="Pouet.net demo ID")
        args = parser.parse_args()
        
        if args.overlay:
            print(generate_stream_overlay(args.demo_id))
        else:
            print(display_demo_info(args.demo_id))
    
    raise SystemExit(main())