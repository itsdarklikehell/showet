# PC-98 Platform Documentation

## Overview
NEC PC-98 is a Japanese computer platform popular in the demoscene for its unique FM synthesis and portrait screen orientation. Known for distinctive visual styles and chiptune music.

## Emulation Setup

### Required Binaries
- **RetroArch (mednafen_pc98_libretro)** - Primary emulator
- **Neko Project II** - Alternative native emulator

### Installation
```bash
# Ubuntu/Debian
sudo apt install retroarch

# PC-98 core should be available
# Check: ls /usr/lib/*/libretro/mednafen_pc98_libretro.so
```

## Platform Configuration
Located at: `nostalgist_configs/nec_pc98.json`

```json
{
  "core": "mednafen_pc98",
  "shader": "crt/crt-pi",
  "extensions": [".d98", ".zip", ".hdi", ".fdd"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .d98 | PC-98 executable | RetroArch |
| .zip | Archive | Extract then run |
| .hdi | Hard disk image | RetroArch |
| .fdd | Floppy disk image | RetroArch |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.hdi --platform nec_pc98

# Run in jukebox mode
showet-jukebox --ids 12345 --platform nec_pc98
```

## CRT Settings
- **Shader**: CRT-Pi (vertical scanlines)
- **Curvature**: Minimal for modern CRT feel
- **Scanlines**: Thin horizontal scanlines
- **Aspect Ratio**: 4:3 (portrait PC-98 mode)

## Troubleshooting

### Common Issues
1. **Japanese text** - PC-98 uses Shift-JIS encoding
2. **Sound issues** - Enable PC-98 FM synthesis in core settings
3. **Performance** - Lower CPU clock in RetroArch settings

## Notable Demos

- **Sorcerian** series
- **FTML** series by MA project
- **Hudson** demos
- Various doujin software productions

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*