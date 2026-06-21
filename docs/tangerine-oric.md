# Oric (Tangerine) Platform Documentation

## Overview
Tangerine Oric is a British 8-bit home computer from 1983. Featured in the demoscene for its distinctive sound and unique graphics mode.

## Emulation Setup

### Required Binaries
- **RetroArch (oric_libretro)** - Primary emulator
- **Oricutron** - Native emulator

### Installation
```bash
# Ubuntu/Debian
sudo apt install retroarch

# Check core
ls /usr/lib/*/libretro/oric* 2>/dev/null
```

## Platform Configuration
Located at: `nostalgist_configs/tangerine_oric.json`

```json
{
  "core": "oric",
  "shader": "crt/crt-pi",
  "extensions": [".tap", ".wav", ".zip"]
}
```

## Demo Types & Formats

| Format | Description |
|--------|-------------|
| .tap | Tape image format |
| .wav | Tape audio format |
| .dsk | Disk image |

## Running Demos

### Using Showet
```bash
showet run /path/to/demo.tap --platform oric
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*