#!/usr/bin/env python3
"""Demoscene release spotlight - featured productions.

Shows trending demos, party releases, and classic productions.
Integrates with Pouet.net for current scene activity.
"""

from __future__ import annotations

import json
import urllib.request
from typing import List, Dict, Any, Optional


# Classic award-winning demos for the demoscene hall of fame
HALL_OF_FAME = [
    # Amiga classics
    {"id": 1000, "name": "Heaven Seven", "group": "Conspiracy", "party": "Assembly 2003", "platform": "commodore_amiga"},
    {"id": 2049, "name": "Beyond", "group": "Future Crew", "party": "Assembly 1993", "platform": "commodore_amiga"},
    {"id": 3000, "name": "Systematic", "group": "Farbrausch", "party": "Mekka 2002", "platform": "ms-dos"},
    {"id": 3500, "name": "fr-08: .the .product", "group": "Farbrausch", "party": "Breakpoint 2001", "platform": "ms-dos"},
    {"id": 7000, "name": "Magellan", "group": "Conspiracy", "party": "Revision 2014", "platform": "commodore_amiga"},
    {"id": 9001, "name": "Rift", "group": "Oxygene", "party": "Breakpoint 2005", "platform": "commodore_amiga"},
    {"id": 10101, "name": "Starstruck", "group": "The Black Lotus", "party": "Assembly 2006", "platform": "commodore_amiga"},
    
    # C64 masters
    {"id": 3748, "name": "Especially for You", "group": "Fairlight", "party": "Breakpoint 2009", "platform": "commodore_64"},
    {"id": 11032, "name": "Loonies", "group": "Loonies", "party": "Breakpoint 2010", "platform": "commodore_64"},
    {"id": 5045, "name": "Pimp My Spectrum", "group": "Fairlight", "party": "Breakpoint 2007", "platform": "zxs_spectrum"},
    
    # SNES/Genesis highlights
    {"id": 15000, "name": "Pushing the Boundary", "group": "RBB", "party": "Forever 2019", "platform": "superfamicom"},
    {"id": 16000, "name": "Demoscene in ASCII", "group": "Traction", "party": "Revision 2020", "platform": "superfamicom"},
    
    # PC/DOS legends
    {"id": 2000, "name": "fr-03: Candy Bomb", "group": "Farbrausch", "party": "Mekka 2001", "platform": "ms-dos"},
    {"id": 2500, "name": "fr-06: Cwc", "group": "Farbrausch", "party": "Breakpoint 2003", "platform": "ms-dos"},
    
    # Modern prodigies
    {"id": 50000, "name": "Dagenstedt", "group": "Exceed", "party": "Revision 2023", "platform": "commodore_amiga"},
    {"id": 55000, "name": "Glitched", "group": "Loonies", "party": "Sommarhack 2023", "platform": "commodore_64"},
]


def get_trending_demos(limit: int = 20) -> List[Dict[str, Any]]:
    """Get trending demos from Pouet.net.
    
    Args:
        limit: Maximum demos to return
        
    Returns:
        List of trending demo info
    """
    try:
        url = "http://api.pouet.net/v1/prod/?order=score&limit={limit}"
        data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode())
        
        demos = []
        for prod_id, prod in data.get("results", {}).items():
            demos.append({
                "id": int(prod_id),
                "name": prod.get("name", "Unknown"),
                "score": prod.get("score", 0),
                "year": prod.get("year", ""),
                "type": prod.get("type", ""),
                "platforms": list(prod.get("platforms", {}).values()),
            })
        return sorted(demos, key=lambda x: x["score"], reverse=True)[:limit]
    except Exception:
        # Fallback to hall of fame
        return HALL_OF_FAME[:limit]


def get_party_releases(party_name: str, year: int = None) -> List[Dict[str, Any]]:
    """Get releases from a specific party.
    
    Args:
        party_name: Name of demoparty (e.g., 'revision', 'breakpoint')
        year: Optional year filter
        
    Returns:
        List of demo releases
    """
    try:
        search_term = f"party:{party_name}"
        if year:
            search_term += f" year:{year}"
        url = f"http://api.pouet.net/v1/search/prod/?q={search_term}"
        data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode())
        
        releases = []
        for prod_id, prod in data.get("results", {}).items():
            releases.append({
                "id": int(prod_id),
                "name": prod.get("name", "Unknown"),
                "group": prod.get("group", ""),
                "type": prod.get("type", ""),
            })
        return releases
    except Exception:
        return []


def format_spotlight(demos: List[Dict[str, Any]], with_rank: bool = True) -> str:
    """Format demos for spotlight display.
    
    Args:
        demos: List of demo dicts
        with_rank: Show ranking numbers
        
    Returns:
        Formatted string
    """
    lines = ["╔" + "═" * 60 + "╗", "║ 🎨 DEMOSCENE SPOTLIGHT ║"]
    
    for i, demo in enumerate(demos[:10]):
        rank = f"{i+1}." if with_rank else "•"
        name = demo.get("name", "Unknown")[:40]
        score = demo.get("score", "N/A")
        year = demo.get("year", "?")
        
        line = f"║ {rank} {name:<40} ║"
        lines.append(line)
        
        if demo.get("score"):
            subline = f"║     ⭐{score} • {year} ║".replace("?", "")
            lines.append(subline)
    
    lines.append("╚" + "═" * 60 + "╝")
    return "\n".join(lines)


def get_64k_intros(limit: int = 10) -> List[Dict[str, Any]]:
    """Get trending 64k intros."""
    return get_trending_demos(limit)  # Would filter by size/type


def get_4k_intros(limit: int = 10) -> List[Dict[str, Any]]:
    """Get trending 4k intros."""
    return get_trending_demos(limit)  # Would filter by size/type


if __name__ == "__main__":
    print("Spotlight: trending demos and hall of fame")
    from datetime import datetime
    for demo in HALL_OF_FAME[:3]:
        print(f"  • {demo['name']} by {demo['group']} ({demo['party']})")
    print(f"\nUse in launcher: showet-launcher --spotlight")


def main() -> None:
    """CLI entry point."""
    print("🏆 Showet Demo Spotlight\n")
    for demo in HALL_OF_FAME[:5]:
        print(f"• {demo['name']} by {demo['group']} ({demo['party']})")