#  Atari xlxe Platform Documentation

## Overview
 Atari xlxe platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- **RetroArch**

### Installation
```bash
sudo apt install retroarch  # or appropriate emulator
```

## Platform Configuration
Located at: `nostalgist_configs/atari_xlxe.json`

```json
{
  "core": "atari800_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .st | Supported format | Native emulator |
| .msa | Supported format | Native emulator |
| .zip | Supported format | Native emulator |
| .stx | Supported format | Native emulator |
| .dim | Supported format | Native emulator |
| .ipf | Supported format | Native emulator |
| .m3u | Supported format | Native emulator |
| .xex | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.st

# Run in museum mode
showet-museum --platform atari_xlxe
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
