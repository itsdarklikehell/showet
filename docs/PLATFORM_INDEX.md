# Showet Platform Index

Complete list of all 84+ supported platforms with links to detailed documentation.

## Home Computers (8-bit & 16-bit Era)

| Platform | Documentation | Extensions | Emulator |
|----------|---------------|------------|----------|
| [Commodore 64](commodore-64.md) | ✅ | `.d64`, `.t64`, `.prg`, `.tap`, `.crt` | VICE, RetroArch |
| [Commodore 128](commodore-128.md) | ✅ | `.d64`, `.d71`, `.d81` | VICE, RetroArch |
| [Commodore Amiga](commodore-amiga.md) | ✅ | `.adf`, `.hdf`, `.ipf` | FS-UAE, RetroArch |
| [Apple II](apple-ii.md) | ✅ | `.dsk`, `.nib`, `.po` | AppleWin, RetroArch |
| [Apple IIGS](apple-iigs.md) | ✅ | `.2mg`, `.dsk` | GSplus, RetroArch |
| [Atari 8-bit](atari-xlxe.md) | ✅ | `.atr`, `.cas`, `.xex` | Altirra, RetroArch |
| [Atari ST](atari-st.md) | ✅ | `.sti`, `.msa` | Hatari, RetroArch |
| [ZX Spectrum](sinclair-zxspectrum.md) | ✅ | `.tap`, `.tzx`, `.z80` | Fuse, RetroArch |
| [Amstrad CPC](amstrad-cpcplus.md) | ✅ | `.dsk`, `.cpr` | Caprice32, RetroArch |

## Gaming Consoles

| Platform | Documentation | Extensions | Emulator |
|----------|---------------|------------|----------|
| [NES/Famicom](nintendo-famicom.md) | ✅ | `.nes`, `.fds` | FCEUX, RetroArch |
| [SNES/Super Famicom](nintendo-superfamicom.md) | ✅ | `.smc`, `.sfc` | Snes9x, RetroArch |
| [Sega Master System](sega-mastersystem.md) | ✅ | `.sms`, `.gg` | Genesis Plus GX |
| [Sega Genesis/Mega Drive](sega-megadrive.md) | ✅ | `.md`, `.bin` | Gens, RetroArch |
| [Atari 2600](atari-2600.md) | ✅ | `.a26`, `.bin` | Stella, RetroArch |

## Modern Platforms

| Platform | Documentation | Extensions | Runtime |
|----------|---------------|------------|----------|
| [Flash/Ruffle](flash-ruffle.md) | ✅ | `.swf` | Ruffle/Web |
| [Android](android-android.md) | ✅ | `.apk` | Android Emulator |
| [WebAssembly](webassembly-web.md) | Planned | `.wasm` | Browser |

## Demoscene-Specific

| Platform | Documentation | Extensions | Notes |
|----------|---------------|------------|-------|
| [DOS/PC](microsoft-msdos.md) | Planned | `.exe`, `.com` | DOSBox-X, Wine |
| [Windows](microsoft-windows.md) | Planned | `.exe` | Wine, Proton |

## Unknown Platforms (Need Documentation)

These platforms are supported but lack detailed documentation:
- Enterprise EP128
- PC-8800, PC-98, PC-FX
- Neo Geo, Neo Geo Pocket
- WonderSwan
- Vectrex
- Phillips CD-i
- 3DO
- Saturn, Dreamcast
- Nintendo 64, GameCube
- PlayStation
- And many more...

## Using the Universal Executor

```bash
# Run any demo file with auto-detection
showet-universal /path/to/demo.zip

# Specify platform manually
showet-universal /path/to/demo.exe --platform windows

# Extract and run
showet-universal --extract /path/to/demo.rar
```

## Adding New Platforms

Each platform requires:
1. `Platform_<Platform>_<System>.py` - Runner class
2. `docs/<platform>-<system>.md` - Documentation
3. Entry in `PLATFORM_EXTENSIONS` in `showet_executor.py`

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.