#!/usr/bin/env python3
"""
Showet Platform Runner - Enhanced demo execution with autostart support.

This module provides the complete execution pipeline for all supported platforms.
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional

# Platform execution profiles with autostart configurations
PLATFORM_PROFILES = {
    "commodore_64": {
        "emulators": ["vice", "retroarch"],
        "retroarch_core": "vice_x64sc",
        "native_runner": "x64sc",
        "extensions": [".d64", ".t64", ".prg", ".crt", ".tap"],
        "autostart": {
            "disk": "LOAD \"*\",8,1\nRUN",
            "tape": "LOAD\nRUN",
            "prg": None,  # Direct execute
        },
        "crt_shader": "crt/crt-easymode",
    },
    "commodore_amiga": {
        "emulators": ["fs-uae", "retroarch"],
        "retroarch_core": "puae",
        "native_runner": "fs-uae",
        "extensions": [".adf", ".hdf"],
        "bios_required": ["kick13.rom", "kick31.rom"],
        "crt_shader": "crt/crt-royale",
    },
    "microsoft_msdos": {
        "emulators": ["dosbox-x", "retroarch"],
        "retroarch_core": "dosbox_core",
        "native_runner": "dosbox-x",
        "extensions": [".exe", ".com", ".bat"],
        "dosbox_config": {
            "machine": "svga_s3",
            "memsize": 16,
            "cycles": "max",
        },
        "crt_shader": "crt/crt-easymode",
    },
    "nintendo_famicom": {
        "emulators": ["fceux", "retroarch"],
        "retroarch_core": "quicknes",
        "native_runner": "fceux",
        "extensions": [".nes", ".fds"],
        "crt_shader": "crt/crt-easymode",
    },
    "nintendo_superfamicom": {
        "emulators": ["snes9x", "retroarch"],
        "retroarch_core": "snes9x",
        "native_runner": "snes9x",
        "extensions": [".smc", ".sfc"],
        "crt_shader": "crt/crt-easymode",
    },
}


def check_emulator(platform: str) -> Optional[str]:
    """Check for available emulator for platform."""
    if platform not in PLATFORM_PROFILES:
        return None

    profile = PLATFORM_PROFILES[platform]
    
    # Check native emulator first
    for emu in profile.get("native_runner", "").split(","):
        if emu and shutil.which(emu):
            return emu

    # Check RetroArch
    if shutil.which("retroarch"):
        core = profile.get("retroarch_core")
        core_path = Path.home() / ".config/retroarch/cores" / f"{core}.so"
        if core_path.exists():
            return "retroarch"

    return None


def get_retroarch_core_path(core: str) -> Optional[Path]:
    """Get RetroArch core path."""
    paths = [
        Path.home() / ".config/retroarch/cores" / f"{core}.so",
        Path("/usr/lib/retroarch/cores") / f"{core}.so",
        Path("/usr/lib/libretro") / f"{core}.so",
    ]
    for p in paths:
        if p.exists():
            return p
    return None


def launch_demo(demo_path: str, platform: str = "auto") -> Optional[subprocess.Popen]:
    """Launch demo with appropriate emulator."""
    path = Path(demo_path)
    
    # Auto-detect if needed
    if platform == "auto":
        for plat, prof in PLATFORM_PROFILES.items():
            for ext in prof.get("extensions", []):
                if path.suffix.lower() == ext or path.suffix.lower() == ".zip":
                    platform = plat
                    break
            if platform != "auto":
                break

    if platform not in PLATFORM_PROFILES:
        print(f"Unknown platform: {platform}")
        return None

    profile = PLATFORM_PROFILES[platform]
    runner = check_emulator(platform)

    if not runner:
        print(f"No emulator available for {platform}")
        return None

    if runner == "retroarch":
        core = profile.get("retroarch_core")
        core_path = get_retroarch_core_path(core)
        
        cmd = ["retroarch", "-L", str(core_path), str(demo_path)]
        
    elif runner == "dosbox-x" or runner == "dosbox":
        cmd = build_dosbox_cmd(demo_path, profile.get("dosbox_config", {}))
        
    elif runner == "x64sc":
        cmd = ["x64sc", "-autostart", str(demo_path)]
        
    elif runner == "fs-uae":
        cmd = build_fsuae_cmd(demo_path)
        
    else:
        cmd = [runner, str(demo_path)]

    return subprocess.Popen(cmd)


def build_dosbox_cmd(demo_path: str, config: dict) -> list[str]:
    """Build DOSBox command with config."""
    import tempfile
    
    conf = f"[autoexec]\nmount c /tmp\n"
    if demo_path.endswith((".exe", ".com", ".bat")):
        name = Path(demo_path).stem
        conf += f"c:\\\n{name}.exe\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:
        f.write(conf)
        conf_path = f.name
    
    return ["dosbox", "-conf", conf_path, "-noconsole"]


def build_fsuae_cmd(demo_path: str) -> list[str]:
    """Build FS-UAE command."""
    return ["fs-uae", "--floppy-drive-0", demo_path]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: showet-platform-runner <demo_path> [--platform <platform>]")
        sys.exit(1)
    
    platform = "auto"
    if "--platform" in sys.argv:
        idx = sys.argv.index("--platform")
        platform = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "auto"
    
    process = launch_demo(sys.argv[1], platform)
    if process:
        print(f"Demo launched with PID: {process.pid}")
    else:
        print("Failed to launch demo")