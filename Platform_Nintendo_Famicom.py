"""Runner for the pouet "nesfamicom" platform.

Nesfamicom demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Nintendo_Famicom(PlatformCommon):
    """Platform runner for Nesfamicom demos."""

    emulators = ["retroarch"]
    cores = ["quicknes_libretro"]
    extensions = ['zip', 'nes', 'fds', 'unf', 'unif', 'qd', 'nsf', 'bin', 'rom']

    def supported_platforms(self) -> list[str]:
        """Return nesfamicom platform slug."""
        return ["nesfamicom"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching nesfamicom demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
