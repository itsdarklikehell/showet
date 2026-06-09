"""Runner for the pouet "amstrad_cpcbplus" platform.

This implements a minimal stub that can be expanded later.  The
``setup`` method should copy any extracted files into the expected
directory and the ``run`` method should launch the emulator using the
correct Retro‑Arch core.
"""

import pathlib, subprocess

class Platform_Amstrad_Cpcplus:
    @staticmethod
    def supported_platforms() -> list[str]:
        return ["amstrad_cpcbplus"]

    CORES = {"amstrad_cpcbplus": "amstrad_cpcplus_libretro.dll"}

    def setup(self, showet_dir, datadir, platform_slugs):
        self.showet_dir = pathlib.Path(showet_dir)
        self.datadir = pathlib.Path(datadir)
        self.platform = platform_slugs

    def run(self):
        core_name = self.CORES.get(self.platform)
        if not core_name:
            raise RuntimeError(f"No Retro‑Arch core configured for {self.platform}")
        game_file = self.datadir / "sample.cpc"
        if not game_file.exists():
            raise RuntimeError(f"Demo file {game_file} not found")
        cmd = ["retroarch", "-L", f"~/.config/retroarch/cores/{core_name}", str(game_file)]
        subprocess.run(cmd, check=True)
