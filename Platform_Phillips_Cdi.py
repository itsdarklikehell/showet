"""Runner for the pouet "palmos" platform.

Palmos demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Phillips_Cdi(PlatformCommon):
    """Platform runner for Palmos demos."""

    emulators = ["retroarch"]
    cores = ["samecdi_libretro"]
    extensions = ['zip', 'chd', 'iso']

    def supported_platforms(self) -> list[str]:
        """Return palmos platform slug."""
        return ["palmos"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching palmos demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
