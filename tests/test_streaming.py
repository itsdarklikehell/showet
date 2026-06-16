#!/usr/bin/env python3
"""Tests for the streaming module."""

import pytest
from streaming import (
    StreamManager,
    StreamConfig,
    StreamPlatform,
    QUALITY_PRESETS,
    get_stream_key,
    setup_stream_key,
)
from pathlib import Path


class TestStreamConfig:
    """Tests for StreamConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = StreamConfig()
        assert config.platform == StreamPlatform.TWITCH
        assert config.quality == "720p"
        assert config.include_audio is True
        assert config.include_webcam is False

    def test_custom_config(self):
        """Test custom configuration."""
        config = StreamConfig(
            platform=StreamPlatform.YOUTUBE,
            stream_key="test_key",
            quality="1080p",
            include_webcam=True,
        )
        assert config.platform == StreamPlatform.YOUTUBE
        assert config.stream_key == "test_key"
        assert config.quality == "1080p"
        assert config.include_webcam is True


class TestStreamManager:
    """Tests for StreamManager class."""

    def test_build_ffmpeg_command(self, tmp_path):
        """Test FFmpeg command building."""
        config = StreamConfig(
            platform=StreamPlatform.TWITCH,
            stream_key="test123",
            quality="720p",
        )
        manager = StreamManager()
        manager.configure(config)

        cmd = manager._build_ffmpeg_command()
        assert "ffmpeg" in cmd
        assert "libx264" in cmd
        assert "flv" in cmd

    def test_build_ffmpeg_command_1080p(self, tmp_path):
        """Test FFmpeg command with 1080p quality."""
        config = StreamConfig(quality="1080p")
        manager = StreamManager()
        manager.configure(config)

        cmd = manager._build_ffmpeg_command()
        assert "1920x1080" in cmd
        assert "4500k" in cmd

    def test_rtsp_url(self):
        """Test RTSP URL generation."""
        config = StreamConfig(platform=StreamPlatform.RTSP)
        manager = StreamManager()
        manager.configure(config)

        url = manager._get_stream_url()
        assert "rtsp://0.0.0.0:8554/showet" == url

    def test_twitch_url(self):
        """Test Twitch URL generation."""
        config = StreamConfig(platform=StreamPlatform.TWITCH, stream_key="abc123")
        manager = StreamManager()
        manager.configure(config)

        url = manager._get_stream_url()
        assert "rtmp://live.twitch.tv/app/abc123" == url

    def test_youtube_url(self):
        """Test YouTube URL generation."""
        config = StreamConfig(platform=StreamPlatform.YOUTUBE, stream_key="xyz789")
        manager = StreamManager()
        manager.configure(config)

        url = manager._get_stream_url()
        assert "rtmp://a.rtmp.youtube.com/live2/xyz789" == url

    def test_get_status(self):
        """Test status reporting."""
        config = StreamConfig(quality="1080p", include_webcam=True)
        manager = StreamManager()
        manager.configure(config)

        status = manager.get_status()
        assert status["streaming"] is False
        assert status["quality"] == "1080p"
        assert status["has_webcam"] is True


class TestQualityPresets:
    """Tests for quality presets."""

    def test_preset_exists(self):
        """Test all presets are defined."""
        assert "480p" in QUALITY_PRESETS
        assert "720p" in QUALITY_PRESETS
        assert "1080p" in QUALITY_PRESETS

    def test_preset_resolution(self):
        """Test preset resolutions."""
        assert QUALITY_PRESETS["720p"]["resolution"] == "1280x720"
        assert QUALITY_PRESETS["1080p"]["resolution"] == "1920x1080"


class TestStreamKeyManagement:
    """Tests for stream key storage."""

    def test_setup_stream_key(self, tmp_path, monkeypatch):
        """Test saving stream key."""
        monkeypatch.setattr(Path, "home", lambda: tmp_path)

        setup_stream_key("twitch", "abc123")

        key_file = tmp_path / ".showet" / "twitch_stream_key"
        assert key_file.exists()
        assert key_file.read_text() == "abc123"

    def test_get_stream_key_existing(self, tmp_path, monkeypatch):
        """Test retrieving existing stream key."""
        monkeypatch.setattr(Path, "home", lambda: tmp_path)

        key_file = tmp_path / ".showet"
        key_file.mkdir(parents=True)
        (key_file / "twitch_stream_key").write_text("stored_key")

        retrieved = get_stream_key("twitch")
        assert retrieved == "stored_key"

    def test_get_stream_key_missing(self, tmp_path, monkeypatch):
        """Test retrieving missing stream key."""
        monkeypatch.setattr(Path, "home", lambda: tmp_path)

        retrieved = get_stream_key("twitch")
        assert retrieved == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])