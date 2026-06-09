"""Runner for the pouet "apple_applei" platform.
"""

import pathlib, subprocess

class Platform_Apple_AppleI:
    @staticmethod
    def supported_platforms() -> list[str]:
        return ["apple_applei"]

    CORES = {"apple_applei": "apple2_libretro.dll"}

    def setup(self, showet_dir, datadir, platform_slugs):
        self.showet_dir = pathlib.Path(showet_dir)
        self.datadir = pathlib.Path(datadir)
        self.platform = platform_slugs

    def run(self):
        core_name = self.CORES.get(self.platform)
        if not core_name:
            raise RuntimeError(f"No Retro‑Arch core configured for {self.platform}")
        game_file = self.datadir / "demo.dsk"
        if not game_file.exists():
            raise RuntimeError(f"Demo file {game_file} not found")
        cmd = ["retroarch", "-L", f"~/.config/retroarch/cores/{core_name}", str(game_file)]
        subprocess.run(cmd, check=True)
