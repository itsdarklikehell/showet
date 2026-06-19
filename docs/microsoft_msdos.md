# Microsoft MS-DOS Platform Documentation

## Overview
The platform that brought demos to the masses with VGA graphics.

## Emulation Setup

### Required Binaries
- **DOSBox-X**
- **RetroArch (dosbox_libretro)**

### Installation
```bash
sudo apt install dosbox-x
```

## Platform Configuration
Located at: `nostalgist_configs/microsoft_msdos.json`

```json
{
  "core": "dosbox_core_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .zip | Supported format | Native emulator |
| .dosz | Supported format | Native emulator |
| .exe | Supported format | Native emulator |
| .com | Supported format | Native emulator |
| .bat | Supported format | Native emulator |
| .iso | Supported format | Native emulator |
| .cue | Supported format | Native emulator |
| .ins | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.zip

# Run in museum mode
showet-museum --platform microsoft_msdos
```

## CRT Settings
- **Shader**: CRT-Easymode
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible with flicker
- **Phosphor Bloom**: Enabled for authentic glow

## Troubleshooting

### Common Issues
1. **Slow execution** - Use cycles=3000 in DOSBox config
2. **Missing DLLs** - Install MSVCRT in Wine prefix
3. **Sound issues** - Set sbtype=sb16 in DOSBox

## Notable Demos

Check pouet.net for top-rated demos on this platform.

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
