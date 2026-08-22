#!/usr/bin/env node
// Static GLSL ES 1.0 lint for the ReShade CRT presets embedded in
// showet_crt_reshade.js. Cannot compile without a GPU/headless-gl (unavailable
// on this host), so this catches the structural WebGL1-incompatibilities that
// would fail at runtime. Final visual confirmation still needs a browser.
const fs = require('fs');
const src = fs.readFileSync('showet_crt_reshade.js', 'utf8');

// Extract every `const FS_XXX = ` template literal (backtick string).
const re = /const (FS_[A-Za-z0-9]+)\s*=\s*`([\s\S]*?)`;/g;
let m, count = 0, failures = 0;

function lint(name, glsl) {
  const issues = [];
  if (!/precision\s+(lowp|mediump|highp)\s+float/.test(glsl))
    issues.push('missing "precision ... float" qualifier');
  if (/\btexture\s*\(/.test(glsl))
    issues.push('uses texture() (GLSL 3.00); WebGL1 needs texture2D()');
  if (/^\s*(in|out)\s+/.test(glsl))
    issues.push('uses in/out qualifiers (GLSL 3.00); WebGL1 uses varying/attribute');
  if (!/gl_FragColor/.test(glsl))
    issues.push('no gl_FragColor write');
  if (!/varying\s+vec2\s+v_texCoord/.test(glsl))
    issues.push('no "varying vec2 v_texCoord"');
  // required uniforms (subset used by all presets)
  if (!/uniform\s+float\s+u_curvature/.test(glsl)) issues.push('missing u_curvature uniform');
  if (!/uniform\s+float\s+u_scanlineIntensity/.test(glsl)) issues.push('missing u_scanlineIntensity uniform');
  if (!/uniform\s+float\s+u_phosphorBloom/.test(glsl)) issues.push('missing u_phosphorBloom uniform');
  if (!/uniform\s+float\s+u_chromaticAberration/.test(glsl)) issues.push('missing u_chromaticAberration uniform');
  // brace balance
  const open = (glsl.match(/{/g) || []).length;
  const close = (glsl.match(/}/g) || []).length;
  if (open !== close) issues.push(`unbalanced braces (${open} vs ${close})`);
  // paren balance
  const po = (glsl.match(/\(/g) || []).length;
  const pc = (glsl.match(/\)/g) || []).length;
  if (po !== pc) issues.push(`unbalanced parens (${po} vs ${pc})`);
  return issues;
}

while ((m = re.exec(src))) {
  count++;
  const issues = lint(m[1], m[2]);
  if (issues.length) {
    failures++;
    console.log(`✗ ${m[1]}: ${issues.length} issue(s)`);
    issues.forEach(i => console.log(`    - ${i}`));
  } else {
    console.log(`✓ ${m[1]}: structurally WebGL1-OK (precision, varyings, 4 uniforms, balanced)`);
  }
}
console.log(`\n${count} fragment shaders checked, ${failures} with issues.`);
process.exit(failures ? 1 : 0);
