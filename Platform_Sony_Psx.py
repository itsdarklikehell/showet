"""Platform runner for Sony PlayStation demos via RetroArch.

Supports PSX, PS2 and other PlayStation demo formats.
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Sony_Psx(PlatformCommon):
    """Platform runner for PlayStation demos.

    Uses RetroArch with PCSX-ReARMed libretro core.
    Supports .cue, .bin, .iso, .chd and other PSX formats.
    """

    emulators = ["retroarch"]
    cores = ["pcsx_rearmed_libretro"]

    extensions = ["zip", "exe", "psx", "psexe", "cue", "toc", "bin", "img",
                  "iso", "chd", "pbp", "ccd", "ecm", "cbn", "mdf", "mds", "psf", "m3u"]

    def supported_platforms(self) -> list[str]:
        """Return PlayStation platform slugs."""
        return ["playstation"]

    def run(self) -> None:
        """Execute the PSX demo using RetroArch."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        core = self.cores[0]
        cmd = ["retroarch", "-L", core, files[0]]

        if DEBUGGING:
            print(f"Launching PSX demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions.

        Returns:
            List of matching file paths.
        """
        found_files = []
        for ext in self.extensions:
            found_files.extend(self.find_files_with_extension(ext))
        return found_files

