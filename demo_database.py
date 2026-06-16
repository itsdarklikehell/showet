#!/usr/bin/env python3
"""Demo database for Showet - demoscene-focused features.

Features:
- Favorite demos with tags
- Demo recommendations based on scene history
- Compo/party tracking
- Pouet.net integration enhancements
- Search and filter capabilities
"""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime
from pathlib import Path

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
        self._data: dict = {}
        self.data = self._load_db()

    def _load_db(self) -> dict:
        """Load database from disk."""
        if self.db_path.exists():
            try:
                return json.loads(self.db_path.read_text())
            except json.JSONDecodeError:
                pass
        return {"favorites": {}, "history": [], "tags": {}, "playlists": {}}

    def save(self) -> None:
        """Persist database to disk."""
        self.db_path.write_text(json.dumps(self.data, indent=2))

    def add_favorite(self, pouet_id: int, tags: list[str] = None, score: int = None) -> None:
        """Add a demo to favorites with optional tags."""
        self.data["favorites"][str(pouet_id)] = {
            "added": datetime.now().isoformat(),
            "tags": tags or [],
            "score": score,
        }
        self.save()

    def remove_favorite(self, pouet_id: int) -> bool:
        """Remove a demo from favorites."""
        if str(pouet_id) in self.data.get("favorites", {}):
            del self.data["favorites"][str(pouet_id)]
            self.save()
            return True
        return False

    def get_favorites(self) -> dict[int, dict]:
        """Get all favorite demos."""
        return {int(k): v for k, v in self.data.get("favorites", {}).items()}

    def add_history(self, pouet_id: int, platform: str, score: int = None) -> None:
        """Record demo viewing history."""
        entry = {
            "pouet_id": pouet_id,
            "platform": platform,
            "played_at": datetime.now().isoformat(),
            "score": score,
        }
        self.data["history"].append(entry)
        self.save()

    def get_history(self, limit: int = 50) -> list[dict]:
        """Get recent viewing history."""
        return sorted(
            self.data.get("history", []),
            key=lambda x: x.get("played_at", ""),
            reverse=True
        )[:limit]

    def search_demos(self, query: str, limit: int = 20) -> list[dict]:
        """Search demos via Pouet.net API.
        
        Note: Pouet API returns results as 'results' dict with prod IDs as keys.
        """
        try:
            url = f"http://api.pouet.net/v1/search/prod/?q={query}"
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode())
            
            if not data.get("success"):
                return []
                
            results = []
            for prod_id, prod_data in list(data.get("results", {}).items())[:limit]:
                results.append({
                    "id": int(prod_id),
                    "name": prod_data.get("name", "Unknown"),
                    "type": prod_data.get("type", ""),
                    "party": prod_data.get("party", ""),
                    "score": prod_data.get("score", 0),
                })
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def search_by_platform(self, platform: str, limit: int = 20) -> list[dict]:
        """Search demos for a specific platform."""
        return self.search_demos(f"platform:{platform}", limit)

    def search_by_party(self, party: str, limit: int = 20) -> list[dict]:
        """Search demos from a specific demoparty."""
        return self.search_demos(f"party:{party}", limit)

    def create_playlist(self, name: str, demo_ids: list[int] = None) -> str:
        """Create a playlist of demos."""
        playlist_id = str(datetime.now().timestamp())[:8]
        self.data.setdefault("playlists", {})[playlist_id] = {
            "name": name,
            "demo_ids": demo_ids or [],
            "created": datetime.now().isoformat(),
        }
        self.save()
        return playlist_id

    def get_playlists(self) -> dict[str, dict]:
        """Get all playlists."""
        return self.data.get("playlists", {})

    def get_recommendations(self, limit: int = 10) -> list[int]:
        """Get demo recommendations based on favorites and party history."""
        # TODO: integrate actual Pouet recommendations API
        return []

    def get_party_demos(self, party: str) -> list[int]:
        """Get demos from a specific party."""
        # Would integrate with Pouet API for party-specific demos
        return []


# Singleton instance
_db_instance: DemoDatabase | None = None


def get_db() -> DemoDatabase:
    """Get the singleton database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = DemoDatabase()
    return _db_instance