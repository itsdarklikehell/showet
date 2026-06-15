"""Runner for the pouet "webassembly" platform.

WebAssembly/web-based demo support via browser or Node.js.
"""
from __future__ import annotations

from platformcommon import PlatformCommon, DEBUGGING


class Platform_WebAssembly_Web(PlatformCommon):
    """Platform runner for WebAssembly/web-based demos."""

    emulators = ["browser"]
    cores = []
    extensions = ["wasm", "html"]

    def supported_platforms(self) -> list[str]:
        """Return WebAssembly platform slugs."""
        return ["webassembly", "web", "html5", "javascript", "wasm"]

    def run(self) -> None:
        """Execute the WebAssembly demo in browser."""
        files = self._find_runnable_files()

        if not files:
            print("Didn't find any runnable files.")
            return

        # Open in default browser for HTML/WASM demos
        cmd = ["xdg-open", files[0]]
        if DEBUGGING:
            print(f"Opening WebAssembly demo in browser: {files[0]}")

        self.run_process(cmd)

    def _find_runnable_files(self) -> list[str]:
        """Find files with supported extensions."""
        found = []
        for ext in self.extensions:
            found.extend(self.find_files_with_extension(ext))
        return found