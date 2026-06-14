"""Runner for the pouet "unknown" platform.

Unknown demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Nintendo_Wii(PlatformCommon):
    """Platform runner for Unknown demos."""

    emulators = ["retroarch"]
    cores = ["dolphin_libretro"]
    extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz', 'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']

    def supported_platforms(self) -> list[str]:
        """Return unknown platform slug."""
        return ["unknown"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching unknown demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
