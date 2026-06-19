# Nintendo Super Famicom (SNES) Platform Documentation

## Overview
16-bit Nintendo with advanced graphics for impressive demos.

## Emulation Setup

### Required Binaries
- **Snes9x**
- **RetroArch (snes9x_libretro)**

### Installation
```bash
sudo apt install snes9x
```

## Platform Configuration
Located at: `nostalgist_configs/nintendo_superfamicom.json`

```json
{
  "core": "snes9x_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .zip | Supported format | Native emulator |
| .sfc | Super Famicom ROM | Snes9x or RetroArch |
| .smc | Super Nintendo ROM | Snes9x or RetroArch |
| .fig | Supported format | Native emulator |
| .swc | Supported format | Native emulator |
| .bs | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.zip

# Run in museum mode
showet-museum --platform nintendo_superfamicom
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
