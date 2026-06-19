# Atari 2600/VCS Platform Documentation

## Overview
Atari 2600 (VCS - Video Computer System) platform for running retro demos with authentic presentation. The console that started it all with its revolutionary cartridge-based system and TIA graphics chip.

## Emulation Setup

### Required Binaries
- **Stella** - Primary native emulator (recommended)
- **RetroArch (stella_libretro)** - Libretro core option

### Installation
```bash
# Ubuntu/Debian
sudo apt install stella

# macOS
brew install stella

# Or download from https://stella.sourceforge.net
```

## Platform Configuration
Located at: `nostalgist_configs/atari_2600.json`

```json
{
  "core": "stella2014_libretro",
  "shader": "crt/crt-royale",
  "extensions": [".a26", ".bin", ".zip"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .a26 | Atari 2600 ROM - Standard format | Stella emulator |
| .bin | Binary ROM - Alternative extension | Stella emulator |
| .zip | Compressed archive - Common distribution | Extract then run |
| .caf | Atari 2600 Advanced Sound Format | Stella with ASF support |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file with auto-detection
showet-universal /path/to/demo.a26

# Run in museum mode
showet-museum --platform atari_2600

# Run in jukebox mode
showet-jukebox --ids 12345 --repeat all

# Extract archive then run
showet-archive --extract demo.zip && showet-universal demo/
```

## CRT Settings
- **Shader**: CRT-Royale (authentic CRT TV look)
- **Curvature**: 0.15 (moderate barrel effect)
- **Scanlines**: Visible with chromatic aberration
- **Phosphor Bloom**: Enabled for fuzzy TV look
- **Aspect Ratio**: 4:3 (standard TV)

## Troubleshooting

### Common Issues
1. **No scanlines** - Enable CRT-Royale shader in RetroArch
2. **Fast execution** - Set frame rate to 60Hz NTSC or 50Hz PAL
3. **Color issues** - Check NTSC/PAL mode matches ROM

## Notable Demos

- **Oystr!** by DraftMan - Modern 2600 demo scene
- **Melvin** by Reindeer - Graphics showcase
- **Robotic Attack** by Out Of The Ashes - Recent production
- **Tornado** by AtariBlast - Assembly demo

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
*Atari 2600 preservation courtesy of the Stella emulator team*
