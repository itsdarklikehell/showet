#!/usr/bin/env python3
"""Common platform runner base class for showet.

This module provides the PlatformCommon base class that all platform runners
inherit from. It handles file discovery, disk sorting, and process execution.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

COREPATH = "/home/rizzo/.config/retroarch/cores"
DEBUGGING: bool = True


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
        """Find all files under the given path recursively.

        Args:
            path: Directory path to search.

        Returns:
            List of absolute file paths found.
        """
        path = Path(path)
        self.prod_files = []

        for root, _, files in os.walk(path):
            for file in files:
                self.prod_files.append(str(Path(root) / file))

        return self.prod_files

    def setup(self, showetdir: Path | str, datadir: Path | str, prod_platform: str) -> None:
        """Initialize the runner for a production.

        Args:
            showetdir: Base showet directory.
            datadir: Production data directory containing downloaded files.
            prod_platform: Platform slug for this production.
        """
        self.showetdir = Path(showetdir)
        self.datadir = Path(datadir)
        self.prod_platform = prod_platform
        self.find_files_recursively(self.datadir)

    def set_options(self, fullscreen: bool = False, audio: bool = True, core: str | None = None) -> None:
        """Set runtime options for the runner.

        Args:
            fullscreen: Start emulator in fullscreen mode.
            audio: Enable/disable audio output.
            core: Override the libretro core to use.
        """
        self.fullscreen = fullscreen
        self.audio = audio
        self.core_override = core

    def supported_platforms(self) -> list[str]:
        """Return list of platform slugs this runner supports.

        Subclasses must override this method.
        """
        raise NotImplementedError("Subclasses must implement supported_platforms()")

    def find_files_with_extension(self, extension: str) -> list[str]:
        """Find files matching the given extension.

        Args:
            extension: File extension without leading dot (e.g., 'd64').

        Returns:
            List of matching file paths.
        """
        return [
            f for f in self.prod_files
            if f.lower().endswith(extension.lower())
        ]

    def sort_disks(self, files: list[str]) -> list[str]:
        """Sort disk images in logical order.

        Args:
            files: List of file paths.

        Returns:
            Sorted list of file paths.
        """
        sorted_list = sorted(files, key=str.lower)
        if len(sorted_list) > 1 and DEBUGGING:
            print("\tGuessing disk order should be: ")
            print(sorted_list)
        return sorted_list

    def run_process(self, arguments: list[str]) -> int:
        """Execute an emulator command and stream output.

        Args:
            arguments: Command and arguments to execute.

        Returns:
            Process exit code.
        """
        # Insert fullscreen option for retroarch
        if self.fullscreen and arguments and arguments[0] == "retroarch":
            arguments.insert(1, "--fullscreen")

        if DEBUGGING:
            print("\tRunning command: ", arguments)
            print(f"\tFullscreen: {self.fullscreen}, Audio: {self.audio}")
            print("\t================================")

        process = subprocess.Popen(
            arguments,
            cwd=str(self.datadir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        process.wait()
        retcode = process.returncode

        for line in process.stdout:
            print(line.decode("utf-8"))

        if retcode and DEBUGGING:
            print(arguments, "\n\tprocess exited with ", retcode)

        return retcode
