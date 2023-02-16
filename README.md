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

### 3do / 4do

See: [Docs/platform_3do.md](Docs/platform_3do.md) for more information.

### Amstrad Notes

See: [platform_Amstrad.md](platform_Amstrad.md) for more information.

### Amiga Notes

Current: `puae2021_libretro`

options:
FS-UAE: `fsuae_libretro`
UAE4ARM: `uae4arm_libretro`
Puae: `puae_libretro`
Puae2021: `puae2021_libretro`

- [FS-uae Libretro Library](https://docs.libretro.com/library/fsuae/)
- [Puae Libretro Library](https://docs.libretro.com/library/puae/)
- [Uae4arm Libretro Library](https://docs.libretro.com/library/uae4arm/)

- [FS-UAE Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/fsuae_libretro.info)
- [Puae Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/puae_libretro.info)
- [Puae 2021 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/puae2021_libretro.info)
- [UAE4ARM Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/uae4arm_libretro.info)

Supported filetypes:
FS-UAE: `adf|ipf|fs-uae`
UAE4ARM: `adf|dms|ipf|adz|wrp|zip|uae|lha|cue|ccd|iso|hdf`

PUA:
Floppies: `adf|adz|dms|fdi|ipf`
Hard Drives: `hdf|hdz|directory|.`
WHDLoad: `lha|slave|info`
CDs: `cue|ccd|chd|nrg|mds|iso`
Other: `uae|m3u|zip|7z|rp9|exe`

Example(s):

AGA:
Name: Mare
By: Ephidrena
Type: demo
Platform: amigaaga
`./showet.py 92240`

OCS/ECS:
Name: MMXXII
By: Cocoon
Type: demo
Platform: amigaocsecs
`./showet.py 92365`

PPC/RTG:
Name: Eighteen
By: Triad
Type: demo,wild
Platform: amigappcrtg
`./showet.py 92257`

#### CPC

Caprice: `cap32_libretro`
CrocoDS: `crocods_libretro`
Enterprise 128: `ep128_libretro`

- [Caprice32 Libretro Library](https://docs.libretro.com/library/caprice32/)
- [Cap32 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/cap32_libretro.info)

- [CrocoDS Libretro Library](https://docs.libretro.com/library/crocods/)
- [CrocoDS Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/crocods_libretro.info)

- [Enterprise 128 Libretro Library](https://docs.libretro.com/library/ep128emu/)
- [Enterprise Libretro core info](https://github.com/libretro/ep128emu-core/blob/core/ep128emu_libretro.info)

Supported filetypes:
Crocods: `dsk|sna|kcr`
Caprice: `dsk|sna|zip|tap|cdt|voc|cpr|m3u`
Enterpirse 128: `img|dsk|tap|dtf|cas|cdt|tzx|bas|com|trn|128|.`

Example(s):

CPC:
Name: Debris
By: Pulpo Corrosivo
Type: 40k
Platform: amstradcpc
`./showet.py 92044`

### Apple(I/II/128K) Notes

Minivmac: `minivmac_libretro`

- [Minivmac Libretro Library](https://docs.libretro.com/library/minivmac/)

- [Minivmac Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/minivmac_libretro.info)

Supported filetypes:
Minivmac: `dsk|img|zip|hvf|cmd`

Example(s):

- [Apple-Vision By Bob Bishop](http://www.pouet.net/prod.php?which=54410)
- type: `zip,dsk`
- CLI: `./showet.py 54410`

### Archimedes Notes

Mame: `mame_libretro`
Mess2015: `mess_libretro`

- [Mame Libretro Library](https://docs.libretro.com/library/mame/)
- [Mame Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mame_libretro.info)

- [Mess Libretro Library](https://docs.libretro.com/library/mess/)
- [Mess Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mess2015_libretro.info)

Supported filetypes:
Mame/Mess: `zip|chd|7z|cmd`

Example(s):

ACORN:
Name: Relentless
By: Phlamethrower
Type: 4k
Platform: acorn
`./showet.py 90078`

### Atari Notes

### Bandai Notes

See: [platform_Bandai.md](platform_Bandai.md) for more information.

#### ST/STE/Falcon

Hatari: `hatari_libretro`

- [Hatari Libretro Library](https://docs.libretro.com/library/hatari/)

- [Hatari Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/hatari_libretro.info)

Supported filetypes:
Hatari: `st|msa|zip|stx|dim|ipf|m3u`

Example(s):

Name: DUNE_255
By: Dune
Type: 256b
Platform: atarifalcon030
`./showet.py 90474`

#### Jaguar

Virtualjaguar: `virtualjaguar_libretro`

- [Virtualjaguar Libretro Library](https://docs.libretro.com/library/virtual_jaguar/)
- [Virtualjaguar Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/virtualjaguar_libretro.info)

Supported filetypes:
Virtualjaguar: `j64|jag|rom|abs|cof|bin|prg`

Example(s):

Name: bootMandel
By: 42Bastian
Type: 128b
Platform: atarijaguar
`./showet.py 91595`

#### Lynx

Handy: `handy_libretro`

- [Handy Libretro Library](https://docs.libretro.com/library/handy/)

- [Handy Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/handy_libretro.info)

Supported filetypes:
handy: `lnx|o`

Example(s):

Name: Planet Techno
By: New Generation
Type: demo
Platform: atarilynx
`./showet.py 90548`

#### 2600

Stella: `stella_libretro`

- [Stella Libretro Library](https://docs.libretro.com/library/stella/)
- [Stella Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/stella_libretro.info)

Supported filetypes:
Stella: `a26|bin`

Example(s):

XLXE:
Name: mode9
By: PPS
Type: 32k,demo
Platform: atarixlxe
`./showet.py 92028`

#### 2500

Atari 800: `atari800_libretro`

- [Atari 800 Libretro Library](https://docs.libretro.com/library/atari800/)
- [Atari 800 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/atari800_libretro.info)

Supported filetypes:
atari800: `xfd|atr|cdm|cas|bin|a52|zip|atx|car|rom|com|xex`

Example(s):

[Back to top](README.md)

#### 7800

ProSystem: `prosystem_libretro`

- [ProSystem Libretro Library](https://docs.libretro.com/library/prosystem/)
- [ProSystem Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/prosystem_libretro.info)

Supported filetypes:

- `a78|bin`

Example(s):

[Back to top](README.md)

### Commodore Notes

See: [platform_Commodore.md](platform_Commodore.md) For more information.

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

VIC20:

C16/116/plus4:

C64:
Name: Help/Poltergeist
Type: 512b
Platform: commodore64
`./showet.py 92355`

C128:
Name: C128 VDC Demo
By: Onslaught
Type: 8k
Platform: commodore128
`./showet.py 81542`

CBM:

PET:

### Java Notes

Squirreljme: `squirreljme_libretro`

- [Squirreljme Libretro Library](https://github.com/SquirrelJME/SquirrelJME)
- [Squirreljme Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/squirreljme_libretro.info)

Supported filetypes:
SquirrelJME: `jar|sqc|jam|jad|kjx`

Example(s):

[Back to top](README.md)

### Linux Notes

Linux: `sh`

- [sh/bash Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/placeholder_libretro.info)

Supported filetypes:
Linux: `exe|elf|sh`

Example(s):

[Back to top](README.md)

### Mattel Notes

Freeintv: `freeintv_libretro`

- [Freeintv Libretro Library](https://docs.libretro.com/library/freeintv/)
- [Freeintv Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/freeintv_libretro.info)

Supported filetypes:
Freeintv: `int|bin|rom`

Example(s):

[Back to top](README.md)

### Microsoft Notes

#### XBOX

Directxbox: `directxbox_libretro`

- [Directxbox Libretro Library](https://docs.libretro.com/library/directxbox/)
- [Directxbox Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/directxbox_libretro.info)

Supported filetypes:
Directxbox: `iso`

Example(s):

[Back to top](README.md)

#### MSX

Bluemsx: `bluemsx_libretro`
Fmsx: `fmsx_libretro`

- [Bluemsx Libretro Library](https://docs.libretro.com/library/bluemsx/)
- [Bluemsx Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/bluemsx_libretro.info)

- [Fmsx Libretro Library](https://docs.libretro.com/library/fmsx/)
- [Fmsx Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/fmsx_libretro.info)

Supported filetypes:
Bluemsx: `rom|ri|mx1|mx2|col|dsk|cas|sg|sc|m3u`
Fmsx: `rom|mx1|mx2|dsk|cas|m3u`

Example(s):

[Back to top](README.md)

#### Windows

Wine: `wine`

- [Wine Manual](https://linux.die.net/man/1/wine)

Supported filetypes:
Wine: `bat|com|exe`

Example(s):

[Back to top](README.md)

#### MsDOS

Dosbox: `dosbox_libretro`
Wine: `wine`

- [Dosbox Libretro Library](https://docs.libretro.com/library/dosbox/)
- [Dosbox Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/dosbox_libretro.info)

Supported filetypes:
Dosbox/Wine: `exe|com|bat|conf`

Example(s):

[Back to top](README.md)

### Music Notes

GameMusicEmu: `gme_libretro`

- [GameMusicEmu Libretro Library](https://docs.libretro.com/library/game_music_emu/)
- [GameMusicEmu Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/gme_libretro.info)

Supported filetypes:
GameMusicEmu: `ay|gbs|gym|hes|kss|nsf|nsfe|sap|spc|vgm|vgz|zip`

Example(s):

[Back to top](README.md)

### Nec Notes

#### PCE

Mednafen pce: `

- [Mednafen pce Libretro Library](https://docs.libretro.com/library/mednafen_pce/)
- [Mednafen pce Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_pce_libretro.info)

Supported filetypes:
Mednafen pce: `pce|sgx|cue|ccd|chd|toc|m3u`

Example(s):

[Back to top](README.md)

#### PCFX

Mednafen pcfx: `

- [Mednafen pcfx Libretro Library](https://docs.libretro.com/library/mednafen_pcfx/)
- [Mednafen pcfx Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_pcfx_libretro.info)

Supported filetypes:
Mednafen pcfx: `cue|ccd|toc|chd`

Example(s):

[Back to top](README.md)

#### PC98

NekoProject2: `

- [NekoProject2 Libretro Library](https://docs.libretro.com/library/neko_project_ii/)
- [NekoProject2kai Libretro Library](https://docs.libretro.com/library/neko_project_ii_kai/)
- [NekoProject2 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/nekop2_libretro.info)
- [NekoProject2kai Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/np2kai_libretro.info)

Supported filetypes:
nekop2/np2kai: `d98|zip|98d|fdi|fdd|2hd|tfd|d88|88d|hdm|xdf|dup|cmd|hdi|thd|nhd|hdd`

Example(s):

[Back to top](README.md)

#### PC8000/PC8800

Quasi88: `

- [Quasi88 Libretro Library](https://docs.libretro.com/library/quasi88/)
- [Quasi88 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/quasi88_libretro.info)

Supported filetypes:
Quasi88: `d88|u88|m3u`

Example(s):

[Back to top](README.md)

#### SuperGrafx

Mednafen Supergrafx: `mednafen_supergrafx_libretro`

- [Mednafen Supergrafx Libretro Library](https://docs.libretro.com/library/beetle_sgx/)
- [Mednafen Supergrafx Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_supergrafx_libretro.info)

Supported filetypes:
Mednafen supergrafx: `pce|sgx|cue|ccd|chd`

Example(s):

[Back to top](README.md)

### NeoGeo Notes

Race: `race_libretro`
Mednafen Ngp: `mednafen_ngp_libretro`

- [Mednafen Ngp Libretro Library](https://docs.libretro.com/library/beetle_neopop/)
- [Race Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/race_libretro.info)
- [Mednafen Ngp Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_ngp_libretro.info)

Supported filetypes:
Race/Mednafen: `ngp|ngc|ngpc|npc`

Example(s):

[Back to top](README.md)

### Nintendo Notes

#### NES

Quicknes: `quicknes_libretro`
Bnes: `bnes_libretro`
Emux NES: `emux_nes_libretro`
Mesen: `mesen_libretro`

- [Quicknes Libretro Library](https://docs.libretro.com/library/quicknes/)
- [Bnes Libretro Library](https://docs.libretro.com/library/bnes/)
- [Emux NES Libretro Library](https://docs.libretro.com/library/emux_nes/)
- [Quicknes Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/quicknes_libretro.info)
- [Bnes Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/bnes_libretro.info)
- [Emux Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/emux_nes_libretro.info)
- [Nestopia Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/nestopia_libretro.info)
- [Fixnes Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/fixnes_libretro.info)
- [FCEUMM Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/fceumm_libretro.info)
- [FCEUMM Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mesen_libretro.info)

Supported filetypes:
Quicknes/Bnes: `nes`
Emux: `nes|bin|rom`
Mesen/Nestopia/Fixnes/Fceumm: `nes|fds|unf|unif`

Example(s):

[Back to top](README.md)

#### SNES

Bsnes: `bsnes_libretro`
Snes9x: `snes9x_libretro`
Mednafen: `mednafen_snes_libretro`
SuperFaust: `mednafen_supafaust_libretro`

- [Snes9x Libretro Library](https://docs.libretro.com/library/snes9x/)
- [Bsnes Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/bsnes_libretro.info)
- [Mednafen snes Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_snes_libretro.info)
- [Superfaust Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_snes_libretro.info)
- [Snes9x Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/snes9x_libretro.info)

Supported filetypes:
Bsnes: `sfc|smc|gb|gbc|bs`
Mednafen: `smc|fig|bs|st|sfc`
Superfaust: `smc|fig|sfc|gd3|gd7|dx2|bsx|swc`
Snes9x: `smc|sfc|swc|fig|bs|st`

Example(s):

[Back to top](README.md)

#### N64

Mupen64plus: `mupen64plus_next_libretro`
Parallel: `parallel_n64_libretro`

- [Mupen64plus Libretro Library](https://docs.libretro.com/library/mupen64plus/)
- [Mupen64plus Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mupen64plus_next_libretro.info)
- [Parallel Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/parallel_n64_libretro.info)

Supported filetypes:
Mupen64plus: `n64|v64|z64|bin|u1`
Parallel: `n64|v64|z64|bin|u1|ndd`

Example(s):

[Back to top](README.md)

#### GB/GBC

Emux: `emux_gb_libretro`
FixGB: `fixgb_libretro`
Gambatte: `gambatte_libretro`
TgbDual: `tgbdual_libretro`
SameBoy: `sameboy_libretro`
Gearboy: `gearboy_libretro`

- [Gambatte Libretro Library](https://docs.libretro.com/library/gambatte/)
- [Emux GB Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/emux_gb_libretro.info)
- [FixGB Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/fixgb_libretro.info)
- [Gambatte Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/gambatte_libretro.info)
- [Sameboy Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/gambatte_libretro.info)
- [Gearboy Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/gearboy_libretro.info)

Supported filetypes:
Emux: `gb|bin|rom`
FixGB: `gb|gbc|gbs`
Gambatte: `gb|gbc|dmg`
TgbDual: `gb|gbc|sgb`
Sameboy: `gb|gbc`
Gearboy: `gb|dmg|gbc|cgb|sgb`

Example(s):

[Back to top](README.md)

#### GBA

Mednafen: `mednafen_gba_libretro`
TempGBA: `tempgba_libretro`
Meteor: `meteor_libretro`
VisualBoyAdvanced: `vba_next_libretro`
VBAM: `vbam_libretro`

- [VisualBoyAdvanced Libretro Library](https://docs.libretro.com/library/vba_next/)
- [Mednafen GBA Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_gba_libretro.info)
- [TempGBA Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/tempgba_libretro.info)
- [Meteor Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/meteor_libretro.info)
- [VisualBoyAdvanced Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vba_next_libretro.info)
- [VBAM Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vbam_libretro.info)

Supported filetypes:
Mednafen GBA: `gba|agb|bin`
TempGBA:`gba|bin|agb|gbz`
Meteor/VisualBoyAdvanced: `gba`
VBAM: `dmg|gb|gbc|cgb|sgb|gba`

Example(s):

[Back to top](README.md)

#### GameCube/WII

Dolphin: `dolphin_libretro`

- [Dolphin Libretro Library](https://docs.libretro.com/library/dolphin/)
- [Dolphin Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/dolphin_libretro.info)
- [Dolphin Launcher Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/dolphin_launcher_libretro.info)

Supported filetypes:
Dolphin: `gcm|iso|wbfs|ciso|gcz|elf|dol|dff|tgc|wad|rvz|m3u`
Dolphin Launcher: `lf|dol|gcm|iso|wbfs|ciso|gcz|wad`

Example(s):

[Back to top](README.md)

#### POKEMINI

Pokemini: `pokemini_libretro`

- [Pokemini Libretro Library](https://docs.libretro.com/library/pokemini/)
- [Pokemini Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/pokemini_libretro.info)

Supported filetypes:

- `min`

Example(s):

[Back to top](README.md)

#### NDS

MelonDS: `melonds_libretro`

- [MelonDS Libretro Library](https://docs.libretro.com/library/melonds/)
- [MelonDS Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/melonds_libretro.info)

Supported filetypes:

- `nds|dsi`

Example(s):

[Back to top](README.md)

#### 3DS

Citra: `citra_libretro`

- [MelonDS Libretro Library](https://docs.libretro.com/library/citra/)
- [MelonDS Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/citra_libretro.info)

Supported filetypes:
Citra: `3ds|3dsx|elf|axf|cci|cxi|app`

Example(s):

[Back to top](README.md)

#### VirtualBoy

Mednafen: `mednafen_vb_libretro`

- [MelonDS Libretro Library](https://docs.libretro.com/library/beetle_vb/)
- [MelonDS Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_vb_libretro.info)

Supported filetypes:
MelonDS: `vb|vboy|bin`

Example(s):

[Back to top](README.md)

### PalmOS Notes

Mu: `mu_libretro`

- [Mu Libretro Library](https://docs.libretro.com/library/mu/)
- [Mu Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mu_libretro.info)

Supported filetypes:
Mu: `prc|pqa|img|pdb`

Example(s):

[Back to top](README.md)

### Pico8 Notes

Retro8: `retro8_libretro`

- [Retro8 Libretro Library](https://docs.libretro.com/library/retro8/)
- [Retro8 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/retro8_libretro.info)

Supported filetypes:
Retro8: `p8|png`

Example(s):

[Back to top](README.md)

### Sega Notes

#### MS/MD/32x/Genesis

- [Blastem Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/blastem_libretro.info)
- [Emux SMS Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/emux_sms_libretro.info)
- [Picodrive Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/picodrive_libretro.info)
- [Smsplus Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/smsplus_libretro.info)
- [Genesis plus GX Libretro Library](https://docs.libretro.com/library/genesis_plus_gx/)
- [Genesis plus GX Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/genesis_plus_gx_libretro.info)

Supported filetypes:
Blastem: `md|bin|smd|gen|68k|sgd`
Emux SMS: `sms|bms|bin|rom`
Picodrive: `bin|gen|gg|smd|pco|md|32x|chd|cue|iso|sms|68k|sgd|m3u`
Smsplus: `sms|bin|rom|col|gg|sg`
Genesis plus: `mdx|md|smd|gen|bin|cue|iso|sms|bms|gg|sg|68k|sgd|chd|m3u`

Example(s):

[Back to top](README.md)

#### Saturn

- [Mednafen saturn Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_saturn_libretro.info)
- [Kronos Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/kronos_libretro.info)
- [Yabause Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/yabause_libretro.info)
- [YabaSanshiro Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/yabasanshiro_libretro.info)

Mednafen: `ccd|chd|cue|toc|m3u`
Kronos: `ccd|chd|cue|iso|mds|zip|m3u`
Yabause/YabaSanshiro: `bin|ccd|chd|cue|iso|mds|zip|m3u`

#### GameGear

Gearsystem: `gearsystem_libretro`

- [Gearsystem Libretro Library](https://docs.libretro.com/library/gearsystem/)
- [Gearsystem Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/gearsystem_libretro.info)
- [Smsplus Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/smsplus_libretro.info)
- [Genesis plus GX Libretro Library](https://docs.libretro.com/library/genesis_plus_gx/)
- [Genesis plus GX Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/genesis_plus_gx_libretro.info)
- [FinalBurn Neo Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/fbneo_libretro.info)

Supported filetypes:
Gearsystem: `sms|gg|sg|bin|rom`
Smsplus: `sms|bin|rom|col|gg|sg`
Genesis plus: `mdx|md|smd|gen|bin|cue|iso|sms|bms|gg|sg|68k|sgd|chd|m3u`
FinalBurn Neo: `zip|7z|cue|ccd`

Example(s):

[Back to top](README.md)

#### Dreamcast

Flycast: `flycast_libretro`

- [Flycast Libretro Library](https://docs.libretro.com/library/flycast/)
- [Flycast Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/flycast_libretro.info)
- [Redream Libretro Library](https://docs.libretro.com/library/redream/)
- [Redream Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/redream_libretro.info)

Supported filetypes:
Flycast: `sms|gg|sg|bin|rom`

Example(s):

[Back to top](README.md)

### Sinclair Notes

#### ZXspectrum/ZX81

Fuse: `fuse_libretro`

- [Fuse Libretro Library](https://docs.libretro.com/library/fuse/)
- [Fuse Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/fuse_libretro.info)

Supported filetypes:
Fuse: `tzx|tap|z80|rzx|scl|trd|dsk|zip`

Example(s):

[Back to top](README.md)

#### ZX81

81: `81_libretro`

- [81 Libretro Library](https://docs.libretro.com/library/eightyone/)
- [81 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/81_libretro.info)

81: `p|tzx|t81`

Example(s):

[Back to top](README.md)

#### Enterprise 64/128

Ep128emu: `ep128emu_libretro`

- [ep128emu Libretro Library](https://docs.libretro.com/library/ep128emu/)
- [ep128emu Libretro core info](https://github.com/libretro/ep128emu-core/blob/core/ep128emu_libretro.info)

Supported filetypes:
Ep128emu: `img|dsk|tap|dtf|com|trn|128|bas|cas|cdt|tzx|.`

Example(s):

[Back to top](README.md)

### Sony Notes

#### PS1

Pcsx1: `pcsx1_libretro`
Pcsxr: `pcsx_rearmed_libretro`
Mednafen: `mednafen_psx_libretro`
Rustation: `rustation_libretro`
Duckstation: `ducktation_libretro`

- [Mednafen Libretro Library](https://docs.libretro.com/library/beetle_psx/)
- [PCSX ReARMed Libretro Library](https://docs.libretro.com/library/pcsx_rearmed/)

- [Mednafen Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mednafen_psx_libretro.info)
- [Rustation Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/rustation_libretro.info)
- [Duckstation Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/duckstation_libretro.info)
- [Swanstation Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/swanstation_libretro.info)

Supported filetypes:
Mednafen: `cue|toc|m3u|ccd|exe|pbp|chd`
Rustation: `cue|toc|m3u|ccd|exe`
Duckstation: `exe|psexe|cue|bin|img|iso|chd|pbp|ecm|mds|psf|m3u`
Swanstation: `exe|psexe|cue|bin|img|iso|chd|pbp|ecm|mds|psf|m3u`

Example(s):

[Back to top](README.md)

#### PS2

Pcsx2: `pcsx2_libretro`

- [Pcsx2 Libretro Library](https://docs.libretro.com/library/pcsx2/)
- [Play! Libretro Library](https://docs.libretro.com/library/play/)

- [Pcsx2 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/pcsx2_libretro.info)
- [Play! Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/play_libretro.info)

Supported filetypes:

Pcsx2: `elf|iso|ciso|chd|cso|bin|mdf|nrg|dump|gz|img|m3u`
Play: `chd|cso|cue|elf|iso|isz`

Example(s):

[Back to top](README.md)

#### PSP

Ppsspp: `ppsspp_libretro`

- [Ppsspp Libretro Library](https://docs.libretro.com/library/ppsspp/)

- [Ppsspp Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/ppsspp_libretro.info)

Supported filetypes:
Ppsspp: `elf|iso|cso|prx|pbp`

Example(s):

[Back to top](README.md)

### Tic80 Notes

Tic80: `tic80_libretro`

- [Tic80 Libretro Library](https://docs.libretro.com/library/tic80/)
- [Tic80 Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/tic80_libretro.info)

Supported filetypes:
tic80: `tic`

Example(s):

[Back to top](README.md)

### Vectrex Notes

Vecx: `vecx_libretro`

- [Vecx Libretro Library](https://docs.libretro.com/library/vecx/)
- [Vecx Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/vecx_libretro.info)

Supported filetypes:
Vecx: `bin|vec`

Example(s):

[Back to top](README.md)

### Video Notes

MPV: `mpv_libretro`
FFmpeg: `ffmpeg_libretro`

- [FFmpeg Libretro Library](https://docs.libretro.com/library/ffmpeg/)
- [MPV Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/mpv_libretro.info)
- [FFmpeg Libretro core info](https://github.com/libretro/libretro-core-info/blob/master/ffmpeg_libretro.info)

Supported filetypes:

MPV/FFmpeg: `mkv|avi|f4v|f4f|3gp|ogm|flv|mp4|mp3|flac|ogg|m4a|webm|3g2|mov|wmv|mpg|mpeg|vob|asf|divx|m2p|m2ts|ps|ts|mxf|wma|wav`
Example(s):

[Back to top](README.md)

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
