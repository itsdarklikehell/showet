"""Runner for the pouet "nintendods" platform.

Nintendods demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Nintendo_3DS(PlatformCommon):
    """Platform runner for Nintendods demos."""

    emulators = ["retroarch"]
    cores = ["citra_libretro"]
    extensions = ['3ds', '3dsx', 'elf', 'axf', 'cci', 'cxi', 'app']

    def supported_platforms(self) -> list[str]:
        """Return nintendods platform slug."""
        return ["nintendods"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching nintendods demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
