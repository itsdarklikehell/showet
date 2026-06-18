#!/usr/bin/env python3
"""Showet First-Time Setup Wizard - Interactive configuration for new users."""

import os
import sys
import shutil
import subprocess
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "showet"
BIOS_DIR = Path.home() / ".config" / "retroarch" / "system"


def check_command(cmd):
    """Check if a command is available."""
    return shutil.which(cmd) is not None


def detect_retroarch():
    """Detect RetroArch installation."""
    ra_paths = [
        "retroarch",
        "ra-mgba",
        "/usr/bin/retroarch",
        "/opt/retroarch/bin/retroarch",
    ]
    for path in ra_paths:
        if check_command(path) or Path(path).exists():
            return True
    return False


def detect_emulators():
    """Detect available emulators."""
    emulators = {
        "RetroArch": detect_retroarch(),
        "Wine": check_command("wine"),
        "DOSBox": check_command("dosbox") or check_command("dosbox-x"),
        "VICE (C64)": check_command("x64sc") or check_command("vice"),
        "Mednafen": check_command("mednafen"),
        "FS-UAE (Amiga)": check_command("fs-uae"),
    }
    return emulators


def check_bios_files():
    """Check for BIOS files for major platforms."""
    bios_files = {
        "Commodore 64": "kernal.d64",
        "Amiga": "kick34005.A590",
        "Atari ST": "tos.img",
        "NES": "nestest.nes",
        "SNES": "spc700.rom",
        "Megadrive": "md.bin",
        "PlayStation": "scph5500.bin",
    }
    found = {}
    for platform, filename in bios_files.items():
        found[platform] = (BIOS_DIR / filename).exists()
    return found


def install_emulators():
    """Run showet-installer to install missing dependencies."""
    print("\n🔧 Installing emulators...")
    try:
        result = subprocess.run(
            ["showet-installer", "install"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Emulators installed successfully")
            return True
        else:
            print(f"⚠️ Installation issue: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ showet-installer not found - skipping")
        return False


def create_config():
    """Create initial configuration files."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    config = {
        "theme": "crt-easymode",
        "default_shader": "crt-royale",
        "prefer_retroarch": True,
        "cache_dir": str(Path.home() / ".cache" / "showet"),
        "bios_dir": str(BIOS_DIR),
        "download_cores": True,
    }
    
    import json
    config_path = CONFIG_DIR / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created config at {config_path}")
    return True


def download_demo_pack():
    """Offer to download demo highlight packs."""
    print("\n🎮 Demo Highlight Packs")
    packs = [
        ("c64-classics", "Commodore 64 Classics (10 demos)"),
        ("amiga-hall-of-fame", "Amiga Hall of Fame (15 demos)"),
        ("dos-retro", "DOS Retro Collection (8 demos)"),
    ]
    
    for pack_id, description in packs:
        print(f"  - {pack_id}: {description}")
    
    print("\n  (Use 'showet-cache' to download demo packs later)")


def main():
    """Run the setup wizard."""
    print("🚀 Showet Setup Wizard - v2.2")
    print("=" * 40)
    
    # Step 1: Detect emulators
    print("\n📍 Step 1: Checking available emulators...")
    emulators = detect_emulators()
    for name, available in emulators.items():
        status = "✅" if available else "❌"
        print(f"  {status} {name}")
    
    missing = [k for k, v in emulators.items() if not v]
    
    if missing:
        print(f"\n⚠️ Missing: {', '.join(missing)}")
        response = input("Install missing emulators? [y/N]: ").strip().lower()
        if response == "y":
            install_emulators()
    
    # Step 2: Check BIOS
    print("\n📍 Step 2: Checking BIOS files...")
    bios = check_bios_files()
    for platform, found in bios.items():
        status = "✅" if found else "⚠️"
        print(f"  {status} {platform}")
    
    # Step 3: Create config
    print("\n📍 Step 3: Creating configuration...")
    create_config()
    
    # Step 4: Demo packs
    print("\n📍 Step 4: Demo Highlight Packs...")
    download_demo_pack()
    
    # Done!
    print("\n" + "=" * 40)
    print("✨ Showet setup complete!")
    print("\nQuick start:")
    print("  showet-auto 'Second Reality'   # Try a classic demo")
    print("  showet-executor demo.zip       # Run any demo")
    print("  python3 -m http.server 8000    # Launch web showcase")
    print("  open http://localhost:8000/showet-showcase.html")


if __name__ == "__main__":
    main()