# Nintendo Game Boy Platform Documentation

## Overview
The Game Boy brought monochrome gaming to the masses. Demoscene thrived with Game Boy Color-enhanced demos using the "DMG" sound chip.

## Emulation Setup

### Required Binaries
- **Gambatte** - Recommended, accurate
- **SameBoy** - Modern, excellent debugger
- **RetroArch** - `gambatte_libretro.so` core

### Installation
```bash
# Ubuntu/Debian
sudo apt install mednafen

# macOS
brew install sameboy

# Using RetroArch
showet-executor demo.gb --download-cores
```

## Platform Configuration
Located at: `nostalgist_configs/nintendo_gameboy.json`

```json
{
  "core": "gambatte",
  "shader": "crt/crt-easymode",
  "extensions": [".gb", ".gbc", ".cgb"]
}
```
## Console Models

| Model | Year | Notes |
|-------|------|-------|
| Game Boy | 1989 | Original monochrome |
| Game Boy Pocket | 1996 | Smaller screen |
| Game Boy Color | 1998 | Color + enhanced CPU |
| Game Boy Advance | 2001 | 32-bit successor |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.gb` | Original Game Boy - Monochrome demos | Classic |
| `.gbc` | Game Boy Color - Enhanced colors | Color |
| `.cgb` | CGB-specific builds | Advanced |

## Notable Demos

### Game Boy Scene
- **PGB** - Professional Game Boy demo group
- **Focus** - European GB demo scene
- **Dualtris** - Notable GB homebrew
- **Tetris Effect** - Modern GB demo aesthetics

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.gb --platform nintendo_gameboy

# Using CLI
showet --demo 12345 --platform nintendo_gameboy
```

## DMG Sound Chip

### Audio Specs
- 4 channels (2 square, 1 wave, 1 noise)
- No DAC output (pure chiptune)
- Tempo tricks via CPU timing

## CRT Settings
- **Shader**: CRT-Easymode (monochrome)
- **Curvature**: 0.05
- **Scanlines**: Dot matrix simulation
- **Colors**: Green/amber monochrome filter