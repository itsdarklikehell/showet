"""Runner for the pouet "zx81" platform.

Zx81 demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Sinclair_Zx81(PlatformCommon):
    """Platform runner for Zx81 demos."""

    emulators = ["retroarch"]
    cores = ["fuse_libretro"]
    extensions = ['tzx', 'tap', 'z80', 'rzx', 'scl', 'trd', 'dsk']

    def supported_platforms(self) -> list[str]:
        """Return zx81 platform slug."""
        return ["zx81"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching zx81 demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
