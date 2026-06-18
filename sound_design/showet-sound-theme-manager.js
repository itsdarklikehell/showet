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
        // Add subtle hard drive spin (low whoosh noise)
        this.createAmbientLoop(200, 'noise', 0.007);
        this.currentTheme = 'dos';
    }

    // Additional nostalgia sounds
    playFloppySeek() {
        this.audio.beep(800, 0.02, 'sine');
        setTimeout(() => this.audio.beep(600, 0.015, 'sine'), 30);
        setTimeout(() => this.audio.beep(850, 0.01, 'sine'), 50);
    }

    playKeyboardClick(volume = 0.1) {
        if (!this.enabled) return;
        const ctx = this.ctx;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        
        osc.frequency.value = 2000;
        osc.type = 'square';
        gain.gain.value = volume;
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.05);
    }

    playDiskInsert() {
        this.audio.beep(1200, 0.03, 'sine');
        setTimeout(() => this.audio.beep(800, 0.05, 'sawtooth'), 30);
    }

    playPowerOn() {
        // Rising power-on sound
        if (!this.enabled) return;
        const ctx = this.ctx;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        
        osc.frequency.setValueAtTime(100, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(800, ctx.currentTime + 1.0);
        osc.type = 'sine';
        
        gain.gain.value = 0.1;
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.0);
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 1.0);
    }

    // Authentic demo startup sounds
    playAmigaBootSound() {
        // Floppy drive tick-tick-tick
        this.playFloppySeek();
        setTimeout(() => this.playFloppySeek(), 200);
        // Early startup chime
        setTimeout(() => this.audio.beep(1000, 0.1, 'sine'), 150);
    }

    playC64TapeLoading() {
        // C64 tape loading sound - rapid beeps ascending
        for (let i = 0; i < 6; i++) {
            setTimeout(() => this.audio.beep(400 + i * 100, 0.03, 'square'), i * 40);
        }
    }

    playDosBootBeep() {
        // PC speaker beep - short, sharp
        this.audio.beep(1200, 0.2, 'square');
        setTimeout(() => this.audio.beep(800, 0.15, 'square'), 200);
    }

    playNesPowerOn() {
        // NES rapid power-on
        this.audio.beep(1800, 0.01, 'square');
        setTimeout(() => this.audio.beep(2200, 0.01, 'square'), 15);
        setTimeout(() => this.audio.beep(1800, 0.02, 'sine'), 30);
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