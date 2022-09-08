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

Puae: puae_libretro

- [Puae Libretro Library](https://docs.libretro.com/library/puae/)
- [Puae Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/puae_libretro.info)
- `zip|m3u|adf|adz|dms|fdi|ipf|hdf|hdz|lha|tga|slave|info|cue|ccd|nrg|mds|iso|chd|uae|7z|rp9|exe|run`

### Amstrad Notes

CrocoDS: crocods_libretro

- [CrocoDS Libretro Library](https://docs.libretro.com/library/crocods/)
- [CrocoDS Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/crocods_libretro.info)
- `dsk|sna|kcr`

Caprice: cap32_libretro

- [Caprice32 Libretro Library](https://docs.libretro.com/library/caprice32/)
- [Cap32 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/cap32_libretro.info)
- `dsk|sna|zip|tap|cdt|voc|cpr|m3u`
  
Amstrad CPC: Debris by Pulpo Corrosivo (<http://www.pouet.net/prod.php?which=92044>)

```bash
./showet.py 92044
```

### Apple(I/II/128K) Notes

Minivmac: minivmac_libretro

- [Minivmac Libretro Library](https://docs.libretro.com/library/minivmac/)
- [Minivmac Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/minivmac_libretro.info)
- `dsk|nib|zip`

### Archimedes Notes

Mame: mame_libretro

- [Mame Libretro Library](https://docs.libretro.com/library/mame/)
- [Mame Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mame_libretro.info)
- `dsk|nib|zip`

### Commodore Notes

Vice: vice_[version]_libretro

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
- `d64|d71|d80|d81|d82|g64|g41|x64|t64|tap|prg|p00|crt|bin|zip|gz|d6z|d7z|d8z|g6z|g4z|x6z|cmd|m3u|vfl|vsf|nib|nbz|d2m|d4m`

C64/.d64 Comaland by Censor Design & Oxyron (<http://www.pouet.net/prod.php?which=64283>)

```bash
./showet.py 64283
```

## Todo

(for now only retroarch is supported, have not yet implemented any other emulator support.)

- [ ] Clean up this README.md file and make a proper documentation/wiki...
- [ ] Alambik Stuff...
      (Have yet to find out whatever that is and how to run them...)
- [ ] Apple Stuff... See: Minivmac Libretro
- [ ] BBC Acorn Stuff...
- [ ] BBC Micro Stuff...
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
- [ ] (Optional/BONUS QUEST! for 100 points.)
      Make it run/install/update on retropie/batocera/recallbox or plain retroarch on a RaspberryPi.
      Allot of retropie/emulationstation uses retroarch cores to run games, it should not be hard to integrate installation, configuring and running of the scripts of showet into the menus of it it, through the `install.sh` and `update.sh` scripts of this repo.
      (Or if we are really in luck maybe eventually even the retropie team notices/adopts us.)
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
- [ ] Steam intergration
      (for the option of using the steam version of retroarch and its cores...)
      (for setting up/using proton...)
- [ ] Thomson Stuff...
      MO/TO
      see theodore_libretro.info
- [ ] Ti-8x (68k/Z80) Stuff...
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
