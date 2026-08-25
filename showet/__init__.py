"""Showet Demoscene Demo Runner - v4.0

The definitive, immersive demo-runner for the demoscene with nostalgic flair.
"""

__version__ = "4.0.0-dev"
__author__ = "SgtStroopwafel"

# Import from legacy showet.py for backward compatibility
import importlib.util
import sys
from pathlib import Path


def _load_legacy_showet():
    """Load the vendored legacy showet module (showet/_legacy_showet.py)."""
    spec = importlib.util.spec_from_file_location(
        "showet_legacy",
        Path(__file__).parent / "_legacy_showet.py",
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["showet_legacy"] = module
    spec.loader.exec_module(module)
    return module


_legacy = _load_legacy_showet()

from showet.core import (  # noqa: E402
    CACHE_DIR,
    DEBUG,
    DEFAULT_TIMEOUT,
    detect_platform,
    execute_demo,
)
from showet.integrations import (  # noqa: E402
    ModArchiveAPI,
    PouetClient,
    SceneOrgClient,
)
from showet.platforms import load_all_platforms as create_platform_runners  # noqa: E402
from showet.utils import (  # noqa: E402
    ArchiveHandler,
    AsyncDownloader,
    DemoCache,
    StreamManager,
)

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