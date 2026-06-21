# Nintendo Virtual Boy Platform Documentation

## Overview
Nintendo Virtual Boy is a unique VR-like console from 1995 with red wireframe 3D graphics. Featured in the demoscene for technical homebrew demos.

## Emulation Setup

### Required Binaries
- **RetroArch (mednafen_vb_libretro)** - Primary emulator
- **Mednafen** - Native emulator

### Installation
```bash
sudo apt install retroarch mednafen
```

## Platform Configuration
Located at: `nostalgist_configs/nintendo_virtualboy.json`

```json
{
  "core": "mednafen_vb",
  "shader": "crt/crt-easymode",
  "extensions": [".vb", ".zip"]
}
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet)*