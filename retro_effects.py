#!/usr/bin/env python3
"""Authentic CRT shader presets for Television Simulator.

These presets recreate the look of classic CRT monitors and TVs
that were used in demoscene productions during the 80s-90s era.

Each preset includes:
- Scanlines
- Curvature
- Phosphor glow
- Color bleeding
- Ghosting (composite artifacts)
"""

from __future__ import annotations

from typing import Any

# Authentic CRT presets for different computer/console eras
CRT_PRESETS: dict[str, dict[str, Any]] = {
    "c64_monitor": {
        "name": "Commodore 64 Monitor (1980s)",
        "description": "CRT monitor with green phosphor and vertical scanlines",
        "shader": "crt/crt-pi",
        "scanline_intensity": 0.7,
        "scanline_period": 2,
        "curvature": 0.1,
        "glow": 0.2,
        "colors": ["#aaaa00", "#ffffff", "#aaaa00", "#aaaaaa"],
        "phosphor": "green",
    },
    "amiga_ocs": {
        "name": "Amiga OCS (1985-1990)",
        "description": "Sharp CRT with horizontal scanlines, characteristic of Amiga displays",
        "shader": "crt/crt-easymode",
        "scanline_intensity": 0.5,
        "scanline_period": 1,
        "curvature": 0.05,
        "glow": 0.15,
        "phosphor": "rgb",
    },
    "atari_st": {
        "name": "Atari ST (1985-1992)",
        "description": "Medium persistence phosphor, visible dot crawl",
        "shader": "crt/crt-royale",
        "scanline_intensity": 0.6,
        "scanline_period": 2,
        "curvature": 0.15,
        "glow": 0.25,
        "phosphor": "white",
    },
    "nes_famicom": {
        "name": "NES/Famicom (1983-1995)",
        "description": "Composite video artifacts, NTSC color bleeding",
        "shader": "crt/crt-easymode",
        "scanline_intensity": 0.8,
        "scanline_period": 1,
        "curvature": 0.2,
        "glow": 0.3,
        "phosphor": "ntsc",
        "composite_artifact": True,
    },
    "snes_superfamicom": {
        "name": "SNES/Super Famicom (1990-2000)",
        "description": "RGB monitor, sharp pixels with subtle scanlines",
        "shader": "crt/crt-pi",
        "scanline_intensity": 0.4,
        "scanline_period": 1,
        "curvature": 0.08,
        "glow": 0.1,
        "phosphor": "rgb",
    },
    "genesis_megadrive": {
        "name": "Genesis/Mega Drive (1988-1995)",
        "description": "CMOS-based CRT, distinct color bleeding",
        "shader": "crt/crt-royale",
        "scanline_intensity": 0.5,
        "scanline_period": 2,
        "curvature": 0.12,
        "glow": 0.2,
        "phosphor": "rgb",
    },
    "vga_vesa": {
        "name": "VGA CRT (1990s PC)",
        "description": "Higher resolution CRT, subtle scanlines",
        "shader": "crt/crt-easymode",
        "scanline_intensity": 0.2,
        "scanline_period": 1,
        "curvature": 0.02,
        "glow": 0.05,
        "phosphor": "rgb",
    },
    "commodore_amiga_pal": {
        "name": "Amiga PAL (Europe)",
        "description": "PAL 50Hz timing, slightly squashed aspect",
        "shader": "crt/crt-pi",
        "scanline_intensity": 0.45,
        "scanline_period": 1,
        "curvature": 0.08,
        "glow": 0.15,
        "phosphor": "rgb",
        "pal_mode": True,
    },
}


def get_preset(platform_slug: str) -> dict[str, Any]:
    """Get CRT preset for a specific platform.
    
    Args:
        platform_slug: Showet platform slug (e.g., 'commodore_64', 'nintendo_famicom')
    
    Returns:
        CRT preset configuration
    """
    slug_lower = platform_slug.lower()
    
    # Map platforms to presets
    platform_map = {
        "commodore_64": "c64_monitor",
        "commodore_pet": "c64_monitor",
        "commodore_vic20": "c64_monitor",
        "nintendo_famicom": "nes_famicom",
        "nintendo_disksystem": "nes_famicom",
        "superfamicom": "snes_superfamicom",
        "nintendo_snes": "snes_superfamicom",
        "nintendo_super": "snes_superfamicom",
        "megadrive": "genesis_megadrive",
        "mastersystem": "genesis_megadrive",
        "sega_megadrive": "genesis_megadrive",
        "commodore_amiga": "amiga_ocs",
        "atari_st": "atari_st",
        "ms-dos": "vga_vesa",
        "microsoft_msdos": "vga_vesa",
    }
    
    # Try exact match first
    for platform, preset_name in platform_map.items():
        if platform in slug_lower:
            return CRT_PRESETS.get(preset_name, CRT_PRESETS["amiga_ocs"])
    
    # Try direct preset match
    if slug_lower in CRT_PRESETS:
        return CRT_PRESETS[slug_lower]
    
    # Default fallback
    return CRT_PRESETS["amiga_ocs"]


def generate_shader_config(platform_slug: str) -> dict[str, Any]:
    """Generate a complete shader configuration for nostalgist.js.
    
    Args:
        platform_slug: Showet platform slug
    
    Returns:
        Configuration dict for nostalgist.js shader system
    """
    preset = get_preset(platform_slug)
    
    return {
        "shader": preset["shader"],
        "parameters": {
            "scanline_intensity": preset["scanline_intensity"],
            "scanline_period": preset["scanline_period"],
            "curvature": preset["curvature"],
            "glow": preset["glow"],
        },
        "preset_name": preset["name"],
        "preset_description": preset["description"],
    }


def generate_all_preset_html() -> str:
    """Generate HTML select options for all CRT presets."""
    options = [
        f'                        <option value="{slug}">{preset["name"]}</option>'
        for slug, preset in CRT_PRESETS.items()
    ]
    return "\n".join(options)


def list_platforms_with_presets() -> list[str]:
    """Get list of platform slugs that have specific presets."""
    platforms = []
    for slug in CRT_PRESETS.keys():
        # These map to multiple possible platform slugs
        platforms.extend([f"{slug.upper()}", slug])
    return platforms


if __name__ == "__main__":
    print("📺 Available CRT Presets:")
    for _slug, preset in CRT_PRESETS.items():
        print(f"  - {preset['name']}: {preset['description']}")
    
    print("\n🎯 Platform mappings:")
    for platform, preset in {
        "c64": "c64_monitor",
        "amiga": "amiga_ocs",
        "nes": "nes_famicom",
        "snes": "snes_superfamicom",
    }.items():
        print(f"  - {platform} → {CRT_PRESETS[preset]['name']}")