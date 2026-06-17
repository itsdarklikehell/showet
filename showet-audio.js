/**
 * Showet Audio Feedback Engine
 * 
 * Provides authentic chiptune sounds for UI interactions
 * Compatible with Web Audio API
 */

class ShowetAudioEngine {
    constructor() {
        this.ctx = null;
        this.enabled = true;
        this.initAudio();
    }

    initAudio() {
        try {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn('Web Audio API not supported');
            this.enabled = false;
        }
    }

    // Classic computer beep (square wave)
    beep(frequency = 440, duration = 0.1, type = 'square') {
        if (!this.enabled || !this.ctx) return;

        const oscillator = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        oscillator.type = type;
        oscillator.frequency.value = frequency;

        gain.gain.setValueAtTime(0.05, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);

        oscillator.connect(gain);
        gain.connect(this.ctx.destination);
        oscillator.start();
        oscillator.stop(this.ctx.currentTime + duration);
    }

    // UI click/selection sound
    click() {
        if (!this.enabled) return;
        this.beep(880, 0.05, 'square');
        setTimeout(() => this.beep(440, 0.08, 'square'), 30);
    }

    // Menu navigation (rollover)
    rollover() {
        if (!this.enabled) return;
        this.beep(660, 0.03, 'sine');
    }

    // Error sound
    error() {
        if (!this.enabled) return;
        this.beep(220, 0.3, 'sawtooth');
    }

    // Success/confirmation sound
    success() {
        if (!this.enabled) return;
        // Quick arpeggio
        [523, 659, 784, 1047].forEach((freq, i) => {
            setTimeout(() => this.beep(freq, 0.05, 'sine'), i * 40);
        });
    }

    // Loading/hard drive seek sound
    loading() {
        if (!this.enabled) return;
        // Simulated disk seek with random frequencies
        let time = 0;
        for (let i = 0; i < 8; i++) {
            setTimeout(() => {
                this.beep(110 + Math.random() * 440, 0.02, 'noise');
            }, time);
            time += 30 + Math.random() * 20;
        }
    }

    // Key press sound (typing)
    keypress() {
        if (!this.enabled) return;
        this.beep(330, 0.01, 'square');
    }

    // Attach to UI elements automatically
    attachToElements() {
        // Buttons
        document.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', () => this.click());
        });

        // Platform items (mouseover)
        document.querySelectorAll('.platform-item').forEach(item => {
            item.addEventListener('mouseenter', () => this.rollover());
        });

        // Search input
        const search = document.getElementById('search');
        if (search) {
            search.addEventListener('input', () => {
                if (search.value.length > 0) this.keypress();
            });
        }

        // Shader selector
        const shaderSelect = document.getElementById('shader-select');
        if (shaderSelect) {
            shaderSelect.addEventListener('change', () => this.success());
        }
    }
}

// Global audio engine instance
window.ShowetAudio = new ShowetAudioEngine();

// Auto-attach on load
document.addEventListener('DOMContentLoaded', () => {
    ShowetAudio.attachToElements();
});