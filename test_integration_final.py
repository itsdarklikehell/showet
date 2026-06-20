#!/usr/bin/env python3
"""Showet Integration Test - Verify demo playback pipeline.

Tests the complete flow: platform detection → core selection → execution readiness.
"""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
sys.modules.setdefault('inquirer', __import__('types').SimpleNamespace())
sys.modules.setdefault('patoolib', __import__('types').SimpleNamespace())

from showet_executor import detect_platform, find_core_path, PLATFORM_CORES, PLATFORM_EXTENSIONS


def test_platform_detection():
    """Test platform detection from file extensions."""
    tests = {
        ".d64": "commodore_64",
        ".nes": "nes",
        ".sms": "mastersystem",
        ".sfc": "snes",
        ".exe": "dos",  # DOS takes priority over Windows for demos
        ".adf": "amiga",
        ".gb": "gameboy",
    }
    
    print("Testing platform detection...")
    for ext, expected in tests.items():
        result = detect_platform(Path(f"test{ext}"))
        status = "✅" if result == expected else "❌"
        print(f"  {status} {ext} -> {result} (expected {expected})")


def test_core_availability():
    """Test core availability for key platforms."""
    print("\nTesting core availability...")
    cores = {
        "commodore_64": "vice_x64_libretro.so",
        "nes": "fceumm_libretro.so",
        "snes": "snes9x_libretro.so",
        "mastersystem": "genesis_plus_gx_libretro.so",
        "dos": "dosbox_core_libretro.so",
    }
    
    for platform, core in cores.items():
        path = find_core_path(core)
        status = "✅" if path else "❌"
        print(f"  {status} {platform}/{core}")


def test_nostalgist_configs():
    """Test nostalgist config validity."""
    print("\nTesting nostalgist configs...")
    config_dir = Path("nostalgist_configs")
    
    ready_platforms = []
    for cfg in config_dir.glob("*.json"):
        if cfg.name == "manifest.json":
            continue
        data = json.loads(cfg.read_text())
        has_core = "core" in data
        has_rom = "rom" in data or data.get("core") != "puae"  # puae needs CDN
        status = "✅" if has_core else "❌"
        if has_core:
            ready_platforms.append(cfg.stem)
        print(f"  {status} {cfg.name}")
    
    return ready_platforms


if __name__ == "__main__":
    print("=" * 60)
    print("SHOWET INTEGRATION TEST")
    print("=" * 60)
    
    test_platform_detection()
    test_core_availability()
    ready = test_nostalgist_configs()
    
    print("\n" + "=" * 60)
    print(f"Platforms ready for testing: {len(ready)}")
    print("=" * 60)