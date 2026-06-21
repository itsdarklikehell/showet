# Commodore CBM-II Platform Documentation

## Overview
Commodore CBM-II (CBM600/700) is a business computer from 1982-83. Part of the CBM-II series with unique keyboard and BASIC.

## Emulation Setup

### Required Binaries
- **VICE** - Primary emulator (x64)
- **RetroArch (vice_x64_libretro)** - Libretro core

## Platform Configuration
Located at: `nostalgist_configs/commodore_cbmii.json`

```json
{
  "core": "vice_x64",
  "shader": "crt/crt-easymode",
  "extensions": [".d64", ".t64", ".prg", ".zip"]
}
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet)*