# Wild Videoffmpeg Platform Documentation

## Overview
Wild Videoffmpeg platform for running retro demos with authentic presentation.

## Emulation Setup

### Required Binaries
- RetroArch
- Native emulator

### Installation
```bash
sudo apt install retroarch
```

## Platform Configuration
Located at: `nostalgist_configs/wild_videoffmpeg.json`

```json
{
  "core": "ffmpeg_libretro",
  "shader": "crt/crt-easymode"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .mkv | Supported format | Native emulator |
| .avi | Supported format | Native emulator |
| .f4v | Supported format | Native emulator |
| .f4f | Supported format | Native emulator |
| .3gp | Supported format | Native emulator |
| .ogm | Supported format | Native emulator |
| .flv | Supported format | Native emulator |
| .mp4 | Supported format | Native emulator |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.mkv

# Run in museum mode
showet-museum --platform wild_videoffmpeg
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
