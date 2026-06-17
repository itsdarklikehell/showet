/**
 * Showet Boot Sequence Engine
 * 
 * Creates authentic retro computer startup sequences
 * Mimics AmigaDOS, MS-DOS, C64, and other classic boot experiences
 */

class ShowetBootSequence {
    constructor() {
        this.bootMessages = [];
        this.currentPhase = 0;
        this.element = null;
    }

    // Classic AmigaDOS boot sequence
    getAmigaDOSBoot() {
        return [
            "Initializing ShowEt Demo Runner...",
            "Checking System Resources...",
            "  CPU: 68000 @ 7.09MHz detected",
            "  RAM: 2MB Chip + 8MB Fast OK",
            "Loading Kickstart ROM...",
            "  Version 3.1 (Amiga '95) OK",
            "Mounting DH0 (Workbench)...",
            "  DH0: Ok, 45% used",
            "Detecting Graphics System...",
            "  AGA Chipset initialized",
            "  PAL/NTSC: PAL",
            "Loading Demo Engine...",
            "  ShowEt v2.0 'Future Crew' Edition",
            "Initializing Nostalgist Bridge...",
            "  nostalgist.js v3.0 loaded",
            "  Television Simulator '99 active",
            "Loading Platform Modules...",
            "  84 platforms ready",
            "Checking Stream Engine...",
            "  RTMP/UDP/WebRTC ready",
            "Starting User Interface...",
            "",
            "✓ System Ready",
            "",
            "   ███████╗██╗  ██╗ ██████╗ ██╗   ██╗███████╗████████╗",
            "   ██╔════╝██║  ██║██╔═══██╗██║   ██║██╔════╝╚══██╔══╝",
            "   ███████╗███████║██║   ██║██║   ██║█████╗     ██║   ",
            "   ╚════██║██╔══██║██║   ██║╚██╗ ██╔╝██╔══╝     ██║   ",
            "   ███████║██║  ██║╚██████╔╝ ╚████╔╝ ███████╗   ██║   ",
            "   ╚══════╝╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝   ╚═╝   ",
            "",
            "▶ SHOWET DEMO RUNNER - 'THE FUTURE IS NOW'",
            "",
            "Type 'HELP' for commands or select a platform to begin..."
        ];
    }

    // MS-DOS style boot
    getDosBoot() {
        return [
            "SHOWET DEMO RUNNER v2.0",
            "Copyright (C) 2024-2026 SgtStroopwafel Labs",
            "",
            "Starting MSDOS...",
            "HIMEM.SYS loaded",
            "EMM386.EXE loaded",
            "DOSSEG.EXE loaded",
            "",
            "Loading SHOWET.EXE...",
            "Initializing VIDEOMANAGER...",
            "Initializing AUDIOCONFIG...",
            "Initializing PLATFORMHANDLER...",
            "",
            "84 platform modules loaded",
            "Streaming subsystem active",
            "",
            "C:\\SHOWET> _"
        ];
    }

    // C64 style boot
    getCommodoreBoot() {
        return [
            "COMMODORE 64 DEMO RUNNER",
            "READY.",
            "",
            "LOAD \"$\",8,1",
            "SEARCHING FOR $:",
            "FOUND SHOWET",
            "LOADING...",
            "",
            "64K RAM SYSTEM  38911 BASIC BYTES FREE",
            "",
            "READY.",
            "",
            "   ███████╗██╗  ██╗ ██████╗ ██╗   ██╗███████╗████████╗",
            "   ██╔════╝██║ ██╔╝██╔═══██╗██║   ██║██╔════╝╚══██╔══╝",
            "   ███████╗█████╔╝ ██║   ██║██║   ██║█████╗     ██║   ",
            "   ╚════██║██╔═██╗ ██║   ██║╚██╗ ██╔╝██╔══╝     ██║   ",
            "   ███████║██║  ██╗╚██████╔╝ ╚████╔╝ ███████╗   ██║   ",
            "   ╚══════╝╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝   ╚═╝   ",
            "",
            "READY."
        ];
    }

    async bootSequence(type = 'amiga', containerId = 'loading') {
        this.element = document.getElementById(containerId);
        if (!this.element) return;

        // Select boot type
        switch(type) {
            case 'dos':
                this.bootMessages = this.getDosBoot();
                break;
            case 'c64':
                this.bootMessages = this.getCommodoreBoot();
                break;
            default:
                this.bootMessages = this.getAmigaDOSBoot();
        }

        this.currentPhase = 0;
        this.element.style.fontFamily = '"Courier New", monospace';
        this.element.style.textAlign = 'left';
        this.element.style.whiteSpace = 'pre';
        this.element.style.letterSpacing = '1px';

        // Play boot sound
        this.playBootSound();

        // Animate boot messages
        for (const msg of this.bootMessages) {
            await this.typeMessage(msg);
            await this.delay(50 + Math.random() * 100);
        }

        // Fade to main UI
        setTimeout(() => {
            this.element.innerHTML = `
                <strong>✓ System Ready</strong><br>
                <span class="scene-info">Select a platform to launch a demo</span>
            `;
        }, 2000);
    }

    typeMessage(message) {
        return new Promise(resolve => {
            const start = this.element.innerHTML.length;
            let i = 0;
            const interval = setInterval(() => {
                if (i < message.length) {
                    this.element.innerHTML += message[i];
                    i++;
                } else {
                    clearInterval(interval);
                    this.element.innerHTML += '\n';
                    resolve();
                }
            }, 10);
        });
    }

    playBootSound() {
        // Create retro boot chime using Web Audio API
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = ctx.createOscillator();
        const gain = ctx.createGain();

        oscillator.type = 'square';
        oscillator.frequency.setValueAtTime(440, ctx.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.3);

        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);

        oscillator.connect(gain);
        gain.connect(ctx.destination);
        oscillator.start();
        oscillator.stop(ctx.currentTime + 0.3);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Auto-boot on page load
window.ShowetBoot = new ShowetBootSequence();
document.addEventListener('DOMContentLoaded', () => {
    // Start boot sequence after brief delay
    setTimeout(() => ShowetBoot.bootSequence('amiga'), 500);
});