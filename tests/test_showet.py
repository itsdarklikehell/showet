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
    def supported_platforms(self):
        return ["dummy-a", "dummy-b"]


class ShowetCliTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
