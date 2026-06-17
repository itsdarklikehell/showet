#!/usr/bin/env python3
"""Showet Universal Demo Executor - Run any demo through native/emulated execution."""

import os
import sys
import shutil
import subprocess
from pathlib import Path

class DemoExecutor:
    """Universal executor for demoscene productions."""
    
    ARCHIVE_HANDLERS = {
        '.zip': ['unzip', '-o'],
        '.rar': ['unrar', 'x'],
        '.7z': ['7z', 'x'],
        '.lha': ['lha', 'x'],
        '.lzh': ['lha', 'x'],
    }
    
    # Libretro core paths (RetroArch integration)
    LIBRETRO_CORES = {
        'commodore_64': 'x64_libretro.so',
        'commodore_amiga': 'puae_libretro.so',
        'dos': 'dosbox_libretro.so',
        'nintendo_famicom': 'nes_libretro.so',
        'nintendo_superfamicom': 'snes9x_libretro.so',
        'sega_megadrive': 'genesis_plus_gx_libretro.so',
        'atari_2600': 'stella_libretro.so',
        'sony_psx': 'mednafen_psx_libretro.so',
    }
    
    LIBRETRO_CORE_URLS = {
        'x64_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/x64_libretro.so',
        'nes_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/nes_libretro.so',
        'snes9x_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/snes9x_libretro.so',
        'genesis_plus_gx_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/genesis_plus_gx_libretro.so',
        'dosbox_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/dosbox_libretro.so',
        'puae_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/puae_libretro.so',
        'stella_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/stella_libretro.so',
    }
    
    PLATFORM_RUNNERS = {
        # Priority: RetroArch > Native emulator > Wine/DOSBox
        'windows': {
            'runner': 'wine',
            'retroarch_core': None,
            'extensions': ['.exe', '.bat', '.com'],
        },
        'dos': {
            'runner': 'dosbox',
            'retroarch_core': 'dosbox_libretro.so',
            'extensions': ['.exe', '.com', '.bat'],
        },
        'linux': {
            'runner': None,  # Direct execution
            'retroarch_core': None,
            'extensions': ['.x86', '.x86_64', ''],
        },
        'amiga': {
            'runner': 'fs-uae',
            'retroarch_core': 'puae_libretro.so',
            'extensions': ['.adf', '.hdf', ''],
        },
        'c64': {
            'runner': 'x64sc',
            'retroarch_core': 'x64_libretro.so',
            'extensions': ['.d64', '.t64', '.prg'],
        },
        'zx_spectrum': {
            'runner': 'fuse',
            'retroarch_core': None,
            'extensions': ['.tap', '.tzx', '.z80'],
        },
        'commodore_amiga': {
            'runner': 'fs-uae',
            'retroarch_core': 'puae_libretro.so',
            'extensions': ['.adf', '.hdf', ''],
        },
        'commodore_64': {
            'runner': 'x64sc',
            'retroarch_core': 'x64_libretro.so',
            'extensions': ['.d64', '.t64', '.prg', '.crt'],
        },
        'nintendo_famicom': {
            'runner': 'fceux',
            'retroarch_core': 'nes_libretro.so',
            'extensions': ['.nes', '.fds'],
        },
        'nintendo_superfamicom': {
            'runner': 'snes9x',
            'retroarch_core': 'snes9x_libretro.so',
            'extensions': ['.smc', '.sfc'],
        },
        'sega_megadrive': {
            'runner': 'gens',
            'retroarch_core': 'genesis_plus_gx_libretro.so',
            'extensions': ['.md', '.bin', '.gen'],
        },
    }
    
    def __init__(self, platform='auto', timeout=300, prefer_retroarch=False, download_cores=False):
        self.platform = platform
        self.timeout = timeout
        self.prefer_retroarch = prefer_retroarch
        self.download_cores = download_cores
    
    def detect_platform(self, demo_path):
        """Auto-detect platform from demo filename/path or executable type."""
        path = Path(demo_path)
        name = path.name.lower()
        
        if 'amiga' in name or path.suffix in ['.adf', '.hdf']:
            return 'amiga'
        if 'c64' in name or 'commodore' in name or path.suffix in ['.d64', '.t64', '.prg']:
            return 'commodore_64'
        if 'dos' in name or path.suffix in ['.exe', '.com', '.bat']:
            return 'dos'
        if '.nes' in name or 'famicom' in name:
            return 'nintendo_famicom'
        if '.smc' in name or '.sfc' in name or 'snes' in name:
            return 'nintendo_superfamicom'
        if path.suffix in ['.zip', '.rar', '.7z', '.lha']:
            # Check internal filenames
            extracted = self.extract_archive(demo_path)
            if extracted:
                return self.detect_platform(extracted[0])
        
        return 'auto'
    
    def extract_archive(self, archive_path):
        """Extract demo archive and return list of executables."""
        archive = Path(archive_path)
        ext = archive.suffix.lower()
        
        if ext not in self.ARCHIVE_HANDLERS:
            return None
        
        extract_dir = Path(f"/tmp/showet_demo_{archive.stem}")
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = self.ARCHIVE_HANDLERS[ext] + ['-o' if ext != '.zip' else '-o', str(archive), str(extract_dir)]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            # Find executables
            files = list(extract_dir.rglob('*'))
            return [f for f in files if f.suffix in ['.exe', '.com', '.adf', '.nes', '.smc']]
        except subprocess.CalledProcessError:
            return None
    
    def find_runner(self, demo_path):
        """Find appropriate runner for demo, prioritizing RetroArch cores."""
        # Check RetroArch first - best compatibility
        if shutil.which('retroarch'):
            for plat, config in self.PLATFORM_RUNNERS.items():
                if config.get('retroarch_core'):
                    core = config['retroarch_core']
                    core_path = self._get_core_path(core)
                    if core_path or self._download_core(core):
                        return 'retroarch'
        
        # Check platform-specific native emulators
        for plat, config in self.PLATFORM_RUNNERS.items():
            if shutil.which(config['runner']):
                runner = config['runner']
                break
        
        # Check Wine for Windows demos
        if demo_path.lower().endswith(('.exe', '.bat', '.com')) and shutil.which('wine'):
            return 'wine'
        
        return runner
    
    def _get_core_path(self, core_name):
        """Get RetroArch core path."""
        retroarch_dir = Path.home() / '.config/retroarch/cores'
        core_path = retroarch_dir / core_name
        return core_path.exists() and str(core_path) or None
    
    def _download_core(self, core_name):
        """Download libretro core if missing."""
        import urllib.request
        
        retroarch_dir = Path.home() / '.config/retroarch/cores'
        retroarch_dir.mkdir(parents=True, exist_ok=True)
        
        if core_name not in self.LIBRETRO_CORE_URLS:
            return False
        
        url = self.LIBRETRO_CORE_URLS[core_name]
        core_path = retroarch_dir / core_name
        
        print(f"Downloading {core_name}...")
        try:
            urllib.request.urlretrieve(url, core_path)
            return True
        except Exception as e:
            print(f"Failed to download core: {e}")
            return False
    
    def run_demo(self, demo_path, platform=None):
        """Execute a demo with auto-detection."""
        if platform is None:
            platform = self.detect_platform(demo_path)
        
        runner = self.find_runner(demo_path)
        
        if runner == 'dosbox':
            return self._run_dosbox(demo_path)
        elif runner == 'wine':
            return self._run_wine(demo_path)
        elif runner == 'retroarch':
            return self._run_retroarch(demo_path, platform)
        else:
            # Try direct execution
            return self._run_native(demo_path)
    
    def _run_dosbox(self, demo_path):
        """Run demo in DOSBox."""
        conf = f"""
[autoexec]
mount c /tmp
c:
{demo_path}
"""
        conf_path = Path("/tmp/showet_dosbox.conf")
        conf_path.write_text(conf)
        
        cmd = ['dosbox', '-conf', str(conf_path), '-noconsole']
        return subprocess.Popen(cmd)
    
    def _run_wine(self, demo_path):
        """Run Windows demo through Wine."""
        cmd = ['wine', str(demo_path)]
        return subprocess.Popen(cmd)
    
    def _run_retroarch(self, demo_path, platform):
        """Run demo through RetroArch with libretro core."""
        core = self._get_libretro_core(platform)
        cmd = ['retroarch', '-L', core, str(demo_path)]
        return subprocess.Popen(cmd)
    
    def _run_native(self, demo_path):
        """Try native execution."""
        if os.access(demo_path, os.X_OK):
            return subprocess.Popen([demo_path])
        return None
    
    def _get_libretro_core(self, platform):
        """Get libretro core path for platform."""
        core_map = {
            'commodore_64': 'VICE/x64_libretro.so',
            'nintendo_famicom': 'QuickNES/nes_libretro.so',
            'nintendo_superfamicom': 'SNES9x/snes_libretro.so',
            'sega_megadrive': 'Genesis Plus GX/genesis_plus_gx_libretro.so',
            'dos': 'DOSBOX/dosbox_libretro.so',
        }
        return core_map.get(platform, 'DOSBOX/dosbox_libretro.so')


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: showet-executor <demo_path> [options]")
        print("\nOptions:")
        print("  --platform auto|dos|windows|amiga|c64|famicom|snes|megadrive")
        print("  --timeout SECONDS     Demo runtime timeout (default: 300)")
        print("  --prefer-retroarch    Use RetroArch even if native emulator exists")
        print("  --download-cores      Download missing RetroArch cores")
        print("\nAuto-detects platform and uses appropriate runner:")
        print("  Windows: Wine")
        print("  DOS: DOSBox (or RetroArch libretro)")
        print("  C64/Amiga/NES/SNES: Native emulator or RetroArch")
        print("  Other: RetroArch libretro cores")
        sys.exit(1)
    
    demo_path = sys.argv[1]
    platform = 'auto'
    timeout = 300
    prefer_retroarch = False
    download_cores = False
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--platform' and i + 1 < len(sys.argv):
            platform = sys.argv[i + 1]
            i += 1
        elif arg == '--timeout' and i + 1 < len(sys.argv):
            timeout = int(sys.argv[i + 1])
            i += 1
        elif arg == '--prefer-retroarch':
            prefer_retroarch = True
        elif arg == '--download-cores':
            download_cores = True
        i += 1
    
    executor = DemoExecutor(platform=platform, timeout=timeout, prefer_retroarch=prefer_retroarch)
    process = executor.run_demo(demo_path)
    
    if process:
        print(f"Demo launched! PID: {process.pid}")
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            print("Demo timed out, killing...")
            process.kill()
    else:
        print("Failed to launch demo - no suitable runner found")
        sys.exit(1)


if __name__ == '__main__':
    main()