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


if __name__ == "__main__":
    unittest.main()