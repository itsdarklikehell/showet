# Showet Improvements Log

## Streaming Enhancements (2025-06-16)

### New Features
- **Twitch/YouTube/Facebook Live streaming** via RTMP
- **RTSP server mode** for local network streaming
- **Webcam overlay support** with position options (top-right, top-left, bottom-right, bottom-left)
- **Text overlays** showing demo name and platform on stream
- **Multiple quality presets**: 480p, 720p, 1080p, 1440p, 4k
- **Local recording** while streaming
- **Secure stream key storage** in `~/.showet/{platform}_stream_key`

### CLI Tools
```bash
showet-stream --platform twitch --demo 12345
showet-stream --save-key twitch --key YOUR_KEY
showet-launcher --demo 12345 --stream youtube
demo-viewer --demo-id 12345
showet-status
```

## Demoscene Features

### CRT Shader Presets (`retro_effects.py`)
8 authentic CRT presets for era-accurate display:
- **c64_monitor** - Green phosphor, vertical scanlines
- **amiga_ocs** - Sharp CRT with horizontal scanlines
- **atari_st** - Medium persistence phosphor
- **nes_famicom** - Composite video artifacts, NTSC color bleeding
- **snes_superfamicom** - RGB monitor, sharp pixels
- **genesis_megadrive** - CMOS-based CRT
- **vga_vesa** - 1990s PC VGA CRT
- **commodore_amiga_pal** - PAL 50Hz timing

### Demo Database (`demo_database.py`)
- Search demos via Pouet.net API
- Favorite demos with tags
- Viewing history tracking
- Playlist creation
- Party-specific demo search

### Unified Launcher (`launcher.py`)
```bash
showet-launcher --demo 12345 --stream twitch --quality 1080p
showet-launcher --search "64k intros 2024"
showet-launcher --favorites
showet-launcher --list-presets
showet-launcher --create-playlist "C64 stream" commodore_64
```

### Demo Viewer (`demo_viewer.py`)
```bash
demo-viewer --demo-id 12345
demo-viewer --overlay --demo-id 12345
```

## Bug Fixes

### PlatformBase.py
- **Added missing `run()` method** - Platform runners now actually execute demos via RetroArch
- Proper ROM discovery and loading
- Fullscreen/audio options support

### Platform Modules (84 files)
- All inherit from PlatformBase correctly
- Ready for streaming integration

## Quick Reference

### Streaming Commands
```bash
# Save stream key
showet-stream --save-key twitch --key YOUR_STREAM_KEY

# Stream a demo to Twitch
showet-stream --platform twitch --demo 12345

# Stream to YouTube Live at 1080p
showet-stream --platform youtube --quality 1080p --demo 12345

# Stream with webcam overlay
showet-stream --platform twitch --webcam --demo 12345

# Local RTSP server (for OBS capture)
showet-stream --rtsp --rtsp-port 8554

# Stream and record locally
showet-stream --platform twitch --record --demo 12345
```

### Environment Variables
- `SHOWET_STREAM_KEY` - Primary stream key
- Platform-specific keys saved in `~/.showet/`

### Using the Modules
```python
from streaming import StreamManager, StreamConfig, StreamPlatform
from demo_database import get_db
from retro_effects import get_preset, generate_shader_config

# Setup streaming
config = StreamConfig(platform=StreamPlatform.TWITCH, stream_key="key", quality="1080p")
manager = StreamManager()
manager.configure(config)

# Get CRT preset for platform
crt = get_preset("commodore_64")  # Green phosphor
shader = generate_shader_config("amiga")  # Complete shader config

# Search demos
db = get_db()
results = db.search_demos("commodore")
```

---
*The demo-runner of the future is now streaming-ready! 📺*