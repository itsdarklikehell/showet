# Nintendo Famicom/NES Platform Documentation

## Overview
The Famicom/NES launched the console demoscene with impressive hardware pushing. Showet provides authentic 8-bit experience with period-correct shaders.

## Emulation Setup

### Required Binaries
- **FCEUX** - Recommended with debugger
- **Nestopia** - Cycle-accurate, macOS
- **Mesen** - Modern, debug features
- **RetroArch** - `nes_libretro.so` core

### Installation
```bash
# Ubuntu/Debian
sudo apt install fceux

# macOS
brew install fceux
```

## Platform Configuration
Located at: `nostalgist_configs/nintendo_famicom.json`

```json
{
  "core": "quicknes",
  "shader": "crt/crt-easymode",
  "extensions": [".nes", ".fds"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.nes` | iNES format - Standard ROMs | Most common |
| `.fds` | Famicom Disk System - Original floppies | Famicom only |
| `.unf` | UNIF format - Extended headers | Modern demos |

## Notable Demos

### Hall of Fame
- **Bad Apple!!** by Anonymous - Famous PDM video
- **Super Mario Bros. 1+2** by various - Speedruns
- **Panda** by something (?) - Classic NES demo
- **NES Demo** by DCE - Early console scene

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.nes --platform nintendo_famicom

# Using CLI
showet --demo 12345 --platform nintendo_famicom

# Museum mode
showet-museum --platform nintendo_famicom
```

## Console Models

| Model | Region | Notes |
|-------|--------|-------|
| Famicom | Japan | Original, hardwired controllers |
| NES | USA/Europe | Lockout chip, different case |
| Famicom Mini | Japan | Modern recreation |
| NES Classic | Global | HDMI output |

## CRT Settings
- **Shader**: CRT-Easymode (composite TV feel)
- **Curvature**: 0.1
- **Scanlines**: Soft, 30% opacity
- **Noise**: Enabled for RF/CVBS feel

## mapper (MMC) Support

### Common Mappers
- **MMC1** - Castlevania, Mega Man 2
- **MMC3** - Super Mario Bros. 3
- **MMC5** - Laser Invasion, advanced features
- **VRC6/VRC7** - Famicom expansion sound

Showet auto-detects mapper requirements from ROM headers.