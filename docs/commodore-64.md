# Commodore 64 Platform Documentation

## Overview
Commodore 64 platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- **VICE (x64sc)** - Primary native emulator
- **RetroArch (vice_x64sc)** - Libretro core option

### Installation
```bash
# Ubuntu/Debian
sudo apt install vice

# macOS
brew install vice

# Or download from https://vice-emu.sourceforge.io
```

## Platform Configuration
Located at: `nostalgist_configs/commodore_64.json`

```json
{
  "core": "vice_x64sc_libretro",
  "shader": "crt/crt-easymode",
  "extensions": [".d64", ".t64", ".prg", ".crt", ".tap"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .d64 | Disk image - Most common format | VICE emulates original floppy |
| .t64 | Tape image - For tape-loaded demos | Commodore tape loading |
| .prg | Program file - Direct executable | Runs directly in emulator |
| .crt | Cartridge image - Fast loaders | VICE with cartridge support |
| .tap | Tape image - Original format | VICE tape loading |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.d64

# Run in museum mode
showet-museum --platform commodore_64

# Run in jukebox mode with loop detection
showet-jukebox --ids 12345  --repeat all

# Find C64 music modules
showet-modarchive-enhanced jukebox-modules commodore_64
```

## CRT Settings
- **Shader**: CRT-Easymode
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible with flicker
- **Phosphor Bloom**: Enabled for authentic glow

## Troubleshooting

### Common Issues
1. **No SID sound** - Check if VICE was compiled with SID support
2. **Wrong colors** - PAL vs NTSC demo mismatch
3. **Cannot run** - Missing kernal ROM file (included in most VICE packages)
4. **Fastloader issues** - Some demos require JiffyDOS or other fastloaders

## Notable Demos

- **Second Reality** by Future Crew - The pinnacle
- **Unreal** by Future Crew - Graphics masterpiece
- **State of the Art** by Spaceballs - Disk magazine
- **Tangent** by Conspiracy - Modern C64 demo

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
