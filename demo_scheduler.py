#!/usr/bin/env python3
"""Demo scheduler for Showet - plan and organize demo sessions.

Features:
- Schedule demo playback sessions
- Voting system for collaborative viewing
- Demoparty countdown
- Stream event planning
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List


class DemoScheduler:
    """Schedule and manage demo playback events."""

    def __init__(self, schedule_path: Optional[Path] = None):
        self.schedule_path = schedule_path or Path.home() / ".showet" / "schedule.json"
        self.schedule_path.parent.mkdir(parents=True, exist_ok=True)
        self._events: List[Dict[str, Any]] = self._load_schedule()

    def _load_schedule(self) -> List[Dict[str, Any]]:
        """Load schedule from disk."""
        if self.schedule_path.exists():
            try:
                return json.loads(self.schedule_path.read_text())
            except json.JSONDecodeError:
                pass
        return []

    def _save_schedule(self) -> None:
        """Save schedule to disk."""
        self.schedule_path.write_text(json.dumps(self._events, indent=2))

    def add_event(
        self,
        demo_id: int,
        platform: str = None,
        when: datetime = None,
        title: str = None,
    ) -> str:
        """Schedule a demo playback event.
        
        Args:
            demo_id: Pouet.net demo ID
            platform: Platform slug (optional)
            when: When to play (defaults to now)
            title: Custom event title
            
        Returns:
            Event ID
        """
        event = {
            "id": str(int(time.time())),
            "demo_id": demo_id,
            "platform": platform or "",
            "scheduled_at": (when or datetime.now()).isoformat(),
            "created_at": datetime.now().isoformat(),
            "title": title or f"Demo {demo_id}",
            "votes": [],
            "status": "scheduled",
        }
        self._events.append(event)
        self._save_schedule()
        return event["id"]

    def get_upcoming(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get upcoming scheduled events."""
        now = datetime.now()
        upcoming = [
            e for e in self._events
            if datetime.fromisoformat(e["scheduled_at"]) > now
        ]
        return sorted(upcoming, key=lambda x: x["scheduled_at"])[:limit]

    def get_next_event(self) -> Optional[Dict[str, Any]]:
        """Get the next scheduled event."""
        upcoming = self.get_upcoming(limit=1)
        return upcoming[0] if upcoming else None

    def vote(self, event_id: str, user: str) -> bool:
        """Vote for a demo to be played sooner."""
        for event in self._events:
            if event["id"] == event_id and user not in event["votes"]:
                event["votes"].append(user)
                self._save_schedule()
                return True
        return False

    def cancel_event(self, event_id: str) -> bool:
        """Cancel a scheduled event."""
        for i, event in enumerate(self._events):
            if event["id"] == event_id:
                event["status"] = "cancelled"
                self._save_schedule()
                return True
        return False


class PartyCountdown:
    """Track upcoming demoparty dates."""

    PARTIES = {
        "revision_2026": {"date": "2026-04-17", "location": "Saarbrücken, Germany"},
        "assembly_2026": {"date": "2026-08-06", "location": "Helsinki, Finland"},
        "evoke_2026": {"date": "2026-08-15", "location": "Cologne, Germany"},
        "x_2026": {"date": "2026-10-24", "location": "Netherlands"},
        "forever_2026": {"date": "2026-05-16", "location": "Horní Lideč, Czech Republic"},
    }

    @classmethod
    def get_next_party(cls) -> Optional[Dict[str, Any]]:
        """Get the next upcoming party."""
        now = datetime.now()
        for name, info in cls.PARTIES.items():
            if info.get("date"):
                party_date = datetime.fromisoformat(info["date"])
                if party_date > now:
                    days = (party_date - now).days
                    return {
                        "name": name.title(),
                        "date": info["date"],
                        "location": info["location"],
                        "days_remaining": days,
                    }
        return None

    @classmethod
    def format_countdown(cls) -> str:
        """Format countdown string for display."""
        party = cls.get_next_party()
        if party:
            return f"📅 {party['name']} in {party['days_remaining']} days ({party['location']})"
        return "No upcoming parties scheduled"


def generate_scheduled_overlay() -> str:
    """Generate overlay text for upcoming scheduled demos."""
    scheduler = DemoScheduler()
    next_event = scheduler.get_next_event()
    if next_event:
        party = PartyCountdown.format_countdown()
        return f"Next: Demo {next_event['demo_id']} • {party}"
    return PartyCountdown.format_countdown()


if __name__ == "__main__":
    print("📺 Showet Demo Scheduler")
    print(PartyCountdown.format_countdown())
    
    scheduler = DemoScheduler()
    next_demo = scheduler.get_next_event()
    if next_demo:
        print(f"\nNext demo: {next_demo['demo_id']} at {next_demo['scheduled_at']}")
    else:
        print("\nNo scheduled demos")