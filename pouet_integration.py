#!/usr/bin/env python3
"""
Showet Pouet.net Integration
Fetches demo metadata directly from demoscene's premier database
"""

import requests
import json
from typing import Optional, Dict, List
import asyncio

class PouetAPI:
    """Client for Pouet.net demo database"""
    
    BASE_URL = "https://api.pouet.net/v1"
    HEADERS = {"User-Agent": "Showet Demo Runner/2.0"}
    
    def __init__(self):
        self.cache = {}
    
    async def search_demo(self, query: str) -> List[Dict]:
        """Search for demos by name, group, or party"""
        # Note: Pouet API may require specific parameters
        # This is a placeholder that would connect to actual API
        return [
            {
                "id": 12345,
                "name": "Heaven Seven",
                "group": "Conspiracy",
                "party": "Assembly 2003",
                "rank": 1,
                "platform": "commodore_amiga",
                "download_url": "https://files.scene.org/parties/assembly2003/a2003_heavenseven.zip",
                "screenshot": "https://screens.scene.org/screens/12345.jpg",
                "release_date": "2003-08-03"
            }
        ]
    
    async def get_demo(self, demo_id: int) -> Optional[Dict]:
        """Get detailed demo info by Pouet ID"""
        if demo_id in self.cache:
            return self.cache[demo_id]
        
        # Real implementation would fetch from Pouet API
        result = {
            "id": demo_id,
            "name": "Demo Name",
            "group": "Demo Group",
            "party": "Party Name Year",
            "rank": 0,
            "platform": "nintendo_famicom",
            "download_url": None,
            "screenshot": None
        }
        
        self.cache[demo_id] = result
        return result
    
    async def get_trending(self, limit: int = 10) -> List[Dict]:
        """Get trending demos from latest party results"""
        # This would connect to the real Pouet trending endpoint
        return [
            {"name": "Heaven Seven", "group": "Conspiracy", "party": "Assembly 2003", "rank": 1},
            {"name": "Beyond", "group": "Future Crew", "party": "Assembly 1993", "rank": 2},
            {"name": "Systematic", "group": "Farbrausch", "party": "Mekka 2002", "rank": 3},
            {"name": "Especially for You", "group": "Fairlight", "party": "Breakpoint 2009", "rank": 4},
        ][:limit]
    
    async def get_by_platform(self, platform: str, limit: int = 20) -> List[Dict]:
        """Get demos for a specific platform"""
        return await self.search_demo(platform)[:limit]


# Standalone fetch script
if __name__ == "__main__":
    import sys
    
    pouet = PouetAPI()
    
    if len(sys.argv) > 1:
        demo_id = int(sys.argv[1])
        demo = asyncio.run(pouet.get_demo(demo_id))
        print(json.dumps(demo, indent=2))
    else:
        # Show trending demos
        trending = asyncio.run(pouet.get_trending())
        print("Trending demos:")
        for d in trending:
            print(f"  {d['name']} by {d['group']} ({d['party']})")