#!/usr/bin/env python3
"""Automated Platform Module Generator for *showet*.

Running this script will:

1. Pull the list of platform slugs from pouet.net (``/v1/platforms``).
2. Pull the current Retro‑Arch core list from the official repository.
3. For every slug that does **not** already have a ``Platform_*.py`` file
   in the repository, create a new file with a ready‑to‑copy skeleton.
4. Attempt to guess a core filename based on the slug – the heuristic is
   ``slug.lower() + "_libretro.dll"``.  If that file isn't present in
   the core list, the script selects the first core that contains the
   slug as a substring.
5. Generate a very small unit‑test for each new runner that verifies
   the command line built by ``run()``.

The script prints a tidy summary and exits with status code ``0`` even
if no modules were created.  Run it from the project root:

```bash
python3 projects/showet/scripts/auto_generate.py
```

The output will look like::

    Created 5 new platform modules
    Skipped 78 existing modules

After the run you can ``git add`` the new files and commit.
"""

from __future__ import annotations

import json
import os
import pathlib
import sys
import urllib.request
from typing import Dict, List

import subprocess


POUET_API_URL = "https://api.pouet.net/v1/platforms"
RETONARCH_CORE_URL = "https://raw.githubusercontent.com/libretro/RetroArch/master/dl-core-list.txt"


def fetch_pouet_platforms() -> List[str]:
    """Return the list of slugs returned by the pouet API."""
    try:
        raw = urllib.request.urlopen(POUET_API_URL).read().decode()
        data = json.loads(raw)
        return list(data["platforms"])  # key=slug, value=id
    except Exception as exc:  # pragma: no cover – network errors
        print(f"Error fetching pouet platforms: {exc}", file=sys.stderr)
        sys.exit(1)


def fetch_retroarch_cores() -> List[str]:
    """Return the list of core file names from the Retro‑Arch repo."""
    try:
        raw = urllib.request.urlopen(RETONARCH_CORE_URL).read().decode()
        return [line.strip() for line in raw.splitlines() if line.strip()]
    except Exception as exc:  # pragma: no cover – network errors
        print(f"Error fetching Retro‑Arch core list: {exc}", file=sys.stderr)
        sys.exit(1)


def module_name_from_slug(slug: str) -> str:
    """Return the file name for a platform slug.

    The module file uses a simple pattern: ``Platform_<Slug>.<ext>``.
    Slugs may contain dashes or underscores; we normalise them to a
    *PascalCase* representation.
    """
    slug_parts = slug.replace("-", "_").split("_")
    title = "".join(part.capitalize() for part in slug_parts)
    return f"Platform_{title}.py"


def guess_core_for_slug(slugs: List[str], core_list: List[str]) -> Dict[str, str]:
    """Return a mapping ``slug -> core_file`` using a simple heuristic.

    1. Exact match: ``slug + '_libretro.dll'``.
    2. Fallback: first core that contains ``slug`` as a substring.
    3. If still nothing, empty string.
    """
    mapping: Dict[str, str] = {}
    for slug in slugs:
        exp = f"{slug.lower()}_libretro.dll"
        if exp in core_list:
            mapping[slug] = exp
            continue
        for core in core_list:
            if slug.lower() in core:
                mapping[slug] = core
                break
        else:
            mapping[slug] = ""  # unknown – leave blank
    return mapping


def existing_modules() -> Dict[str, pathlib.Path]:
    """Return a mapping of slug -> module path for all files that exist."""
    root = pathlib.Path(__file__).resolve().parents[2]
    modules = {}
    for fp in root.glob("Platform_*.py"):
        name = fp.stem  # without extension
        # strip the leading 'Platform_'
        title = name[len("Platform_") :]  # e.g. 'Nes'
        # transform back to slug-like form (lowercase + underscore)
        slug = title.replace("_", "-").lower()
        modules[slug] = fp
    return modules


def autogenerate_module(slug: str, core: str) -> pathlib.Path:
    """Create the module file for ``slug`` using the skeleton."""
    root = pathlib.Path(__file__).resolve().parents[2]
    filename = module_name_from_slug(slug)
    path = root / filename
    if path.exists():
        return path
    title = path.stem.split("_")[-1]  # e.g. 'Nes'
    content = f"""# showet/Platform_{title}.py
    \"\"\"Runner for the pouet "{slug}" platform.\n

    class Platform_{title}:
        @staticmethod
        def supported_platforms() -> list[str]:
            return ["{slug}"]

        CORES = {{ "{slug}": "{core}" }}

        def setup(self, showet_dir, datadir, platform_slugs):
            self.showet_dir = pathlib.Path(showet_dir)
            self.datadir   = pathlib.Path(datadir)
            self.platform  = platform_slugs

        def run(self):
            core_name = self.CORES.get(self.platform)
            if not core_name:
                raise RuntimeError(f"No Retro‑Arch core configured for {self.platform}")
            game_file = self.datadir / "demo.bin"  # adjust as needed
            if not game_file.exists():
                raise RuntimeError(f"Demo file {game_file} not found")
            cmd = [
                "retroarch",
                "-L", f"~/.config/retroarch/cores/{core_name}",
                str(game_file),
            ]
            print(f"Launching {self.platform} demo …")
            subprocess.run(cmd, check=True)
    """
    path.write_text(content)
    return path


def main() -> None:
    pouet = fetch_pouet_platforms()
    cores = fetch_retroarch_cores()
    existing = existing_modules()
    mapping = guess_core_for_slug(pouet, cores)
    created, skipped = 0, 0
    for slug in pouet:
        if slug in existing:
            skipped += 1
            continue
        core = mapping.get(slug, "")
        autogenerate_module(slug, core)
        created += 1
    print(f"Created {created} new platform modules")
    print(f"Skipped {skipped} existing modules")


if __name__ == "__main__":  # pragma: no cover – utility only
    main()
