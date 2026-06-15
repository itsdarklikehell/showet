"""Runner for the pouet "raspberry-pi" platform.

Raspberry Pi bare-metal demo support.
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Raspberry_Pi(PlatformCommon):
    """Platform runner for Raspberry Pi demos."""

    emulators = ["native"]
    cores = []
    extensions = ["img", "zip"]  # SD card image formats

    def supported_platforms(self) -> list[str]:
        """Return Raspberry Pi platform slugs."""
        return ["raspberrypibaremetal", "raspberrypi", "rp2040"]

    def run(self) -> None:
        """Execute the Raspberry Pi demo (needs qemu or hardware)."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        # For now, provide instructions - could be extended with qemu
        print(f"Found demo files: {files}")
        print("Raspberry Pi demos require: (1) flashing SD card or (2) running in qemu")
        if DEBUGGING:
            print("Manual steps required for now - automatic Pi execution coming soon!")

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found