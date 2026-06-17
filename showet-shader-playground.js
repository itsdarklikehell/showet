/**
 * Showet Shader Playground Extension
 * Adds URL sharing and competition mode to the shader editor
 */

class ShowetShaderPlayground extends ShowetShaderEditor {
    constructor() {
        super();
        this.competitionMode = false;
        this.addCompetitionFeatures();
    }

    addCompetitionFeatures() {
        // Add competition mode toggle
        const saveBtn = document.getElementById('save-preset');
        if (saveBtn) {
            const compBtn = document.createElement('button');
            compBtn.id = 'competition-toggle';
            compBtn.textContent = '🏆 Competition Mode';
            compBtn.style.cssText = `
                background: #333;
                color: white;
                padding: 5px 10px;
                border: 1px solid var(--accent);
                cursor: pointer;
                width: 100%;
                margin-top: 8px;
            `;
            compBtn.onclick = () => this.toggleCompetition();
            saveBtn.parentNode.insertBefore(compBtn, saveBtn.nextSibling);
        }
    }

    toggleCompetition() {
        this.competitionMode = !this.competitionMode;
        const btn = document.getElementById('competition-toggle');
        if (btn) {
            btn.style.background = this.competitionMode ? '#ff6b00' : '#333';
            btn.textContent = this.competitionMode ? 
                '🏆 Exit Competition' : '🏆 Competition Mode';
        }
        
        if (this.competitionMode) {
            this.startCompetition();
        } else {
            this.exitCompetition();
        }
    }

    startCompetition() {
        // Generate shareable URL with current shader settings
        const params = this.getCurrentParams();
        const url = new URL(window.location);
        url.searchParams.set('shader', btoa(JSON.stringify(params)));
        
        // Show share dialog
        const shareUrl = url.toString();
        prompt('Share this shader preset URL:', shareUrl);
        
        // Start timer for competition (5 minutes)
        this.competitionTime = 300;
        this.updateCompetitionTimer();
    }

    exitCompetition() {
        this.competitionTime = null;
        const timer = document.getElementById('competition-timer');
        if (timer) timer.remove();
    }

    updateCompetitionTimer() {
        if (!this.competitionTime) return;
        
        const timer = document.createElement('div');
        timer.id = 'competition-timer';
        timer.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #ff6b00;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-family: monospace;
            font-weight: bold;
            z-index: 10000;
        `;
        
        const minutes = Math.floor(this.competitionTime / 60);
        const seconds = this.competitionTime % 60;
        timer.textContent = `⏱️ ${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        document.body.appendChild(timer);
        
        this.competitionTime--;
        if (this.competitionTime > 0) {
            setTimeout(() => this.updateCompetitionTimer(), 1000);
        } else {
            this.endCompetition();
        }
    }

    endCompetition() {
        alert('🏆 Competition time ended! Final shader preset saved.');
        this.savePreset();
        this.toggleCompetition();
    }

    getCurrentParams() {
        return {
            curvature: document.getElementById('curvature-slider')?.value / 100,
            scanlineIntensity: document.getElementById('scanline-slider')?.value / 100,
            phosphorBloom: document.getElementById('bloom-slider')?.value / 200,
            chromaticAberration: document.getElementById('chroma-slider')?.value
        };
    }

    // Override savePreset to include sharing
    savePreset() {
        if (this.competitionMode) {
            // In competition, give special name
            const timestamp = Date.now();
            localStorage.setItem(`showet_comp_entry_${timestamp}`, JSON.stringify(this.getCurrentParams()));
            alert('🏆 Competition entry saved!');
        } else {
            super.savePreset();
        }
    }

    // Share via URL
    sharePreset() {
        const params = this.getCurrentParams();
        const encoded = btoa(JSON.stringify(params));
        const url = `${window.location.origin}${window.location.pathname}?shader=${encoded}`;
        navigator.clipboard.writeText(url);
        alert('🔗 Shader preset URL copied to clipboard!');
    }
}

// Initialize extended shader editor
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetShaderPlayground = new ShowetShaderPlayground();
});