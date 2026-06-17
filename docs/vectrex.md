# Vectrex Platform Documentation

## Overview
The Vectrex is a unique vector-display console with built-in monitor. No external display needed - demos run on the integrated CRT with distinctive line-vector graphics.

## Emulation Setup

### Required Binaries
- **VecX** - Simple, accurate emulator
- **ParaJVE** - Java-based with debugging
- **RetroArch** - `vecx_libretro.so` core

### Installation
```bash
# Ubuntu/Debian
sudo apt install vecx

# macOS
brew install vecx

# Using RetroArch
showet-executor demo.bin --download-cores
```

## Platform Configuration
Located at: `nostalgist_configs/gce_vectrex.json`

```json
{
  "core": "vecx",
  "shader": "crt/crt-easymode",
  "extensions": [".vec", ".bin"]
}
```

## Unique Characteristics

| Feature | Description |
|---------|-------------|
| Vector Display | Analog lines, no pixels |
| Self-contained | Built-in monitor |
| Rotatable | 330° action buttons |
| Unique Sound | General Instrument AY-3-8910 |

## Demo Types & Formats

| Format | Description | Runtime |
|--------|-------------|---------|
| `.vec` | Native Vectrex image - Most common | Original format |
| `.bin` | Raw binary - Popular for homebrew | Homebrew |

## Notable Demos

### Homebrew Scene
- **Vector Pilot** - Modern homebrew masterpiece
- **MineStorm** - Classic built-in upgraded
- **Solar Wars** - Multiplayer vector action
- **Head On** - Car racing vector demo
- **Star Castle** - Arcade port

### Running a Demo
```bash
# Using Showet executor
showet-executor /path/to/demo.vec --platform gce_vectrex

# Using CLI
showet --demo 12345 --platform gce_vectrex

# Museum mode
showet-museum --platform gce_vectrex
```

## Vector CRT Effects

### Special Considerations
- **No scanlines** - Vector draws lines
- **Phosphor trail** - Authentic analog decay
- **Glow effect** - Bright line emission
- **Screen curvature** - Built-in CRT curvature

### Shader Settings
```glsl
// Use crt-easymode with:
// - Line emphasis boost
// - Glow radius: 2.0
// - No scanlines (set to 0)
```

## Modern Homebrew

The Vectrex has an active homebrew scene with:
- Modern releases from 2020-2024
- Multi-cart compilations
- Development tools available