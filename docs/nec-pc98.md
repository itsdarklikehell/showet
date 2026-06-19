# Nec Pc98 Platform Documentation

## Overview
Nec Pc98 platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- RetroArch
- Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/nec_pc98.json`

```json
{
  "core": "nekop2_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .d98 | Supported format | Native emulator |
| .zip | Supported format | Native emulator |
| .98d | Supported format | Native emulator |
| .fdi | Supported format | Native emulator |
| .fdd | Supported format | Native emulator |
| .2hd | Supported format | Native emulator |
| .tfd | Supported format | Native emulator |
| .d88 | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.d98

# Run in museum mode
showet-museum --platform nec_pc98
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
