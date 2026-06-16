#!/usr/bin/env python3
"""Local demo cache manager for showet.

Manages downloading, caching, and retrieving demos for offline playback.
Demos are cached by pouet.net ID in ~/.cache/showet/
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import urllib.request
from pathlib import Path
from typing import Optional


class CacheManager:
    """Manages local demo cache."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize cache manager.

        Args:
            cache_dir: Custom cache directory (default: ~/.cache/showet)
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "showet"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / "metadata.json"
        self._metadata: dict[int, dict] = {}

    def _load_metadata(self) -> None:
        """Load metadata from disk."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    self._metadata = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._metadata = {}
        else:
            self._metadata = {}

    def _save_metadata(self) -> None:
        """Save metadata to disk."""
        with open(self.metadata_file, "w") as f:
            json.dump(self._metadata, f, indent=2)

    def _get_demo_dir(self, prod_id: int) -> Path:
        """Get cache directory for a demo."""
        return self.cache_dir / str(prod_id)

    def is_cached(self, prod_id: int) -> bool:
        """Check if a demo is cached."""
        self._load_metadata()
        return prod_id in self._metadata and self._get_demo_dir(prod_id).exists()

    def get_cached_path(self, prod_id: int) -> Optional[Path]:
        """Get the path to a cached demo file."""
        if not self.is_cached(prod_id):
            return None

        demo_dir = self._get_demo_dir(prod_id)
        meta = self._metadata.get(prod_id, {})
        filename = meta.get("filename")

        if not filename:
            # Find first file in directory
            files = list(demo_dir.glob("*"))
            if files:
                return files[0]
            return None

        path = demo_dir / filename
        return path if path.exists() else None

    def cache_demo(self, prod_id: int, download_url: str, filename: str,
                   metadata: Optional[dict] = None) -> Optional[Path]:
        """Download and cache a demo.

        Args:
            prod_id: Pouet.net production ID
            download_url: URL to download demo from
            filename: Expected filename
            metadata: Optional metadata to store (name, platform, etc.)

        Returns:
            Path to cached file, or None on failure
        """
        demo_dir = self._get_demo_dir(prod_id)
        demo_dir.mkdir(parents=True, exist_ok=True)

        output_path = demo_dir / filename

        # Download file
        try:
            print(f"Downloading demo {prod_id} from {download_url}")
            urllib.request.urlretrieve(download_url, output_path)
        except Exception as e:
            print(f"Failed to download: {e}")
            if demo_dir.exists():
                shutil.rmtree(demo_dir)
            return None

        # Store metadata
        self._load_metadata()
        self._metadata[prod_id] = {
            "filename": filename,
            "download_url": download_url,
            "cached_at": int(os.path.getmtime(output_path)),
            **(metadata or {}),
        }
        self._save_metadata()

        return output_path

    def get_metadata(self, prod_id: int) -> Optional[dict]:
        """Get metadata for a cached demo."""
        self._load_metadata()
        return self._metadata.get(prod_id)

    def list_cached_demos(self) -> list[dict]:
        """List all cached demos with metadata."""
        self._load_metadata()
        demos = []
        for prod_id, meta in self._metadata.items():
            demo_path = self.get_cached_path(prod_id)
            if demo_path:
                demos.append({
                    "id": prod_id,
                    "path": str(demo_path),
                    **meta
                })
        return sorted(demos, key=lambda x: x.get("cached_at", 0), reverse=True)

    def remove_demo(self, prod_id: int) -> bool:
        """Remove a demo from cache.

        Returns:
            True if demo was removed, False if not found
        """
        demo_dir = self._get_demo_dir(prod_id)
        if demo_dir.exists():
            shutil.rmtree(demo_dir)

        self._load_metadata()
        if prod_id in self._metadata:
            del self._metadata[prod_id]
            self._save_metadata()
            return True
        return False

    def get_cache_size(self) -> int:
        """Get total cache size in bytes."""
        total = 0
        for path in self.cache_dir.rglob("*"):
            if path.is_file():
                total += path.stat().st_size
        return total

    def clear_cache(self) -> None:
        """Clear all cached demos."""
        for demo_dir in self.cache_dir.iterdir():
            if demo_dir.is_dir() and demo_dir.name.isdigit():
                shutil.rmtree(demo_dir)

        self._metadata = {}
        self._save_metadata()