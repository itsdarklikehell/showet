# Atari ST Platform Documentation

## Overview
The Atari ST was a cornerstone of the early demoscene, known for its affordability and the unique Yamaha YM2149F chip. Birthplace of groups like Equinox and The Exceptions.

## Emulation Setup

### Required Binaries
- **Hatari** - Recommended, full ST/STE support
- **AROS** - For full Atari TOS compatibility
- **RetroArch** - `hatari_libretro.so` core

### Installation
```bash
# Ubuntu/Debian
sudo apt install hatari

# macOS
brew install hatari
```

## Platform Configuration
Located at: `nostalgist_configs/atari_stettfalcon.json`

```json
{
  "core": "hatari",
  "shader": "crt/crt-royale",
  "extensions": [".st", ".msa", ".dim"]
}
```

## Atari Models

| Model | Year | CPU | RAM | Notes |
|-------|------|-----|-----|-------|
| ST | 1985 | 68000 | 512KB-4MB | Original |
| STE | 1989 | 68000 | 512KB-4MB | Blitter, better audio |
| Falcon | 1992 | 68030 | 4-14MB | 32-bit, DSP |
| TT | 1990 | 68030 | 4-16MB | 32-bit bus |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.st` | ST disk image - Most common | Floppy |
| `.msa` | Magic Shadow format - Compressed | MSA utility |
| `.dim` | Disk image - Various tools | DIM format |
| `.prg` | Executable - Direct run | TOS |

## Notable Demos

### Early Scene Milestones
- **The Paradox** by Equinorx - Falcon 030 masterpiece
- **The Chaos Engine** - STE raster effects
- **Transplantation** by SYNC - ST/E hybrid
- **Delirious** by The Exceptions - Early STE
- **Meat Mine** by Equinorx - STE scroller

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.st --platform atari_stettfalcon

# Using CLI
showet --demo 12345 --platform atari_stettfalcon

# Museum mode
showet-museum --platform atari_stettfalcon
```

## Sound Integration

### Yamaha YM2149F
- 3-voice PSG + 1 noise
- Stereo output via STE DMA
- Famous "ST sound" character

### YM2149 Chip Synth
Many demos use this chip for:
- Square wave bass
- Arpeggiated leads
- Noise percussion

## CRT Settings
- **Shader**: CRT-Royale (RGB monitor)
- **Curvature**: 0.05 (flat ST monitor)
- **Scanlines**: Subtle for crisp pixels
- **Aspect**: 4:3 locked (no overscan)

## TOS (The Operating System) Requirements

### ROM Files Needed
- **TOS 1.02** - Original ST ROM
- **TOS 2.06** - STE/Enhanced
- Place in `~/.hatari/tos.img`

### Memory Configuration
- **512KB** - Minimum for most demos
- **1MB** - Recommended for STE
- **14MB** - Falcon 030 full RAM