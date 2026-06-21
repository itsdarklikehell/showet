# PC-Engine / TurboGrafx-16 Platform Documentation

## Overview
NEC PC-Engine (TurboGrafx-16 in US) is an 8-bit console with 16-bit capabilities from 1987. Featured in the demoscene for HuC6270 video chip demos.

## Emulation Setup

### Required Binaries
- **RetroArch (mednafen_pce_fast_libretro)** - Primary emulator
- **Mednafen** - Native emulator

### Installation
```bash
sudo apt install retroarch mednafen
```

## Platform Configuration
Located at: `nostalgist_configs/nec_pcengine.json`

```json
{
  "core": "mednafen_pce_fast",
  "shader": "crt/crt-easymode",
  "extensions": [".pce", ".cue", ".bin", ".zip"]
}
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet)*