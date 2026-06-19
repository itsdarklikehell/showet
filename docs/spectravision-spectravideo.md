# Spectravision Spectravideo Platform Documentation

## Overview
Spectravision Spectravideo platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- RetroArch
- Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/spectravision_spectravideo.json`

```json
{
  "core": "bluemsx_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .rom | Supported format | Native emulator |
| .ri | Supported format | Native emulator |
| .mx1 | Supported format | Native emulator |
| .mx2 | Supported format | Native emulator |
| .col | Supported format | Native emulator |
| .dsk | Supported format | Native emulator |
| .cas | Supported format | Native emulator |
| .sg | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.rom

# Run in museum mode
showet-museum --platform spectravision_spectravideo
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
