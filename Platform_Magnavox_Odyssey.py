# Refactored for Modern Architecture - Phase 1
# This module inherits from PlatformBase which extends PlatformCommon

from __future__ import annotations

from typing import Any

from PlatformBase import PlatformBase


class Platform_Magnavox_Odyssey(PlatformBase):
    """Platform runner for Magnavox Odyssey demos."""

    def __init__(self):
        super().__init__("magnavox_odyssey", version="2.0.0-refactored")
        self.emulators = ["retroarch"]
        self.cores = ["o2em_libretro"]
        self.extensions = ['zip', 'bin']

    def supported_platforms(self) -> list[str]:
        """Return the platform slug(s) this runner supports."""
        return ["magnavox_odyssey"]

    def initialize(self) -> bool:
        print("[Magnavox Odyssey] Initializing...")
        self._is_initialized = True
        return True

    def load_game(self, rom_path: str) -> bool:
        if not self.is_initialized():
            return False
        self._last_rom_path = rom_path
        print(f"[Magnavox Odyssey] Loaded: {rom_path}")
        return True

    def run_frame(self, controls: dict[str, Any]) -> bool:
        if not self.is_initialized() or not self._last_rom_path:
            return False
        if controls:
            print("[Magnavox Odyssey] Note: Control mapping pending")
        return True

    def get_status_report(self) -> dict[str, Any]:
        return {
            "platform": self.platform_name,
            "initialized": self.is_initialized(),
            "current_rom": self._last_rom_path or "none"
        }

    def save_state(self) -> bytes:
        print("[Magnavox Odyssey] State save: Delegated to RetroArch")
        return b""

    def load_state(self, state_data: bytes) -> bool:
        print("[Magnavox Odyssey] State load: Delegated to RetroArch")
        return True
