## Showet Emulation Project

This repository contains the source code and infrastructure for **Showet**, a comprehensive, multi-platform emulation framework designed to run games and applications across a vast array of vintage and modern gaming consoles and computer systems.

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

### 🏗️ Modernization Status - ✅ PHASE 1-3 COMPLETE
| Component | Status | Notes |
|-----------|--------|-------|
| `PlatformBase.py` | ✅ Complete | Abstract base class defining the OOP contract |
| All 84 Platform modules | ✅ Refactored | All now inherit from `PlatformBase` |
| `scripts/refactor_platforms.py` | ✅ Created | Automation script for future platform additions |
| `CONTRIBUTING.md` | ✅ Complete | Developer guidelines and standards |
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

**Supported Cores (mapped):** quicknes, genesis_plus_gx, vice_x64sc, snes9x, picodrive, and more.

### 🚀 Deployment Options
```bash
# Docker (quick deployment)
docker build -t showet -f Dockerfile.showet .
docker run -p 8000:8000 showet

# GitHub Actions CI auto-builds on push to main
```

### 📋 Next Steps
1. Build web UI with demo browser
2. Add chat overlay for co-streaming
3. Implement RTMP relay for multiple outputs
4. Add hardware encoder support (VAAPI/VAAPI/V4L2)

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
```

### 🛠️ Complete CLI Toolset
| Command | Description |
|---------|-------------|
| `showet` | Run a demo by Pouet ID |
| `showet-stream` | Stream demos to Twitch/YouTube |
| `showet-launcher` | Unified launcher with streaming |
| `showet-spotlight` | Featured demos + hall of fame |
| `showet-status` | System status dashboard |
| `showet-parties` | Upcoming demoparty calendar |
| `demo-viewer` | Demo metadata viewer |
| `save_stream_key` | Securely store stream credentials |

---
*The demo-runner of the future is now streaming-ready! 📺*