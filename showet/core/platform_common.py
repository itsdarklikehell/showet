"""Platform common utilities for Showet.

Provides base functionality for file discovery, disk management, and process execution.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any


class PlatformCommon:
    """Base class for all platform runners.

    Provides common functionality for file discovery, disk management,
    and emulator process execution.
    """

    emulators: list[str] = []
    cores: list[str] = []
    extensions: list[str] = []

    def __init__(self) -> None:
        self.showetdir: Path | None = None
        self.datadir: Path | None = None
        self.prod_platform: str | None = None
        self.prod_files: list[str] = []
        self.fullscreen: bool = False
        self.audio: bool = True
        self.core_override: str | None = None

    def find_files_recursively(self, path: Path | str) -> list[str]:
        """Find all files under the given path recursively."""
        path = Path(path)
        self.prod_files = []

        for root, _, files in os.walk(path):
            for file in files:
                self.prod_files.append(str(Path(root) / file))

        return self.prod_files

    def setup(self, showetdir: Path | str, datadir: Path | str, prod_platform: str) -> None:
        """Initialize the runner for a production."""
        self.showetdir = Path(showetdir)
        self.datadir = Path(datadir)
        self.prod_platform = prod_platform
        self.find_files_recursively(self.datadir)

    def set_options(self, fullscreen: bool = False, audio: bool = True, core: str | None = None) -> None:
        """Set runtime options for the runner."""
        self.fullscreen = fullscreen
        self.audio = audio
        self.core_override = core

    def supported_platforms(self) -> list[str]:
        """Return list of platform slugs this runner supports."""
        raise NotImplementedError("Subclasses must implement supported_platforms()")

    def find_files_with_extension(self, extension: str) -> list[str]:
        """Find files matching the given extension."""
        return [
            f for f in self.prod_files
            if f.lower().endswith(extension.lower())
        ]

    def sort_disks(self, files: list[str]) -> list[str]:
        """Sort disk images in logical order."""
        return sorted(files, key=str.lower)

    def run_process(self, arguments: list[str]) -> int:
        """Execute an emulator command and stream output."""
        process = subprocess.Popen(
            arguments,
            cwd=str(self.datadir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        process.wait()
        return process.returncode