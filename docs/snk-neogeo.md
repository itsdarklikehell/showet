# Neo Geo Platform Documentation

## Overview
SNK Neo Geo is an arcade/home console hybrid from 1990. Featured in the demoscene for homebrew productions and technical demos pushing arcade hardware limits.

## Emulation Setup

### Required Binaries
- **RetroArch (fbneo_libretro)** - Primary emulator
- **FinalBurn Neo** - Standalone emulator
- **MAME** - Alternative

### Installation
```bash
sudo apt install retroarch mame
```

## Platform Configuration
Located at: `nostalgist_configs/snk_neogeo.json`

```json
{
  "core": "fbneo",
  "shader": "crt/crt-royale",
  "extensions": [".zip", ".neo", ".cue"]
}
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet)*