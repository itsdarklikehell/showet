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

- Python script that can download, extract and run demos from pouet.net with the right emulator.
- Supported platforms / emulator
  Microsoft: Windows/wine,native: `exe`
  MS-DOS: ms-dos/dosbox_core_libretro: `exe|com|bat|conf|cue|iso|m3u|zip`
  Apple: `dsk|nib|zip`
  Archimedes: Acorn/mame_libretro: `zip|chd|7z|cmd`
  Atari: Falcon/hatari_libretro: `st|dim|msa|stx|ipf|m3u|vsf|m3u|zip` ST/hatari_libretro: `st|msa|stx|ipf|m3u|vsf|m3u|zip` XLXE/hatari_libretro: `xfd|atr|xfdx|cdm|cas|bin|a52|xex|m3u|zip` Jaguar/virtualjaguar_libretro: `j64|jag|rom|abs|cof|bin|prg` Lynx/handy_libretro `lnx|o|m3u|zip` Vcs/stella_libretro `a26|bin`
  Enterprise: Enterprise/ep128emu_core_libretro: `img|dsk|tap|dtf|com|trn|128|bas|cas|cdt|tzx|.`
  Java: Java/squirreljme_libretro: `jar|sqc|jam|jad|kjx`
  Linux: Linux/native: `exe|elf`
  Mattel: Intellivison/freeintv_libretro :`int|bin|rom`
- GUI frontend

## Usage

- Install the debian package (available in github releases page)
- Launch showet from menu
- Search for a production and click run to run it
- Alt-F4 quits from emulators

### Amiga Notes

- OSECS,AGA,PPCRTG: puae_libretro
- [Libretro Library](https://docs.libretro.com/library/puae/)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/puae_libretro.info)
- `zip|m3u|adf|adz|dms|fdi|ipf|hdf|hdz|lha|tga|slave|info|cue|ccd|nrg|mds|iso|chd|uae|7z|rp9|exe|run`

### Amstrad Notes

- CrocoDS: crocods_libretro
- [Libretro Library](https://docs.libretro.com/library/crocods/)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/crocods_libretro.info)
- `dsk|sna|kcr`

- Caprice: cap32_libretro
- [Libretro Library](https://docs.libretro.com/library/caprice32/)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/cap32_libretro.info)
- `dsk|sna|zip|tap|cdt|voc|cpr|m3u`
  
Amstrad CPC: Debris by Pulpo Corrosivo (<http://www.pouet.net/prod.php?which=92044>)

```bash
./showet.py 92044
```

### Apple(I/II/128K) Notes

- [minivmac](https://www.gryphel.com/c/minivmac/)
- [Libretro Library](https://docs.libretro.com/library/minivmac/)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/minivmac_libretro.info)
- `dsk|nib|zip`

### Archimedes Notes

- [Libretro Library](https://docs.libretro.com/library/mame/)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mame_libretro.info)
- `dsk|nib|zip`

### Commodore Notes

- [Libretro Library](https://docs.libretro.com/library/vice/)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_x64_libretro.info)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_x64sc_libretro.info)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xcpu64_libretro.info)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xpet_libretro.info)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_x128_libretro.info)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xplus4_libretro.info)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xcbm2_libretro.info)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xcbm5x0_libretro.info)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xvic_libretro.info)
- [Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_x128_libretro.info)
- `d64|d71|d80|d81|d82|g64|g41|x64|t64|tap|prg|p00|crt|bin|zip|gz|d6z|d7z|d8z|g6z|g4z|x6z|cmd|m3u|vfl|vsf|nib|nbz|d2m|d4m`

C64/.d64 Comaland by Censor Design & Oxyron (<http://www.pouet.net/prod.php?which=64283>)

```bash
./showet.py 64283
```

## Todo

(for now only retroarch is supported, have not yet implemented any other emulator support.)

- [ ] Clean up this README.md file and make a proper documentation/wiki...
- [x] Archimedes/Acorn Stuff...
      Acorn is Supported by:
      retroarch core(s): `mame_libretro.so` or `mess2015_libretro`
      see `mame_libretro.info` or `mess2015_libretro.info`
- [ ] Alambik Stuff...
      (Have yet to find out whatever that is and how to run them...)
- [x] Amiga Stuff...
      AGA/OCS/ECS/PPC/RTG is Supported by:
      retroarch core(s): `puae_libretro.so`
      see `puae_libretro.info`
      (for now only retroarch is supported, have not yet implemented any other emulator support.)
- [x] Amstrad Stuff...
      CPC/PLUS is Supported by:
      retroarch core(s): `cap32_libretro.so`
      see `cap32_libretro.info`
      (for now only retroarch is supported, have not yet implemented any other emulator support.)
- [ ] Apple Stuff...
      (<https://github.com/audetto/AppleWin>)
- [x] Atari Stuff...
      Falcon/Lynx/ST(e)/TT/VCS/XL/XE is Supported by:
      retroarch cores: `hatari_libretro.so`
      see `hatari_libretro.info`
      Jaguar is Supported by:
      retroarch cores: `virtualjaguar_libretro.so`
      see `virtualjaguar_libretro.info`
      Lynx is Supported by:
      retroarch cores: `handy_libretro.so`
      see `handy_libretro.info`
      VCS is Supported by:
      retroarch cores: `stella_libretro.so`
      see `stella_libretro.info`
      (for now only retroarch is supported, have not yet implemented any other emulator support.)
- [ ] BBC Acorn Stuff...
- [ ] BBC Micro Stuff...
- [x] Commodore Stuff...
      C16/116/plus4/C64/CDTV/C128 is Supported by:
      retroarch core(s): `vice_x64_libretro.so`
      see `vice_x64_libretro.info`
      (for now only retroarch is supported, have not yet implemented any other emulator support.)
- [x] Decompress archives:
      (Currently implemented: .zip .tar .gz .lha)
      (But this is really not needed for retroarch because it can manage (decompress/run) many compressed fileformats.)
      (This is more for those scenes that run in dosbox, wine or proton or if using a native emulator that cant manage compressed files.)
- [ ] Design metadata format to fix non-working demos
- [x] Disk change support.
      (retroarch does support the use of many playlist fileformats. for instance pls, m3u, vfl etc.)
      (As mentioned above, it can also run and decompress many compressed fileformats. for instance .zip .tz .7z .gz .chd and retroarch can automatically generates playlist files after decompressing files if it detects multiple roms/disks.)
- [ ] Debian packaging.
      (Currently not yet fully finished this, but retroarch has its own repos.)
- [ ] (Optional/BONUS QUEST! for 100 points.)
      Make it run/install/update on retropie/batocera/recallbox or plain retroarch on a RaspberryPi.
      Allot of retropie/emulationstation uses retroarch cores to run games, it should not be hard to integrate installation, configuring and running of the scripts of showet into the menus of it it, through the `install.sh` and `update.sh` scripts of this repo.
      (Or if we are really in luck maybe eventually even the retropie team notices/adopts us.)
- [x] DOS Stuff...
      EXE/COM etc. is Supported by:
      retroarch core(s): `dosbox_core_libretro.so`
      see `dosbox_core_libretro.info`
      (for now only retroarch is supported, have not yet implemented any other emulator support.)
- [ ] Flash Stuff... (look into: Flashpoint, lightspark or ruffle)
- [x] GUI...
- [ ] GamePark Stuff...
      (GP2x/GP32)
- [x] General Video/Animation Stuff...
      video is Supported by:
      retroarch core(s): `ffmpeg_libretro.so`
      see `ffmpeg_libretro.info`
- [ ] Intellivison Stuff...
      (see: FreeIntv)
- [ ] Java Stuff...
      (see: freej2me_libretro.info)
- [ ] Linux Stuff...
      (almost working)
- [x] Microsoft Stuff...
      MSX/MSX2/MSX2+/MSX Turbo-r is Supported by:
      retroarch core(s): `bluemsx_libretro.so` `fmsx_libretro.so`
      see `bluemsx_libretro.info` `fmsx_libretro.info`
      WIN (windows) Supported by:
      wine (or proton)
      see wine/proton-tricks for installation of dlls.
- [ ] Microsoft XBOX Stuff...
      (XBOX/XBOX360)
- [x] NeoGeo Stuff...
      pocket/pocket color is Supported by:
      retroarch core(s): `mednafen_ngb_libretro.so`
      see `mednafen_ngb_libretro.info`
- [x] NEC Stuff...
      (TurboGrafx/PC Engine)
- [x] Nintendo Stuff...
      (for now only retroarch is supported, have not yet implemented any other emulator support.)
      NES (Famicom) is Supported by:
      retroarch core(s): `quicknes_libretro.so`
      see `quicknes_libretro.info`
      SNES (Super Famicom) is Supported by:
      retroarch core(s): `snes9x_libretro.so`
      see `snes9x_libretro.info`
      N64 (Reality) is Supported by:
      retroarch core(s): `mupen64plus_next_libretro` `parrallel_n64_libretro.so`
      see `mupen64plus_next_libretro.info` `parrallel_n64_libretro.info`
      GB (Gameboy) GBC (Gameboy Color) is Supported by:
      retroarch core(s): `gambatte_libretro.so` `sameboy_libretro.so`
      see `gambatte_libretro.info` `sameboy_libretro.info`
      GBA (Gameboy Advance) is Supported by:
      retroarch core(s): `vbam_libretro.so` `gpsp_libretro.so`
      see `vbam_libretro.info` `gpsp_libretro.info`
      GC (GameCube) is Supported by:
      retroarch core(s): `dolphin_libretro.so`
      see `dolphin_libretro.info`
      DS (NDS/3DS/3DSi) is Supported by:
      retroarch core(s): `melonds_libretro.so`
      see `melonds_libretro.info`
      VB (VirtuaBoy) is Supported by:
      retroarch core(s):`mednafen_vb_libretro.so`
      see `mednafen_vb_libretro.info`
      WII/WIIu is Supported by:
      retroarch core(s): `dolphin_libretro.so`
      see `dolphin_libretro.info`
      (for now only retroarch is supported, have not yet implemented any other emulator support.)
- [ ] Nintendo Switch Stuff...
- [ ] Oric Stuff... (see oricutron)
- [ ] Option to set/select the emulator
      i.e to select retroarch core if multiple possible cores are available or to use native emulation.
- [ ] Option to set fullscreen on/off.
      (retroarch --fullscreen)
- [ ] Option to set audio on/off.
- [ ] Option for setting custom command line options.
      to pass to chosen emulator (ie retroarch core options or native emulator options).
- [ ] Pico8 Stuff...
- [x] PokeMini Stuff...
      Pokemini is Supported by:
      retroarch core(s): `pokemini_libretro.so`
      see `pokemini_libretro.info`
- [x] Proof of concept...
- [ ] Sega (GameGear/Megadrive/Genesis/mastersystem) Stuff...
- [ ] Sgi IRIX Stuff...
- [ ] Sharp Stuff...
- [ ] Sony (PSX/PS2/PS3/PSP) Stuff... (see duckstation_libretro.info and ppsppp_libretro.)
- [ ] Spectravideo Stuff...
      See bluemsx_libretro.info
- [ ] Steam intergration
      (for the option of using the steam version of retroarch and its cores...)
      (for setting up/using proton...)
- [ ] Thomson Stuff...
      MO/TO
      see theodore_libretro.info
- [ ] Ti-8x (68k/Z80) Stuff...

- [x] TIC80 Stuff...
      TIC80 is Supported by:
      retroarch core(s): `tic80_libretro.so`
      see `tic80_libretro.info`
- [ ] TRS80/CoCo/Dragon32 Stuff...
- [ ] Vectrex Stuff...
- [ ] Whitelist & blacklist of known working & broken demo extensions.
- [ ] WonderSwan Stuff...
- [ ] ZX (ZX Enhanced/ZX Spectrum/ZX 81) Stuff...

Pull requests welcome.

## Command line examples

You can use the command line tool to quickly test running any demos.


Windows: MFX's Deities (<http://www.pouet.net/prod.php?which=24487>)

```bash
./showet.py 24487
```

NES/nes: Matrix(<http://www.pouet.net/prod.php?which=90520>)

```bash
./showet.py 90520
```

SNES/sfc: Bad Apple (<http://www.pouet.net/prod.php?which=91610>)

```bash
./showet.py 91610
```

GB/gb: Turbocharged(<http://www.pouet.net/prod.php?which=91987>)

```bash
./showet.py 91987
```

GBC/gb: Titan - To The Lighthouse!(<http://www.pouet.net/prod.php?which=91968>)

```bash
./showet.py 91968
```

Amiga/dms Origin by Complex (<http://www.pouet.net/prod.php?which=3741>)

```bash
./showet.py 3741
```

Amiga/lha Tint by TBL (<http://www.pouet.net/prod.php?which=701>)

```bash
./showet.py 701
```



To build debian package, run:

```bash
debuild -us -uc -b
```

[![asciicast](https://asciinema.org/a/sXH854ysSs5Ya5C9EGRQB0TzV.png)](https://asciinema.org/a/sXH854ysSs5Ya5C9EGRQB0TzV)

Install the package to get dependencies.

## Authors

Code: Ville Ranki. (Original Author 2004)
Code: Bauke Molenaar. (Since: 2022)
Logo & Icon: Manu / Fit
