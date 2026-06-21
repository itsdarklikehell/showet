"""Scene.org integration module for Showet.

Fetch demos directly from the scene.org file archives.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from urllib.parse import quote

import requests

SCENE_ORG_BASE = "https://files.scene.org"


class SceneOrgClient:
    """Client for scene.org file archives."""

    def __init__(self, download_dir: str = "demos"):
        self.download_dir = download_dir
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Showet Demo Runner/4.0 (+https://github.com/itsdarklikehell/showet)"
        })

    def search_demos(self, query: str, limit: int = 50) -> list[dict]:
        """Search scene.org for demo files."""
        results = []
        
        known_paths = [
            "/parties/assembly", "/parties/breakpoint", "/parties/revision",
            "/parties/synchronicity", "/parties/theparty", "/demos",
        ]
        
        for path in known_paths[:10]:
            try:
                url = f"{SCENE_ORG_BASE}{path}/{quote(query)}.zip"
                response = self.session.head(url, timeout=2)
                if response.status_code == 200:
                    results.append({
                        "name": query,
                        "url": url,
                        "type": "archive",
                        "size": response.headers.get("Content-Length", "unknown"),
                    })
                    if len(results) >= limit:
                        break
            except Exception:
                continue
                
        return results

    def get_party_demos(self, party: str, year: Optional[int] = None) -> list[dict]:
        """Get demos from a specific demoparty."""
        results = []
        path = f"/parties/{party}/{year}" if year else f"/parties/{party}"
        
        try:
            url = f"{SCENE_ORG_BASE}{path}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                from html.parser import HTMLParser
                
                class LinkExtractor(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.links = []
                        
                    def handle_starttag(self, tag, attrs):
                        if tag == "a":
                            for attr, value in attrs:
                                if value and any(value.endswith(ext) for ext in ['.zip', '.exe', '.lha', '.rar']):
                                    self.links.append(value)
                                    
                parser = LinkExtractor()
                parser.feed(response.text)
                
                for link in parser.links[:20]:
                    results.append({"name": os.path.basename(link), "url": f"{url}/{link}"})
        except Exception:
            pass
            
        return results

    def download_demo(self, url: str, filename: Optional[str] = None) -> str:
        """Download a demo file from scene.org."""
        os.makedirs(self.download_dir, exist_ok=True)
        
        if not filename:
            filename = url.split("/")[-1]
            
        local_path = os.path.join(self.download_dir, filename)
        
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return local_path
        except Exception:
            return ""