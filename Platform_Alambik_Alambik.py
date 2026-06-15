"""Runner for Alambik demos.

Alambik is a proprietary Windows browser plugin for interactive demos.
Note: This is experimental - Alambik Player is Windows-only and may require Wine.
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Alambik_Alambik(PlatformCommon):
    """Platform runner for Alambik interactive demos."""

    emulators = ["wine"]
    cores = []
    extensions = ["sam", "alb"]

    def supported_platforms(self) -> list[str]:
        """Return Alambik platform slugs."""
        return ["alambik"]

    def run(self) -> None:
        """Execute the Alambik demo using Wine."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        if DEBUGGING:
            print("Alambik demos require the Alambik Player plugin.")

        # Try to find Alambik Player in Wine
        alambik_path = self._find_alambik_player()
        if not alambik_path:
            print("Alambik Player not found. Please install it in Wine.")
            print("Download from: https://www.alambik.com/")
            return

        if DEBUGGING:
            print(f"Launching Alambik demo: {files[0]}")

        # Alambik files can be opened by the player
        cmd = ["wine", str(alambik_path), str(self.datadir / files[0])]
        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
            found.extend(self.find_files_with_extension(ext.upper()))
        return found

    def _find_alambik_player(self) -> str | None:
        """Find Alambik Player installation in Wine."""
        import os
        from pathlib import Path

        # Common Wine installation paths for Alambik
        possible_paths = [
            Path.home() / ".wine" / "drive_c" / "Program Files" / "Alambik" / "AlambikPlayer.exe",
            Path.home() / ".wine" / "drive_c" / "Program Files (x86)" / "Alambik" / "AlambikPlayer.exe",
            Path.home() / ".local" / "share" / "wine" / "prefix" / "drive_c" / "Program Files" / "Alambik" / "AlambikPlayer.exe",
        ]

        for path in possible_paths:
            if path.exists():
                return str(path)
        return None