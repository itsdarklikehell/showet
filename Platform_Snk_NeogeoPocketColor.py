"""Runner for the pouet "neogeopocketcolor" platform.

Neogeopocketcolor demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Snk_NeogeoPocketColor(PlatformCommon):
    """Platform runner for Neogeopocketcolor demos."""

    emulators = ["retroarch"]
    cores = ["mednafen_ngp_libretro"]
    extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']

    def supported_platforms(self) -> list[str]:
        """Return neogeopocketcolor platform slug."""
        return ["neogeopocketcolor"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching neogeopocketcolor demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
