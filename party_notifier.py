#!/usr/bin/env python3
"""Party release notifier - alerts for new demoscene releases.

Features:
- Track new releases at demoparties
- Pouet API integration for fresh demos
- Notification system for streams
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Classic demoparty release patterns
PARTY_PATTERNS = {
    "revision": {"search": "revision 2026", "tags": ["pc", "demo", "4k"]},
    "assembly": {"search": "assembly 2026", "tags": ["pc", "demo"]},
    "evoke": {"search": "evoke 2026", "tags": ["pc", "demo"]},
}


def check_for_new_releases(party: str = None, days: int = 7) -> List[Dict[str, Any]]:
    """Check Pouet for new releases.
    
    Args:
        party: Party name to search (e.g., 'revision', 'assembly')
        days: Days to look back
        
    Returns:
        List of new demos
    """
    try:
        if party:
            search = PARTY_PATTERNS.get(party, {}).get("search", f"{party} 2026")
            url = f"http://api.pouet.net/v1/search/prod/?q={search}&days={days}"
        else:
            url = "http://api.pouet.net/v1/prod/?order=released"

        # Placeholder - would connect to actual API
        return []
    except Exception:
        return []


def generate_party_overlay(party_name: str, next_release: str = None) -> str:
    """Generate overlay for party release streams.
    
    Args:
        party_name: Name of the party
        next_release: Next release being played
        
    Returns:
        HTML overlay for streaming
    """
    from demo_scheduler import PartyCountdown
    party = PartyCountdown.get_next_party()
    
    days = party.get("days_remaining", 0) if party else 0
    
    return f'''
<div id="party-overlay" style="
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255, 107, 0, 0.9);
    padding: 10px 30px;
    border-radius: 5px;
    color: white;
    font-family: 'Courier New', monospace;
    font-weight: bold;
    z-index: 9999;
    border: 2px solid #ff6b00;
">
    <div>{party_name.upper()} • {days} days to go</div>
    {f'<div style="font-size: 12px; margin-top: 5px;">Now Playing: {next_release}</div>' if next_release else ''}
</div>
'''


def create_release_notification(demo_id: int, party: str = None) -> str:
    """Create notification text for a new release.
    
    Args:
        demo_id: Pouet demo ID
        party: Party name (optional)
        
    Returns:
        Notification string
    """
    return f"🚨 NEW RELEASE! Demo {demo_id} just dropped{' at ' + party if party else ''}"


if __name__ == "__main__":
    from demo_scheduler import PartyCountdown
    party = PartyCountdown.get_next_party()
    if party:
        print(f"📅 Next party: {party['name']}")
        print(f"   In {party['days_remaining']} days")
        print(f"   Location: {party['location']}")
    else:
        print("No upcoming parties")
    
    print("\n📡 Check for new releases before streaming a party!")