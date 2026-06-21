"""Async I/O module for Showet.

Provides async download manager and parallel archive extraction.
"""

from __future__ import annotations

import asyncio
import json
import os
import sqlite3
from pathlib import Path
from typing import Optional

try:
    import aiohttp
except ImportError:
    aiohttp = None  # type: ignore


class AsyncDownloader:
    """Async downloader for parallel demo fetching."""

    def __init__(self, max_concurrent: int = 4) -> None:
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "AsyncDownloader":
        if aiohttp is None:
            raise ImportError("aiohttp required: pip install aiohttp")
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args: object) -> None:
        if self.session:
            await self.session.close()

    async def download(self, url: str, dest: Path) -> bool:
        """Download a single file asynchronously."""
        async with self.semaphore:
            if not self.session:
                return False
            try:
                async with self.session.get(url) as response:
                    response.raise_for_status()
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with open(dest, "wb") as f:
                        f.write(await response.read())
                return True
            except Exception:
                return False

    async def download_batch(self, urls: list[tuple[str, Path]]) -> list[bool]:
        """Download multiple URLs concurrently."""
        tasks = [self.download(url, path) for url, path in urls]
        return await asyncio.gather(*tasks)


class DemoCache:
    """SQLite-based offline cache for demos and metadata."""

    def __init__(self, cache_dir: Optional[Path] = None) -> None:
        self.cache_dir = cache_dir or Path.home() / ".showet" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.cache_dir / "demos.db"
        self.sync_manifest: Optional[Path] = None
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS demos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pouet_id INTEGER UNIQUE,
                sceneorg_id INTEGER,
                source TEXT,
                title TEXT,
                platform TEXT,
                path TEXT,
                downloaded_at TEXT,
                size INTEGER,
                tags TEXT,
                rating REAL DEFAULT 0.0,
                play_count INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                created_at TEXT,
                demo_ids TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                demo_id INTEGER,
                operation TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_demo(self, demo_id: int, source: str, title: str, 
                 platform: str, path: str) -> None:
        """Add demo to cache."""
        import time
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO demos (pouet_id, source, title, platform, path, downloaded_at) VALUES (?, ?, ?, ?, ?, ?)",
            (demo_id, source, title, platform, path, time.strftime("%Y-%m-%d"))
        )
        conn.commit()
        conn.close()

    def get_cached(self, demo_id: int) -> Optional[str]:
        """Get cached demo path."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT path FROM demos WHERE pouet_id = ?", (demo_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def add_demo(self, demo_id: int, source: str, title: str,
                 platform: str, path: str, tags: str = None) -> None:
        """Add demo to cache with optional tags."""
        import time
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO demos 
               (pouet_id, source, title, platform, path, downloaded_at, tags) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (demo_id, source, title, platform, path, time.strftime("%Y-%m-%d"), tags)
        )
        conn.commit()
        conn.close()

    def create_playlist(self, name: str, demo_ids: list[int]) -> int:
        """Create a playlist with demo IDs."""
        import time
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO playlists (name, created_at, demo_ids) VALUES (?, ?, ?)",
            (name, time.strftime("%Y-%m-%d"), ",".join(map(str, demo_ids)))
        )
        conn.commit()
        playlist_id = cursor.lastrowid
        conn.close()
        return playlist_id

    def get_playlist(self, name: str) -> Optional[list[int]]:
        """Get demo IDs from a playlist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT demo_ids FROM playlists WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return [int(x) for x in row[0].split(",")]
        return None

    def list_all(self, limit: int = 50) -> list[dict]:
        """List all cached demos."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM demos ORDER BY downloaded_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def increment_play_count(self, demo_id: int) -> None:
        """Increment play counter for a demo."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE demos SET play_count = play_count + 1 WHERE pouet_id = ?", (demo_id,))
        conn.commit()
        conn.close()

    def export_sync_manifest(self, dest: Path) -> int:
        """Export cache as JSON manifest for sync."""
        demos = self.list_all(1000)
        manifest = {
            "exported": time.strftime("%Y-%m-%d"),
            "version": "1.0",
            "demos": demos,
        }
        dest.write_text(json.dumps(manifest, indent=2))
        return len(demos)

    def import_sync_manifest(self, src: Path) -> int:
        """Import demos from sync manifest."""
        data = json.loads(src.read_text())
        count = 0
        for demo in data.get("demos", []):
            self.add_demo(
                demo.get("pouet_id"),
                demo.get("source", "import"),
                demo.get("title", "Unknown"),
                demo.get("platform", "unknown"),
                demo.get("path"),
                demo.get("tags")
            )
            count += 1
        return count


async def download_demo_async(demo_id: int, dest_dir: Path) -> Optional[Path]:
    """Download a demo by ID asynchronously."""
    try:
        url = f"http://api.pouet.net/v1/prod/?id={demo_id}"
        import urllib.request
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            prod = data.get("prod", {})
            download_url = prod.get("download")
            
            if download_url:
                filename = f"{demo_id}.zip"
                dest = dest_dir / filename
                
                if aiohttp:
                    async with AsyncDownloader() as dl:
                        success = await dl.download(download_url, dest)
                        return dest if success else None
    except Exception:
        pass
    return None