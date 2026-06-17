# Showet Bug Fix Log

## 2026-06-17

### Fixed: Museum Mode Demo Rotation
**Issue:** In `showet-museum-mode.js`, the `currentIndex` was incremented immediately after calling `launchDemo()`, causing demo rotation to skip entries.

**Fix:** Moved the index increment to a separate `nextDemo()` method that auto-advances after the progress bar completes.

### Fixed: Party Mode Duplicate Controls
**Issue:** In `showet-party-client.js`, calling `startPartySession()` would add duplicate Party Mode controls because `onHostAssigned()` was called redundantly.

**Fix:** Removed duplicate `onHostAssigned()` call and added check to prevent duplicate button addition.

### Fixed: Scaffold Platform Template
**Issue:** `showet-scaffold.py` generated Platform files that called `super().__init__()` without the required `platform_name` and `version` parameters.

**Fix:** Updated template to call `super().__init__("platform_key", version="1.0.0-scaffold")` matching the pattern in existing platform files like `Platform_Atari_2600.py`.

### Fixed: UI Button Overlap
**Issue:** Museum Mode button (`bottom: 100px`) and Timeline button (`bottom: 60px`) would overlap with each other and with the Shader Editor panel.

**Fix:** Moved Museum Mode button to `top: 20px` to avoid conflicts. Timeline button integration removed in favor of viewer controls.

## Known Limitations (for future work)

### Museum Mode
- Uses hardcoded demo list; should integrate with Pouet API for dynamic loading
- Preview clips system references non-existent video files; needs recording integration
- Demo launch integration with nostalgist needs actual demo mapping

### Party Mode
- Requires WebSocket server (`showet-party-mode.py`) to be running
- Demo launch by name uses fuzzy matching; could fail for similar demo names
- No actual nostalgist.js playback synchronization implemented yet

### Sound Theme Manager
- Uses synthetic oscillators; could benefit from actual recorded ambient samples
- No volume control per theme

## Testing Commands

```bash
# Test scaffold tool
python3 showet-scaffold.py --list
python3 showet-scaffold.py neogeo --dir .

# Test demo scoring
python3 showet-demo-scoring.py

# Verify JS syntax
node --check sound_design/showet-sound-theme-manager.js
node --check showet-timeline.js showet-museum-mode.js showet-party-client.js showet-shader-playground.js
```