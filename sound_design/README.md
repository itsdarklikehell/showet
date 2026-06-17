# Sound Design

Authentic period-accurate audio for the ultimate retro demo experience.

## Themes Available

Press `S` in the viewer or use `--sound-theme` CLI option:

| Theme | Platform | Description |
|-------|----------|-------------|
| `c64` | Commodore 64 | Warm power supply hum + SID chip interference |
| `amiga` | Amiga | Workbench hum + floppy drive idle ambience |
| `dos` | MS-DOS | PC internal hum + hard drive spin |
| `silent` | Any | Exhibition mode (no audio) |

## Sound Effects

### Floppy Disk Sounds
```javascript
ShowetAudio.playFloppySeek()  // Simulate disk seeking
ShowetAudio.playDiskInsert()  // Disk insertion sound
```

### Keyboard Feedback
```javascript
ShowetAudio.playKeyboardClick()  // Mechanical keyboard click
ShowetAudio.playPowerOn()      // System startup sound
```

## Integration

Sound themes automatically activate when:
- Launching a demo in the Showcase
- Starting Museum Mode
- Using Party Mode (syncs across clients)

---
*Made with Web Audio API synthesis - no external assets needed for authentic retro feel.*