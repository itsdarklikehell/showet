# 3DO Platform Documentation

## Overview
Panasonic 3DO Interactive Multiplayer is a CD-based console from 1993. Featured in the demoscene for technical demos and homebrew productions.

## Emulation Setup

### Required Binaries
- **RetroArch (opera_libretro)** - Primary emulator
- **Opera** - Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/panasonic_3do.json`

```json
{
  "core": "opera",
  "shader": "crt/crt-royale",
  "extensions": [".iso", ".cue", ".bin", ".zip"]
}
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet)*