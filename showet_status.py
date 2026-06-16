#!/usr/bin/env python3
"""Showet Status Dashboard - overview of the demo-runner.

Shows current status, available features, and quick actions.
"""

import subprocess
from pathlib import Path

def check_ffmpeg() -> bool:
    """Check if ffmpeg is available for streaming."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def check_retroarch() -> bool:
    """Check if retroarch is available."""
    try:
        subprocess.run(["retroarch", "--version"], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def check_stream_keys() -> dict:
    """Check for saved stream keys."""
    keys_dir = Path.home() / ".showet"
    keys = {}
    if keys_dir.exists():
        for f in keys_dir.glob("*_stream_key"):
            platform = f.stem.replace("_stream_key", "")
            keys[platform] = True
    return keys

def main():
    print("═" * 50)
    print("📺 SHOWET STATUS DASHBOARD")
    print("═" * 50)
    
    print(f"\n🔧 Dependencies:")
    print(f"   FFmpeg: {'✅ Available' if check_ffmpeg() else '❌ Not found (install for streaming)'}")
    print(f"   RetroArch: {'✅ Available' if check_retroarch() else '❌ Not found'}")
    
    keys = check_stream_keys()
    if keys:
        print(f"\n🔑 Saved Stream Keys:")
        for platform in keys:
            print(f"   - {platform}")
    else:
        print(f"\n🔑 No stream keys saved (use: showet-stream --save-key twitch --key YOUR_KEY)")
    
    print(f"\n🚀 Quick Commands:")
    print(f"   - Run demo: showet 12345")
    print(f"   - Stream demo: showet-stream --platform twitch --demo 12345")
    print(f"   - Search demos: showet-launcher --search commodore")
    print(f"   - View CRT presets: showet-launcher --list-presets")
    print(f"   - Demo info: demo-viewer --demo-id 12345")
    
    print(f"\n💾 Cache Location: ~/.cache/showet/")
    cache_dir = Path.home() / ".cache" / "showet"
    if cache_dir.exists():
        demo_count = len([d for d in cache_dir.iterdir() if d.is_dir() and d.name.isdigit()])
        print(f"   Cached demos: {demo_count}")
    
    print(f"\n🌐 nostalgist Integration:")
    nostalgist_dir = Path(__file__).parent / "nostalgist_configs"
    if nostalgist_dir.exists():
        config_count = len(list(nostalgist_dir.glob("*.json")))
        print(f"   Platform configs: {config_count}")
    
    print("\n" + "═" * 50)

if __name__ == "__main__":
    main()