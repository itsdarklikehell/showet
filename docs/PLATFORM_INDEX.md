# Showet Platform Documentation Index - v2.1

## Overview
Showet supports **85 platforms** across 5 decades of computing history. Each platform is integrated with period-authentic emulators, shaders, and optional sound themes.

## Platform Categories

### Home Computers (8-bit & 16-bit Era)
| Platform | Emulator | Core/Runner | Default Shader | Archive Format |
|----------|----------|-------------|----------------|----------------|
| Commodore 64 | VICE | vice_x64sc | CRT-Easymode | D64, T64, PRG, CRT |
| Commodore 128 | VICE | vice_x128 | CRT-Royale | D64, T64 |
| Commodore Amiga | FS-UAE/UAE | puae | CRT-Royale | ADF, HDF, WHDLoad |
| Atari 8-bit | Atari800 | atari800 | CRT-PI | ATR, XEX |
| Atari ST | Hatari | hatari | CRT-Easymode | ST, MSA |
| ZX Spectrum | Fuse | fuse | CRT-PI | TAP, TZX, Z80 |
| Amstrad CPC | Caprice32 | cap32 | CRT-Easymode | DSK, IPF |
| MSX | blueMSX | bluemsx | CRT-PI | ROM, DSK |
| PC-Engine/TurboGrafx | Mednafen | mednafen_supergrafx | CRT-Easymode | PCE, ISO |

### Gaming Consoles
| Platform | Emulator | Default Shader | Archive Format |
|----------|----------|----------------|----------------|
| NES/Famicom | FCEUX/QuickNES | CRT-Easymode | NES, FDS |
| SNES/Super Famicom | Snes9x | CRT-PI | SMC, SFC |
| Sega Master System | Genesis Plus GX | CRT-PI | SMS |
| Sega Megadrive/Genesis | Genesis Plus GX | CRT-Easymode | MD, BIN |
| Sega Saturn | Yabause | CRT-Royale | BIN, ISO |
| Sony PlayStation | PCSX-ReARMed | CRT-Royale | BIN, ISO, CUE |
| Nintendo 64 | Mupen64Plus | CRT-Royale | N64, Z64 |
| Atari 2600 | Stella | CRT-PI | A26, BIN |
| Atari 7800 | ProSystem | CRT-PI | A78 |
| Atari Lynx | Handy | CRT-Easymode | LYNX |
| Nintendo Game Boy | Gambatte | CRT-PI | GB, GBC |
| Nintendo Game Boy Advance | Meteor | CRT-Royale | GBA |
| Neo Geo | FinalBurn Neo | CRT-Easymode | NG, ZIP |
| Neo Geo Pocket | Mednafen | CRT-Easymode | NGP |
| PC-FX | Mednafen | CRT-Royale | PCFX |

### Arcade & Specialized Systems
| Platform | Emulator | Default Shader | Archive Format |
|----------|----------|----------------|----------------|
| Arcade (MAME) | MAME | CRT-Royale | ZIP |
| Vectrex | VecX | CRT-Easymode | BIN |
| WonderSwan | Mednafen | CRT-PI | WSR |
| 3DO | 4DO | CRT-Royale | ISO |
| Phillips CD-i | Sinden | CRT-Easymode | ISO, CHD |

### Modern Platforms
| Platform | Runner | Notes |
|----------|--------|-------|
| Windows PC | Wine + Native | For modern demos |
| Linux Native | Native | Direct execution |
| WebGL/DOSBox | Emscripten | Browser-based DOS demos |

## Integration Sources

### External Platforms & APIs
- **Pouet.net** - Primary demo database (download links, metadata, ratings)
- **Scene.org** - Official demoscene archive (production files)
- **ModArchive.org** - Music module downloads (for synth demos)
- **Demozoo.org** - Extended demoscene metadata
- **ArtCity** - Demoscene art and screenshots
- **HVSC** - High Voltage SID Collection (C64 music)

### Emulation Frameworks
- **RetroArch/libretro** - Universal core-based emulation (recommended)
- **nostalgist.js** - Browser-based RetroArch wrapper
- **Television Simulator '99** - CRT TV visual frontend
- **Wine** - Windows compatibility layer
- **DOSBox-X/Boxer** - DOS emulation with enhanced features

### Authentic Experience Files
- **BezelProject** - Platform-specific screen bezels
- **CRT Shaders** - scanline, curvature, phosphor effects (see shaders/)
- **HVSC** - Authentic SID chip music for C64 demos
- **ASMA** - Amiga scene music archive

## Archive Format Support

Showet handles all common demoscene archive formats:

| Format | Extension | Tool |
|--------|-----------|------|
| ZIP | .zip | unzip |
| RAR | .rar | unrar |
| 7-Zip | .7z | 7z |
| LHA | .lha, .lzh | lha |

Password-protected archives are supported (use `--password` flag).

## Execution Methods

### Auto-Detection Order
1. **Platform suffix/extension** (e.g., `.d64` → C64)
2. **Archive internal files** (extracts and inspects)
3. **Filename patterns** (e.g., `amiga` in path)
4. **Interactive selection** (if ambiguous)

### Runner Priority
1. **RetroArch** (if core available) - Best compatibility
2. **Native emulator** - VICE, FS-UAE, Snes9x (best performance)
3. **Wine** - For Windows demos
4. **DOSBox** - For DOS demos

## Configuration

All platform configs are in `nostalgist_configs/` as JSON. Each config includes:
- `core` - RetroArch core or emulator
- `shader` - CRT effect to apply
- `extensions` - Supported file types
- `originalName` - Display name

## Related Documentation
- [README.md](/README.md) - Full setup guide
- [ROADMAP.md](/ROADMAP.md) - Future enhancements
- [CHANGELOG.md](/CHANGELOG.md) - Version history

---
*Showet v2.1 - Universal demo-runner with 85 platform support*