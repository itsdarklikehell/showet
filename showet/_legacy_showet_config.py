#!/usr/bin/env python3
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
    "loop", "looping", "infinite", "64k", "4k", "intro"
])

# Supported archive extensions
ARCHIVE_EXTENSIONS: Final = frozenset([".zip", ".rar", ".7z", ".lha", ".lzh"])