"""Runner for the pouet "playstationportable" platform.

Playstationportable demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Sony_Psp(PlatformCommon):
    """Platform runner for Playstationportable demos."""

    emulators = ["retroarch"]
    cores = ["ppsspp_libretro"]
    extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']

    def supported_platforms(self) -> list[str]:
        """Return playstationportable platform slug."""
        return ["playstationportable"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching playstationportable demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
