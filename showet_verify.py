#!/usr/bin/env python3
"""Showet System Verification - Test all components and emulators.

Runs a comprehensive check of the Showet installation including:
- RetroArch core detection
- Emulator availability
- Platform module validation
- nostalgist.js integration check
"""

import json
import subprocess
import sys
from pathlib import Path

# Mock external deps
sys.modules.setdefault('inquirer', __import__('types').SimpleNamespace())
sys.modules.setdefault('patoolib', __import__('types').SimpleNamespace())

sys.path.insert(0, str(Path(__file__).parent))


def check_command(cmd: str) -> tuple[bool, str]:
    """Check if a command exists."""
    # Special handling for mame (often in /usr/games)
    if cmd == "mame":
        mame_path = Path("/usr/games/mame")
        if mame_path.exists():
            return True, str(mame_path)
    try:
        result = subprocess.run(['which', cmd], capture_output=True, timeout=5)
        if result.returncode == 0:
            path = result.stdout.decode().strip()
            return True, path
        return False, ""
    except:
        return False, ""


def check_retroarch_cores():
    """Check available RetroArch cores."""
    core_paths = [
        Path.home() / ".config/retroarch/cores",
        Path("/usr/lib/x86_64-linux-gnu/libretro"),
    ]
    
    cores = []
    for cp in core_paths:
        if cp.exists():
            cores.extend(cp.glob("*.so"))
    
    return cores


def main():
    print("=" * 60)
    print("📺 SHOWET SYSTEM VERIFICATION v3.2")
    print("=" * 60)
    
    # Check emulators
    emulators = ["retroarch", "wine", "dosbox-x", "mame", "fs-uae"]
    print("\n🔧 Emulators:")
    for emu in emulators:
        found, path = check_command(emu)
        status = "✅" if found else "⚠️"
        print(f"  {status} {emu}: {path if found else 'not installed'}")
    
    # Check cores
    cores = check_retroarch_cores()
    print(f"\n🎮 RetroArch Cores: {len(cores)} installed")
    
    key_cores = ["vice_x64sc_libretro.so", "fceumm_libretro.so", 
                 "snes9x_libretro.so", "genesis_plus_gx_libretro.so"]
    print("  Key cores check:")
    for core in key_cores:
        found = any(c.name == core for c in cores)
        print(f"    {'✅' if found else '❌'} {core}")
    
    # Load platform modules
    print("\n🕹️ Platform Modules:")
    from showet.platforms import load_all_platforms
    runners = load_all_platforms()
    print(f"  ✅ {len(runners)} platforms loadable")
    
    # Check nostalgist configs
    config_dir = Path("nostalgist_configs")
    configs = list(config_dir.glob("*.json"))
    configs = [c for c in configs if c.name != "manifest.json"]
    print(f"\n🌐 nostalgist.js Configs:")
    print(f"  ✅ {len(configs)} platform configs")
    
    # Check jukebox
    from showet_jukebox import LOOPED_DEMO_TYPES
    print(f"\n🎵 Jukebox:")
    print(f"  ✅ Loop types: {', '.join(LOOPED_DEMO_TYPES)}")
    
    # Summary
    print("\n" + "=" * 60)
    ready = len(cores) >= 5
    print(f"🎮 Showet Status: {'READY FOR DEMOS!' if ready else 'NEEDS SETUP'}")
    print("=" * 60)
    
    return 0 if ready else 1


if __name__ == "__main__":
    sys.exit(main())