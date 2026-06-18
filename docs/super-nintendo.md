# Super Nintendo/Super Famicom Platform Documentation

## Overview
The Super Nintendo/Super Famicom brought 16-bit graphics and advanced sound to the demoscene. Known for Mode 7 effects, SPC700 audio, and stunning visual demos.

## Emulation Setup

### Required Binaries
- **Snes9x** - Recommended, accurate
- **bsnes/higan** - Cycle-accurate
- **RetroArch** - `snes9x_libretro.so` or `bsnes_libretro.so` core

### Installation
```bash
# Ubuntu/Debian
sudo apt install snes9x

# macOS
brew install snes9x

# Using RetroArch
showet-executor demo.sfc --download-cores
```

## Platform Configuration
Located at: `nostalgist_configs/nintendo_snes.json`

```json
{
  "core": "snes9x",
  "shader": "crt/crt-pi",
  "extensions": [".smc", ".sfc", ".fig", ".swc", ".bs"]
}
```

## Console Models

| Model | Region | Notes |
|-------|--------|-------|
| Super Famicom | Japan | Original |
| Super Nintendo | USA/Europe | Different shell |
| SNES Mini | Global | Emulation-based |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.smc`/`.sfc` | Standard ROM - Most common | Cartridge |
| `.fig`/`.swc` | Multi-cart format | Special |
| `.bs` | Broadcast Satellaview | BS-X |

## Notable Demos

### SNES Scene
- **Bad Apple!!** - Famous black/white video
- **Star Ocean** - 48 megabit monster
- **SD Gundam** - Capcom sprite work
- **Shonen Jump** - Manga-style demos

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.smc --platform nintendo_snes

# Using CLI
showet --demo 12345 --platform nintendo_snes
```

## SPC700 Audio

### Sound Specs
- 8-channel ADPCM (BRR format)
- Echo and ADSR envelopes
- Sample-based chiptunes

### Integration with ModArchive
SNES demos use:
- SPC packs for music
- BRR samples

## CRT Settings
- **Shader**: CRT-PI (composite NTSC)
- **Curvature**: 0.08
- **Scanlines**: Medium for CRT TV feel
- **Aspect**: 4:3 (standard)