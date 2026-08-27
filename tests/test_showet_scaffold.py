"""Regression tests for showet-scaffold.py.

These lock in the fixes from BUGFIX.md where the scaffold tool emitted platform
runners whose ``super().__init__()`` omitted the required ``platform_name`` /
``version`` arguments, produced duplicate runners, or wrote malformed nostalgist
configs. Every generated artifact is now verified at generation time; these tests
guarantee that property holds for all configured platforms.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _load_scaffold():
    spec = importlib.util.spec_from_file_location(
        "_showet_scaffold", str(REPO_ROOT / "showet-scaffold.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_scaffold = _load_scaffold()
PLATFORM_CONFIGS = _scaffold.PLATFORM_CONFIGS
create_platform_runner = _scaffold.create_platform_runner
verify_platform_runner = _scaffold.verify_platform_runner

KNOWN_KEYS = list(PLATFORM_CONFIGS.keys())


@pytest.fixture
def tmp_out(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    return out


@pytest.mark.parametrize("key", KNOWN_KEYS)
def test_scaffold_generates_verified_platform_runner(key, tmp_out):
    assert create_platform_runner(key, str(tmp_out)) is True
    runner = tmp_out / f"Platform_{key}.py"
    assert runner.exists()
    ok, message = verify_platform_runner(runner, key)
    assert ok, message


def test_generated_runner_is_platformbase_subclass(tmp_out):
    key = KNOWN_KEYS[0]
    assert create_platform_runner(key, str(tmp_out)) is True
    runner = tmp_out / f"Platform_{key}.py"

    spec = importlib.util.spec_from_file_location(f"_t_{key}_{id(runner)}", str(runner))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    from PlatformBase import PlatformBase

    subs = [
        obj
        for obj in vars(module).values()
        if isinstance(obj, type) and issubclass(obj, PlatformBase) and obj is not PlatformBase
    ]
    assert subs, "no PlatformBase subclass generated"
    instance = subs[0]()
    assert instance.platform_name == key


def test_unknown_platform_returns_false(tmp_out, capsys):
    assert create_platform_runner("does_not_exist", str(tmp_out)) is False
    assert "Unknown platform" in capsys.readouterr().out


def test_refuses_to_overwrite_existing_runner(tmp_out, capsys):
    key = KNOWN_KEYS[0]
    assert create_platform_runner(key, str(tmp_out)) is True
    # A second scaffold of the same platform must be refused, not silently clobbered.
    assert create_platform_runner(key, str(tmp_out)) is False
    assert "Refusing to overwrite" in capsys.readouterr().out


def test_nostalgist_config_is_valid_json(tmp_out):
    key = KNOWN_KEYS[0]
    assert create_platform_runner(key, str(tmp_out)) is True
    cfg = tmp_out / "nostalgist_configs" / f"{key}.json"
    assert cfg.exists()
    data = json.loads(cfg.read_text())
    assert data["platform"] == key
    assert "core" in data
    assert "display" in data
    assert data["display"]["width"] == PLATFORM_CONFIGS[key]["width"]


def test_shader_stub_is_created(tmp_out):
    key = KNOWN_KEYS[0]
    assert create_platform_runner(key, str(tmp_out)) is True
    shader = tmp_out / "shaders" / f"{key}_scanlines.glsl"
    assert shader.exists()
    assert "void main" in shader.read_text()
