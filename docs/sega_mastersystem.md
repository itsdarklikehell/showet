#  Sega Mastersystem Platform Documentation

## Overview
 Sega Mastersystem platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- **RetroArch**

### Installation
```bash
sudo apt install retroarch  # or appropriate emulator
```

## Platform Configuration
Located at: `nostalgist_configs/sega_mastersystem.json`

```json
{
  "core": "genesis_plus_gx_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .zip | Supported format | Native emulator |
| .mdx | Supported format | Native emulator |
| .md | Supported format | Native emulator |
| .smd | Supported format | Native emulator |
| .gen | Supported format | Native emulator |
| .bin | Supported format | Native emulator |
| .cue | Supported format | Native emulator |
| .iso | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.zip

# Run in museum mode
showet-museum --platform sega_mastersystem
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
