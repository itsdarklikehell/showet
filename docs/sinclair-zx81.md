# Sinclair Zx81 Platform Documentation

## Overview
Sinclair Zx81 platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- RetroArch
- Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/sinclair_zx81.json`

```json
{
  "core": "fuse_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .tzx | Supported format | Native emulator |
| .tap | Supported format | Native emulator |
| .z80 | Supported format | Native emulator |
| .rzx | Supported format | Native emulator |
| .scl | Supported format | Native emulator |
| .trd | Supported format | Native emulator |
| .dsk | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.tzx

# Run in museum mode
showet-museum --platform sinclair_zx81
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
