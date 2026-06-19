# Nintendo 3Ds Platform Documentation

## Overview
Nintendo 3Ds platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- RetroArch
- Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/nintendo_3ds.json`

```json
{
  "core": "citra_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .3ds | Supported format | Native emulator |
| .3dsx | Supported format | Native emulator |
| .elf | Supported format | Native emulator |
| .axf | Supported format | Native emulator |
| .cci | Supported format | Native emulator |
| .cxi | Supported format | Native emulator |
| .app | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.3ds

# Run in museum mode
showet-museum --platform nintendo_3ds
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
