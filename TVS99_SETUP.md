# Television Simulator '99 - Showet Browser Integration

## Quick Start

```bash
# 1. Generate configs
python3 nostalgist_bridge.py

# 2. Start server
python3 -m http.server 8000

# 3. Open in browser
open http://localhost:8000/showet-showcase.html
```

## Available Browser Platforms

| Platform | Core | Status |
|----------|------|--------|
| **NES/Famicom** | quicknes, fceumm, nestopia | ✅ Working |
| **C64** | vice_x64sc, vice_x64 | ✅ Working |
| **Game Boy** | gambatte | ✅ Working |
| **Game Boy Color** | gambatte | ✅ Working |
| **SNES** | snes9x | ✅ Working |
| **Genesis/Mega Drive** | genesis_plus_gx | ✅ Working |
| **Atari 2600** | stella | ✅ Working |
| **Master System** | genesis_plus_gx | ✅ Working |
| **Arcade** | mame2003 | ⚠ Limited ROMs |
| **Amiga** | puae | ❌ Not in CDN |

## Local Run (Recommended)

For Amiga demos and other platforms without browser cores:

```bash
# Run demo locally with FS-UAE
./showet-demo-run.sh /path/to/demo.adf

# Or with RetroArch directly
retroarch -L ~/.config/retroarch/cores/fsuae_libretro.so demo.adf
```

## Demo Sources Integration

- **Pouet.net** - `showet --demo <pouet_id>`
- **Scene.org** - `scene-org --party assembly --search <demo>`
- **ModArchive** - `showet-modarchive search <query>`

---
*Showet makes demos accessible anywhere - browser or native!*