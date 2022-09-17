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
- GUI frontend

## Usage

- Install the debian package (available in github releases page)
- Launch showet from menu
- Search for a production and click run to run it
- Alt-F4 quits from emulators

## Build instructions

Clone the repo:

```bash
git clone https://github.com/itsdarklikehell/showet
cd showet
./install.sh --update
./install.sh --install-showet
./install.sh --install-emulators
```

To build debian package, run:

```bash
debuild -us -uc -b
```

Install the package to get dependencies.

## Supported Platforms

### Amiga Notes

Puae: `puae_libretro`

- [Puae Libretro Library](https://docs.libretro.com/library/puae/)
- [Puae Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/puae_libretro.info)

Supported filetypes:

- Floppies: `adf|adz|dms|fdi|ipf`
- Hard Drives: `hdf|hdz|directory`
- WHDLoad: `lha|slave|info`
- CDs: `cue|ccd|chd|nrg|mds|iso`
- Other: `uae|m3u|zip|7z|rp9|exe`

Example(s):

- [Starstruck By Black Lotus](http://www.pouet.net/prod.php?which=25778)
- type: `zip,exe`
- CLI: `./showet.py 22778`

### Amstrad Notes

CrocoDS: `crocods_libretro`

- [CrocoDS Libretro Library](https://docs.libretro.com/library/crocods/)
- [CrocoDS Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/crocods_libretro.info)

Supported filetypes:

- `dsk|sna|kcr`

Example(s):

- [CRTC3 By Flower Corp](http://www.pouet.net/prod.php?which=248542)
- type: (multidisk) `zip,dsk`
- CLI: `./showet.py 248542`

Caprice: `cap32_libretro`

- [Caprice32 Libretro Library](https://docs.libretro.com/library/caprice32/)
- [Cap32 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/cap32_libretro.info)

Supported filetypes:

- `dsk|sna|zip|tap|cdt|voc|cpr|m3u`

Example(s):

- [Batman Forever By Batman Group](http://www.pouet.net/prod.php?which=56761)
- type: (multidisk) `zip,dsk`
- CLI: `./showet.py 56761`

### Apple(I/II/128K) Notes

Minivmac: `minivmac_libretro`

- [Minivmac Libretro Library](https://docs.libretro.com/library/minivmac/)
- [Minivmac Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/minivmac_libretro.info)

Supported filetypes:

- `dsk|img|zip|hvf|cmd`

Example(s):

- [Apple-Vision By Bob Bishop](http://www.pouet.net/prod.php?which=54410)
- type: `zip,dsk`
- CLI: `./showet.py 54410`

### Archimedes Notes

Mame: `mame_libretro`

- [Mame Libretro Library](https://docs.libretro.com/library/mame/)
- [Mame Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mame_libretro.info)

Supported filetypes:

- `zip|chd|7z|cmd`

Example(s):

### Atari Notes

Hatari: `hatari_libretro`

- [Hatari Libretro Library](https://docs.libretro.com/library/hatari/)
- [Hatari Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/hatari_libretro.info)

Supported filetypes:

- `st|msa|zip|stx|dim|ipf|m3u`

Example(s):

Virtualjaguar: `virtualjaguar_libretro`

- [Virtualjaguar Libretro Library](https://docs.libretro.com/library/virtual_jaguar/)
- [Virtualjaguar Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/virtualjaguar_libretro.info)

Supported filetypes:

- `j64|jag|rom|abs|cof|bin|prg`

Example(s):

Handy: `handy_libretro`

- [Handy Libretro Library](https://docs.libretro.com/library/handy/)
- [Handy Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/handy_libretro.info)

Supported filetypes:

- `lnx|o`

Example(s):

Stella: `stella_libretro`

- [Stella Libretro Library](https://docs.libretro.com/library/stella/)
- [Stella Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/stella_libretro.info)

Supported filetypes:

- `a26|bin`

Example(s):

### Commodore Notes

Vice: `vice_[version]_libretro`

- [Vice Libretro Library](https://docs.libretro.com/library/vice/)
- [Vice x64 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_x64_libretro.info)
- [Vice x64sc Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_x64sc_libretro.info)
- [Vice xcpu64 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xcpu64_libretro.info)
- [Vice xpet Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xpet_libretro.info)
- [Vice x128 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_x128_libretro.info)
- [Vice xplus4 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xplus4_libretro.info)
- [Vice xcbm2 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xcbm2_libretro.info)
- [Vice xcbm5x0 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xcbm5x0_libretro.info)
- [Vice xvic Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vice_xvic_libretro.info)

Supported filetypes:

- Floppies: `d64|d6z|d71|d7z|d80|d81|d82|d8z|g64|g6z|g41|g4z|x64|x6z|nib|nbz|d2m|d4m`
- Tapes: `t64|tap`
- Other: `cmd|m3u|vfl|vsf|zip|7z|gz|prg|p00|crt|bin`
- VIC20: `20|40|60|a0|b0|rom`

Example(s):

- [Comaland by Censor Design & Oxyron](http://www.pouet.net/prod.php?which=64283)
- CLI: `./showet.py 64283`

### Enterprise 64/128 Notes

Ep128emu: `ep128emu_libretro`

- [ep128emu Libretro Library](https://docs.libretro.com/library/ep128emu/)
- [ep128emu Libretro core info](https://github.com/libretro/ep128emu-core/blob/core/ep128emu_libretro.info)

Supported filetypes:

- `img|dsk|tap|dtf|com|trn|128|bas|cas|cdt|tzx|.`

Example(s):

### Java Notes

Squirreljme: `squirreljme_libretro`

- [Squirreljme Libretro Library](https://github.com/SquirrelJME/SquirrelJME)
- [Squirreljme Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/squirreljme_libretro.info)

Supported filetypes:

- `jar|sqc|jam|jad|kjx`

Example(s):

### Linux Notes

### Mattel Notes

Freeintv: `freeintv_libretro`

- [Freeintv Libretro Library](https://docs.libretro.com/library/freeintv/)
- [Freeintv Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/freeintv_libretro.info)

Supported filetypes:

- `int|bin|rom`

Example(s):

### Microsoft Notes

Directxbox: `directxbox_libretro`

- [Directxbox Libretro Library](https://docs.libretro.com/library/directxbox/)
- [Directxbox Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/directxbox_libretro.info)

Supported filetypes:

- `iso`

Example(s):

Bluemsx: `bluemsx_libretro`

- [Bluemsx Libretro Library](https://docs.libretro.com/library/bluemsx/)
- [Bluemsx Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/bluemsx_libretro.info)

Supported filetypes:

- `rom|ri|mx1|mx2|col|dsk|cas|sg|sc|m3u`

Example(s):

Wine: `wine`

- [Wine Manual](https://linux.die.net/man/1/wine)

Supported filetypes:

- `bat|com|exe`

Example(s):

### MsDOS Notes

Dosbox: `dosbox_libretro`

- [Dosbox Libretro Library](https://docs.libretro.com/library/dosbox/)
- [Dosbox Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/dosbox_libretro.info)

Supported filetypes:

- `exe|com|bat|conf`

Example(s):

### Music Notes

GameMusicEmu: `gme_libretro`

- [GameMusicEmu Libretro Library](https://docs.libretro.com/library/game_music_emu/)
- [GameMusicEmu Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/gme_libretro.info)

Supported filetypes:

- `ay|gbs|gym|hes|kss|nsf|nsfe|sap|spc|vgm|vgz|zip`

Example(s):

### Nec Notes

Mednafen Supergrafx: `mednafen_supergrafx_libretro`

- [Mednafen Supergrafx Libretro Library](https://docs.libretro.com/library/beetle_sgx/)
- [Mednafen Supergrafx Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_supergrafx.info)

Supported filetypes:

- `pce|sgx|cue|ccd|chd`

Example(s):

### NeoGeo Notes

Mednafen Ngp: `mednafen_ngp_libretro`

- [Mednafen Ngp Libretro Library](https://docs.libretro.com/library/beetle_neopop/)
- [Mednafen Ngp Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_ngp_libretro.info)

Supported filetypes:

- `ngp|ngc|ngpc|npc`

Example(s):

Mednafen Ngpc: `mednafen_ngpc_libretro`

- [Mednafen Ngpc Libretro Library](https://docs.libretro.com/library/beetle_neopop/)
- [Mednafen Ngpc Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_ngpc_libretro.info)

Supported filetypes:

- `ngp|ngc|ngpc|npc`

Example(s):

### Nintendo Notes

Quicknes: `quicknes_libretro`

- [Quicknes Libretro Library](https://docs.libretro.com/library/quicknes/)
- [Quicknes Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/quicknes_libretro.info)

Supported filetypes:

- `nes`

Example(s):

Snes9x: `snes9x_libretro`

- [Snes9x Libretro Library](https://docs.libretro.com/library/snes9x/)
- [Snes9x Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/snes9x_libretro.info)

Supported filetypes:

- `smc|sfc|swc|fig|bs|st`

Example(s):

Mupen64plus: `mupen64plus_next_libretro`

- [Mupen64plus Libretro Library](https://docs.libretro.com/library/mupen64plus/)
- [Mupen64plus Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mupen64plus_next_libretro.info)

Supported filetypes:

- `n64|v64|z64|bin|u1`

Example(s):

Gambatte: `gambatte_libretro`

- [Gambatte Libretro Library](https://docs.libretro.com/library/gambatte/)
- [Gambatte Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/gambatte_libretro.info)

Supported filetypes:

- `gb|gbc|dmg`

Example(s):

VisualBoyAdvanced: `vba_next_libretro`

- [VisualBoyAdvanced Libretro Library](https://docs.libretro.com/library/vba_next/)
- [VisualBoyAdvanced Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vba_next_libretro.info)

Supported filetypes:

- `gba`

Example(s):

Dolphin: `dolphin_libretro`

- [Dolphin Libretro Library](https://docs.libretro.com/library/dolphin/)
- [Dolphin Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/dolphin_libretro.info)

Supported filetypes:

- `gcm|iso|wbfs|ciso|gcz|elf|dol|dff|tgc|wad|rvz|m3u`

Example(s):

Pokemini: `pokemini_libretro`

- [Pokemini Libretro Library](https://docs.libretro.com/library/pokemini/)
- [Pokemini Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/pokemini_libretro.info)

Supported filetypes:

- `min`

Example(s):

MelonDS: `melonds_libretro`

- [MelonDS Libretro Library](https://docs.libretro.com/library/melonds/)
- [MelonDS Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/melonds_libretro.info)

Supported filetypes:

- `nds|dsi`

Example(s):

Mednafen: `mednafen_vb_libretro`

- [MelonDS Libretro Library](https://docs.libretro.com/library/beetle_vb/)
- [MelonDS Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_vb_libretro.info)

Supported filetypes:

- `vb|vboy|bin`

Example(s):

### PalmOS Notes

Mu: `mu_libretro`

- [Mu Libretro Library](https://docs.libretro.com/library/mu/)
- [Mu Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mu_libretro.info)

Supported filetypes:

- `prc|pqa|img|pdb`

Example(s):

### Pico8 Notes

Retro8: `retro8_libretro`

- [Retro8 Libretro Library](https://docs.libretro.com/library/retro8/)
- [Retro8 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/retro8_libretro.info)

Supported filetypes:

- `p8|png`

Example(s):

### Sega Notes

Genesis plus GX: `genesis_plus_gx_libretro`

- [Genesis plus GX Libretro Library](https://docs.libretro.com/library/genesis_plus_gx/)
- [Genesis plus GX Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/genesis_plus_gx_libretro.info)

Supported filetypes:

- `mdx|md|smd|gen|bin|cue|iso|sms|bms|gg|sg|68k|sgd|chd|m3u`

Example(s):

Gearsystem: `gearsystem_libretro`

- [Gearsystem Libretro Library](https://docs.libretro.com/library/gearsystem/)
- [Gearsystem Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/gearsystem_libretro.info)

Supported filetypes:

- `sms|gg|sg|bin|rom`

Example(s):

Flycast: `flycast_libretro`

- [Flycast Libretro Library](https://docs.libretro.com/library/flycast/)
- [Flycast Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/flycast_libretro.info)

Supported filetypes:

- `sms|gg|sg|bin|rom`

Example(s):

FlycastGLES2: `flycast_gles2_libretro`

- [Flycast Libretro Library](https://docs.libretro.com/library/flycast/)
- [Flycast Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/flycast_gles2_libretro.info)

Supported filetypes:

- `chd|cdi|elf|bin|cue|gdi|lst|zip|dat|7z|m3u`

Example(s):

### Sinclair Notes

Fuse: `fuse_libretro`

- [Fuse Libretro Library](https://docs.libretro.com/library/fuse/)
- [Fuse Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/fuse_libretro.info)

Supported filetypes:

- `tzx|tap|z80|rzx|scl|trd|dsk|zip`

Example(s):

81: `81_libretro`

- [81 Libretro Library](https://docs.libretro.com/library/eightyone/)
- [81 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/81_libretro.info)

Supported filetypes:

- `p|tzx|t81`

Example(s):

### Sony Notes

Mednafen: `mednafen_psx_libretro`

- [Mednafen Libretro Library](https://docs.libretro.com/library/beetle_psx/)
- [PCSX ReARMed Libretro Library](https://docs.libretro.com/library/pcsx_rearmed/)
- [Mednafen Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_psx_libretro.info)
- [Rustation Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/rustation_libretro.info)
- [Duckstation Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/ducktation_libretro.info)

Supported filetypes:

- `cue|toc|m3u|ccd|exe|pbp|chd`

Example(s):

Pcsx2: `pcsx2_libretro`

- [Pcsx2 Libretro Library](https://docs.libretro.com/library/pcsx2/)
- [Pcsx2 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/pcsx2_libretro.info)

Supported filetypes:

- `elf|iso|ciso|chd|cso|bin|mdf|nrg|dump|gz|img|m3u`

Example(s):

Ppsspp: `ppsspp_libretro`

- [Ppsspp Libretro Library](https://docs.libretro.com/library/ppsspp/)
- [Ppsspp Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/ppsspp_libretro.info)

Supported filetypes:

- `elf|iso|cso|prx|pbp`

Example(s):

### Tic80 Notes

Tic80: `tic80_libretro`

- [Tic80 Libretro Library](https://docs.libretro.com/library/tic80/)
- [Tic80 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/tic80_libretro.info)

Supported filetypes:

- `tic`

Example(s):

### Vectrex Notes

Tic80: `vecx_libretro`

- [Tic80 Libretro Library](https://docs.libretro.com/library/vecx/)
- [Tic80 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vecx_libretro.info)

Supported filetypes:

- `bin|vec`

Example(s):

### Video Notes

FFmpeg: `ffmpeg_libretro`

- [Tic80 Libretro Library](https://docs.libretro.com/library/ffmpeg/)
- [Tic80 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/ffmpeg_libretro.info)

Supported filetypes:

- `mkv|avi|f4v|f4f|3gp|ogm|flv|mp4|mp3|flac|ogg|m4a|webm|3g2|mov|wmv|mpg|mpeg|vob|asf|divx|m2p|m2ts|ps|ts|mxf|wma|wav`

Example(s):

## Todo

(for now only retroarch emulation is supported, have not yet implemented any other emulator support.)

- [ ] Clean up and finish the rest of this too damn long README.md file or make some awesome ascii art filled cli help/documentation or wiki thing...
- [ ] Alambik Stuff...
      (Have yet to find out whatever that is and how to run them...)
- [ ] Decompress archives:
      (Currently implemented: .zip .tar .gz .lha)
      (But this is really not needed for retroarch because it can manage (decompress/run) many compressed fileformats.)
      (This is more for those scenes that run in dosbox, wine or proton or if using a native emulator that cant manage compressed files.)
- [ ] Design metadata format to fix non-working demos
- [x] Disk change support.
      (retroarch does support the use of many playlist fileformats. for instance pls, m3u, vfl etc.)
      (As mentioned above, it can also run and decompress many compressed fileformats. for instance .zip .tz .7z .gz .chd and retroarch can automatically generates playlist files after decompressing files if it detects multiple roms/disks.)
- [ ] Debian packaging.
      (Currently not yet fully finished this, but retroarch has its own repos.)
- [ ] Flash Stuff... (look into: Flashpoint, lightspark or ruffle)
- [x] GUI...
- [ ] GamePark Stuff...
      (GP2x/GP32)
- [ ] Linux Stuff...
      (almost working)
- [ ] Microsoft XBOX Stuff...
      (XBOX/XBOX360)
- [ ] Nintendo Switch Stuff...
- [ ] Oric Stuff... (see oricutron)
- [ ] Option to set/select the emulator
      i.e to select retroarch core if multiple possible cores are available or to use native emulation.
- [ ] Option to set fullscreen on/off.
      (retroarch --fullscreen)
- [ ] Option to set audio on/off.
- [ ] Option for setting custom command line options.
      to pass to chosen emulator (ie retroarch core options or native emulator options).
- [x] Proof of concept...
- [ ] Sgi IRIX Stuff...
- [ ] Sharp Stuff...
- [ ] Steam version intergration...
      (either for the option of using the steam version of retroarch and its cores and/or for setting up a proton version to rin stuff in incase needed...)
- [ ] Thomson Stuff...
      MO/TO
      see theodore_libretro.info
- [x] Ti-8x (68k/Z80) Stuff...
- [ ] TRS80/CoCo/Dragon32 Stuff...
- [x] Vectrex Stuff...
- [ ] Whitelist & blacklist of known working & broken demo extensions.
- [x] WonderSwan Stuff...
- [x] ZX (ZX Enhanced/ZX Spectrum/ZX 81) Stuff...
- [ ] (Optional/BONUS QUEST! for 100 points.)
      Make it run/install/update on retropie/batocera/recallbox or plain retroarch on a RaspberryPi.
      Allot of retropie/emulationstation uses the same retroarch cores to run roms, it should not be hard to integrate installation, configuring and running of these scripts of showet into the menus of it it, either through running the `install.sh` or `update.sh` scripts of this repo and add them to the `~/RetroPie/retropiemenu/` folder.
      (And if we are really in luck maybe eventually even the RetroPie-Setup team will add(opt) us.. and thereby help give the DemoScene some much needed love and attention!)

Pull requests and suggestions are always welcome (if they are not breaking anything).

## Authors

Code: Ville Ranki. (Original Author 2004)
Code: Bauke Molenaar. (Since: 2022)
Logo & Icon: Manu / Fit
