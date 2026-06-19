# Showet Platform Documentation

Detailed guides for each supported platform, including setup, emulators, and demo recommendations.

## 📚 Complete Documentation

| Document | Description | Status |
|----------|-------------|--------|
| [SHOWET_GUIDE.md](SHOWET_GUIDE.md) | Complete user guide with streaming, CRT, and tools | ✅ Complete |
| [PLATFORM_INDEX.md](PLATFORM_INDEX.md) | All 84 platforms overview | ✅ Complete |
| [API.md](API.md) | Python API reference | ✅ Complete |
| [streaming-guide.md](streaming-guide.md) | Advanced streaming setup | ✅ Complete |
| [tvs99-integration.md](tvs99-integration.md) | Television Simulator '99 integration | ✅ Complete |
| [retropie-integration.md](retropie-integration.md) | RetroPie setup guide | ✅ Complete |

## 🎮 Platform-Specific Guides

All 84 platforms now have individual documentation files. Key platforms include:

| Platform | File | Status |
|----------|------|--------|
| Commodore 64 | [commodore-64.md](commodore-64.md) | ✅ Complete |
| Commodore Amiga | [commodore-amiga.md](commodore-amiga.md) | ✅ Complete |
| MS-DOS PC | [microsoft-msdos.md](microsoft-msdos.md) | ✅ Complete |
| Nintendo Famicom/NES | [nintendo-famicom.md](nintendo-famicom.md) | ✅ Complete |
| Super Nintendo/Super Famicom | [nintendo-superfamicom.md](nintendo-superfamicom.md) | ✅ Complete |
| Sega Megadrive/Genesis | [sega-megadrive.md](sega-megadrive.md) | ✅ Complete |
| Atari 2600/VCS | [atari-2600.md](atari-2600.md) | ✅ Complete |
| ZX Spectrum | [sinclair-zxspectrum.md](sinclair-zxspectrum.md) | ✅ Complete |

Full platform index: `ls docs/*.md` shows all available guides.

## 🔧 Quick Reference

```bash
# One-command runner (download + install + run)
showet-auto "demo name"
showet-auto 12345                    # Pouet ID
showet-auto /path/to/demo.zip         # Local file

# Manual workflow
showet-installer install                    # Install emulators
showet-archive demo.zip --extract           # Extract archives
showet-executor demo.d64 --prefer-retroarch  # Run demo
```

## Related
- [README.md](../../README.md) - Project overview & installation
- [ROADMAP.md](../../ROADMAP.md) - Future enhancements