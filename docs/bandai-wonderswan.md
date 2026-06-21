# WonderSwan Platform Documentation

## Overview
Bandai WonderSwan is a Japanese handheld console from 1999. Featured in the demoscene for homebrew productions and technical demos.

## Emulation Setup

### Required Binaries
- **RetroArch (mednafen_wswan_libretro)** - Primary emulator
- **Mednafen** - Native emulator

### Installation
```bash
sudo apt install retroarch mednafen
```

## Platform Configuration
Located at: `nostalgist_configs/bandai_wonderswan.json`

```json
{
  "core": "mednafen_wswan",
  "shader": "crt/crt-pi",
  "extensions": [".ws", ".wsc", ".zip"]
}
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet)*