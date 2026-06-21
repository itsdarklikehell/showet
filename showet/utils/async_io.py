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
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS demos (
                id INTEGER PRIMARY KEY,
                pouet_id INTEGER,
                source TEXT,
                title TEXT,
                platform TEXT,
                path TEXT UNIQUE,
                downloaded_at TEXT,
                size INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY,
                name TEXT,
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