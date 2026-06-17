#!/usr/bin/env python3
"""
Showet Scene.org Integration
Fetch demos directly from the scene.org file archives
The definitive demoscene archive since 1997
"""

import requests
from typing import Optional, Dict, List
from urllib.parse import quote
import os

SCENE_ORG_BASE = "https://files.scene.org"
SCENE_SEARCH_ENDPOINT = "https://web.archive.org/cdx/search/cdx"

class SceneOrgClient:
    """Client for scene.org file archives and search"""
    
    def __init__(self, download_dir: str = "demos"):
        self.download_dir = download_dir
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Showet Demo Runner/2.1 (+https://github.com/itsdarklikehell/showet)"})
        
    def search_demos(self, query: str, limit: int = 50) -> List[Dict]:
        """Search scene.org for demo files
        
        Args:
            query: Search term (demo name, group, party, etc.)
            limit: Maximum results to return
            
        Returns:
            List of demo metadata with download URLs
        """
        # Scene.org doesn't have a public search API, but we can use:
        # - Wayback Machine CDX API for historical listings
        # - Direct URL guessing for known parties/paths
        results = []
        
        # Common party paths on scene.org
        known_paths = [
            "/parties/assembly",
            "/parties/breakpoint", 
            "/parties/revision",
            "/parties/synchronicity",
            "/parties/theparty",
            "/parties/mekka",
            "/demos",
            "/music",
            "/graphics"
        ]
        
        # Try to find demos in known locations
        for path in known_paths[:10]:  # Limit search
            try:
                url = f"{SCENE_ORG_BASE}{path}/{quote(query)}.zip"
                response = self.session.head(url, timeout=2)
                if response.status_code == 200:
                    results.append({
                        "name": query,
                        "url": url,
                        "type": "archive",
                        "size": response.headers.get("Content-Length", "unknown")
                    })
                    if len(results) >= limit:
                        break
            except:
                continue
                
        return results
    
    def get_party_demos(self, party: str, year: Optional[int] = None) -> List[Dict]:
        """Get demos from a specific demoparty
        
        Args:
            party: Party name (e.g., 'assembly', 'revision', 'breakpoint')
            year: Optional year filter
            
        Returns:
            List of demos with download info
        """
        results = []
        
        # Construct party URL
        if year:
            path = f"/parties/{party}/{year}"
        else:
            path = f"/parties/{party}"
            
        try:
            url = f"{SCENE_ORG_BASE}{path}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                # Parse HTML for .zip/.exe/.lha links
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
                
                for link in parser.links[:limit]:
                    results.append({
                        "name": os.path.basename(link),
                        "url": f"{url}/{link}" if not link.startswith('http') else link,
                        "type": "demo"
                    })
        except Exception as e:
            print(f"Error fetching party demos: {e}")
            
        return results
    
    def download_demo(self, url: str, filename: Optional[str] = None) -> str:
        """Download a demo file from scene.org
        
        Args:
            url: Direct download URL
            filename: Optional custom filename
            
        Returns:
            Local path to downloaded file
        """
        os.makedirs(self.download_dir, exist_ok=True)
        
        if not filename:
            filename = url.split("/")[-1]
            
        local_path = os.path.join(self.download_dir, filename)
        
        try:
            print(f"Downloading {filename} from scene.org...")
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            print(f"Saved to: {local_path}")
            return local_path
            
        except Exception as e:
            print(f"Download failed: {e}")
            return ""
    
    def get_download_path(self, demo_name: str, platform: str = "commodore_amiga") -> str:
        """Get the expected scene.org download path for a demo
        
        Args:
            demo_name: Name of the demo
            platform: Target platform
            
        Returns:
            Constructed download URL
        """
        # Common patterns for scene.org demo paths
        patterns = [
            f"/parties/assembly/{demo_name.lower().replace(' ', '_')}.zip",
            f"/parties/revision/{demo_name.lower().replace(' ', '_')}.zip",
            f"/demos/{demo_name.lower().replace(' ', '_')}.zip",
        ]
        
        for pattern in patterns:
            yield f"{SCENE_ORG_BASE}{pattern}"


# CLI interface
if __name__ == "__main__":
    import sys
    
    client = SceneOrgClient()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--party" and len(sys.argv) > 2:
            party = sys.argv[2]
            year = int(sys.argv[3]) if len(sys.argv) > 3 else None
            demos = client.get_party_demos(party, year)
            for d in demos:
                print(f"  {d['name']} - {d['url']}")
        elif sys.argv[1] == "--download" and len(sys.argv) > 2:
            url = sys.argv[2]
            client.download_demo(url)
        else:
            query = sys.argv[1]
            results = client.search_demos(query)
            for r in results:
                print(f"  {r.get('name', 'Unknown')} - {r.get('url', 'N/A')}")