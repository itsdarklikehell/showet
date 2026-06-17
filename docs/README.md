# Platform Documentation

Detailed guides for each supported platform, including setup, emulators, and demo recommendations.

## Available Documentation

| Platform | File | Status |
|----------|------|--------|
| Commodore 64 | [commodore64.md](commodore64.md) | ✅ Complete |
| Commodore Amiga | [commodore-amiga.md](commodore-amiga.md) | ✅ Complete |
| MS-DOS PC | [ms-dos.md](ms-dos.md) | ✅ Complete |
| Nintendo Famicom/NES | [nintendo-famicom.md](nintendo-famicom.md) | ✅ Complete |
| Sega Megadrive/Genesis | [sega-megadrive.md](sega-megadrive.md) | ✅ Complete |
| Atari ST | [atari-st.md](atari-st.md) | ✅ Complete |
| ZX Spectrum | [zx-spectrum.md](zx-spectrum.md) | ✅ Complete |
| PC-Engine/TurboGrafx | [pc-engine.md](pc-engine.md) | ✅ Complete |

## Quick Reference

```bash
# Run any demo (auto-detect)
showet-executor /path/to/demo.zip

# Run with explicit platform
showet-executor /path/to/demo.d64 --platform commodore_64
showet-executor /path/to/demo.adf --platform commodore_amiga
showet-executor /path/to/demo.exe --platform microsoft_msdos
showet-executor /path/to/demo.nes --platform nintendo_famicom
```

## Complete Platform Index
See [PLATFORM_INDEX.md](../PLATFORM_INDEX.md) for all 85 supported platforms.

## Related
- [README.md](../../README.md) - Full setup guide
- [ROADMAP.md](../../ROADMAP.md) - Future enhancements