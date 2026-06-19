# Microsoft Windows Platform Documentation

## Overview
Microsoft Windows platform for running PC demos with authentic presentation. Supports classic Windows demos from Windows 95 through Windows XP era, featuring DirectX, OpenGL, and early shader effects.

## Emulation Setup

### Required Binaries
- **Wine** (6.0+) - Windows compatibility layer for Linux
- **Wine (Staging)** - Enhanced compatibility patches
- **RetroArch** - Optional fallback via DOSBox core

### Installation
```bash
# Ubuntu/Debian - Wine for Windows demos
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install wine64 wine32

# For better compatibility
sudo apt install wine-staging

# Or using the official Wine repository
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
sudo add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ focal main'
sudo apt update
sudo apt install --install-recommends winehq-stable
```

## Wine Configuration for Demos

### Demo-Specific Setup
```bash
# Create a dedicated Wine prefix for demos
export WINEPREFIX="$HOME/.wine-showet"
wineboot --init

# Install Windows core fonts (helps with many demos)
winetricks corefonts

# Set Windows version for compatibility
winetricks win7  # or win98 for older demos
```

### Common Dependencies
Many demos require legacy DirectX or Visual C++ runtime:
```bash
# For DirectX 9 demos
winetricks directx9

# For Visual C++ 2019 demos
winetricks vcrun2019

# For older games/demos
winetricks directx8
winetricks vcrun2010
```

## Platform Configuration
Located at: `nostalgist_configs/microsoft_windows.json`

```json
{
  "core": "wine",
  "shader": "crt/crt-royale",
  "extensions": [".exe", ".msi"],
  "wine_prefix": "~/.wine-showet",
  "windows_version": "win7"
}
```

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| .exe | Windows executable - Most common demo format | Wine compatibility layer |
| .msi | Windows installer package | Wine msiexec |
| .bat | Batch launcher - Multi-part demos | Wine cmd |
| .zip | Archive - Compressed demos | Extract then run |

## Running Demos

### Using Showet
```bash
# Run by Pouet ID
showet 12345

# Run local file
showet-executor /path/to/demo.exe

# Run in museum mode
showet-museum --platform microsoft_windows

# Run in jukebox mode with loop detection
showet-jukebox --ids 12345 67890 --repeat all

# Extract archive then run
showet-archive --extract demo.zip && showet-universal demo/
```

## CRT Settings
- **Shader**: CRT-Royale (for Windows resolution flexibility)
- **Curvature**: 0.05 (subtle barrel effect)
- **Scanlines**: Visible at 1080p, subtle at 720p
- **Phosphor Bloom**: Enabled for CRT monitor effect
- **Resolution**: Configurable 640x480 to 1920x1080

## Wine Performance Tuning

### For Smooth Demo Playback
```bash
# In ~/.wine-showet/user.reg, add:
[AppDefaults\\demo.exe\\Direct3D]
"DirectDrawRenderer"="opengl"
"Multisampling"="enabled"

# For fullscreen demos
export WINE_FULLSCREEN_FOCUS=$(xdotool getactivewindow)
```

### Common Compatibility Fixes
1. **Black screen** - Try `winetricks ddr=opengl`
2. **No sound** - Check `winetricks sound=alsa` or `sound=pulse`
3. **Crashes on startup** - Set Windows version to winxp or win2k
4. **DirectX errors** - Install `winetricks directx9`

## Loop Detection for Windows Demos

Windows demos often:
- Have built-in looping (64k/4k intros)
- Use fullscreen exclusive mode
- Run for a fixed duration

Showet automatically detects loop behavior by:
- Checking Pouet.net tags for "looping" or "infinite"
- Demo type detection (intros often loop)
- File size heuristics (larger = longer demo)

## Notable Demos

- **Heaven Seven** by Conspiracy - DirectX masterpiece
- **Chaos Control** by Conspiracy - Early Windows demo
- **Synesthetics** by Kewlers - Music disk
- **FR-08** by Farbrausch - Shader experiment
- **FR-27** by Farbrausch - Procedural content

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*
*Wine integration powered by WineHQ - https://winehq.org*
