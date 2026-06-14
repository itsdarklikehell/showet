"""Runner for the pouet "pico8" platform.

Pico8 demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_FanCon_Pico8(PlatformCommon):
    """Platform runner for Pico8 demos."""

    emulators = ["retroarch"]
    cores = ["retro8_libretro"]
    extensions = ['zip', 'p8', 'png']

    def supported_platforms(self) -> list[str]:
        """Return pico8 platform slug."""
        return ["pico8"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching pico8 demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
