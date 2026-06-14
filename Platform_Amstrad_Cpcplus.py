"""Runner for the pouet "amstrad_cpcbplus" platform.

This implements a minimal stub that can be expanded later.  The
setup method copies any extracted files into the expected directory and
the run method launches the emulator using the correct RetroArch core.
Refactored to use PlatformCommon as base class.
"""
from __future__ import annotations

from platformcommon import PlatformCommon


class Platform_Amstrad_Cpcplus(PlatformCommon):
    """Platform runner for Amstrad CPC+ demos.

    Uses RetroArch with Amstrad CPC libretro core.
    Currently a stub implementation.
    """

    emulators = ["retroarch"]
    cores = ["cap32_libretro"]
    extensions = ["dsk", "sna", "kcr"]

    def supported_platforms(self) -> list[str]:
        """Return CPC+ platform slugs supported by this runner."""
        return ["amstrad_cpcbplus"]

    def run(self) -> None:
        """Execute the CPC demo using RetroArch."""
        # Find any runnable file with supported extensions
        for ext in self.extensions:
            files = self.find_files_with_extension(ext)
            if files:
                cmd = ["retroarch", "-L", self.cores[0], files[0]]
                self.run_process(cmd)
                return
        raise RuntimeError("No CPC demo files found")
