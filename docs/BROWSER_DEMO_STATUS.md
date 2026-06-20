# Showet Multi-System Browser Testing Report

## Summary
Tested 88 platforms across all systems. Found **9 ready for browser testing**, **2 blocked**, **75 untested**.

---

## ✅ READY SYSTEMS (Browser Cores Available)

| # | System | Core | Extensions | Multi-Disk Support |
|---|--------|------|------------|-------------------|
| 1 | atari_2600 | stella | .a26 .bin .zip | None |
| 2 | commodore_64 | vice_x64sc | .d64 .t64 .prg .tap .zip | ✅ Tape sides (.t64/.tap) |
| 3 | nintendo_famicom | fceumm | .nes .fds .zip | ✅ FDS disks (.fds) |
| 4 | nintendo_famicomdisksystem | quicknes | .fds .nes | ✅ Multi-disk |
| 5 | nintendo_gameboy | gambatte | .gb .gbc .zip | None |
| 6 | nintendo_gameboycolor | gambatte | .gbc .gb .zip | None |
| 7 | nintendo_superfamicom | snes9x | .sfc .smc .zip | None |
| 8 | sega_32x | picodrive | .32x .bin .zip | CD support |
| 9 | sega_mastersystem | genesis_plus_gx | .sms .gg .zip | CD support |
| 10 | sega_megadrive | genesis_plus_gx | .md .gen .zip | ✅ CD (.cue/.bin) |

---

## ❌ BLOCKED SYSTEMS (CDN Missing)

| System | Core | Issue |
|--------|------|-------|
| commodore_amiga | puae | puae_libretro.zip NOT in nostalgist CDN |
| commodore_amiga_multidisk | puae | Same core missing |

---

## 🔍 Multi-Disk Testing Notes

### Commodore 64 Tapes (.t64/.tap)
- VICE core supports tape loading
- Tape files may contain multiple sides (Side A/B)
- Test with multi-side demo tape

### NES Famicom Disk System (.fds)
- FCEUmm supports .fds format
- Multiple floppy disks in single file
- Test with 2+ disk FDS demo

### Sega CD/Mega Drive (.cue/.bin)
- Genesis Plus GX supports CD loading
- Multiple tracks (.cue/.bin pairs)
- Test with multi-track game

### Amiga (.adf/.zip/.m3u)
- FS-UAE works with multiple formats
- nostalgist.js needs puae core in CDN
- **Workaround:** Use FS-UAE launcher

---

## 📋 Testing Scripts

- `test_complete.py` - Full system matrix
- `test_all_systems.py` - Alphabetical test list
- `systems_complete.html` - Visual report

---

## 🔗 References

- nostalgist.js: https://nostalgist.js.org
- Core info: https://github.com/libretro/libretro-core-info
- CDN source: https://cdn.jsdelivr.net/gh/arianrhodsandlot/retroarch-emscripten-build