"""Runner for the pouet "enterprise" platform.

Enterprise demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Enterprise_Ep128(PlatformCommon):
    """Platform runner for Enterprise demos."""

    emulators = ["retroarch"]
    cores = ["ep128emu_libretro"]
    extensions = ['zip', 'img', 'dsk', 'tap', 'dtf', 'com', 'trn', '128', 'bas', 'cas', 'cdt', 'tzx', '.']

    def supported_platforms(self) -> list[str]:
        """Return enterprise platform slug."""
        return ["enterprise"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching enterprise demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
