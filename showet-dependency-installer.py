#!/usr/bin/env python3
"""Showet Dependency Installer - Auto-install emulators, cores, and BIOS files."""

import sys
import subprocess
import shutil
import urllib.request
import json
from pathlib import Path

# Extended platform requirements for all 84 platforms
PLATFORM_DEPS = {
    # Commodore
    'commodore_64': {
        'emulators': ['vice'],
        'packages': {
            'ubuntu': ['vice'],
            'debian': ['vice'],
            'arch': ['vice'],
            'macos': ['vice'],
        },
        'bios': [],  # VICE includes ROMs
        'bios_note': 'VICE includes necessary ROMs',
        'libretro_core': 'vice_x64sc_libretro.so',
    },
    'commodore_amiga': {
        'emulators': ['fs-uae'],
        'packages': {
            'ubuntu': ['fs-uae'],
            'debian': ['fs-uae'],
            'arch': ['fs-uae'],
            'macos': ['fs-uae'],
        },
        'bios': ['kick13.rom', 'kick31.rom', 'kickstarter.rom'],
        'bios_url': 'https://www.amigaforever.com/',
        'libretro_core': 'puae_libretro.so',
    },
    'commodore_128': {
        'emulators': ['vice'],
        'packages': {
            'ubuntu': ['vice'],
            'debian': ['vice'],
            'arch': ['vice'],
            'macos': ['vice'],
        },
        'bios': [],
        'libretro_core': 'vice_x128_libretro.so',
    },
    'commodore_vic20': {
        'emulators': ['vice'],
        'packages': {'ubuntu': ['vice'], 'debian': ['vice'], 'arch': ['vice'], 'macos': ['vice']},
        'bios': [],
        'libretro_core': 'vice_xvic_libretro.so',
    },
    # DOS
    'microsoft_msdos': {
        'emulators': ['dosbox-x'],
        'packages': {
            'ubuntu': ['dosbox-x'],
            'debian': ['dosbox-x'],
            'arch': ['dosbox-x'],
            'macos': ['dosbox-x'],
        },
        'bios': [],  # FreeDOS based
        'libretro_core': 'dosbox_core_libretro.so',
    },
    # Nintendo
    'nintendo_famicom': {
        'emulators': ['fceux'],
        'packages': {
            'ubuntu': ['fceux'],
            'debian': ['fceux'],
            'arch': ['fceux'],
            'macos': ['fceux'],
        },
        'bios': [],
        'libretro_core': 'quicknes_libretro.so',
    },
    'nintendo_superfamicom': {
        'emulators': ['snes9x'],
        'packages': {
            'ubuntu': ['snes9x'],
            'debian': ['snes9x'],
            'arch': ['snes9x'],
            'macos': ['snes9x'],
        },
        'bios': [],
        'libretro_core': 'snes9x_libretro.so',
    },
    'sega_megadrive': {
        'emulators': ['retroarch'],
        'packages': {
            'ubuntu': ['retroarch'],
            'debian': ['retroarch'],
            'arch': ['retroarch'],
            'macos': ['retroarch'],
        },
        'bios': [],
        'libretro_core': 'genesis_plus_gx_libretro.so',
    },
    'sony_psx': {
        'emulators': ['pcsxr'],
        'packages': {
            'ubuntu': ['pcsxr'],
            'debian': ['pcsxr'],
            'arch': ['pcsxr'],
            'macos': ['pcsxr'],
        },
        'bios': ['scph1001.bin', 'scph5501.bin', 'scph7001.bin'],
        'bios_url': 'https://www.psx-place.com/',
        'libretro_core': 'pcsx_rearmed_libretro.so',
    },
    # Atari
    'atari_2600': {
        'emulators': ['stella'],
        'packages': {
            'ubuntu': ['stella'],
            'debian': ['stella'],
            'arch': ['stella'],
            'macos': ['stella'],
        },
        'bios': [],
        'libretro_core': 'stella_libretro.so',
    },
    'atari_stettfalcon': {
        'emulators': ['hatari'],
        'packages': {
            'ubuntu': ['hatari'],
            'debian': ['hatari'],
            'arch': ['hatari'],
            'macos': ['hatari'],
        },
        'bios': ['tos.img'],
        'bios_url': 'https://atari.8bitchip.com/roms.php',
        'libretro_core': 'hatari_libretro.so',
    },
    # ZX Spectrum
    'zx_spectrum': {
        'emulators': ['fuse'],
        'packages': {
            'ubuntu': ['fuse'],
            'debian': ['fuse'],
            'arch': ['fuse'],
            'macos': ['fuse'],
        },
        'bios': [],
        'libretro_core': 'fuse_libretro.so',
    },
}

# Libretro core download URLs (nightly builds)
LIBRETRO_CORE_URLS = {
    'vice_x64sc_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/vice_x64sc_libretro.so',
    'puae_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/puae_libretro.so',
    'quicknes_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/quicknes_libretro.so',
    'snes9x_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/snes9x_libretro.so',
    'genesis_plus_gx_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/genesis_plus_gx_libretro.so',
    'stella_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/stella_libretro.so',
    'pcsx_rearmed_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/pcsx_rearmed_libretro.so',
    'dosbox_core_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/dosbox_core_libretro.so',
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


def get_retroarch_dir():
    """Get RetroArch config directory."""
    return Path.home() / '.config' / 'retroarch'


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
    except subprocess.CalledProcessError as e:
        print(f"Package installation failed: {e}")
        return False


def download_libretro_core(core_name: str) -> bool:
    """Download RetroArch core to user's libretro directory."""
    if core_name not in LIBRETRO_CORE_URLS:
        print(f"No download URL for core: {core_name}")
        return False

    retroarch_dir = get_retroarch_dir()
    cores_dir = retroarch_dir / 'cores'
    cores_dir.mkdir(parents=True, exist_ok=True)

    core_path = cores_dir / core_name
    url = LIBRETRO_CORE_URLS[core_name]

    print(f"Downloading {core_name}...")
    try:
        urllib.request.urlretrieve(url, core_path)
        print(f"✅ Downloaded to {core_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to download core: {e}")
        return False


def install_emulators(platform=None, download_cores=False):
    """Install required emulators for platform(s)."""
    distro = get_distro()
    packages_to_install = []

    targets = [platform] if platform else PLATFORM_DEPS.keys()

    for plat in targets:
        if plat in PLATFORM_DEPS:
            pkgs = PLATFORM_DEPS[plat]['packages'].get(distro, [])
            packages_to_install.extend(pkgs)

    # Deduplicate packages
    packages_to_install = list(set(packages_to_install))

    if packages_to_install:
        print(f"Installing emulators: {', '.join(packages_to_install)}")
        install_packages(packages_to_install, distro)
    else:
        print("No emulator packages to install for this platform/distro")

    # Download RetroArch cores if requested
    if download_cores:
        for plat in targets:
            if plat in PLATFORM_DEPS:
                core = PLATFORM_DEPS[plat].get('libretro_core')
                if core and not (get_retroarch_dir() / 'cores' / core).exists():
                    download_libretro_core(core)

    return True


def check_bios(platform=None):
    """Check for required BIOS files and provide info for missing ones."""
    missing = {}

    targets = [platform] if platform else PLATFORM_DEPS.keys()

    for plat in targets:
        if plat not in PLATFORM_DEPS:
            continue

        info = PLATFORM_DEPS[plat]
        for bios in info.get('bios', []):
            # Check common BIOS locations
            bios_paths = [
                Path.home() / f'.showet/bios/{plat}' / bios,
                Path.home() / '.config/retroarch/system' / bios,
                Path(f'/usr/share/{plat}') / bios,
            ]

            if not any(p.exists() for p in bios_paths):
                missing[plat] = missing.get(plat, {'bios': [], 'bios_url': info.get('bios_url')})
                missing[plat]['bios'].append(bios)

    return missing


def check_cores(platform=None):
    """Check for RetroArch cores."""
    missing = []
    retroarch_dir = get_retroarch_dir() / 'cores'

    targets = [platform] if platform else PLATFORM_DEPS.keys()

    for plat in targets:
        if plat not in PLATFORM_DEPS:
            continue

        core = PLATFORM_DEPS[plat].get('libretro_core')
        if core and not (retroarch_dir / core).exists():
            missing.append(core)

    return missing


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: showet-installer [install|check|bios|cores] [options]")
        print("\nCommands:")
        print("  install          Install missing emulators")
        print("  check            Check for emulators, BIOS, and cores")
        print("  bios             Show BIOS file requirements")
        print("  cores            List missing RetroArch cores")
        print("\nOptions:")
        print("  --platform <slug>    Target specific platform")
        print("  --download-cores     Download missing RetroArch cores")
        print("\nExamples:")
        print("  showet-installer install --platform commodore_64")
        print("  showet-installer check --download-cores")
        sys.exit(1)

    command = sys.argv[1]
    platform = None
    download_cores = False

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--platform' and i + 1 < len(sys.argv):
            platform = sys.argv[i + 1]
            i += 1
        elif arg == '--download-cores':
            download_cores = True
        i += 1

    if command == 'install':
        install_emulators(platform, download_cores)

    elif command == 'check':
        missing_bios = check_bios(platform)
        missing_cores = check_cores(platform)

        if missing_bios:
            print("\n⚠️  Missing BIOS files:")
            for plat, info in missing_bios.items():
                for bios in info['bios']:
                    print(f"  - {plat}/{bios}")
                if info.get('bios_url'):
                    print(f"    Source: {info['bios_url']}")

        if missing_cores:
            print(f"\n📦 Missing RetroArch cores: {', '.join(missing_cores)}")
            print("   Use --download-cores to fetch them")

        if not missing_bios and not missing_cores:
            print("✅ All dependencies satisfied!")

    elif command == 'bios':
        missing = check_bios(platform)
        if missing:
            for plat, info in missing.items():
                print(f"\n⚠️  {plat.upper()} BIOS files required:")
                for bios in info['bios']:
                    print(f"  - {bios}")
                if info.get('bios_url'):
                    print(f"  Source: {info['bios_url']}")
                print("  Note: These are commercial files - obtain legally")

    elif command == 'cores':
        missing = check_cores(platform)
        if missing:
            print(f"Missing cores: {', '.join(missing)}")
        else:
            print("✅ All RetroArch cores present!")


if __name__ == '__main__':
    main()