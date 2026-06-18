# Sega Master System Platform Documentation

## Overview
The Master System was Sega's 8-bit console with powerful VDP graphics. Strong demo scene in Europe and Brazil with impressive scrolling effects.

## Emulation Setup

### Required Binaries
- **Genesis Plus GX** - Recommended for RetroArch
- **RetroArch** - `genesis_plus_gx_libretro.so` core
- **MEKA** - Original with debugging
- **SMS Plus** - Accurate, multi-platform

### Installation
```bash
# Ubuntu/Debian
sudo apt install mednafen

# macOS
brew install mednafen

# Using RetroArch
showet-executor demo.sms --download-cores
```

## Platform Configuration
Located at: `nostalgist_configs/segasms.json`

```json
{
  "core": "genesis_plus_gx",
  "shader": "crt/crt-easymode",
  "extensions": [".sms", ".sg", ".bml", ".bin"]
}
```

## Console Models

| Model | Region | Notes |
|-------|--------|-------|
| Master System | Europe/US | Standard |
| Mark III | Japan | Original design |
| Master System II | Worldwide | Compact, no card slot |
| Sega Game 1000 | Australia | Bundled version |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.sms`/`.bin` | ROM image - Most common | Cartridge |
| `.sg` | SG-1000 backward compatible | Hybrid |
| `.bml` | BIOS Markup Language | Special |

## Notable Demos

### Scene Highlights
- **Power Strike** - European demo scene
- **The Last Ninja** - Music demo conversions
- **Alex Kidd** - Sprite demo excellence

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.sms --platform sega_master_system

# Using CLI
showet --demo 12345 --platform sega_master_system
```

## VDP Graphics

### Features
- 32 colors from 32768 palette
- 8x8 tile-based backgrounds
- Hardware scrolling
- Sprite zooming

## CRT Settings
- **Shader**: CRT-Easymode (RGB)
- **Curvature**: 0.06
- **Scanlines**: Subtle for sharp pixels
- **Aspect**: 4:3 with border