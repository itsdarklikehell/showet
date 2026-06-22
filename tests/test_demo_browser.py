"""Tests for showet demo browser API."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestPlatformConfigs:
    """Tests for platform config loading."""

    def test_get_platform_configs_empty(self):
        """Test get_platform_configs with no config directory."""
        from showet_demo_browser import get_platform_configs
        
        with patch("showet_demo_browser.Path.exists", return_value=False):
            result = get_platform_configs()
            assert result == []


class TestSearchDemos:
    """Tests for demo search functionality."""

    def test_search_demos_empty(self):
        """Test search with no cached demos."""
        from showet_demo_browser import search_demos
        
        with patch("showet_demo_browser.get_cached_demos", return_value=[]):
            result = search_demos("test")
            assert result == []

    def test_search_demos_no_match(self):
        """Test search with no matching demos."""
        from showet_demo_browser import search_demos
        
        with patch("showet_demo_browser.get_cached_demos", return_value=[
            {"title": "Some Demo", "platform": "c64"}
        ]):
            result = search_demos("amiga")
            assert result == []


class TestFastAPIAvailability:
    """Tests for FastAPI conditional import."""

    def test_app_exists(self):
        """Test that app module loaded."""
        from showet_demo_browser import app
        # App may be None if FastAPI not installed
        assert app is None or hasattr(app, 'get')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])