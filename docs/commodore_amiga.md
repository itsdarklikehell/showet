# Commodore Amiga Platform Documentation

## Overview
Revolutionary multimedia computer with incredible demo scene.

## Emulation Setup

### Required Binaries
- **FS-UAE**
- **RetroArch (puae_libretro)**

### Installation
```bash
sudo apt install fs-uae
```

## Platform Configuration
Located at: `nostalgist_configs/commodore_amiga.json`

```json
{
  "core": "puae_libretro\", \"fsuae_libretro\", \"uae4arm_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .adf | Amiga Disk image | FS-UAE or WinUAE |
| .dms | Supported format | Native emulator |
| .ipf | Supported format | Native emulator |
| .adz | Supported format | Native emulator |
| .lha | Supported format | Native emulator |
| .zip | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.adf

# Run in museum mode
showet-museum --platform commodore_amiga
```

## CRT Settings
- **Shader**: CRT-Easymode
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible with flicker
- **Phosphor Bloom**: Enabled for authentic glow

## Troubleshooting

### Common Issues
1. **Kickstart required** - Amiga needs BIOS files
2. **WHDLoad** - Use HFS for best compatibility
3. **Chip RAM** - Some demos need more RAM

## Notable Demos

Check pouet.net for top-rated demos on this platform.

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
