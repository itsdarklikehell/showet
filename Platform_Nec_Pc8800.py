"""Runner for the pouet "pc8800" platform.

Pc8800 demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Nec_Pc8800(PlatformCommon):
    """Platform runner for Pc8800 demos."""

    emulators = ["retroarch"]
    cores = ["quasi88_libretro"]
    extensions = ['d88', 'u88', 'm3u']

    def supported_platforms(self) -> list[str]:
        """Return pc8800 platform slug."""
        return ["pc8800"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching pc8800 demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
