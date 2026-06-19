# Commodore 64 Platform Documentation

## Overview
The most iconic demoscene platform with legendary productions like Second Reality.

## Emulation Setup

### Required Binaries
- **VICE (x64sc)**
- **RetroArch (vice_x64sc)**

### Installation
```bash
sudo apt install vice
```

## Platform Configuration
Located at: `nostalgist_configs/commodore_64.json`

```json
{
  "core": "vice_x64sc_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .zip | Supported format | Native emulator |
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
showet-executor /path/to/demo.zip

# Run in museum mode
showet-museum --platform commodore_64
```

## CRT Settings
- **Shader**: CRT-Easymode
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible with flicker
- **Phosphor Bloom**: Enabled for authentic glow

## Troubleshooting

### Common Issues
1. **No SID sound** - Check if VICE was compiled with SID support
2. **Wrong colors** - PAL vs NTSC demo mismatch
3. **Cannot run** - Missing kernal ROM file

## Notable Demos

- **Second Reality** by Future Crew - The pinnacle
- **Unreal** by Future Crew - Graphics masterpiece
- **State of the Art** by Spaceballs - Disk magazine

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
