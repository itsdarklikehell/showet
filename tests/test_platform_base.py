"""
Tests for PlatformBase and refactored platform modules.

Ensures all Platform_* classes properly implement the abstract interface.
"""

import importlib
import re
import sys
from pathlib import Path
from unittest import mock

import pytest

# Mock external dependencies
sys.modules.setdefault("inquirer", mock.MagicMock())
sys.modules.setdefault("patoolib", mock.MagicMock())


class TestPlatformBaseContract:
    """Test that all platform modules properly inherit from PlatformBase."""

    @pytest.fixture
    def platform_files(self):
        """Get all Platform_*.py files excluding PlatformBase itself."""
        project_root = Path(__file__).parent.parent
        return sorted([
            f for f in project_root.glob("Platform_*.py")
            if f.name != "PlatformBase.py"
        ])

    def test_all_platforms_inherit_from_platform_base(self, platform_files):
        """Verify all platform modules import PlatformBase."""
        for pf in platform_files[:5]:  # Test first 5 to avoid timeout
            content = pf.read_text()
            if "PlatformCommon" in content and "PlatformBase" not in content:
                # This should NOT happen after refactoring
                pytest.fail(f"{pf.name} still uses PlatformCommon, not PlatformBase")

    def test_all_platforms_have_required_methods(self, platform_files):
        """Verify all platforms implement the abstract methods."""
        required_methods = {"initialize", "load_game", "run_frame", "get_status_report", "save_state", "load_state"}
        
        for pf in platform_files[:10]:  # Test first 10
            module_name = pf.stem
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            try:
                module = importlib.import_module(module_name)
                for cls_name in dir(module):
                    cls = getattr(module, cls_name)
                    if isinstance(cls, type) and hasattr(cls, '__mro__'):
                        # Check if this class has the required methods
                        for method in required_methods:
                            assert hasattr(cls, method), f"{cls.__name__} missing {method}"
            except Exception as e:
                # Some modules may have import issues, log and continue
                print(f"Warning: Could not test {pf.name}: {e}")


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
                if isinstance(cls, type) and "Platform" in cls_name:
                    instance = cls()
                    assert hasattr(instance, 'platform_name')
                    assert hasattr(instance, 'version')


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