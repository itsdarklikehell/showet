#!/usr/bin/env python3
"""Tests for ML Paper Reading List."""

import pytest
from showet_ml_papers import MLPaperTracker, MLPaper


class TestMLPaperTracker:
    """Tests for MLPaperTracker."""

    def test_tracker_init(self):
        """Test tracker initialization."""
        tracker = MLPaperTracker()
        assert tracker.cache_dir.exists() or tracker.cache_dir.parent.exists()

    def test_paper_dataclass(self):
        """Test MLPaper dataclass creation."""
        paper = MLPaper(
            title="Test Paper",
            authors=["Author One", "Author Two"],
            summary="Test summary",
            published="2026-01-01",
            arxiv_id="1234.5678",
            score=0.5,
        )
        assert paper.title == "Test Paper"
        assert len(paper.authors) == 2

    def test_extract_github(self):
        """Test GitHub URL extraction."""
        tracker = MLPaperTracker()
        assert tracker._extract_github("Check github.com/user/repo for code") == "https://github.com/user/repo"
        assert tracker._extract_github("No repo here") is None

    def test_score_for_demos(self):
        """Test demo relevance scoring."""
        tracker = MLPaperTracker()
        # Text with demo keywords
        score = tracker._score_for_demos("real-time interactive generative graphics")
        assert score > 0.3

        # Text without keywords
        score = tracker._score_for_demos("statistical analysis methods")
        assert score == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])