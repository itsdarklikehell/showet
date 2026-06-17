## 🗺️ ShowEt Demoscene Demo Runner - v2.1 (Phase 7 Complete!)

This repository contains the source code and infrastructure for **Showet**, the definitive, immersive demo-runner for the demoscene with nostalgic flair.

### 🎯 Project Overview
Showet aims to be a unified platform for retro gaming enthusiasts, providing a consistent interface for emulating hardware from the Atari 2600 all the way up to more modern systems, alongside a modular architecture to integrate future platforms.

### 📦 Quick Start
```bash
# Install
pip install -e .

# View available platforms
python3 -c "from showet import create_platform_runners; print([r.supported_platforms() for r in create_platform_runners()])"

# Run a demo (example)
python3 showet.py 12345  # Pouet.net demo ID
```

### 📺 Live Streaming Support

Showet supports live streaming demos to popular platforms:

```bash
# Stream to Twitch
showet-stream --platform twitch --demo 12345

# Stream to YouTube Live
showet-stream --platform youtube --quality 1080p --demo 12345

# Stream to Facebook Live
showet-stream --platform facebook --demo 12345

# Local RTSP streaming (for OBS/other capture)
showet-stream --rtsp --rtsp-port 8554

# Save your stream key for convenience
showet-stream --save-key twitch --key YOUR_TWITCH_STREAM_KEY

# Stream with webcam overlay
showet-stream --platform twitch --webcam --demo 12345

# Stream and record locally
showet-stream --platform twitch --record --demo 12345
```

**Environment variables:**
- `SHOWET_STREAM_KEY` - Your stream key (takes precedence)
- Configure platform-specific keys with `--save-key`

**Available options:**
- `--quality`: 480p, 720p, 1080p, 1440p, 4k
- `--overlay`: Custom text overlay on stream
- `--webcam`: Include webcam picture-in-picture
- `--no-audio`: Disable audio capture
- `--fullscreen`: Stream in fullscreen mode
- `--record`: Record stream locally while broadcasting

### 📂 Structure Highlights
The project is highly modular, with the core logic separated by platform:

*   **Platforms:** 84 dedicated files (e.g., `Platform_Atari_2600.py`, `Platform_Nintendo_Famicom.py`) house the emulation logic for specific hardware.
*   **UI/API:** The `showet-gui/`, `showet-webui/`, and `showet_api.py` folders manage the user interface and backend services.
*   **nostalgist Bridge:** `nostalgist_bridge.py` generates JSON configs for browser-based demo playback.

## 💾 DEMOSCENE AUTHENTICITY KIT (PHASE 1 - ENHANCED!)
Showet now delivers museum-grade retro presentation through our integrated enhancement suite.

### 🎨 Visual Authenticity
*   **CRT Shader Engine (`showet-crt-shader.js`):** WebGL-powered authentic monitor effects including barrel curvature, chromatic aberration, phosphor bloom, and scanline flicker
*   **SVG Filter Effects:** Hardware-accelerated CRT simulation via SVG filters for modern browsers
*   **Shader Pack (`shaders/`):** Curated collection of GLSL shaders (Easymode, Royale, Pi) for instant period-accurate visuals

### 🔤 Boot Sequence Simulator (`showet-boot-sequence.js`)
Experience authentic system startup with multiple era options:
*   **AmigaDOS Boot:** Classic Commodore Amiga startup sequence
*   **MS-DOS Boot:** Microsoft DOS-style initialization
*   **C64 Boot:** Vintage Commodore 64 feel

### 🔊 Period-Accurate Audio (`showet-audio.js`)
Chiptune sound effects for every interaction:
*   UI clicks and rollovers
*   Loading sequences
*   Success/error chimes

### 🎮 Demo Showcase (`showet-showcase.html`)
Interactive demo gallery with:
- Platform search and filtering
- Hall of Fame with legendary demos
- One-click streaming to Twitch/YouTube
- CRT shader selection
- Demo info panel with platform details

### 🔧 Phase 7 Enhancements (COMPLETE! ✅)
| Feature | Description | Status |
|---------|-------------|--------|
| Demo preview automation | Auto-generate 30-second highlights | ✅ Done |
| Scene.org integration | Direct download from scene.org archives | ✅ Done |
| CRT OSD effects | On-screen display effects (power LED, channel numbers) | ✅ Done |
| Demo recording | Built-in capture for creating content | ✅ Done |
| Platform thumbnails | Grid view with preview thumbnails | ✅ Done |
| Demo difficulty tags | Wild, intro, demo, executable categories | Planned |

---

## 🏗️ Modernization Status - ✅ PHASE 1-4 COMPLETE
| Component | Status | Notes |
|-----------|--------|-------|
| `PlatformBase.py` | ✅ Complete | Abstract base class defining the OOP contract |
| All 84 Platform modules | ✅ Refactored | All now inherit from `PlatformBase` |
| `showet-crt-shader.js` | ✅ Complete | WebGL CRT effects with curvature/bloom |
| `showet-boot-sequence.js` | ✅ Complete | Authentic OS-style boot sequences |
| `showet-audio.js` | ✅ Complete | Retro sound feedback engine |
| `shaders/` | ✅ Complete | CRT-Easymode, Royale, Pi GLSL pack |
| `pouet_integration.py` | ✅ Complete | Direct Pouet.net demo database API |
| `nostalgist_bridge.py` | ✅ Complete | Generates 84 JSON configs for TVS integration |
| `nostalgist_configs/` | ✅ Generated | 84 platform configs + manifest.json |
| GitHub Actions CI | ✅ Complete | `.github/workflows/ci.yml` |
| Docker support | ✅ Complete | `Dockerfile.showet` |

### 📺 nostalgist.js Integration (Production Ready!)
Launch demos in the browser with Television Simulator '99:

```bash
# Generate configs
python3 nostalgist_bridge.py
python3 generate_manifest.py

# Serve the configs (view in browser)
python3 -m http.server 8000
# Open: http://localhost:8000/showet-viewer.html
```

**Integration Stack:**
- **nostalgist.js** - Browser-based RetroArch/Emscripten wrapper
- **Television Simulator '99** - CRT TV visual effect frontend
- **showet-nostalgist-loader.js** - JavaScript loader for demos
- **showet-crt-shader.js** - Authentic CRT WebGL effects
- **showet-boot-sequence.js** - OS-style startup sequences

**Launch Demo Showcase:**
```bash
# Serve and view in browser (with full CRT effects!)
python3 -m http.server 8000
# Open: http://localhost:8000/showet-showcase.html
```

**Supported Cores (mapped):** quicknes, genesis_plus_gx, vice_x64sc, snes9x, picodrive, and more.

### 🚀 Deployment Options
```bash
# Docker (quick deployment)
docker build -t showet -f Dockerfile.showet .
docker run -p 8000:8000 showet

# GitHub Actions CI auto-builds on push to main
```

### 📋 Phase 4+ Enhancements (COMPLETE!)
1. ✅ **Hardware Encoder Bridge** - VAAPI/V4L2 support for low-latency streaming
2. ✅ **LAN Multiplayer Sync** - Synchronized playback across multiple devices
3. ✅ **AI Demo Curator** - Intelligent demo discovery and recommendations

### 🎮 Demoscene Features (COMPLETE!)
```bash
# View upcoming demoparties
showet-parties

# See trending demos and hall of fame
showet-spotlight

# Stream demos live to Twitch/YouTube
showet-stream --platform twitch --demo 12345

# Create collaborative viewing session with streaming
python3 -c "from collaborative import create_session; print(create_session('commodore_64', 12345, 'twitch'))"

# Check system status
showet-status

# View demo metadata
demo-viewer --demo-id 12345

# Launch demo with all features
showet-launcher --demo 12345 --stream twitch --webcam

# Start Party Mode for synchronized group viewing
python3 showet-party-mode.py 8765
```

### 🎉 Party Mode - Remote Demoparty Viewing
Host synchronized demo sessions for remote demoparty viewing:
*   **Host Role:** Select demos, control playback, all viewers sync automatically
*   **Client Role:** Join sessions, view synchronized playback with friends
*   **Auto-Launch:** When host launches a demo, all connected clients load it automatically
*   **Playback Sync:** Real-time synchronization ensures everyone sees the same frame

Start a party in the viewer by clicking "Start Party Session" in the control panel!

### 🏛️ Museum Mode - Exhibition-Quality Presentation
Perfect for demoparties, museums, or public installations:
*   **Fullscreen Kiosk:** Automatic rotation of milestone demos
*   **Curatorial Notes:** Historical context displayed for each demo
*   **Progress Tracking:** Visual progress bar shows demo sequence

Click the "🏛️ Museum Mode" button in the viewer to begin!

### 🔧 Complete CLI Toolset
| Command | Description |
|---------|-------------|
| `showet` | Run a demo by Pouet ID |
| `showet-recorder` | Record demos with retro-authentic CRT encoding |
| `showet-stream` | Stream demos to Twitch/YouTube |
| `showet-launcher` | Unified launcher with streaming |
| `showet-spotlight` | Featured demos + hall of fame |
| `showet-status` | System status dashboard |
| `showet-parties` | Upcoming demoparty calendar |
| `demo-viewer` | Demo metadata viewer |
| `save_stream_key` | Securely store stream credentials |
| `showet_ai_curator.py` | AI-powered demo recommendations |
| `hardware_bridge.py` | Hardware-accelerated streaming |
| `showet-lan.py` | LAN multiplayer synchronization |
| `showet-party-mode.py` | Start Party Mode server for synchronized viewing |
| `showet-museum-mode.js` | Exhibition-quality fullscreen demo presentation |
| `showet-shader-playground.js` | Competition mode with URL sharing |
| `showet-preview-clips.js` | Demo preview clip system |
| `showet-demo-scoring.py` | Historical significance scoring algorithm |
| `showet-scaffold.py` | Platform addition CLI tool |
| `scene_org_integration.py` | Download demos directly from scene.org archives |
| `showet-osd-controls.js` | CRT on-screen display effects (power LED, channel numbers) |

---
*The demo-runner of the future is now streaming-ready! 📺*
*With authentic CRT shaders, real-time collaboration, and AI-powered discovery.*