# ZX Spectrum Platform Documentation

## Overview
The ZX Spectrum was the UK's premier home computer, birthplace of the British demo scene. Known for its distinctive colored stripes loading screen and Z80 processor.

## Emulation Setup

### Required Binaries
- **Fuse** - Recommended, accurate emulation
- **RetroArch** - `fuse_libretro.so` core
- **ZXSpin** - Windows, good debugger
- **ZEsarUX** - Multi-platform, advanced features

### Installation
```bash
# Ubuntu/Debian
sudo apt install fuse-emulator-gtk

# macOS
brew install fuse
```

## Platform Configuration
Located at: `nostalgist_configs/sinclair_zxspectrum.json`

```json
{
  "core": "fuse",
  "shader": "crt/crt-pi",
  "extensions": [".tap", ".tzx", ".z80", ".szx"]
}
```

## Computer Models

| Model | Year | RAM | Features |
|-------|------|-----|----------|
| Spectrum 48K | 1982 | 48KB | Original |
| Spectrum 128K | 1985 | 128KB | More RAM, AY-3-8912 sound |
| Spectrum +2 | 1986 | 128KB | Built-in tape/floppy |
| Spectrum +3 | 1987 | 128KB | Floppy drive |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.tap` | Tape image - Authentic loading | Tape |
| `.tzx` | Turbo tape - Faster loading | Turbo tape |
| `.z80` | Snapshot - Instant load | Memory state |
| `.szx` | ZX-Spin - Advanced features | Emulator |

## Notable Demos

### Hall of Fame
- **Shinobi** by Rawwar - Famous loading stripes
- **Ziggy** by Rawwar - Technical showcase
- **Alone** by Rawwar - Multi-screen demo
- **Flash MX** by BS1 - Modern Speccy
- **Tales from the Loop** - Contemporary scene

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.tap --platform sinclair_zxspectrum

# Using CLI
showet --demo 12345 --platform sinclair_zxspectrum
```

## Sound Integration

### AY-3-8912 Chip
- 3-voice PSG (square waves)
- White noise generator
- Used in 128K models

### Integration with ModArchive
Spectrum demos often use:
- Turbo Sound FM mods
- Synthetic drum patterns

## CRT Settings
- **Shader**: CRT-PI (composite TV feel)
- **Curvature**: 0.1
- **Scanlines**: Visible for authentic CRT
- **Loading Stripes**: Simulated on black borders