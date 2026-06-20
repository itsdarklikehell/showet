#!/usr/bin/env python3
"""
nostalgist.js bridge for Showet.

Generates JSON configuration files that nostalgist.js can use to launch
Showet-downloaded demos in the browser.

Reference: https://nostalgist.js.org/apis/launch/#core
Supported cores: https://github.com/arianrhodsandlot/retroarch-emscripten-build
"""

import json
import re
from pathlib import Path
from typing import Any

# Core name mapping from Showet's Platform modules to nostalgist.js core names
CORE_MAPPING: dict[str, str] = {
    # Famicom/NES
    "quicknes_libretro": "quicknes",
    "fceumm_libretro": "fceumm",
    "nestopia_libretro": "nestopia",

    # Sega
    "genesis_plus_gx_libretro": "genesis_plus_gx",
    "picodrive_libretro": "picodrive",
    "gearsystem_libretro": "gearsystem",
    "sms_libretro": "gearsystem",

    # Nintendo
    "snes9x_libretro": "snes9x",
    "bsnes_libretro": "bsnes",
    "gambatte_libretro": "gambatte",
    "meteor_libretro": "meteor",

    # Commodore
    "vice_x64_libretro": "vice_x64",
    "vice_x64sc_libretro": "vice_x64sc",
    "vice_x128_libretro": "vice_x128",
    "puae_libretro": "puae",  # Amiga core (needs to be in nostalgist CDN)
    "puae2021_libretro": "puae2021",

    # Arcade
    "fbalpha_libretro": "fbalpha2012",
    "mame_libretro": "mame2003",

    # Playstation
    "pcsx_rearmed_libretro": "pcsx_rearmed",

    # Atari
    "stella_libretro": "stella",
    "stella2014_libretro": "stella",
    "hatari_libretro": "hatari",

    # Computer
    "fuse_libretro": "fuse",
    "mednafen_libretro": "mednafen",
}

# Default shaders for CRT effect
SHADER_MAP = {
    "commodore_64": "crt/crt-easymode",
    "commodore_vic20": "crt/crt-easymode",
    "commodore_amiga": "crt/crt-royale",
    "nintendo_famicom": "crt/crt-easymode",
    "nintendo_gameboy": "crt/crt-pi",
    "nintendo_superfamicom": "crt/crt-easymode",
    "sega_megadrive": "crt/crt-easymode",
    "sega_mastersystem": "crt/crt-pi",
    "sony_psx": "crt/crt-royale",
    "atari": "crt/crt-pi",
    "zx_spectrum": "crt/crt-pi",
    "default": "crt/crt-easymode",
}


def generate_nostalgist_config(
    platform_slug: str,
    rom_path: str,
    core_name: str,
    system_bios: str | None = None,
    shader: str | None = None,
    **kwargs: Any
) -> dict[str, Any]:
    """Generate a nostalgist.js launch configuration."""
    # Map Showet core to nostalgist core (strip .so extension for CDN)
    mapped_core = CORE_MAPPING.get(core_name, core_name.replace("_libretro.so", "").replace("_libretro", ""))

    config: dict[str, Any] = {
        "core": mapped_core,
        "rom": rom_path,
    }

    if system_bios:
        config["systemFiles"] = system_bios

    if shader:
        config["shader"] = shader
    else:
        slug_lower = platform_slug.lower()
        for key, shader_name in SHADER_MAP.items():
            if key in slug_lower:
                config["shader"] = shader_name
                break
        else:
            config["shader"] = SHADER_MAP["default"]

    config.update(kwargs)
    return config


def parse_platform_module(filepath: Path) -> dict[str, Any] | None:
    """Parse a Platform_*.py file to extract configuration."""
    content = filepath.read_text()

    slug_match = re.search(r'super\(\).__init__\("([^"]+)"', content)
    if not slug_match:
        return None

    slug = slug_match.group(1)

    cores_match = re.search(r'cores\s*=\s*\[([^\]]+)\]', content)
    core = None
    if cores_match:
        core_str = cores_match.group(1)
        cores = [c.strip().strip("'\"") for c in core_str.split(',') if c.strip().strip("'\"")]
        core = cores[0] if cores else None

    ext_match = re.search(r'extensions\s*=\s*\[([^\]]+)\]', content)
    extensions = []
    if ext_match:
        ext_str = ext_match.group(1)
        extensions = [e.strip().strip("'\"") for e in ext_str.split(',') if e.strip().strip("'\"")]

    return {
        "slug": slug,
        "core": core,
        "extensions": extensions,
        "file": filepath.name,
    }


def generate_batch_configs(
    platforms_dir: Path,
    output_dir: Path,
    rom_base_url: str | None = None
) -> list[str]:
    """Generate nostalgist configs for all platform modules."""
    output_dir.mkdir(exist_ok=True)
    generated = []

    for platform_file in platforms_dir.glob("Platform_*.py"):
        if platform_file.name == "PlatformBase.py":
            continue

        platform_info = parse_platform_module(platform_file)

        if not platform_info or not platform_info.get("core"):
            continue

        slug = platform_info["slug"]
        core = platform_info["core"]
        extensions = platform_info.get("extensions", [])

        config = generate_nostalgist_config(
            platform_slug=slug,
            rom_path=rom_base_url or f"/roms/{slug}/",
            core_name=core,
            style={"backgroundColor": "black", "width": "100%", "height": "100%"},
        )

        config["extensions"] = extensions

        config_file = output_dir / f"{slug}.json"
        config_file.write_text(json.dumps(config, indent=2))
        generated.append(config_file.name)

    return generated


if __name__ == "__main__":
    project_root = Path(__file__).parent
    configs = generate_batch_configs(
        platforms_dir=project_root,
        output_dir=project_root / "nostalgist_configs",
    )

    print("📺 nostalgist.js integration ready!")
    print(f"Generated {len(configs)} configs in nostalgist_configs/")
    print("Point ROM URLs to your demo files and serve these configs to the frontend.")
    if configs:
        print(f"\nSample configs: {configs[:5]}")