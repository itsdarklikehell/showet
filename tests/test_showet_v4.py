"""Showet v4.0 Integration Tests - Core functionality tests."""

import tempfile
from pathlib import Path

import pytest


# Test package structure
class TestPackageStructure:
    """Test the new package structure is correct."""

    def test_package_init_exists(self):
        """Verify main package __init__.py exists."""
        assert Path("showet/__init__.py").exists()

    def test_core_package_exists(self):
        """Verify core package exists."""
        assert Path("showet/core/__init__.py").exists()
        assert Path("showet/core/config.py").exists()
        assert Path("showet/core/executor.py").exists()
        assert Path("showet/core/platform_common.py").exists()

    def test_integrations_package_exists(self):
        """Verify integrations package exists."""
        assert Path("showet/integrations/__init__.py").exists()
        assert Path("showet/integrations/pouet.py").exists()
        assert Path("showet/integrations/scene_org.py").exists()
        assert Path("showet/integrations/modarchive.py").exists()

    def test_utils_package_exists(self):
        """Verify utils package exists."""
        assert Path("showet/utils/__init__.py").exists()
        assert Path("showet/utils/archive_handler.py").exists()
        assert Path("showet/utils/stream_manager.py").exists()
        assert Path("showet/utils/async_io.py").exists()


# Test platform detection
class TestPlatformDetection:
    """Tests for platform auto-detection."""

    def test_detect_amiga(self):
        """Test Amiga detection from .adf extension."""
        from showet.core.executor import detect_platform
        assert detect_platform(Path("demo.adf")) == "amiga"

    def test_detect_c64(self):
        """Test C64 detection from .d64 extension."""
        from showet.core.executor import detect_platform
        assert detect_platform(Path("demo.d64")) == "commodore_64"

    def test_detect_nes(self):
        """Test NES detection from .nes extension."""
        from showet.core.executor import detect_platform
        assert detect_platform(Path("demo.nes")) == "nes"

    def test_detect_snes(self):
        """Test SNES detection from .sfc extension."""
        from showet.core.executor import detect_platform
        assert detect_platform(Path("demo.sfc")) == "snes"

    def test_detect_dos(self):
        """Test DOS detection from .exe extension."""
        from showet.core.executor import detect_platform
        assert detect_platform(Path("demo.exe")) == "dos"

    def test_detect_archive(self):
        """Test archive detection."""
        from showet.core.executor import detect_platform
        assert detect_platform(Path("demo.zip")) == "archive"
        assert detect_platform(Path("demo.lha")) == "archive"


# Test loop detection
class TestLoopDetection:
    """Tests for jukebox loop detection."""

    def test_looped_64k_demo(self):
        """Test 64k intros are detected as looping."""
        from showet.core.jukebox import is_looped_demo
        demo = {"type": "64k intro", "rating": 0}
        assert is_looped_demo(demo) is True

    def test_looped_4k_demo(self):
        """Test 4k intros are detected as looping."""
        from showet.core.jukebox import is_looped_demo
        demo = {"type": "4k", "rating": 0}
        assert is_looped_demo(demo) is True

    def test_looped_by_tag(self):
        """Test demos with loop tag are detected."""
        from showet.core.jukebox import is_looped_demo
        demo = {"type": "demo", "tags": "loop infinite endless"}
        assert is_looped_demo(demo) is True

    def test_high_rated_intro_loops(self):
        """Test high-rated intros are detected as looping."""
        from showet.core.jukebox import is_looped_demo
        demo = {"type": "intro", "rating": 4.5}
        assert is_looped_demo(demo) is True


# Test integrations
class TestPouetIntegration:
    """Tests for Pouet.net integration."""

    def test_pouet_client_class_exists(self):
        """Verify PouetClient exists."""
        from showet.integrations.pouet import PouetClient
        client = PouetClient()
        assert client.API_BASE == "http://api.pouet.net/v1"


class TestSceneOrgIntegration:
    """Tests for Scene.org integration."""

    def test_scene_org_client_exists(self):
        """Verify SceneOrgClient exists."""
        from showet.integrations.scene_org import SceneOrgClient
        client = SceneOrgClient()
        assert client.download_dir == "demos"


class TestModArchiveIntegration:
    """Tests for ModArchive.org integration."""

    def test_modarchive_client_exists(self):
        """Verify ModArchiveAPI exists."""
        from showet.integrations.modarchive import ModArchiveAPI
        api = ModArchiveAPI()
        assert api.cache_dir.name == "modarchive"


# Test archive handler
class TestArchiveHandler:
    """Tests for archive extraction."""

    def test_handler_class_exists(self):
        """Verify ArchiveHandler class exists."""
        from showet.utils.archive_handler import ArchiveHandler
        handler = ArchiveHandler()
        assert handler.work_dir is not None


# Test CLI
class TestCLI:
    """Tests for CLI interface."""

    def test_cli_parser_exists(self):
        """Verify CLI parser is created."""
        from showet.cli.main import create_main_parser
        parser = create_main_parser()
        assert parser is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])