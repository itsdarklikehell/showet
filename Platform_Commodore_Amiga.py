"""Runner for the pouet "commodore_amiga" platform.

This module handles Amiga demo execution via RetroArch/libretro cores.
Refactored to use PlatformCommon as the base class for consistent interface.
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Commodore_Amiga(PlatformCommon):
    """Platform runner for Commodore Amiga demos.

    Uses RetroArch with appropriate libretro core for Amiga emulation.
    Supports .adf, .dms, .ipf, .adz disk images and .lha archives.
    """

    # Emulators and cores configuration
    emulators = ["retroarch"]
    cores = ["puae_libretro", "fsuae_libretro", "uae4arm_libretro"]
    extensions = ["adf", "dms", "ipf", "adz", "lha", "zip"]

    def supported_platforms(self) -> list[str]:
        """Return Amiga platform slugs supported by this runner."""
        return ["commodore_amiga"]

    def run(self) -> None:
        """Execute the Amiga demo using RetroArch with the configured core."""
        # Find runnable files
        files = []
        for ext in self.extensions:
            found = self.find_files_with_extension(ext)
            if found:
                files.extend(found)

        if not files:
            print("Didn't find any runnable files.")
            raise RuntimeError("No Amiga demo files found")

        # Sort disks if multiple found
        files = self.sort_disks(files)

        # Use first core (puae_libretro)
        core = self.cores[0]

        # Build retroarch command
        cmd = ["retroarch", "-L", core, files[0]]

        if DEBUGGING:
            print(f"Launching Amiga demo via RetroArch: {files[0]}")

        self.run_process(cmd)
