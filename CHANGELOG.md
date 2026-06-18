# Showet v2.1 Release Notes

## 🎉 What's New - The Ultimate Nostalgic Demo-Runner

### Phase 7: Advanced Demoscene Features (COMPLETE)
- **Scene.org Integration** - Direct downloads from the scene's archive (`scene-org` CLI)
- **Demo Recording** - Built-in capture with retro-authentic CRT encoding (`showet-recorder`)
- **CRT OSD Effects** - Power LED, channel display, static interference (`showet-osd-controls.js`)
- **Platform Icons** - Emoji icons in showcase grid for visual recognition
- **Preview Gallery** - Enhanced demo preview system with scene.org integration

### Phase 8: AI & Offline (COMPLETE)  
- **AI Curator Enhancement** - Scene.org discovery + demo rating predictions (`showet-ai`)
- **Local Cache Manager** - Offline demo playback support (`showet-cache`)

### Phase 9: Universal Demo Execution (COMPLETE)
- **Universal Demo Executor** (`showet-executor`) - Auto-detect and run any demo
- **Archive Handler** (`showet-archive`) - ZIP/RAR/7z/LHA extraction with passwords
- **RetroArch Integration** - Auto-select libretro cores, download missing cores
- **Dependency Installer** (`showet-installer`) - Auto-install Wine, DOSBox, VICE, RetroArch

### Phase 10: Enhanced Documentation (COMPLETE)
- **Platform Docs** - 8 detailed guides (C64, Amiga, DOS, NES, Megadrive, Atari ST, Spectrum, PC-Engine)
- **External Sources** - All integrations documented in README
- **One-Command Runner** (`showet-auto`) - Complete download → install → run pipeline
- **Consolidated Docs** - Single clean `docs/` folder structure
- **Setup Wizard** (`showet-setup-wizard`) - Interactive first-time configuration

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Launch Showcase
python3 -m http.server 8000
open http://localhost:8000/showet-showcase.html

# Setup Wizard (first time only)
showet-setup-wizard

# CLI Tools
scene-org --search "Assembly 2024"
showet-cache --cache <url> -n demo.zip
showet-ai --predict-rating "Second Reality"

# Run any demo (auto-detect platform)
showet-executor /path/to/demo.zip --download-cores

# One-command runner (download + install + run)
showet-auto "Second Reality"
showet-auto 12345

# Install emulators
showet-installer install
```

## 🏆 The Demo-Runner of the Future
With authentic CRT shaders, immersive soundscapes, AI-powered discovery, and universal execution - Showet is the definitive demoscene experience.

---
*Showet v2.2 - Nostalgia++ Edition*
*Setup Wizard + More Platforms*
*June 2026*