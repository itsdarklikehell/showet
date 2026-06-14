#!/usr/bin/env python3
"""Web UI launcher for showet - serves the API and opens the browser."""
from __future__ import annotations

import webbrowser
from pathlib import Path

from showet_api import main


def launch_browser(port: int = 8765) -> None:
    """Start the API server and open the browser."""
    import threading
    import time

    # Open browser after a short delay
    def open_browser():
        time.sleep(1)
        url = f"http://localhost:{port}"
        print(f"Opening {url} in browser...")
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()
    main(port)