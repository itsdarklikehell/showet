"""Runner for the pouet "spectravision" platform.

Spectravision demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_SpectraVision_SpectraVideo(PlatformCommon):
    """Platform runner for Spectravision demos."""

    emulators = ["retroarch"]
    cores = ["bluemsx_libretro"]
    extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

    def supported_platforms(self) -> list[str]:
        """Return spectravision platform slug."""
        return ["spectravision"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching spectravision demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
