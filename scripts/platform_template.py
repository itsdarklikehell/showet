#!/usr/bin/env python3
"""Template generator for refactored platform runners.

This script generates a clean template for platform runner files.
It's used during the modernization effort to standardize all Platform_*.py files.
"""
from __future__ import annotations

PLATFORM_TEMPLATE = '''"""{docstring}"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class {class_name}(PlatformCommon):
    """{class_docstring}"""

    emulators = ["retroarch"]
    cores = ["{core}"]
    extensions = {extensions}

    def supported_platforms(self) -> list[str]:
        """Return platform slugs."""
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


def generate_platform_runner(class_name: str, slug: str, core: str, extensions: list[str], description: str = "") -> str:
    """Generate a platform runner file content."""
    platforms = {
        "commodore64": "Commodore 64 demos",
        "commodore128": "Commodore 128 demos",
        "commodore_amiga": "Commodore Amiga demos",
        "playstation": "Sony PlayStation demos",
        "atarivcs": "Atari VCS (2600) demos",
    }
    
    docstring = f"Runner for the pouet '{slug}' platform.\n\n{platforms.get(slug, description)}"
    class_docstring = platforms.get(slug, description) or f"{slug.replace('_', ' ').title()} platform runner"
    
    return PLATFORM_TEMPLATE.format(
        docstring=docstring,
        class_name=class_name,
        class_docstring=class_docstring,
        core=core,
        extensions=repr(extensions),
        slug=slug,
    )


if __name__ == "__main__":
    # Example usage
    print(generate_platform_runner(
        "Platform_Atari_2600",
        "atarivcs",
        "stella_libretro",
        ["zip", "a26", "bin"]
    ))