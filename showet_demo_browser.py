#!/usr/bin/env python3
"""Showet Demo Browser - Web UI API backend.

Provides HTTP endpoints for the web-based demo browser UI.
Integrates with nostalgist.js config files and SQLite cache.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import JSONResponse
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


def get_cached_demos() -> list[dict]:
    """Get demo list from SQLite cache."""
    try:
        from showet.utils.async_io import DemoCache
        cache = DemoCache()
        return cache.list_all()
    except Exception:
        return []


def get_platform_configs() -> list[dict]:
    """Get all nostalgist.js platform configs."""
    config_dir = Path(__file__).parent / "nostalgist_configs"
    manifest_path = config_dir / "manifest.json"
    
    if not manifest_path.exists():
        return []
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    return manifest.get("platforms", [])


def search_demos(query: str, limit: int = 20) -> list[dict]:
    """Search demos by title or platform."""
    demos = get_cached_demos()
    query_lower = query.lower()
    
    results = []
    for demo in demos:
        title = demo.get("title", "").lower()
        platform = demo.get("platform", "").lower()
        if query_lower in title or query_lower in platform:
            results.append(demo)
    
    return results[:limit]


if FASTAPI_AVAILABLE:
    app = FastAPI(title="Showet Demo Browser API")
    
    @app.get("/api/platforms")
    async def api_platforms():
        """List all supported platforms."""
        return JSONResponse(get_platform_configs())
    
    @app.get("/api/demos")
    async def api_demos(limit: int = 50):
        """Get cached demos."""
        return JSONResponse(get_cached_demos()[:limit])
    
    @app.get("/api/demos/{demo_id}")
    async def api_demo(demo_id: int):
        """Get specific demo info."""
        from showet.utils.async_io import DemoCache
        cache = DemoCache()
        path = cache.get_cached(demo_id)
        
        if not path:
            raise HTTPException(status_code=404, detail="Demo not found")
        
        return JSONResponse({
            "id": demo_id,
            "path": path,
            "exists": Path(path).exists() if path else False
        })
    
    @app.get("/api/search")
    async def api_search(q: str, limit: int = 20):
        """Search demos."""
        return JSONResponse(search_demos(q, limit))
else:
    app = None


def main() -> int:
    """CLI entry point."""
    import argparse
    import uvicorn
    
    parser = argparse.ArgumentParser(description="Showet Demo Browser")
    parser.add_argument("--serve", "-s", action="store_true", help="Start web server")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Server port")
    parser.add_argument("--list-platforms", "-l", action="store_true", help="List platforms")
    args = parser.parse_args()

    if args.list_platforms:
        configs = get_platform_configs()
        print(f"Loaded {len(configs)} platform configs")
        for c in configs[:5]:
            print(f"  - {c.get('slug')}: {c.get('core')}")
            
    if args.serve:
        if app is None:
            print("FastAPI not installed. Install with: pip install fastapi uvicorn")
            return 1
        print(f"🚀 Starting Showet Demo Browser on port {args.port}")
        uvicorn.run(app, host="0.0.0.0", port=args.port)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())