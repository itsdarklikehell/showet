/**
 * Showet CRT Shader Engine
 * 
 * Applies authentic retro monitor effects using WebGL shaders
 * Integrates with nostalgist.js Television Simulator '99
 */

class ShowetCRTShader {
    constructor(canvasId = 'tvs-canvas') {
        this.canvas = document.getElementById(canvasId);
        this.gl = this.canvas?.getContext('webgl2') || this.canvas?.getContext('webgl');
        this.program = null;
        this.uniforms = {};
        this.textures = {};
        this.time = 0;
        this.init();
    }

    init() {
        if (!this.gl) {
            console.warn('WebGL not supported, falling back to CSS filters');
            this.useCSSFallback();
            return;
        }
        
        this.compileShaders();
        this.setupUniforms();
    }

    useCSSFallback() {
        // Advanced CSS-based CRT effect as fallback
        const style = document.createElement('style');
        style.textContent = `
            .crt-fallback {
                filter: url(#crt-curvature);
            }
            .scanlines {
                position: relative;
                overflow: hidden;
            }
            .scanlines::before {
                content: "";
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: linear-gradient(
                    to bottom,
                    transparent 50%,
                    rgba(0,0,0,0.2) 50%
                );
                background-size: 100% 4px;
                pointer-events: none;
                animation: scanline-flicker 8ms infinite;
            }
            @keyframes scanline-flicker {
                0%, 100% { opacity: 0.7; }
                50% { opacity: 0.85; }
            }
            .phosphor-glow {
                filter: 
                    contrast(1.1) 
                    saturate(1.2) 
                    brightness(1.05);
            }
        `;
        document.head.appendChild(style);
    }

    compileShaders() {
        // Vertex shader for basic quad rendering
        const vsSource = `
            attribute vec2 a_position;
            attribute vec2 a_texCoord;
            varying vec2 v_texCoord;
            void main() {
                gl_Position = vec4(a_position, 0, 1);
                v_texCoord = a_texCoord;
            }
        `;

        // Fragment shader with CRT effects: curvature, scanlines, phosphor bloom
        const fsSource = `
            precision mediump float;
            uniform sampler2D u_texture;
            uniform float u_time;
            uniform vec2 u_resolution;
            uniform float u_curvature;
            uniform float u_scanlineIntensity;
            uniform float u_phosphorBloom;
            uniform float u_chromaticAberration;
            varying vec2 v_texCoord;

            vec2 curve(vec2 coord) {
                // Barrel distortion for CRT curvature
                coord = coord - 0.5;
                coord *= 1.0 + (coord.yx * coord.yx) * u_curvature * 0.1;
                return coord + 0.5;
            }

            void main() {
                vec2 uv = curve(v_texCoord);
                vec2 uvR = curve(v_texCoord + vec2(u_chromaticAberration, 0.0) / u_resolution);
                vec2 uvB = curve(v_texCoord - vec2(u_chromaticAberration, 0.0) / u_resolution);

                vec4 colorR = texture2D(u_texture, uvR);
                vec4 colorG = texture2D(u_texture, uv);
                vec4 colorB = texture2D(u_texture, uvB);

                // Combine with chromatic aberration
                vec3 color = vec3(colorR.r, colorG.g, colorB.b);

                // Scanlines
                float scanline = sin(uv.y * u_resolution.y * 2.0 * 3.14159 * 0.5) * 0.5 + 0.5;
                scanline = pow(scanline, 1.0 - u_scanlineIntensity);
                color *= scanline;

                // Phosphor bloom effect
                vec3 bloom = color * u_phosphorBloom;
                color = mix(color, vec3(1.0) - (vec3(1.0) - color) * (vec3(1.0) - bloom), 0.5);

                // Curvature vignette
                float vignette = 1.0 - pow(distance(uv, vec2(0.5)), 2.0);
                color *= vignette;

                gl_FragColor = vec4(color, 1.0);
            }
        `;

        // Compile and link shaders
        const vs = this.compileShader(this.gl.VERTEX_SHADER, vsSource);
        const fs = this.compileShader(this.gl.FRAGMENT_SHADER, fsSource);
        
        this.program = this.gl.createProgram();
        this.gl.attachShader(this.program, vs);
        this.gl.attachShader(this.program, fs);
        this.gl.linkProgram(this.program);
        
        if (!this.gl.getProgramParameter(this.program, this.gl.LINK_STATUS)) {
            console.error('Shader compilation failed');
        }
    }

    compileShader(type, source) {
        const shader = this.gl.createShader(type);
        this.gl.shaderSource(shader, source);
        this.gl.compileShader(shader);
        return shader;
    }

    setupUniforms() {
        this.uniforms.time = this.gl.getUniformLocation(this.program, 'u_time');
        this.uniforms.resolution = this.gl.getUniformLocation(this.program, 'u_resolution');
        this.uniforms.curvature = this.gl.getUniformLocation(this.program, 'u_curvature');
        this.uniforms.scanlineIntensity = this.gl.getUniformLocation(this.program, 'u_scanlineIntensity');
        this.uniforms.phosphorBloom = this.gl.getUniformLocation(this.program, 'u_phosphorBloom');
        this.uniforms.chromaticAberration = this.gl.getUniformLocation(this.program, 'u_chromaticAberration');
    }

    apply(uniformOverrides = {}) {
        if (!this.gl || !this.program) return;

        this.gl.useProgram(this.program);
        
        // Default CRT values (max nostalgia!)
        const defaults = {
            curvature: 0.2,           // Subtle barrel distortion
            scanlineIntensity: 0.7,    // Strong scanlines
            phosphorBloom: 0.4,        // Soft phosphor glow
            chromaticAberration: 2.0   // RGB separation
        };

        const params = { ...defaults, ...uniformOverrides };
        
        this.gl.uniform1f(this.uniforms.time, this.time);
        this.gl.uniform2f(this.uniforms.resolution, this.canvas.width, this.canvas.height);
        this.gl.uniform1f(this.uniforms.curvature, params.curvature);
        this.gl.uniform1f(this.uniforms.scanlineIntensity, params.scanlineIntensity);
        this.gl.uniform1f(this.uniforms.phosphorBloom, params.phosphorBloom);
        this.gl.uniform1f(this.uniforms.chromaticAberration, params.chromaticAberration);
    }
}

// Global instance
window.ShowetCRT = new ShowetCRTShader();