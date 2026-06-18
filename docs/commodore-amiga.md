# Commodore Amiga Platform Documentation

## Overview
Commodore Amiga platform for running retro demos with authentic presentation. Revolutionary multimedia computer that defined the demoscene with incredible graphics and sound.

## Emulation Setup

### Required Binaries
- **FS-UAE** - Primary native emulator with WHDLoad support
- **RetroArch (puae_libretro)** - Libretro core option

### Installation
```bash
# Ubuntu/Debian
sudo apt install fs-uae

# macOS
brew install fs-uae

# Or download from https://fs-uae.net
```

### BIOS Required
- **Kickstart 1.3** (kick13.rom) - For most demos
- **Kickstart 3.1** (kick31.rom) - For later demos
- Place in: `~/.config/retroarch/system/` or FS-UAE kickstart directory

## Platform Configuration
Located at: `nostalgist_configs/commodore_amiga.json`

```json
{
  "core": "puae_libretro",
  "shader": "crt/crt-royale",
  "extensions": [".adf", ".dms", ".ipf", ".adz", ".lha", ".zip"]
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .adf | Amiga Disk image - Most common | FS-UAE or WinUAE |
| .hdf | Hard disk image - WHDLoad demos | FS-UAE with WHDLoad |
| .dms | Disk Master image - Compressed | FS-UAE or decompression |
| .ipf | Interchangeable Preservation Format | SPS/IPF support required |
| .lha | LZH archive - Common distribution | Extract then run |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.adf

# Run WHDLoad with FS-UAE
showet-executor /path/to/demo.lha --whdload

# Run in museum mode
showet-museum --platform commodore_amiga

# Find Amiga music modules
showet-modarchive-enhanced jukebox-modules commodore_amiga
```

## CRT Settings
- **Shader**: CRT-Royale (authentic Amiga monitor look)
- **Curvature**: 0.1 (subtle barrel effect)
- **Scanlines**: Visible with flicker
- **Phosphor Bloom**: Enabled for authentic glow

## Troubleshooting

### Common Issues
1. **Kickstart required** - Amiga needs BIOS files in system directory
2. **WHDLoad** - Use WHDLoad for best demo compatibility
3. **Chip RAM** - Some demos need more RAM (set chip_memory=2048)
4. **Sound Stutter** - Reduce Paula audio buffer size

## Notable Demos

- **Second Reality** by Future Crew - The pinnacle
- **Arte** by Sanctuary - Raytraced masterpiece
- **Especially for You** by Fairlight
- **Life Is A Miracle** by Conspiracy

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
