#!/usr/bin/env python3
"""Runner for the pouet "commodore_amiga" platform.

This minimal stub demonstrates how an Amiga demo would be launched.  It
extracts the game file (typically an .adf or .lha) and then launches the
Amiga emulator (emulation core) via Retro‑Arch.
"""

import pathlib, subprocess, os

class Platform_Commodore_Amiga:
    @staticmethod
    def supported_platforms() -> list[str]:
        return ["commodore_amiga"]

    CORES = {"commodore_amiga": "amiga_libretro.dll"}

    def setup(self, showet_dir, datadir, platform_slugs):
        self.showet_dir = pathlib.Path(showet_dir)
        self.datadir = pathlib.Path(datadir)
        self.platform = platform_slugs

    def run(self):
        core_name = self.CORES.get(self.platform)
        if not core_name:
            raise RuntimeError(f"No Retro‑Arch core configured for {self.platform}")

        # For Amiga demos we expect an .adf or other archive containing the
        # booted game.  This example just looks for the first .adf file.
        adf_file = next(self.datadir.glob("*.adf"), None)
        if not adf_file:
            raise RuntimeError(f"Demo disk file not found in {self.datadir}")

        cmd = [
            "retroarch",
            "-L", f"~/.config/retroarch/cores/{core_name}",
            adf_file.as_posix(),
        ]
        print(f"Launching Amiga demo via Retro‑Arch: {adf_file}")
        subprocess.run(cmd, check=True)
