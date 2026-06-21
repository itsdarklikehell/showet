"""Showet Demoscene Demo Runner - v4.0

The definitive, immersive demo-runner for the demoscene with nostalgic flair.
"""

__version__ = "4.0.0-dev"
__author__ = "SgtStroopwafel"

# Import from legacy showet.py for backward compatibility
import importlib.util
import sys
from pathlib import Path

_legacy_showet_path = Path(__file__).parent.parent / "showet.py"
_spec = importlib.util.spec_from_file_location("showet_legacy", _legacy_showet_path)
_legacy = importlib.util.module_from_spec(_spec)
sys.modules["showet_legacy"] = _legacy
_spec.loader.exec_module(_legacy)

from showet.core import (
    CACHE_DIR, DEBUG, DEFAULT_TIMEOUT,
    execute_demo, detect_platform,
)
from showet.integrations import (
    PouetClient, SceneOrgClient, ModArchiveAPI,
)
from showet.utils import (
    ArchiveHandler, StreamManager, AsyncDownloader, DemoCache,
)
from showet.platforms import load_all_platforms as create_platform_runners

# Forward legacy module functions
build_arg_parser = _legacy.build_arg_parser
run_production = _legacy.run_production
main = _legacy.main
_select_runner = _legacy._select_runner
download_production_json = _legacy.download_production_json

__all__ = [
    "__version__",
    "__author__",
    "CACHE_DIR",
    "DEBUG",
    "DEFAULT_TIMEOUT",
    "execute_demo",
    "detect_platform",
    "PouetClient",
    "SceneOrgClient",
    "ModArchiveAPI",
    "ArchiveHandler",
    "StreamManager",
    "AsyncDownloader",
    "DemoCache",
    "create_platform_runners",
    "build_arg_parser",
    "run_production",
    "main",
]