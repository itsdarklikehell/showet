"""ModArchive.org integration module for Showet.

Music module downloads for synth demos.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional


class ModArchiveAPI:
    """Client for ModArchive.org music module database."""

    BASE_URL = "https://modarchive.org"
    SEARCH_URL = "https://modarchive.org/include/query.php"

    def __init__(self) -> None:
        self.cache_dir = Path.home() / ".showet" / "modarchive"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def search_modules(
        self, query: str, format: Optional[str] = None, artist: Optional[str] = None
    ) -> list[dict]:
        """Search for music modules."""
        params = {"query": query}
        if format:
            params["format"] = format
        if artist:
            params["artist"] = artist

        url = f"{self.SEARCH_URL}?{urllib.parse.urlencode(params)}"

        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Showet Demo Runner/4.0"}
            )
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())

            modules = []
            for item in data.get("results", []):
                modules.append({
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "artist": item.get("artist"),
                    "format": item.get("format", "").upper(),
                    "genre": item.get("genre"),
                    "download_url": f"https://modarchive.org/download/{item.get('id')}",
                })
            return modules[:50]
        except Exception:
            return []

    def get_module(self, module_id: int) -> Optional[dict]:
        """Get detailed info for a specific module."""
        cache_file = self.cache_dir / f"{module_id}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())

        try:
            url = f"https://modarchive.org/module.php?{module_id}"
            req = urllib.request.Request(url, headers={"User-Agent": "Showet Demo Runner/4.0"})
            response = urllib.request.urlopen(req, timeout=10)
            return self._parse_module_page(response.read().decode())
        except Exception:
            return None

    def _parse_module_page(self, html: str) -> dict:
        """Parse module.php HTML to extract metadata."""
        import re
        title_match = re.search(r"<title>([^<]+)", html)
        title = title_match.group(1) if title_match else "Unknown"
        return {"title": title}

    def download_module(self, module_id: int, dest_dir: Optional[Path] = None) -> Optional[Path]:
        """Download a music module to local storage."""
        dest_dir = dest_dir or self.cache_dir
        dest_dir.mkdir(parents=True, exist_ok=True)

        module = self.get_module(module_id)
        if not module or not module.get("download_url"):
            return None

        try:
            response = urllib.request.urlopen(module["download_url"], timeout=30)
            module_path = dest_dir / f"{module_id}.mod"
            module_path.write_bytes(response.read())
            return module_path
        except Exception:
            return None