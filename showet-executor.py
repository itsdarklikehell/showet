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
        'dos': 'dosbox_core_libretro.so',
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
        'dosbox_core_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/dosbox_core_libretro.so',
        'puae_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/puae_libretro.so',
        'stella_libretro.so': 'https://buildbot.libretro.com/nightly/linux/x86_64/latest/stella_libretro.so',
    }
    
    PLATFORM_RUNNERS = {
        # Priority: RetroArch > Native emulator > Wine/DOSBox
        'windows': {
            'runner': 'wine',
            'retroarch_core': None,
            'dosbox_alt': 'dosbox-x',
            'extensions': ['.exe', '.bat', '.com'],
        },
        'dos': {
            'runner': 'dosbox-x',
            'retroarch_core': 'dosbox_core_libretro.so',
            'extensions': ['.exe', '.com', '.bat'],
        },
        'dosbox_x': {
            'runner': 'dosbox-x',
            'retroarch_core': 'dosbox_core_libretro.so',
            'extensions': ['.exe', '.com', '.bat'],
        },
        'linux': {
            'runner': None,
            'retroarch_core': None,
            'extensions': ['.x86', '.x86_64', ''],
        },
        'amiga': {
            'runner': 'fs-uae',
            'retroarch_core': 'puae_libretro.so',
            'extensions': ['.adf', '.hdf', ''],
            'bios_required': ['kick13.rom', 'kick31.rom'],
        },
        'c64': {
            'runner': 'x64sc',
            'retroarch_core': 'x64_libretro.so',
            'extensions': ['.d64', '.t64', '.prg'],
        },
        'commodore_amiga': {
            'runner': 'fs-uae',
            'retroarch_core': 'puae_libretro.so',
            'extensions': ['.adf', '.hdf', ''],
            'bios_required': ['kick13.rom', 'kick31.rom'],
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
        'zx_spectrum': {
            'runner': 'fuse',
            'retroarch_core': None,
            'extensions': ['.tap', '.tzx', '.z80'],
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
        
        # Check archives first
        if path.suffix.lower() in ['.zip', '.rar', '.7z', '.lha']:
            extracted = self.extract_archive(demo_path)
            if extracted:
                return self.detect_platform(extracted[0])
        
        # Platform detection
        if path.suffix in ['.adf', '.hdf']:
            return 'commodore_amiga'
        if 'amiga' in name:
            return 'commodore_amiga'
        if path.suffix in ['.d64', '.t64', '.prg', '.crt', '.tap']:
            return 'commodore_64'
        if 'c64' in name or 'commodore' in name:
            return 'commodore_64'
        if path.suffix in ['.exe', '.com', '.bat']:
            # Check if it's a DOS or Windows executable
            if shutil.which('dosbox-x') and self._is_dos_exe(demo_path):
                return 'dos'
            return 'windows'
        if path.suffix in ['.nes', '.fds']:
            return 'nintendo_famicom'
        if path.suffix in ['.smc', '.sfc']:
            return 'nintendo_superfamicom'
        if path.suffix in ['.md', '.bin', '.gen']:
            return 'sega_megadrive'
        if path.suffix in ['.tap', '.tzx', '.z80']:
            return 'zx_spectrum'
        
        return 'auto'

    def _is_dos_exe(self, demo_path):
        """Check if executable is DOS (vs Windows) using file command."""
        try:
            result = subprocess.run(['file', demo_path], capture_output=True, text=True)
            return 'DOS' in result.stdout or '16-bit' in result.stdout
        except:
            return False

    def extract_archive(self, archive_path):
        """Extract demo archive and return list of executables."""
        archive = Path(archive_path)
        ext = archive.suffix.lower()
        
        if ext not in self.ARCHIVE_HANDLERS:
            return None
        
        extract_dir = Path(f"/tmp/showet_demo_{archive.stem}")
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = self.ARCHIVE_HANDLERS[ext].copy()
        if ext == '.zip':
            cmd.extend([str(archive), '-d', str(extract_dir)])
        else:
            cmd.extend([str(archive), str(extract_dir)])
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            files = list(extract_dir.rglob('*'))
            return [f for f in files if f.suffix.lower() in 
                    ['.exe', '.com', '.adf', '.nes', '.smc', '.sfc', '.d64', '.prg', '.tap']]
        except subprocess.CalledProcessError:
            return None

    def find_runner(self, demo_path):
        """Find appropriate runner for demo, prioritizing RetroArch cores."""
        # Check RetroArch first
        if shutil.which('retroarch'):
            for plat, config in self.PLATFORM_RUNNERS.items():
                if config.get('retroarch_core'):
                    core = config['retroarch_core']
                    core_path = self._get_core_path(core)
                    if core_path or self._download_core(core):
                        return 'retroarch'
        # Check Wine for Windows demos
        if demo_path.lower().endswith(('.exe', '.bat', '.msi')):
            if shutil.which('wine'):
                return 'wine'
        # Check native emulators
        for plat, config in self.PLATFORM_RUNNERS.items():
            runner = config.get('runner')
            if runner and shutil.which(runner):
                return runner
        return None

    def _get_core_path(self, core_name):
        """Get RetroArch core path."""
        for search_path in [
            Path.home() / '.config/retroarch/cores' / core_name,
            Path('/usr/lib/retroarch/cores') / core_name,
            Path('/usr/lib/libretro') / core_name,
        ]:
            if search_path.exists():
                return str(search_path)
        return None

    def _download_core(self, core_name):
        """Download libretro core if missing."""
        if core_name not in self.LIBRETRO_CORE_URLS:
            return False
        
        retroarch_dir = Path.home() / '.config/retroarch/cores'
        retroarch_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Downloading {core_name}...")
        try:
            import urllib.request
            urllib.request.urlretrieve(self.LIBRETRO_CORE_URLS[core_name], retroarch_dir / core_name)
            return True
        except Exception as e:
            print(f"Failed to download core: {e}")
            return False

    def run_demo(self, demo_path, platform=None):
        """Execute a demo with auto-detection."""
        if platform is None:
            platform = self.detect_platform(demo_path)
        
        runner = self.find_runner(demo_path)
        
        if platform == 'dos' or runner == 'dosbox-x':
            return self._run_dosbox(demo_path)
        elif runner == 'wine':
            return self._run_wine(demo_path)
        elif runner == 'retroarch':
            return self._run_retroarch(demo_path, platform)
        elif runner in ['x64sc', 'fs-uae', 'fceux', 'snes9x', 'fuse']:
            return self._run_native(runner, demo_path)
        else:
            return self._run_native(None, demo_path)

    def _run_dosbox(self, demo_path):
        """Run demo in DOSBox-X with optimized config."""
        conf = f"""[sdl]
output = opengl

[cpu]
cycles = max
core = dynamic

[autoexec]
mount c /tmp
c:
{Path(demo_path).stem}.exe
"""
        conf_path = Path("/tmp/showet_dosbox.conf")
        conf_path.write_text(conf)
        
        cmd = ['dosbox-x', '-conf', str(conf_path)]
        return subprocess.Popen(cmd)

    def _run_wine(self, demo_path):
        """Run Windows demo through Wine."""
        cmd = ['wine', str(demo_path)]
        env = os.environ.copy()
        env['WINEDEBUG'] = '-all'  # Reduce output noise
        return subprocess.Popen(cmd, env=env)

    def _run_retroarch(self, demo_path, platform):
        """Run demo through RetroArch with libretro core."""
        core = self.LIBRETRO_CORES.get(platform, 'dosbox_core_libretro.so')
        core_path = self._get_core_path(core)
        
        if not core_path:
            print(f"RetroArch core not found for {platform}")
            return None
            
        cmd = ['retroarch', '-L', core_path, str(demo_path)]
        return subprocess.Popen(cmd)

    def _run_native(self, emulator, demo_path):
        """Try native execution or emulator."""
        if emulator:
            cmd = [emulator, str(demo_path)]
            return subprocess.Popen(cmd)
        if os.access(demo_path, os.X_OK):
            return subprocess.Popen([demo_path])
        return None


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
        print("  DOS: DOSBox-X (or RetroArch libretro)")
        print("  C64/Amiga/NES/SNES: Native emulator or RetroArch")
        print("  Archives: Auto-extracts then runs")
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