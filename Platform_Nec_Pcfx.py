"""Runner for the pouet "pcfx" platform.

PC-FX demo support via RetroArch.
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Nec_Pcfx(PlatformCommon):
    """Platform runner for NEC PC-FX demos via RetroArch."""

    emulators = ["retroarch"]
    cores = ["mednafen_pcfx_libretro"]
    extensions = ["cue", "ccd", "toc", "chd"]

    def supported_platforms(self) -> list[str]:
        """Return PC-FX platform slug."""
        return ["pcfx"]

    def run(self) -> None:
        """Execute the PC-FX demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)
        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching PC-FX demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found

