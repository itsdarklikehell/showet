"""Runner for the pouet "vic20" platform.

Vic20 demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Commodore_Vic20(PlatformCommon):
    """Platform runner for Vic20 demos."""

    emulators = ["retroarch"]
    cores = ["vice_xvic_libretro"]
    extensions = ['zip']

    def supported_platforms(self) -> list[str]:
        """Return vic20 platform slug."""
        return ["vic20"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching vic20 demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
