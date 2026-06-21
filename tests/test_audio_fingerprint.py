"""Tests for audio fingerprinting module."""

import pytest
from pathlib import Path


class TestModuleDetection:
    """Tests for module format detection."""

    def test_detect_unknown_format(self, tmp_path):
        """Test detection with non-module file."""
        from showet_audio_fingerprint import detect_module_format
        
        fake_mod = tmp_path / "notamod.txt"
        fake_mod.write_bytes(b"This is not a module file")
        
        result = detect_module_format(str(fake_mod))
        assert result["format"] == "unknown"
        assert result["confidence"] == 0

    def test_detect_small_file(self, tmp_path):
        """Test detection rejects too-small files."""
        from showet_audio_fingerprint import detect_module_format
        
        tiny = tmp_path / "tiny.bin"
        tiny.write_bytes(b"M.K.")
        
        result = detect_module_format(str(tiny))
        assert result["format"] == "unknown"


class TestLoopPatterns:
    """Tests for loop pattern analysis."""

    def test_analyze_missing_file(self):
        """Test analysis with missing file."""
        from showet_audio_fingerprint import analyze_loop_points
        
        result = analyze_loop_points("/nonexistent/file.mod", "protracker")
        assert result == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])