"""Showet Demo Runner - The definitive demoscene demo-runner.

This module implements the *showet* CLI for the showet project.  It
represents the entry point that orchestrates:

* Argument parsing – see :func:`build_arg_parser`
* Platform discovery – :func:`create_platform_runners`
* Decision making – deciding which platform runner should be used for a
  particular production (:func:`run_production`).

The project provides a unified interface for running demos from pouet.net,
scene.org, and modarchive.org across 84+ platforms with authentic CRT presentation.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Iterable, List

from showet_config import CACHE_DIR, DEBUG
from showet_downloader import download_production_json, download_production_file, get_random_production_id

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("showet")

# Cache for platform runners to avoid repeated imports
_runner_cache: List[object] | None = None


# ---------------------------------------------------------------------------
# Utility helpers – only used inside this module, no public API.
# ---------------------------------------------------------------------------
def _load_platform_module(name: str):
    """Dynamically import a platform module.

    The project layout places each platform implementation in the same
    directory as this file.  ``importlib`` can load it without a package
    prefix.
    """
    import importlib
    try:
        return importlib.import_module(name)
    except Exception as exc:  # pragma: no cover – exercised by tests
        raise RuntimeError(f"Failed to import platform module {name}") from exc


def build_arg_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Show a demo on screen.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  showet 12345              Run demo by pouet.net ID
  showet 12345 --fullscreen  Run in fullscreen mode
  showet 12345 --core pcsx_rearmed_libretro  Use specific RetroArch core
  showet --platforms         List supported platforms
        """,
    )
    parser.add_argument(
        "pouetid",
        type=int,
        nargs="?",
        help="Pouet ID of the production to show",
    )
    parser.add_argument(
        "--platforms", action="store_true", help="List supported platforms and exit"
    )
    parser.add_argument(
        "--random", action="store_true", help="Play random productions"
    )
    parser.add_argument(
        "--fullscreen", action="store_true",
        help="Start emulator in fullscreen mode (where supported)"
    )
    parser.add_argument(
        "--audio", action="store_true", default=True,
        help="Enable audio output (default: True, use --no-audio to disable)"
    )
    parser.add_argument(
        "--no-audio", dest="audio", action="store_false",
        help="Disable audio output"
    )
    parser.add_argument(
        "--core", type=str,
        help="Specify libretro core to use (e.g., pcsx_rearmed_libretro)"
    )
    return parser


def create_platform_runners() -> List[object]:
    """Instantiate runner objects for every known platform.

    Uses caching to avoid repeated module imports on subsequent calls.
    Lazily loads platform modules to reduce import overhead and prevent side‑effects.
    """
    global _runner_cache

    if _runner_cache is not None:
        return _runner_cache

    module_names = [
        "Platform_Alambik_Alambik",
        "Platform_Amstrad_Cpcplus",
        "Platform_Android_Android",
        "Platform_Apple_AppleI",
        "Platform_Apple_AppleII",
        "Platform_Apple_AppleIIGS",
        "Platform_Arcade_Arcade",
        "Platform_Archimedes_Acorn",
        "Platform_Atari_2600",
        "Platform_Atari_5200",
        "Platform_Atari_7800",
        "Platform_Atari_Jaguar",
        "Platform_Atari_Lynx",
        "Platform_Atari_ST",
        "Platform_Atari_STe",
        "Platform_Atari_STETTFalcon",
        "Platform_Atari_xlxe",
        "Platform_Bandai_Wonderswan",
        "Platform_Commodore_64",
        "Platform_Commodore_128",
        "Platform_Commodore_Amiga",
        "Platform_Commodore_Amiga_AGA",
        "Platform_Commodore_CBMII",
        "Platform_Commodore_Pet",
        "Platform_Commodore_Plus4",
        "Platform_Commodore_Vic20",
        "Platform_Elektronika_Pdp11",
        "Platform_Enterprise_Ep128",
        "Platform_Fairchild_Channelf",
        "Platform_FanCon_Pico8",
        "Platform_Flash_Ruffle",
        "Platform_Gamepark_2X",
        "Platform_Gamepark_32",
        "Platform_GCE_Vectrex",
        "Platform_Java_Java",
        "Platform_Linux_Linux",
        "Platform_Magnavox_Odyssey",
        "Platform_Mattel_Intellivision",
        "Platform_Microsoft_Msdos",
        "Platform_Microsoft_Msx",
        "Platform_Microsoft_Windows",
        "Platform_Microsoft_Xbox",
        "Platform_Nec_Pc98",
        "Platform_Nec_Pc8000",
        "Platform_Nec_Pc8800",
        "Platform_Nec_Pcengine",
        "Platform_Nec_Pcfx",
        "Platform_Nec_Supergrafx",
        "Platform_Nintendo_3DS",
        "Platform_Nintendo_Famicom",
        "Platform_Nintendo_FamicomDisksystem",
        "Platform_Nintendo_Gameboy",
        "Platform_Nintendo_GameboyAdvance",
        "Platform_Nintendo_GameboyColor",
        "Platform_Nintendo_GameCube",
        "Platform_Nintendo_N64",
        "Platform_Nintendo_Pokemini",
        "Platform_Nintendo_SuperFamicom",
        "Platform_Nintendo_VirtualBoy",
        "Platform_Nintendo_Wii",
        "Platform_Palm_PalmOS",
        "Platform_Panasonic_3do",
        "Platform_Phillips_Cdi",
        "Platform_Sega_32X",
        "Platform_Sega_Dreamcast",
        "Platform_Sega_GameGear",
        "Platform_Sega_Mastersystem",
        "Platform_Sega_Megadrive",
        "Platform_Sega_Saturn",
        "Platform_Sega_SG1000",
        "Platform_Sega_Stv",
        "Platform_Sega_Vmu",
        "Platform_Sharp_MZ",
        "Platform_Sinclair_Zx81",
        "Platform_Sinclair_Zxspectrum",
        "Platform_Spectrum_ZXEnhanced",
        "Platform_Snk_Neogeo",
        "Platform_Snk_NeogeoPocket",
        "Platform_Snk_NeogeoPocketColor",
        "Platform_Sony_Ps2",
        "Platform_Sony_Psp",
        "Platform_Sony_Psx",
        "Platform_SpectraVision_SpectraVideo",
        "Platform_Thomson_MOTO",
        "Platform_TI_8x",
        "Platform_Wild_Gamemusic",
        "Platform_Wild_VideoFFMPEG",
        "Platform_Wild_VideoMPV",
        "Platform_Tangerine_Oric",
        "Platform_WebAssembly_Web",
        "Platform_Raspberry_Pi",
    ]

    runners: List[object] = []
    for mod_name in module_names:
        mod = _load_platform_module(mod_name)
        cls = getattr(mod, mod_name)
        runners.append(cls())
    _runner_cache = runners
    return runners


def list_supported_platforms(platform_runners: Iterable[object]) -> None:
    """Print a sorted list of all supported platforms across runners."""
    seen = set()
    for runner in platform_runners:
        for platform in runner.supported_platforms():
            if platform not in seen:
                print(platform)
                seen.add(platform)


def run_production(args: argparse.Namespace, platform_runners: List[object]) -> int:
    """Execute a production based on the supplied CLI arguments.

    Returns 0 on success, -1 on error.
    """
    if not args.pouetid and not args.random:
        print("No pouet id specified. Use --help to see options.")
        return -1

    prod_id = args.pouetid
    if args.random:
        prod_id = get_random_production_id()
        if prod_id == -1:
            print("Could not find a random demo.")
            return -1
        print(f"Randomly selected demo ID: {prod_id}")

    data = download_production_json(prod_id)
    prod_platforms = [p["slug"] for p in data["prod"]["platforms"].values()]
    runner, platform_found = _select_runner(platform_runners, prod_platforms)
    if not runner:
        print(f"ERROR: Platform {prod_platforms} not supported (yet!).")
        return -1

    if len(prod_platforms) > 1:
        print(
            "Demo supports platforms ", prod_platforms,
            "of which", platform_found, "rules the most."
        )

    if DEBUG:
        print("\tName:", data["prod"]["name"])  # pragma: no cover – side‑effect
        if data["prod"]["groups"]:
            print("\tBy:", data["prod"]["groups"][0]["name"])  # pragma: no cover
        print("\tType:", data["prod"]["type"])  # pragma: no cover
        print("\tPlatform:", platform_found)  # pragma: no cover

    datadir = Path.home() / ".showet" / "data" / str(prod_id)
    download_production_file(data, datadir)
    runner.setup(Path.home() / ".showet", datadir, platform_found)
    runner.set_options(
        fullscreen=getattr(args, "fullscreen", False),
        audio=getattr(args, "audio", True),
        core=getattr(args, "core", None),
    )
    runner.run()
    return 0


def _select_runner(runners: List[object], potential_platforms: List[str]) -> tuple[object | None, str | None]:
    """Return the first runner that supports any of the supplied platforms.

    The function returns a tuple ``(runner, matched_slug)`` – ``matched_slug`` is
    the slug that caused the match (i.e. the slug returned from
    ``supported_platforms()``).  ``runner`` will be ``None`` if no runner
    matches.
    """
    for reason in potential_platforms:
        for prunner in runners:
            if reason in prunner.supported_platforms():
                return prunner, reason
    return None, None


def main(argv: List[str] | None = None) -> int:
    """Entry point for ``python -m showet``."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    runners = create_platform_runners()
    if args.platforms:
        list_supported_platforms(runners)
        return 0
    return run_production(args, runners)


if __name__ == "__main__":  # pragma: no cover – CLI invoker
    raise SystemExit(main())
