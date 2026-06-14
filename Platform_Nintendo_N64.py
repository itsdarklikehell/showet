"""Runner for the pouet "nintendo64" platform.

Nintendo64 demos
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Nintendo_N64(PlatformCommon):
    """Platform runner for Nintendo64 demos."""

    emulators = ["retroarch"]
    cores = ["mupen64plus_libretro"]
    extensions = ['n64', 'v64', 'z64', 'bin', 'u1', 'ndd']

    def supported_platforms(self) -> list[str]:
        """Return nintendo64 platform slug."""
        return ["nintendo64"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching nintendo64 demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
