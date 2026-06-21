"""Universal demo executor for Showet.

Auto-detects platform and runs demos through appropriate emulator.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger("showet.executor")

# Platform detection mappings
PLATFORM_EXTENSIONS = {
    "dos": [".exe", ".com", ".bat", ".iso", ".cue"],
    "windows": [".exe", ".msi", ".bat"],
    "commodore_64": [".d64", ".t64", ".prg", ".tap", ".crt"],
    "commodore_128": [".d64", ".d71", ".d81", ".t64"],
    "amiga": [".adf", ".hdf", ".ipf", ".lha"],
    "nes": [".nes", ".fds"],
    "snes": [".smc", ".sfc", ".fig"],
    "gameboy": [".gb", ".gbc", ".dmg"],
    "gameboycolor": [".gbc", ".gb"],
    "gameboyadvance": [".gba", ".agb"],
    "megadrive": [".md", ".bin", ".gen"],
    "mastersystem": [".sms", ".gg", ".sg", ".bin"],
    "zx_spectrum": [".tap", ".tzx", ".z80"],
    "flash": [".swf"],
    "android": [".apk"],
}

# RetroArch core mappings
PLATFORM_CORES = {
    "commodore_64": "vice_x64sc_libretro.so",
    "commodore_128": "vice_x128_libretro.so",
    "amiga": "puae_libretro.so",
    "dos": "dosbox_core_libretro.so",
    "nes": "quicknes_libretro.so",
    "snes": "snes9x_libretro.so",
    "gameboy": "gambatte_libretro.so",
    "gameboycolor": "gambatte_libretro.so",
    "gameboyadvance": "mgba_libretro.so",
    "megadrive": "genesis_plus_gx_libretro.so",
    "mastersystem": "genesis_plus_gx_libretro.so",
    "zx_spectrum": "fuse_libretro.so",
}


def detect_platform(file_path: Path) -> str:
    """Detect platform from file extension."""
    ext = file_path.suffix.lower()
    
    # Check archive types first
    if ext in [".zip", ".rar", ".7z", ".lha", ".lzh"]:
        return "archive"
    
    for platform, extensions in PLATFORM_EXTENSIONS.items():
        if ext in extensions:
            return platform
    
    return "unknown"


def find_core_path(core_name: str) -> Optional[Path]:
    """Find RetroArch core path."""
    search_paths = [
        Path.home() / ".config" / "retroarch" / "cores" / core_name,
        Path("/usr/lib/retroarch/cores") / core_name,
        Path("/usr/lib/x86_64-linux-gnu/libretro") / core_name,
    ]
    
    for path in search_paths:
        if path.exists():
            return path
    return None


def check_emulator_available(emulator: str) -> bool:
    """Check if an emulator is available."""
    try:
        result = subprocess.run(["which", emulator], capture_output=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False


def execute_demo(
    file_path: str,
    platform: Optional[str] = None,
    fullscreen: bool = False,
) -> int:
    """Execute a demo file with auto-detected or specified platform."""
    from showet.utils.archive_handler import ArchiveHandler
    
    path = Path(file_path)
    
    if not path.exists():
        logger.error("File not found: %s", file_path)
        return -1
    
    detected_platform = platform or detect_platform(path)
    logger.info("Detected platform: %s", detected_platform)
    
    if detected_platform == "archive":
        handler = ArchiveHandler()
        files = handler.extract(str(path))
        if files:
            # Find first executable
            for f in files[:10]:
                if f.suffix.lower() in [".exe", ".d64", ".nes", ".adf"]:
                    return execute_demo(str(f), detect_platform(f), fullscreen)
        return -1
    
    core = PLATFORM_CORES.get(detected_platform)
    if not core:
        logger.error("No core found for platform: %s", detected_platform)
        return -1
    
    core_path = find_core_path(core)
    if not core_path:
        logger.warning("Core %s not found", core)
    
    cmd = ["retroarch", "-L", str(core_path or core), str(path)]
    if fullscreen:
        cmd.insert(1, "--fullscreen")
    
    try:
        result = subprocess.run(cmd)
        return result.returncode
    except Exception as e:
        logger.error("Execution failed: %s", e)
        return -1


def cli_main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Showet Universal Demo Executor")
    parser.add_argument("file", help="Path to demo file")
    parser.add_argument("--platform", "-p", help="Platform override")
    parser.add_argument("--fullscreen", "-f", action="store_true")
    args = parser.parse_args()
    
    return execute_demo(args.file, args.platform, args.fullscreen)


if __name__ == "__main__":
    raise SystemExit(cli_main())