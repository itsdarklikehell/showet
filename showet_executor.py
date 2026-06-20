#!/usr/bin/env python3
"""Showet Universal Demo Executor - Auto-detect and run demos from any source.

This module provides the showet-executor CLI that:
- Auto-detects platform from file extension or archive contents
- Extracts archives (ZIP, RAR, 7z, LHA) automatically
- Runs demos through RetroArch, Wine, or DOSBox-X as appropriate
- Handles native executables and emulator fallback logic
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("showet.executor")

# Platform detection mappings
PLATFORM_EXTENSIONS = {
    # DOS/Windows
    "dos": [".exe", ".com", ".bat", ".iso", ".cue"],
    "windows": [".exe", ".msi", ".bat"],
    # Commodore
    "commodore_64": [".d64", ".t64", ".prg", ".tap", ".crt"],
    "commodore_128": [".d64", ".d71", ".d81", ".t64"],
    "amiga": [".adf", ".hdf", ".ipf", ".lha"],
    # Nintendo
    "nes": [".nes", ".fds"],
    "snes": [".smc", ".sfc", ".fig"],
    # Sega
    "megadrive": [".md", ".bin", ".gen"],
    "mastersystem": [".sms", ".gg", ".sg", ".bin"],
    "gamegear": [".gg", ".sms"],
    # Others
    "zx_spectrum": [".tap", ".tzx", ".z80"],
    "flash": [".swf"],
    "android": [".apk"],
}

# Emulator commands
EMULATOR_COMMANDS = {
    "retroarch": {
        "cmd": ["retroarch"],
        "core_flag": "--libretro",
        "fullscreen_flag": "--fullscreen",
    },
    "wine": {
        "cmd": ["wine"],
        "fullscreen_flag": None,
    },
    "dosbox": {
        "cmd": ["dosbox-x"],
        "fullscreen_flag": "-fullscreen",
    },
    "native": {
        "cmd": None,
        "fullscreen_flag": None,
    },
}

# RetroArch core mappings per platform
PLATFORM_CORES = {
    "commodore_64": "vice_x64sc_libretro.so",
    "commodore_128": "vice_x128_libretro.so",
    "amiga": "puae_libretro.so",
    "dos": "dosbox_core_libretro.so",
    "windows": None,  # Wine, not RetroArch
    "nes": "quicknes_libretro.so",
    "snes": "snes9x_libretro.so",
    "megadrive": "genesis_plus_gx_libretro.so",
    "mastersystem": "genesis_plus_gx_libretro.so",
    "zx_spectrum": "fuse_libretro.so",
    "flash": "ruffle_libretro.so",
}


def detect_platform(file_path: Path) -> str:
    """Detect platform from file extension.
    
    Args:
        file_path: Path to the demo file
        
    Returns:
        Platform slug or "unknown"
    """
    ext = file_path.suffix.lower()
    
    for platform, extensions in PLATFORM_EXTENSIONS.items():
        if ext in extensions:
            # Handle DOS/Windows overlap
            if ext in PLATFORM_EXTENSIONS["dos"] and ext in PLATFORM_EXTENSIONS["windows"]:
                # Prefer checking if it's a DOS-specific file
                return "dos"
            return platform
    
    # Check if it's an archive
    if ext in [".zip", ".rar", ".7z", ".lha", ".lzh"]:
        return "archive"
    
    return "unknown"


def find_core_path(core_name: str) -> Optional[Path]:
    """Find RetroArch core path.
    
    Args:
        core_name: Libretro core filename
        
    Returns:
        Path to core or None if not found
    """
    search_paths = [
        Path.home() / ".config" / "retroarch" / "cores" / core_name,
        Path("/usr/lib/retroarch/cores") / core_name,
        Path("/usr/local/lib/retroarch/cores") / core_name,
        Path("/usr/lib/x86_64-linux-gnu/libretro") / core_name,
        Path("/usr/lib/aarch64-linux-gnu/libretro") / core_name,
    ]
    
    for path in search_paths:
        if path.exists():
            return path
    
    return None


def check_emulator_available(emulator: str) -> bool:
    """Check if an emulator is available on the system.
    
    Args:
        emulator: Emulator name/command
        
    Returns:
        True if available, False otherwise
    """
    cmd = ["which", emulator] if emulator != "retroarch" else ["which", "retroarch"]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False


def extract_archive(archive_path: Path, dest_dir: Path, password: Optional[str] = None) -> bool:
    """Extract archive to destination directory.
    
    Args:
        archive_path: Path to archive file
        dest_dir: Destination directory for extraction
        password: Optional password for encrypted archives
        
    Returns:
        True on success, False on failure
    """
    ext = archive_path.suffix.lower()
    
    try:
        if ext == ".zip":
            cmd = ["unzip", "-o", str(archive_path), "-d", str(dest_dir)]
            if password:
                cmd.extend(["-P", password])
            subprocess.run(cmd, check=True, capture_output=True)
            return True
            
        elif ext == ".rar":
            cmd = ["unrar", "x", "-o+", str(archive_path), f"{dest_dir}/"]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
            
        elif ext == ".7z":
            cmd = ["7z", "x", f"-o{dest_dir}", str(archive_path)]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
            
        elif ext in [".lha", ".lzh"]:
            cmd = ["lha", "x", str(archive_path), str(dest_dir)]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
            
    except subprocess.CalledProcessError as e:
        logger.error("Archive extraction failed: %s", e)
        return False
    
    return False


def find_executable(directory: Path, extensions: list[str]) -> Optional[Path]:
    """Find an executable file in a directory.
    
    Args:
        directory: Directory to search
        extensions: List of valid extensions
        
    Returns:
        Path to executable or None
    """
    for ext in extensions:
        for f in directory.rglob(f"*{ext}"):
            return f
    return None


def run_with_retroarch(rom_path: Path, core_name: str, fullscreen: bool = False) -> int:
    """Run a demo through RetroArch.
    
    Args:
        rom_path: Path to ROM/demo file
        core_name: Libretro core to use
        fullscreen: Whether to start in fullscreen mode
        
    Returns:
        Process exit code
    """
    if not check_emulator_available("retroarch"):
        logger.error("RetroArch not found. Install with: sudo apt install retroarch")
        return -1
    
    core_path = find_core_path(core_name)
    if not core_path:
        logger.warning("Core %s not found, RetroArch may auto-download", core_name)
        core_path = core_name
    
    cmd = ["retroarch", "-L", str(core_path), str(rom_path)]
    
    if fullscreen:
        cmd.insert(1, "--fullscreen")
    
    logger.info("Running: %s", " ".join(cmd))
    
    try:
        result = subprocess.run(cmd, cwd=rom_path.parent if rom_path.is_file() else None)
        return result.returncode
    except Exception as e:
        logger.error("RetroArch execution failed: %s", e)
        return -1


def run_with_wine(rom_path: Path, fullscreen: bool = False) -> int:
    """Run a Windows demo through Wine.
    
    Args:
        rom_path: Path to .exe file
        fullscreen: Ignored for Wine (windowed only)
        
    Returns:
        Process exit code
    """
    if not check_emulator_available("wine"):
        logger.error("Wine not found. Install with: sudo apt install wine")
        return -1
    
    cmd = ["wine", str(rom_path)]
    logger.info("Running with Wine: %s", rom_path.name)
    
    try:
        result = subprocess.run(cmd)
        return result.returncode
    except Exception as e:
        logger.error("Wine execution failed: %s", e)
        return -1


def run_with_dosbox(rom_path: Path, fullscreen: bool = False) -> int:
    """Run a DOS demo through DOSBox-X.
    
    Args:
        rom_path: Path to DOS executable or disk image
        fullscreen: Whether to start in fullscreen mode
        
    Returns:
        Process exit code
    """
    if not check_emulator_available("dosbox-x"):
        # Try regular dosbox as fallback
        if check_emulator_available("dosbox"):
            dosbox_cmd = "dosbox"
        else:
            logger.error("DOSBox not found. Install with: sudo apt install dosbox-x")
            return -1
    else:
        dosbox_cmd = "dosbox-x"
    
    cmd = [dosbox_cmd]
    
    if fullscreen:
        cmd.append("-fullscreen")
    
    # For executables, mount the directory and run
    if rom_path.suffix.lower() == ".exe":
        cmd.extend(["-c", f"mount c {rom_path.parent} --readonly"])
        cmd.extend(["-c", f"c:"])
        cmd.extend(["-c", f"dosbox-x"])
        cmd.extend(["-c", f"{rom_path.name}"])
    else:
        # For disk images, just pass the file
        cmd.append(str(rom_path))
    
    cmd.append("-exit")
    
    logger.info("Running with DOSBox: %s", rom_path.name)
    
    try:
        result = subprocess.run(cmd)
        return result.returncode
    except Exception as e:
        logger.error("DOSBox execution failed: %s", e)
        return -1


def execute_demo(
    file_path: str,
    platform: Optional[str] = None,
    fullscreen: bool = False,
    retroarch_only: bool = False,
    wine_only: bool = False,
    dosbox_only: bool = False,
) -> int:
    """Execute a demo file with auto-detected or specified platform.
    
    Args:
        file_path: Path to demo file or archive
        platform: Optional platform slug override
        fullscreen: Start in fullscreen mode
        retroarch_only: Only use RetroArch
        wine_only: Only use Wine
        dosbox_only: Only use DOSBox
        
    Returns:
        Process exit code
    """
    path = Path(file_path)
    
    if not path.exists():
        logger.error("File not found: %s", file_path)
        return -1
    
    # Handle archives
    if path.suffix.lower() in [".zip", ".rar", ".7z", ".lha", ".lzh"]:
        with tempfile.TemporaryDirectory() as tmpdir:
            if extract_archive(path, Path(tmpdir)):
                # Find executable in extracted contents
                all_platforms = list(PLATFORM_EXTENSIONS.keys())
                for plat_exts in [".exe", ".com", ".d64", ".adf", ".nes", ".smc", ".sfc"]:
                    executable = find_executable(Path(tmpdir), [plat_exts])
                    if executable:
                        path = Path(tmpdir) / executable.name
                        break
            else:
                logger.error("Failed to extract archive")
                return -1
    
    # Detect or use specified platform
    detected_platform = platform or detect_platform(path)
    logger.info("Detected platform: %s", detected_platform)
    
    # Execute based on platform
    if detected_platform == "windows" or detect_platform(path) == "windows":
        if not wine_only:
            if retroarch_only:
                # Try RetroArch first for Windows demos that might work
                core = PLATFORM_CORES.get("windows")
                if core:
                    return run_with_retroarch(path, core, fullscreen)
            return run_with_wine(path, fullscreen)
    
    elif detected_platform == "dos" or detect_platform(path) == "dos":
        if not retroarch_only:
            if dosbox_only:
                return run_with_dosbox(path, fullscreen)
        core = PLATFORM_CORES.get("dos")
        if core:
            return run_with_retroarch(path, core, fullscreen)
    
    else:
        # RetroArch-based platforms
        core = PLATFORM_CORES.get(detected_platform)
        if core:
            return run_with_retroarch(path, core, fullscreen)
        elif detected_platform == "unknown":
            logger.error("Unknown platform, cannot determine how to run")
            return -1
    
    return 0


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Showet Universal Demo Executor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("file", help="Path to demo file or archive")
    parser.add_argument("--platform", "-p", help="Platform override (dos, windows, c64, amiga, etc.)")
    parser.add_argument("--fullscreen", "-f", action="store_true", help="Start in fullscreen")
    parser.add_argument("--retroarch-only", action="store_true", help="Only use RetroArch")
    parser.add_argument("--wine-only", action="store_true", help="Only use Wine")
    parser.add_argument("--dosbox-only", action="store_true", help="Only use DOSBox")
    args = parser.parse_args()

    return execute_demo(
        file_path=args.file,
        platform=args.platform,
        fullscreen=args.fullscreen,
        retroarch_only=args.retroarch_only,
        wine_only=args.wine_only,
        dosbox_only=args.dosbox_only,
    )


if __name__ == "__main__":
    raise SystemExit(main())