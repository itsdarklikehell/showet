"""Runner for the pouet "apple_applei" platform.

Refactored to use PlatformCommon as base class.
"""
from __future__ import annotations

from platformcommon import PlatformCommon


class Platform_Apple_AppleI(PlatformCommon):
    """Platform runner for Apple I demos via RetroArch."""

    emulators = ["retroarch"]
    cores = ["minivmac_libretro"]
    extensions = ["dsk", "img", "zip", "hvf", "cmd"]

    def supported_platforms(self) -> list[str]:
        """Return Apple I platform slugs."""
        return ["apple_applei"]

    def run(self) -> None:
        """Execute the Apple I demo using RetroArch."""
        for ext in self.extensions:
            files = self.find_files_with_extension(ext)
            if files:
                cmd = ["retroarch", "-L", self.cores[0], files[0]]
                self.run_process(cmd)
                return
        raise RuntimeError("No Apple I demo files found")
