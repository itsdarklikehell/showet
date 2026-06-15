"""Runner for Android demos.

Android demo support via various emulators.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Android_Android(PlatformCommon):
    """Platform runner for Android demos.

    Supports .apk files via Android emulators.
    """

    emulators = ["android-emulator", "anbox", "qemu"]
    cores = []  # No libretro core available yet
    extensions = ["apk", "aab", "xapk"]

    def supported_platforms(self) -> list[str]:
        """Return Android platform slugs."""
        return ["android", "androidmobile"]

    def run(self) -> None:
        """Execute the Android demo using available emulator."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        apk_file = files[0]

        # Try available emulators in order
        emulator_cmd = self._get_emulator_command(apk_file)
        if not emulator_cmd:
            print("No Android emulator found. Install Anbox or Android SDK.")
            print(f"Found APK: {apk_file}")
            return

        if DEBUGGING:
            print(f"Launching Android demo via {emulator_cmd[0]}")

        self.run_process(emulator_cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
            found.extend(self.find_files_with_extension(ext.upper()))
        return found

    def _get_emulator_command(self, apk_path: str) -> list[str] | None:
        """Get command for available Android emulator.

        Tries Anbox first (easiest on Linux), then falls back to others.
        """
        apk_file = Path(apk_path)

        # Try Anbox (Linux Android container)
        if shutil.which("anbox"):
            return ["anbox", "launch", "--package", self._extract_package_name(apk_file)]

        # Try Android Emulator (AVD)
        android_emulator = shutil.which("emulator")
        if android_emulator:
            # Would need AVD setup - simplified for now
            return [android_emulator, "-avd", "showet_demo", "-install", str(apk_file)]

        # Try adb install + emu
        if shutil.which("adb"):
            return ["adb", "install", str(apk_file)]

        return None

    def _extract_package_name(self, apk_path: Path) -> str:
        """Extract package name from APK filename as fallback.

        Real implementation would use aapt or unzip to read manifest.
        """
        # Fallback: use filename as identifier
        return apk_path.stem.lower().replace("_", "-").replace(" ", "-")