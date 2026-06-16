# PlatformBase.py - Abstract Base Class for Showet Emulation
# Extends PlatformCommon to enforce a consistent OOP contract across all platforms

from __future__ import annotations

import abc
from typing import Dict, Any, List
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

    @abc.abstractmethod
    def initialize(self) -> bool:
        """Performs emulator setup. Returns True on success."""
        pass

    @abc.abstractmethod
    def load_game(self, rom_path: str) -> bool:
        """Loads a game ROM. Returns True on success."""
        pass

    @abc.abstractmethod
    def run_frame(self, controls: Dict[str, Any]) -> bool:
        """Executes one frame of emulation. Returns True on success."""
        pass

    @abc.abstractmethod
    def get_status_report(self) -> Dict[str, Any]:
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