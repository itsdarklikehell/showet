# Enterprise EP128 Platform Documentation

## Overview
Enterprise Elan Enterprise 128 is a British 8-bit home computer from the 1980s. Featured in the demoscene for its unique graphics capabilities and Z80-based architecture.

## Emulation Setup

### Required Binaries
- **RetroArch (ep128emu_libretro)** - Primary emulator
- **EP128Emu** - Native emulator

### Installation
```bash
# Ubuntu/Debian
sudo apt install retroarch

# Check core availability
ls /usr/lib/*/libretro/ep128* 2>/dev/null || echo "Manual core installation may be needed"
```

## Platform Configuration
Located at: `nostalgist_configs/enterprise_ep128.json`

```json
{
  "core": "ep128emu",
  "shader": "crt/crt-easymode",
  "extensions": [".ep128", ".tap", ".wav", ".zip"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .ep128 | Enterprise executable | RetroArch/EP128Emu |
| .tap | Tape image | RetroArch/EP128Emu |
| .wav | Tape image (audio) | RetroArch/EP128Emu |
| .zip | Archive | Extract then run |

## Running Demos

### Using Showet
```bash
showet run /path/to/demo.ep128 --platform enterprise_ep128
```

## CRT Settings
- **Shader**: CRT-Easymode
- **Curvature**: Standard 8-bit curvature
- **Scanlines**: 60Hz PAL scanlines
- **Resolution**: 320x240 (bordered mode)

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*