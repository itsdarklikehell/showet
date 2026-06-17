#!/usr/bin/env python3
"""Showet Dependency Installer - Auto-install emulators and BIOS files."""

import sys
import subprocess
import shutil
from pathlib import Path

# Platform requirements: (emulator_packages, bios_files, bios_sources)
PLATFORM_DEPS = {
    'commodore_64': {
        'emulators': ['vice'],
        'packages': {
            'ubuntu': ['vice', 'x64sc'],
            'debian': ['vice'],
            'arch': ['vice'],
            'macos': ['vice'],
        },
        'bios': ['vicerc', 'kernal', 'basic', 'chargen'],
        'bios_url': 'https://vice-emu.sourceforge.io/vice.html',  # VICE includes ROMs
    },
    'commodore_amiga': {
        'emulators': ['fs-uae'],
        'packages': {
            'ubuntu': ['fs-uae'],
            'debian': ['fs-uae'],
            'arch': ['fs-uae'],
            'macos': ['fs-uae'],
        },
        'bios': ['kick13.rom', 'kick31.rom'],
        'bios_url': 'https://www.amigaforever.com/',  # Commercial Kickstart
    },
    'dos': {
        'emulators': ['dosbox-x'],
        'packages': {
            'ubuntu': ['dosbox-x'],
            'debian': ['dosbox-x'],
            'arch': ['dosbox-x'],
            'macos': ['dosbox-x'],
        },
        'bios': [],  # FreeDOS based
    },
    'nintendo_famicom': {
        'emulators': ['fceux'],
        'packages': {
            'ubuntu': ['fceux'],
            'debian': ['fceux'],
            'arch': ['fceux'],
            'macos': ['fceux'],
        },
        'bios': [],  # Open source
    },
    'atari_st': {
        'emulators': ['hatari'],
        'packages': {
            'ubuntu': ['hatari'],
            'debian': ['hatari'],
            'arch': ['hatari'],
            'macos': ['hatari'],
        },
        'bios': ['tos.img', 'st-rom.bin'],
        'bios_url': 'https://atari.8bitchip.com/roms.php',  # TOS ROMs
    },
    'sega_megadrive': {
        'emulators': ['retroarch'],
        'packages': {
            'ubuntu': ['retroarch', 'libretro'],
            'debian': ['retroarch'],
            'arch': ['retroarch'],
            'macos': ['retroarch'],
        },
        'bios': [],  # Genesis has no BIOS needed
    },
}


def get_distro():
    """Detect Linux distribution."""
    if Path('/etc/os-release').exists():
        with open('/etc/os-release') as f:
            content = f.read().lower()
            if 'ubuntu' in content or 'debian' in content:
                return 'ubuntu' if 'ubuntu' in content else 'debian'
            if 'arch' in content:
                return 'arch'
    if shutil.which('brew'):
        return 'macos'
    if shutil.which('apt'):
        return 'ubuntu'
    return 'unknown'


def install_packages(packages, distro):
    """Install packages using native package manager."""
    if distro == 'ubuntu' or distro == 'debian':
        cmd = ['sudo', 'apt', 'install', '-y'] + packages
    elif distro == 'arch':
        cmd = ['sudo', 'pacman', '-S', '--noconfirm'] + packages
    elif distro == 'macos':
        cmd = ['brew', 'install'] + packages
    else:
        print(f"Unsupported distribution: {distro}")
        return False
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def install_emulators(platform=None):
    """Install required emulators for platform(s)."""
    distro = get_distro()
    packages_to_install = []
    
    targets = [platform] if platform else PLATFORM_DEPS.keys()
    
    for plat in targets:
        if plat in PLATFORM_DEPS:
            pkgs = PLATFORM_DEPS[plat]['packages'].get(distro, [])
            packages_to_install.extend(pkgs)
    
    packages_to_install = list(set(packages_to_install))
    
    if packages_to_install:
        print(f"Installing: {', '.join(packages_to_install)}")
        if install_packages(packages_to_install, distro):
            print("✅ Emulators installed successfully")
            return True
    return False


def check_bios(platform=None):
    """Check for required BIOS files and provide info for missing ones."""
    missing_bios = {}
    
    targets = [platform] if platform else PLATFORM_DEPS.keys()
    
    for plat in targets:
        if plat in PLATFORM_DEPS:
            for bios in PLATFORM_DEPS[plat]['bios']:
                # Check common BIOS locations
                bios_paths = [
                    Path.home() / f".{plat}" / bios,
                    Path.home() / f".showet/bios/{plat}" / bios,
                    Path(f"/usr/share/{plat}") / bios,
                ]
                
                if not any(p.exists() for p in bios_paths):
                    missing_bios[plat] = PLATFORM_DEPS[plat]
    
    return missing_bios


def print_bios_instructions(missing_bios):
    """Print instructions for obtaining BIOS files (respecting copyright)."""
    for plat, info in missing_bios.items():
        print(f"\n⚠️  {plat.upper()} BIOS files required:")
        for bios in info['bios']:
            print(f"  - {bios}")
        if 'bios_url' in info:
            print(f"  Source: {info['bios_url']}")
        print("  Note: These are commercial files - you must obtain them legally")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: showet-installer [install|check|bios] [--platform <platform>]")
        print("\nCommands:")
        print("  install          Install missing emulators")
        print("  check            Check for installed emulators and BIOS")
        print("  bios             Show BIOS file requirements")
        print("\nPlatforms:", ' '.join(PLATFORM_DEPS.keys()))
        sys.exit(1)
    
    command = sys.argv[1]
    platform = None
    
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--platform' and i < len(sys.argv):
            platform = sys.argv[i + 1]
    
    if command == 'install':
        install_emulators(platform)
    
    elif command == 'check':
        missing = check_bios(platform)
        if missing:
            print_bios_instructions(missing)
        else:
            print("✅ All dependencies satisfied!")
    
    elif command == 'bios':
        print_bios_instructions(check_bios(platform))


if __name__ == '__main__':
    main()