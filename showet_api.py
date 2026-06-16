#!/usr/bin/env python3
"""
Showet API - Modernized to work with PlatformBase architecture.

Provides programmatic access to all platform runners.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

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
        for pf in project_root.glob("Platform_*.py"):
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

    def get_platform(self, name: str) -> Optional[PlatformBase]:
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
        # This would integrate with showet.py's download logic
        # For now, return status
        return {
            "status": "ready",
            "platform": platform,
            "message": f"Demo {pouet_id} prepared for playback"
        }

    def get_status(self) -> dict[str, Any]:
        """Get API status and platform availability."""
        self._ensure_loaded()
        return {
            "platforms_loaded": len(self._platforms),
            "platforms": self.list_platforms(),
            "version": "2.0.0"
        }


# Create global API instance
_api: ShowetAPI | None = None


def get_api() -> ShowetAPI:
    """Get the singleton API instance."""
    global _api
    if _api is None:
        _api = ShowetAPI()
    return _api


def main() -> int:
    """CLI entry point for API status."""
    api = get_api()
    status = api.get_status()
    print(f"Showet API v{status['version']}")
    print(f"Platforms loaded: {status['platforms_loaded']}")
    print("Available platforms:")
    for p in status['platforms'][:10]:
        print(f"  - {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())