# Arcade Demos Platform Documentation

## Overview
Showet supports arcade demos through MAME and RetroArch's arcade cores. Run classic demoparty arcade productions and homebrew demos directly from scene.org archives.

## Emulation Setup

### Primary Emulators
| Emulator | Type | Notes |
|----------|------|-------|
| **MAME** | Native | Most compatible, full ROM support |
| **FinalBurn Neo** | RetroArch | Faster, good for homebrew |
| **FBAlpha** | RetroArch | Alternative arcade core |

### Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mame retroarch libretro-fbneo

# macOS
brew install mame
brew install --cask retroarch

# Arch Linux
sudo pacman -S mame retroarch libretro-fbn

# Download arcade demos
# Place .zip ROM files in ~/.showet/roms/arcade/
```

### MAME Configuration
```bash
# Create MAME directories
mkdir -p ~/.mame/roms
mkdir -p ~/.mame/config

# Configure for Showet
echo 'video                    opengl' >> ~/.mame/mame.ini
echo 'window                   0' >> ~/.mame/mame.ini
echo 'maximize                 1' >> ~/.mame/mame.ini
```

## Showet Integration

### nostalgist.js Configuration
Located at: `nostalgist_configs/arcade_arcade.json`

```json
{
  "core": "mame2003",
  "shader": "crt/crt-easymode",
  "style": {
    "backgroundColor": "black",
    "width": "100%",
    "height": "100%"
  },
  "extensions": [".zip", ".chd", ".7z"]
}
```

### Platform Extensions
- `.zip` - Standard MAME ROM archives
- `.chd` - Compressed Hard Drive images
- `.7z` - 7-Zip compressed archives
- `.cmd` - MAME command files

## Demo Sources

### Scene.org Arcade Archives
```bash
# Browse arcade demos
scene-org --party assembly --platform arcade --list

# Download specific demo
scene-org --download /parties/assembly/2023/entries/demo.zip
```

### Pouet.net Arcade Filter
- Search: Platform → "Arcade"
- Filter by party entries
- Download .zip files

## Running Demos

### Local MAME
```bash
# List available arcade demos
ls ~/.showet/roms/arcade/*.zip

# Run with MAME
mame -rompath ~/.showet/roms/arcade <demo_name>

# Run specific demo
showet-executor ~/.showet/roms/arcade/demo.zip --platform arcade_arcade
```

### RetroArch
```bash
# Load arcade core
retroarch -L ~/.config/retroarch/cores/mame_libretro.so ~/.showet/roms/arcade/demo.zip

# Fullscreen with CRT shader
retroarch -L ~/.config/retroarch/cores/mame_libretro.so demo.zip --fullscreen --shader crt-easymode
```

### Browser via nostalgist.js
```javascript
// Load arcade demo in browser
const config = {
    core: "mame2003",
    rom: "/roms/arcade/demo.zip",
    shader: "crt/crt-easymode"
};
nostalgist.launch(config);
```

## Recommended Arcade Demos

### Classic Demo Scene
- **Assembly Arcade Entries** - Annual Finnish demo compo
- **Revision Competitions** - German demoparty arcade category
- **Evoke Demos** - Cologne scene productions

### Homebrew Excellence
- **ROMM demos** - Modern arcade homebrew
- **PICO-8 arcade ports** - Demade productions
- **TIC-80 arcade releases** - Fantasy console

## CRT Authenticity Settings

| Setting | Value | Notes |
|---------|-------|-------|
| **Shader** | `crt/crt-easymode` | RGB phosphor effect |
| **Curvature** | 0.1-0.2 | Subtle barrel distortion |
| **Scanlines** | 0.3-0.5 | Horizontal line effect |
| **Bloom** | 0.2-0.4 | CRT phosphor glow |
| **Aspect** | 4:3 | Original arcade ratio |

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| **"Missing ROM"** | Ensure ROM is in `~/.showet/roms/arcade/` |
| **No audio** | Check MAME sound drivers (`mame -listaudio`) |
| **Slow performance** | Use FinalBurn Neo core instead of MAME |
| **Controls not working** | Configure RetroArch input in `retroarch.cfg` |

### BIOS Files
Most arcade demos don't require BIOS files. Commercial games may need:
- `neogeo.zip` - Neo Geo AES BIOS
- `namco50.zip` - Namco System 11 BIOS

Place in `~/.mame/roms/` or `~/.config/retroarch/system/`

## Performance Tips

```bash
# Use frame skip for smoother playback
mame -frameskip 2 demo

# Reduce resolution
mame -resolution 640x480 demo

# Skip nag screens
mame -skip_gameinfo demo
```

## Related Platforms

- [Neo Geo](snk-neogeo.md) - SNK arcade system
- [PICO-8](fancon-pico8.md) - Fantasy console demos
- [Flash/Ruffle](flash-ruffle.md) - Browser arcade ports

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
*With authentic CRT shaders, real-time streaming, and jukebox mode.*