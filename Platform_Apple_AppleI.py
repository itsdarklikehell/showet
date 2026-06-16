# Refactored for Modern Architecture - Phase 1
# This module inherits from PlatformBase which extends PlatformCommon

from __future__ import annotations

from typing import Dict, Any, List
from PlatformBase import PlatformBase

class Platform_Apple_AppleI(PlatformBase):
    """Platform runner for Apple AppleI demos."""

    def __init__(self):
        super().__init__("apple_applei", version="2.0.0-refactored")
        self.emulators = ["retroarch"]
        self.cores = ["minivmac_libretro"]
        self.extensions = ["dsk", "img", "zip", "hvf", "cmd"]

    def initialize(self) -> bool:
        print(f"[Apple AppleI] Initializing...")
        self._is_initialized = True
        return True

    def load_game(self, rom_path: str) -> bool:
        if not self.is_initialized():
            return False
        self._last_rom_path = rom_path
        print(f"[Apple AppleI] Loaded: {rom_path}")
        return True

    def run_frame(self, controls: Dict[str, Any]) -> bool:
        if not self.is_initialized() or not self._last_rom_path:
            return False
        if controls:
            print(f"[Apple AppleI] Note: Control mapping pending")
        return True

    def get_status_report(self) -> Dict[str, Any]:
        return {
            "platform": self.platform_name,
            "initialized": self.is_initialized(),
            "current_rom": self._last_rom_path or "none"
        }

    def save_state(self) -> bytes:
        print(f"[Apple AppleI] State save: Delegated to RetroArch")
        return b""

    def load_state(self, state_data: bytes) -> bool:
        print(f"[Apple AppleI] State load: Delegated to RetroArch")
        return True
