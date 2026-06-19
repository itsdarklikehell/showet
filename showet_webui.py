#!/usr/bin/env python3
"""Showet Web UI - Browser-based demo interface.

Provides a web server for browsing and running demos from any device.
Integrates with nostalgist.js for browser-based emulation.
"""

import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs


class ShowetWebUI(SimpleHTTPRequestHandler):
    """HTTP handler for Showet web interface."""

    def __init__(self, *args, **kwargs):
        self.project_root = Path(__file__).parent
        self.nostalgist_configs = self.project_root / "nostalgist_configs"
        super().__init__(*args, directory=str(self.project_root), **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/platforms":
            self._handle_api_platforms()
        elif path == "/api/demos/search":
            query = parse_qs(parsed.query).get("q", [""])[0]
            self._handle_api_search(query)
        elif path == "/api/demo/info":
            demo_id = parse_qs(parsed.query).get("id", [""])[0]
            self._handle_api_demo_info(demo_id)
        else:
            super().do_GET()

    def _handle_api_platforms(self):
        """Return list of supported platforms."""
        platforms = []
        config_dir = self.nostalgist_configs

        if config_dir.exists():
            for config_file in config_dir.glob("*.json"):
                if config_file.name == "manifest.json":
                    continue
                data = json.loads(config_file.read_text())
                platforms.append({
                    "slug": config_file.stem,
                    "core": data.get("core", ""),
                    "extensions": data.get("extensions", []),
                })

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(platforms).encode())

    def _handle_api_search(self, query: str):
        """Search demos via Pouet.net API."""
        try:
            import urllib.request
            url = f"http://api.pouet.net/v1/search/prod/?q={query}"
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode())

            results = []
            for prod_id, prod in list(data.get("results", {}).items())[:20]:
                results.append({
                    "id": int(prod_id),
                    "name": prod.get("name", "Unknown"),
                    "type": prod.get("type", ""),
                    "score": prod.get("score", 0),
                })

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def _handle_api_demo_info(self, demo_id: str):
        """Get demo info from Pouet.net."""
        try:
            import urllib.request
            url = f"http://api.pouet.net/v1/prod/?id={demo_id}"
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode())

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data.get("prod", {})).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())


def launch_browser(port: int = 8765) -> int:
    """Open the web UI in a browser."""
    url = f"http://localhost:{port}"
    print(f"Opening {url} in browser...")
    webbrowser.open(url)
    return 0


def main(port: int = 8765) -> int:
    """Run the web server."""
    print(f"🌐 Showet Web UI starting on port {port}")
    print(f"   Open http://localhost:{port} in your browser")
    print("   Or use showet-webui --browser to auto-open")

    server = HTTPServer(("0.0.0.0", port), ShowetWebUI)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())