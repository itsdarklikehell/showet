#  Commodore 128 Platform Documentation

## Overview
 Commodore 128 platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- **RetroArch**

### Installation
```bash
sudo apt install retroarch  # or appropriate emulator
```

## Platform Configuration
Located at: `nostalgist_configs/commodore_128.json`

```json
{
  "core": "vice_x128_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .d64 | Disk image - Most common format | VICE emulates original floppy |
| .d71 | Supported format | Native emulator |
| .d81 | Supported format | Native emulator |
| .t64 | Tape image - For tape-loaded demos | Commodore tape loading |
| .tap | Supported format | Native emulator |
| .prg | Program file - Direct executable | Runs directly in emulator |
| .p00 | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.d64

# Run in museum mode
showet-museum --platform commodore_128
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
