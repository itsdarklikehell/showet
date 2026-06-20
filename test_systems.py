#!/usr/bin/env python3
"""
Multi-system demo tester for Showet/nostalgist integration.
Tests available platforms with their working browser cores.
"""

import json
from pathlib import Path

# Systems with working nostalgist.js cores
WORKING_CORES = {
    "nintendo_famicom": {"core": "fceumm", "extensions": [".nes", ".zip"]},
    "nintendo_gameboy": {"core": "gambatte", "extensions": [".gb", ".gbc", ".zip"]},
    "nintendo_superfamicom": {"core": "snes9x", "extensions": [".smc", ".sfc", ".zip"]},
    "sega_megadrive": {"core": "genesis_plus_gx", "extensions": [".md", ".gen", ".zip"]},
    "commodore_64": {"core": "vice_x64sc", "extensions": [".d64", ".t64", ".prg", ".tap"]},
}

# Multi-disk formats to test
MULTI_DISK_FORMATS = {
    "amiga": [".adf", ".zip", ".m3u"],  # Multi-disk ADF, ZIP with disks, M3U playlist
    "c64_tape": [".t64", ".tap"],  # Tape side A/B
    "pc_engine": [".pce", ".zip"],  # Multi-disk CD
    "mega_cd": [".cue", ".bin", ".zip"],  # Multi-disc
    "saturn": [".cue", ".bin", ".zip"],  # Multi-disc
}

def generate_test_matrix():
    """Generate test matrix for all systems."""
    print("=== SHOWET BROWSER TEST MATRIX ===\n")
    
    print("Working nostalgist.js cores:")
    for slug, info in WORKING_CORES.items():
        print(f"  {slug}: {info['core']} → {info['extensions']}")
    
    print("\nMulti-disk formats to test:")
    for system, formats in MULTI_DISK_FORMATS.items():
        print(f"  {system}: {formats}")
    
    print("\nRecommended test order:")
    print("  1. Amiga (multi-disk) - FS-UAE working, nostalgist waiting for puae core")
    print("  2. C64 - vice_x64sc available, download PRG/T64 for testing")
    print("  3. NES - fceumm available, download NES for testing")
    print("  4. SNES - snes9x available, download SMC for testing")
    print("  5. C64 tapes - test side A/B swapping with T64/TAP")

if __name__ == "__main__":
    generate_test_matrix()