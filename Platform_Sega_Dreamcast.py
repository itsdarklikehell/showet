"""Runner for the pouet "dreamcast" platform.

Dreamcast demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Sega_Dreamcast(PlatformCommon):
    """Platform runner for Dreamcast demos."""

    emulators = ["retroarch"]
    cores = ["flycast_libretro"]
    extensions = ['chd', 'cdi', 'elf', 'bin', 'cue', 'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']

    def supported_platforms(self) -> list[str]:
        """Return dreamcast platform slug."""
        return ["dreamcast"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching dreamcast demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
