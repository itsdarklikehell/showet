#!/usr/bin/env python3
"""Showet Cache CLI - Manage offline demo cache with sync capabilities.

Commands:
  showet-cache add <demo_id> <path>     Add demo to cache
  showet-cache list                     List cached demos
  showet-cache playlist <name>            Create playlist
  showet-cache sync export <file>         Export cache manifest
  showet-cache sync import <file>         Import cache manifest
"""

import json
import sys
from pathlib import Path
from showet.utils.async_io import DemoCache


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        return 0

    cache = DemoCache()
    cmd = sys.argv[1]

    if cmd == "add" and len(sys.argv) >= 4:
        demo_id = int(sys.argv[2])
        path = sys.argv[3]
        cache.add_demo(demo_id, "manual", f"Demo {demo_id}", "unknown", path)
        print(f"✅ Added demo {demo_id} to cache")

    elif cmd == "list":
        demos = cache.list_all()
        for d in demos:
            print(f"  {d['pouet_id']}: {d['title'][:40]} ({d['platform']})")

    elif cmd == "playlist" and len(sys.argv) >= 3:
        name = sys.argv[2]
        if len(sys.argv) >= 4:
            demo_ids = [int(x) for x in sys.argv[3:]]
            cache.create_playlist(name, demo_ids)
            print(f"✅ Created playlist '{name}' with {len(demo_ids)} demos")
        else:
            ids = cache.get_playlist(name)
            if ids:
                print(f"Playlist '{name}': {ids}")
            else:
                print(f"No playlist '{name}'")

    elif cmd == "sync":
        if len(sys.argv) >= 4:
            if sys.argv[2] == "export":
                dest = Path(sys.argv[3])
                count = cache.export_sync_manifest(dest)
                print(f"✅ Exported {count} demos to {dest}")
            elif sys.argv[2] == "import":
                src = Path(sys.argv[3])
                count = cache.import_sync_manifest(src)
                print(f"✅ Imported {count} demos from {src}")
        else:
            print("Usage: showet-cache sync [export|import] <file>")

    else:
        print(__doc__)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())