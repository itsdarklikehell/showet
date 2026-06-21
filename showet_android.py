#!/usr/bin/env python3
"""Showet Android Integration - Mobile demo playback support.

Provides integration with Android emulators (MAME, RetroArch, Dolphin)
and mobile-friendly web UI for touch devices.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


ANDROID_EMULATORS = {
    "dolphin": {
        "name": "Dolphin",
        "platforms": ["gamecube", "wii"],
        "package": "dolphin-emu",
        "flatpak": "org.DolphinEmu.dolphin-emu-nightly",
    },
    "yuzu": {
        "name": "Yuzu",
        "platforms": ["switch"],
        "package": "yuzu",
        "flatpak": "org.yuzu_emu.yuzu",
    },
    "citra": {
        "name": "Citra",
        "platforms": ["3ds"],
        "package": "citra",
        "flatpak": "org.citra_emu.Citra",
    },
    "ppsspp": {
        "name": "PPSSPP",
        "platforms": ["psp"],
        "package": "ppsspp",
        "flatpak": "org.ppsspp.PPSSPP",
    },
}


def detect_android_sdk() -> bool:
    """Check for Android SDK/ADB availability."""
    import shutil
    return bool(shutil.which("adb") or shutil.which("android"))


def get_android_devices() -> list[dict]:
    """Get connected Android devices via ADB."""
    import subprocess
    devices = []
    
    if not detect_android_sdk():
        return devices
    
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            timeout=10
        )
        for line in result.stdout.splitlines()[1:]:
            if "\tdevice" in line:
                serial = line.split("\t")[0]
                devices.append({"serial": serial, "status": "connected"})
    except Exception:
        pass
    
    return devices


def get_emulator_package(emu_name: str) -> Optional[dict]:
    """Get emulator configuration."""
    return ANDROID_EMULATORS.get(emu_name)


def install_android_emulator(emu_name: str, method: str = "flatpak") -> bool:
    """Install Android emulator."""
    import subprocess
    config = get_emulator_package(emu_name)
    
    if not config:
        return False
    
    if method == "flatpak" and config.get("flatpak"):
        try:
            subprocess.run(
                ["flatpak", "install", "-y", config["flatpak"]],
                check=True
            )
            return True
        except Exception:
            pass
    
    return False


def generate_mobile_html(demos: list[dict]) -> str:
    """Generate mobile-friendly HTML for touch devices."""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin: 0; background: #0a0a0a; color: #e0e0e0; font-family: sans-serif; }
        .demo-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; padding: 10px; }
        .demo-card { background: #1a1a1a; border-radius: 8px; padding: 10px; touch-action: manipulation; }
        .demo-card h3 { margin: 0 0 5px 0; font-size: 14px; }
        .demo-card button { width: 100%; padding: 8px; background: #ff6b00; border: none; border-radius: 4px; color: #000; font-weight: bold; }
    </style>
</head>
<body>
    <div class="demo-grid">
"""
    for demo in demos[:20]:
        html += f"""        <div class="demo-card">
            <h3>{demo.get('title', 'Demo')}</h3>
            <button onclick="playDemo('{demo.get('id')}')">▶ Play</button>
        </div>
"""
    html += """    </div>
    <script>
        function playDemo(id) { console.log('Playing demo:', id); }
    </script>
</body>
</html>"""
    return html


def main() -> int:
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Android Integration")
    parser.add_argument("--devices", "-d", action="store_true", help="List Android devices")
    parser.add_argument("--install", "-i", help="Install emulator")
    parser.add_argument("--mobile-html", "-m", help="Generate mobile HTML")
    args = parser.parse_args()

    if args.devices:
        devices = get_android_devices()
        for dev in devices:
            print(f"📱 {dev['serial']} - {dev['status']}")
        if not devices:
            print("No Android devices connected")
            
    elif args.install:
        success = install_android_emulator(args.install)
        print(f"{'✅' if success else '❌'} Installed {args.install}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())