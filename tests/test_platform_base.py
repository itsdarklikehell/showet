"""Tests for Showet platform base classes and integrations."""

import importlib
import sys
from pathlib import Path
from unittest.mock import patch

import pytest


class TestPlatformInstantiation:
    """Test that platform classes can be instantiated."""

    @pytest.fixture
    def sample_platforms(self):
        """Get a few sample platform modules for testing."""
        return ["Platform_Nintendo_Famicom", "Platform_Atari_2600", "Platform_Commodore_64"]

    def test_platform_classes_instantiate(self, sample_platforms):
        """Verify platform classes can be created without error."""
        for module_name in sample_platforms:
            if module_name in sys.modules:
                del sys.modules[module_name]

            module = importlib.import_module(module_name)
            for cls_name in dir(module):
                cls = getattr(module, cls_name)
                if isinstance(cls, type) and "Platform" in cls_name and not getattr(cls, '__abstractmethods__', None):
                    instance = cls()
                    assert hasattr(instance, 'platform_name')
                    assert hasattr(instance, 'version')


class TestPlatformBaseMethods:
    """Test PlatformBase abstract class functionality."""

    def test_base_has_is_initialized(self):
        """Verify PlatformBase has is_initialized method."""
        from PlatformBase import PlatformBase
        # PlatformBase is abstract, check the method exists on the class
        assert hasattr(PlatformBase, 'is_initialized')

    def test_platform_has_run_method(self):
        """Verify platforms inherit run method from PlatformBase."""
        from Platform_Commodore_64 import Platform_Commodore_64
        platform = Platform_Commodore_64()
        assert hasattr(platform, 'run')
        assert callable(platform.run)


class TestNostalgistBridge:
    """Tests for nostalgist_bridge.py."""

    def test_core_mapping_covers_common_cores(self):
        """Verify core mapping has entries for common RetroArch cores."""
        from nostalgist_bridge import CORE_MAPPING

        # Check some key mappings exist
        assert "quicknes_libretro" in CORE_MAPPING
        assert "genesis_plus_gx_libretro" in CORE_MAPPING
        assert "vice_x64sc_libretro" in CORE_MAPPING

    def test_generate_config_returns_required_fields(self):
        """Verify generated configs have the required fields."""
        from nostalgist_bridge import generate_nostalgist_config

        config = generate_nostalgist_config(
            platform_slug="nesfamicom",
            rom_path="https://example.com/game.nes",
            core_name="quicknes_libretro"
        )

        assert "core" in config
        assert "rom" in config
        assert config["core"] == "quicknes"
        assert config["rom"] == "https://example.com/game.nes"

    def test_shader_inference_from_platform_slug(self):
        """Verify shader is inferred from platform slug."""
        from nostalgist_bridge import generate_nostalgist_config

        config = generate_nostalgist_config(
            platform_slug="superfamicom",
            rom_path="/rom.sfc",
            core_name="snes9x_libretro"
        )

        assert "shader" in config

    def test_parse_platform_module_extracts_slug(self):
        """Verify parse_platform_module extracts platform info."""
        from nostalgist_bridge import parse_platform_module
        
        # Get the actual file path
        platform_file = Path(__file__).parent.parent / "Platform_Commodore_64.py"
        info = parse_platform_module(platform_file)

        assert info is not None
        assert info["slug"] == "commodore_64"
        assert "vice_x64sc_libretro" in info["core"]


class TestRetroEffects:
    """Tests for retro_effects.py CRT presets."""

    def test_get_preset_returns_valid_preset(self):
        """Verify get_preset returns a valid preset for known platforms."""
        from retro_effects import get_preset
        
        preset = get_preset("commodore_64")
        assert preset is not None
        assert "shader" in preset
        assert preset["shader"] in ["crt/crt-easymode", "crt/crt-royale", "crt/crt-pi"]

    def test_generate_shader_config_returns_full_config(self):
        """Verify generate_shader_config returns complete config."""
        from retro_effects import generate_shader_config

        config = generate_shader_config("commodore_64")

        assert "shader" in config
        assert "parameters" in config
        assert "scanline_intensity" in config["parameters"]

    def test_crt_presets_have_required_fields(self):
        """Verify all CRT presets have required fields."""
        from retro_effects import CRT_PRESETS

        for preset_name, preset in CRT_PRESETS.items():
            assert "name" in preset, f"{preset_name} missing name"
            assert "shader" in preset, f"{preset_name} missing shader"
            assert "scanline_intensity" in preset, f"{preset_name} missing scanline_intensity"


class TestDemoDatabase:
    """Tests for demo_database.py."""

    def test_get_db_returns_singleton(self):
        """Verify get_db returns a singleton DemoDatabase instance."""
        from demo_database import DemoDatabase, get_db
        
        db1 = get_db()
        db2 = get_db()

        assert db1 is db2
        assert isinstance(db1, DemoDatabase)

    def test_search_demos_returns_list(self, tmp_path, monkeypatch):
        """Verify search_demos returns a list (empty on mock failure)."""
        from demo_database import DemoDatabase

        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        db = DemoDatabase()

        # Search without network should return empty list
        results = db.search_demos("test")
        assert isinstance(results, list)

    def test_create_playlist_returns_id(self, tmp_path, monkeypatch):
        """Verify create_playlist returns an ID."""
        from demo_database import DemoDatabase

        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        db = DemoDatabase()
        playlist_id = db.create_playlist("test_playlist", [123, 456])

        assert playlist_id is not None
        assert len(playlist_id) > 0


class TestShowetAPI:
    """Tests for showet_api.py."""

    def test_api_singleton(self):
        """Verify API singleton works correctly."""
        from showet_api import ShowetAPI, get_api
        
        api1 = get_api()
        api2 = get_api()

        assert api1 is api2
        assert isinstance(api1, ShowetAPI)

    def test_api_list_platforms(self):
        """Verify API can list platforms."""
        from showet_api import ShowetAPI

        api = ShowetAPI()
        platforms = api.list_platforms()

        assert isinstance(platforms, list)
        assert len(platforms) > 0
        # Check that commodore_64 is in the list
        assert "commodore_64" in platforms

    def test_api_get_status(self):
        """Verify API status check works."""
        from showet_api import ShowetAPI

        api = ShowetAPI()
        status = api.get_status()

        assert "platforms_loaded" in status
        assert "version" in status


class TestLauncher:
    """Tests for launcher.py."""

    def test_launcher_crt_presets(self):
        """Verify launcher can list CRT presets."""
        from launcher import DemoLauncher
        
        launcher = DemoLauncher()
        preset = launcher.get_crt_preset("commodore_64")

        assert preset is not None
        assert "name" in preset


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
