#!/usr/bin/env python3
"""
Generate platform manifest for frontend consumption.

Creates a JSON manifest listing all available platforms and their nostalgist configs.
Enhanced version that extracts full extension info from platform modules.
"""

import json
import re
from pathlib import Path
from datetime import datetime


def get_platform_extensions(slug: str) -> list[str]:
    """Extract extensions from platform module for a given slug."""
    platform_file = Path(__file__).parent / f"Platform_{slug}.py"
    if not platform_file.exists():
        for pf in Path(__file__).parent.glob("Platform_*.py"):
            content = pf.read_text()
            slug_match = re.search(r'return \[([^\]]+)\]', content)
            if slug_match and slug in slug_match.group(1):
                platform_file = pf
                break

    extensions = []
    if platform_file.exists():
        content = platform_file.read_text()
        ext_match = re.search(r'extensions\s*=\s*\[([^\]]+)\]', content)
        if ext_match:
            ext_str = ext_match.group(1)
            extensions = [e.strip().strip("'\"") for e in ext_str.split(',') if e.strip().strip("'\"")]

    return extensions


def format_platform_name(slug: str) -> str:
    """Format platform slug as display name."""
    name_map = {
        "commodore_64": "Commodore 64",
        "commodore_amiga": "Commodore Amiga",
        "commodore_128": "Commodore 128",
        "commodore_vic20": "Commodore VIC-20",
        "microsoft_msdos": "MS-DOS",
        "nintendo_famicom": "Nintendo Famicom (NES)",
        "nintendo_superfamicom": "Nintendo Super Famicom (SNES)",
        "sega_megadrive": "Sega Mega Drive (Genesis)",
        "sony_psx": "Sony PlayStation",
        "atari_2600": "Atari 2600",
        "zx_spectrum": "ZX Spectrum",
        "pc_engine": "PC Engine",
    }
    return name_map.get(slug, slug.replace("_", " ").replace("-", " ").title())


def generate_manifest():
    """Generate platform manifest from nostalgist configs."""
    config_dir = Path(__file__).parent / "nostalgist_configs"
    platforms = []

    for config_file in sorted(config_dir.glob("*.json")):
        if config_file.name == "manifest.json":
            continue
        if config_file.stem == "crt_presets":
            continue

        try:
            config = json.loads(config_file.read_text())
            extensions = get_platform_extensions(config_file.stem)
            platforms.append({
                "slug": config_file.stem,
                "core": config.get("core", "unknown"),
                "extensions": extensions,
                "shader": config.get("shader", "crt/crt-easymode"),
                "originalName": format_platform_name(config_file.stem),
            })
        except Exception as e:
            print(f"Warning: Could not parse {config_file.name}: {e}")

    manifest = {
        "generated": datetime.now().strftime("%Y-%m-%d"),
        "total": len(platforms),
        "platforms": platforms,
    }

    manifest_path = config_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Generated manifest with {len(platforms)} platforms")
    return manifest


def regenerate_configs_with_extensions():
    """Regenerate nostalgist configs with proper extensions."""
    from nostalgist_bridge import generate_nostalgist_config

    config_dir = Path(__file__).parent / "nostalgist_configs"

    for platform_file in Path(__file__).parent.glob("Platform_*.py"):
        content = platform_file.read_text()

        slug_match = re.search(r'super\(\).__init__\("([^"]+)"', content)
        core_match = re.search(r'cores\s*=\s*\[([^\]]+)\]', content)

        if not slug_match or not core_match:
            continue

        slug = slug_match.group(1)
        core_str = core_match.group(1)
        # Parse cores - handle quoted strings properly
        cores = []
        for part in core_str.split(','):
            c = part.strip().strip("'\"")
            if c:
                cores.append(c)
        core = cores[0] if cores else "unknown"

        ext_match = re.search(r'extensions\s*=\s*\[([^\]]+)\]', content)
        extensions = []
        if ext_match:
            ext_str = ext_match.group(1)
            extensions = [e.strip().strip("'\"") for e in ext_str.split(',') if e.strip().strip("'\"")]

        config = generate_nostalgist_config(
            platform_slug=slug,
            rom_path=f"/roms/{slug}/",
            core_name=core,
            style={"backgroundColor": "black", "width": "100%", "height": "100%"},
        )

        config["extensions"] = extensions

        config_file = config_dir / f"{slug}.json"
        config_file.write_text(json.dumps(config, indent=2))
        print(f"Updated: {config_file.name}")


if __name__ == "__main__":
    regenerate_configs_with_extensions()
    generate_manifest()
    print("\n✅ Platform configs and manifest regenerated!")