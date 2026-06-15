# Platform Compatibility Matrix

This document lists all supported platforms, their emulators, libretro cores, and file extensions.

## By System Family

### Commodore

| Platform | Emulator | Core | Extensions |
|----------|----------|------|------------|
| commodore64 | retroarch | vice_x64sc_libretro | zip, d64, d71, d81, t64, tap, prg, p00, g64 |
| commodore128 | retroarch | vice_x128_libretro | d64, d71, d81, t64, tap, prg, p00 |
| commodoreamiga | retroarch | puae_libretro, fsuae_libretro, uae4arm_libretro | adf, dms, ipf, adz, lha, zip |
| commodorecbmii | retroarch | vice_xcbm2_libretro | zip |
| commodorepet | retroarch | vice_xpet_libretro | zip |
| commodoreplus4 | retroarch | vice_xplus4_libretro | zip |
| commodorevic20 | retroarch | vice_xvic_libretro | zip |

### Atari

| Platform | Emulator | Core | Extensions |
|----------|----------|------|------------|
| atari2600 | retroarch | stella2014_libretro | zip, a26, bin |
| atari5200 | retroarch | atari800_libretro | zip, xfd, atr, cdm, cas, bin, a52, atx, car, rom, com, xex |
| atari7800 | retroarch | prosystem_libretro | zip, a78, bin |
| atarijaguar | retroarch | virtualjaguar_libretro | zip, j64, jag, rom, abs, cof, bin, prg |
| atarilynx | retroarch | handy_libretro | lnx, o |
| atarist | retroarch | hatari_libretro | st, msa, stx, dim, ipf, m3u |
| atarifalcon030 | retroarch | hatari_libretro | st, msa, zip, stx, dim, ipf, m3u, xex |
| atarixlxe | retroarch | atari800_libretro | st, msa, zip, stx, dim, ipf, m3u, xex |

### Nintendo

| Platform | Emulator | Core | Extensions |
|----------|----------|------|------------|
| nintendofami (NES) | retroarch | quicknes_libretro | zip, nes, fds, unf, unif, qd, nsf, bin, rom |
| nintendodisk (FDS) | retroarch | quicknes_libretro | zip, nes, fds, unf, unif, qd, nsf |
| superfamicom (SNES) | retroarch | snes9x_libretro | zip, sfc, smc, fig, swc, bs |
| nintendo64 | retroarch | mupen64plus_libretro | n64, v64, z64, bin, u1, ndd |
| gameboy | retroarch | gambatte_libretro | zip, gb, dmg, bin, u1, ndd |
| gameboycolor | retroarch | gambatte_libretro | zip, gbc, dmg, bin, u1, ndd |
| gameboyadvance | retroarch | meteor_libretro | zip, gb, gbc, gba, dmg, agb, bin, cgb, sgb |
| gamecube | retroarch | dolphin_libretro | gcm, iso, wbfs, ciso, gcz, elf, dol, dff, tgc, wad, rvz, m3u |
| wii | retroarch | dolphin_libretro | gcm, iso, wbfs, ciso, gcz, elf, dol, dff, tgc, wad, rvz, m3u |
| nintendo3ds | retroarch | citra_libretro | 3ds, 3dsx, elf, axf, cci, cxi, app |
| pokemini | retroarch | pokemini_libretro | zip, min |

### Sony PlayStation

| Platform | Emulator | Core | Extensions |
|----------|----------|------|------------|
| playstation | retroarch | pcsx_rearmed_libretro | zip, exe, psx, psexe, cue, toc, bin, img, iso, chd, pbp, ccd, ecm, cbn, mdf, mds, psf, m3u |
| ps2 | retroarch | pcsx2_libretro | zip, exe, psexe, cue, toc, bin, img, iso, chd, pbp, ccd, ecm, cbn, mdf, mds, psf, m3u |
| psp | retroarch | ppsspp_libretro | elf, iso, cso, prx, pbp |

### Sega

| Platform | Emulator | Core | Extensions |
|----------|----------|------|------------|
| megadrive | retroarch | genesis_plus_gx_libretro | zip, mdx, md, smd, gen, bin, cue, iso, sms, bms, gg, sg, 68k, sgd, chd, m3u |
| mastersystem | retroarch | genesis_plus_gx_libretro | zip, mdx, md, smd, gen, bin, cue, iso, sms, bms, gg, sg, 68k, sgd, chd, m3u |
| saturn | retroarch | yabause_libretro | zip, sms, gg, sg, bin, rom |
| dreamcast | retroarch | flycast_libretro | chd, cdi, elf, bin, cue, gdi, lst, zip, dat, 7z, m3u |
| gamegear | retroarch | gearsystem_libretro | zip, sms, gg, sg, bin, rom |
| sg1000 | retroarch | gearsystem_libretro | rom, ri, mx1, mx2, col, dsk, cas, sg, sc, m3u |
| sega32x | retroarch | picodrive_libretro | zip, bin, gen, gg, smd, pco, md, 32x, chd, cue, iso, sms, 68k, sgd, m3u |
| stv | retroarch | yabause_libretro | zip, ccd, chd, cue, iso, mds, m3u |
| vmu | retroarch | vemulator_libretro | zip, vms, dci, bin |

### NEC / PC

| Platform | Emulator | Core | Extensions |
|----------|----------|------|------------|
| pcengine | retroarch | mednafen_supergrafx_libretro | zip, pce, sgx, cue, ccd, chd |
| pcfx | retroarch | mednafen_pcfx_libretro | cue, ccd, toc, chd |
| supergrafx | retroarch | mednafen_supergrafx_libretro | zip, pce, sgx, cue, ccd, chd |
| pc98 | retroarch | nekop2_libretro | d98, zip, 98d, fdi, fdd, 2hd, tfd, d88, 88d, hdm, xdf, dup, cmd, hdi, thd, nhd, hdd |
| pc8800 | retroarch | quasi88_libretro | d88, u88, m3u |
| pc8000 | retroarch | quasi88_libretro | zip, pce, sgx, cue, ccd, chd |

### Microsoft

| Platform | Emulator | Core | Extensions |
|----------|----------|------|------------|
| ms-dos | retroarch | dosbox_core_libretro | zip, dosz, exe, com, bat, iso, cue, ins, img, ima, vhd, jrc, tc, m3u, m3u8 |
| msx | retroarch | bluemsx_libretro | rom, ri, mx1, mx2, col, dsk, cas, sg, sc, m3u |
| windows | wine, proton | wine | exe |
| xbox | retroarch | directxbox_libretro | zip, iso |

### Other Platforms

| Platform | Emulator | Core | Extensions |
|----------|----------|------|------------|
| amstradcpc | retroarch | cap32_libretro | dsk, sna, kcr |
| applei | retroarch | minivmac_libretro | dsk, img, zip, hvf, cmd |
| appleii | retroarch | minivmac_libretro | dsk, img, zip, hvf, cmd |
| appleiigs | retroarch | minivmac_libretro | dsk, img, zip, hvf, cmd |
| arcade | retroarch | mame_libretro | zip, chd, 7z, cmd |
| acorn | retroarch | mame_libretro | zip, chd, 7z, cmd |
| wonderswan | retroarch | mednafen_wswan_libretro | zip, ws, wsc, pc2 |
| oric | euphoric, mame | oric_libretro | tap, crt |
| webassembly | browser | - | wasm, html |
| raspberry-pi | native | - | img, zip |
| android | android-emulator, anbox, qemu | - | apk, aab, xapk |
| vectrex | retroarch | vecx_libretro | zip, bin, vec |
| palm | retroarch | mu_libretro | prc, pqa, img, pdb, zip |
| panasonic3do | retroarch | 4do_libretro | iso, bin, chd, cue |
| phillipscdi | retroarch | samecdi_libretro | zip, chd, iso |
| neogeo | retroarch | fbneo_libretro | zip, ngp, ngc, ngpc, npc |
| neogeopocket | retroarch | mednafen_ngp_libretro | zip, ngp, ngc, ngpc, npc |
| neogeopocketcolor | retroarch | mednafen_ngp_libretro | zip, ngp, ngc, ngpc, npc |
| pdp11 | retroarch | bk_libretro | bin |
| channelf | retroarch | freechaf_libretro | zip, bin, chf |
| pico8 | retroarch | retro8_libretro | zip, p8, png |
| flash | retroarch, ruffle | ruffle_libretro | swf, spl |
| gamemusic | retroarch | gme_libretro | zip, ay, gbs, gym, hes, kss, nsf, nsfe, sap, spc, vgm, vgz |
| video | retroarch | ffmpeg_libretro, mpv_libretro | mkv, avi, f4v, f4f, 3gp, ogm, flv, mp4, mp3, flac, ogg, m4a, webm, 3g2, mov, wmv, mpg, mpeg, vob, asf, divx, m2p, m2ts, ps, ts, mxf, wma, wav |

## Legend

- **Emulator**: Software used to run the demo
  - `retroarch` - Libretro/RetroArch frontend
  - `wine` - Wine for Windows executables
  - `proton` - Valve Proton compatibility layer
  - `native` - Direct platform execution
  - `browser` - WebAssembly demos in browser
  - `euphoric` - Oric emulator
  - `mame` - Multiple Arcade Machine Emulator

- **Core**: Libretro core name for RetroArch
- **Extensions**: Supported file formats for each platform

## Adding New Platforms

To add a new platform:

1. Create `Platform_<Name>.py` with class extending `PlatformCommon`
2. Implement required methods: `supported_platforms()`, `setup()`, `run()`
3. Add the module to `showet.py`'s `create_platform_runners()` list
4. Update this documentation

## Notes

- Extension lists may not be exhaustive
- Some platforms have multiple core options (Amiga, Windows)
- Non-libretro emulators (wine, native, browser) don't use core configuration