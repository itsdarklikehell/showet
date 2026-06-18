#!/usr/bin/env python3
"""Generate platform documentation for all Showet platforms.

Creates markdown files in docs/ for each platform with execution instructions,
emulator setup, and supported formats.
"""

import json
import re
from pathlib import Path

PLATFORM_INFO = {
    "commodore_64": {
        "displayName": "Commodore 64",
        "shortName": "C64",
        "description": "The most iconic demoscene platform with legendary productions like Second Reality.",
        "emulators": ["VICE (x64sc)", "RetroArch (vice_x64sc)"],
        "default_roms": "D64, T64, PRG, CRT, TAP",
    },
    "commodore_amiga": {
        "displayName": "Commodore Amiga",
        "shortName": "Amiga",
        "description": "Revolutionary multimedia computer with incredible demo scene.",
        "emulators": ["FS-UAE", "RetroArch (puae_libretro)"],
        "default_roms": "ADF, HDF, Kickstart required",
    },
    "microsoft_msdos": {
        "displayName": "Microsoft MS-DOS",
        "shortName": "DOS",
        "description": "The platform that brought demos to the masses with VGA graphics.",
        "emulators": ["DOSBox-X", "RetroArch (dosbox_libretro)"],
        "default_roms": "EXE, COM, BAT (no BIOS needed)",
    },
    "nintendo_famicom": {
        "displayName": "Nintendo Famicom (NES)",
        "shortName": "NES",
        "description": "8-bit Nintendo console with countless homebrew demos.",
        "emulators": ["FCEUX", "RetroArch (quicknes_libretro)"],
        "default_roms": "NES, FDS (no BIOS for most games)",
    },
    "nintendo_superfamicom": {
        "displayName": "Nintendo Super Famicom (SNES)",
        "shortName": "SNES",
        "description": "16-bit Nintendo with advanced graphics for impressive demos.",
        "emulators": ["Snes9x", "RetroArch (snes9x_libretro)"],
        "default_roms": "SMC, SFC (no BIOS needed)",
    },
}

PLATFORM_DOCS_TEMPLATE = """# {displayName} Platform Documentation

## Overview
{description}

## Emulation Setup

### Required Binaries
{emulator_list}

### Installation
```bash
{install_commands}
```

## Platform Configuration
Located at: `nostalgist_configs/{slug}.json`

```json
{cfg_json}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
{format_table}

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet {example_id}

# Run local file
showet-executor /path/to/demo.{example_ext}

# Run in museum mode
showet-museum --platform {slug}
```

## CRT Settings
- **Shader**: CRT-{shader}
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible with flicker
- **Phosphor Bloom**: Enabled for authentic glow

## Troubleshooting

### Common Issues
{trouble_list}

## Notable Demos

{hall_of_fame}

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
"""


def generate_platform_docs():
    """Generate documentation for all platform modules."""
    project_root = Path(__file__).parent.parent  # scripts is in project root
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    for platform_file in sorted(project_root.glob("Platform_*.py")):
        slug = platform_file.stem.replace("Platform_", "").lower().replace("_", " ").replace("-", " ")
        slug = platform_file.stem.replace("Platform_", "").lower().replace("_", " ")

        # Try to extract info from platform file
        content = platform_file.read_text()

        # Get extensions
        ext_match = re.search(r'extensions\s*=\s*\[([^\]]+)\]', content)
        extensions = []
        if ext_match:
            ext_str = ext_match.group(1)
            extensions = [e.strip().strip("'\"") for e in ext_str.split(',')]

        # Get core
        core_match = re.search(r'cores\s*=\s*\[([^\]]+)\]', content)
        core = core_match.group(1).strip().strip("'\"") if core_match else "unknown"

        # Get platform slug from supported_platforms
        slug_match = re.search(r'return \[([^\]]+)\]', content)
        internal_slug = slug_match.group(1).strip().strip("'\"") if slug_match else slug

        # Use known info or generate defaults
        info = PLATFORM_INFO.get(internal_slug, {})
        display_name = info.get("displayName", platform_file.stem.replace("Platform_", " ").replace("_", " "))
        short_name = info.get("shortName", display_name.split()[0])
        description = info.get(
            "description",
            f"{display_name} platform for running retro demos with authentic presentation."
        )
        emulators = info.get("emulators", ["RetroArch"])
        default_roms = info.get("default_roms", ", ".join(extensions))

        # Generate documentation
        emulator_list = "\n".join(f"- **{e}**" for e in emulators)
        install_commands = _get_install_commands(internal_slug)
        cfg_json = json.dumps({
            "core": core,
            "shader": "crt/crt-easymode",
        }, indent=2)
        format_table = _generate_format_table(extensions)
        trouble_list = _get_troubleshooting(internal_slug)
        hall_of_fame = _get_hall_of_fame(internal_slug)

        doc_content = PLATFORM_DOCS_TEMPLATE.format(
            displayName=display_name,
            description=description,
            emulator_list=emulator_list,
            install_commands=install_commands,
            slug=internal_slug,
            cfg_json=cfg_json,
            example_id=str(_get_example_id(internal_slug)),
            example_ext=extensions[0] if extensions else "zip",
            shader="Easymode",
            format_table=format_table,
            trouble_list=trouble_list,
            hall_of_fame=hall_of_fame,
        )

        doc_file = docs_dir / f"{internal_slug.replace(' ', '-')}.md"
        doc_file.write_text(doc_content)
        print(f"Generated: {doc_file.name}")


def _get_install_commands(slug: str) -> str:
    """Get platform-specific install commands."""
    commands = {
        "commodore_64": "sudo apt install vice",
        "commodore_amiga": "sudo apt install fs-uae",
        "microsoft_msdos": "sudo apt install dosbox-x",
        "nintendo_famicom": "sudo apt install fceux",
        "nintendo_superfamicom": "sudo apt install snes9x",
        "sega_megadrive": "sudo apt install retroarch",
        "sony_psx": "sudo apt install pcsxr",
    }
    return commands.get(slug, "sudo apt install retroarch  # or appropriate emulator")


def _generate_format_table(extensions: list[str]) -> str:
    """Generate format description table."""
    ext_info = {
        "d64": ("Disk image - Most common format", "VICE emulates original floppy"),
        "t64": ("Tape image - For tape-loaded demos", "Commodore tape loading"),
        "prg": ("Program file - Direct executable", "Runs directly in emulator"),
        "adf": ("Amiga Disk image", "FS-UAE or WinUAE"),
        "hdf": ("Amiga Hard disk image", "FS-UAE direct boot"),
        "nes": ("NES ROM - Nintendo 8-bit", "FCEUX or RetroArch"),
        "sfc": ("Super Famicom ROM", "Snes9x or RetroArch"),
        "smc": ("Super Nintendo ROM", "Snes9x or RetroArch"),
    }

    rows = []
    for ext in extensions[:8]:
        info = ext_info.get(ext, ("Supported format", "Native emulator"))
        rows.append(f"| .{ext} | {info[0]} | {info[1]} |")

    return "\n".join(rows) if rows else "| Various | See platform module | Check extensions list |"


def _get_troubleshooting(slug: str) -> str:
    """Get troubleshooting tips for platform."""
    tips = {
        "commodore_64": "1. **No SID sound** - Check if VICE was compiled with SID support\n2. **Wrong colors** - PAL vs NTSC demo mismatch\n3. **Cannot run** - Missing kernal ROM file",
        "commodore_amiga": "1. **Kickstart required** - Amiga needs BIOS files\n2. **WHDLoad** - Use HFS for best compatibility\n3. **Chip RAM** - Some demos need more RAM",
        "microsoft_msdos": "1. **Slow execution** - Use cycles=3000 in DOSBox config\n2. **Missing DLLs** - Install MSVCRT in Wine prefix\n3. **Sound issues** - Set sbtype=sb16 in DOSBox",
    }
    return tips.get(slug, "Check emulator installation and BIOS files if required.")


def _get_hall_of_fame(slug: str) -> str:
    """Get hall of fame demos for platform."""
    demos = {
        "commodore_64": "- **Second Reality** by Future Crew - The pinnacle\n- **Unreal** by Future Crew - Graphics masterpiece\n- **State of the Art** by Spaceballs - Disk magazine",
    }
    return demos.get(slug, "Check pouet.net for top-rated demos on this platform.")


def _get_example_id(slug: str) -> int:
    """Get example Pouet ID for platform."""
    ids = {
        "commodore_64": 12345,  # Placeholder
        "commodore_amiga": 12345,
        "microsoft_msdos": 12345,
    }
    return ids.get(slug, 12345)


if __name__ == "__main__":
    generate_platform_docs()
    print("\n✅ All platform documentation generated!")