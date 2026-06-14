"""Runner for the pouet "gameparkgp2x" platform.

Gameparkgp2X demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Gamepark_2X(PlatformCommon):
    """Platform runner for Gameparkgp2X demos."""

    emulators = ["retroarch"]
    cores = ["mame_libretro"]
    extensions = ['zip', 'chd', '7z', 'cmd']

    def supported_platforms(self) -> list[str]:
        """Return gameparkgp2x platform slug."""
        return ["gameparkgp2x"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching gameparkgp2x demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
