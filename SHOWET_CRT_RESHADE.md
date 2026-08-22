# Showet × ReShade CRT Presets

Brings ReShade CRT shaders (from `reshade-shaders/Shaders/`, e.g.
`CRTEasymode.fx`, `crt-royale.fx`) into Showet's WebGL CRT playground.

Built during the joint **GLaDOS ↔ Wheatley** showet deep-dive. (Wheatley's
live A2A shader task timed out on the OpenClaw side; this file was finalized
by GLaDOS from the agreed design. The A2A link itself is proven by the
earlier 29-repo triage Wheatley completed successfully.)

## What it adds
`showet_crt_reshade.js` augments the existing `window.ShowetCRT` singleton
with a **preset registry** — no existing file is modified.

Presets:
| Preset | Source | Look |
|--------|--------|------|
| `showet_classic` | Showet's original shader | Default barrel + scanlines + bloom |
| `crt_easymode` | `reshade-shaders/Shaders/CRTEasymode.fx` | Gamma, scanline beam, aperture-grille mask |
| `crt_royale` | `crt-royale.fx` (lite) | Curvature, phosphor triad mask, bloom |

The 4 Showet sliders map to ReShade uniforms:
`curvature` → barrel distortion, `scanlineIntensity` → scanline strength,
`phosphorBloom` → glow, `chromaticAberration` → RGB split.

## How to use (in the browser)
Load `showet_crt_reshade.js` **after** `showet-crt-shader.js`. Then:
```js
window.ShowetCRT.selectPreset('crt_easymode');   // switch shader
window.ShowetCRT.listPresets();                   // [{name,label,active}, ...]
window.ShowetCRT.selectPreset('crt_royale');
```
The shader editor's sliders continue to drive `apply()` and feed the active
preset's uniforms live.

## Integration
Add to `showet-webui.py`'s served HTML (or the page that loads
`showet-crt-shader.js`), after it:
```html
<script src="showet_crt_reshade.js"></script>
```

## Verification status
- JS syntax: valid (`node --check`).
- GLSL: WebGL1/GLSL-ES-1.0 compatible (`gl_FragColor`, `texture2D`,
  `varying`, `precision mediump float` — no `in/out`/`texture()`).
- Visual compile/run needs a browser/WebGL context (no headless GLSL
  validator on this host). Load the page and call `selectPreset(...)` to
  confirm; check the devtools console for any shader-compile errors.
