# MS-DOS Platform Documentation

## Overview
MS-DOS PC demos represent the transition to modern PC hardware with VGA, SVGA, and early 3D acceleration. Showet uses DOSBox-X for authentic reproduction.

## Emulation Setup

### Required Binaries
- **DOSBox-X** - Recommended (enhanced DOSBox)
- **DOSBox** - Standard version
- **Boxer** - macOS-native DOSBox
- **RetroArch** - `dosbox_libretro.so` core

### Installation
```bash
# Ubuntu/Debian
sudo apt install dosbox-x

# macOS
brew install dosbox-x

# Using RetroArch
# Download dosbox_libretro.so to retroarch/cores/
```

## Platform Configuration
Located at: `nostalgist_configs/microsoft_msdos.json`

```json
{
  "core": "dosbox_core",
  "shader": "crt/crt-pi",
  "extensions": [".exe", ".com", ".bat", ".zip"]
}
```

## Hardware Requirements

| Era | CPU | RAM | Graphics | Sound |
|-----|-----|-----|----------|-------|
| Early (1990-1993) | 286-386 | 1-4MB | CGA/EGA/VGA | AdLib/OPL |
| Mid (1994-1996) | 486-Pentium | 4-8MB | VGA/SVGA | Sound Blaster |
| Late (1997-2000) | Pentium MMX | 16-32MB | VESA | SB16/AWE32 |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.exe` | Native executable - Most common | MS-DOS |
| `.com` | 16-bit executable - Small demos | MS-DOS |
| `.bat` | Batch file - Often with TSR | MS-DOS shell |
| `.zip` | Archive - Extract first | Various |

## Notable Demos

### Hall of Fame
- **Second Reality** by Future Crew - Pinnacle (Score: 94.0)
- **Verses** by Conspiracy - Modern PC excellence
- **Heaven Seven** by Loveboat - Classic PC demo
- **System Satisfaction** by Kewlers - 3D-accelerated
- **Iconoclast** by ASD - Technical showcase

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.exe --platform dos

# Using CLI
showet --demo 12345 --platform microsoft_msdos

# Auto-extract and run
showet-executor /path/to/demo.zip --platform dos
```

## Sound Cards

### Supported Cards
- **Sound Blaster** (SB16/AWE32) - Most common
- **Gravis UltraSound** (GUS) - High-quality samples
- **AdLib/OPL** - FM synthesis classic
- **Roland MT-32** - MIDI module synth

### DOSBox Configuration
```ini
[sblaster]
sbtype=sb16
sbbase=220
irq=7
dma=1

[gus]
gus=false
```

## CRT Settings
- **Shader**: CRT-PI (accurate VGA monitor)
- **Curvature**: 0.08 (typical CRT)
- **Scanlines**: Strong for authentic look
- **Phosphor Bloom**: Moderate for VGA feel

## DOS Extenders & Requirements

Many demos require:
- **DOS/4GW** - Protected mode extender
- **CWSDPMI** - DOS extender for 32-bit
- **UniVBE** - Universal VESA driver

These are auto-injected by Showet when detected in archives.