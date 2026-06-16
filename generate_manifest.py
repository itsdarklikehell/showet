#!/usr/bin/env python3
"""
Generate platform manifest for frontend consumption.

Creates a JSON manifest listing all available platforms and their nostalgist configs.
"""

import json
from pathlib import Path

def generate_manifest():
    """Generate platform manifest from nostalgist configs."""
    config_dir = Path(__file__).parent / "nostalgist_configs"
    
    platforms = []
    for config_file in sorted(config_dir.glob("*.json")):
        config = json.loads(config_file.read_text())
        platform = {
            "slug": config_file.stem,
            "core": config.get("core", "unknown"),
            "extensions": config.get("extensions", []),
            "shader": config.get("shader", "crt/crt-easymode")
        }
        platforms.append(platform)
    
    # Write manifest
    manifest = {
        "generated": "2025-06-16",
        "total": len(platforms),
        "platforms": platforms
    }
    
    manifest_path = config_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    
    print(f"Generated manifest with {len(platforms)} platforms")
    return manifest

if __name__ == "__main__":
    generate_manifest()