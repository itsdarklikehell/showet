# Commodore 64 Platform Documentation

## Overview
The Commodore 64 is the most iconic computer in demoscene history, with thousands of legendary productions. Showet provides native VICE integration with CRT authenticity.

## Emulation Setup

### Required Binaries
- **VICE** (recommended) - `x64sc` for authentic C64 experience
- **RetroArch** - `x64_libretro.so` core for browser integration
- **CCS64** - Alternative emulator, Windows-only

### Installation
```bash
# Ubuntu/Debian
sudo apt install vice

# macOS (Homebrew)
brew install vice

# Using RetroArch
# Download x64_libretro.so to retroarch/cores/
```

## Platform Configuration
Located at: `nostalgist_configs/commodore_64.json`

```json
{
  "core": "vice_x64sc",
  "shader": "crt/crt-easymode",
  "extensions": [".d64", ".t64", ".prg", ".crt", ".tap"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.d64` | Disk image - Most common | Original C64 floppy |
| `.t64` | Tape image - For tape-loaded demos | Original C64 tape |
| `.prg` | Program file - Direct executable | Runs directly |
| `.crt` | Cartridge - Most authentic hardware feel | C64 cartridge port |
| `.tap` | Tape image - Higher fidelity than T64 | Original C64 tape |

## Notable Demos

### Hall of Fame
- **Second Reality** by Future Crew - The pinnacle (Score: 94.0)
- **Unreal** by Future Crew - Graphics masterpiece
- **State of the Art** by Spaceballs - Disk magazine
- **The Last Hope** by Censor Design - Modern C64 demo
- **Legion** by Censor Design - Stereo SID effects

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.d64

# Using CLI
showet --demo 12345 --platform commodore_64

# Museum mode auto-rotation
showet-museum --platform commodore_64
```

## Sound Themes
Enable authentic C64 SID sounds in `sound_design/showet-sound-theme-manager.js`:
- **SID Chip** - Authentic MOS 6581/8580 emulation
- **Disk Drive** - 1541 floppy seek sounds
- **Keyboard Click** - VIC-20 style typing feedback

## CRT Settings
- **Shader**: CRT-Easymode (authentic composite monitor)
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible, 50% opacity
- **Phosphor Bloom**: Enabled for authentic glow

## Troubleshooting

### Common Issues
1. **No SID sound** - Check if VICE was compiled with SID support
2. **Wrong colors** - PAL vs NTSC demo mismatch
3. **Cannot run** - Missing `kernal` ROM file (copyrighted)

### PAL vs NTSC
Many demos are region-specific:
- **PAL** (Europe) - Slower but more colors
- **NTSC** (USA) - Faster but fewer colors

Showet auto-detects from demo metadata when available.