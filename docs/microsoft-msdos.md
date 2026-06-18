# Microsoft MS-DOS Platform Documentation

## Overview
Microsoft MS-DOS platform for running retro demos with authentic presentation. The platform that brought demos to the masses with VGA graphics and Sound Blaster audio.

## Emulation Setup

### Required Binaries
- **DOSBox-X** - Primary native emulator
- **RetroArch (dosbox_core_libretro)** - Libretro core option

### Installation
```bash
# Ubuntu/Debian
sudo apt install dosbox-x

# macOS
brew install dosbox-x

# Or download from https://dosbox-x.com
```

## Platform Configuration
Located at: `nostalgist_configs/microsoft_msdos.json`

```json
{
  "core": "dosbox_core_libretro",
  "shader": "crt/crt-easymode",
  "extensions": [".exe", ".com", ".bat", ".iso", ".cue"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .exe | Executable - Most common demo format | Direct execution in DOSBox |
| .com | COM program - Small intros | Direct execution in DOSBox |
| .bat | Batch launcher - Multi-part demos | DOSBox with auto-run |
| .zip | Archive - Compressed demos | Extract then run |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.exe

# Run in museum mode
showet-museum --platform microsoft_msdos

# Run in jukebox mode
showet-jukebox --ids 12345 67890 --repeat all

# Find DOS music modules
showet-modarchive-enhanced jukebox-modules microsoft_msdos
```

## CRT Settings
- **Shader**: CRT-Easymode
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible with flicker
- **Phosphor Bloom**: Enabled for authentic glow

## Troubleshooting

### Common Issues
1. **Slow execution** - Use cycles=3000 in DOSBox config
2. **Missing DLLs** - Install MSVCRT in Wine prefix for Windows demos
3. **Sound issues** - Set sbtype=sb16 and enable sound in DOSBox
4. **VGA resolution** - Some demos require specific machine type (vgaonly)

## Notable Demos

- **Second Reality** by Future Crew (PC port)
- **Unreal** by Future Crew
- **Chaos Control** by Conspiracy
- **Systematic** by Farbrausch

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
