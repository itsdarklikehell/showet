# Refactored for Modern Architecture - Phase 1
# This module inherits from PlatformBase which extends PlatformCommon

from __future__ import annotations

from typing import Any

from PlatformBase import PlatformBase


class Platform_Microsoft_Windows(PlatformBase):
    """Platform runner for Microsoft Windows demos."""

    def __init__(self):
        super().__init__("microsoft_windows", version="2.0.0-refactored")
        self.emulators = ["wine", "proton"]
        self.cores = ["wine"]
        self.extensions = ["exe"]

    def supported_platforms(self) -> list[str]:
        """Return the platform slug(s) this runner supports."""
        return ["microsoft_windows"]

    def initialize(self) -> bool:
        print("[Microsoft Windows] Initializing...")
        self._is_initialized = True
        return True

    def load_game(self, rom_path: str) -> bool:
        if not self.is_initialized():
            return False
        self._last_rom_path = rom_path
        print(f"[Microsoft Windows] Loaded: {rom_path}")
        return True

    def run_frame(self, controls: dict[str, Any]) -> bool:
        if not self.is_initialized() or not self._last_rom_path:
            return False
        if controls:
            print("[Microsoft Windows] Note: Control mapping pending")
        return True

    def get_status_report(self) -> dict[str, Any]:
        return {
            "platform": self.platform_name,
            "initialized": self.is_initialized(),
            "current_rom": self._last_rom_path or "none"
        }

    def save_state(self) -> bytes:
        print("[Microsoft Windows] State save: Delegated to RetroArch")
        return b""

    def load_state(self, state_data: bytes) -> bool:
        print("[Microsoft Windows] State load: Delegated to RetroArch")
        return True
