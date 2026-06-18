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
        "jukebox_loops": 3,
    },
    "commodore_amiga": {
        "emulators": ["fs-uae", "retroarch"],
        "retroarch_core": "puae",
        "native_runner": "fs-uae",
        "extensions": [".adf", ".hdf"],
        "bios_required": ["kick13.rom", "kick31.rom"],
        "autostart": {
            "disk": "WHDLoad",  # Use WHDLoad for demos
            "hdf": "Boot from HDF",
        },
        "crt_shader": "crt/crt-royale",
        "jukebox_loops": 3,
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
        "autostart": {
            "executable": "Auto-run from mounted C:",
        },
        "crt_shader": "crt/crt-easymode",
        "jukebox_loops": 1,
    },
    "nintendo_famicom": {
        "emulators": ["fceux", "retroarch"],
        "retroarch_core": "quicknes",
        "native_runner": "fceux",
        "extensions": [".nes", ".fds"],
        "crt_shader": "crt/crt-easymode",
        "jukebox_loops": 2,  # NES intros often loop
    },
    "nintendo_superfamicom": {
        "emulators": ["snes9x", "retroarch"],
        "retroarch_core": "snes9x",
        "native_runner": "snes9x",
        "extensions": [".smc", ".sfc"],
        "crt_shader": "crt/crt-easymode",
        "jukebox_loops": 3,
    },
    "sega_megadrive": {
        "emulators": ["retroarch"],
        "retroarch_core": "genesis_plus_gx",
        "native_runner": None,
        "extensions": [".md", ".bin", ".smd"],
        "crt_shader": "crt/crt-easymode",
        "jukebox_loops": 2,
    },
    "sony_psx": {
        "emulators": ["pcsxr", "retroarch"],
        "retroarch_core": "pcsx_rearmed",
        "native_runner": "pcsxr",
        "extensions": [".bin", ".cue", ".iso"],
        "bios_required": ["scph1001.bin"],
        "crt_shader": "crt/crt-royale",
        "jukebox_loops": 1,
    },
    "zx_spectrum": {
        "emulators": ["fuse", "retroarch"],
        "retroarch_core": "fuse",
        "native_runner": "fuse",
        "extensions": [".tap", ".tzx", ".z80"],
        "crt_shader": "crt/crt-pi",
        "jukebox_loops": 3,
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


def get_autostart_commands(platform: str, demo_path: Path) -> list[str]:
    """Get autostart commands for a platform-specific demo.
    
    Args:
        platform: Platform slug
        demo_path: Path to demo file
        
    Returns:
        List of autostart commands (platform-specific)
    """
    if platform not in PLATFORM_PROFILES:
        return []
    
    profile = PLATFORM_PROFILES[platform]
    ext = demo_path.suffix.lower()
    
    # Check for platform-specific autostart
    if "autostart" in profile:
        for key, cmd in profile["autostart"].items():
            if key in ext or key == "executable":
                return [cmd] if isinstance(cmd, str) else cmd
    
    return []


def get_jukebox_loop_count(platform: str, is_looping: bool = False) -> int:
    """Get default loop count for platform in jukebox mode.
    
    Args:
        platform: Platform slug
        is_looping: Whether the demo itself loops
        
    Returns:
        Number of times to play in jukebox
    """
    if platform in PLATFORM_PROFILES:
        base_loops = PLATFORM_PROFILES[platform].get("jukebox_loops", 1)
        if is_looping:
            # Looped demos get platform's default + 2
            return base_loops + 2
        return 1
    return 1


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