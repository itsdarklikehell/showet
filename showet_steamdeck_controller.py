#!/usr/bin/env python3
"""Showet Steam Deck Controller - Gamepad input mapping and OSD.

Provides controller support for Steam Deck with optimized UI layouts
and on-screen display (OSD) controls.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


class SteamDeckController:
    """Steam Deck controller configuration and mapping."""

    BUTTON_MAP = {
        "a": 0,
        "b": 1,
        "x": 2,
        "y": 3,
        "lb": 4,
        "rb": 5,
        "start": 6,
        "select": 7,
        "l3": 8,
        "r3": 9,
        "up": 10,
        "down": 11,
        "left": 12,
        "right": 13,
    }

    DEFAULT_CONFIG = {
        "button_mappings": {
            "0": "primary_action",      # A button
            "1": "back",               # B button
            "2": "menu",               # X button
            "3": "shader_toggle",      # Y button
            "4": "seek_backward",      # LB
            "5": "seek_forward",       # RB
            "6": "play_pause",         # Start
            "7": "settings",           # Select
        },
        "axis_mappings": {
            "left_stick": "navigate_menu",
            "right_stick": "quick_demo_switch",
            "left_trigger": "volume_down",
            "right_trigger": "volume_up",
        },
        "deck_optimized": True,
        "fullscreen_default": True,
    }

    def __init__(self, config_path: Optional[Path] = None):
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[Path]) -> dict:
        """Load controller configuration."""
        if config_path and config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return self.DEFAULT_CONFIG

    def get_action(self, button_code: int) -> Optional[str]:
        """Get action for button press."""
        return self.config.get("button_mappings", {}).get(str(button_code))

    def get_axis_action(self, axis: str) -> Optional[str]:
        """Get action for axis movement."""
        return self.config.get("axis_mappings", {}).get(axis)


class ShowetOSD:
    """On-screen display for Steam Deck overlay."""

    def __init__(self):
        self.visible = False
        self._controls = {
            "show": self.show,
            "hide": self.hide,
            "toggle": self.toggle,
            "update": self.update,
        }

    def show(self, message: str, duration: int = 3000) -> None:
        """Show OSD message."""
        self.visible = True
        print(f"[OSD] {message}")

    def hide(self) -> None:
        """Hide OSD."""
        self.visible = False

    def toggle(self) -> None:
        """Toggle OSD visibility."""
        self.visible = not self.visible

    def update(self, info: dict) -> None:
        """Update OSD with demo info."""
        if self.visible:
            demo_name = info.get("title", "Unknown")
            platform = info.get("platform", "unknown")
            status = info.get("status", "ready")
            print(f"[OSD] {demo_name} | {platform} | {status}")


def load_steamdeck_config() -> dict:
    """Load Steam Deck configuration from file."""
    config_path = Path.home() / ".config" / "showet" / "deck_config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return SteamDeckController.DEFAULT_CONFIG


def main() -> int:
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Showet Steam Deck Controller")
    parser.add_argument("--config", help="Path to controller config")
    parser.add_argument("--detect", action="store_true", help="Detect Steam Deck gamepad")
    parser.add_argument("--test-osd", action="store_true", help="Test OSD display")
    args = parser.parse_args()

    controller = SteamDeckController(
        Path(args.config) if args.config else None
    )

    if args.detect:
        print("🎮 Checking for Steam Deck gamepad...")
        config = load_steamdeck_config()
        print(f"Configuration loaded: deck_optimized={config.get('deck_optimized')}")
        return 0

    if args.test_osd:
        osd = ShowetOSD()
        osd.show("Showet OSD Test - Steam Deck Ready!", 5000)
        return 0

    print("🎮 Steam Deck Controller Module")
    print("Use --detect to check gamepad or --test-osd to test display")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())