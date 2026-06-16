#!/usr/bin/env python3
"""Retro loader animations for Showet.

Provides authentic CRT/loading effects for the CLI.
"""

import itertools
import sys
import time


def crt_loader(message: str = "LOADING", frames: int = 20) -> None:
    """Display a retro CRT-style loading animation."""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    
    for _ in range(frames):
        for char in itertools.cycle(chars):
            sys.stdout.write(f'\r{char} {message}... ')
            sys.stdout.flush()
            time.sleep(0.1)
            break


def demo_banner(platform: str, demo_name: str = "") -> None:
    """Print an awesome demoscene-style banner."""
    banner = f"""
╔══════════════════════════════════════════╗
║   SHOWET DEMO RUNNER '99               ║
║   Platform: {platform:<28}║
║   Demo: {demo_name:<32}║
╚══════════════════════════════════════════╝
    """
    print(banner)


if __name__ == "__main__":
    demo_banner("commodore_64", "Pimp My Spectrum")
    print("\nReady to launch!")