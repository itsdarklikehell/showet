/**
 * Showet CRT OSD Effects - Authentic On-Screen Display Overlays
 * Adds period-authentic OSD elements: power LEDs, channel numbers, 
 * static interference, and vintage TV effects
 */

class ShowetCRTOsd {
    constructor(canvasId = 'tvs-canvas') {
        this.canvas = document.getElementById(canvasId) || document.createElement('canvas');
        this.overlay = null;
        this.powerOn = false;
        this.channel = 3;
        this.init();
    }

    init() {
        this.createOsdOverlay();
        this.addPowerButton();
    }

    createOsdOverlay() {
        // Create OSD overlay canvas positioned over the emulator
        const overlay = document.createElement('div');
        overlay.id = 'crt-osd-overlay';
        overlay.style.cssText = `
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 10;
            display: none;
        `;
        
        // Power LED indicator
        const powerLed = document.createElement('div');
        powerLed.id = 'power-led';
        powerLed.style.cssText = `
            position: absolute;
            top: 10px; right: 10px;
            width: 12px; height: 12px;
            background: #ff0000;
            border-radius: 50%;
            box-shadow: 0 0 10px #ff0000;
            opacity: 0.5;
        `;
        
        // Channel display
        const channelDisplay = document.createElement('div');
        channelDisplay.id = 'channel-display';
        channelDisplay.style.cssText = `
            position: absolute;
            top: 50%; right: 20px;
            transform: translateY(-50%);
            color: #0f0;
            font-family: 'Courier New', monospace;
            font-size: 24px;
            text-shadow: 0 0 5px #0f0;
            opacity: 0;
            transition: opacity 0.3s;
        `;
        
        // Static effect overlay
        const staticOverlay = document.createElement('div');
        staticOverlay.id = 'static-overlay';
        staticOverlay.style.cssText = `
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiIgaGVpZ2h0PSIxMDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgcj0iMSIgZmlsbD0icmVkIi8+PC9zdmc+);
            opacity: 0;
            pointer-events: none;
        `;
        
        overlay.appendChild(staticOverlay);
        overlay.appendChild(powerLed);
        overlay.appendChild(channelDisplay);
        this.overlay = overlay;
    }

    addPowerButton() {
        const btn = document.createElement('button');
        btn.id = 'power-toggle';
        btn.innerHTML = '🔌';
        btn.title = 'Power LED Toggle';
        btn.style.cssText = `
            position: fixed;
            bottom: 230px;
            right: 20px;
            background: rgba(255,0,0,0.5);
            color: white;
            border: none;
            padding: 8px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            z-index: 11;
        `;
        btn.onclick = () => this.togglePower();
        document.body.appendChild(btn);
    }

    togglePower() {
        this.powerOn = !this.powerOn;
        const led = document.getElementById('power-led');
        if (led) {
            led.style.background = this.powerOn ? '#00ff00' : '#ff0000';
            led.style.boxShadow = this.powerOn ? '0 0 15px #00ff00' : '0 0 10px #ff0000';
        }
    }

    showChannel(channel) {
        this.channel = channel;
        const display = document.getElementById('channel-display');
        if (display) {
            display.textContent = this.formatChannel(channel);
            display.style.opacity = '1';
            setTimeout(() => {
                display.style.opacity = '0';
            }, 2000);
        }
    }

    formatChannel(ch) {
        // Format like old TVs: "3" or "13-1"
        if (ch < 10) return ` ${ch}`;
        if (ch > 99) return ` ${ch - 99}-1`;
        return String(ch);
    }

    addStaticEffect(duration = 300) {
        const overlay = document.getElementById('static-overlay');
        if (overlay) {
            overlay.style.opacity = '0.8';
            setTimeout(() => {
                overlay.style.opacity = '0';
            }, duration);
        }
    }

    pressChannelButton(direction) {
        if (direction === 'up') {
            this.channel = Math.min(99, this.channel + 1);
        } else {
            this.channel = Math.max(2, this.channel - 1);
        }
        this.showChannel(this.channel);
        
        // Play channel change sound
        if (window.ShowetAudio) {
            ShowetAudio.beep(1200, 0.05, 'square');
            setTimeout(() => ShowetAudio.beep(800, 0.05, 'square'), 30);
        }
    }

    attachTo(containerId) {
        const container = document.getElementById(containerId);
        if (container && this.overlay) {
            container.style.position = 'relative';
            container.appendChild(this.overlay);
        }
    }

    setScanlines(intensity = 0.3) {
        if (!this.overlay) return;
        
        const scanlineOverlay = document.createElement('div');
        scanlineOverlay.id = 'osd-scanlines';
        scanlineOverlay.style.cssText = `
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(
                to bottom,
                transparent ${50 - intensity * 50}%,
                rgba(0,0,0,${intensity}) ${50 - intensity * 25}%,
                transparent ${50 + intensity * 25}%,
                rgba(0,0,0,${intensity / 2}) ${50 + intensity * 50}%
            );
            background-size: 100% ${1 + intensity * 4}px;
            opacity: ${intensity};
            pointer-events: none;
        `;
        
        const existing = document.getElementById('osd-scanlines');
        if (existing) existing.remove();
        this.overlay.appendChild(scanlineOverlay);
    }
}

// Initialize OSD effects
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetCRTOsd = new ShowetCRTOsd();
});