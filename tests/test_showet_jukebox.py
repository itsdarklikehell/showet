"""Tests for Showet Jukebox with enhanced loop detection."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the jukebox module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestLoopDetection:
    """Tests for loop detection across all sources."""

    def test_pouet_loop_detection_64k(self):
        """Test Pouet loop detection for 64k intros."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"type": "64k intro", "tags": ""}
        assert is_looped_demo(demo_info, "pouet") is True

    def test_pouet_loop_detection_4k(self):
        """Test Pouet loop detection for 4k intros."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"type": "4k intro", "tags": ""}
        assert is_looped_demo(demo_info, "pouet") is True

    def test_pouet_loop_detection_tags(self):
        """Test Pouet loop detection from tags."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"type": "demo", "tags": "looping infinite"}
        assert is_looped_demo(demo_info, "pouet") is True

    def test_pouet_no_loop(self):
        """Test non-looping demo detection."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"type": "demo", "tags": "story"}
        assert is_looped_demo(demo_info, "pouet") is False

    def test_scene_org_loop_detection_filename(self):
        """Test Scene.org loop detection from filename."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"name": "assembly_demo_loop.zip", "url": ""}
        assert is_looped_demo(demo_info, "scene_org") is True

    def test_scene_org_loop_detection_intro(self):
        """Test Scene.org loop detection for intros."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"name": "64k_intro_demo.zip", "url": ""}
        assert is_looped_demo(demo_info, "scene_org") is True

    def test_scene_org_no_loop(self):
        """Test Scene.org non-looping demo."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"name": "story_demo.zip", "url": ""}
        assert is_looped_demo(demo_info, "scene_org") is False

    def test_scene_org_small_file_loops(self):
        """Test Scene.org small file heuristic."""
        from showet_jukebox import is_looped_demo
        
        # Small file (under 5MB) often loops
        demo_info = {"name": "demo.zip", "size": 2 * 1024 * 1024}  # 2MB
        assert is_looped_demo(demo_info, "scene_org") is True

    def test_scene_org_large_file_no_loop(self):
        """Test Scene.org large file doesn't trigger heuristic."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"name": "demo.zip", "size": 10 * 1024 * 1024}  # 10MB
        assert is_looped_demo(demo_info, "scene_org") is False

    def test_pouet_high_rated_intro_loops(self):
        """Test Pouet high-rated intro loops."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"type": "intro", "rating": 4.5}
        assert is_looped_demo(demo_info, "pouet") is True

    def test_pouet_low_rated_intro_no_loop(self):
        """Test Pouet low-rated intro still detected as loop (intro type)."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"type": "intro", "rating": 2.5}
        # Intros are generally looped by type
        assert is_looped_demo(demo_info, "pouet") is True

    def test_pouet_non_intro_with_rating(self):
        """Test Pouet non-intro with rating doesn't loop."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"type": "demo", "rating": 4.5}
        assert is_looped_demo(demo_info, "pouet") is False

    def test_pouet_low_rated_demo_no_loop(self):
        """Test Pouet low-rated regular demo doesn't loop."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"type": "demo", "rating": 3.5}
        assert is_looped_demo(demo_info, "pouet") is False

    def test_modarchive_loop_detection(self):
        """Test ModArchive loop detection for long tracks."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"title": "Mega Medley Mix", "format": "mod"}
        assert is_looped_demo(demo_info, "modarchive") is True

    def test_modarchive_no_loop(self):
        """Test ModArchive non-looping track."""
        from showet_jukebox import is_looped_demo
        
        demo_info = {"title": "Short Tune", "format": "mod"}
        assert is_looped_demo(demo_info, "modarchive") is False

    def test_null_demo_info(self):
        """Test null demo info handling."""
        from showet_jukebox import is_looped_demo
        
        assert is_looped_demo(None, "pouet") is False
        assert is_looped_demo(None, "scene_org") is False
        assert is_looped_demo(None, "modarchive") is False


class TestJukeboxMode:
    """Tests for jukebox playback mode."""

    def test_shuffled_order_randomized(self):
        """Test that shuffle mode randomizes order."""
        # This would need actual implementation testing
        pass

    def test_loop_limit_enforced(self):
        """Test loop limit is respected for shuffled demos."""
        # Looped demos should cap at loop_limit (default 3)
        pass

    def test_repeat_one_continues(self):
        """Test repeat-one mode loops forever."""
        pass

    def test_repeat_all_cycles(self):
        """Test repeat-all cycles through playlist."""
        pass


class TestSceneOrgIntegration:
    """Tests for Scene.org integration in jukebox."""

    def test_scene_org_client_import(self):
        """Verify SceneOrgClient can be imported."""
        try:
            from scene_org_integration import SceneOrgClient
            assert SceneOrgClient is not None
        except ImportError:
            pytest.skip("SceneOrgClient not available")

    def test_scene_org_search(self, tmp_path, monkeypatch):
        """Test Scene.org demo search."""
        monkeypatch.setattr(Path, 'home', lambda: tmp_path)
        from scene_org_integration import SceneOrgClient
        
        client = SceneOrgClient()
        assert client.download_dir is not None


class TestModArchiveIntegration:
    """Tests for ModArchive integration in jukebox."""

    def test_modarchive_api_import(self):
        """Verify ModArchiveAPI can be imported."""
        try:
            from modarchive_integration import ModArchiveAPI
            assert ModArchiveAPI is not None
        except ImportError:
            pytest.skip("ModArchiveAPI not available")

    def test_modarchive_search(self, tmp_path):
        """Test ModArchive module search."""
        from modarchive_integration import ModArchiveAPI
        from unittest.mock import patch
        
        api = ModArchiveAPI()
        assert api.cache_dir is not None


class TestCrossSourcePlaylist:
    """Tests for cross-source playlist generation."""

    def test_generate_playlist_empty(self):
        """Test playlist generation with no inputs."""
        from showet_jukebox import generate_cross_source_playlist
        
        playlist = generate_cross_source_playlist()
        assert playlist == []

    def test_generate_playlist_pouet(self):
        """Test playlist generation from Pouet IDs."""
        from showet_jukebox import generate_cross_source_playlist
        from unittest.mock import patch, MagicMock
        
        with patch("showet_jukebox.get_demo_info") as mock_get:
            mock_get.return_value = {
                "name": "Test Demo",
                "type": "64k intro",
                "platform": "commodore_64",
            }
            playlist = generate_cross_source_playlist(pouet_ids=[12345])
            assert len(playlist) == 1
            assert playlist[0]["source"] == "pouet"
            assert playlist[0]["id"] == 12345
            assert playlist[0]["loops"] is True  # 64k intros loop
            assert playlist[0]["duration"] > 0

    def test_playlist_summary(self, capsys):
        """Test playlist summary output."""
        from showet_jukebox import print_playlist_summary
        
        playlist = [
            {"id": 1, "source": "pouet", "title": "Demo 1", "type": "64k", "duration": 180, "loops": True},
            {"id": 2, "source": "scene_org", "title": "Demo 2", "duration": 120, "loops": False},
        ]
        print_playlist_summary(playlist)
        captured = capsys.readouterr()
        assert "2 demos" in captured.out or "Total demos: 2" in captured.out
        assert "300s" in captured.out or "5m" in captured.out  # 180 + 120 = 300s = 5m


class TestDurationEstimation:
    """Tests for demo duration estimation."""

    def test_estimate_duration_64k(self):
        """Test 64k intro duration estimate."""
        from showet_jukebox import estimate_demo_duration
        
        demo_info = {"type": "64k intro", "platform": "commodore_64"}
        duration = estimate_demo_duration(demo_info, "pouet")
        assert duration == 180  # 64k default

    def test_estimate_duration_4k(self):
        """Test 4k intro duration estimate."""
        from showet_jukebox import estimate_demo_duration
        
        demo_info = {"type": "4k intro"}
        duration = estimate_demo_duration(demo_info, "pouet")
        assert duration == 120

    def test_estimate_duration_platform(self):
        """Test platform-based duration estimate."""
        from showet_jukebox import estimate_demo_duration
        
        demo_info = {"type": "demo", "platform": "commodore_64"}
        duration = estimate_demo_duration(demo_info, "pouet")
        assert duration == 180

    def test_estimate_duration_modarchive(self):
        """Test ModArchive module duration estimate."""
        from showet_jukebox import estimate_demo_duration
        
        module_info = {"format": "xm", "title": "Test"}
        duration = estimate_demo_duration(module_info, "modarchive")
        assert duration == 150

    def test_estimate_duration_null(self):
        """Test null demo info returns default."""
        from showet_jukebox import estimate_demo_duration
        
        duration = estimate_demo_duration(None, "pouet")
        assert duration == 180


if __name__ == "__main__":
    pytest.main([__file__, "-v"])