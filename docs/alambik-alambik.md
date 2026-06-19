# Alambik Alambik Platform Documentation

## Overview
Alambik Alambik platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- RetroArch
- Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/alambik_alambik.json`

```json
{
  "core": "libretro_core",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .sam | Supported format | Native emulator |
| .alb | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.sam

# Run in museum mode
showet-museum --platform alambik_alambik
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
