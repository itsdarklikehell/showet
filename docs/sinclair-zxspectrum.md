# Sinclair ZX Spectrum Platform Documentation

## Overview
Sinclair ZX Spectrum platform for running retro demos with authentic presentation. The beloved British home computer that defined the European demoscene with its distinctive rubber keyboard and colorful attribute clash.

## Emulation Setup

### Required Binaries
- **Fuse** - Primary native emulator (recommended)
- **RetroArch (fuse_libretro)** - Libretro core option

### Installation
```bash
# Ubuntu/Debian
sudo apt install fuse

# macOS
brew install fuse

# Or download from https://fuse-emulator.sourceforge.net
```

## Platform Configuration
Located at: `nostalgist_configs/sinclair_zxspectrum.json`

```json
{
  "core": "fuse_libretro",
  "shader": "crt/crt-easymode",
  "extensions": [".tzx", ".tap", ".z80", ".rzx", ".scl", ".trd", ".dsk"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .tzx | TZX tape image - Preserves tape loading with turbo loaders | Fuse tape loading |
| .tap | TAP tape image - Most common format | Fuse tape loading |
| .z80 | Z80 snapshot - Instant state loading | Fuse snapshot load |
| .rzx | RZX recording - Replayable demo runs | Fuse recording playback |
| .scl | SCL disk image - TR-DOS disk format | Fuse with TR-DOS |
| .trd | TRD disk image - TR-DOS disk format | Fuse with TR-DOS |
| .dsk | Disk image - Generic format | Fuse disk loading |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file with auto-detection
showet-universal /path/to/demo.tzx

# Run in museum mode
showet-museum --platform zx_spectrum

# Run in jukebox mode with loop detection
showet-jukebox --ids 12345 --loops 3 --repeat all

# Extract archive then run
showet-archive --extract demo.zip && showet-universal demo/
```

## CRT Settings
- **Shader**: CRT-Easymode
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible with flicker
- **Phosphor Bloom**: Enabled for authentic glow
- **Aspect Ratio**: 4:3 (typical TV)

## Loop Detection for ZX Spectrum Demos

ZX Spectrum demos typically:
- Are single-file programs that run to completion
- Have no built-in looping
- Run for a fixed duration (usually 1-5 minutes)

Showet jukebox handles this by:
- Detecting intro/4k/64k tags for loop status
- Using configurable loop count when shuffling
- Automatically advancing to next demo

## Notable Demos

- **Shiny** by Fairlight - Attribute clash graphics masterpiece
- **The Decrunch** by Censor Design - Fast loading demo
- **Ruka** by Traction - Multiface demo
- **Moscow Olympics** by CyberPunks United - Russian demoscene

## Demoparty Connection

The Spectrum demoscene is particularly active in:
- **Forever** - Czech demoparty with strong ZX focus
- **Vega** - Russian demoparty
- **Zosya** - Russian demoparty

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
*ZX Spectrum preservation courtesy of the Fuse team*
