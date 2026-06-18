#!/usr/bin/env python3
"""Enhance ModArchive.org integration with demo-music linking.

Provides features:
- Search modules by demo group artists
- Auto-download music from demos
- Link modules to productions
"""

import json
import urllib.request
from pathlib import Path
from typing import Optional, List, Dict
from modarchive_integration import ModArchiveAPI


class ShowetModArchive(ModArchiveAPI):
    """Enhanced ModArchive integration for Showet demos."""

    # Known demoscene artists/groups for music module suggestions
    DEMO_ARTISTS = {
        "future crew": ["second reality", "unreal", "grimreefer"],
        "farbrausch": ["fr-08", "fr-10", "fr-11", "fr-12"],
        "conspiracy": ["heaven seven", "life is a miracle", "a line in the sand"],
        "fairlight": ["especially for you", "lightspeed"],
        "censor design": ["pain", "titanic"],
    }

    def find_modules_for_demo_group(self, group_name: str) -> List[Dict]:
        """Find modules by a demoscene group/artist name.
        
        Args:
            group_name: Demoscene group name (e.g., "Future Crew")
            
        Returns:
            List of modules by this artist
        """
        return self.search_modules(group_name)

    def find_modules_for_production(self, production_name: str) -> List[Dict]:
        """Find modules associated with a production.
        
        Searches for modules that might have been used in or 
        are related to a specific demo production.
        
        Args:
            production_name: Demo name (e.g., "Second Reality")
            
        Returns:
            List of potentially related modules
        """
        # Search for modules by production keywords
        keywords = production_name.lower().split()
        
        # Add common music-related suffixes
        for kw in keywords:
            results = self.search_modules(kw)
            if results:
                return results[:10]
        
        return []

    def download_modules_for_jukebox(self, demo_ids: List[int], 
                                    platform: str = "commodore_64") -> List[Path]:
        """Download modules for use in jukebox playback.
        
        Creates a collection of modules that can be played
        alongside demo playback.
        
        Args:
            demo_ids: List of Pouet demo IDs
            platform: Target platform for module format preference
            
        Returns:
            List of downloaded module paths
        """
        downloaded = []
        format_preference = {
            "commodore_64": "sid",
            "commodore_amiga": "mod",
            "zx_spectrum": "sid",
            "nintendo_famicom": "nsf",
        }.get(platform, "mod")
        
        # Find and download top modules for the platform
        modules = self.search_modules(f"type:{format_preference}")
        
        dest_dir = Path.home() / ".showet" / "jukebox_modules" / platform
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        for module in modules[:5]:  # Top 5 for jukebox
            path = self.download_module(module["id"], dest_dir)
            if path:
                downloaded.append(path)
        
        return downloaded


def main():
    """CLI entry point for enhanced ModArchive integration."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: showet-modarchive-enhanced [command]")
        print("\nCommands:")
        print("  search <query>              Search modules")
        print("  group-modules <artist>      Find modules by demoscene artist")
        print("  demo-modules <demo_name>    Find modules for a demo")
        print("  jukebox-modules <platform>  Download modules for jukebox")
        print("\nExamples:")
        print("  showet-modarchive-enhanced group-modules 'future crew'")
        print("  showet-modarchive-enhanced jukebox-modules commodore_64")
        sys.exit(1)
    
    api = ShowetModArchive()
    cmd = sys.argv[1]
    
    if cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        modules = api.search_modules(query)
        for m in modules[:10]:
            print(f"[{m['id']}] {m['title']} by {m['artist']} ({m['format']})")
    
    elif cmd == "group-modules":
        artist = sys.argv[2] if len(sys.argv) > 2 else ""
        modules = api.find_modules_for_demo_group(artist)
        print(f"Modules by {artist}:")
        for m in modules[:10]:
            print(f"  [{m['id']}] {m['title']} ({m['format']})")
    
    elif cmd == "demo-modules":
        demo = sys.argv[2] if len(sys.argv) > 2 else ""
        modules = api.find_modules_for_production(demo)
        print(f"Modules for {demo}:")
        for m in modules[:10]:
            print(f"  [{m['id']}] {m['title']} by {m['artist']}")
    
    elif cmd == "jukebox-modules":
        platform = sys.argv[2] if len(sys.argv) > 2 else "commodore_64"
        paths = api.download_modules_for_jukebox([], platform)
        print(f"Downloaded {len(paths)} modules for {platform} jukebox")
        for p in paths:
            print(f"  {p}")


if __name__ == "__main__":
    main()