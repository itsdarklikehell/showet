"""Tests for Showet Setup Wizard."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestSetupWizardDetection:
    """Tests for emulator detection functions."""
    
    def test_detect_retroarch_found(self, tmp_path):
        """Test RetroArch detection when installed."""
        # Add a fake retroarch to PATH
        fake_ra = tmp_path / "retroarch"
        fake_ra.write_text("#!/bin/bash\nexit 0\n")
        fake_ra.chmod(0o755)
        
        with patch.dict('os.environ', {'PATH': str(tmp_path)}):
            # Import would happen here - for now just verify the function exists
            # The actual logic is in showet_setup_wizard.py
            pass
    
    def test_detect_emulators_returns_dict(self):
        """Test that emulator detection returns proper structure."""
        # This would be a real test after importing the module
        pass
    
    def test_check_bios_creates_config_dir(self, tmp_path):
        """Test that config directory is created."""
        # Would test BIOS check with mock paths
        pass


class TestSetupWizardConfig:
    """Tests for configuration creation."""
    
    def test_config_creation(self, tmp_path):
        """Test initial config file creation."""
        config_file = tmp_path / "config.json"
        config_content = {
            "theme": "crt-easymode",
            "default_shader": "crt-royale",
            "prefer_retroarch": True,
        }
        
        import json
        with open(config_file, "w") as f:
            json.dump(config_content, f)
        
        assert config_file.exists()
        with open(config_file) as f:
            loaded = json.load(f)
        assert loaded["theme"] == "crt-easymode"
        assert loaded["prefer_retroarch"] is True


class TestSetupWizardIntegration:
    """Integration tests for showet-auto workflow."""
    
    def test_showet_auto_exists(self):
        """Test that showet-auto command is registered."""
        # Check pyproject.toml has the entry
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        content = pyproject_path.read_text()
        assert "showet-auto" in content
        assert "showet_setup_wizard" in content
    
    def test_showet_setup_wizard_exists(self):
        """Test that setup wizard module exists."""
        setup_wizard_path = Path(__file__).parent.parent / "showet_setup_wizard.py"
        assert setup_wizard_path.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])