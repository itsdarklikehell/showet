#!/usr/bin/env python3
"""HTTP API for showet demo viewer.

Provides REST endpoints for:
- GET /api/platforms - List supported platforms
- GET /api/search - Search pouet.net productions
- POST /api/run/<id> - Run a demo
- GET /* - Serve static UI files
"""
from __future__ import annotations

import json
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any

# Import showet functionality
import showet
from cache_manager import CacheManager
from favorites_manager import FavoritesManager

# Initialize managers
cache = CacheManager()
favorites = FavoritesManager()


class ShowetAPIHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for showet API with static file serving."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent / "showet-ui"), **kwargs)

    def _send_json(self, data: Any, status: int = 200) -> None:
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_error(self, message: str, status: int = 400) -> None:
        """Send error response."""
        self._send_json({"error": message, "success": False}, status)

    def do_GET(self) -> None:
        """Handle GET requests."""
        if self.path == "/api/platforms":
            self._handle_platforms()
        elif self.path.startswith("/api/search"):
            self._handle_search()
        elif self.path == "/api/cache":
            self._handle_cache_list()
        elif self.path == "/api/favorites":
            self._handle_favorites_list()
        elif self.path.startswith("/api/random"):
            self._handle_random()
        elif self.path.startswith("/api/cache/"):
            prod_id = self.path.split("/")[-1]
            self._handle_cache_get(prod_id)
        elif self.path.startswith("/api/favorites/"):
            prod_id = self.path.split("/")[-1]
            self._handle_favorites_get(prod_id)
        elif self.path == "/" or self.path == "/index.html":
            self._serve_index()
        else:
            # Serve static files
            super().do_GET()

    def _serve_index(self) -> None:
        """Serve the index.html file."""
        index_path = Path(__file__).parent / "showet-ui" / "index.html"
        if index_path.exists():
            content = index_path.read_text()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())
            return
        self._send_error("Index not found", 404)

    def do_POST(self) -> None:
        """Handle POST requests."""
        if self.path.startswith("/api/run/"):
            self._handle_run()
        elif self.path.startswith("/api/favorites/"):
            prod_id = self.path.split("/")[-1]
            self._handle_favorites_add(prod_id)
        elif self.path.startswith("/api/cache/clear"):
            self._handle_cache_clear()
        else:
            self._send_error("Not found", 404)

    def do_DELETE(self) -> None:
        """Handle DELETE requests."""
        if self.path.startswith("/api/favorites/"):
            prod_id = self.path.split("/")[-1]
            self._handle_favorites_remove(prod_id)
        elif self.path.startswith("/api/cache/"):
            prod_id = self.path.split("/")[-1]
            self._handle_cache_remove(prod_id)
        else:
            self._send_error("Not found", 404)

    def _handle_cache_list(self) -> None:
        """List all cached demos."""
        demos = cache.list_cached_demos()
        cache_size = cache.get_cache_size()
        self._send_json({
            "success": True,
            "demos": demos,
            "count": len(demos),
            "cache_size_bytes": cache_size,
            "cache_size_human": self._format_bytes(cache_size)
        })

    def _handle_cache_get(self, prod_id: str) -> None:
        """Get cache info for a specific demo."""
        try:
            prod_id_int = int(prod_id)
        except ValueError:
            self._send_error("Invalid production ID")
            return

        if not cache.is_cached(prod_id_int):
            self._send_json({"success": False, "cached": False}, 404)
            return

        path = cache.get_cached_path(prod_id_int)
        meta = cache.get_metadata(prod_id_int)
        self._send_json({
            "success": True,
            "cached": True,
            "path": str(path) if path else None,
            "metadata": meta
        })

    def _handle_cache_remove(self, prod_id: str) -> None:
        """Remove a demo from cache."""
        try:
            prod_id_int = int(prod_id)
        except ValueError:
            self._send_error("Invalid production ID")
            return

        removed = cache.remove_demo(prod_id_int)
        self._send_json({
            "success": removed,
            "message": "Demo removed from cache" if removed else "Demo not in cache"
        })

    def _handle_cache_clear(self) -> None:
        """Clear all cached demos."""
        cache.clear_cache()
        self._send_json({
            "success": True,
            "message": "Cache cleared"
        })

    def _handle_favorites_list(self) -> None:
        """List all favorite demos."""
        favs = favorites.list_favorites()
        self._send_json({
            "success": True,
            "favorites": favs,
            "count": len(favs)
        })

    def _handle_favorites_get(self, prod_id: str) -> None:
        """Check if a demo is favorited and get its metadata."""
        try:
            prod_id_int = int(prod_id)
        except ValueError:
            self._send_error("Invalid production ID")
            return

        if not favorites.is_favorite(prod_id_int):
            self._send_json({"success": False, "favorited": False}, 404)
            return

        meta = favorites.get_favorite(prod_id_int)
        self._send_json({
            "success": True,
            "favorited": True,
            "metadata": meta
        })

    def _handle_favorites_add(self, prod_id: str) -> None:
        """Add a demo to favorites (reads JSON body)."""
        try:
            prod_id_int = int(prod_id)
        except ValueError:
            self._send_error("Invalid production ID")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self._send_error("Missing request body")
            return

        try:
            data = json.loads(self.rfile.read(content_length).decode())
        except json.JSONDecodeError:
            self._send_error("Invalid JSON")
            return

        name = data.get("name", "")
        platform = data.get("platform", "")
        notes = data.get("notes", "")

        if not name:
            self._send_error("Missing 'name' field")
            return

        favorites.add_favorite(prod_id_int, name, platform, notes)
        self._send_json({
            "success": True,
            "message": "Added to favorites"
        })

    def _handle_favorites_remove(self, prod_id: str) -> None:
        """Remove a demo from favorites."""
        try:
            prod_id_int = int(prod_id)
        except ValueError:
            self._send_error("Invalid production ID")
            return

        removed = favorites.remove_favorite(prod_id_int)
        self._send_json({
            "success": removed,
            "message": "Removed from favorites" if removed else "Demo not in favorites"
        })

    def _handle_random(self) -> None:
        """Get a random demo from pouet.net."""
        import random
        import urllib.parse

        # Search for random terms to get varied results
        random_terms = ["demo", "intro", "64k", "4k", "music", "animation"]
        query = random.choice(random_terms)

        url = f"http://api.pouet.net/v1/search/prod/?q={query}"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            if data.get("success") and data.get("results"):
                # Pick a random result
                results = list(data["results"].items())
                if results:
                    random_prod = random.choice(results)
                    prod_id, prod_info = random_prod
                    self._send_json({
                        "success": True,
                        "id": prod_id,
                        **prod_info
                    })
                    return
        except Exception as e:
            pass

        self._send_error("Could not find a random demo")

    def _format_bytes(self, bytes_count: int) -> str:
        """Format bytes as human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.1f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.1f} TB"
        """Return list of supported platforms."""
        runners = showet.create_platform_runners()
        platforms = []
        seen = set()
        for runner in runners:
            for platform in runner.supported_platforms():
                if platform not in seen:
                    platforms.append(platform)
                    seen.add(platform)
        self._send_json({"success": True, "platforms": sorted(platforms)})

    def _handle_search(self) -> None:
        """Search pouet.net for productions."""
        query = ""
        if "?" in self.path:
            params = self.path.split("?")[1]
            for param in params.split("&"):
                if param.startswith("q="):
                    query = param[2:]

        if not query:
            self._send_error("Missing query parameter 'q'")
            return

        url = f"http://api.pouet.net/v1/search/prod/?q={query}"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            self._send_json(data)
        except Exception as e:
            self._send_error(f"Search failed: {e}")

    def _handle_run(self) -> None:
        """Run a demo by pouet ID."""
        try:
            prod_id = int(self.path.split("/")[-1])
        except ValueError:
            self._send_error("Invalid production ID")
            return

        # Parse query params for options
        fullscreen = "fullscreen=true" in self.path
        no_audio = "no_audio=true" in self.path
        core = None
        if "core=" in self.path:
            import urllib.parse
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            core = params.get("core", [None])[0]

        import argparse
        args = argparse.Namespace(
            pouetid=prod_id,
            platforms=False,
            random=False,
            fullscreen=fullscreen,
            no_audio=no_audio,
            core=core,
        )

        runners = showet.create_platform_runners()
        result = showet.run_production(args, runners)

        self._send_json({
            "success": result == 0,
            "message": "Demo launched" if result == 0 else "Failed to launch demo"
        })

    def log_message(self, format: str, *args) -> None:
        """Log to stdout instead of stderr."""
        pass


def main(port: int = 8765) -> None:
    """Start the HTTP API server."""
    server = HTTPServer(("", port), ShowetAPIHandler)
    print(f"Showet API server running on http://localhost:{port}")
    print("Endpoints: /api/platforms, /api/search?q=..., /api/run/<id>")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()