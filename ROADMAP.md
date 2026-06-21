# 🗺️ ShowEt Modernization Roadmap - v4.0

The future of demoscene viewing is here. Showet is becoming the definitive, immersive demo-runner that captures authentic retro aesthetics while delivering cutting-edge functionality.

---

## 📋 Current Status (v3.2 Complete → v4.0 In Progress)

| Phase | Status | Deliverables |
|-------|--------|--------------|
| 🔧 Phase 1-11 | ✅ Complete | All previous phases done |
| 📦 Phase 12: Package Refactor | 🔄 In Progress | Clean package structure, async I/O, enhanced integrations |
| 🎵 Phase 13: Intelligence | Pending | ML-based demo discovery, smart caching |
| 🌐 Phase 14: Web UI | Pending | Full nostalgist.js integration, TVS99 bridge |

---

## 🔮 Phase 12: Clean Package Architecture (In Progress)

### Goals
- Refactor flat module structure into clean `showet/` package
- Separate concerns: core, platforms, integrations, cli, utils
- Async I/O for parallel downloads and cache management
- Enhanced integration modules

### Progress
- [x] Create `showet/core/` - config, executor, jukebox
- [x] Create `showet/integrations/` - pouet, scene_org, modarchive
- [x] Create `showet/utils/` - archive_handler, stream_manager
- [x] Create `showet/cli/` - unified command interface
- [x] Integrate legacy `showet.py` with v4.0 package (backward compatible)
- [x] Migrate platform modules to `showet/platforms/__init__.py`
- [x] Add async download/download manager
- [x] Implement SQLite cache layer with sync capabilities
- [x] Update pyproject.toml for new structure (fixed duplicate optional-dependencies)

---

## 🔮 Phase 13: Intelligence Enhancement

### Goals
- [x] ML-based demo recommendation engine
- [x] Smart loop detection with file analysis
- [x] SQLite offline cache with sync
- [x] Demo thumbnail generation service
- [x] Audio fingerprinting for module detection

---

## 🔮 Phase 14: Web Integration

### Goals
- [ ] Full nostalgist.js web launcher
- [ ] Television Simulator '99 integration
- [ ] Hall of Fame browser
- [ ] Demo tour guides with storytelling
- [ ] Party mode synchronized playback
- [ ] Demoscene Timeline Explorer - Interactive historical guide to releases/parties

---

## 🔮 Phase 10: Enhanced Source Integration (Complete)

### Goals
- Enhanced loop detection for scene.org demos
- ModArchive module loop intelligence  
- Unified demo metadata across all sources
- Cross-source playlist generation

### Completed
- [x] Enhanced jukebox with scene.org loop detection
- [x] ModArchive integration with loop heuristics
- [x] Unified source parameter in jukebox CLI
- [x] Cross-source demo metadata handling
- [x] Universal demo executor with Wine/DOSBox integration
- [x] Cross-source playlist generation (`generate_cross_source_playlist()`)
- [x] Demo duration estimation (`estimate_demo_duration()`)

---

## 🔮 Phase 11: Intelligent Jukebox v3 (Complete)

### Goals
Smart demo playback with context-aware behavior:

- [x] Demo duration estimation (audio analysis)
- [x] Smart loop detection (filename + metadata + heuristics)
- [x] Party-mode synchronized playback
- [x] Time-based demo scheduling
- [x] Demo rating integration for shuffle bias

---

## 🔮 Phase 12: Platform Expansion

### Goals
Expand platform support and improve existing integrations:

- [x] Raspberry Pi/RetroPie integration improvements
- [x] Steam Deck optimized build
- [ ] Android emulator support
- [x] WebAssembly compilation targets

---

## 🔮 Phase 13: v3.0 - The Complete Experience

### Features
- [x] Cross-platform installer (Linux/macOS/Windows)
- [x] Touch/mobile UI for tablets
- [x] RetroPie/RetroArch integration
- [x] Steam Deck optimized build
- [x] Offline mode with cached demos
- [x] Demo thumbnail generation
- [x] AI-powered demo recommendations
- [ ] Twitch streaming integration with chat

---

## 🏆 Integration Showcase

Showet integrates with the entire demoscene ecosystem:

### Demo Databases
| Project | Status | Integration |
|---------|--------|-------------|
| **Pouet.net** | ✅ Complete | Primary demo database with API integration |
| **Scene.org** | ✅ Complete | Direct production file downloads, party archives |
| **Demozoo.org** | ✅ Complete | Extended metadata, group credits |
| **ArtCity** | ✅ Available | Art collections, screenshots |

### Music Archives
| Project | Status | Integration |
|---------|--------|-------------|
| **ModArchive.org** | ✅ Complete | Module downloads, jukebox support |
| **HVSC** | ✅ Complete | C64 SID collection support |
| **ASMA** | ✅ Complete | Amiga scene music archive |
| **VGMParadise** | ✅ Available | Video game music for related demos |

### Emulation Frameworks
| Project | Status | Integration |
|---------|--------|-------------|
| **RetroArch/libretro** | ✅ Complete | 89 cores installed, universal emulation |
| **nostalgist.js** | ✅ Complete | 84 platform configs, CDN-ready cores |
| **Television Simulator '99** | ✅ Complete | CRT TV visual frontend, OSD controls |
| **Wine** | ✅ Complete | Windows compatibility layer |
| **DOSBox-X** | ✅ Complete | Enhanced DOS emulation |
| **VICE** | ✅ Complete | C64 native emulator |
| **FS-UAE** | ✅ Installed | Amiga WHDLoad support (needs Kickstart) |
| **MAME** | ✅ Complete | 0.285 - arcade demos ready |

### Authentic Experience Assets
| Project | Status | Integration |
|---------|--------|-------------|
| **BezelProject** | ✅ Complete | Platform-specific screen bezels |
| **Libretro Shaders** | ✅ Complete | CRT effects (Easymode, Royale, Pi) |
| **The Made** | ✅ Available | Historical context |

---

## 📊 Success Metrics Achieved

- ✅ **Visual:** Authentic CRT feel through WebGL shaders
- ✅ **Community:** WebSocket-based collaboration
- ✅ **Performance:** Hardware acceleration ready
- ✅ **Engagement:** Multi-user synchronized viewing
- ✅ **Discovery:** AI-powered hidden gem recommendations
- ✅ **Authenticity:** Loop detection across all sources
- ✅ **Integration:** nostalgist.js + Television Simulator '99
- ✅ **Archive Support:** ZIP/RAR/7z/LHA extraction
- ✅ **Auto-Installation:** RetroArch core downloads via apt
- ✅ **Platform Coverage:** 84+ platforms with configs
- ✅ **Docker Deployment:** Easy install with docker-compose
- ✅ **Arcade Support:** MAME 0.285 ready for arcade demos

---

## 🔧 Technical Improvements Completed

- [x] Async I/O for faster downloads
- [x] SQLite caching for offline mode
- [x] FastAPI backend for web UI
- [ ] Plugin system for custom platforms
- [ ] Configuration profiles for different setups

---

## 🎯 Contributing

Help improve Showet! Priority areas:
1. Platform documentation
2. Archive format handlers (password-protected archives)
3. BIOS file detection guides
4. Demo thumbnail generation
5. Test coverage improvements

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

*The demo-runner of the future is now streaming-ready! 📺*
*With authentic CRT shaders, real-time collaboration, and AI-powered discovery.*