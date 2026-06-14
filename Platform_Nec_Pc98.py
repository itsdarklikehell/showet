"""Runner for the pouet "pc-98" platform.

Pc-98 demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Nec_Pc98(PlatformCommon):
    """Platform runner for Pc-98 demos."""

    emulators = ["retroarch"]
    cores = ["nekop2_libretro"]
    extensions = ['d98', 'zip', '98d', 'fdi', 'fdd', '2hd', 'tfd', 'd88', '88d', 'hdm', 'xdf', 'dup', 'cmd', 'hdi', 'thd', 'nhd', 'hdd']

    def supported_platforms(self) -> list[str]:
        """Return pc-98 platform slug."""
        return ["pc-98"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching pc-98 demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
