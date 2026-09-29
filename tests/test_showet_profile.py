"""Tests for showet-profile configuration profiles (TDD — expect RED before implementation)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

PROFILES_DIR_ENV = "SHOWET_PROFILES_DIR"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _profiles_dir(tmp_path: Path) -> Path:
    d = tmp_path / "profiles"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _run_profile_cli(profiles_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env[PROFILES_DIR_ENV] = str(profiles_dir)
    # Use the editable install's entry-point; fall back to module invocation.
    cmd = [sys.executable, "-m", "showet.cli.profile_cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=30)


# ---------------------------------------------------------------------------
# 1. Profile directory & persistence
# ---------------------------------------------------------------------------

class TestProfileDirDefaults:
    """The profile system must resolve ~/.showet/profiles when no env override is set."""

    def test_default_profiles_dir_is_under_showet_home(self, tmp_path):
        from showet.core.config import SHOWET_DIR
        from showet.profile import profiles_dir

        expected = SHOWET_DIR / "profiles"
        # Without env override the function returns the static default.
        assert profiles_dir() == expected


class TestProfileDirOverride:
    """SHOWET_PROFILES_DIR must redirect the profiles directory."""

    def test_env_overrides_default(self, tmp_path, monkeypatch):
        from showet.profile import profiles_dir

        alt = tmp_path / "custom-profiles"
        alt.mkdir()
        monkeypatch.setenv(PROFILES_DIR_ENV, str(alt))
        assert profiles_dir() == alt


class TestProfilePersistence:
    """create stores a valid JSON file; show reads it back."""

    def test_create_writes_json_file(self, tmp_path):
        from showet.profile import ProfileStore

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("test-proj", {"SHOWET_DEBUG": "true"})
        p = store.profile_path("test-proj")
        assert p.exists()
        data = json.loads(p.read_text())
        assert data["name"] == "test-proj"
        assert data["variables"]["SHOWET_DEBUG"] == "true"

    def test_create_replaces_existing_profile(self, tmp_path):
        from showet.profile import ProfileStore

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("dup", {"SHOWET_DEBUG": "0"})
        store.create("dup", {"SHOWET_DEBUG": "1", "SHOWET_TIMEOUT": "10"})
        data = json.loads((store.profile_path("dup")).read_text())
        assert data["variables"]["SHOWET_DEBUG"] == "1"
        assert data["variables"]["SHOWET_TIMEOUT"] == "10"

    def test_show_returns_stored_values(self, tmp_path):
        from showet.profile import ProfileStore

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("s", {"SHOWET_DEBUG": "true", "SHOWET_TIMEOUT": "5"})
        profile = store.load("s")
        assert profile["variables"]["SHOWET_DEBUG"] == "true"
        assert profile["variables"]["SHOWET_TIMEOUT"] == "5"


# ---------------------------------------------------------------------------
# 2. Profile name validation
# ---------------------------------------------------------------------------

class TestProfileNameValidation:
    """Profile names must be safe filesystem identifiers."""

    def test_valid_names_accepted(self):
        from showet.profile import validate_profile_name

        for name in ("dev", "steamdeck", "my-profile_1", "a", "x" * 40):
            assert validate_profile_name(name) is None

    def test_empty_name_rejected(self):
        from showet.profile import validate_profile_name

        with pytest.raises(ValueError, match="name"):
            validate_profile_name("")

    def test_name_with_slash_rejected(self):
        from showet.profile import validate_profile_name

        with pytest.raises(ValueError, match="name"):
            validate_profile_name("a/b")

    def test_name_with_backslash_rejected(self):
        from showet.profile import validate_profile_name

        with pytest.raises(ValueError, match="name"):
            validate_profile_name("a\\b")

    def test_name_with_dotdot_rejected(self):
        from showet.profile import validate_profile_name

        with pytest.raises(ValueError, match="name"):
            validate_profile_name("../esc")

    def test_name_with_null_rejected(self):
        from showet.profile import validate_profile_name

        with pytest.raises(ValueError, match="name"):
            validate_profile_name("\x00name")


# ---------------------------------------------------------------------------
# 3. Environment variable validation
# ---------------------------------------------------------------------------

class TestEnvVarKeyValidation:
    """Only SHOWET_* keys are accepted; duplicates within a profile are rejected."""

    def test_non_showet_key_rejected(self):
        from showet.profile import validate_variables

        with pytest.raises(ValueError, match="SHOWET_"):
            validate_variables({"PATH": "/usr/bin"})

    def test_showet_key_accepted(self):
        from showet.profile import validate_variables

        # Should not raise.
        assert validate_variables({"SHOWET_DEBUG": "true"}) is None

    def test_duplicate_keys_rejected(self):
        from showet.profile import validate_variables

        with pytest.raises(ValueError, match="duplicate"):
            validate_variables([("SHOWET_DEBUG", "true"), ("SHOWET_DEBUG", "false")])


class TestEnvVarValueValidation:
    """Values must be non-empty strings without embedded newlines (practical CLI use)."""

    def test_empty_value_rejected(self):
        from showet.profile import validate_variables

        with pytest.raises(ValueError, match="value"):
            validate_variables({"SHOWET_DEBUG": ""})

    def test_multiline_value_rejected(self):
        from showet.profile import validate_variables

        with pytest.raises(ValueError, match="newline"):
            validate_variables({"SHOWET_DEBUG": "line1\nline2"})

    def test_normal_value_accepted(self):
        from showet.profile import validate_variables

        assert validate_variables({"SHOWET_TIMEOUT": "300"}) is None


# ---------------------------------------------------------------------------
# 4. list / show / delete via CLI
# ---------------------------------------------------------------------------

class TestListCommand:
    """showet-profile list prints every profile name, one per line."""

    def test_list_empty(self, tmp_path, capsys):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import list_profiles

        store = ProfileStore(_profiles_dir(tmp_path))
        list_profiles(store)
        out = capsys.readouterr().out
        assert out.strip() == ""

    def test_list_multiple(self, tmp_path, capsys):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import list_profiles

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("alpha", {"SHOWET_DEBUG": "1"})
        store.create("beta", {"SHOWET_DEBUG": "0"})
        list_profiles(store)
        out = capsys.readouterr().out
        lines = [l for l in out.splitlines() if l.strip()]
        assert "alpha" in lines
        assert "beta" in lines


class TestShowCommand:
    """showet-profile show <name> prints the profile's variables (secrets masked)."""

    def test_show_existing(self, tmp_path, capsys):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import show_profile

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("demo", {"SHOWET_DEBUG": "true", "SHOWET_TIMEOUT": "60"})
        show_profile(store, "demo")
        out = capsys.readouterr().out
        assert "SHOWET_DEBUG" in out
        assert "true" in out
        assert "SHOWET_TIMEOUT" in out
        assert "60" in out

    def test_show_unknown_profile(self, tmp_path, capsys):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import show_profile

        store = ProfileStore(_profiles_dir(tmp_path))
        ret = show_profile(store, "nope")
        assert ret != 0
        out = capsys.readouterr().out
        assert "nope" in out.lower() or "not found" in out.lower()

    def test_show_masks_secrets(self, tmp_path, capsys):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import show_profile

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("sec", {"SHOWET_API_KEY": "secret-value", "SHOWET_DEBUG": "1"})
        show_profile(store, "sec")
        out = capsys.readouterr().out
        assert "secret-value" not in out
        assert "API_KEY" in out  # key name still shown


class TestDeleteCommand:
    """showet-profile delete <name> removes the profile file."""

    def test_delete_removes_file(self, tmp_path, capsys):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import delete_profile

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("gone", {"SHOWET_DEBUG": "1"})
        assert store.profile_path("gone").exists()
        ret = delete_profile(store, "gone")
        assert ret == 0
        assert not store.profile_path("gone").exists()

    def test_delete_unknown_is_noop(self, tmp_path, capsys):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import delete_profile

        store = ProfileStore(_profiles_dir(tmp_path))
        ret = delete_profile(store, "nope")
        assert ret != 0


# ---------------------------------------------------------------------------
# 5. run command — env injection + child execution
# ---------------------------------------------------------------------------

class TestRunCommand:
    """showet-profile run <name> -- <child-command...> injects variables and execs."""

    def test_run_injects_variables(self, tmp_path):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import run_profile

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("envtest", {"SHOWET_DEBUG": "from-profile"})
        # Child that prints matched env var.
        child = [sys.executable, "-c", "import os; print(os.environ.get('SHOWET_DEBUG','MISSING'))"]
        rc, out, err = run_profile(store, "envtest", child)
        assert rc == 0
        assert out.strip() == "from-profile"

    def test_run_overrides_existing_var(self, tmp_path):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import run_profile

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("override", {"SHOWET_DEBUG": "profile-value"})
        child = [sys.executable, "-c", "import os; print(os.environ.get('SHOWET_DEBUG','MISSING'))"]
        rc, out, err = run_profile(store, "override", child, extra_env={"SHOWET_DEBUG": "original"})
        # Profile value should win.
        assert out.strip() == "profile-value"

    def test_run_unknown_profile_fails(self, tmp_path):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import run_profile

        store = ProfileStore(_profiles_dir(tmp_path))
        rc, out, err = run_profile(store, "nope", [sys.executable, "-c", "print(1)"])
        assert rc != 0

    def test_run_passes_child_exit_code(self, tmp_path):
        from showet.profile import ProfileStore
        from showet.cli.profile_cli import run_profile

        store = ProfileStore(_profiles_dir(tmp_path))
        store.create("x", {})
        rc, out, err = run_profile(store, "x", [sys.executable, "-c", "raise SystemExit(7)"])
        assert rc == 7


# ---------------------------------------------------------------------------
# 6. End-to-end: editable CLI entry point
# ---------------------------------------------------------------------------

@pytest.mark.e2e
class TestProfileCLIE2E:
    """Verify the installed editable `showet-profile` entry point works."""

    def test_entry_point_list_empty(self, tmp_path, monkeypatch):
        monkeypatch.setenv(PROFILES_DIR_ENV, str(_profiles_dir(tmp_path)))
        r = _run_profile_cli(_profiles_dir(tmp_path), "list")
        assert r.returncode == 0
        assert r.stdout.strip() == ""

    def test_entry_point_create_and_show(self, tmp_path, monkeypatch):
        d = _profiles_dir(tmp_path)
        monkeypatch.setenv(PROFILES_DIR_ENV, str(d))
        r = _run_profile_cli(d, "create", "e2e", "SHOWET_DEBUG=true", "SHOWET_TIMEOUT=10")
        assert r.returncode == 0, r.stderr
        r = _run_profile_cli(d, "show", "e2e")
        assert r.returncode == 0, r.stderr
        assert "SHOWET_DEBUG" in r.stdout
        assert "true" in r.stdout

    def test_entry_point_run(self, tmp_path, monkeypatch):
        d = _profiles_dir(tmp_path)
        monkeypatch.setenv(PROFILES_DIR_ENV, str(d))
        _run_profile_cli(d, "create", "run-test", "SHOWET_DEBUG=e2e-ok")
        child = [sys.executable, "-c", "import os; print(os.environ.get('SHOWET_DEBUG','MISS'))"]
        r = _run_profile_cli(d, "run", "run-test", *child)
        assert r.returncode == 0, r.stderr
        assert "e2e-ok" in r.stdout

    def test_entry_point_delete(self, tmp_path, monkeypatch):
        d = _profiles_dir(tmp_path)
        monkeypatch.setenv(PROFILES_DIR_ENV, str(d))
        _run_profile_cli(d, "create", "to-delete", "SHOWET_DEBUG=1")
        r = _run_profile_cli(d, "delete", "to-delete")
        assert r.returncode == 0, r.stderr
        assert not (d / "to-delete.json").exists()
