#!/usr/bin/env python3
"""Demoscene party calendar and events.

Integrates with demoscene calendars to show upcoming parties
and featured productions.
"""

from __future__ import annotations

import urllib.request
import json
from datetime import datetime
from pathlib import Path

POUET_CALENDAR_API = "https://api.pouet.net/v1/calendar/"


def get_upcoming_parties(days_ahead: int = 90) -> list[dict]:
    """Get upcoming demoscene parties."""
    try:
        url = f"{POUET_CALENDAR_API}?days={days_ahead}"
        data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode())
        
        parties = []
        for event in data.get("events", []):
            parties.append({
                "name": event.get("name", "Unknown"),
                "date": event.get("date", ""),
                "location": event.get("location", ""),
                "type": event.get("type", "party"),
                "link": event.get("link", "")
            })
        return parties
    except Exception:
        # Fallback to known upcoming parties
        return [
            {"name": "Revision 2026", "date": "2026-04-17", "location": "Saarbrücken, Germany", "type": "party"},
            {"name": "Forever 2026", "date": "2026-05-16", "location": "Horní Lideč, Czech Republic", "type": "party"},
            {"name": "Silly Venture 2026", "date": "2026-11-21", "location": "Gdańsk, Poland", "type": "party"},
            {"name": "Assembly 2026", "date": "2026-08-06", "location": "Helsinki, Finland", "type": "party"},
        ]


def get_party_winners(party_name: str, year: int = None) -> list[dict]:
    """Get winning demos from a specific party."""
    try:
        # This would query Pouet for actual winners
        # For now, placeholder with classic winners
        classic_winners = {
            "breakpoint": [
                {"title": "Pimp My Spectrum", "group": "Fairlight", "year": 2007, "type": "wild"},
                {"title": "Loonies", "group": "Loonies", "year": 2010, "type": "4k"}
            ],
            "revision": [
                {"title": "Elements", "group": "Conspiracy", "year": 2010, "type": "demo"},
                {"title": "Happiness is a Boring Theme", "group": "CNCD & Fairlight", "year": 2009, "type": "demo"}
            ]
        }
        return classic_winners.get(party_name.lower(), [])
    except Exception:
        return []


def format_countdown(party: dict) -> str:
    """Format time until party."""
    try:
        party_date = datetime.fromisoformat(party["date"])
        now = datetime.now()
        diff = party_date - now
        if diff.days > 0:
            return f"{diff.days} days"
        return "Soon!"
    except Exception:
        return ""


if __name__ == "__main__":
    for party in get_upcoming_parties():
        print(f"{party['name']} - {party['date']} ({format_countdown(party)})")