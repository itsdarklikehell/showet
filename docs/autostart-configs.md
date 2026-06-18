# Platform Autostart Configurations

This document describes the autostart configurations for each platform to enable seamless demo playback.

## Overview

Each platform has specific autostart configurations that handle:
- Disk image mounting
- Autoloader setup
- Default settings for demo playback
- CRT shader presets

## Platform Configurations

### Commodore 64 (`commodore_64`)
- **Disk images**: D64 is auto-mounted to drive 8
- **Tape images**: T64/TAP auto-load with `LOAD "",8,1`
- **Programs**: PRG/CRT run directly with `SYS 64802` for autostart
- **Settings**: `VICEAutostartOn = 1`, `VDCDelay = 2000`

### Commodore Amiga (`commodore_amiga`)
- **Disk images**: ADF auto-mounted to DF0:
- **Hard drives**: HDF with WHDLoad
- **Kickstart**: kick13.rom/kick31.rom required
- **Settings**: `joyport_mode = mouse`, ` gfx_framerate = 1`

### MS-DOS (`microsoft_msdos`)
- **Executables**: EXE/COM auto-run
- **DOSBox config**: `cycles = max`, `sbtype = sb16`
- **Settings**: `memsize = 16`, `machine = svga_s3`

### Nintendo Famicom (`nintendo_famicom`)
- **ROMs**: NES auto-load
- **Settings**: `fceumm_region = Auto`, `fceumm_turbo = enabled`

### Nintendo Super Famicom (`nintendo_superfamicom`)
- **ROMs**: SMC/SFC auto-load
- **Settings**: `snes9x_layer_1 = enabled`, `snes9x_layer_2 = enabled`

## Autostart Config Generator

The `showet-dependency-installer.py` can generate autostart configs:

```bash
# Generate configs for all platforms
showet-installer install --generate-configs

# Or for a specific platform
showet-installer install --platform commodore_64 --generate-configs
```

## RetroArch Overrides

Platform-specific RetroArch overrides are stored in:

```
nostalgist_configs/
├── commodore_64.json
│   ├── core: "vice_x64sc"
│   ├── shader: "crt/crt-easymode"
│   └── extensions: ["d64", "t64", "prg"]
└── commodore_amiga.json
    ├── core: "puae"
    ├── shader: "crt/crt-royale"
    └── extensions: ["adf", "hdf"]
```

## Usage

```python
from nostalgist_bridge import generate_nostalgist_config

config = generate_nostalgist_config(
    platform_slug="commodore_64",
    rom_path="/demos/demo.d64",
    core_name="vice_x64sc_libretro"
)
```

This generates a config ready for TVS99/Nostalgist.js to launch with authentic settings.