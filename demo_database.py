#!/usr/bin/env python3
"""Demo database for Showet - demoscene-focused features.

Features:
- Favorite demos with tags
- Demo recommendations based on scene history
- Compo/party tracking
- Pouet.net integration enhancements
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

# Demoscene parties for recommendations
PARTY_HISTORY = {
    "assembly": {"year": 1998, "place": "Finland", "type": "large"},
    "breakpoint": {"year": 1998, "place": "Germany", "type": "legendary"},
    "evoke": {"year": 1998, "place": "Germany", "type": "classic"},
    "revision": {"year": 2011, "place": "Germany", "type": "major"},
    "x": {"year": 1988, "place": "Netherlands", "type": "legendary"},
    "forever": {"year": 2003, "place": "Poland", "type": "classic"},
    "sillyventure": {"year": 2002, "place": "Poland", "type": "atari"},
    "gg": {"year": 2020, "place": "Global", "type": "online"},
}


class DemoDatabase:
    """Database for tracking and discovering demoscene productions."""

    def __init__(self, db_path: Path | str = None):
        self.db_path = Path(db_path) if db_path else Path.home() / ".showet" / "demo_db.json"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load_db()

    def _load_db(self) -> dict:
        """Load database from disk."""
        if self.db_path.exists():
            return json.loads(self.db_path.read_text())
        return {"favorites": {}, "history": [], "tags": {}}

    def save(self) -> None:
        """Persist database to disk."""
        self.db_path.write_text(json.dumps(self.data, indent=2))

    def add_favorite(self, pouet_id: int, tags: list[str] = None) -> None:
        """Add a demo to favorites with optional tags."""
        self.data["favorites"][str(pouet_id)] = {
            "added": datetime.now().isoformat(),
            "tags": tags or []
        }
        self.save()

    def get_favorites(self) -> dict[int, dict]:
        """Get all favorite demos."""
        return {int(k): v for k, v in self.data.get("favorites", {}).items()}

    def add_history(self, pouet_id: int, platform: str, score: int = None) -> None:
        """Record demo viewing history."""
        entry = {
            "pouet_id": pouet_id,
            "platform": platform,
            "played_at": datetime.now().isoformat(),
            "score": score
        }
        self.data["history"].append(entry)
        self.save()

    def get_recommendations(self, limit: int = 10) -> list[int]:
        """Get demo recommendations based on favorites and party history."""
        # For now, return random popular demos
        # In future: ML-based recommendations
        return []

    def get_party_demos(self, party: str) -> list[int]:
        """Get demos from a specific party."""
        # Placeholder - would integrate with Pouet API
        return []


# Singleton instance
_db_instance: DemoDatabase | None = None

def get_db() -> DemoDatabase:
    """Get the singleton database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = DemoDatabase()
    return _db_instance