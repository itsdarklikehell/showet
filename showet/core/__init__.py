"""Core module exports."""

from showet.core.config import (
    CACHE_DIR,
    DEBUG,
    DEFAULT_LOOP_LIMIT,
    DEFAULT_TIMEOUT,
    LOOPED_KEYWORDS,
    MODARCHIVE_API_BASE,
    POUET_API_BASE,
    SCENE_ORG_API_BASE,
)
from showet.core.executor import detect_platform, execute_demo
from showet.core.platform_common import PlatformCommon

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