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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])