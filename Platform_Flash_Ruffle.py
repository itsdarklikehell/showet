"""Runner for Flash/SWF demos.

Supports Adobe Flash demos via Ruffle emulator.
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Flash_Ruffle(PlatformCommon):
    """Platform runner for Flash/SWF demos via Ruffle."""

    emulators = ["retroarch", "ruffle"]
    cores = ["ruffle_libretro"]
    extensions = ["swf", "spl"]

    def supported_platforms(self) -> list[str]:
        """Return Flash platform slugs."""
        return ["flash", "swfv10", "swfv9", "swfv8", "swfv7", "swfv6", "swfv5", "swfv4", "swfv3", "swfv2", "swfv1"]

    def run(self) -> None:
        """Execute the Flash demo using Ruffle."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)

        if DEBUGGING:
            print(f"Found Flash files: {files}")

        # Use core override if specified
        core = self.core_override or self.cores[0]

        # Try retroarch first if core is specified or ruffle_libretro available
        if core and core != self.ruffle_path():
            cmd = ["retroarch", "-L", core, str(self.datadir / files[0])]
            if DEBUGGING:
                print(f"Launching Flash demo via RetroArch core {core}: {files[0]}")
        elif self._has_ruffle_standalone():
            cmd = [self.ruffle_path(), str(self.datadir / files[0])]
            if DEBUGGING:
                print(f"Launching Flash demo via Ruffle standalone: {files[0]}")
        else:
            cmd = ["retroarch", "-L", self.cores[0], str(self.datadir / files[0])]
            if DEBUGGING:
                print(f"Launching Flash demo via RetroArch: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
            found.extend(self.find_files_with_extension(ext.upper()))
        return found

    def _has_ruffle_standalone(self) -> bool:
        """Check if Ruffle standalone is available."""
        import shutil
        return shutil.which("ruffle") is not None or shutil.which("ruffle-desktop") is not None

    def ruffle_path(self) -> str:
        """Return the path to Ruffle executable."""
        import shutil
        ruffle = shutil.which("ruffle")
        if ruffle:
            return ruffle
        ruffle_desktop = shutil.which("ruffle-desktop")
        if ruffle_desktop:
            return ruffle_desktop
        return "ruffle"  # Default