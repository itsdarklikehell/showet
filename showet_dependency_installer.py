#!/usr/bin/env python3
"""Showet Dependency Installer - Check and install missing emulators.

Verifies RetroArch cores, native emulators, and BIOS files.
Can install missing packages automatically or report what's needed.
Supports Linux (apt/dnf/pacman), macOS (brew), and Steam Deck.
"""

import argparse
import json
import platform
import shutil
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

# Steam Deck specific package mappings
STEAM_DECK_PACKAGES = {
    "vice": "games-vice",
    "fs-uae": "fs-uae",
    "dosbox-x": "dosbox-x",
    "retroarch": "games-retroarch",
}

# Linux package managers
PACKAGE_MANAGER_COMMANDS = {
    "apt": ["apt-get", "install", "-y"],
    "dnf": ["dnf", "install", "-y"],
    "pacman": ["pacman", "-S", "--noconfirm"],
    "brew": ["brew", "install"],
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


def detect_platform() -> str:
    """Detect the current operating system."""
    system = platform.system().lower()
    
    # Check for Steam Deck
    if Path("/etc/os-release").exists():
        with open("/etc/os-release") as f:
            content = f.read()
            if "steam" in content.lower() or "deck" in content.lower():
                return "steamdeck"
    
    if system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    return "unknown"


def detect_package_manager() -> str:
    """Detect the available package manager."""
    for pm in ["apt", "dnf", "pacman", "brew"]:
        if shutil.which(pm):
            return pm
    return "unknown"


def install_packages_linux(packages: list[str], package_manager: str) -> int:
    """Install packages using Linux package manager."""
    if package_manager == "unknown":
        print("❌ No supported package manager found")
        return 0
    
    cmd_args = PACKAGE_MANAGER_COMMANDS[package_manager]
    if package_manager == "brew":
        cmd = cmd_args + packages
    else:
        cmd = cmd_args + packages
    
    try:
        subprocess.run(cmd, check=True)
        return len(packages)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return 0


def install_packages_steamdeck(packages: list[str]) -> int:
    """Install packages on Steam Deck using flatpak or system packages."""
    # Steam Deck uses flatpak for most applications
    flatpak_packages = {
        "vice": "com.artsoft.vice",
        "fs-uae": None,  # Not available as flatpak
        "retroarch": "org.libretro.RetroArch",
    }
    
    installed = 0
    for pkg in packages:
        steam_pkg = STEAM_DECK_PACKAGES.get(pkg)
        if steam_pkg and shutil.which("flatpak"):
            try:
                subprocess.run(["flatpak", "install", "-y", steam_pkg], check=True)
                installed += 1
            except subprocess.CalledProcessError:
                print(f"⚠️ Could not install {steam_pkg} via flatpak")
        elif shutil.which("pacman"):
            # Steam Deck can also use pacman directly
            try:
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", pkg], check=True)
                installed += 1
            except subprocess.CalledProcessError:
                print(f"⚠️ Could not install {pkg} via pacman")
    return installed


def install_packages_macos(packages: list[str]) -> int:
    """Install packages on macOS using Homebrew."""
    if not shutil.which("brew"):
        print("❌ Homebrew not found")
        return 0
    
    installed = 0
    for pkg in packages:
        try:
            subprocess.run(["brew", "install", pkg], check=True)
            installed += 1
        except subprocess.CalledProcessError:
            print(f"⚠️ Could not install {pkg}")
    return installed


def install_steamdeck_dependencies(platform_filter: str = None) -> int:
    """Install Showet dependencies on Steam Deck with optimized settings."""
    print("🎮 Steam Deck detected - installing optimized dependencies...")
    
    # Essential packages for Steam Deck
    packages = ["vice", "dosbox-x"]
    
    # Install via flatpak/pacman
    installed = install_packages_steamdeck(packages)
    
    # Configure for Steam Deck controller
    config_dir = Path.home() / ".config" / "showet"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    steamdeck_config = {
        "controller_mode": True,
        "deck_optimized": True,
        "joystick_index": 0,
        "fullscreen_default": True,
        "shader": "crt/crt-easymode",
        "deck_buttons": {
            "a": "primary_action",
            "b": "back",
            "x": "menu",
            "y": "filter_toggle",
            "start": "play_pause",
            "select": "settings",
            "l": "seek_backward",
            "r": "seek_forward",
        }
    }
    
    with open(config_dir / "deck_config.json", "w") as f:
        json.dump(steamdeck_config, f, indent=2)
    
    print(f"✅ Installed {installed}/{len(packages)} packages")
    print("✅ Created Steam Deck controller configuration")
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
    parser.add_argument("--steamdeck", action="store_true", help="Optimize for Steam Deck installation")
    parser.add_argument("--detect-os", action="store_true", help="Detect and show OS information")
    args = parser.parse_args()

    # Detect OS if requested
    if args.detect_os:
        detected = detect_platform()
        pm = detect_package_manager()
        print(f"🖥️ Detected platform: {detected}")
        print(f"📦 Package manager: {pm}")
        return 0

    # Steam Deck optimized install
    if args.steamdeck or detect_platform() == "steamdeck":
        return install_steamdeck_dependencies(args.platform)

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

        # Detect package manager
        pm = detect_package_manager()
        if pm == "unknown" and Path("/etc/os-release").exists():
            with open("/etc/os-release") as f:
                if "steam" in f.read().lower():
                    print("🎮 Steam Deck detected!")
                    return install_steamdeck_dependencies(args.platform)

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