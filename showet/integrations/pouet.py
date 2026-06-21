"""Pouet.net integration module for Showet."""

from __future__ import annotations

import urllib.request
from typing import Optional


class PouetClient:
    """Client for pouet.net API."""

    API_BASE = "http://api.pouet.net/v1"

    def __init__(self) -> None:
        pass

    def get_production(self, prod_id: int) -> Optional[dict]:
        """Fetch production metadata."""
        try:
            url = f"{self.API_BASE}/prod/?id={prod_id}"
            with urllib.request.urlopen(url, timeout=10) as response:
                import json
                data = json.loads(response.read().decode())
                return data.get("prod")
        except Exception:
            return None

    def get_download_url(self, prod_id: int) -> Optional[str]:
        """Get download URL for a production."""
        prod = self.get_production(prod_id)
        if prod:
            return prod.get("download")
        return None

    def search(self, query: str, limit: int = 50) -> list[dict]:
        """Search productions (requires web scraping or alternate API)."""
        # Pouet API v1 doesn't have search, would need scraping
        return []