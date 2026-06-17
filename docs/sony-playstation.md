# Sony PlayStation Platform Documentation

## Overview
The Sony PlayStation marked the transition to 32-bit CD-based demos. Known for full-motion video, CD audio, and advanced 3D graphics.

## Emulation Setup

### Required Binaries
- **PCSX-ReARMed** - Recommended for Raspberry Pi/Linux
- **DuckStation** - Modern, high compatibility
- **RetroArch** - `mednafen_psx_libretro.so` core

### Installation
```bash
# Ubuntu/Debian
sudo apt install pcsxr

# macOS
brew install pcsx-redux

# Using RetroArch
showet-executor demo.cue --download-cores
```

## Platform Configuration
Located at: `nostalgist_configs/sony_psx.json`

```json
{
  "core": "pcsx_rearmed",
  "shader": "crt/crt-royale",
  "extensions": [".bin", ".cue", ".iso", ".img", ".mdf"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.bin/.cue` | CDRWIN image - Most common | CD-ROM |
| `.iso` | ISO image - Direct burn | CD-ROM |
| `.img/.ccd` | CloneCD image - Subchannel data | CD-ROM |
| `.mdf/.mds` | Alcohol image - Mixed mode | CD-ROM |

## Notable Demos

### PlayStation Scene
- **Zero Motion** by Necros - First PSX demo
- **The Third Eye** - FMV showcase
- **Beats of Rage** - Homebrew scene
- **YOPPP!** by OXYGENE - French demo scene
- **RealityXL** by Nerve - Modern PSX

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.cue --platform sony_psx

# Using CLI
showet --demo 12345 --platform sony_psx

# Museum mode
showet-museum --platform sony_psx
```

## BIOS Requirements

### Required Files (Commercial)
Place in `~/.config/retroarch/system/` or emulator BIOS folder:
- `scph5500.bin` - Japanese BIOS
- `scph5501.bin` - USA BIOS
- `scph5502.bin` - European BIOS

### Boot Sequence
PlayStation boots with:
- White Sony logo
- Memory card check
- CD-ROM spin-up

## CRT Settings
- **Shader**: CRT-Royale (composite/RGB)
- **Curvature**: 0.05 (flat CRT monitor)
- **Scanlines**: Subtle for crisp PSX look
- **Aspect**: 4:3 (standard TV) or 16:9 (widescreen modes)