# PC-FX Platform Documentation

## Overview
NEC PC-FX is a Japanese gaming console released in 1994, featuring advanced 2D graphics capabilities and CD-ROM storage. Popular in the demoscene for its unique visual effects and HuC6270 video chip.

## Emulation Setup

### Required Binaries
- **RetroArch (mednafen_pcfx_libretro)** - Primary emulator
- **Mednafen** - Native alternative

### Installation
```bash
# Ubuntu/Debian
sudo apt install retroarch mednafen

# Verify core
ls /usr/lib/*/libretro/mednafen_pcfx_libretro.so
```

## Platform Configuration
Located at: `nostalgist_configs/nec_pcfx.json`

```json
{
  "core": "mednafen_pcfx",
  "shader": "crt/crt-easymode",
  "extensions": [".cue", ".bin", ".iso", ".zip"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .cue/.bin | CD-ROM image | RetroArch/Mednafen |
| .iso | ISO CD image | RetroArch/Mednafen |
| .zip | Archive | Extract then run |

## Running Demos

### Using Showet
```bash
# Run local file
showet-executor /path/to/demo.cue --platform nec_pcfx

# Check for demos
showet-spotlight --platform nec_pcfx
```

## CRT Settings
- **Shader**: CRT-Easymode (authentic 90s CRT)
- **Curvature**: Moderate barrel effect
- **Scanlines**: Visible horizontal lines
- **Phosphor Bloom**: Enabled for glow effect

## Troubleshooting

### Common Issues
1. **BIOS required** - Place PC-FX ROM in RetroArch system folder
2. **Slow loading** - Enable fast CD loading in core options
3. **Audio crackling** - Adjust sound buffer size in RetroArch

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*