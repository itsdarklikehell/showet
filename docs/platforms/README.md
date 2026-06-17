# Platform Documentation

Each platform has dedicated documentation with setup instructions and demo recommendations.

## Available Documentation

| Platform | File | Status |
|----------|------|--------|
| Commodore 64 | [commodore64.md](platforms/commodore64.md) | ✅ Complete |
| Commodore Amiga | [commodore-amiga.md](platforms/commodore-amiga.md) | ✅ Complete |
| MS-DOS PC | [ms-dos.md](platforms/ms-dos.md) | ✅ Complete |
| Nintendo Famicom/NES | [nintendo-famicom.md](platforms/nintendo-famicom.md) | ✅ Complete |

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

See [PLATFORM_INDEX.md](../PLATFORM_INDEX.md) for full list of 85 supported platforms.