#!/usr/bin/env python3
"""Showet One-Command Demo Runner - Complete 'demo-to-playback' experience."""

import sys
import subprocess
from pathlib import Path

def download_demo(source, demo_id=None, search=None):
    """Download demo from pouet.net or scene.org."""
    if source == 'pouet' and demo_id:
        cmd = ['showet', '--demo', demo_id, '--download']
    elif source == 'scene-org':
        cmd = ['scene-org', '--search', search or demo_id, '--download']
    else:
        return None
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Parse output to find downloaded file
    for line in result.stdout.split('\n'):
        if 'downloaded' in line.lower() or 'saved' in line.lower():
            # Extract file path from output
            parts = line.split()
            for part in parts:
                if Path(part).exists():
                    return part
    return result.stdout


def install_dependencies(platform):
    """Check and install dependencies for platform."""
    result = subprocess.run(['showet-installer', 'check', '--platform', platform],
                          capture_output=True, text=True)
    
    if 'BIOS' in result.stdout or 'required' in result.stdout:
        print("🔧 Some BIOS files may be required - installing emulators...")
        subprocess.run(['showet-installer', 'install', '--platform', platform])


def extract_and_run(demo_path, platform='auto'):
    """Extract archive if needed and run demo."""
    path = Path(demo_path)
    
    # Check if archive
    if path.suffix.lower() in ['.zip', '.rar', '.7z', '.lha', '.lzh']:
        print(f"📦 Extracting {path.name}...")
        result = subprocess.run(['showet-archive', demo_path, '--extract'],
                            capture_output=True, text=True)
        # Find extracted file
        for line in result.stdout.split('\n'):
            if Path(line.strip()).exists():
                demo_path = line.strip()
                break
    
    # Run demo
    print(f"▶️ Running {demo_path}...")
    subprocess.run(['showet-executor', demo_path, '--prefer-retroarch'])


def run_one_command(demo_ref):
    """
    One-command demo runner.
    
    Args:
        demo_ref: Can be:
            - Pouet ID (numeric)
            - scene.org search term
            - Local file path
    """
    path = Path(demo_ref)
    
    # Local file
    if path.exists():
        print(f"📂 Found local demo: {demo_ref}")
        # Detect platform and run
        subprocess.run(['showet-executor', demo_ref, '--prefer-retroarch'])
        return
    
    # Pouet ID (numeric)
    if demo_ref.isdigit():
        print(f"📥 Downloading from Pouet.net ID: {demo_ref}")
        demo_path = download_demo('pouet', demo_id=demo_ref)
        if demo_path:
            install_dependencies(demo_ref)
            extract_and_run(demo_path)
        return
    
    # Scene.org search or other
    print(f"🔍 Searching scene.org: {demo_ref}")
    demo_path = download_demo('scene-org', search=demo_ref)
    if demo_path:
        extract_and_run(demo_path)


def main():
    if len(sys.argv) < 2:
        print("🚀 Showet One-Command Demo Runner")
        print("\nUsage: showet-auto <demo_ref>")
        print("\nDemo reference can be:")
        print("  - Pouet.net ID (e.g., 12345)")
        print("  - scene.org search term (e.g., 'Second Reality')")
        print("  - Local file path (e.g., /path/to/demo.zip)")
        print("\nExample:")
        print("  showet-auto 12345          # Pouet ID")
        print("  showet-auto 'Second Reality'  # Search")
        print("  showet-auto demo.d64       # Local file")
        sys.exit(1)
    
    demo_ref = sys.argv[1]
    run_one_command(demo_ref)


if __name__ == '__main__':
    main()