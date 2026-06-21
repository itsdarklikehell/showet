"""Showet configuration module.

Centralized configuration for API endpoints, settings, and constants.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

# API Configuration
POUET_API_BASE: Final = os.environ.get(
    "SHOWET_POUET_API_BASE", "http://api.pouet.net/v1"
)
SCENE_ORG_API_BASE: Final = os.environ.get(
    "SHOWET_SCENE_ORG_API_BASE", "https://archive.scene.org"
)
MODARCHIVE_API_BASE: Final = os.environ.get(
    "SHOWET_MODARCHIVE_API_BASE", "https://modarchive.org"
)

# Cache directories
SHOWET_DIR: Final = Path.home() / ".showet"
CACHE_DIR: Final = SHOWET_DIR / "data"
DOWNLOAD_DIR: Final = SHOWET_DIR / "downloads"
LOGS_DIR: Final = SHOWET_DIR / "logs"

# Default settings
DEBUG: Final = os.environ.get("SHOWET_DEBUG", "false").lower() in ("true", "1", "yes")
DEFAULT_TIMEOUT: Final = int(os.environ.get("SHOWET_TIMEOUT", "300"))
DEFAULT_LOOP_LIMIT: Final = int(os.environ.get("SHOWET_LOOP_LIMIT", "3"))

# Loop detection keywords
LOOPED_KEYWORDS: Final = frozenset([
    "loop", "looping", "infinite", "64k", "4k", "intro", "cracktro", "dentro"
])

# Extended loop indicators
LOOP_PATTERNS: Final = frozenset([
    "loop", "endless", "forever", "replay", "continuous", "eternal",
    "repeat", "cyclic", "cycle", "oscillating"
])

# Common demoparty names known for looped intros (Assembly, Breakpoint, etc.)
PARTY_LOOP_INCENTIVE: Final = frozenset([
    "assembly", "breakpoint", "revision", "evoke", "forever", "spring",
    "silly", "csdb", "pouet"
])

# Platform-specific loop tendency (some platforms favor looping demos)
PLATFORM_LOOP_TENDENCY: Final = {
    "commodore_64": 0.7,   # C64 demos often loop
    "commodore_amiga": 0.6, # Amiga intros commonly loop
    "nintendo_famicom": 0.5, # NES has looping intros
    "nintendo_gameboy": 0.4, # GB has some looped intros
    "zx_spectrum": 0.6,    # ZX has many cracktros
    "atari": 0.5,          # Atari intros loop
}

# Supported archive extensions
ARCHIVE_EXTENSIONS: Final = frozenset([".zip", ".rar", ".7z", ".lha", ".lzh"])

# Platform categories
PLATFORM_CATEGORIES: Final = {
    "home_computers": [
        "commodore_64", "commodore_128", "commodore_amiga", "commodore_vic20",
        "apple_ii", "apple_iigs", "atari_8bit", "zx_spectrum", "amstrad_cpc",
    ],
    "gaming_consoles": [
        "nes", "snes", "megadrive", "mastersystem", "gamegear", "gameboy",
        "gameboycolor", "gameboyadvance", "atari_2600", "atari_7800",
    ],
    "arcade": ["mame", "arcade"],
}