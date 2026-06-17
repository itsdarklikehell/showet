/**
 * Showet Sound Theme Manager
 *
 * Extends ShowetAudioEngine to provide looped ambient themes for demoscene atmosphere.
 * Each theme simulates a period-authentic computing environment sound.
 */

class SoundThemeManager {
    constructor(audioEngine) {
        this.audio = audioEngine;
        this.ctx = audioEngine.ctx;
        this.enabled = audioEngine.enabled;
        this.currentTheme = null;
        this.ambientNodes = [];
    }

    // Core method to create a looping ambient node
    createAmbientLoop(frequency, type = 'sine', gain = 0.02, detuneVariation = 0) {
        if (!this.enabled || !this.ctx) return;

        const oscillator = this.ctx.createOscillator();
        const gainNode = this.ctx.createGain();
        const filter = this.ctx.createBiquadFilter();

        oscillator.type = type;
        oscillator.frequency.value = frequency;
        if (detuneVariation > 0) {
            oscillator.detune.setValueAtTime((Math.random() * 2 - 1) * detuneVariation, this.ctx.currentTime);
        }

        // Low-pass filter to soften the sound
        filter.type = 'lowpass';
        filter.frequency.value = 800;

        gainNode.gain.value = gain;

        oscillator.connect(filter);
        filter.connect(gainNode);
        gainNode.connect(this.ctx.destination);

        oscillator.loop = true;
        oscillator.start();

        this.ambientNodes.push({ oscillator, gainNode, filter });
        return oscillator;
    }

    // Themes
    c64RoomTone() {
        this.stopAllAmbience();
        // Low, warm hum of the C64 power supply
        this.createAmbientLoop(55, 'sine', 0.015);
        // Subtle high-frequency noise (RF interference from the SID)
        this.createAmbientLoop(4400, 'noise', 0.008);
        this.currentTheme = 'c64';
    }

    amigaWorkbenchHum() {
        this.stopAllAmbience();
        // Deeper hum of the Amiga's power supply and fan
        this.createAmbientLoop(60, 'sine', 0.02);
        // Floppy drive idle (soft whir) - uses white noise, low
        this.createAmbientLoop(1200, 'noise', 0.01);
        this.currentTheme = 'amiga';
    }

    dosPcSpeakerDrone() {
        this.stopAllAmbience();
        // PC internal PSU hum
        this.createAmbientLoop(60, 'sine', 0.018);
        // PC speaker subtle feedback (very low square wave)
        const osc = this.createAmbientLoop(120, 'square', 0.005);
        if (osc) {
            // Add slight randomness to simulate unstable speaker
            osc.frequency.setValueAtTime(120 + Math.random() * 5, this.ctx.currentTime);
        }
        this.currentTheme = 'dos';
    }

    silentExhibition() {
        this.stopAllAmbience();
        this.currentTheme = 'silent';
    }

    stopAllAmbience() {
        this.ambientNodes.forEach(({ oscillator, gainNode }) => {
            try {
                oscillator.stop();
                gainNode.disconnect();
            } catch (e) { /* Already stopped */ }
        });
        this.ambientNodes = [];
    }

    // Public method to apply a theme
    applyTheme(themeName) {
        const themes = {
            c64: () => this.c64RoomTone(),
            amiga: () => this.amigaWorkbenchHum(),
            dos: () => this.dosPcSpeakerDrone(),
            silent: () => this.silentExhibition()
        };

        if (themes[themeName]) {
            themes[themeName]();
            this.audio.success(); // Play confirmation sound
        } else {
            console.warn(`Unknown sound theme: ${themeName}`);
        }
    }

    // Attach to a dropdown selector
    attachSelector() {
        const selector = document.getElementById('sound-theme-selector');
        if (selector) {
            selector.addEventListener('change', (e) => {
                this.applyTheme(e.target.value);
            });
        }
    }
}

// Initialize Theme Manager once audio engine is ready
document.addEventListener('DOMContentLoaded', () => {
    if (window.ShowetAudio) {
        window.SoundThemes = new SoundThemeManager(window.ShowetAudio);
        window.SoundThemes.attachSelector();
    }
});