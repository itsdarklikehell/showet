#!/usr/bin/env python3
"""Batch refactor script for Platform_*.py files.

Identifies files using the old pattern and refactors them to the clean template.
"""
import re
from pathlib import Path


def extract_platform_info(content: str) -> dict:
    """Extract slug, core, and extensions from a platform file."""
    slug_match = re.search(r'return \[["\']([^"\']+)["\']\]', content)
    core_match = re.search(r"cores = \[[\s\n]*['\"]([^'\"]+)['\"]", content)
    
    # Try to find extensions
    extensions_match = re.search(r"extensions = \[([^\]]+)\]", content, re.DOTALL)
    
    slug = slug_match.group(1) if slug_match else "unknown"
    core = core_match.group(1) if core_match else "libretro"
    
    # Default extensions for common platforms
    default_extensions = {
        "commodore128": ["d64", "d71", "d81", "t64", "tap", "prg", "p00"],
        "commodore_amiga": ["adf", "dms", "ipf", "adz", "lha", "zip"],
        "atarivcs": ["zip", "a26", "bin"],
    }
    
    if extensions_match:
        ext_str = extensions_match.group(1)
        extensions = re.findall(r"['\"]([^'\"]+)['\"]", ext_str)
    else:
        extensions = default_extensions.get(slug, ["zip"])
    
    # Class name
    class_match = re.search(r"class (Platform_\w+)\(", content)
    class_name = class_match.group(1) if class_match else "Platform"
    
    return {
        "slug": slug,
        "core": core,
        "extensions": extensions,
        "class_name": class_name,
    }


def generate_clean_platform(data: dict) -> str:
    """Generate clean platform runner content."""
    slug = data["slug"]
    core = data["core"]
    extensions = data["extensions"]
    class_name = data["class_name"]
    
    platform_descs = {
        "commodore64": "Commodore 64 demos",
        "commodore128": "Commodore 128 demos",
        "commodore_amiga": "Commodore Amiga demos",
        "playstation": "Sony PlayStation demos",
        "atarivcs": "Atari VCS (2600) demos",
    }
    
    description = platform_descs.get(slug, f"{slug.replace('_', ' ').title()} demos")
    
    return f'''"""Runner for the pouet "{slug}" platform.

{description}
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class {class_name}(PlatformCommon):
    """Platform runner for {description}."""

    emulators = ["retroarch"]
    cores = ["{core}"]
    extensions = {repr(extensions)}

    def supported_platforms(self) -> list[str]:
        """Return {slug} platform slug."""
        return ["{slug}"]

    def run(self) -> None:
        """Execute the demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        cmd = ["retroarch", "-L", self.cores[0], files[0]]

        if DEBUGGING:
            print(f"Launching {slug} demo via RetroArch: {{files[0]}}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found
'''


def main():
    project_dir = Path(__file__).parent.parent
    platform_files = sorted(project_dir.glob("Platform_*.py"))
    
    old_pattern_count = 0
    for pf in platform_files:
        content = pf.read_text()
        if "emulator.append('-L')" in content:
            old_pattern_count += 1
            info = extract_platform_info(content)
            new_content = generate_clean_platform(info)
            pf.write_text(new_content)
            print(f"Refactored: {pf.name}")
    
    print(f"\\nTotal files refactored: {old_pattern_count}")


if __name__ == "__main__":
    main()