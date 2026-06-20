# Refactored for Modern Architecture - Phase 1
# This module inherits from PlatformBase which extends PlatformCommon

from __future__ import annotations

from typing import Dict, Any, List
from PlatformBase import PlatformBase

class Platform_Atari_ST(PlatformBase):
    """Platform runner for Atari ST demos."""

    def __init__(self):
        super().__init__("atari_st", version="2.0.0-refactored")
        self.emulators = ["retroarch", "hatari"]
        self.cores = ["hatari_libretro"]
        self.extensions = ['st', 'msa', 'stx', 'dim', 'ipf', 'm3u', 'zip']

    def supported_platforms(self) -> list[str]:
        return ["atari_st"]

    def initialize(self) -> bool:
        print(f"[Atari ST] Initializing...")
        self._is_initialized = True
        return True

    def load_game(self, rom_path: str) -> bool:
        if not self.is_initialized():
            return False
        self._last_rom_path = rom_path
        print(f"[Atari ST] Loaded: {rom_path}")
        return True

    def run_frame(self, controls: Dict[str, Any]) -> bool:
        if not self.is_initialized() or not self._last_rom_path:
            return False
        return True

    def get_status_report(self) -> Dict[str, Any]:
        return {
            "platform": self.platform_name,
            "initialized": self.is_initialized(),
            "current_rom": self._last_rom_path or "none"
        }

    def save_state(self) -> bytes:
        return b""

    def load_state(self, state_data: bytes) -> bool:
        return True