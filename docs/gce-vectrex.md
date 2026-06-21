# Vectrex Platform Documentation

## Overview
GCE Vectrex is a unique home console from 1982 featuring vector display and built-in screen. Has a cult following in the demoscene for its distinctive monochrome vector graphics.

## Emulation Setup

### Required Binaries
- **RetroArch (vecx_libretro)** - Primary emulator
- **VecX** - Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/gce_vectrex.json`

```json
{
  "core": "vecx",
  "shader": "crt/crt-easymode",
  "extensions": [".vec", ".bin", ".zip"]
}
```

## Demo Types & Formats
- .vec - Vectrex cartridge ROM
- .bin - Binary ROM
- .zip - Archive

---
*Part of [Showet](https://github.com/itsdarklikehell/showet)*