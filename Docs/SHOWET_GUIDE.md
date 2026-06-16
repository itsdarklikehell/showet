# Showet Demo-Runner - Complete Feature Guide

## 🚀 Quick Setup

```bash
# Install
pip install -e .

# Check your system
showet-status

# Configure streaming (example for Twitch)
showet-stream --save-key twitch --key YOUR_STREAM_KEY

# You're ready! Stream a demo:
showet-stream --platform twitch --demo 12345
```

## 📺 Streaming Guide

### Basic Streaming
```bash
# To Twitch
showet-stream --platform twitch --demo 12345

# To YouTube Live  
showet-stream --platform youtube --demo 12345 --quality 1080p

# Local RTSP (for OBS capture)
showet-stream --rtsp
# Then add in OBS: Media Source → rtsp://localhost:8554/showet
```

### Advanced Streaming
```bash
# With webcam overlay
showet-stream --platform twitch --webcam --demo 12345

# Stream with custom overlay text
showet-stream --platform twitch --overlay "My Demo Stream" --demo 12345

# Stream and record locally
showet-stream --platform twitch --record --demo 12345 --record-path ~/videos/demos/

# Multiple stream keys (for switching between platforms)
showet-stream --save-key twitch --key TWITCH_KEY
showet-stream --save-key youtube --key YOUTUBE_KEY
```

## 🎨 CRT Authentic Display

### Available Presets
| Preset | Platform | Authentic Features |
|--------|----------|-------------------|
| `c64_monitor` | Commodore 64 | Green phosphor, vertical scanlines |
| `amiga_ocs` | Amiga | Sharp pixels, horizontal scanlines |
| `atari_st` | Atari ST | Medium persistence, dot crawl |
| `nes_famicom` | NES/Famicom | Composite artifacts, NTSC bleed |
| `snes_superfamicom` | SNES | RGB monitor, clean scanlines |
| `genesis_megadrive` | Genesis | CMOS timing, color separation |
| `vga_vesa` | PC | Low scanlines, crisp pixels |
| `commodore_amiga_pal` | Amiga | PAL 50Hz, squashed aspect |

### Using CRT Presets
```bash
# Via launcher (auto-detects platform)
showet-launcher --demo 12345 --crt-preset c64_monitor

# In nostalgist configs
# The configs in nostalgist_configs/ already include shader references
```

## 🔧 Demoscene Tools

### Demo Discovery
```bash
# See trending demos
showet-spotlight

# Search for specific demos
showet-launcher --search "commodore 64 2024"

# View upcoming demoparties
showet-parties

# View demo metadata
demo-viewer --demo-id 12345
```

### Demo Management
```bash
# Add to favorites
showet-launcher --demo 12345 --favorite

# Schedule demo playback
showet-launcher --schedule --demo 12345 --at "20:00"

# Create a playlist
showet-launcher --create-playlist "C64 Classics" commodore_64

# View history
showet-launcher --history
```

### Collaborative Viewing
```python
# Python API
from collaborative import create_session, generate_session_html

session = create_session(platform="commodore_64", demo_id=12345, stream_to="twitch")
html = generate_session_html(session, with_stream=True, spectator_mode=True)
```

## 🌐 nostalgist.js Browser Integration

```bash
# Generate configs
python3 nostalgist_bridge.py
python3 generate_manifest.py

# Serve locally
python3 -m http.server 8000

# Open in browser
# http://localhost:8000/showet-showcase.html
```

The showcase includes:
- Platform browser with search
- CRT shader selector
- Streaming controls
- Chat overlay

## 🎛️ OBS Integration

```python
# Python API
from obs_integration import OBSController, SCENES

obs = OBSController(host="localhost", port=4444, password="secret")
obs.switch_scene(SCENES["demo"])
obs.update_stream_info(demo_name="Heaven Seven", platform="amiga")
```

Scenes available:
- `demo` - Demo playback
- `intermission` - Between demos
- `credits` - Group credits
- `setup` - Loading screens
- `waiting` - Lobby/waiting room

## 📊 System Architecture

```
                    ┌─────────────┐
                    │   Pouet     │
                    │     API     │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│   Showet    │  │  Streaming   │  │   Browser    │
│   Player    │  │   Manager    │  │ nostalgist   │
└──────┬──────┘  └──────┬───────┘  └──────┬───────┘
       │                │                 │
       ▼                ▼                 ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│ RetroArch   │  │    FFmpeg    │  │   Canvas     │
│   Cores     │  │  → Twitch    │  │              │
└─────────────┘  │  → YouTube   │  └──────────────┘
                 │  → RTSP      │
                 └──────────────┘
```

## 🎯 Pro Tips

1. **Stream keys**: Store them securely with `--save-key`. Never commit to git!

2. **CRT presets**: Match the preset to your demo's platform for authenticity

3. **Collaborative sessions**: Share the session ID for group viewing

4. **Recording**: Always record while streaming for archival purposes

5. **Party integration**: Schedule release parties around major demoparties

6. **Favorites**: Tag demos by style (64k, 4k, wild, etc.)

---
*Showet - The demoscene demo-runner of the future, with the soul of the past.*