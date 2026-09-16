#!/usr/bin/env python3
"""Showet API - Modernized to work with PlatformBase architecture.

Provides programmatic access to all platform runners, demo database,
and streaming capabilities.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any

from PlatformBase import PlatformBase


class ShowetAPI:
    """High-level API for showet platform operations."""

    def __init__(self) -> None:
        self._platforms: dict[str, PlatformBase] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        """Lazy-load all platforms."""
        if self._loaded:
            return

        import importlib

        # Discover and load all Platform_* modules
        project_root = Path(__file__).parent
        for pf in sorted(project_root.glob("Platform_*.py")):
            module_name = pf.stem
            if module_name == "PlatformBase":
                continue
            try:
                module = importlib.import_module(module_name)
                cls = getattr(module, module_name)
                instance = cls()
                if hasattr(instance, 'platform_name'):
                    self._platforms[instance.platform_name] = instance
            except Exception as e:
                print(f"Warning: Could not load {module_name}: {e}")

        self._loaded = True

    def get_platform(self, name: str) -> PlatformBase | None:
        """Get a platform runner by name."""
        self._ensure_loaded()
        return self._platforms.get(name)

    def list_platforms(self) -> list[str]:
        """List all available platform names."""
        self._ensure_loaded()
        return sorted(self._platforms.keys())

    def run_demo(self, pouet_id: int, platform: str = None, **options) -> dict[str, Any]:
        """Run a demo by Pouet ID.
        
        Args:
            pouet_id: The Pouet.net production ID
            platform: Optional platform name (auto-detected if None)
            
        Returns:
            Status dictionary
        """
        # Get demo metadata
        try:
            url = f"http://api.pouet.net/v1/prod/?id={pouet_id}"
            data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode())
            prod = data.get("prod", {})

            # Determine platform if not specified
            if not platform:
                platforms = [p["slug"] for p in prod.get("platforms", {}).values()]
                platform = platforms[0] if platforms else None

            return {
                "status": "ready",
                "platform": platform,
                "demo_name": prod.get("name", "Unknown"),
                "message": f"Demo {pouet_id} prepared for playback"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def get_demo_info(self, pouet_id: int) -> dict | None:
        """Get demo metadata from Pouet.net.
        
        Args:
            pouet_id: Pouet.net production ID
            
        Returns:
            Demo metadata dict or None on error
        """
        try:
            url = f"http://api.pouet.net/v1/prod/?id={pouet_id}"
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode())
            return data.get("prod")
        except Exception:
            return None

    def get_status(self) -> dict[str, Any]:
        """Get API status and platform availability."""
        self._ensure_loaded()
        return {
            "platforms_loaded": len(self._platforms),
            "platforms": self.list_platforms(),
            "version": "4.0.0-dev",
            "nostalgist_ready": (Path(__file__).parent / "nostalgist_configs" / "manifest.json").exists()
        }

    def get_status_extended(self) -> dict[str, Any]:
        """Get extended API status."""
        self._ensure_loaded()
        db_ready = Path.home() / ".showet" / "demo_db.json"
        return {
            "platforms_loaded": len(self._platforms),
            "platforms": self.list_platforms(),
            "version": "4.0.0-dev",
            "nostalgist_ready": (Path(__file__).parent / "nostalgist_configs" / "manifest.json").exists(),
            "demo_db_ready": db_ready.exists(),
            "db_path": str(db_ready),
            "platform_count": len(self._platforms),
        }

    def get_recommendations(self, limit: int = 10) -> list[int]:
        """Get offline demo recommendations from local demo database.

        Returns a ranked list of Pouet.net production IDs based on
        local favorites and viewing history. Works without an API key.
        """
        try:
            from demo_database import DemoDatabase
            db = DemoDatabase()
            return db.get_recommendations(limit=limit)
        except Exception:
            return []

    def list_favorites(self) -> list[dict]:
        """List all favorite demos with metadata."""
        try:
            from favorites_manager import FavoritesManager
            fm = FavoritesManager()
            return fm.list_favorites()
        except Exception:
            return []

    def add_favorite(self, pouet_id: int, name: str, platform: str = "",
                     notes: str = "") -> dict:
        """Add a demo to favorites."""
        try:
            from favorites_manager import FavoritesManager
            fm = FavoritesManager()
            fm.add_favorite(pouet_id, name, platform, notes)
            return {"status": "ok", "id": pouet_id, "name": name}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def remove_favorite(self, pouet_id: int) -> dict:
        """Remove a demo from favorites."""
        try:
            from favorites_manager import FavoritesManager
            fm = FavoritesManager()
            removed = fm.remove_favorite(pouet_id)
            return {"status": "ok", "removed": removed}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_history(self, limit: int = 50) -> list[dict]:
        """Get recent viewing history."""
        try:
            from demo_database import DemoDatabase
            db = DemoDatabase()
            return db.get_history(limit=limit)
        except Exception:
            return []

    def get_playlists(self) -> dict:
        """Get all playlists."""
        try:
            from demo_database import DemoDatabase
            db = DemoDatabase()
            return db.get_playlists()
        except Exception:
            return {}

    def search_demos(self, query: str, limit: int = 20, platform: str = None) -> list[dict]:
        """Search demos via Pouet.net API.

        Args:
            query: Search term
            limit: Maximum results to return
            platform: Optional platform slug filter

        Returns:
            List of demo metadata
        """
        try:
            url = f"http://api.pouet.net/v1/search/prod/?q={query}"
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode())

            results = []
            for prod_id, prod in list(data.get("results", {}).items())[:limit]:
                prod_platforms = [p["slug"] for p in prod.get("platforms", {}).values()]
                # Apply platform filter if specified
                if platform and prod_platforms:
                    if platform not in prod_platforms:
                        continue
                results.append({
                    "id": int(prod_id),
                    "name": prod.get("name", "Unknown"),
                    "type": prod.get("type", ""),
                    "score": prod.get("score", 0),
                    "platform": prod_platforms[0] if prod_platforms else None,
                })
            return results
        except Exception:
            return []


# Create global API instance
_api: ShowetAPI | None = None


def get_api() -> ShowetAPI:
    """Get the singleton API instance."""
    global _api
    if _api is None:
        _api = ShowetAPI()
    return _api


def main(port: int = 8765) -> int:
    """CLI entry point for API status."""
    api = get_api()
    status = api.get_status()
    print(f"Showet API v{status['version']}")
    print(f"Platforms loaded: {status['platforms_loaded']}")
    print(f"nostalgist.js ready: {status['nostalgist_ready']}")
    print("Available platforms:")
    for p in status['platforms'][:10]:
        print(f"  - {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
