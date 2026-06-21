"""Tests for RetroPie integration."""

import pytest
from pathlib import Path
from unittest.mock import patch


class TestPiDetection:
    """Tests for Raspberry Pi detection."""

    def test_detect_retropie_false(self):
        """Test RetroPie detection on non-RetroPie system."""
        from showet_retropie import detect_retropie
        
        with patch("showet_retropie.Path.exists", return_value=False):
            result = detect_retropie()
            assert result is False


class TestPiModel:
    """Tests for Pi model detection."""

    def test_get_pi_model_none(self):
        """Test model detection with no /proc/cpuinfo."""
        from showet_retropie import get_pi_model
        
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = get_pi_model()
            assert result is None


class TestGPUMemory:
    """Tests for GPU memory detection."""

    def test_get_gpu_memory_default(self):
        """Test GPU memory returns default on missing config."""
        from showet_retropie import get_gpu_memory
        
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = get_gpu_memory()
            assert result == 128


class TestOptimize:
    """Tests for Pi optimization."""

    def test_optimize_for_pi(self):
        """Test optimization recommendations."""
        from showet_retropie import optimize_for_pi
        
        with patch("showet_retropie.get_pi_model", return_value=None), \
             patch("showet_retropie.get_gpu_memory", return_value=128):
            recs = optimize_for_pi()
            assert "model" in recs
            assert "gpu_mem" in recs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])