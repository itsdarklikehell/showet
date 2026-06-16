#!/usr/bin/env python3
"""Favorites manager for showet.

Stores and retrieves favorite demos with user notes.
Favorites are stored in ~/.config/showet/favorites.json
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class FavoritesManager:
    """Manages favorite demos."""

    def __init__(self, favorites_file: Optional[Path] = None):
        """Initialize favorites manager.

        Args:
            favorites_file: Custom favorites file (default: ~/.config/showet/favorites.json)
        """
        if favorites_file is None:
            config_dir = Path.home() / ".config" / "showet"
            config_dir.mkdir(parents=True, exist_ok=True)
            favorites_file = config_dir / "favorites.json"
        self.favorites_file = Path(favorites_file)
        self._favorites: dict[int, dict] = {}

    def _load_favorites(self) -> None:
        """Load favorites from disk."""
        if self.favorites_file.exists():
            try:
                with open(self.favorites_file, "r") as f:
                    self._favorites = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._favorites = {}
        else:
            self._favorites = {}

    def _save_favorites(self) -> None:
        """Save favorites to disk."""
        with open(self.favorites_file, "w") as f:
            json.dump(self._favorites, f, indent=2)

    def add_favorite(self, prod_id: int, name: str, platform: str = "",
                     notes: str = "") -> None:
        """Add a demo to favorites.

        Args:
            prod_id: Pouet.net production ID
            name: Demo name
            platform: Platform name (optional)
            notes: User notes (optional)
        """
        self._load_favorites()
        self._favorites[prod_id] = {
            "name": name,
            "platform": platform,
            "notes": notes,
            "added_at": datetime.now().isoformat(),
        }
        self._save_favorites()

    def remove_favorite(self, prod_id: int) -> bool:
        """Remove a demo from favorites.

        Returns:
            True if removed, False if not in favorites
        """
        self._load_favorites()
        if prod_id in self._favorites:
            del self._favorites[prod_id]
            self._save_favorites()
            return True
        return False

    def is_favorite(self, prod_id: int) -> bool:
        """Check if a demo is in favorites."""
        self._load_favorites()
        return prod_id in self._favorites

    def get_favorite(self, prod_id: int) -> Optional[dict]:
        """Get favorite metadata."""
        self._load_favorites()
        return self._favorites.get(prod_id)

    def list_favorites(self) -> list[dict]:
        """List all favorites with metadata."""
        self._load_favorites()
        favorites = []
        for prod_id, meta in self._favorites.items():
            favorites.append({
                "id": prod_id,
                **meta
            })
        # Sort by added_at, most recent first
        favorites.sort(key=lambda x: x.get("added_at", ""), reverse=True)
        return favorites

    def update_note(self, prod_id: int, notes: str) -> bool:
        """Update notes for a favorite.

        Returns:
            True if updated, False if not found
        """
        self._load_favorites()
        if prod_id in self._favorites:
            self._favorites[prod_id]["notes"] = notes
            self._save_favorites()
            return True
        return False

    def get_count(self) -> int:
        """Get number of favorites."""
        self._load_favorites()
        return len(self._favorites)