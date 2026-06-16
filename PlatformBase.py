# PlatformBase.py - Abstract Base Class for Showet Emulation
# Extends PlatformCommon to enforce a consistent OOP contract across all platforms

from __future__ import annotations

import abc
from pathlib import Path
from typing import Any

from platformcommon import PlatformCommon


class PlatformBase(PlatformCommon, abc.ABC):
    """
    Abstract base class providing the OOP interface contract for all platform emulators.
    All platforms must inherit from this to ensure polymorphic compatibility.
    """

    def __init__(self, platform_name: str, version: str = "0.1.0"):
        """
        Initializes the platform emulator instance.
        
        :param platform_name: The name of the hardware platform (e.g., "NES", "C64").
        :param version: The version string of the emulator/platform implementation.
        """
        PlatformCommon.__init__(self)
        self.platform_name = platform_name
        self.version = version
        self._is_initialized: bool = False
        self._last_rom_path: str = ""
        self._run_duration: float = 0.0

    @abc.abstractmethod
    def initialize(self) -> bool:
        """Performs emulator setup. Returns True on success."""
        pass

    @abc.abstractmethod
    def load_game(self, rom_path: str) -> bool:
        """Loads a game ROM. Returns True on success."""
        pass

    @abc.abstractmethod
    def run_frame(self, controls: dict[str, Any]) -> bool:
        """Executes one frame of emulation. Returns True on success."""
        pass

    @abc.abstractmethod
    def get_status_report(self) -> dict[str, Any]:
        """Returns diagnostic status data."""
        pass

    @abc.abstractmethod
    def save_state(self) -> bytes:
        """Captures emulator state to bytes."""
        pass

    @abc.abstractmethod
    def load_state(self, state_data: bytes) -> bool:
        """Restores emulator state from bytes. Returns True on success."""
        pass

    def is_initialized(self) -> bool:
        """Check if platform has been initialized."""
        return self._is_initialized

    def run(self, frames: int = -1, frame_delay: float = 1/60) -> int:
        """Run the demo for a specified number of frames or until completion.
        
        This is the main entry point for running demos. It:
        1. Initializes the emulator
        2. Loads the ROM/disk image
        3. Runs the emulation loop
        4. Handles RetroArch integration
        
        Args:
            frames: Number of frames to run (-1 for continuous)
            frame_delay: Delay between frames in seconds
            
        Returns:
            0 on success, -1 on error
        """
        # Initialize if needed
        if not self.is_initialized():
            if not self.initialize():
                print(f"[{self.platform_name}] Initialization failed")
                return -1

        # Find and load the ROM
        if not self._last_rom_path:
            for ext in self.extensions:
                files = self.find_files_with_extension(ext)
                if files:
                    self._last_rom_path = files[0]
                    break

        if not self._last_rom_path:
            print(f"[{self.platform_name}] No ROM found in {self.datadir}")
            return -1

        if not self.load_game(self._last_rom_path):
            print(f"[{self.platform_name}] Failed to load ROM")
            return -1

        # Build RetroArch command
        core = self.core_override or (self.cores[0] if self.cores else None)
        if not core:
            print(f"[{self.platform_name}] No core specified")
            return -1

        core_path = Path.home() / ".config" / "retroarch" / "cores" / f"{core}.so"
        if not core_path.exists():
            # Try alternate location
            core_path = Path("/usr/lib/retroarch/cores") / f"{core}.so"

        cmd = ["retroarch"]
        
        # Add fullscreen option
        if self.fullscreen:
            cmd.append("--fullscreen")
        
        # Add audio option
        if not self.audio:
            cmd.append("--audio-null")
        
        # Add core and ROM
        cmd.extend([
            "--libretro", core_path if core_path.exists() else f"/usr/lib/retroarch/cores/{core}.so",
            self._last_rom_path,
        ])

        # Run RetroArch
        retcode = self.run_process(cmd)
        
        return 0 if retcode == 0 else -1