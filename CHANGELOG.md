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

### Production Polish
- **Loading Screen** - Demoscene-style loading with boot messages and progress bars
- **Sound Design** - Disk drive, keyboard click, and power-on sound effects
- **Platform Documentation** - All 87 platforms indexed in `docs/PLATFORM_INDEX.md`

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Launch Showcase
python3 -m http.server 8000
open http://localhost:8000/showet-showcase.html

# CLI Tools
scene-org --search "Assembly 2024"
showet-cache --cache <url> -n demo.zip
showet-ai --predict-rating "Second Reality"
```

## 🏆 The Demo-Runner of the Future
With authentic CRT shaders, immersive soundscapes, and AI-powered discovery - Showet delivers the definitive demoscene experience.

---
*v2.1 - Where nostalgia meets modern convenience*
*June 2026*