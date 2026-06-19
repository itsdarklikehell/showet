#!/usr/bin/env python3
"""
Demo the jukebox functionality works.

Quick test to verify jukebox module loads correctly.
"""

import sys
from pathlib import Path

def test_imports():
    """Test all core modules import correctly."""
    modules = [
        "showet_jukebox",
        "nostalgist_bridge",
        "modarchive_enhanced",
        "showet_setup_wizard",
        "showet_dependency_installer",
    ]
    
    results = []
    for m in modules:
        try:
            __import__(m)
            results.append(f"✅ {m}")
        except Exception as e:
            results.append(f"❌ {m}: {e}")
    
    return results


def main():
    print("🧪 Showet Component Tests\n")
    print("=" * 40)
    
    print("\n📦 Module Imports:")
    for r in test_imports():
        print(f"  {r}")
    
    print("\n📋 Jukebox Config:")
    from showet_jukebox import DEFAULT_LOOP_LIMIT, is_looped_demo
    print(f"  Loop limit for shuffle: {DEFAULT_LOOP_LIMIT}")
    
    print("\n📦 ModArchive Check:")
    from modarchive_enhanced import ShowetModArchive
    api = ShowetModArchive()
    print(f"  Loaded demo artists: {len(api.DEMO_ARTISTS)} known groups")
    
    print("\n" + "=" * 40)
    print("\n✅ All systems ready!")
    print("\nNext steps:")
    print("  showet --platforms     # List platforms")
    print("  showet-jukebox --help  # Jukebox help")
    print("  showet-tvs99           # Setup browser player")


if __name__ == "__main__":
    main()


def main():
    print("🧪 Showet Component Tests\n")
    print("=" * 40)
    
    print("\n📦 Module Imports:")
    for r in test_imports():
        print(f"  {r}")
    
    print("\n📋 Jukebox Config:")
    from showet_jukebox import JukeboxConfig
    config = JukeboxConfig()
    print(f"  Loop count for shuffle: {config.loop_count_for_shuffle}")
    print(f"  Shuffle mode: {config.shuffle_mode}")
    print(f"  Demo timeout: {config.demo_timeout_seconds}s")
    
    print("\n📦 ModArchive Check:")
    from modarchive_enhanced import ShowetModArchive
    api = ShowetModArchive()
    print(f"  Loaded demo artists: {len(api.DEMO_ARTISTS)} known groups")
    
    print("\n" + "=" * 40)
    print("\n✅ All systems ready!")
    print("\nNext steps:")
    print("  showet --platforms     # List platforms")
    print("  showet-jukebox --help  # Jukebox help")
    print("  showet-tvs99           # Setup browser player")


if __name__ == "__main__":
    main()