"""Showet configuration profiles.

Named profiles store SHOWET_* environment variables as JSON files under
``~/.showet/profiles/<name>.json``.  Use them to switch between setups
(e.g. "steamdeck", "dev", "streaming") without manual env manipulation.

Security note
-------------
Profile JSON is plaintext on disk.  Do not store credentials you would not
want on an unencrypted filesystem.  Prefer the system keyring or dedicated
secret env-vars for sensitive values; the ``show`` / ``list`` commands mask
keys ending in ``KEY``, ``SECRET``, ``TOKEN``, ``PASSWORD`` or ``CREDENTIAL``
in their output, but the stored file itself is not encrypted.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

from showet.core.config import SHOWET_DIR

# -- directory ----------------------------------------------------------------

def profiles_dir() -> Path:
    """Return the directory where profile JSON files are stored.

    Respects ``SHOWET_PROFILES_DIR`` if set; otherwise defaults to
    ``~/.showet/profiles``.
    """
    override = os.environ.get("SHOWET_PROFILES_DIR")
    if override:
        return Path(override)
    return SHOWET_DIR / "profiles"


# -- validation ----------------------------------------------------------------

_PROFILE_NAME_RE = __import__("re").compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def validate_profile_name(name: str) -> None:
    """Raise ``ValueError`` if *name* is not a safe profile identifier."""
    if not name:
        raise ValueError("profile name must not be empty")
    if len(name) > 64:
        raise ValueError("profile name must be at most 64 characters")
    if "\x00" in name:
        raise ValueError("profile name must not contain null bytes")
    # Block path separators and traversal sequences.
    for ch in ("/", "\\", "\n", "\r"):
        if ch in name:
            raise ValueError(f"profile name must not contain {ch!r}")
    if name in (".", ".."):
        raise ValueError("profile name must not be '.' or '..'")
    if not _PROFILE_NAME_RE.match(name):
        raise ValueError(
            f"profile name {name!r} contains invalid characters "
            "(allowed: alphanumeric, '.', '-', '_' ; must start with alphanumeric)"
        )


_SECRET_SUFFIXES = ("KEY", "SECRET", "TOKEN", "PASSWORD", "CREDENTIAL")


def _is_secret_key(key: str) -> bool:
    upper = key.upper()
    return any(upper.endswith(s) for s in _SECRET_SUFFIXES)


def validate_variables(
    variables: dict[str, str] | Sequence[tuple[str, str]],
) -> None:
    """Validate the variable mapping for a profile.

    Accepts either a plain ``dict[str, str]`` or a sequence of
    ``(key, value)`` pairs.  Raises ``ValueError`` on:

    * any key not starting with ``SHOWET_``
    * duplicate keys (only detectable when a pair sequence is passed)
    * empty values or values containing newlines
    """
    if isinstance(variables, dict):
        items: Sequence[tuple[str, str]] = list(variables.items())
        # dict keys are unique by construction — no duplicate check needed.
        for key, value in items:
            if not key.startswith("SHOWET_"):
                raise ValueError(
                    f"variable key {key!r} does not start with 'SHOWET_'"
                )
            if not isinstance(value, str) or value == "":
                raise ValueError(f"variable value for {key!r} must be a non-empty string")
            if "\n" in value or "\r" in value:
                raise ValueError(f"variable value for {key!r} must not contain newlines")
        return

    # pair sequence — duplicates are detectable here
    seen: set[str] = set()
    for key, value in variables:
        if not key.startswith("SHOWET_"):
            raise ValueError(
                f"variable key {key!r} does not start with 'SHOWET_'"
            )
        if key in seen:
            raise ValueError(f"duplicate variable key {key!r}")
        seen.add(key)
        if not isinstance(value, str) or value == "":
            raise ValueError(f"variable value for {key!r} must be a non-empty string")
        if "\n" in value or "\r" in value:
            raise ValueError(f"variable value for {key!r} must not contain newlines")


# -- storage ------------------------------------------------------------------

class ProfileStore:
    """Read/write named profiles in a profiles directory."""

    def __init__(self, root: Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    def profile_path(self, name: str) -> Path:
        validate_profile_name(name)
        return self._root / f"{name}.json"

    def list_names(self) -> list[str]:
        """Return sorted profile names (without .json extension)."""
        if not self._root.exists():
            return []
        names: list[str] = []
        for p in sorted(self._root.glob("*.json")):
            names.append(p.stem)
        return names

    def create(
        self,
        name: str,
        variables: dict[str, str] | Sequence[tuple[str, str]],
        *,
        description: str = "",
    ) -> None:
        """Write or overwrite a profile.

        *variables* must satisfy ``validate_variables``.
        """
        validate_profile_name(name)
        validate_variables(variables)
        path = self.profile_path(name)
        doc: dict[str, Any] = {
            "name": name,
            "description": description,
            "variables": dict(variables),
        }
        path.write_text(json_dumps(doc), encoding="utf-8")

    def load(self, name: str) -> dict[str, Any]:
        """Return the full profile document for *name*, or raise ``KeyError``."""
        validate_profile_name(name)
        path = self.profile_path(name)
        if not path.exists():
            raise KeyError(name)
        return json_loads(path.read_text(encoding="utf-8"))

    def delete(self, name: str) -> bool:
        """Delete the profile file.  Returns ``True`` if it existed."""
        validate_profile_name(name)
        path = self.profile_path(name)
        if not path.exists():
            return False
        path.unlink()
        return True


# -- helpers ------------------------------------------------------------------

def json_dumps(obj: Any) -> str:
    import json
    return json.dumps(obj, indent=2, sort_keys=True) + "\n"


def json_loads(text: str) -> Any:
    import json
    return json.loads(text)


def _mask_value(key: str, value: str) -> str:
    if _is_secret_key(key):
        return "********"
    return value


def print_profile(doc: dict[str, Any], *, mask_secrets: bool = True) -> None:
    """Pretty-print a profile document to stdout."""
    print(f"Profile: {doc['name']}")
    if doc.get("description"):
        print(f"Description: {doc['description']}")
    variables = doc.get("variables", {})
    if not variables:
        print("No variables set.")
        return
    print("Variables:")
    for key in sorted(variables):
        val = variables[key]
        if mask_secrets:
            val = _mask_value(key, val)
        print(f"  {key}={val}")


# -- run ----------------------------------------------------------------------

def run_profile(
    store: ProfileStore,
    name: str,
    child_cmd: list[str],
    *,
    extra_env: dict[str, str] | None = None,
) -> tuple[int, str, str]:
    """Set profile variables and execute *child_cmd*.

    Returns ``(returncode, stdout, stderr)`` from the child process.
    """
    try:
        doc = store.load(name)
    except KeyError:
        print(f"Error: profile {name!r} not found", file=sys.stderr)
        return 1, "", ""

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    for key, val in doc.get("variables", {}).items():
        env[key] = val

    try:
        proc = subprocess.run(
            child_cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except FileNotFoundError:
        print(f"Error: command not found: {child_cmd[0]!r}", file=sys.stderr)
        return 127, "", ""
    except subprocess.TimeoutExpired:
        print(f"Error: command timed out: {' '.join(child_cmd)!r}", file=sys.stderr)
        return 124, "", ""

    return proc.returncode, proc.stdout, proc.stderr
