"""Runner for the pouet "segastv" platform.

Segastv demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Sega_Stv(PlatformCommon):
    """Platform runner for Segastv demos."""

    emulators = ["retroarch"]
    cores = ["yabause_libretro"]
    extensions = ['zip', 'ccd', 'chd', 'cue', 'iso', 'mds', 'm3u']

    def supported_platforms(self) -> list[str]:
        """Return segastv platform slug."""
        return ["segastv"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching segastv demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
