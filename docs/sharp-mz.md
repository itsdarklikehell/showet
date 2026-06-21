# Sharp MZ Platform Documentation

## Overview
Sharp MZ is a Japanese home computer series from the late 1970s-80s. Featured in the demoscene for its unique MZ-700 and MZ-800 series with distinctive monitor design.

## Emulation Setup

### Required Binaries
- **RetroArch (mz800em_libretro)** - Primary emulator
- **MZ800Emu** - Native emulator

### Installation
```bash
# Ubuntu/Debian
sudo apt install retroarch

# Check core
ls /usr/lib/*/libretro/mz800* 2>/dev/null
```

## Platform Configuration
Located at: `nostalgist_configs/sharp_mz.json`

```json
{
  "core": "mz800em",
  "shader": "crt/crt-easymode",
  "extensions": [".mzt", ".m12", ".zip"]
}
```

## Demo Types & Formats

| Format | Description |
|--------|-------------|
| .mzt | Tape image format |
| .m12 | MZ-1200 format |
| .dsk | Disk image |

## Running Demos

### Using Showet
```bash
showet run /path/to/demo.mzt --platform sharp_mz
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*