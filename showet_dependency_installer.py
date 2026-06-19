#!/usr/bin/env python3
"""Showet Dependency Installer - Check and install missing emulators.

Verifies RetroArch cores, native emulators, and BIOS files.
Can install missing packages automatically or report what's needed.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Platform requirements
PLATFORM_REQUIREMENTS = {
    "commodore_64": {
        "package": "vice",
        "cores": ["vice_x64_libretro"],
        "check_cmd": ["x64sc"],
    },
    "commodore_amiga": {
        "package": "fs-uae",
        "cores": ["puae_libretro"],
        "bios": ["kick13.rom", "kick31.rom"],
        "check_cmd": ["fs-uae"],
    },
    "dos": {
        "package": "dosbox-x",
        "cores": ["dosbox_core_libretro"],
        "check_cmd": ["dosbox-x"],
    },
    "windows": {
        "package": "wine",
        "check_cmd": ["wine", "--version"],
    },
    "nintendo_famicom": {
        "package": "fceux",
        "cores": ["quicknes_libretro"],
        "check_cmd": ["fceux"],
    },
    "nintendo_superfamicom": {
        "package": "snes9x",
        "cores": ["snes9x_libretro"],
        "check_cmd": ["snes9x"],
    },
    "sega_megadrive": {
        "package": "gens",
        "cores": ["genesis_plus_gx_libretro"],
        "check_cmd": ["gens"],
    },
    "zx_spectrum": {
        "package": "fuse",
        "cores": ["fuse_libretro"],
        "check_cmd": ["fuse"],
    },
}

RETROARCH_CORE_URLS = {
    "vice_x64_libretro.so": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/vice_x64_libretro.so",
    "puae_libretro.so": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/puae_libretro.so",
    "dosbox_core_libretro.so": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/dosbox_core_libretro.so",
    "quicknes_libretro.so": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/quicknes_libretro.so",
    "snes9x_libretro.so": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/snes9x_libretro.so",
    "genesis_plus_gx_libretro.so": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/genesis_plus_gx_libretro.so",
}


def check_command_exists(cmd: str) -> bool:
    """Check if a command exists on the system."""
    result = subprocess.run(["which", cmd], capture_output=True)
    return result.returncode == 0


def check_retroarch_core(core_name: str) -> bool:
    """Check if RetroArch core exists."""
    core_path = Path.home() / ".config" / "retroarch" / "cores" / core_name
    if core_path.exists():
        return True
    alt_path = Path("/usr/lib/retroarch/cores") / core_name
    return alt_path.exists()


def check_emulator_installed(platform: str) -> dict:
    """Check if emulator and cores are installed for a platform."""
    req = PLATFORM_REQUIREMENTS.get(platform, {})
    status = {
        "platform": platform,
        "package_installed": False,
        "core_installed": False,
        "bios_missing": [],
        "needs_install": [],
    }

    # Check package
    package = req.get("package")
    if package:
        status["package_installed"] = check_command_exists(package)

    # Check RetroArch cores
    cores = req.get("cores", [])
    for core in cores:
        core_file = f"{core}.so" if not core.endswith(".so") else core
        if not check_retroarch_core(core_file):
            status["needs_install"].append(core_file)
        else:
            status["core_installed"] = True

    # Check BIOS files
    bios_files = req.get("bios", [])
    bios_dir = Path.home() / ".config" / "retroarch" / "system"
    for bios in bios_files:
        if not (bios_dir / bios).exists():
            status["bios_missing"].append(bios)

    return status


def check_all_platforms() -> list[dict]:
    """Check all platform requirements."""
    results = []
    for platform in PLATFORM_REQUIREMENTS:
        results.append(check_emulator_installed(platform))
    return results


def install_retroarch_cores(cores: list[str], download_cores: bool = True) -> int:
    """Install missing RetroArch cores."""
    import urllib.request

    retroarch_dir = Path.home() / ".config" / "retroarch" / "cores"
    retroarch_dir.mkdir(parents=True, exist_ok=True)

    installed = 0
    for core in cores:
        core_file = f"{core}.so" if not core.endswith(".so") else core
        if core_file in RETROARCH_CORE_URLS and download_cores:
            print(f"Downloading {core_file}...")
            try:
                urllib.request.urlretrieve(RETROARCH_CORE_URLS[core_file], retroarch_dir / core_file)
                installed += 1
            except Exception as e:
                print(f"Failed to download {core_file}: {e}")
    return installed


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Install missing Showet dependencies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--check", action="store_true", help="Check what's missing")
    parser.add_argument("--install", action="store_true", help="Install missing packages/cores")
    parser.add_argument("--platform", type=str, help="Check specific platform")
    parser.add_argument("--download-cores", action="store_true", default=True, help="Download RetroArch cores")
    parser.add_argument("--all", action="store_true", help="Check/install all platforms")
    args = parser.parse_args()

    if args.check or args.all:
        platforms = [args.platform] if args.platform else list(PLATFORM_REQUIREMENTS.keys())
        print("🔍 Checking platform requirements...")

        for platform in platforms:
            status = check_emulator_installed(platform)
            pkg_status = "✓" if status["package_installed"] else "⚠"
            print(f"\n{platform}:")
            print(f"  Package: {pkg_status}")
            if status["bios_missing"]:
                print(f"  Missing BIOS: {status['bios_missing']}")
            if status["needs_install"]:
                print(f"  Missing cores: {status['needs_install']}")

    if args.install or args.all:
        print("\n📦 Installing missing dependencies...")

        # Collect all missing cores
        all_cores = []
        for platform in PLATFORM_REQUIREMENTS:
            status = check_emulator_installed(platform)
            all_cores.extend(status["needs_install"])

        # Deduplicate
        all_cores = list(set(all_cores))

        if all_cores:
            print(f"Installing {len(all_cores)} RetroArch cores...")
            install_retroarch_cores(all_cores, args.download_cores)
            print("✅ Done!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())