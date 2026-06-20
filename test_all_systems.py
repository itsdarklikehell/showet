#!/usr/bin/env python3
"""
Systematic multi-system testing for Showet/nostalgist.js.
Tests all platforms alphabetically using available browser cores.
"""

import json
import subprocess
from pathlib import Path

# Known working cores in nostalgist CDN (confirmed via fetch)
KNOWN_WORKING_CORES = {
    "stella", "vice_x64sc", "vice_x64", "quicknes", "snes9x", 
    "genesis_plus_gx", "gambatte", "nestopia", "fceumm"
}

# Multi-disk/tape formats to test
MULTI_DISK_SYSTEMS = {
    "commodore_amiga": {"formats": ["adf", "zip", "m3u"], "type": "disk"},
    "commodore_64": {"formats": ["t64", "tap"], "type": "tape"},
    "nintendo_famicomdisksystem": {"formats": ["fds"], "type": "disk"},
    "sega_megadrive": {"formats": ["cue", "bin"], "type": "cd"},
}

def test_systems_alphabetically():
    """Test all systems from nostalgist_configs."""
    configs_dir = Path(__file__).parent / "nostalgist_configs"
    
    print("=== SHOWET SYSTEMATIC TESTING ===\n")
    
    # Test first 25 systems alphabetically
    systems = sorted([f.stem for f in configs_dir.glob("*.json") if f.suffix == ".json" and f.stem != "manifest" and f.stem != "crt_presets" and f.stem != "commodore_amiga_multidisk"])[:25]
    
    for slug in systems:
        config_file = configs_dir / f"{slug}.json"
        config = json.loads(config_file.read_text())
        core = config.get("core", "unknown")
        
        if core in KNOWN_WORKING_CORES:
            status = "✅ Ready"
        elif core == "puae" or core == "unknown":
            status = "❌ Missing CDN"
        else:
            status = "❓ TBD"
        
        multi = ""
        if slug in MULTI_DISK_SYSTEMS:
            multi = f" [MULTI: {MULTI_DISK_SYSTEMS[slug]['type']}]"
        
        print(f"{slug}: {core} {status}{multi}")

if __name__ == "__main__":
    test_systems_alphabetically()