# Refactored for Modern Architecture - Phase 1
# This module inherits from PlatformBase which extends PlatformCommon

from __future__ import annotations

from typing import Dict, Any, List
from PlatformBase import PlatformBase

class Platform_Tangerine_Oric(PlatformBase):
    """Platform runner for Tangerine Oric demos."""

    def __init__(self):
        super().__init__("tangerine_oric", version="2.0.0-refactored")
        self.emulators = ["euphoric", "mame"]
        self.cores = ["oric_libretro"]
        self.extensions = ["tap", "crt"]

    def initialize(self) -> bool:
        print(f"[Tangerine Oric] Initializing...")
        self._is_initialized = True
        return True

    def load_game(self, rom_path: str) -> bool:
        if not self.is_initialized():
            return False
        self._last_rom_path = rom_path
        print(f"[Tangerine Oric] Loaded: {rom_path}")
        return True

    def run_frame(self, controls: Dict[str, Any]) -> bool:
        if not self.is_initialized() or not self._last_rom_path:
            return False
        if controls:
            print(f"[Tangerine Oric] Note: Control mapping pending")
        return True

    def get_status_report(self) -> Dict[str, Any]:
        return {
            "platform": self.platform_name,
            "initialized": self.is_initialized(),
            "current_rom": self._last_rom_path or "none"
        }

    def save_state(self) -> bytes:
        print(f"[Tangerine Oric] State save: Delegated to RetroArch")
        return b""

    def load_state(self, state_data: bytes) -> bool:
        print(f"[Tangerine Oric] State load: Delegated to RetroArch")
        return True
