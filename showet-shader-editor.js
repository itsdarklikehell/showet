// Showet Shader Live Editor - Real-time CRT shader customization
class ShowetShaderEditor {
    constructor(canvasId = 'tvs-canvas') {
        this.canvas = document.getElementById(canvasId);
        this.gl = this.canvas?.getContext('webgl2') || this.canvas?.getContext('webgl');
        this.shaderSelect = document.getElementById('shader-select');
        this.customPanel = null;
        this.init();
    }

    init() {
        this.createCustomPanel();
        this.setupLivePreview();
    }

    createCustomPanel() {
        // Create floating shader control panel
        const panel = document.createElement('div');
        panel.id = 'shader-editor-panel';
        panel.style.cssText = `
            position: fixed;
            top: 50%;
            right: 20px;
            transform: translateY(-50%);
            background: rgba(0,0,0,0.9);
            padding: 15px;
            border: 2px solid var(--accent);
            border-radius: 8px;
            font-family: monospace;
            color: white;
            font-size: 12px;
            display: none;
            z-index: 1000;
        `;
        
        panel.innerHTML = `
            <h4 style="margin:0 0 10px 0;color:var(--accent);">🎨 Shader Tuner</h4>
            <div style="margin-bottom:10px;">
                <label>Curvature: <input type="range" id="curvature-slider" min="0" max="50" value="20"></label>
            </div>
            <div style="margin-bottom:10px;">
                <label>Scanlines: <input type="range" id="scanline-slider" min="0" max="100" value="70"></label>
            </div>
            <div style="margin-bottom:10px;">
                <label>Bloom: <input type="range" id="bloom-slider" min="0" max="100" value="40"></label>
            </div>
            <div style="margin-bottom:10px;">
                <label>Chromatic: <input type="range" id="chroma-slider" min="0" max="10" value="2"></label>
            </div>
            <button id="save-preset" style="background:#333;color:white;padding:5px 10px;border:1px solid var(--accent);cursor:pointer;width:100%;">
                💾 Save Preset
            </button>
        `;
        
        document.body.appendChild(panel);
        this.customPanel = panel;
        
        // Add toggle button to showcase
        const toggleBtn = document.createElement('button');
        toggleBtn.textContent = '🎨';
        toggleBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #ff6b00;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 50%;
            cursor: pointer;
            z-index: 999;
        `;
        toggleBtn.onclick = () => this.togglePanel();
        document.body.appendChild(toggleBtn);
        
        // Hook up sliders
        this.setupSliders();
    }

    setupSliders() {
        ['curvature', 'scanline', 'bloom', 'chroma'].forEach(id => {
            const slider = document.getElementById(`${id}-slider`);
            if (slider) {
                slider.oninput = () => this.updatePreview();
            }
        });
        
        const saveBtn = document.getElementById('save-preset');
        if (saveBtn) {
            saveBtn.onclick = () => this.savePreset();
        }
    }

    updatePreview() {
        const values = {
            curvature: document.getElementById('curvature-slider')?.value / 100 || 0.2,
            scanlineIntensity: document.getElementById('scanline-slider')?.value / 100 || 0.7,
            phosphorBloom: document.getElementById('bloom-slider')?.value / 200 || 0.4,
            chromaticAberration: document.getElementById('chroma-slider')?.value || 2.0
        };
        
        if (window.ShowetCRT) {
            window.ShowetCRT.apply(values);
        }
    }

    savePreset() {
        const values = {
            curvature: document.getElementById('curvature-slider')?.value / 100,
            scanlineIntensity: document.getElementById('scanline-slider')?.value / 100,
            phosphorBloom: document.getElementById('bloom-slider')?.value / 200,
            chromaticAberration: document.getElementById('chroma-slider')?.value
        };
        
        localStorage.setItem('showet_shader_preset', JSON.stringify(values));
        alert('✅ Shader preset saved!');
    }

    loadPreset() {
        const saved = localStorage.getItem('showet_shader_preset');
        if (saved) {
            const values = JSON.parse(saved);
            // Apply values to sliders and preview
            Object.entries(values).forEach(([key, val]) => {
                const slider = document.getElementById(`${key}-slider`);
                if (slider) {
                    slider.value = key === 'phosphorBloom' ? val * 200 : 
                                  key === 'scanlineIntensity' ? val * 100 : val;
                }
            });
            this.updatePreview();
        }
    }

    togglePanel() {
        if (this.customPanel) {
            this.customPanel.style.display = 
                this.customPanel.style.display === 'none' ? 'block' : 'none';
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetShaderEditor = new ShowetShaderEditor();
    // Auto-load saved preset
    setTimeout(() => ShowetShaderEditor.loadPreset(), 1000);
});