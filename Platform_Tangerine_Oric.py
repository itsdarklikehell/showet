"""Runner for the pouet "oric" platform.

Oric-1/Atmos demo support via Euphoric or MAME.
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Tangerine_Oric(PlatformCommon):
    """Platform runner for Oric-1/Atmos demos."""

    emulators = ["euphoric", "mame"]
    cores = ["oric_libretro"]
    extensions = ["tap", "crt"]

    def supported_platforms(self) -> list[str]:
        """Return Oric platform slugs."""
        return ["oric", "oric1", "oricatmos"]

    def run(self) -> None:
        """Execute the Oric demo."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        cmd = ["euphoric", files[0]]
        if DEBUGGING:
            print(f"Launching Oric demo via Euphoric: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found