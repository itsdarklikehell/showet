#!/usr/bin/env python3
"""Showet Setup Wizard - Interactive first-time configuration.

Guides users through setting up emulators, RetroArch cores, and dependencies
for all supported platforms.
"""

import subprocess
import sys
from pathlib import Path

try:
    import inquirer
except ImportError:
    print("inquirer required: pip install inquirer")
    sys.exit(1)

# Platform categories with their dependencies
PLATFORM_CATEGORIES = {
    "Commodore 64": {
        "package": "vice",
        "cores": ["vice_x64sc_libretro"],
        "extensions": [".d64", ".t64", ".prg", ".crt", ".tap"],
    },
    "Commodore Amiga": {
        "package": "fs-uae",
        "cores": ["puae_libretro"],
        "extensions": [".adf", ".hdf", ".ipf"],
        "bios": ["kick13.rom", "kick31.rom"],
    },
    "MS-DOS": {
        "package": "dosbox-x",
        "cores": ["dosbox_core_libretro"],
        "extensions": [".exe", ".com", ".bat"],
    },
    "NES/Famicom": {
        "package": "fceux",
        "cores": ["quicknes_libretro", "fceumm_libretro"],
        "extensions": [".nes", ".fds"],
    },
    "SNES/Super Famicom": {
        "package": "snes9x",
        "cores": ["snes9x_libretro"],
        "extensions": [".smc", ".sfc", ".fig"],
    },
    "Sega Mega Drive": {
        "package": "gens",
        "cores": ["genesis_plus_gx_libretro"],
        "extensions": [".md", ".bin", ".gen"],
    },
    "ZX Spectrum": {
        "package": "fuse",
        "cores": ["fuse_libretro"],
        "extensions": [".tap", ".tzx", ".z80"],
    },
    "Windows": {
        "package": "wine",
        "cores": [],
        "extensions": [".exe", ".msi"],
    },
}

RETROARCH_CORE_URLS = {
    "vice_x64sc_libretro": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/vice_x64sc_libretro.so",
    "puae_libretro": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/puae_libretro.so",
    "dosbox_core_libretro": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/dosbox_core_libretro.so",
    "quicknes_libretro": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/quicknes_libretro.so",
    "snes9x_libretro": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/snes9x_libretro.so",
    "genesis_plus_gx_libretro": "https://buildbot.libretro.com/nightly/linux/x86_64/latest/genesis_plus_gx_libretro.so",
}


def check_package_installed(package: str) -> bool:
    """Check if a system package is installed."""
    result = subprocess.run(["which", package], capture_output=True)
    return result.returncode == 0


def check_retroarch_core(core: str) -> bool:
    """Check if a RetroArch core is available."""
    core_paths = [
        Path.home() / ".config" / "retroarch" / "cores" / core,
        Path("/usr/lib/retroarch/cores") / core,
    ]
    return any(p.exists() for p in core_paths)


def download_retroarch_core(core: str) -> bool:
    """Download a RetroArch core."""
    if core not in RETROARCH_CORE_URLS:
        return False

    import urllib.request

    retroarch_dir = Path.home() / ".config" / "retroarch" / "cores"
    retroarch_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"  Downloading {core}...")
        urllib.request.urlretrieve(RETROARCH_CORE_URLS[core], retroarch_dir / core)
        return True
    except Exception as e:
        print(f"  Failed: {e}")
        return False


def install_package(package: str) -> bool:
    """Install a system package."""
    import platform

    system = platform.system().lower()
    if system == "linux":
        distro = ""
        try:
            with open("/etc/os-release") as f:
                content = f.read()
                if "ubuntu" in content or "debian" in content:
                    distro = "debian"
                elif "fedora" in content:
                    distro = "fedora"
                elif "arch" in content:
                    distro = "arch"
        except FileNotFoundError:
            pass

        if distro == "debian":
            cmd = ["sudo", "apt", "install", "-y", package]
        elif distro == "fedora":
            cmd = ["sudo", "dnf", "install", "-y", package]
        elif distro == "arch":
            cmd = ["sudo", "pacman", "-S", "--noconfirm", package]
        else:
            print(f"  Unknown distro, please install {package} manually")
            return False

        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    return False


def main() -> int:
    """Run the setup wizard."""
    print("🚀 Showet Setup Wizard")
    print("=" * 50)

    # Check which platforms to set up
    choices = [
        inquirer.Checkbox(
            "platforms",
            message="Select platforms to configure",
            choices=list(PLATFORM_CATEGORIES.keys()),
            default=["Commodore 64", "Commodore Amiga", "MS-DOS"],
        ),
    ]
    answers = inquirer.prompt(choices)
    if not answers:
        print("Setup cancelled.")
        return 0

    selected = answers["platforms"]
    if not selected:
        print("No platforms selected. Run again to configure.")
        return 0

    print("\n🔧 Checking and installing dependencies...")
    for name in selected:
        info = PLATFORM_CATEGORIES[name]
        package = info["package"]
        cores = info.get("cores", [])

        # Check/install package
        if check_package_installed(package):
            print(f"  ✓ {package} is installed")
        else:
            print(f"  ⚠ {package} not found, installing...")
            install_package(package)

        # Check/install RetroArch cores
        for core in cores:
            if check_retroarch_core(core):
                print(f"  ✓ {core} available")
            else:
                print(f"  ⚠ {core} not found, downloading...")
                download_retroarch_core(core)

        # Check for BIOS files (if needed)
        bios_files = info.get("bios", [])
        if bios_files:
            bios_dir = Path.home() / ".config" / "retroarch" / "system"
            for bios in bios_files:
                if not (bios_dir / bios).exists():
                    print(f"  ⚠ BIOS {bios} missing - download from libretro docs")

    # Create showet directories
    showet_dir = Path.home() / ".showet"
    showet_dir.mkdir(exist_ok=True)
    (showet_dir / "data").mkdir(exist_ok=True)
    (showet_dir / "cache").mkdir(exist_ok=True)
    print(f"\n📁 Showet directories created at {showet_dir}")

    # Create configuration
    config = {
        "platforms": selected,
        "retroarch_path": str(Path.home() / ".config" / "retroarch"),
        "cache_dir": str(showet_dir / "cache"),
    }
    config_file = showet_dir / "config.json"
    config_file.write_text(__import__("json").dumps(config, indent=2))
    print(f"⚙️  Configuration saved to {config_file}")

    print("\n✅ Setup complete! Run 'showet --platforms' to see available platforms.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())