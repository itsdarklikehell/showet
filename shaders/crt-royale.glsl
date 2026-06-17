// CRT Royale Shader - Advanced curvature with bloom and chromatic aberration
precision mediump float;
uniform sampler2D u_texture;
uniform vec2 u_resolution;
uniform float u_time;
varying vec2 v_texCoord;

vec2 curve(vec2 coord) {
    // Barrel distortion
    coord = coord - 0.5;
    coord *= 1.0 + (coord.yx * coord.yx) * 0.2;
    return coord + 0.5;
}

void main() {
    vec2 uv = curve(v_texCoord);
    vec2 uvR = curve(v_texCoord + vec2(2.0, 0.0) / u_resolution);
    vec2 uvB = curve(v_texCoord - vec2(2.0, 0.0) / u_resolution);
    
    vec4 colorR = texture2D(u_texture, uvR);
    vec4 colorG = texture2D(u_texture, uv);
    vec4 colorB = texture2D(u_texture, uvB);
    
    // Combine with chromatic aberration
    vec3 color = vec3(colorR.r, colorG.g, colorB.b);
    
    // Scanlines with flicker
    float scanline = sin(uv.y * u_resolution.y * 2.0 * 3.14159 * 0.5 + sin(u_time * 0.5)) * 0.3 + 0.7;
    
    // Phosphor bloom
    vec3 bloom = color * 0.2;
    color = mix(color, vec3(1.0) - (vec3(1.0) - color) * (vec3(1.0) - bloom), 0.5);
    
    // Vignette
    float vignette = 1.0 - pow(distance(uv, vec2(0.5)), 2.0);
    color *= vignette;
    
    gl_FragColor = vec4(color, 1.0);
}