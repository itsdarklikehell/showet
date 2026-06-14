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
        else:
            self._send_error("Not found", 404)

    def _handle_platforms(self) -> None:
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

        import argparse
        args = argparse.Namespace(pouetid=prod_id, platforms=False, random=False)

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