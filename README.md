# showet

Demo viewer using Pouet.net's metadata

Consider this "MAME for demos"

Developed on Ubuntu (17.10 - 22.10), other platforms may work.

![Screenshot](screenshot.png?raw=true "Screenshot of the GUI")

## Idea

- Browse and search demos using pouet.net's database
- Select a demo, it will be downloaded and set up
- Easily run the demo natively or using emulator (fs-uae, or retroarch) or wine
- Support at least linux, windows .exe (wine), Amiga (UAE), C64 (Vice) demos
- Smart autodetection as far as possible
- Support per-demo metadata to define how it should be run if autodetection fails

## Current implementation

- Python script that can download & run demos
- Supported platforms: windows .exe, Amiga (.adf, .dms, .lha), C64 (d64|d71|d80|d81|d82|g64|g41|x64|t64|tap|prg|p00|crt|bin|zip|gz|d6z|d7z|d8z|g6z|g4z|x6z|cmd|m3u|vfl|vsf|nib|nbz|d2m|d4m)
- GUI frontend

## Usage

- Install the debian package (available in github releases page)
- Launch showet from menu
- Search for a production and click run to run it
- Alt-F4 quits from emulators

### Amiga Notes

For Amiga demos you'll need kickstart rom files. See
http://fs-uae.net/docs/kickstarts on how to obtain and install those.

Setup fs-uae default settings to your liking - it'll be used as
base for launching amiga demos.

### C64 Notes

supported_extensions = "d64|d71|d80|d81|d82|g64|g41|x64|t64|tap|prg|p00|crt|bin|zip|gz|d6z|d7z|d8z|g6z|g4z|x6z|cmd|m3u|vfl|vsf|nib|nbz|d2m|d4m"

Vice shipped with Ubuntu doesn't contain kernal files due to
copyright reasons.

- Go to http://vice-emu.sourceforge.net/index.html#download and download
  the source tarball.
- Create directory ~/.vice
- Copy everything from tarball's data/ directory to ~/.vice

You can configure vice / x64 any way you want. Showet starts it
with -fullscreen by default

Use Alt-N to cycle disk sides for multi-disk demos.

## Todo

- [x] Proof of concept
- [x] Windows Supported by: wine
- [ ] General Video/Animation Stuff... (could use VLC here.)
- [x] Amiga Supported by: retroarch core(s):
- [ ] Atari (Falcon/Jaguar/Lynx/ST(e)/TT/VCS/XL/XE) Supported by: retroarch cores: hatari_libretro
- [x] Commodore (C16/116/plus4/C64/CDTV/C128) Supported by: retroarch core(s): vice_x64_libretro
- [x] Nintendo NES (Famicom) Supported by: retroarch core(s): quicknes_libretro
- [x] Nintendo SNES (Super Famicom) Supported by: retroarch core(s): snes9x_libretro
- [x] Nintendo N64 Supported by: retroarch core(s): mupen64plus_next_libretro, parrallel_n64_libretro
- [x] Nintendo GB (Gameboy) Supported by: retroarch core(s): gambatte_libretro, sameboy_libretro
- [x] Nintendo GBC (Gameboy Color) Supported by: retroarch core(s): gambatte_libretro, sameboy_libretro
- [x] Nintendo GBA (Gameboy Advance) Supported by: retroarch core(s): vbam_libretro, gpsp_libretro
- [x] Nintendo GC (GameCube) Supported by: retroarch core(s): dolphin_libretro
- [x] Nintendo DS (NDS/3DS/3DSi) Supported by: retroarch core(s): menlonds_libretro
- [x] Nintendo VB (VirtuaBoy) Supported by: retroarch core(s): mednafen_vb_libretro
- [x] Nintendo WII/WIIu Supported by: retroarch core(s): dolphin_libretro
- [ ] Nintendo Switch Stuff...
- [x] PokeMini Stuff... (see pokemini_libretro.info implementing this should be easy, there are only 3 scenes for this system so obviously not a priority..)
- [ ] WonderSwan Stuff...
- [ ] Amstrad (CPC/PLUS) Stuff... (see cap32_libretro.info)
- [ ] Sega (GameGear/Megadrive/Genesis/mastersystem) Stuff...
- [ ] Pico8 Stuff...
- [ ] TIC80 Stuff...
- [ ] TRS80/CoCo/Dragon32 Stuff...
- [ ] Vectrex Stuff...
- [ ] Sony (PSX/PS2/PS3/PSP) Stuff... (see duckstation_libretro.info and ppsppp_libretro.)
- [ ] Apple Stuff...
- [ ] GamePark (GP2x/GP32) Stuff...
- [ ] Microsoft (MSX/MSX2/MSX2+/MSX Turbo-r) Stuff...
- [ ] Microsoft (XBOX/XBOX360) Stuff...
- [ ] NEC TurboGrafx/PC Engine Stuff...
- [ ] NeoGeo (pocket/pocket color) Stuff...
- [ ] Intellivison Stuff... (see: FreeIntv)
- [ ] Java Stuff... (see: freej2me_libretro.info)
- [ ] Flash Stuff... (see: Flashpoint)
- [ ] ZX (ZX Enhanced/ZX Spectrum/ZX 81) Stuff...
- [x] DOS support: Supported by: retroarch core(s): dosbox_core_libretro
- [ ] Linux support (almost working) Supported by: OS
- [x] GUI
- [ ] Option to set/select the emulator (retroarch core or native emulation) to run if more than one is supported.
- [ ] Option to set fullscreen on/off. (retroarch --fullscreen)
- [ ] Option to set audio on/off.
- [ ] Option for setting custom commandline options to pass to chosen emulator (core).
- [x] unzip decompress (This is really not needed for retroarch but more for those that run in dosbox or wine.)
- [x] unrar decompress (Same as above.)
- [x] tar/gz/lhA decompress (Same as above.)
- [ ] Design metadata format to fix non-working demos
- [ ] Disk change support (C64/Amiga) (PSX) (retroarch has playlist support for pls, m3u, vfl etc.)
- [x] debian packaging
- [ ] Whitelist & blacklist of known working & broken demos

Pull requests welcome.

## Command line examples

You can use the command line tool to quickly test running any demos.

Windows: MFX's Deities (http://www.pouet.net/prod.php?which=24487)

```
./showet.py 24487
```

NES/nes: Matrix(http://www.pouet.net/prod.php?which=90520)

```
./showet.py 90520
```

SNES/sfc: Bad Apple (http://www.pouet.net/prod.php?which=91610)

```

./showet.py 91610
```

GB/gb: Turbocharged(http://www.pouet.net/prod.php?which=91987)

```
./showet.py 91987
```

GBC/gb: Titan - To The Lighthouse!(http://www.pouet.net/prod.php?which=91968)

```
./showet.py 91968
```

Amiga/dms Origin by Complex (http://www.pouet.net/prod.php?which=3741)

```
./showet.py 3741
```

Amiga/lha Tint by TBL (http://www.pouet.net/prod.php?which=701)

```
./showet.py 701
```

C64/.d64 Comaland by Censor Design & Oxyron (http://www.pouet.net/prod.php?which=64283)

```
./showet.py 64283
```

To build debian package, run:

```
debuild -us -uc -b
```

[![asciicast](https://asciinema.org/a/sXH854ysSs5Ya5C9EGRQB0TzV.png)](https://asciinema.org/a/sXH854ysSs5Ya5C9EGRQB0TzV)

Install the package to get dependencies.

## Authors:

Code: 2004: Ville Ranki 2022: Bauke Molenaar.
Logo & Icon: Manu / Fit
