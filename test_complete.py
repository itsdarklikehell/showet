#!/usr/bin/env python3
"""Full system test matrix - shows all systems and their status."""

import json
from pathlib import Path

KNOWN_WORKING_CORES = {
    "stella", "vice_x64sc", "vice_x64", "quicknes", "snes9x", 
    "genesis_plus_gx", "gambatte", "nestopia", "fceumm"
}

MULTI_DISK_SYSTEMS = {
    "commodore_amiga": {"formats": ["adf", "zip", "m3u"], "type": "disk", "note": "puae core missing from CDN"},
    "commodore_64": {"formats": ["t64", "tap"], "type": "tape", "note": "tape side A/B"},
    "nintendo_famicomdisksystem": {"formats": ["fds"], "type": "disk", "note": "FDS floppy"},
    "sega_megadrive": {"formats": ["cue", "bin"], "type": "cd", "note": "CD swapping"},
    "msx": {"formats": ["multiple disks"], "type": "disk"},
}

configs_dir = Path(__file__).parent / "nostalgist_configs"

print("=" * 60)
print("SHOWET COMPLETE SYSTEM TESTING MATRIX")
print("=" * 60)

systems = sorted([f.stem for f in configs_dir.glob("*.json") 
                  if f.suffix == ".json" and f.stem not in ["manifest", "crt_presets"]])

ready = []
blocked = []
testing = []

for slug in systems:
    config_file = configs_dir / f"{slug}.json"
    config = json.loads(config_file.read_text())
    core = config.get("core", "unknown")
    
    multi = MULTI_DISK_SYSTEMS.get(slug)
    
    if core in KNOWN_WORKING_CORES:
        status = "READY"
        ready.append((slug, core, multi))
    elif core == "puae":
        status = "BLOCKED"
        blocked.append((slug, core, multi))
    else:
        status = "TBD"
        testing.append((slug, core, multi))

print(f"\n📋 READY SYSTEMS ({len(ready)}):")
print("-" * 40)
for slug, core, multi in ready:
    note = f" [M: {multi['type']}]" if multi else ""
    print(f"  {slug}: {core}{note}")

print(f"\n🚫 BLOCKED SYSTEMS ({len(blocked)}):")
print("-" * 40)
for slug, core, multi in blocked:
    note = f" - {multi.get('note', '')}" if multi else ""
    print(f"  {slug}: {core}{note}")

print(f"\n❓ TBD SYSTEMS ({len(testing)}):")
print("-" * 40)
for slug, core, multi in testing[:15]:
    note = f" [M: {multi['type']}]" if multi else ""
    print(f"  {slug}: {core}{note}")
print("  ...")

print(f"\nSUMMARY: {len(ready)} ready, {len(blocked)} blocked, {len(testing)} untested")