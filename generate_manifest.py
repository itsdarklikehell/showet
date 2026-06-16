#!/usr/bin/env python3
"""
Generate platform manifest for frontend consumption.

Creates a JSON manifest listing all available platforms and their nostalgist configs.
"""

import json
import re
from pathlib import Path

def get_platform_info(slug: str, config: dict) -> dict:
    """Extract platform info from config and platform module."""
    # Try to get extensions from platform module
    platform_file = Path(__file__).parent / f"Platform_{slug}.py"
    if not platform_file.exists():
        # Try to find matching platform file
        for pf in Path(__file__).parent.glob(f"Platform_*{slug}*.py"):
            platform_file = pf
            break
    
    extensions = []
    if platform_file.exists():
        content = platform_file.read_text()
        ext_match = re.search(r'extensions\s*=\s*\[([^\]]+)\]', content)
        if ext_match:
            ext_str = ext_match.group(1)
            extensions = [e.strip().strip("'\"") for e in ext_str.split(',')]
    
    return {
        "slug": slug,
        "core": config.get("core", "unknown"),
        "extensions": extensions,
        "shader": config.get("shader", "crt/crt-easymode"),
        "originalName": slug.replace("_", " ").replace("-", " ").title()
    }

def generate_manifest():
    """Generate platform manifest from nostalgist configs."""
    config_dir = Path(__file__).parent / "nostalgist_configs"
    
    platforms = []
    for config_file in sorted(config_dir.glob("*.json")):
        if config_file.name == "manifest.json":
            continue
        config = json.loads(config_file.read_text())
        platforms.append(get_platform_info(config_file.stem, config))
    
    # Write manifest
    from datetime import datetime
    manifest = {
        "generated": datetime.now().strftime("%Y-%m-%d"),
        "total": len(platforms),
        "platforms": platforms
    }
    
    manifest_path = config_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    
    print(f"Generated manifest with {len(platforms)} platforms")
    return manifest

if __name__ == "__main__":
    generate_manifest()