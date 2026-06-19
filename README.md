# 🗺️ ShowEt Demoscene Demo Runner - v3.0

The definitive, immersive demo-runner for the demoscene with nostalgic flair. Showet provides a unified interface for running demos from pouet.net, scene.org, and modarchive.org across **84+ platforms** with authentic CRT presentation.

## 🎯 What is Showet?

Showet transforms your computer into a demoscene powerhouse that can:
- **Download** demos from pouet.net and scene.org with one command
- **Auto-detect** the correct platform and emulator
- **Extract** archives (ZIP, RAR, 7z, LHA) automatically
- **Install** missing emulators and RetroArch cores
- **Run** demos natively or through emulation (RetroArch, Wine, DOSBox)
- **Stream** to Twitch/YouTube/Facebook with real-time CRT effects
- **Jukebox Mode** - Continuous playback with loop/shuffle/repeat
- **Experience** authentic retro visuals with Television Simulator '99

## 🚀 Quick Start

```bash
# Install the project
pip install -e .

# Check available platforms
showet --platforms

# Run a demo by Pouet.net ID
showet 12345

# Search and run a random demo
showet --random --fullscreen

# Or use the universal executor
showet-executor /path/to/demo.zip

# Check for missing dependencies
showet-installer check

# Install missing emulators
showet-installer install

# Stream to Twitch
showet-stream --platform twitch --demo 12345
```

## 📺 Live Streaming

Showet supports streaming demos to popular platforms with authentic CRT effects:

```bash
# Stream to Twitch
showet-stream --platform twitch --demo 12345

# Stream to YouTube Live  
showet-stream --platform youtube --quality 1080p --demo 12345

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

## 🔧 Complete CLI Toolset (v2.1)

| Command | Description |
|---------|-------------|
| `showet` | Run a demo by Pouet ID |
| `showet-executor` | Universal demo executor with auto-detection |
| `showet-archive` | Extract demo archives (ZIP/RAR/7z/LHA) |
| `showet-installer` | Install missing emulators and cores |
| `showet-recorder` | Record demos with retro-authentic CRT encoding |
| `scene-org` | Search and download from scene.org archives |
| `showet-modarchive` | Search and download music modules |
| `showet-cache` | Manage local offline demo cache |
| `showet-ai` | AI-powered demo discovery and recommendations |
| `showet-stream` | Stream demos to Twitch/YouTube |
| `showet-launcher` | Unified launcher with streaming |
| `showet-spotlight` | Featured demos + hall of fame |
| `showet-jukebox` | Loop/Shuffle/Repeat demo playback |
| `showet-status` | System status dashboard |
| `showet-parties` | Upcoming demoparty calendar |
| `demo-viewer` | Demo metadata viewer |

## 🎨 Demoscene Authenticity Kit

Museum-grade retro presentation through integrated enhancement suite:

### Visual Authenticity
- **CRT Shader Engine** (`showet-crt-shader.js`) - WebGL-powered authentic monitor effects
- **SVG Filter Effects** - Hardware-accelerated CRT simulation
- **Shader Pack** (`shaders/`) - Curated GLSL shaders (Easymode, Royale, Pi)

### Period-Accurate Audio (`showet-audio.js`)
Chiptune sound effects for UI interactions, loading sequences, and notifications.

### Boot Sequence Simulator (`showet-boot-sequence.js`)
Authentic OS startup sequences for AmigaDOS, MS-DOS, and C64.

### Museum Mode
Fullscreen kiosk with automatic demo rotation and curatorial notes.

## 🌐 Integrated Projects & Sources

Showet connects to the entire demoscene ecosystem, integrating with the following projects and databases:

### Demo Databases
| Project | URL | Integration |
|---------|-----|-------------|
| **Pouet.net** | https://www.pouet.net | Primary demo database with API integration for download links, metadata, ratings |
| **Scene.org** | https://scene.org | Official demoscene archive since 1997, direct production file downloads |
| **Demozoo.org** | https://demozoo.org | Extended demoscene metadata, group information, member credits, release dates |
| **ArtCity** | https://artcity.bitfellas.org | Demoscene art collections, screenshots, visual history |

### Music Archives
| Project | URL | Integration |
|---------|-----|-------------|
| **ModArchive.org** | https://modarchive.org | Module downloads for synth demos, s3m/xm/it/mod formats |
| **HVSC** | http://hvsc.c64.org | High Voltage SID Collection for authentic C64 music |
| **ASMA** | http://asma.scene.org | Amiga Scene Music Archive integration |
| **VGMParadise** | https://vgmparadise.net | Video game music for related demo content |

### Emulation Frameworks
| Project | URL | Integration |
|---------|-----|-------------|
| **RetroArch/libretro** | https://www.retroarch.com | Universal core-based emulation, primary runtime backend |
| **nostalgist.js** | https://nostalgist.js.org | Browser-based RetroArch wrapper for web demos |
| **Television Simulator '99** | https://github.com/sgtstroopwafel/television-simulator-99 | CRT TV visual frontend with authentic display effects |
| **Wine** | https://www.winehq.org | Windows compatibility layer for PC demos |
| **DOSBox-X** | https://dosbox-x.com | Enhanced DOS emulation for MS-DOS productions |
| **VICE** | https://vice-emu.sourceforge.io | C64/Amiga/VIC-20 native emulator |
| **FS-UAE** | https://fs-uae.net | Amiga emulation with WHDLoad support |
| **Mednafen** | https://mednafen.github.io | Multi-system emulator fallback |

### Authentic Experience Assets
| Project | URL | Integration |
|---------|-----|-------------|
| **Television Simulator '99** | https://github.com/sgtstroopwafel/television-simulator-99 | CRT TV visual frontend with authentic display effects, OSD controls, jukebox mode |
| **nostalgist.js** | https://nostalgist.js.org | Browser-based RetroArch wrapper for web demos |
| **BezelProject** | https://www.bezelproject.com | Platform-specific screen bezels for CRT/cab simulation |
| **Libretro Shaders** | https://github.com/libretro/common-shaders | CRT effects (Easymode, Royale, Pi, etc.) |
| **The Made** | https://themade.org | Historical context and demoscene preservation |

## 📂 Supported Platforms (84+)

Showet supports platforms across 5 decades of computing:

### Home Computers (8-bit & 16-bit Era)
Commodore 64, Amiga, 128, VIC-20, PET, Plus/4, Atari 8-bit, ST, Falcon, ZX Spectrum, Amstrad CPC, MSX, PC-Engine/TurboGrafx, PC-8800, PC-98, PC-FX, Enterprise EP128, Oric, Apple II/IIGS

### Gaming Consoles
NES/Famicom, SNES/Super Famicom, Sega Master System, Megadrive/Genesis, Saturn, Dreamcast, PlayStation, Nintendo 64, Game Boy (Color/Advance), Neo Geo, WonderSwan, Vectrex, Atari 2600/7800/Lynx, 3DO, Phillips CD-i

### Arcade & Specialized Systems
MAME-compatible arcade, Homebrew platforms (PICO-8, Flash/Ruffle), Wild (Video/FFmpeg), WebAssembly

### See Full Platform Index
See [docs/PLATFORM_INDEX.md](docs/PLATFORM_INDEX.md) for complete documentation.

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- RetroArch (optional but recommended)
- Wine (for Windows demos)
- DOSBox-X (for DOS demos)

### From PyPI (Coming Soon)
```bash
pip install showet
```

### From Source
```bash
git clone https://github.com/itsdarklikehell/showet
cd showet
pip install -e .
```

### Runtime Dependencies (Auto-Install)
```bash
# Install all emulators
showet-installer install

# Check what's missing
showet-installer check
```

### Usage Examples

### Download & Run Demo
```bash
# Run by Pouet ID (downloads + runs)
showet 12345

# Run local file with auto-detection
showet-executor /path/to/demo.zip

# Stream to Twitch with webcam
showet-stream --platform twitch --webcam --demo 12345

# Run jukebox with multiple demos
showet-jukebox --ids 12345 67890 --loops 3 --shuffle random --repeat all
```

### TVS99 Setup
```bash
# Setup Television Simulator '99
showet-tvs99

# Verify all components work
showet-check

# Install all dependencies at once
showet-installer all
```

### Browser Integration

Showet includes complete browser-based demo playback via nostalgist.js:

```bash
# Generate nostalgist.js configs
python3 nostalgist_bridge.py
python3 generate_manifest.py

# Serve the configs
python3 -m http.server 8000
# Open: http://localhost:8000/showet-showcase.html
```

### nostalgist.js Integration
- **nostalgist_bridge.py** - Generates JSON configs for all 84 platforms
- **Core mapping** - Automatic translation from Showet cores to nostalgist cores
- **Shader presets** - CRT effects automatically applied per platform
- **Browser playback** - Run demos in browser without local emulator install

### Demo Discovery & Music
```bash
# View trending demos
showet-spotlight

# Find upcoming parties
showet-parties

# AI-powered recommendations
showet-ai

# Search ModArchive for music modules
showet-modarchive search "future crew"

# Download modules for jukebox
showet-modarchive-enhanced jukebox-modules commodore_64
```

## 🏛️ Party Mode - Remote Demoparty Viewing

Synchronized demo viewing across multiple devices:

```bash
# Host a party session
python3 showet-party-mode.py

# Join as client
python3 -c "from showet_party_client_node import join_party; join_party('HOST_IP')"
```

**Features:**
- Real-time playback synchronization
- One-click demo launching
- Multi-viewer support
- Integrated chat overlay

## 📺 Museum Mode - Exhibition-Quality Presentation

```bash
# Start fullscreen kiosk
python3 -c "from showet_museum_mode import launch_museum; launch_museum('commodore_64')"
```

**Use Cases:**
- Demoparty demo walls
- Museum exhibitions
- Public installations
- Retro gaming showcase

## 🚀 Deployment Options

### Docker
```bash
docker build -t showet -f Dockerfile.showet .
docker run -p 8000:8000 showet
```

### GitHub Actions
CI automatically builds on push to main branch.

## 🎵 Jukebox Mode - Loop/Shuffle/Repeat

Showet's jukebox mode provides continuous demo playback with intelligent looping across all sources:

```bash
# Play multiple demos in shuffle mode
showet-jukebox --ids 12345 67890 11223 --shuffle random --repeat all

# Play looped demos 3 times in shuffle
showet-jukebox --ids 12345 67890 --loops 3 --shuffle random

# From scene.org
showet-jukebox --source scene_org --ids 12345 --loops 3

# From ModArchive
showet-jukebox --source modarchive --ids 12345 --loops 3

# Repeat a single demo
showet-jukebox --ids 12345 --repeat one

# Custom timeout per demo
showet-jukebox --ids 12345 67890 --timeout 600
```

### Intelligent Loop Detection
Showet automatically detects looping demos based on multiple sources:

| Source | Detection Method |
|--------|-----------------|
| **Pouet.net** | Tags (loop, looping), Type (64k/4k intros) |
| **Scene.org** | Filename patterns (loop, endless), Party context |
| **ModArchive** | Track patterns (medley, mix, remix) |

### Shuffle Intelligence
When shuffling:
- Non-looping demos play once
- Looped demos play up to 3 times (configurable)
- Automatically advances to next demo after completion

## 📋 Project Status

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | ✅ Complete | Retro Immersion (CRT Shaders, Boot Sequences, Audio) |
| Phase 2 | ✅ Complete | Demoscene Integration (Pouet API, Shaders, Metadata) |
| Phase 3 | ✅ Complete | Community Features (WebSocket, Chat, Curator) |
| Phase 4 | ✅ Complete | Future-Proofing (AI, Hardware Encoders, LAN Sync) |
| Phase 5 | ✅ Complete | Experiential Polish (Sound Themes, Timeline, Party Mode) |

## 🔮 Roadmap

See [ROADMAP.md](ROADMAP.md) for upcoming enhancements.

## 📄 Documentation

- [PLATFORM_INDEX.md](docs/PLATFORM_INDEX.md) - All platform documentation
- [docs/](docs/) - Individual platform guides (C64, Amiga, DOS, NES, etc.)
- [docs/streaming-guide.md](docs/streaming-guide.md) - Streaming setup
- [docs/retropie-integration.md](docs/retropie-integration.md) - RetroPie setup

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License

GPL-3.0-or-later

---

*The demo-runner of the future is now streaming-ready! 📺*
*With authentic CRT shaders, real-time collaboration, and AI-powered discovery.*