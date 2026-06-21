# Saturn Platform Documentation

## Overview
Sega Saturn is a 32-bit console from 1994. Featured in the demoscene for homebrew 3D demos and technical productions.

## Emulation Setup

### Required Binaries
- **RetroArch (mednafen_saturn_libretro)** - Primary emulator
- **Mednafen** - Native emulator

### Installation
```bash
sudo apt install retroarch mednafen
```

## Platform Configuration
Located at: `nostalgist_configs/sega_saturn.json`

```json
{
  "core": "mednafen_saturn",
  "shader": "crt/crt-royale",
  "extensions": [".cue", ".bin", ".iso", ".zip"]
}
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet)*