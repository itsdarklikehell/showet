#!/usr/bin/env python3
"""Showet Demozoo.org Integration - Extended demoscene metadata.

Demozoo provides additional production details beyond Pouet.net.
This module enriches Showet with group info, member credits, and release dates.
"""

import json
import urllib.request
from pathlib import Path
from typing import Optional

class DemozooAPI:
    """Client for Demozoo.org demoscene database."""

    BASE_URL = "https://demozoo.org/api/v1"
    HEADERS = {"User-Agent": "Showet Demo Runner/2.0"}

    def __init__(self):
        self.cache_dir = Path.home() / ".showet" / "demozoo"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def search_productions(self, query: str) -> list[dict]:
        """Search for productions by name, group, or party."""
        cache_file = self.cache_dir / f"search_{query.replace(' ', '_')}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())

        url = f"{self.BASE_URL}/productions/?search={query}"
        try:
            req = urllib.request.Request(url, headers=self.HEADERS)
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            results = data.get("results", [])
            cache_file.write_text(json.dumps(results))
            return results[:20]
        except Exception as e:
            print(f"Demozoo search failed: {e}")
            return []

    def get_production(self, prod_id: int) -> Optional[dict]:
        """Get extended production info by Demozoo ID."""
        cache_file = self.cache_dir / f"prod_{prod_id}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())

        url = f"{self.BASE_URL}/productions/{prod_id}/"
        try:
            req = urllib.request.Request(url, headers=self.HEADERS)
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            cache_file.write_text(json.dumps(data))
            return data
        except Exception as e:
            print(f"Failed to fetch production {prod_id}: {e}")
            return None

    def get_groups(self, query: str = "") -> list[dict]:
        """Search for demoscene groups."""
        url = f"{self.BASE_URL}/groups/"
        if query:
            url += f"?search={query}"

        try:
            req = urllib.request.Request(url, headers=self.HEADERS)
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            return data.get("results", [])[:20]
        except Exception as e:
            print(f"Demozoo groups search failed: {e}")
            return []

    def get_parties(self, year: Optional[int] = None) -> list[dict]:
        """Get demoparty information."""
        url = f"{self.BASE_URL}/parties/"
        if year:
            url += f"?year={year}"

        try:
            req = urllib.request.Request(url, headers=self.HEADERS)
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            return sorted(data.get("results", []), key=lambda x: x.get("start_date", ""), reverse=True)[:20]
        except Exception as e:
            print(f"Demozoo parties fetch failed: {e}")
            return []


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: showet-demozoo [search|production|groups|parties] [options]")
        print("\nCommands:")
        print("  search <query>     Search productions")
        print("  production <id>    Get extended production info")
        print("  groups [query]     Search groups")
        print("  parties [year]     List demoparties")
        sys.exit(1)

    api = DemozooAPI()
    command = sys.argv[1]

    if command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        results = api.search_productions(query)
        print(f"Found {len(results)} productions")
        for r in results[:10]:
            title = r.get("title", "Unknown")
            group = r.get("group", {}).get("name", "Solo")
            print(f"  {title} by {group}")

    elif command == "production":
        if len(sys.argv) < 3:
            print("Usage: showet-demozoo production <id>")
            sys.exit(1)
        prod_id = int(sys.argv[2])
        data = api.get_production(prod_id)
        if data:
            print(json.dumps(data, indent=2))

    elif command == "groups":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        results = api.get_groups(query)
        for g in results[:10]:
            print(f"  {g.get('name')} ({g.get('country', '')})")

    elif command == "parties":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else None
        results = api.get_parties(year)
        for p in results[:10]:
            print(f"  {p.get('name')} ({p.get('start_date', '???')})")


if __name__ == "__main__":
    main()