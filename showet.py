"""Show a demo from pouet.net using platform runners.

This module implements the *showet* CLI for the showet project.  It
represents the entry point that orchestrates:

* Argument parsing – see :func:`build_arg_parser`
* Platform discovery – :func:`create_platform_runners`
* Decision making – deciding which platform runner should be used for a
  particular production (:func:`run_production`).

The project originally bundled a naïve implementation that conducted
heavy‑lifting at import time.  The refactored version keeps import
side‑effects to a minimum and splits behaviour into small, testable
functions.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from pathlib import Path
from typing import Iterable, List

DEBUGGING = True

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
    parser = argparse.ArgumentParser(description="Show a demo on screen.")
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
        "Platform_Atari_STETTFalcon",
        "Platform_Atari_xlxe",
        "Platform_Bandai_Wonderswan",
        "Platform_Commodore_64",
        "Platform_Commodore_128",
        "Platform_Commodore_Amiga",
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
        "Platform_Sinclair_Zx81",
        "Platform_Sinclair_Zxspectrum",
        "Platform_Snk_Neogeo",
        "Platform_Snk_NeogeoPocket",
        "Platform_Snk_NeogeoPocketColor",
        "Platform_Sony_Ps2",
        "Platform_Sony_Psp",
        "Platform_Sony_Psx",
        "Platform_SpectraVision_SpectraVideo",
        "Platform_Thomson_MOTO",
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


# ---------------------------------------------------------------------------
# Production download & setup
# ---------------------------------------------------------------------------
def _download_json(prod_id: int) -> dict:
    """Download JSON metadata for a production, caching it locally."""
    cache_dir = Path.home() / ".showet" / "data" / str(prod_id)
    cache_dir.mkdir(parents=True, exist_ok=True)
    json_path = cache_dir / "pouet.json"
    if json_path.exists() and DEBUGGING:
        print("Json already downloaded.")
        return json.loads(json_path.read_text())
    url = f"http://api.pouet.net/v1/prod/?id={prod_id}"
    json_str = urllib.request.urlopen(url).read().decode()
    json_path.write_text(json_str)
    return json.loads(json_str)


def _download_production_file(data: dict, datadir: Path) -> Path:
    """Download the production file (if missing) and return its path."""
    download_url = data["prod"]["download"].replace(
        "https://files.scene.org/view", "https://files.scene.org/get"
    )
    flag_file = datadir / ".FILES_DOWNLOADED"
    if flag_file.exists():
        if DEBUGGING:
            print("\tFile already downloaded")
        return datadir
    if DEBUGGING:
        print(f"\tDownloading prod file from {download_url}...")
    response = urllib.request.urlopen(download_url)
    filename = os.path.basename(response.url)
    if not filename:
        raise RuntimeError(f"Error downloading file at {download_url}")
    dest = datadir / filename
    dest.write_bytes(response.read())
    if DEBUGGING:
        print(f"\tDownloaded: {dest}")
        print(f"\tFilesize: {dest.stat().st_size}")
    flag_file.touch()
    return datadir


def run_production(args: argparse.Namespace, platform_runners: List[object]) -> int:
    """Execute a production based on the supplied CLI arguments.

    Returns 0 on success, -1 on error.
    """
    if not args.pouetid:
        print("No pouet id specified. Use --help to see options.")
        return -1

    data = _download_json(args.pouetid)
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

    if DEBUGGING:
        print("\tName:", data["prod"]["name"])  # pragma: no cover – side‑effect
        if data["prod"]["groups"]:
            print("\tBy:", data["prod"]["groups"][0]["name"])  # pragma: no cover
        print("\tType:", data["prod"]["type"])  # pragma: no cover
        print("\tPlatform:", platform_found)  # pragma: no cover

    datadir = Path.home() / ".showet" / "data" / str(args.pouetid)
    _download_production_file(data, datadir)
    runner.setup(Path.home() / ".showet", datadir, platform_found)
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
