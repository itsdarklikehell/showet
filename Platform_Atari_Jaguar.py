"""Runner for the pouet "atarijaguar" platform.

Atarijaguar demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Atari_Jaguar(PlatformCommon):
    """Platform runner for Atarijaguar demos."""

    emulators = ["retroarch"]
    cores = ["virtualjaguar_libretro"]
    extensions = ['zip', 'j64', 'jag', 'rom', 'abs', 'cof', 'bin', 'prg']

    def supported_platforms(self) -> list[str]:
        """Return atarijaguar platform slug."""
        return ["atarijaguar"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching atarijaguar demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
