"""Tests for the Showet local demo database (recommendations + party demos)."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from demo_database import PARTY_HISTORY, DemoDatabase  # noqa: E402


@pytest.fixture
def temp_db(tmp_path):
    """Provide an isolated DemoDatabase backed by a temp file."""
    return DemoDatabase(db_path=tmp_path / "demo_db.json")


class TestRecommendations:
    """Tests for get_recommendations (offline, local-data based)."""

    def test_empty_db_returns_empty(self, temp_db):
        """No favorites or history means no recommendations."""
        assert temp_db.get_recommendations() == []

    def test_favorites_ranked_first(self, temp_db):
        """Favorited demos should be recommended and ranked above history."""
        temp_db.add_favorite(100, tags=["c64"], score=5)
        temp_db.add_history(200, "amiga", score=3)
        recs = temp_db.get_recommendations()
        assert recs[0] == 100
        assert 100 in recs and 200 in recs

    def test_respects_limit(self, temp_db):
        """Recommendation count should not exceed the requested limit."""
        for pid in range(1, 15):
            temp_db.add_favorite(pid)
        assert len(temp_db.get_recommendations(limit=3)) == 3

    def test_no_duplicates(self, temp_db):
        """A demo that is both favorited and in history appears once."""
        temp_db.add_favorite(42)
        temp_db.add_history(42, "c64")
        recs = temp_db.get_recommendations()
        assert recs.count(42) == 1

    def test_party_history_fallback(self, temp_db):
        """With no local data, party history anchors suggestions offline."""
        fake_party_demo = {
            "id": 999,
            "name": "Test Demo",
            "type": "",
            "party": "",
            "score": 0,
        }
        with patch.object(temp_db, "search_by_party", return_value=[fake_party_demo]):
            recs = temp_db.get_recommendations()
        assert 999 in recs


class TestPartyDemos:
    """Tests for get_party_demos."""

    def test_returns_ids_from_search(self, temp_db):
        """Party demos should map search results to a list of IDs."""
        fake = [
            {"id": 11, "name": "A", "type": "", "party": "", "score": 0},
            {"id": 22, "name": "B", "type": "", "party": "", "score": 0},
        ]
        with patch.object(temp_db, "search_by_party", return_value=fake):
            result = temp_db.get_party_demos("assembly")
        assert result == [11, 22]

    def test_known_parties_exist(self, temp_db):
        """Sanity check that the party history table is populated."""
        assert "assembly" in PARTY_HISTORY
        assert "revision" in PARTY_HISTORY


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
