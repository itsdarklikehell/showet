// CRT Pi Shader - Raspberry Pi style shader with pixel curvature
precision mediump float;
uniform sampler2D u_texture;
uniform vec2 u_resolution;
varying vec2 v_texCoord;

// Integer pixelation
vec2 pixelCoords(vec2 coord, vec2 resolution) {
    vec2 pixels = coord * resolution;
    pixels = floor(pixels / 4.0) * 4.0;
    return pixels / resolution;
}

void main() {
    // Pixelated coordinates
    vec2 uv = pixelCoords(v_texCoord, u_resolution);
    
    // Strong scanlines
    float scanline = mod(floor(uv.y * u_resolution.y / 2.0), 2.0) > 0.5 ? 0.7 : 1.0;
    
    vec4 color = texture2D(u_texture, uv);
    
    // Curved scanlines (like CRT phosphor)
    float curve = sin(uv.y * 3.14159) * 0.1;
    color.rgb *= mix(0.8, 1.2, scanline + curve * 0.1);
    
    gl_FragColor = vec4(color.rgb, 1.0);
}