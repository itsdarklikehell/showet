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
| [PC-98](nec-pc98.md) | ✅ | `.d98`, `.hdi`, `.zip` | Mednafen, RetroArch |
| [PC-FX](nec-pcfx.md) | ✅ | `.cue`, `.bin`, `.iso` | Mednafen, RetroArch |
| [Phillips CD-i](phillips-cdi.md) | ✅ | `.cue`, `.bin`, `.iso` | RetroArch, MAME |
| [Enterprise EP128](enterprise-ep128.md) | 🔄 | `.ep128`, `.tap` | EP128Emu |
| [Oric](tangerine-oric.md) | 🔄 | `.tap`, `.wav` | Oricutron |
| [Sharp MZ](sharp-mz.md) | 🔄 | `.mzt`, `.m12` | MZ800Emu |

## Gaming Consoles

| Platform | Documentation | Extensions | Emulator |
|----------|---------------|------------|----------|
| [NES/Famicom](nintendo-famicom.md) | ✅ | `.nes`, `.fds` | FCEUX, RetroArch |
| [SNES/Super Famicom](nintendo-superfamicom.md) | ✅ | `.smc`, `.sfc` | Snes9x, RetroArch |
| [Sega Master System](sega-mastersystem.md) | ✅ | `.sms`, `.gg` | Genesis Plus GX |
| [Sega Genesis/Mega Drive](sega-megadrive.md) | ✅ | `.md`, `.bin` | Gens, RetroArch |
| [Atari 2600](atari-2600.md) | ✅ | `.a26`, `.bin` | Stella, RetroArch |
| [Game Boy](nintendo-gameboy.md) | 🔄 | `.gb` | Gambatte, RetroArch |
| [Game Boy Color](nintendo-gameboycolor.md) | 🔄 | `.gbc` | Gambatte, RetroArch |
| [Neo Geo](snk-neogeo.md) | 🔄 | `.zip`, `.neo` | FBAlpha, RetroArch |
| [Neo Geo Pocket](snk-neogeopocket.md) | 🔄 | `.ngp` | Mednafen, RetroArch |
| [WonderSwan](bandai-wonderswan.md) | 🔄 | `.ws` | Cygne, RetroArch |
| [Vectrex](gce-vectrex.md) | 🔄 | `.vec` | Vecx, RetroArch |

## Modern Platforms

| Platform | Documentation | Extensions | Runtime |
|----------|---------------|------------|----------|
| [Flash/Ruffle](flash-ruffle.md) | ✅ | `.swf` | Ruffle/Web |
| [Android](android-android.md) | ✅ | `.apk` | Android Emulator |
| [WebAssembly](webassembly-web.md) | Planned | `.wasm` | Browser |
| [PICO-8](fancon-pico8.md) | 🔄 | `.p8`, `.png` | PICO-8, RetroArch |

## Demoscene-Specific

| Platform | Documentation | Extensions | Notes |
|----------|---------------|------------|-------|
| [DOS/PC](microsoft-msdos.md) | ✅ | `.exe`, `.com` | DOSBox-X, Wine |
| [Windows](microsoft-windows.md) | 🔄 | `.exe` | Wine, Proton |
| [Linux](linux-linux.md) | 🔄 | Native executables | Native |
| [Video](wild-videoffmpeg.md) | 🔄 | `.mp4`, `.avi` | FFmpeg |
| [Game Music](wild-gamemusic.md) | 🔄 | `.vgz`, `.nsf` | MediaPlayer |

## Using the Universal Executor

```bash
# Run any demo file with auto-detection
showet run /path/to/demo.zip

# Play jukebox
showet jukebox --ids 12345 67890

# Stream to platform
showet stream --platform twitch --demo 12345
```

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*