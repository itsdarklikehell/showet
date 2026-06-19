# Sega Dreamcast Platform Documentation

## Overview
Sega Dreamcast platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- RetroArch
- Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/sega_dreamcast.json`

```json
{
  "core": "flycast_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .chd | Supported format | Native emulator |
| .cdi | Supported format | Native emulator |
| .elf | Supported format | Native emulator |
| .bin | Supported format | Native emulator |
| .cue | Supported format | Native emulator |
| .gdi | Supported format | Native emulator |
| .lst | Supported format | Native emulator |
| .zip | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.chd

# Run in museum mode
showet-museum --platform sega_dreamcast
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
