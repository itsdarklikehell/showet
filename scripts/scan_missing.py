#!/usr/bin/env python3
"""Utility script to list platforms that exist on pouet.net but have no
corresponding *Platform_* module in the showet source tree.

Usage:

    python3 scripts/scan_missing.py

The script fetches the platform list from the pouet API and
compares the slug names against the module names that are present.
It prints a short report and exits with a non‑zero status code if
any missing platforms are found.
"""

from __future__ import annotations

import json
import pathlib
import sys
import urllib.request
from collections import defaultdict


def pull_pouet_platforms() -> list[str]:
    """Return the list of platform slugs from the pouet API."""
    url = "https://api.pouet.net/v1/platforms"
    try:
        data = json.loads(urllib.request.urlopen(url).read().decode())
        return list(data["platforms"])  # JSON format is dict of slug->id
    except Exception as exc:  # pragma: no cover – network errors
        sys.stderr.write(f"Failed to fetch pouet platforms: {exc}\n")
        sys.exit(1)


def module_slugs() -> set[str]:
    """Return the set of slugs that have a ``Platform_*.py`` inside this repo."""
    # Find files matching the pattern under this repo root.
    proj_root = pathlib.Path(__file__).resolve().parents[2]
    module_files = proj_root.glob("*.py")
    slugs = set()
    for fp in module_files:
        if fp.name.startswith("Platform_"):
            slug = fp.name[len("Platform_") : -len(".py")]
            # Titles in the repo cascade in the form *UpperCase* slug
            slugs.add(slug.replace("_", ""))  # simple conversion
    return slugs


def main() -> None:
    pouet_set = set(pull_pouet_platforms())
    mod_set = module_slugs()
    missing = pouet_set - {s.lower() for s in mod_set}
    if not missing:
        print("✅  All pouet platforms are represented in the source tree.")
        sys.exit(0)

    print("❌  The following pouet platforms are missing modules:")
    for slug in sorted(missing):
        print(f"  - {slug}")
    sys.exit(1)


if __name__ == "__main__":  # pragma: no cover – CLI test only
    main()
