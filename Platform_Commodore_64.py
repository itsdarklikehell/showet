# Refactored for Modern Architecture - Phase 1
# This module inherits from PlatformBase which extends PlatformCommon

from __future__ import annotations

from typing import Any

from PlatformBase import PlatformBase


class Platform_Commodore_64(PlatformBase):
    """Platform runner for Commodore 64 demos."""

    def __init__(self):
        super().__init__("commodore_64", version="2.0.0-refactored")
        self.emulators = ["retroarch"]
        self.cores = ["vice_x64sc_libretro"]
        self.extensions = ['zip', 'd64', 'd71', 'd81', 't64', 'tap', 'prg', 'p00', 'g64']

    def supported_platforms(self) -> list[str]:
        """Return the platform slug(s) this runner supports."""
        return ["commodore_64", "commodore64"]

    def run(self, frames: int = -1, frame_delay: float = 1/60) -> int:
        """Run the C64 demo using VICE (x64sc) directly.
        
        Args:
            frames: Number of frames (ignored by VICE).
            frame_delay: Frame delay (ignored by VICE).
        """
        from pathlib import Path
        import subprocess

        d64s = self.find_files_with_extension('d64')
        prgs = self.find_files_with_extension('prg')

        if not d64s and not prgs:
            print("Didn't find any d64 or prg files.")
            return -1

        cmd = ['x64sc']
        if self.fullscreen:
            cmd.append('-fullscreen')

        if d64s:
            # Write fliplist for multi-disk
            flipfile = Path(self.datadir) / "fliplist.vfl"
            with open(flipfile, "w") as f:
                f.write("UNIT 8\n")
                for disk in sorted(d64s):
                    f.write(str(disk) + "\n")
            cmd.extend(['-flipname', str(flipfile), str(d64s[0])])

        if prgs and not d64s:
            cmd.append(str(prgs[0]))

        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=self.datadir)
        return result.returncode

    def initialize(self) -> bool:
        print("[Commodore 64] Initializing...")
        self._is_initialized = True
        return True

    def load_game(self, rom_path: str) -> bool:
        if not self.is_initialized():
            return False
        self._last_rom_path = rom_path
        print(f"[Commodore 64] Loaded: {rom_path}")
        return True

    def run_frame(self, controls: dict[str, Any]) -> bool:
        if not self.is_initialized() or not self._last_rom_path:
            return False
        if controls:
            print("[Commodore 64] Note: Control mapping pending")
        return True

    def get_status_report(self) -> dict[str, Any]:
        return {
            "platform": self.platform_name,
            "initialized": self.is_initialized(),
            "current_rom": self._last_rom_path or "none"
        }

    def save_state(self) -> bytes:
        print("[Commodore 64] State save: Delegated to RetroArch")
        return b""

    def load_state(self, state_data: bytes) -> bool:
        print("[Commodore 64] State load: Delegated to RetroArch")
        return True
