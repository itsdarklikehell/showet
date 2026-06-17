# PC-Engine/TurboGrafx Platform Documentation

## Overview
The PC-Engine (TurboGrafx-16 in the US) was NEC's 8-bit console with 16-bit capabilities. Strong demo scene in Japan and Europe.

## Emulation Setup

### Required Binaries
- **Mednafen** - Recommended, accurate
- **RetroArch** - `mednafen_pce_libretro.so` core
- **Ootake** - Windows, good compatibility
- **Beetle PCE** - RetroArch core variant

### Installation
```bash
# Ubuntu/Debian
sudo apt install mednafen

# macOS
brew install mednafen
```

## Platform Configuration
Located at: `nostalgist_configs/nec_pcengine.json`

```json
{
  "core": "mednafen_supergrafx",
  "shader": "crt/crt-easymode",
  "extensions": [".pce", ".cue", ".iso"]
}
```

## Console Models

| Model | Region | Notes |
|-------|--------|-------|
| PC-Engine | Japan | Original |
| TurboGrafx-16 | USA | Different case, HuCard slot |
| PC-Engine CD | Japan | CD-ROM add-on |
| TurboDuo | USA | Combined console + CD |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.pce` | HuCard ROM - Most common | Cartridge |
| `.cue/.iso` | CD image - CD demos | CD-ROM |
| `.hcd` | HuCard dump - Direct | HuCard format |

## Notable Demos

### Scene Highlights
- **Psycho Dream** - Famous Japanese demo
- **Super Star Soldier** - HuCard excellence
- **Gradius** - Classic shooter demo scene
- **Castlevania** - Konami titles

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.pce --platform nec_pcengine

# Using CLI
showet --demo 12345 --platform nec_pcengine
```

## Sound Integration

### HuC6280 Audio
- 5 channels (3 square, 1 noise, 1 ADPCM)
- Integrated with CPU
- Excellent for chiptune demos

## CRT Settings
- **Shader**: CRT-Easymode (RGB output)
- **Curvature**: 0.08
- **Scanlines**: Subtle for sharp pixels
- **Aspect**: 4:3 with overscan