"""Core module exports."""

from showet.core.config import (
    CACHE_DIR, DEBUG, DEFAULT_TIMEOUT, DEFAULT_LOOP_LIMIT, LOOPED_KEYWORDS,
    POUET_API_BASE, SCENE_ORG_API_BASE, MODARCHIVE_API_BASE,
)
from showet.core.platform_common import PlatformCommon
from showet.core.executor import execute_demo, detect_platform

__all__ = [
    "CACHE_DIR",
    "DEBUG",
    "DEFAULT_TIMEOUT",
    "DEFAULT_LOOP_LIMIT",
    "LOOPED_KEYWORDS",
    "POUET_API_BASE",
    "SCENE_ORG_API_BASE",
    "MODARCHIVE_API_BASE",
    "PlatformCommon",
    "execute_demo",
    "detect_platform",
]