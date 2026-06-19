# Wild Gamemusic Platform Documentation

## Overview
Wild Gamemusic platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- RetroArch
- Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/wild_gamemusic.json`

```json
{
  "core": "gme_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .zip | Supported format | Native emulator |
| .ay | Supported format | Native emulator |
| .gbs | Supported format | Native emulator |
| .gym | Supported format | Native emulator |
| .hes | Supported format | Native emulator |
| .kss | Supported format | Native emulator |
| .nsf | Supported format | Native emulator |
| .nsfe | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.zip

# Run in museum mode
showet-museum --platform wild_gamemusic
```

## CRT Settings
- **Shader**: CRT-Easymode
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible with flicker
- **Phosphor Bloom**: Enabled for authentic glow

## Troubleshooting

### Common Issues
Check emulator installation and BIOS files if required.

## Notable Demos

Check pouet.net for top-rated demos on this platform.

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
