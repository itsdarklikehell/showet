#!/usr/bin/env python3
"""Showet ModArchive CLI wrapper - Enhanced music module integration."""

import sys
import json
from pathlib import Path
from modarchive_integration import ModArchiveAPI


def main():
    """Entry point for showet-modarchive CLI command."""
    if len(sys.argv) < 2:
        print("Usage: showet-modarchive [search|download|scan|demo-search] [options]")
        print("\nCommands:")
        print("  search <query>       Search modules by keyword/artist/format")
        print("  download <id>        Download module by ID")
        print("  scan <path>          Find modules in demo directory")
        print("  demo-search <demo>   Find modules for a demoscene production")
        print("\nExamples:")
        print("  showet-modarchive search 'future crew'")
        print("  showet-modarchive download 12345")
        print("  showet-modarchive demo-search 'second reality'")
        sys.exit(1)
    
    api = ModArchiveAPI()
    command = sys.argv[1]
    
    if command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        format_filter = None
        artist_filter = None
        
        # Parse optional filters
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--format" and i + 1 < len(sys.argv):
                format_filter = sys.argv[i + 1]
                i += 1
            elif sys.argv[i] == "--artist" and i + 1 < len(sys.argv):
                artist_filter = sys.argv[i + 1]
                i += 1
            i += 1
        
        modules = api.search_modules(query, format=format_filter, artist=artist_filter)
        print(f"Found {len(modules)} modules:")
        for m in modules[:15]:
            print(f"  [{m['id']}] {m['title']} by {m['artist']} ({m['format']})")
    
    elif command == "download":
        if len(sys.argv) < 3:
            print("Error: Module ID required")
            sys.exit(1)
        dest = None
        module_id = int(sys.argv[2])
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--output" and i + 1 < len(sys.argv):
                dest = Path(sys.argv[i + 1])
                i += 1
            i += 1
        
        path = api.download_module(module_id, dest)
        if path:
            print(f"Module downloaded to: {path}")
    
    elif command == "scan":
        if len(sys.argv) < 3:
            print("Error: Directory path required")
            sys.exit(1)
        demo_path = Path(sys.argv[2])
        modules = api.get_modules_for_demo(demo_path)
        print(f"Found {len(modules)} modules in {demo_path}:")
        for m in modules:
            print(f"  {m.name}")
    
    elif command == "demo-search":
        # Search for modules associated with a demo
        demo_query = sys.argv[2] if len(sys.argv) > 2 else ""
        modules = api.search_modules(demo_query)
        print(f"Modules related to '{demo_query}':")
        for m in modules[:10]:
            print(f"  [{m['id']}] {m['title']} by {m['artist']} ({m['format']})")


if __name__ == "__main__":
    main()