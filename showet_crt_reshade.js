/**
 * Showet x ReShade CRT Presets
 * -----------------------------
 * Ports ReShade CRT shaders (github.com/itsdarklikehell/reshade-shaders) into
 * Showet's WebGL CRT engine (showet-crt-shader.js -> window.ShowetCRT).
 *
 * Authored during the joint GLaDOS<->Wheatley showet deep-dive (GLaDOS built
 * the MCP server; the CRT port was finalized by GLaDOS from the agreed design
 * after Wheatley's live A2A shader task timed out on the OpenClaw side — the
 * A2A link itself is proven by Wheatley's successful 29-repo triage).
 *
 * NON-BREAKING: this file only ADDS behaviour. It does not modify
 * showet-crt-shader.js or showet-shader-editor.js. It augments the existing
 * window.ShowetCRT singleton with a swappable preset registry, a UI <select>,
 * and the methods documented in README.md: setPreset / listPresets /
 * activePreset / resetToLegacy.
 *
 * Slider -> ReShade uniform mapping (the 4 ShowetShaderEditor sliders):
 *   curvature          -> barrel / pincushion distortion
 *   scanlineIntensity  -> scanline darkening
 *   phosphorBloom      -> phosphor glow / bloom
 *   chromaticAberration-> R/G/B channel split
 */

// ---------------------------------------------------------------------------
// GLSL ES 1.0 fragment shaders (WebGL1/2 compatible: gl_FragColor, texture2D,
// varying, precision mediump float — no ReShade macros, no in/out).
// Each is derived from the named reshade-shaders/Shaders/*.fx file.
// ---------------------------------------------------------------------------

// crt-royale.fx (lite): geometry + beam bloom + phosphor triad mask.
const FS_ROYALE = `
precision mediump float;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_resolution;
uniform float u_curvature;
uniform float u_scanlineIntensity;
uniform float u_phosphorBloom;
uniform float u_chromaticAberration;
varying vec2 v_texCoord;
vec2 curve(vec2 uv){
  uv = uv - 0.5;
  float k = u_curvature * 0.2;
  uv *= 1.0 + (uv.yx * uv.yx) * k;
  return uv + 0.5;
}
void main(){
  vec2 uv = curve(v_texCoord);
  vec2 res = u_resolution;
  float ca = u_chromaticAberration / max(res.x, 1.0);
  vec3 col;
  col.r = texture2D(u_texture, curve(v_texCoord + vec2(ca, 0.0))).r;
  col.g = texture2D(u_texture, uv).g;
  col.b = texture2D(u_texture, curve(v_texCoord - vec2(ca, 0.0))).b;
  float scan = sin(uv.y * res.y * 3.14159) * 0.5 + 0.5;
  scan = pow(scan, mix(0.5, 2.5, u_scanlineIntensity));
  col *= mix(1.0, scan, u_scanlineIntensity);
  float tri = mod(floor(uv.x * res.x), 3.0);
  vec3 mask = tri < 1.0 ? vec3(1.0, 0.6, 0.6)
            : tri < 2.0 ? vec3(0.6, 1.0, 0.6)
                        : vec3(0.6, 0.6, 1.0);
  col *= mix(vec3(1.0), mask, 0.35 * u_phosphorBloom);
  col = mix(col, col + col * u_phosphorBloom, 0.5);
  gl_FragColor = vec4(col, 1.0);
}`;

// CRTEasymode.fx: gamma, scanline beam weighting, aperture-grille RGB mask.
const FS_EASYMODE = `
precision mediump float;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_resolution;
uniform float u_curvature;
uniform float u_scanlineIntensity;
uniform float u_phosphorBloom;
uniform float u_chromaticAberration;
varying vec2 v_texCoord;
#define PI 3.141592653589
vec2 curve(vec2 uv){
  uv = uv - 0.5;
  uv *= 1.0 + (uv.yx * uv.yx) * u_curvature * 0.15;
  return uv + 0.5;
}
float curve_dist(float x, float sharp){
  float x_step = step(0.5, x);
  float c = 0.5 - sqrt(0.25 - (x - x_step) * (x - x_step)) * sign(0.5 - x);
  return mix(x, c, sharp);
}
void main(){
  vec2 uv = curve(v_texCoord);
  vec2 res = u_resolution;
  float ca = u_chromaticAberration / max(res.x, 1.0);
  vec3 col;
  col.r = texture2D(u_texture, curve(v_texCoord + vec2(ca, 0.0))).r;
  col.g = texture2D(u_texture, uv).g;
  col.b = texture2D(u_texture, curve(v_texCoord - vec2(ca, 0.0))).b;
  float gi = mix(1.0, 2.0, u_phosphorBloom);
  col = pow(col, vec3(gi));
  float bright = (max(col.r, max(col.g, col.b)) + dot(vec3(0.2126,0.7152,0.0722), col)) * 0.5;
  float beam = mix(1.5, 3.5, u_scanlineIntensity);
  float scan = 1.0 - pow(cos(uv.y * 2.0 * PI * res.y) * 0.5 + 0.5, beam) * u_scanlineIntensity;
  col *= vec3(scan);
  float mask_strength = u_scanlineIntensity * 0.4;
  vec2 grid = floor(uv * res / 3.0);
  int dot_no = int(mod(grid.x + mod(grid.y, 2.0) * 3.0, 3.0));
  vec3 mask_w = dot_no == 0 ? vec3(1.0, mask_strength, mask_strength)
              : dot_no == 1 ? vec3(mask_strength, 1.0, mask_strength)
                            : vec3(mask_strength, mask_strength, 1.0);
  col *= mask_w;
  col = mix(col, vec3(1.0) - (vec3(1.0) - col) * (vec3(1.0) - col * u_phosphorBloom), 0.35);
  col *= 1.2;
  col = pow(col, vec3(1.0 / 1.8));
  float vig = 1.0 - pow(distance(uv, vec2(0.5)), 2.0);
  col *= vig;
  gl_FragColor = vec4(col, 1.0);
}`;

// CRTPi.fx (lite): quadratic scanline weight, Raspberry-Pi style soft mask.
const FS_CRTPi = `
precision mediump float;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_resolution;
uniform float u_curvature;
uniform float u_scanlineIntensity;
uniform float u_phosphorBloom;
uniform float u_chromaticAberration;
varying vec2 v_texCoord;
vec2 curve(vec2 uv){
  uv = uv - 0.5;
  uv *= 1.0 + (uv.yx * uv.yx) * u_curvature * 0.12;
  return uv + 0.5;
}
void main(){
  vec2 uv = curve(v_texCoord);
  vec2 res = u_resolution;
  float ca = u_chromaticAberration / max(res.x, 1.0);
  vec3 col;
  col.r = texture2D(u_texture, curve(v_texCoord + vec2(ca, 0.0))).r;
  col.g = texture2D(u_texture, uv).g;
  col.b = texture2D(u_texture, curve(v_texCoord - vec2(ca, 0.0))).b;
  // Quadratic scanline weight (CRTPi signature)
  float sl = uv.y * res.y;
  float scan = 1.0 - u_scanlineIntensity * (1.0 - 4.0 * (fract(sl) - 0.5) * (fract(sl) - 0.5));
  col *= clamp(scan, 0.0, 1.0);
  // Soft Pi-style phosphor mask
  float tri = mod(floor(uv.x * res.x), 3.0);
  vec3 mask = tri < 1.0 ? vec3(1.0, 0.7, 0.7)
            : tri < 2.0 ? vec3(0.7, 1.0, 0.7)
                        : vec3(0.7, 0.7, 1.0);
  col *= mix(vec3(1.0), mask, 0.25 * u_phosphorBloom);
  gl_FragColor = vec4(col, 1.0);
}`;

// CRT_Yee64.fx (lite): chunky nearest-neighbour pixel crush + light scanline.
const FS_YEE64 = `
precision mediump float;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_resolution;
uniform float u_curvature;
uniform float u_scanlineIntensity;
uniform float u_phosphorBloom;
uniform float u_chromaticAberration;
varying vec2 v_texCoord;
vec2 curve(vec2 uv){
  uv = uv - 0.5;
  uv *= 1.0 + (uv.yx * uv.yx) * u_curvature * 0.1;
  return uv + 0.5;
}
void main(){
  vec2 uv = curve(v_texCoord);
  vec2 res = u_resolution;
  // Chunky pixel crush: snap to a coarse grid (Yee64 "64" look)
  float px = mix(1.0, 64.0 / max(res.y, 1.0), u_scanlineIntensity);
  vec2 crushed = (floor(uv * res * px) + 0.5) / (res * px);
  float ca = u_chromaticAberration / max(res.x, 1.0);
  vec3 col;
  col.r = texture2D(u_texture, crushed + vec2(ca, 0.0)).r;
  col.g = texture2D(u_texture, crushed).g;
  col.b = texture2D(u_texture, crushed - vec2(ca, 0.0)).b;
  float scan = sin(crushed.y * res.y * 3.14159) * 0.5 + 0.5;
  col *= mix(1.0, scan, u_scanlineIntensity * 0.6);
  col = mix(col, col + col * u_phosphorBloom, 0.4);
  gl_FragColor = vec4(col, 1.0);
}`;

// TVCRTPixels.fx (lite): R/G/B sub-pixel triads (aperture-grille style).
const FS_TVPIXELS = `
precision mediump float;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_resolution;
uniform float u_curvature;
uniform float u_scanlineIntensity;
uniform float u_phosphorBloom;
uniform float u_chromaticAberration;
varying vec2 v_texCoord;
vec2 curve(vec2 uv){
  uv = uv - 0.5;
  uv *= 1.0 + (uv.yx * uv.yx) * u_curvature * 0.15;
  return uv + 0.5;
}
void main(){
  vec2 uv = curve(v_texCoord);
  vec2 res = u_resolution;
  float ca = u_chromaticAberration / max(res.x, 1.0);
  vec3 col;
  col.r = texture2D(u_texture, curve(v_texCoord + vec2(ca, 0.0))).r;
  col.g = texture2D(u_texture, uv).g;
  col.b = texture2D(u_texture, curve(v_texCoord - vec2(ca, 0.0))).b;
  // R/G/B sub-pixel triads
  float sub = mod(floor(uv.x * res.x * 3.0), 3.0);
  vec3 mask = sub < 1.0 ? vec3(1.0, 0.3, 0.3)
            : sub < 2.0 ? vec3(0.3, 1.0, 0.3)
                        : vec3(0.3, 0.3, 1.0);
  col *= mix(vec3(1.0), mask, 0.5 * u_phosphorBloom);
  float scan = sin(uv.y * res.y * 3.14159) * 0.5 + 0.5;
  col *= mix(1.0, scan, u_scanlineIntensity * 0.7);
  gl_FragColor = vec4(col, 1.0);
}`;

// BasicCRT.fx (lite): lightweight tinted chromatic CRT.
const FS_BASICCRT = `
precision mediump float;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_resolution;
uniform float u_curvature;
uniform float u_scanlineIntensity;
uniform float u_phosphorBloom;
uniform float u_chromaticAberration;
varying vec2 v_texCoord;
vec2 curve(vec2 uv){
  uv = uv - 0.5;
  uv *= 1.0 + (uv.yx * uv.yx) * u_curvature * 0.1;
  return uv + 0.5;
}
void main(){
  vec2 uv = curve(v_texCoord);
  vec2 res = u_resolution;
  float ca = u_chromaticAberration / max(res.x, 1.0);
  vec3 col;
  col.r = texture2D(u_texture, curve(v_texCoord + vec2(ca, 0.0))).r;
  col.g = texture2D(u_texture, uv).g;
  col.b = texture2D(u_texture, curve(v_texCoord - vec2(ca, 0.0))).b;
  float scan = sin(uv.y * res.y * 3.14159) * 0.5 + 0.5;
  col *= mix(1.0, scan, u_scanlineIntensity);
  // Warm tube tint
  col *= vec3(1.05, 1.0, 0.95);
  col = mix(col, col + col * u_phosphorBloom, 0.4);
  gl_FragColor = vec4(col, 1.0);
}`;

// ---------------------------------------------------------------------------
// Preset registry + ShowetCRT augmentation
// ---------------------------------------------------------------------------
(function installReshadePresets(){
  const crt = window.ShowetCRT;
  if (!crt) {
    console.warn('[showet_crt_reshade] ShowetCRT not ready; retrying on DOMContentLoaded.');
    window.addEventListener('DOMContentLoaded', installReshadePresets);
    return;
  }

  // The built-in shader, captured so resetToLegacy() can restore it.
  const LEGACY_FS = `
    precision mediump float;
    uniform sampler2D u_texture; uniform float u_time; uniform vec2 u_resolution;
    uniform float u_curvature; uniform float u_scanlineIntensity;
    uniform float u_phosphorBloom; uniform float u_chromaticAberration;
    varying vec2 v_texCoord;
    vec2 curve(vec2 c){ c=c-0.5; c*=1.0+(c.yx*c.yx)*u_curvature*0.1; return c+0.5; }
    void main(){ vec2 uv=curve(v_texCoord);
      vec2 uvR=curve(v_texCoord+vec2(u_chromaticAberration,0.0)/u_resolution);
      vec2 uvB=curve(v_texCoord-vec2(u_chromaticAberration,0.0)/u_resolution);
      vec4 r=texture2D(u_texture,uvR); vec4 g=texture2D(u_texture,uv); vec4 b=texture2D(u_texture,uvB);
      vec3 col=vec3(r.r,g.g,b.b);
      float s=sin(uv.y*u_resolution.y*2.0*3.14159*0.5)*0.5+0.5;
      s=pow(s,1.0-u_scanlineIntensity); col*=s;
      vec3 bloom=col*u_phosphorBloom; col=mix(col, vec3(1.0)-(vec3(1.0)-col)*(vec3(1.0)-bloom),0.5);
      float v=1.0-pow(distance(uv,vec2(0.5)),2.0); col*=v;
      gl_FragColor=vec4(col,1.0);
    }`;

  crt.presets = {
    royale:   { label: "ReShade: CRT-Royale (lite)",  fs: FS_ROYALE },
    easymode: { label: "ReShade: CRT-Easymode",       fs: FS_EASYMODE },
    crtpi:    { label: "ReShade: CRTPi (lite)",        fs: FS_CRTPi },
    yee64:    { label: "ReShade: CRT-Yee64 (lite)",    fs: FS_YEE64 },
    tvpixels: { label: "ReShade: TVCRT Pixels",        fs: FS_TVPIXELS },
    basiccrt: { label: "ReShade: BasicCRT",           fs: FS_BASICCRT },
  };
  const LEGACY_KEY = "__legacy__";
  crt._activePreset = LEGACY_KEY;
  crt._lastOverrides = null;

  crt._compileProgram = function(fsSource){
    const gl = this.gl;
    if (!gl) return null;
    const vs = gl.createShader(gl.VERTEX_SHADER);
    gl.shaderSource(vs,
      `attribute vec2 a_position; attribute vec2 a_texCoord; varying vec2 v_texCoord;
       void main(){ gl_Position=vec4(a_position,0.0,1.0); v_texCoord=a_texCoord; }`);
    gl.compileShader(vs);
    const fs = gl.createShader(gl.FRAGMENT_SHADER);
    gl.shaderSource(fs, fsSource);
    gl.compileShader(fs);
    if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) {
      console.error('[showet_crt_reshade] FS compile failed:', gl.getShaderInfoLog(fs));
      return null;
    }
    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      console.error('[showet_crt_reshade] link failed:', gl.getProgramInfoLog(prog));
      return null;
    }
    return prog;
  };

  crt.recompileWith = function(fsSource){
    const prog = this._compileProgram(fsSource);
    if (!prog) return false;
    this.program = prog;
    this.uniforms.time = this.gl.getUniformLocation(prog, 'u_time');
    this.uniforms.resolution = this.gl.getUniformLocation(prog, 'u_resolution');
    this.uniforms.curvature = this.gl.getUniformLocation(prog, 'u_curvature');
    this.uniforms.scanlineIntensity = this.gl.getUniformLocation(prog, 'u_scanlineIntensity');
    this.uniforms.phosphorBloom = this.gl.getUniformLocation(prog, 'u_phosphorBloom');
    this.uniforms.chromaticAberration = this.gl.getUniformLocation(prog, 'u_chromaticAberration');
    if (typeof this.apply === 'function') this.apply();
    return true;
  };

  // setPreset(name, overrides?) — name omitted/unknown => legacy shader.
  crt.setPreset = function(name, overrides){
    crt._lastOverrides = overrides || null;
    if (!name || !crt.presets[name]) {
      crt._activePreset = LEGACY_KEY;
      crt.recompileWith(LEGACY_FS);
      if (crt._selectEl) crt._selectEl.value = LEGACY_KEY;
      return false;
    }
    crt._activePreset = name;
    const ok = crt.recompileWith(crt.presets[name].fs);
    if (ok && overrides) crt.apply(overrides);
    if (crt._selectEl) crt._selectEl.value = name;
    return ok;
  };

  crt.resetToLegacy = function(){ return crt.setPreset(null); };
  crt.activePreset = function(){ return crt._activePreset === LEGACY_KEY ? 'legacy' : crt._activePreset; };
  crt.listPresets = function(){
    return ['legacy'].concat(Object.keys(crt.presets))
      .map(k => ({ name: k, label: k === 'legacy' ? 'ReShade: Legacy' : crt.presets[k].label,
                   active: (k === 'legacy' ? crt._activePreset === LEGACY_KEY : crt._activePreset === k) }));
  };

  // Auto-inject a <select> beside #shader-select in showet-showcase.html.
  function injectSelect(){
    const anchor = document.getElementById('shader-select');
    if (!anchor || crt._selectEl) return;
    const sel = document.createElement('select');
    sel.id = 'showet-crt-preset-select';
    sel.style.cssText = 'margin-left:8px;';
    sel.innerHTML = crt.listPresets().map(p =>
      `<option value="${p.name}"${p.active ? ' selected' : ''}>${p.label}</option>`).join('');
    sel.addEventListener('change', () => crt.setPreset(sel.value));
    anchor.parentNode.insertBefore(sel, anchor.nextSibling);
    crt._selectEl = sel;
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectSelect);
  } else { injectSelect(); }

  console.log('[showet_crt_reshade] installed presets:',
    Object.keys(crt.presets).join(', '));
})();
