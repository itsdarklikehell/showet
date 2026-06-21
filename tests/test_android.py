"""Tests for Android integration."""

import pytest
from unittest.mock import patch


class TestAndroidDetection:
    """Tests for Android SDK detection."""

    def test_detect_android_sdk_false(self):
        """Test Android SDK detection when not present."""
        from showet_android import get_android_devices
        
        devices = get_android_devices()
        # Should return empty list when no SDK
        assert isinstance(devices, list)


class TestEmulatorConfig:
    """Tests for emulator configuration."""

    def test_get_emulator_package_invalid(self):
        """Test getting invalid emulator config."""
        from showet_android import get_emulator_package
        
        result = get_emulator_package("invalid")
        assert result is None

    def test_get_emulator_package_valid(self):
        """Test getting valid emulator config."""
        from showet_android import get_emulator_package
        
        result = get_emulator_package("dolphin")
        assert result is not None
        assert result["name"] == "Dolphin"


class TestMobileHTML:
    """Tests for mobile HTML generation."""

    def test_generate_mobile_html(self):
        """Test HTML generation for demos."""
        from showet_android import generate_mobile_html
        
        demos = [{"id": "123", "title": "Test Demo"}]
        html = generate_mobile_html(demos)
        
        assert "<!DOCTYPE html>" in html
        assert "Test Demo" in html
        assert "playDemo" in html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])