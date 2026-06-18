# Television Simulator '99 Integration Guide

Television Simulator '99 (TVS99) is the frontend for nostalgist.js that provides authentic CRT TV effects for demo playback in the browser.

## Quick Start

```bash
# Generate nostalgist configs
python3 nostalgist_bridge.py

# Generate manifest
python3 generate_manifest.py

# Serve the frontend
python3 -m http.server 8000

# Open in browser
# http://localhost:8000/showet-showcase.html
```

## Project Structure

```
nostalgist_configs/         # JSON configs for each platform
├── commodore_64.json      # C64 config with core, shader, extensions
├── nintendo_famicom.json  # NES config  
├── manifest.json          # Full platform list for frontend
└── ...                   # 84 platform configs

showet-showcase.html       # Main demo showcase page
showet-nostalgist-loader.js # JavaScript loader for demos
showet-crt-shader.js     # CRT effect shaders
showet-boot-sequence.js  # OS boot animations
showet-audio.js          # Retro sound effects
```

## TVS99 Features

### Visual Effects
- **CRT Curvature** - Barrel distortion simulation
- **Scanlines** - Phosphor scanline overlay
- **Phosphor Bloom** - Authentic TV glow effect
- **Chromatic Aberration** - CRT color separation
- **Static Noise** - Period-authentic interference

### OSD Effects
- **Power LED** - System power indicator
- **Channel Numbers** - Channel selection overlay
- **V-Hold** - Vertical hold adjustment effect
- **Color Bars** - Calibration pattern

## nostalgist.js Integration

### Core Mappings

| RetroArch Core | nostalgist Core | Platforms |
|---------------|-----------------|-----------|
| vice_x64sc_libretro | vice_x64sc | Commodore 64 |
| puae_libretro | puae | Amiga |
| quicknes_libretro | quicknes | NES/Famicom |
| snes9x_libretro | snes9x | SNES/Super Famicom |
| genesis_plus_gx_libretro | genesis_plus_gx | Sega Genesis/Mega Drive |
| stella_libretro | stella | Atari 2600 |
| dosbox_libretro | dosbox | MS-DOS |
| pcsx_rearmed_libretro | pcsx_rearmed | PlayStation |

### Configuration Format

```json
{
  "core": "vice_x64sc",
  "rom": "/roms/commodore_64/demo.d64",
  "shader": "crt/crt-easymode",
  "extensions": ["d64", "t64", "prg"],
  "style": {
    "backgroundColor": "black",
    "width": "100%",
    "height": "100%"
  }
}
```

## Setup Requirements

### 1. RetroArch Installation

```bash
# Ubuntu/Debian
sudo apt install retroarch libretro-core

# macOS
brew install retroarch

# Or download from https://www.retroarch.com
```

### 2. nostalgist.js

Include in your HTML:

```html
<script src="https://cdn.jsdelivr.net/npm/nostalgist@latest/dist/nostalgist.min.js"></script>
```

### 3. CORS Configuration

For local demo files, serve via HTTP:

```bash
python3 -m http.server 8000
# Or use nginx with proper CORS headers
```

## Running Demos

### From Python

```python
from nostalgist_bridge import generate_nostalgist_config

config = generate_nostalgist_config(
    platform_slug="commodore_64",
    rom_path="/demos/second_reality.d64",
    core_name="vice_x64sc_libretro"
)

# Save to nostaldic_configs for frontend use
```

### From Command Line

```bash
# List available platforms
showet --platforms

# Generate all configs
python3 nostalgist_bridge.py

# View in browser
python3 -m http.server 8000
open http://localhost:8000/showet-showcase.html
```

## TVS99 Controls

- **1-9** - Select channel/platform
- **Enter** - Launch demo
- **F** - Fullscreen mode
- **S** - Shader selection
- **M** - Mute/Unmute
- **Space** - Pause emulation

## Troubleshooting

### Demo Won't Load
1. Check ROM path is accessible via HTTP
2. Verify core name exists in nostalgist
3. Check browser console for errors

### Slow Performance
1. Use HTTPS for better WASM performance
2. Lower canvas resolution
3. Disable shader for testing

### No Audio
1. Check browser autoplay policy
2. Click inside window first
3. Verify core supports audio

## Advanced Configuration

### Custom Shaders

Edit `shaders/custom.glsl` and reference in config:

```json
{
  "shader": "/shaders/custom.glsl"
}
```

### Loading Screen

Add boot sequence to platform configs:

```json
{
  "bootSequence": "amiga"  // Options: amiga, dos, c64, none
}
```

## Related Documentation

- [nostalgist.js API Docs](https://nostalgist.js.org/apis/launch/)
- [Libreto Shaders](https://github.com/libretro/common-shaders)
- [showet-showcase.html](showet-showcase.html) - Demo implementation