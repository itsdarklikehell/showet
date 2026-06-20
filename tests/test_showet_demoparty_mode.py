"""Tests for Showet Demoparty Mode."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the demoparty module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestPartyKeywords:
    """Tests for party keyword mappings."""

    def test_party_keywords_exist(self):
        """Verify party keywords are defined."""
        from showet_demoparty_mode import PARTY_KEYWORDS
        assert "assembly" in PARTY_KEYWORDS
        assert "revision" in PARTY_KEYWORDS

    def test_party_keywords_values(self):
        """Test party keyword values."""
        from showet_demoparty_mode import PARTY_KEYWORDS
        assert PARTY_KEYWORDS["assembly"] == "assembly"


class TestPouetPartySearch:
    """Tests for Pouet party search."""

    def test_search_pouet_party_structure(self):
        """Test search returns list of demos."""
        from showet_demoparty_mode import search_pouet_party
        
        with patch("showet_demoparty_mode.urllib.request") as mock_req:
            mock_req.urlopen.return_value.__enter__ = MagicMock()
            mock_req.urlopen.return_value.__enter__.return_value.read.return_value = b'{"prods": []}'
            
            results = search_pouet_party("assembly")
            assert isinstance(results, list)


class TestSceneOrgPartySearch:
    """Tests for Scene.org party search."""

    def test_search_party_demos(self):
        """Test party demo search."""
        from showet_demoparty_mode import search_party_demos
        
        with patch("showet_demoparty_mode.SceneOrgClient") as mock_client:
            mock_instance = MagicMock()
            mock_instance.search_demos.return_value = [
                {"name": "demo.zip", "url": "http://example.com/demo.zip", "size": 1000}
            ]
            mock_client.return_value = mock_instance
            
            results = search_party_demos("assembly")
            assert len(results) > 0


class TestDemopartyWatch:
    """Tests for demoparty watch mode."""

    def test_demoparty_watch_no_results(self):
        """Test demoparty watch with no results."""
        from showet_demoparty_mode import demoparty_watch
        
        with patch("showet_demoparty_mode.search_party_demos") as mock_search:
            mock_search.return_value = []
            
            result = demoparty_watch("unknown_party")
            assert result == 0

    def test_demoparty_watch_with_results(self):
        """Test demoparty watch with results."""
        from showet_demoparty_mode import demoparty_watch
        
        with patch("showet_demoparty_mode.search_party_demos") as mock_search:
            mock_search.return_value = [
                {"id": 123, "name": "Demo", "source": "pouet"}
            ]
            with patch("showet_demoparty_mode.subprocess.run"):
                result = demoparty_watch("assembly")
                assert result > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])