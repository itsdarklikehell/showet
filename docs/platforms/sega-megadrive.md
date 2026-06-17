# Sega Megadrive/Genesis Platform Documentation

## Overview
The Sega Megadrive/Genesis was a demo scene powerhouse in the 16-bit console wars. Known for impressive pushing of the hardware, including raster effects and FM synthesis.

## Emulation Setup

### Required Binaries
- **Genesis Plus GX** - Recommended, libretro version
- **Picodrive** - Fast with good compatibility
- **RetroArch** - `genesis_plus_gx_libretro.so` core
- **Gens** - Windows-focused, good debugger

### Installation
```bash
# Ubuntu/Debian
sudo apt install mednafen

# Using RetroArch
# Core auto-downloads with --download-cores flag
showet-executor demo.md --download-cores
```

## Platform Configuration
Located at: `nostalgist_configs/sega_megadrive.json`

```json
{
  "core": "genesis_plus_gx",
  "shader": "crt/crt-easymode",
  "extensions": [".md", ".bin", ".gen", ".cue"]
}
```

## Console Models

| Model | Region | Unique Features |
|-------|--------|-----------------|
| Megadrive | Japan/Europe | 50Hz, RGB output |
| Genesis | USA | 60Hz, lockout chip |
| WonderMega | Japan | X-ray mode |
| Sega CD | Add-on | CD audio, extra RAM |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.md/.gen/.bin` | Raw ROM - Most common | Cartridge |
| `.cue/.bin` | CD image - Sega CD demos | Sega CD |
| `.sms` | Master System - Backward compatible | MS mode |

## Notable Demos

### Hall of Fame
- **Bad Apple!!** - Famous PDM video
- **Red Zone** by Touko Paraiso - Masterpiece
- **Overdrive** by Resistance - Technical demo
- **Overdrive 2** by Resistance - Sequel excellence
- **Limp Brains** by Hokuto Force - Modern scene

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.bin --platform sega_megadrive

# Using CLI
showet --demo 12345 --platform sega_megadrive

# Museum mode
showet-museum --platform sega_megadrive
```

## Sound Integration

### YM2612 FM Synthesis
- 6 channels + 1 DAC
- PCM sample playback
- Stunning for 16-bit console

### Integration with ModArchive
Sega demos often use MOD format for music - auto-linked via `showet-archive --download`.

## CRT Settings
- **Shader**: CRT-Easymode (composite/RGB)
- **Curvature**: 0.08
- **Scanlines**: Visible for authentic 90s feel
- **Composite**: Optional for TV output simulation

## SRAM & Backup Memory
Support for save RAM:
- `.srm` files auto-created
- Battery-backed SRAM for high scores
- EEPROM for Sega CD demos

## Region Considerations
- **PAL** (Europe) - 50Hz, more borders
- **NTSC** (USA/Japan) - 60Hz, full screen
- Auto-detect via `--region ntsc/pal/auto`