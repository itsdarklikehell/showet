"""Runner for the pouet "playstation2" platform.

Playstation2 demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Sony_Ps2(PlatformCommon):
    """Platform runner for Playstation2 demos."""

    emulators = ["retroarch"]
    cores = ["pcsx2_libretro"]
    extensions = ['zip', 'exe', 'psexe', 'cue', 'toc', 'bin', 'img', 'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

    def supported_platforms(self) -> list[str]:
        """Return playstation2 platform slug."""
        return ["playstation2"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching playstation2 demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
