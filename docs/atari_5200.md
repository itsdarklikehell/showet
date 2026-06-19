#  Atari 5200 Platform Documentation

## Overview
 Atari 5200 platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- **RetroArch**

### Installation
```bash
sudo apt install retroarch  # or appropriate emulator
```

## Platform Configuration
Located at: `nostalgist_configs/atari_5200.json`

```json
{
  "core": "atari800_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .zip | Supported format | Native emulator |
| .xfd | Supported format | Native emulator |
| .atr | Supported format | Native emulator |
| .cdm | Supported format | Native emulator |
| .cas | Supported format | Native emulator |
| .bin | Supported format | Native emulator |
| .a52 | Supported format | Native emulator |
| .atx | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.zip

# Run in museum mode
showet-museum --platform atari_5200
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
