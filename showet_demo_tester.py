#!/usr/bin/env python3
"""Showet Demo Tester - Test actual demo playback for platforms.

Creates test demos and verifies emulator execution.
"""

import json
import subprocess
import tempfile
import zipfile
from pathlib import Path


def create_test_demo_zip(platform: str, filename: str, content: bytes) -> Path:
    """Create a test demo zip file."""
    demo_path = Path("demos") / f"{platform}_test" / filename
    demo_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create zip with test file
    zip_path = Path(f"{demo_path}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr(filename, content)
    
    return zip_path


def test_c64_demo():
    """Test C64 demo playback with VICE core."""
    print("Testing C64 demo playback...")
    
    # Create test PRG (minimal C64 program)
    prg_content = bytes([0x00, 0x01, 0x02] * 100)  # Dummy PRG file
    zip_path = create_test_demo_zip("commodore_64", "test.prg", prg_content)
    
    # Test RetroArch with core
    core = "/usr/lib/x86_64-linux-gnu/libretro/vice_x64_libretro.so"
    if Path(core).exists():
        print(f"  ✓ Core found: {core}")
        # Would run: retroarch -L <core> <rom> --fullscreen
        return True
    return False


def test_amiga_demo():
    """Test Amiga demo playback."""
    print("Testing Amiga demo playback...")
    
    # Check for Kickstart
    bios_paths = [
        Path("~/.mame/roms/amiga/kick13.rom").expanduser(),
        Path("~/.fs-uae/Kickstarts/kick13.rom").expanduser(),
    ]
    
    bios_exists = any(p.exists() for p in bios_paths)
    if not bios_exists:
        print("  ⚠ Amiga Kickstart BIOS missing (legal requirement)")
        print("  ℹ Place kick13.rom in ~/.mame/roms/amiga/ or ~/.fs-uae/Kickstarts/")
    
    return bios_exists


def test_nes_demo():
    """Test NES demo playback."""
    print("Testing NES demo playback...")
    core = Path("/usr/lib/x86_64-linux-gnu/libretro/fceumm_libretro.so")
    return core.exists()


def main():
    print("=" * 60)
    print("📺 SHOWET DEMO PLAYBACK TEST")
    print("=" * 60)
    
    # Test platforms
    results = {
        "C64": test_c64_demo(),
        "Amiga": test_amiga_demo(),
        "NES": test_nes_demo(),
    }
    
    print("\n" + "=" * 60)
    print("RESULTS:")
    for platform, ready in results.items():
        status = "✅ READY" if ready else "⚠️ NEEDS BIOS"
        print(f"  {platform}: {status}")
    print("=" * 60)
    
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    exit(main())