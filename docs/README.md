# Showet Platform Documentation

Detailed guides for each supported platform, including setup, emulators, and demo recommendations.

## 📚 Complete Documentation

| Document | Description |
|----------|-------------|
| [SHOWET_GUIDE.md](SHOWET_GUIDE.md) | Complete user guide with streaming, CRT, and tools |
| [PLATFORM_INDEX.md](PLATFORM_INDEX.md) | All 85 platforms overview |
| [API.md](API.md) | Python API reference |
| [streaming-guide.md](streaming-guide.md) | Advanced streaming setup |
| [platform-compatibility.md](platform-compatibility.md) | Platform support matrix |

## 🎮 Platform-Specific Guides

| Platform | File | Status |
|----------|------|--------|
| Commodore 64 | [commodore64.md](commodore64.md) | ✅ Complete |
| Commodore Amiga | [commodore-amiga.md](commodore-amiga.md) | ✅ Complete |
| MS-DOS PC | [ms-dos.md](ms-dos.md) | ✅ Complete |
| Nintendo Famicom/NES | [nintendo-famicom.md](nintendo-famicom.md) | ✅ Complete |
| Super Nintendo/Super Famicom | [super-nintendo.md](super-nintendo.md) | ✅ Complete |
| Sega Megadrive/Genesis | [sega-megadrive.md](sega-megadrive.md) | ✅ Complete |
| Sega Master System | [sega-master-system.md](sega-master-system.md) | ✅ Complete |
| Nintendo Game Boy | [nintendo-gameboy.md](nintendo-gameboy.md) | ✅ Complete |
| Atari 2600/VCS | [atari-2600.md](atari-2600.md) | ✅ Complete |
| Atari ST | [atari-st.md](atari-st.md) | ✅ Complete |
| ZX Spectrum | [zx-spectrum.md](zx-spectrum.md) | ✅ Complete |
| PC-Engine/TurboGrafx | [pc-engine.md](pc-engine.md) | ✅ Complete |
| Sony PlayStation | [sony-playstation.md](sony-playstation.md) | ✅ Complete |
| Vectrex | [vectrex.md](vectrex.md) | ✅ Complete |

## 🔧 Quick Reference

```bash
# One-command runner (download + install + run)
showet-auto "Second Reality"
showet-auto 12345                    # Pouet ID
showet-auto /path/to/demo.zip         # Local file

# Manual workflow
showet-installer install                    # Install emulators
showet-archive demo.zip --extract            # Extract archives
showet-executor demo.d64 --prefer-retroarch  # Run demo
```

## Related
- [README.md](../../README.md) - Project overview & installation
- [ROADMAP.md](../../ROADMAP.md) - Future enhancements