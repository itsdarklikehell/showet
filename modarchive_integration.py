#!/usr/bin/env python3
"""Showet ModArchive.org Integration - Music module downloads for synth demos.

ModArchive.org provides thousands of tracked music modules for demoscene productions.
This module integrates with Showet to fetch and play music modules.
"""

import json
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional


class ModArchiveAPI:
    """Client for ModArchive.org music module database."""

    BASE_URL = "https://modarchive.org"
    SEARCH_URL = "https://modarchive.org/include/query.php"

    def __init__(self):
        self.cache_dir = Path.home() / ".showet" / "modarchive"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def search_modules(
        self, query: str, format: Optional[str] = None, artist: Optional[str] = None
    ) -> list[dict]:
        """Search for music modules.

        Args:
            query: Search term (module name, artist, genre)
            format: Module format filter (mod, s3m, xm, it, etc.)
            artist: Artist name filter

        Returns:
            List of module metadata dictionaries.
        """
        params = {"query": query}
        if format:
            params["format"] = format
        if artist:
            params["artist"] = artist

        url = f"{self.SEARCH_URL}?{urllib.parse.urlencode(params)}"

        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Showet Demo Runner/2.0"}
            )
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())

            modules = []
            for item in data.get("results", []):
                modules.append(
                    {
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "artist": item.get("artist"),
                        "format": item.get("format").upper(),
                        "genre": item.get("genre"),
                        "rating": item.get("rating"),
                        "download_url": f"https://modarchive.org/download/{item.get('id')}",
                    }
                )
            return modules[:50]  # Limit results
        except Exception as e:
            print(f"ModArchive search failed: {e}")
            return []

    def get_module(self, module_id: int) -> Optional[dict]:
        """Get detailed info for a specific module.

        Args:
            module_id: ModArchive module ID

        Returns:
            Module metadata dictionary or None.
        """
        cache_file = self.cache_dir / f"{module_id}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())

        url = f"https://modarchive.org/module.php?{module_id}"
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Showet Demo Runner/2.0"}
            )
            response = urllib.request.urlopen(req, timeout=10)
            # Parse the HTML page for module info
            data = self._parse_module_page(response.read().decode())
            cache_file.write_text(json.dumps(data))
            return data
        except Exception as e:
            print(f"Failed to fetch module {module_id}: {e}")
            return None

    def _parse_module_page(self, html: str) -> dict:
        """Parse module.php HTML to extract metadata."""
        import re

        # Extract key info from the page
        title_match = re.search(r"<title>([^<]+)", html)
        title = title_match.group(1) if title_match else "Unknown"

        download_match = re.search(r"href=\"(/download/(\d+)\")", html)
        download_id = download_match.group(2) if download_match else None

        return {
            "title": title,
            "download_url": f"https://modarchive.org/download/{download_id}" if download_id else None,
        }

    def download_module(
        self, module_id: int, dest_dir: Optional[Path] = None
    ) -> Optional[Path]:
        """Download a music module to local storage.

        Args:
            module_id: ModArchive module ID
            dest_dir: Destination directory (default: ~/.showet/modarchive/)

        Returns:
            Path to downloaded file or None.
        """
        dest_dir = dest_dir or self.cache_dir
        dest_dir.mkdir(parents=True, exist_ok=True)

        module = self.get_module(module_id)
        if not module or not module.get("download_url"):
            return None

        download_url = module["download_url"]
        module_path = dest_dir / f"{module_id}.mod"

        try:
            response = urllib.request.urlopen(download_url, timeout=30)
            module_path.write_bytes(response.read())
            print(f"Downloaded module {module_id} to {module_path}")
            return module_path
        except Exception as e:
            print(f"Download failed: {e}")
            return None

    def get_modules_for_demo(self, demo_path: Path) -> list[Path]:
        """Find all modules in a demo directory.

        Args:
            demo_path: Path to extracted demo

        Returns:
            List of module file paths found.
        """
        extensions = [".mod", ".s3m", ".xm", ".it", ".mtm", ".669"]
        modules = []

        for ext in extensions:
            modules.extend(demo_path.rglob(f"*{ext}"))

        return modules


def main():
    """CLI entry point for ModArchive integration."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: showet-modarchive [search|download|scan] [options]")
        print("\nCommands:")
        print("  search <query>     Search modules by keyword")
        print("  download <id>      Download module by ID")
        print("  scan <path>        Find modules in demo directory")
        print("\nExamples:")
        print("  showet-modarchive search 'future crew'")
        print("  showet-modarchive download 12345")
        sys.exit(1)

    api = ModArchiveAPI()
    command = sys.argv[1]

    if command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        modules = api.search_modules(query)
        print(f"Found {len(modules)} modules:")
        for m in modules[:10]:
            print(
                f"  [{m['id']}] {m['title']} by {m['artist']} ({m['format']})"
            )

    elif command == "download":
        if len(sys.argv) < 3:
            print("Error: Module ID required")
            sys.exit(1)
        module_id = int(sys.argv[2])
        path = api.download_module(module_id)
        if path:
            print(f"Module downloaded to: {path}")

    elif command == "scan":
        if len(sys.argv) < 3:
            print("Error: Directory path required")
            sys.exit(1)
        demo_path = Path(sys.argv[2])
        modules = api.get_modules_for_demo(demo_path)
        print(f"Found {len(modules)} modules in {demo_path}:")
        for m in modules:
            print(f"  {m.name}")


if __name__ == "__main__":
    main()