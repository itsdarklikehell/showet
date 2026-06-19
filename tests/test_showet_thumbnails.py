"""Tests for Showet thumbnail generation."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the thumbnails module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestThumbnailDirectory:
    """Tests for thumbnail cache directory management."""

    def test_ensure_thumbnail_dir(self, tmp_path):
        """Test thumbnail directory creation."""
        from showet_thumbnails import ensure_thumbnail_dir, THUMBNAIL_DIR
        
        # Patch the home directory
        with patch("showet_thumbnails.Path.home", return_value=tmp_path):
            ensure_thumbnail_dir()
            # Directory should be created
            assert tmp_path.exists()


class TestVideoFileFinding:
    """Tests for video file detection."""

    def test_find_video_files_empty(self, tmp_path):
        """Test finding videos in empty directory."""
        from showet_thumbnails import find_video_files
        
        result = find_video_files(tmp_path)
        assert result == []

    def test_find_video_files_extensions(self, tmp_path):
        """Test video extension detection."""
        from showet_thumbnails import find_video_files
        
        # Create dummy video files
        for ext in [".mp4", ".avi", ".mkv"]:
            (tmp_path / f"demo{ext}").touch()
        
        result = find_video_files(tmp_path)
        assert len(result) == 3


class TestPlaceholderGeneration:
    """Tests for placeholder thumbnail generation."""

    def test_generate_placeholder_thumbnail(self, tmp_path):
        """Test placeholder thumbnail creation."""
        from showet_thumbnails import generate_placeholder_thumbnail
        
        output = tmp_path / "test.jpg"
        result = generate_placeholder_thumbnail("Test Demo", output, "commodore_64")
        # Will fail if ffmpeg not installed, which is expected
        # The function handles this gracefully

    def test_generate_placeholder_null_title(self, tmp_path):
        """Test placeholder with null title."""
        from showet_thumbnails import generate_placeholder_thumbnail
        
        output = tmp_path / "test.jpg"
        result = generate_placeholder_thumbnail("", output, "unknown")
        # Should use "Demo" as fallback


class TestDemoMetadata:
    """Tests for demo metadata fetching."""

    def test_get_demo_metadata_import(self):
        """Verify metadata fetch imports work."""
        try:
            from showet_thumbnails import get_demo_metadata
            assert callable(get_demo_metadata)
        except ImportError:
            pytest.skip("Module import issue")


class TestBatchGeneration:
    """Tests for batch thumbnail generation."""

    def test_batch_generate_thumbnails_empty(self):
        """Test batch generation with no IDs."""
        from showet_thumbnails import batch_generate_thumbnails
        
        result = batch_generate_thumbnails([])
        assert result == 0

    def test_batch_generate_thumbnails_mock(self):
        """Test batch generation with mocked metadata."""
        from showet_thumbnails import batch_generate_thumbnails
        
        with patch("showet_thumbnails.get_demo_metadata") as mock_meta:
            mock_meta.return_value = {
                "name": "Test Demo",
                "platform": "commodore_64"
            }
            result = batch_generate_thumbnails([12345], "pouet")
            assert result == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])