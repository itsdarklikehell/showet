# Refactored for Modern Architecture - Phase 1
# This module inherits from PlatformBase which extends PlatformCommon

from __future__ import annotations

from typing import Dict, Any, List
from PlatformBase import PlatformBase

class Platform_Snk_NeogeoPocket(PlatformBase):
    """Platform runner for Snk NeogeoPocket demos."""

    def __init__(self):
        super().__init__("snk_neogeopocket", version="2.0.0-refactored")
        self.emulators = ["retroarch"]
        self.cores = ["mednafen_ngp_libretro"]
        self.extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']

    def supported_platforms(self) -> list[str]:
        """Return the platform slug(s) this runner supports."""
        return ["snk_neogeopocket"]

    def initialize(self) -> bool:
        print(f"[Snk NeogeoPocket] Initializing...")
        self._is_initialized = True
        return True

    def load_game(self, rom_path: str) -> bool:
        if not self.is_initialized():
            return False
        self._last_rom_path = rom_path
        print(f"[Snk NeogeoPocket] Loaded: {rom_path}")
        return True

    def run_frame(self, controls: Dict[str, Any]) -> bool:
        if not self.is_initialized() or not self._last_rom_path:
            return False
        if controls:
            print(f"[Snk NeogeoPocket] Note: Control mapping pending")
        return True

    def get_status_report(self) -> Dict[str, Any]:
        return {
            "platform": self.platform_name,
            "initialized": self.is_initialized(),
            "current_rom": self._last_rom_path or "none"
        }

    def save_state(self) -> bytes:
        print(f"[Snk NeogeoPocket] State save: Delegated to RetroArch")
        return b""

    def load_state(self, state_data: bytes) -> bool:
        print(f"[Snk NeogeoPocket] State load: Delegated to RetroArch")
        return True
