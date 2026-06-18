# Atari 2600/VCS Platform Documentation

## Overview
The Atari 2600 (Video Computer System) launched the cartridge-based console era. Demoscene pushed the 6507 CPU to produce impressive raster effects and sound.

## Emulation Setup

### Required Binaries
- **Stella** - Recommended, accurate
- **RetroArch** - `stella_libretro.so` core
- **BizHawk** - Multi-system with debugging

### Installation
```bash
# Ubuntu/Debian
sudo apt install stella

# macOS
brew install stella

# Using RetroArch
showet-executor demo.a26 --download-cores
```

## Platform Configuration
Located at: `nostalgist_configs/atari_2600.json`

```json
{
  "core": "stella",
  "shader": "crt/crt-pi",
  "extensions": [".a26", ".bin"]
}
```

## Console Models

| Model | Year | Notes |
|-------|------|-------|
| Atari 2600 | 1977 | Original VCS |
| Atari 2600 VCS | 1980 | Refreshed design |
| Atari Jr. | 1986 | Smaller, cost-reduced |
| 2600 Plug & Play | 2000s | Modern re-releases |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.a26` | Atari 2600 ROM - Standard | Cartridge |
| `.bin` | Raw binary - Homebrew | 2600 format |

## Notable Demos

### Homebrew Scene
- **Made in Russia** - Modern 2600 democoders
- **Z280** - Z80-like extensions
- **Boulder Dash** - Homebrew excellence
- **Okie Dokie** - Smooth scrolling demo

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.a26 --platform atari_2600

# Using CLI
showet --demo 12345 --platform atari_2600
```

## CRT Settings
- **Shader**: CRT-PI (composite NTSC artifacts)
- **Curvature**: 0.1
- **Scanlines**: Visible for CRT TV feel
- **Aspect**: 4:3 with overscan (160x192 resolution)