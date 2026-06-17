// Showet Spectrum Analyzer - Visual audio for demoscene productions
class ShowetSpectrum {
    constructor(canvasId = 'tvs-canvas') {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas?.getContext('2d');
        this.audioCtx = null;
        this.analyzer = null;
        this.source = null;
        this.visCanvas = null;
        this.visCtx = null;
        this.animationId = null;
        this.enabled = false;
        this.init();
    }

    init() {
        this.createVisualizerOverlay();
    }

    createVisualizerOverlay() {
        // Create overlay canvas for spectrum
        const overlay = document.createElement('canvas');
        overlay.id = 'spectrum-overlay';
        overlay.width = 320;
        overlay.height = 80;
        overlay.style.cssText = `
            position: absolute;
            bottom: 50px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.7);
            border: 1px solid var(--accent);
            border-radius: 4px;
            display: none;
        `;
        
        const container = document.getElementById('emulator-container');
        if (container) {
            container.appendChild(overlay);
        }
        
        this.visCanvas = overlay;
        this.visCtx = overlay.getContext('2d');
        
        // Add toggle button
        const btn = document.createElement('button');
        btn.textContent = '🎵';
        btn.style.cssText = `
            position: fixed;
            bottom: 90px;
            right: 20px;
            background: rgba(0,212,255,0.8);
            color: black;
            border: 1px solid white;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            z-index: 999;
        `;
        btn.onclick = () => this.toggle();
        document.body.appendChild(btn);
    }

    async initAudio() {
        if (!this.audioCtx) {
            this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    toggle() {
        if (!this.visCanvas) return;
        
        this.enabled = !this.enabled;
        if (this.enabled) {
            this.visCanvas.style.display = 'block';
            this.startVisualization();
        } else {
            this.visCanvas.style.display = 'none';
            if (this.animationId) {
                cancelAnimationFrame(this.animationId);
            }
        }
    }

    startVisualization() {
        const draw = () => {
            if (!this.enabled) return;
            
            const width = this.visCanvas.width;
            const height = this.visCanvas.height;
            
            // Clear with fade effect
            this.visCtx.fillStyle = 'rgba(0,0,0,0.3)';
            this.visCtx.fillRect(0, 0, width, height);
            
            // Draw authentic CRT-style bars
            if (this.analyzer) {
                const data = new Uint8Array(this.analyzer.frequencyBinCount);
                this.analyzer.getByteFrequencyData(data);
                
                const barWidth = width / data.length * 2.5;
                
                for (let i = 0; i < data.length; i += 4) {
                    const barHeight = data[i] / 255 * height;
                    
                    // CRT phosphor green glow
                    this.visCtx.fillStyle = '#00ff88';
                    this.visCtx.fillRect(i / 4 * barWidth, height - barHeight, barWidth - 1, barHeight);
                    
                    // Glow effect
                    this.visCtx.fillStyle = '#00aa66';
                    this.visCtx.fillRect(i / 4 * barWidth, height - barHeight, barWidth - 1, barHeight * 0.5);
                }
            } else {
                // Simulate demo audio with authentic patterns
                this.drawSimulatedBars();
            }
            
            this.animationId = requestAnimationFrame(draw);
        };
        
        draw();
    }

    drawSimulatedBars() {
        // Simulated demo scene audio pattern
        const time = Date.now() / 1000;
        const width = this.visCanvas.width;
        const height = this.visCanvas.height;
        
        for (let i = 0; i < 64; i++) {
            const barHeight = Math.abs(Math.sin(time + i * 0.1)) * height * 0.8;
            const hue = (time * 50 + i * 5) % 360;
            
            // Vintage oscilloscope style
            this.visCtx.fillStyle = `hsl(${hue}, 80%, 60%)`;
            this.visCtx.fillRect(i * 5, height - barHeight, 4, barHeight);
        }
    }

    connectAudioSource(source) {
        // Connect an audio source to the analyzer
        this.initAudio().then(() => {
            this.source = this.audioCtx.createMediaElementSource(source);
            this.analyzer = this.audioCtx.createAnalyser();
            this.analyzer.fftSize = 256;
            this.source.connect(this.analyzer);
            this.analyzer.connect(this.audioCtx.destination);
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetSpectrum = new ShowetSpectrum();
});