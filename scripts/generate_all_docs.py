#!/usr/bin/env python3
"""Generate platform documentation for all Showet platforms."""

import json
import re
from pathlib import Path

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

def _get_install_commands(slug: str) -> str:
    commands = {
        "commodore_64": "sudo apt install vice",
        "commodore_amiga": "sudo apt install fs-uae",
        "microsoft_msdos": "sudo apt install dosbox-x",
        "nintendo_famicom": "sudo apt install fceux",
        "nintendo_superfamicom": "sudo apt install snes9x",
    }
    return commands.get(slug, "sudo apt install retroarch")

def _generate_format_table(extensions: list) -> str:
    rows = [f"| .{ext} | Supported format | Native emulator |" for ext in extensions[:8]]
    return "\n".join(rows) if rows else "| Various | See platform module | Check extensions list |"

def _get_troubleshooting(slug: str) -> str:
    tips = {
        "commodore_64": "1. **No SID sound** - Check if VICE was compiled with SID support\n2. **Wrong colors** - PAL vs NTSC demo mismatch\n3. **Cannot run** - Missing kernal ROM file",
    }
    return tips.get(slug, "Check emulator installation and BIOS files if required.")

def _get_hall_of_fame(slug: str) -> str:
    demos = {
        "commodore_64": "- **Second Reality** by Future Crew - The pinnacle\n- **Unreal** by Future Crew - Graphics masterpiece",
    }
    return demos.get(slug, "Check pouet.net for top-rated demos on this platform.")

def _get_example_id(slug: str) -> int:
    ids = {"commodore_64": 12345}
    return ids.get(slug, 12345)

def main():
    project_root = Path(".")
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    count = 0
    for platform_file in sorted(project_root.glob("Platform_*.py")):
        if platform_file.name == "PlatformBase.py":
            continue

        content = platform_file.read_text()

        # Get core
        core_match = re.search(r"cores\s*=\s*\[([^\]]+)\]", content)
        core = core_match.group(1).strip().strip("'\"") if core_match else "unknown"

        # Get extensions
        ext_match = re.search(r"extensions\s*=\s*\[([^\]]+)\]", content)
        extensions = []
        if ext_match:
            ext_str = ext_match.group(1)
            extensions = [e.strip().strip("'\"") for e in ext_str.split(",")]

        # Get platform slug from supported_platforms
        slug_match = re.search(r"return \[([^\]]+)\]", content)
        internal_slug = slug_match.group(1).strip().strip("'\"") if slug_match else platform_file.stem.replace("Platform_", "").lower().replace("_", "-")

        # Generate doc
        doc_content = PLATFORM_DOCS_TEMPLATE.format(
            displayName=internal_slug.replace("_", " ").title(),
            description=f"{internal_slug.replace('_', ' ').title()} platform for running retro demos with authentic presentation.",
            emulator_list="- RetroArch\n- Native emulator",
            install_commands=_get_install_commands(internal_slug),
            slug=internal_slug,
            cfg_json=json.dumps({"core": core, "shader": "crt/crt-easymode"}, indent=2),
            format_table=_generate_format_table(extensions),
            example_id=str(_get_example_id(internal_slug)),
            example_ext=extensions[0] if extensions else "zip",
            shader="Easymode",
            trouble_list=_get_troubleshooting(internal_slug),
            hall_of_fame=_get_hall_of_fame(internal_slug),
        )

        doc_file = docs_dir / f"{internal_slug.replace('_', '-')}.md"
        doc_file.write_text(doc_content)
        count += 1

    print(f"Generated {count} platform documentation files")

if __name__ == "__main__":
    main()