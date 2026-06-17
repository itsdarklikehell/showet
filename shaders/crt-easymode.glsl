// CRT Easymode Shader - Clean scanlines with minimal curvature
precision mediump float;
uniform sampler2D u_texture;
uniform vec2 u_resolution;
varying vec2 v_texCoord;

void main() {
    vec2 uv = v_texCoord;
    
    // Subtle scanlines
    float scanline = sin(uv.y * u_resolution.y * 2.0) * 0.1 + 0.9;
    
    vec4 color = texture2D(u_texture, uv);
    color.rgb *= scanline;
    
    gl_FragColor = color;
}