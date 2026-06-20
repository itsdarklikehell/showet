#!/usr/bin/env python3
"""Showet local runner - runs demos with available system emulators."""
import subprocess
import sys
import json

def run_amiga_demo(demo_path):
    """Run Amiga demo using FS-UAE."""
    config = f"""[config]
amiga_model = A500

[floppy_drive_0]
floppy_image = {demo_path}

[video]
fullscreen = false
"""
    config_path = "/tmp/showet_amiga.conf"
    with open(config_path, 'w') as f:
        f.write(config)
    
    return f"fs-uae {config_path}"

def main():
    # Load demo index
    with open('demo_cache_index.json') as f:
        demos = json.load(f)
    
    print("Available demos:")
    for d in demos:
        print(f"  - {d['name']} ({d['platform']})")
    
    print("\nTo run Amiga demo locally:")
    print("  DISPLAY=:0 fs-uae /tmp/showet_amiga.conf")
    print("\nOr use the script: ./showet-demo-run.sh ~/.showet/data/12345/Drifters-BlackWhite2A.adf")

if __name__ == '__main__':
    main()