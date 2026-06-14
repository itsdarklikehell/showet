"""Runner for the pouet "atarixlxe" platform.

Atarixlxe demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Atari_5200(PlatformCommon):
    """Platform runner for Atarixlxe demos."""

    emulators = ["retroarch"]
    cores = ["atari800_libretro"]
    extensions = ['zip', 'xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'atx', 'car', 'rom', 'com', 'xex']

    def supported_platforms(self) -> list[str]:
        """Return atarixlxe platform slug."""
        return ["atarixlxe"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching atarixlxe demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
