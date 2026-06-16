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
from typing import Dict, Any, Optional, List

# Core name mapping from Showet's Platform modules to nostalgist.js core names
CORE_MAPPING: Dict[str, str] = {
    # Famicom/NES
    "quicknes_libretro": "quicknes",
    "fceumm_libretro": "fceumm",
    "nestopia_libretro": "nestopia",
    
    # Sega
    "genesis_plus_gx_libretro": "genesis_plus_gx",
    "picodrive_libretro": "picodrive",
    "gearsystem_libretro": "gearsystem",  # Master System
    "sms_libretro": "gearsystem",
    
    # Nintendo
    "snes9x_libretro": "snes9x",
    "bsnes_libretro": "bsnes",
    
    # Commodore
    "vice_x64_libretro": "vice_x64",
    "vice_x64sc_libretro": "vice_x64sc",
    "vice_x128_libretro": "vice_x128",
    
    # Arcade
    "fbalpha_libretro": "fbalpha2012",
    "mame_libretro": "mame2003",
    
    # Playstation
    "pcsx_rearmed_libretro": "pcsx_rearmed",
    
    # Atari
    "stella_libretro": "stella",
    "stella2014_libretro": "stella",
    
    # Fallback: strip _libretro suffix
}

# Default shaders for CRT effect
SHADER_MAP = {
    "nes": "crt/crt-easymode",
    "famicom": "crt/crt-easymode",
    "snes": "crt/crt-easymode", 
    "superfamicom": "crt/crt-easymode",
    "genesis": "crt/crt-easymode",
    "megadrive": "crt/crt-easymode",
    "c64": "crt/crt-easymode",
    "default": "crt/crt-easymode",
}

def generate_nostalgist_config(
    platform_slug: str,
    rom_path: str,
    core_name: str,
    system_bios: Optional[str] = None,
    shader: Optional[str] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Generate a nostalgist.js launch configuration.
    
    Args:
        platform_slug: The Showet platform identifier (e.g., 'nintendo_famicom')
        rom_path: Path or URL to the ROM file
        core_name: The RetroArch core name used by Showet
        system_bios: Optional path to BIOS file
        shader: Optional shader preset name
        
    Returns:
        Dictionary suitable for Nostalgist.launch() in JavaScript
    """
    # Map Showet core to nostalgist core
    mapped_core = CORE_MAPPING.get(core_name, core_name.replace("_libretro", "").replace("genesis_plus_gx_libretro", "genesis_plus_gx"))
    
    config: Dict[str, Any] = {
        "core": mapped_core,
        "rom": rom_path,
    }
    
    if system_bios:
        config["systemFiles"] = system_bios
        
    if shader:
        config["shader"] = shader
    else:
        # Infer shader from platform
        slug_lower = platform_slug.lower()
        for key, shader_name in SHADER_MAP.items():
            if key in slug_lower:
                config["shader"] = shader_name
                break
        else:
            config["shader"] = SHADER_MAP["default"]
    
    # Add any additional options
    config.update(kwargs)
    
    return config

def parse_platform_module(filepath: Path) -> Optional[Dict[str, Any]]:
    """Parse a Platform_*.py file to extract configuration."""
    content = filepath.read_text()
    
    # Extract platform slug from __init__ call
    slug_match = re.search(r'super\(\).__init__\("([^"]+)"', content)
    if not slug_match:
        return None
    
    slug = slug_match.group(1)
    
    # Extract core from cores list
    cores_match = re.search(r'cores\s*=\s*\[([^\]]+)\]', content)
    core = cores_match.group(1).strip().strip("'\"") if cores_match else None
    
    return {
        "slug": slug,
        "core": core,
        "file": filepath.name
    }

def generate_batch_configs(
    platforms_dir: Path,
    output_dir: Path,
    rom_base_url: Optional[str] = None
) -> List[str]:
    """
    Generate nostalgist configs for all platform modules.
    
    Args:
        platforms_dir: Directory containing Platform_*.py files
        output_dir: Directory to write JSON configs
        rom_base_url: Optional base URL for ROM files
        
    Returns:
        List of generated config file names
    """
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
        
        config = generate_nostalgist_config(
            platform_slug=slug,
            rom_path=rom_base_url or f"/roms/{slug}/",
            core_name=core,
            style={"backgroundColor": "black", "width": "100%", "height": "100%"}
        )
        
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
    
    print(f"📺 nostalgist.js integration ready!")
    print(f"Generated {len(configs)} configs in nostalgist_configs/")
    print(f"Point ROM URLs to your demo files and serve these configs to the frontend.")
    if configs:
        print(f"\nSample configs: {configs[:5]}")