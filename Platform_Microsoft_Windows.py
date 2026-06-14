"""Runner for the pouet "windows" platform.

Windows demo support via Wine.
"""
from __future__ import annotations

import os

from platformcommon import PlatformCommon, DEBUGGING


class Platform_Microsoft_Windows(PlatformCommon):
    """Platform runner for Windows demos via Wine."""

    emulators = ["wine", "proton"]
    cores = ["wine"]
    extensions = ["exe"]

    def supported_platforms(self) -> list[str]:
        """Return Windows and wild platform slugs."""
        return ["windows", "wild"]

    def run(self) -> None:
        """Execute the Windows demo using Wine."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        files = self.sort_disks(files)
        exefile = files[0]

        if DEBUGGING:
            print("\tGuessed executable file: " + exefile)

        wineprefix = str(self.showetdir) + "/wineprefix"
        os.putenv("WINEPREFIX", wineprefix)

        if not os.path.exists(wineprefix):
            os.makedirs(wineprefix)
            print("Creating wine prefix: " + str(wineprefix))
            os.system('WINEARCH="win64" winecfg')

        cmd = ["wine", self.datadir + "/" + exefile]
        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
            found.extend(self.find_files_with_extension(ext.upper()))
        return found
