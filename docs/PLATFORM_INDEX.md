# Showet Platform Index

Complete list of all 84+ supported platforms with links to detailed documentation.

## Home Computers (8-bit & 16-bit Era)

| Platform | Docs | Emulator |
|----------|------|----------|
| **Commodore 64** | [commodore-64.md](commodore-64.md) | VICE, RetroArch |
| **Commodore Amiga** | [commodore-amiga.md](commodore-amiga.md) | FS-UAE, RetroArch |
| **Commodore 128** | [commodore-128.md](docs/commodore-128.md) | VICE |
| **Commodore VIC-20** | [commodore-vic20.md](docs/commodore-vic20.md) | VICE |
| **Commodore Plus/4** | [commodore-plus4.md](docs/commodore-plus4.md) | VICE |
| **Atari 8-bit** | [atari-xlxe.md](docs/atari-xlxe.md) | Atari800 |
| **Atari ST/Falcon** | [atari-stettfalcon.md](docs/atari-stettfalcon.md) | Hatari |
| **ZX Spectrum** | [sinclair-zxspectrum.md](docs/sinclair-zxspectrum.md) | Fuse |
| **ZX81** | [sinclair-zx81.md](docs/sinclair-zx81.md) | Fuse |
| **Amstrad CPC** | [amstrad-cpcplus.md](docs/amstrad-cpcplus.md) | Cap32 |
| **MSX** | [microsoft-msx.md](docs/microsoft-msx.md) | BlueMSX |
| **PC Engine/TurboGrafx** | [nec-pcengine.md](docs/nec-pcengine.md) | Mednafen |
| **PC-8800/PC-98** | [nec-pc8800.md](docs/nec-pc8800.md), [nec-pc98.md](docs/nec-pc98.md) | Quasi88/Nekop2 |
| **Apple II/IIGS** | [apple-applei.md](docs/apple-applei.md), [apple-appleiigs.md](docs/apple-appleiigs.md) | MiniVMac |
| **Enterprise EP128** | [enterprise-ep128.md](docs/enterprise-ep128.md) | EP128Emu |
| **Oric** | [tangerine-oric.md](docs/tangerine-oric.md) | Oric |
| **Thomson MO/TO** | [thomson-moto.md](docs/thomson-moto.md) | Theodore |

## Gaming Consoles

| Platform | Docs | Emulator |
|----------|------|----------|
| **NES/Famicom** | [nintendo-famicom.md](docs/nintendo-famicom.md) | FCEUX, RetroArch |
| **SNES/Super Famicom** | [nintendo-superfamicom.md](docs/nintendo-superfamicom.md) | Snes9x, RetroArch |
| **Nintendo 64** | [nintendo-n64.md](docs/nintendo-n64.md) | Mupen64Plus |
| **GameCube** | [nintendo-gamecube.md](docs/nintendo-gamecube.md) | Dolphin |
| **PS1** | [sony-psx.md](sony-psx.md) | PCSX-ReARMed, RetroArch |
| **PS2** | [sony-ps2.md](docs/sony-ps2.md) | PCSX2 |
| **Sega Genesis** | [sega-megadrive.md](docs/sega-megadrive.md) | Genesis Plus GX |
| **Sega Master System** | [sega-mastersystem.md](docs/sega-mastersystem.md) | Gearsystem |
| **Sega Game Gear** | [sega-gamegear.md](docs/sega-gamegear.md) | Gearsystem |
| **Sega Dreamcast** | [sega-dreamcast.md](docs/sega-dreamcast.md) | Flycast |
| **Sega Saturn** | [sega-saturn.md](docs/sega-saturn.md) | Yabause |
| **Atari 2600** | [atari-2600.md](atari-2600.md) | Stella, RetroArch |
| **Atari 5200/Lynx** | [atari-5200.md](docs/atari-5200.md), [atari-lynx.md](docs/atari-lynx.md) | Atari800, Handy |

## Arcade & Specialized Systems

| Platform | Docs | Emulator |
|----------|------|----------|
| **Arcade (MAME)** | [arcade-arcade.md](docs/arcade-arcade.md) | RetroArch (MAME2003) |
| **PICO-8** | [fancon-pico8.md](docs/fancon-pico8.md) | Retro8 |
| **Flash/SWF** | [flash-ruffle.md](docs/flash-ruffle.md) | Ruffle |
| **Video/FFmpeg** | [wild-videoffmpeg.md](docs/wild-videoffmpeg.md) | FFmpeg via RetroArch |
| **Game Music** | [wild-gamemusic.md](docs/wild-gamemusic.md) | GME |

## Using Showet with Platforms

### Jukebox Mode
Play demos from specific platforms with loop detection:
```bash
showet-jukebox --ids 12345 --platform commodore_64 --loops 3
```

### Platform-Specific Features
- **C64/Amiga**: Full WHDLoad/BIOS support
- **DOS**: Automatic DOSBox config generation
- **NES/SNES**: Fast loading with RetroArch cores
- **Video demos**: Direct FFmpeg playback

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) to add new platform support.

---
*Part of [Showet](https://github.com/itsdarklikehell/showet) - The demoscene demo-runner*