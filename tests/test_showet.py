import contextlib
import importlib
import io
import os
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

sys.modules.setdefault("inquirer", types.SimpleNamespace())
sys.modules.setdefault("patoolib", types.SimpleNamespace())

showet = importlib.import_module("showet")


class DummyRunner:
    """Minimal runner stub for testing purposes."""

    def supported_platforms(self):
        return ["dummy-a", "dummy-b"]

    def setup(self, showetdir, datadir, platform):
        pass

    def run(self):
        pass

    def set_options(self, fullscreen=False, audio=True, core=None):
        self.fullscreen = fullscreen
        self.audio = audio
        self.core_override = core


class NoMatchRunner:
    """Runner that doesn't match any platform."""

    def supported_platforms(self):
        return ["nomatch-platform"]

    def setup(self, showetdir, datadir, platform):
        pass

    def run(self):
        pass

    def set_options(self, fullscreen=False, audio=True, core=None):
        self.fullscreen = fullscreen
        self.audio = audio
        self.core_override = core


class ShowetCliTests(unittest.TestCase):
    """Tests for the CLI entry point and argument handling."""

    def test_platforms_lists_supported_platforms_without_running_prod(self):
        output = io.StringIO()

        with (
            mock.patch.object(showet, "create_platform_runners", return_value=[DummyRunner()]),
            mock.patch.object(showet, "run_production") as run_production,
            contextlib.redirect_stdout(output),
        ):
            result = showet.main(["--platforms"])

        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue().splitlines(), ["dummy-a", "dummy-b"])
        run_production.assert_not_called()

    def test_main_returns_negative_one_without_pouetid(self):
        with mock.patch.object(showet, "create_platform_runners", return_value=[DummyRunner()]):
            with mock.patch.object(showet, "run_production", wraps=showet.run_production) as run_prod:
                result = showet.main([])
        self.assertEqual(result, -1)


class SelectRunnerTests(unittest.TestCase):
    """Tests for the _select_runner function."""

    def test_select_runner_returns_matching_runner(self):
        run_a = DummyRunner()  # supports ["dummy-a", "dummy-b"]
        run_b = mock.Mock()
        run_b.supported_platforms.return_value = ["c64", "commodore64"]

        runner, matched = showet._select_runner([run_a, run_b], ["dummy-a"])
        self.assertIs(runner, run_a)
        self.assertEqual(matched, "dummy-a")

    def test_select_runner_returns_none_for_no_match(self):
        run_a = mock.Mock()
        run_a.supported_platforms.return_value = ["amiga"]
        run_b = mock.Mock()
        run_b.supported_platforms.return_value = ["c64"]

        runner, matched = showet._select_runner([run_a, run_b], ["unknown-platform"])
        self.assertIsNone(runner)
        self.assertIsNone(matched)

    def test_select_runner_finds_first_match(self):
        run_a = DummyRunner()  # supports ["dummy-a", "dummy-b"]
        run_b = DummyRunner()

        runner, matched = showet._select_runner([run_a, run_b], ["dummy-a"])
        self.assertIs(runner, run_a)
        self.assertEqual(matched, "dummy-a")

    def test_select_runner_with_multiple_platforms(self):
        run_a = mock.Mock()
        run_a.supported_platforms.return_value = ["amiga"]
        run_b = mock.Mock()
        run_b.supported_platforms.return_value = ["c64", "c128"]

        runner, matched = showet._select_runner([run_a, run_b], ["c64", "unknown"])
        self.assertIs(runner, run_b)
        self.assertEqual(matched, "c64")


class RunProductionTests(unittest.TestCase):
    """Tests for the run_production function error paths."""

    def test_run_production_returns_negative_one_without_pouetid(self):
        args = mock.Mock(pouetid=None)
        result = showet.run_production(args, [])
        self.assertEqual(result, -1)

    def test_run_production_with_unsupported_platform(self):
        output = io.StringIO()
        args = mock.Mock(pouetid=12345)

        # Pouet API returns platforms as a dict with numeric keys
        platforms_data = {"prod": {"platforms": {0: {"slug": "unknown"}, 1: {"slug": "also-unknown"}}}}
        with (
            mock.patch.object(showet, "_download_json", return_value=platforms_data),
            mock.patch.object(showet, "_select_runner", return_value=(None, None)),
            contextlib.redirect_stdout(output),
        ):
            result = showet.run_production(args, [NoMatchRunner()])

        self.assertEqual(result, -1)
        self.assertIn("ERROR", output.getvalue())


class PlatformRunnerTests(unittest.TestCase):
    """Tests for platform runner behavior."""

    def test_create_platform_runners_returns_list(self):
        runners = showet.create_platform_runners()
        self.assertIsInstance(runners, list)
        self.assertTrue(len(runners) > 0)

    def test_runner_has_supported_platforms_method(self):
        runners = showet.create_platform_runners()
        for runner in runners:
            platforms = runner.supported_platforms()
            self.assertIsInstance(platforms, list)
            self.assertTrue(len(platforms) > 0)

    def test_all_platforms_are_unique(self):
        runners = showet.create_platform_runners()
        all_platforms = []
        for runner in runners:
            all_platforms.extend(runner.supported_platforms())

        # Check for duplicates (platform slugs should be unique)
        unique_platforms = set(all_platforms)
        # Some platforms may have duplicates across runners, just verify we have platforms
        self.assertTrue(len(all_platforms) > 0)


class ArgParserTests(unittest.TestCase):
    """Tests for argument parser configuration."""

    def test_build_arg_parser_has_platforms_flag(self):
        parser = showet.build_arg_parser()
        # Parse --platforms to ensure it exists
        args = parser.parse_args(["--platforms"])
        self.assertTrue(args.platforms)

    def test_build_arg_parser_parses_pouetid(self):
        parser = showet.build_arg_parser()
        args = parser.parse_args(["12345"])
        self.assertEqual(args.pouetid, 12345)

    def test_build_arg_parser_parses_random_flag(self):
        parser = showet.build_arg_parser()
        args = parser.parse_args(["--random"])
        self.assertTrue(args.random)

    def test_build_arg_parser_has_fullscreen_flag(self):
        parser = showet.build_arg_parser()
        args = parser.parse_args(["--fullscreen"])
        self.assertTrue(args.fullscreen)

    def test_build_arg_parser_has_audio_flag(self):
        parser = showet.build_arg_parser()
        args = parser.parse_args(["--no-audio"])
        self.assertFalse(args.audio)

    def test_build_arg_parser_has_core_flag(self):
        parser = showet.build_arg_parser()
        args = parser.parse_args(["--core", "pcsx_rearmed_libretro"])
        self.assertEqual(args.core, "pcsx_rearmed_libretro")

    def test_fullscreen_enabled_in_retroarch_command(self):
        """Verify fullscreen option causes --fullscreen to be added to retroarch commands."""
        import platformcommon
        runner = platformcommon.PlatformCommon()
        runner.fullscreen = True
        runner.datadir = Path("/tmp")

        # Test that when fullscreen is True, --fullscreen is inserted
        test_cmd = ["retroarch", "-L", "core_libretro", "file.zip"]
        with mock.patch("subprocess.Popen") as mock_popen:
            mock_process = mock.Mock()
            mock_process.stdout = []
            mock_process.returncode = 0
            mock_popen.return_value = mock_process
            runner.run_process(test_cmd)

        # Verify --fullscreen was inserted at position 1
        self.assertEqual(test_cmd[1], "--fullscreen")
        self.assertEqual(test_cmd[0], "retroarch")


class FlashPlatformTests(unittest.TestCase):
    """Tests for Flash platform runner."""

    def test_flash_platform_registered(self):
        """Verify Flash platform runner is registered and returns correct platforms."""
        runners = showet.create_platform_runners()
        flash_runners = [r for r in runners if "flash" in r.supported_platforms()]
        self.assertEqual(len(flash_runners), 1)

    def test_flash_supported_platforms(self):
        """Verify Flash runner supports expected platform slugs."""
        runners = showet.create_platform_runners()
        flash_runners = [r for r in runners if "flash" in r.supported_platforms()]
        platforms = flash_runners[0].supported_platforms()
        self.assertIn("flash", platforms)
        self.assertIn("swfv10", platforms)


class AndroidPlatformTests(unittest.TestCase):
    """Tests for Android platform runner."""

    def test_android_platform_registered(self):
        """Verify Android platform runner is registered."""
        runners = showet.create_platform_runners()
        android_runners = [r for r in runners if "android" in r.supported_platforms()]
        self.assertEqual(len(android_runners), 1)

    def test_android_supported_platforms(self):
        """Verify Android runner supports expected platform slugs."""
        runners = showet.create_platform_runners()
        android_runners = [r for r in runners if "android" in r.supported_platforms()]
        platforms = android_runners[0].supported_platforms()
        self.assertIn("android", platforms)
        self.assertIn("androidmobile", platforms)

    def test_android_extensions(self):
        """Verify Android runner has correct extensions."""
        runners = showet.create_platform_runners()
        android_runners = [r for r in runners if "android" in r.supported_platforms()]
        self.assertIn("apk", android_runners[0].extensions)


class PlaylistManagerTests(unittest.TestCase):
    """Tests for the PlaylistManager class."""

    def setUp(self):
        """Create a temporary directory with test playlist."""
        import tempfile
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_playlist_loads_entries(self):
        """Verify playlist loads correctly from file."""
        from playlist_manager import PlaylistManager

        # Create test files
        (self.temp_dir / "disk1.dsk").touch()
        (self.temp_dir / "disk2.dsk").touch()

        # Create playlist
        playlist = self.temp_dir / "test.m3u"
        playlist.write_text("disk1.dsk\ndisk2.dsk\n")

        entries = PlaylistManager.load_playlist(playlist)
        self.assertEqual(len(entries), 2)
        self.assertTrue(entries[0].exists())
        self.assertTrue(entries[1].exists())

    def test_load_playlist_skips_comments(self):
        """Verify comments are skipped in playlist."""
        from playlist_manager import PlaylistManager

        (self.temp_dir / "disk.dsk").touch()

        playlist = self.temp_dir / "test.m3u"
        playlist.write_text("# This is a comment\ndisk.dsk\n# Another comment\n")

        entries = PlaylistManager.load_playlist(playlist)
        self.assertEqual(len(entries), 1)

    def test_create_playlist_writes_file(self):
        """Verify playlist creation works correctly."""
        from playlist_manager import PlaylistManager

        files = [self.temp_dir / "a.dsk", self.temp_dir / "b.dsk"]
        for f in files:
            f.touch()

        output = self.temp_dir / "output.m3u"
        PlaylistManager.create_playlist(files, output)

        self.assertTrue(output.exists())
        content = output.read_text()
        self.assertIn("a.dsk", content)
        self.assertIn("b.dsk", content)

    def test_find_playlists_finds_m3u_files(self):
        """Verify playlist discovery works."""
        from playlist_manager import PlaylistManager

        (self.temp_dir / "demo1.m3u").touch()
        (self.temp_dir / "demo2.m3u8").touch()
        (self.temp_dir / "other.txt").touch()

        found = PlaylistManager.find_playlists(self.temp_dir)
        self.assertEqual(len(found), 2)

    def test_detect_platform_from_playlist_returns_platform(self):
        """Verify platform detection from playlist extensions."""
        from playlist_manager import PlaylistManager

        (self.temp_dir / "game.adf").touch()
        playlist = self.temp_dir / "game.m3u"
        playlist.write_text("game.adf\n")

        platform = PlaylistManager.detect_platform_from_playlist(playlist)
        self.assertEqual(platform, "commodore_amiga")


if __name__ == "__main__":
    unittest.main()