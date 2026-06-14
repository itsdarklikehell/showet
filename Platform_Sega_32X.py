"""Runner for the pouet "sega32x" platform.

Sega32X demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Sega_32X(PlatformCommon):
    """Platform runner for Sega32X demos."""

    emulators = ["retroarch"]
    cores = ["picodrive_libretro"]
    extensions = ['zip', 'bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']

    def supported_platforms(self) -> list[str]:
        """Return sega32x platform slug."""
        return ["sega32x"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching sega32x demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
