# Commodore Amiga Platform Documentation

## Overview
The Amiga defined the demoscene with its advanced graphics and audio capabilities. Showet supports all major Amiga models through FS-UAE and VICE.

## Emulation Setup

### Required Binaries
- **FS-UAE** - Recommended for Amiga 500/1200 demos
- **WinUAE** - Windows-only, highest accuracy
- **UAE4ARM** - Raspberry Pi optimized
- **RetroArch** - `puae_libretro.so` core

### Installation
```bash
# Ubuntu/Debian
sudo apt install fs-uae

# macOS
brew install fs-uae

# Kickstart ROMs required (not included)
# Place in ~/.fs-uae/Kickstarts/
```

## Platform Configuration
Located at: `nostalgist_configs/commodore_amiga.json`

```json
{
  "core": "puae, fsuae, uae4arm",
  "shader": "crt/crt-royale",
  "extensions": [".adf", ".hdf", ".lha"]
}
```

## Amiga Models

| Model | Best For | Configuration |
|-------|----------|-------------|
| A500 | Classic demos (90s era) | 68000, 1MB Chip RAM |
| A1200 | AGA demos (late 90s) | 68020, 2MB Fast RAM |
| A4000 | High-end productions | 68040, maximum RAM |
| CD32 | CD-based demos | A1200 + CD-ROM support |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.adf` | Amiga Disk File - Bootable demos | Amiga floppy |
| `.hdf` | Hard Drive Image - Full installations | Amiga hard drive |
| `.lha` | Compressed archive - Common in scene | Extract then run |
| `.exe` | Amiga executable - Self-extracting | AmigaOS |

## Notable Demos

### Hall of Fame
- **Second Reality** by Future Crew - The legendary demo (Score: 94.0)
- **Jesus on E's** by Sanity - Amiga's finest moment
- **Arte** by Sanity - Stunning visuals
- **9 Fingers** by Spaceballs - Classic Amiga demo
- **Desert Dream** by Kefrens - Pioneering techniques

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.adf --platform commodore_amiga

# Using CLI
showet --demo 12345 --platform commodore_amiga

# Museum mode
showet-museum --platform commodore_amiga
```

## Audio Integration

### Paula Chip Sound
- **4-channel stereo** native
- **MOD/XM/S3M** module support
- **AHI** audio drivers for modern sound cards

### Integration with ModArchive
```bash
# Download Amiga music modules
showet-archive --download-url "https://modarchive.org/.../module.xm"
```

## CRT Settings
- **Shader**: CRT-Royale (RGB monitor feel)
- **Curvature**: 0.05 (subtle)
- **Scanlines**: Visible for authentic CRT look
- **Phosphor Bloom**: Enabled for bright pixel glow

## WHDLoad Support
WHDLoad packages are fully supported for easy demo installation.

## Kickstart ROM Requirements
Amiga emulation requires Kickstart ROM files:
- Kickstart 1.3 - For A500 compatibility
- Kickstart 3.1 - For A1200/CD32 demos

Place ROMs in `~/.fs-uae/Kickstarts/` or configure in `fs-uae.conf`.