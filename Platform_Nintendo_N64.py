# Refactored for Modern Architecture - Phase 1
# This module inherits from PlatformBase which extends PlatformCommon

from __future__ import annotations

from typing import Dict, Any, List
from PlatformBase import PlatformBase

class Platform_Nintendo_N64(PlatformBase):
    """Platform runner for Nintendo N64 demos."""

    def __init__(self):
        super().__init__("nintendo_n64", version="2.0.0-refactored")
        self.emulators = ["retroarch"]
        self.cores = ["mupen64plus_libretro"]
        self.extensions = ['n64', 'v64', 'z64', 'bin', 'u1', 'ndd']

    def supported_platforms(self) -> list[str]:
        """Return the platform slug(s) this runner supports."""
        return ["nintendo_n64"]

    def initialize(self) -> bool:
        print(f"[Nintendo N64] Initializing...")
        self._is_initialized = True
        return True

    def load_game(self, rom_path: str) -> bool:
        if not self.is_initialized():
            return False
        self._last_rom_path = rom_path
        print(f"[Nintendo N64] Loaded: {rom_path}")
        return True

    def run_frame(self, controls: Dict[str, Any]) -> bool:
        if not self.is_initialized() or not self._last_rom_path:
            return False
        if controls:
            print(f"[Nintendo N64] Note: Control mapping pending")
        return True

    def get_status_report(self) -> Dict[str, Any]:
        return {
            "platform": self.platform_name,
            "initialized": self.is_initialized(),
            "current_rom": self._last_rom_path or "none"
        }

    def save_state(self) -> bytes:
        print(f"[Nintendo N64] State save: Delegated to RetroArch")
        return b""

    def load_state(self, state_data: bytes) -> bool:
        print(f"[Nintendo N64] State load: Delegated to RetroArch")
        return True
