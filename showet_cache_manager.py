#!/usr/bin/env python3
"""
Showet Local Cache Manager
Offline demo playback support - download once, play anywhere
Integrates with scene.org and Pouet.net for caching
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

CACHE_DIR = Path.home() / ".showet" / "cache"
METADATA_FILE = CACHE_DIR / "cache_metadata.json"

class ShowetCache:
    """Local cache manager for offline demo playback"""
    
    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.cache_dir = cache_dir
        self.metadata = {}
        self._load_metadata()
        
    def _load_metadata(self):
        """Load cache metadata from disk"""
        if METADATA_FILE.exists():
            with open(METADATA_FILE) as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"files": {}, "total_size": 0}
    
    def _save_metadata(self):
        """Save cache metadata to disk"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        with open(METADATA_FILE, "w") as f:
            json.dump(self.metadata, f, indent=2)
    
    def _get_file_hash(self, path: Path) -> str:
        """Calculate MD5 hash for file deduplication"""
        if not path.exists():
            return ""
        return hashlib.md5(path.read_bytes()).hexdigest()[:8]
    
    def cache_demo(self, url: str, platform: str, name: str) -> Path:
        """Download and cache a demo for offline playback"""
        # Create platform subdirectory
        platform_dir = self.cache_dir / platform
        platform_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine filename
        safe_name = name.replace(" ", "_").replace("/", "-")
        filename = f"{safe_name}.zip"
        cache_path = platform_dir / filename
        
        # Download if not exists
        if not cache_path.exists():
            try:
                import requests
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                cache_path.write_bytes(response.content)
                self.metadata["total_size"] += cache_path.stat().st_size
            except Exception as e:
                print(f"Cache download failed: {e}")
                return None
        
        # Update metadata
        file_hash = self._get_file_hash(cache_path)
        self.metadata["files"][str(cache_path)] = {
            "url": url,
            "platform": platform,
            "name": name,
            "size": cache_path.stat().st_size,
            "hash": file_hash,
            "cached_at": str(Path.cwd())
        }
        self._save_metadata()
        
        return cache_path
    
    def get_cached_demo(self, name: str, platform: str = None) -> Optional[Path]:
        """Get cached demo path if available"""
        for file_path, meta in self.metadata.get("files", {}).items():
            if meta["name"].lower() == name.lower():
                if platform is None or meta["platform"].lower() == platform.lower():
                    path = Path(file_path)
                    if path.exists():
                        return path
        return None
    
    def list_cached(self) -> List[Dict]:
        """List all cached demos"""
        return list(self.metadata.get("files", {}).values())
    
    def cache_status(self) -> Dict:
        """Get cache statistics"""
        return {
            "total_files": len(self.metadata.get("files", {})),
            "total_size_mb": self.metadata.get("total_size", 0) / (1024 * 1024),
            "cache_dir": str(self.cache_dir)
        }
    
    def clear_cache(self, platform: str = None):
        """Clear cache for platform or entire cache"""
        to_delete = []
        for file_path, meta in self.metadata.get("files", {}).items():
            if platform is None or meta["platform"] == platform:
                to_delete.append(file_path)
        
        for fp in to_delete:
            path = Path(fp)
            if path.exists():
                self.metadata["total_size"] -= path.stat().st_size
                path.unlink()
            del self.metadata["files"][fp]
        
        self._save_metadata()


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Showet Cache Manager")
    parser.add_argument("--cache", "-c", help="Cache a demo URL")
    parser.add_argument("--platform", "-p", help="Platform for demo")
    parser.add_argument("--name", "-n", help="Demo name")
    parser.add_argument("--list", "-l", action="store_true", help="List cached demos")
    parser.add_argument("--status", "-s", action="store_true", help="Show cache status")
    parser.add_argument("--clear", action="store_true", help="Clear cache")
    args = parser.parse_args()
    
    cache = ShowetCache()
    
    if args.cache:
        path = cache.cache_demo(args.cache, args.platform or "unknown", args.name or "downloaded")
        print(f"Cached to: {path}")
    elif args.list:
        for demo in cache.list_cached():
            print(f"  {demo['name']} ({demo['platform']})")
    elif args.status:
        status = cache.cache_status()
        print(f"Cache: {status['total_files']} files, {status['total_size_mb']:.1f}MB")
        print(f"Location: {status['cache_dir']}")
    elif args.clear:
        cache.clear_cache()
        print("Cache cleared")


if __name__ == "__main__":
    main()