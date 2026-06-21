# Phillips CD-i Platform Documentation

## Overview
Phillips CD-i (Compact Disc Interactive) is a rare multimedia console from the early 90s. While not traditionally a demoscene platform, it has unique hardware capabilities and some experimental demo productions.

## Emulation Setup

### Required Binaries
- **RetroArch (bluemsx_libretro)** - Primary emulator
- **MESS/MAME** - Alternative emulator

### Installation
```bash
# Ubuntu/Debian
sudo apt install retroarch mame

# Verify core
ls /usr/lib/*/libretro/*cdi* 2>/dev/null || echo "CD-i core may need manual install"
```

## Platform Configuration
Located at: `nostalgist_configs/phillips_cdi.json`

```json
{
  "core": "bluemsx",
  "shader": "crt/crt-royale",
  "extensions": [".cue", ".bin", ".iso", ".zip"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .cue/.bin | CD-ROM image | RetroArch |
| .iso | ISO image | RetroArch/MAME |
| .zip | Archive | Extract then run |

## Running Demos

### Using Showet
```bash
# Run local file
showet-executor /path/to/demo.cue --platform phillips_cdi

# Note: Limited demo availability for this platform
```

## CRT Settings
- **Shader**: CRT-Royale (authentic mid-90s CRT)
- **Curvature**: Moderate
- **Scanlines**: Standard NTSC scanlines
- **Phosphor Bloom**: Light bloom effect

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*