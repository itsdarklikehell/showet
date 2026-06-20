# Sega Master System Platform Documentation

## Overview
The Master System was Sega's 8-bit console released in 1986. It featured advanced VDP graphics for its time with hardware scrolling, sprite zooming, and a 32-color palette from 32768 colors. The demoscene on Master System is strongest in Europe and Brazil, creating impressive visual effects despite the system's limitations.

## Emulation Setup

### Primary Emulators
| Emulator | Platform | Notes |
|----------|----------|-------|
| **Genesis Plus GX** | RetroArch | Most compatible, recommended |
| **SMS Plus** | Standalone | Lightweight, accurate |
| **MEKA** | Multi | Includes debugger |

### Installation Commands

```bash
# Using RetroArch (recommended)
# Download genesis_plus_gx_libretro core
showet-installer install --platform sega_master_system

# Or manually via RetroArch
# Main Menu → Online Updater → Core Downloader → Sega - Master System

# Standalone MEKA
sudo apt install mednafen  # mednafen supports SMS

# macOS
brew install mednafen
```

## Showet Integration

### nostalgist.js Configuration
Located at: `nostalgist_configs/sega_mastersystem.json`

```json
{
  "core": "genesis_plus_gx",
  "shader": "crt/crt-pi",
  "extensions": [".sms", ".gg", ".sg", ".bin", ".m3u"],
  "style": {
    "backgroundColor": "black",
    "width": "100%",
    "height": "100%"
  }
}
```

### File Extensions Supported
- `.sms` - Standard ROM images
- `.gg` - Game Gear ROMs (compatible)
- `.sg` - SG-1000 backward compatible
- `.bin` - Raw dumps
- `.m3u` - Multi-disk playlists (for SD-style compilations)

## Console Models

| Model | Region | Notes |
|-------|--------|-------|
| Master System | Europe/US | Standard version |
| Mark III | Japan | Original design (white) |
| Master System II | Worldwide | Compact, no card slot |
| Sega Game 1000 | Australia | Bundled version |
| Master System III | Brazil | Multiple variants |

## Demo Scene Highlights

### Recommended Demos
- **Power Strike Collection** - European scene excellence
- **VDP Demo** - Graphics showcase
- **Sound Test ROMs** - Audio demonstrations
- **Brazilian productions** - Active modern scene

### Running Demos with Showet

```bash
# Run a single demo
showet-executor /path/to/demo.sms --fullscreen

# Run from scene.org archive
scene-org --party assembly --platform sega_mastersystem

# Use in jukebox mode
showet-jukebox --ids 12345 67890 --platform sega_mastersystem --shuffle

# Browser playback via nostalgist.js
# Open showet-showcase.html and select Sega Master System
```

## VDP Graphics Capabilities

### Technical Specs
- **Colors**: 32 simultaneous from 32768 palette
- **Resolution**: 256×192 (display), 32×24 tiles
- **Sprites**: 64 max, 8 per scanline
- **Scrolling**: Horizontal + vertical hardware

### Demo Techniques
- **Raster effects** - Color changes mid-frame
- **Line scrolling** - Animated wave effects
- **Sprite multiplexing** - More than 8 sprites
- **Mode tricks** - Extended palettes

## CRT Authenticity Settings

| Setting | Value |
|---------|-------|
| **Shader** | `crt/crt-pi` or `crt/crt-easymode` |
| **Curvature** | 0.06 (subtle) |
| **Scanlines** | 0.3 (retro CRT effect) |
| **Blur** | 0.02 (sharp pixels) |
| **Aspect Ratio** | 4:3 with border |

## Troubleshooting

### Common Issues
- **No audio**: Check core audio settings in RetroArch
- **Screen flicker**: Try `genesis_plus_gx` vs `bluemsx` core
- **Controls not working**: Verify RetroArch gamepad config

### BIOS Files
Master System typically doesn't require BIOS files. Some cores may use `bios_E.sms` for specific region locking.

## Demo Sources

| Source | URL | Notes |
|--------|-----|-------|
| **Scene.org** | `/parties/assembly` | European SMS demos |
| **Pouet.net** | Search "Sega Master System" | Curated productions |
| **Demozoo** | Platform filter | New releases |

## Related Platforms
- [Sega Mega Drive](sega-megadrive.md) - 16-bit successor
- [Game Gear](sega-gamegear.md) - Portable variant
- [Genesis](https://github.com/itsdarklikehell/showet/blob/main/docs/sega-megadrive.md) - US-named Mega Drive