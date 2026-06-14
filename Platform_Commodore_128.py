"""Runner for the pouet "commodore128" platform.

Commodore 128 demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Commodore_128(PlatformCommon):
    """Platform runner for Commodore 128 demos."""

    emulators = ["retroarch"]
    cores = ["vice_x128_libretro"]
    extensions = ['d64', 'd71', 'd81', 't64', 'tap', 'prg', 'p00']

    def supported_platforms(self) -> list[str]:
        """Return commodore128 platform slug."""
        return ["commodore128"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching commodore128 demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
