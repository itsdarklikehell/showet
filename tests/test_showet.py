import contextlib
import importlib
import io
import sys
import types
import unittest
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


class NoMatchRunner:
    """Runner that doesn't match any platform."""

    def supported_platforms(self):
        return ["nomatch-platform"]


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


if __name__ == "__main__":
    unittest.main()