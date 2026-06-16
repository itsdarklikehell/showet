# Refactored for Modern Architecture - Phase 1
# This module inherits from PlatformBase which extends PlatformCommon

from __future__ import annotations

from typing import Dict, Any, List
from PlatformBase import PlatformBase

class Platform_Commodore_64(PlatformBase):
    """Platform runner for Commodore 64 demos."""

    def __init__(self):
        super().__init__("commodore_64", version="2.0.0-refactored")
        self.emulators = ["retroarch"]
        self.cores = ["vice_x64sc_libretro"]
        self.extensions = ['zip', 'd64', 'd71', 'd81', 't64', 'tap', 'prg', 'p00', 'g64']

    def supported_platforms(self) -> List[str]:
        """Return the platform slug(s) this runner supports."""
        return ["commodore_64"]

    def initialize(self) -> bool:
        print(f"[Commodore 64] Initializing...")
        self._is_initialized = True
        return True

    def load_game(self, rom_path: str) -> bool:
        if not self.is_initialized():
            return False
        self._last_rom_path = rom_path
        print(f"[Commodore 64] Loaded: {rom_path}")
        return True

    def run_frame(self, controls: Dict[str, Any]) -> bool:
        if not self.is_initialized() or not self._last_rom_path:
            return False
        if controls:
            print(f"[Commodore 64] Note: Control mapping pending")
        return True

    def get_status_report(self) -> Dict[str, Any]:
        return {
            "platform": self.platform_name,
            "initialized": self.is_initialized(),
            "current_rom": self._last_rom_path or "none"
        }

    def save_state(self) -> bytes:
        print(f"[Commodore 64] State save: Delegated to RetroArch")
        return b""

    def load_state(self, state_data: bytes) -> bool:
        print(f"[Commodore 64] State load: Delegated to RetroArch")
        return True
