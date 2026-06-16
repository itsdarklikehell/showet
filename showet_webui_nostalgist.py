#!/usr/bin/env python3
"""
Showet nostalgist.js integration server.

Serves platform configurations and demos to the nostalgist.js frontend.
Uses Flask/SimpleHTTP for demo purposes - can be adapted to any WSGI server.

Usage:
    python3 showet_webui_nostalgist.py

Then open showet-viewer.html in a browser.
"""

import json
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs


# Core name mapping (mirrors nostalgist_bridge.py)
CORE_MAPPING: Dict[str, str] = {
    "quicknes_libretro": "quicknes",
    "genesis_plus_gx_libretro": "genesis_plus_gx",
    "vice_x64sc_libretro": "vice_x64sc",
    "snes9x_libretro": "snes9x",
    "picodrive_libretro": "picodrive",
    # ... more mappings as needed
}


class NostalgistConfigHandler(SimpleHTTPRequestHandler):
    """Custom handler to serve platform configs dynamically."""

    def __init__(self, *args, **kwargs):
        self.project_root = Path(__file__).parent
        super().__init__(*args, directory=str(self.project_root), **kwargs)

    def do_GET(self):
        """Handle GET requests for config endpoints."""
        parsed = urlparse(self.path)
        
        if parsed.path == "/nostalgist/config":
            self.handle_config_request(parse_qs(parsed.query))
        elif parsed.path.startswith("/nostalgist/rom/"):
            # Proxy to ROM file
            self.handle_rom_request(parsed.path)
        else:
            super().do_GET()

    def handle_config_request(self, query: Dict[str, str]):
        """Generate and serve nostalgist config for a platform."""
        platform = query.get("platform", [None])[0]
        
        if not platform:
            self.send_error(400, "Missing platform parameter")
            return
        
        # Find the platform module
        platform_file = self.project_root / f"Platform_{platform}.py"
        if not platform_file.exists():
            # Try underscore format
            platform_file = self.project_root / f"Platform_{platform.replace('-', '_')}.py"
        
        if not platform_file.exists():
            # Search for matching platform
            for pf in self.project_root.glob(f"Platform_*{platform}*.py"):
                platform_file = pf
                break
        
        if platform_file.exists():
            content = platform_file.read_text()
            core_match = re.search(r'cores\s*=\s*\[([^\]]+)\]', content)
            slug_match = re.search(r'super\(\).__init__\("([^"]+)"', content)
            
            core = core_match.group(1).strip().strip("'\"") if core_match else "quicknes"
            slug = slug_match.group(1) if slug_match else platform
            mapped_core = CORE_MAPPING.get(core, core.replace("_libretro", ""))
            
            config = {
                "core": mapped_core,
                "rom": f"/nostalgist/rom/{platform}/",
                "shader": "crt/crt-easymode",
            }
        else:
            config = {"error": f"Platform {platform} not found"}
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(config).encode())

    def handle_rom_request(self, path: str):
        """Serve ROM files (placeholder - implement your download logic)."""
        # This would integrate with showet's download system
        # For now, return placeholder
        self.send_error(501, "ROM serving not yet implemented")