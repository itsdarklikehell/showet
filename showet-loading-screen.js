/**
 * Showet Loading Screen - Demoscene-Style Loading Experience
 * Authentic loading screens with period-appropriate progress indicators
 */

class ShowetLoadingScreen {
    constructor() {
        this.container = null;
        this.progressBar = null;
        this.loadingText = null;
        this.bootLines = [];
        this.visible = false;
    }

    create() {
        if (this.container) return;

        this.container = document.createElement('div');
        this.container.id = 'showet-loading';
        this.container.style.cssText = `
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(135deg, #001a33, #000);
            z-index: 9999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Courier New', monospace;
            color: #0f0;
            transition: opacity 0.5s;
        `;

        this.container.innerHTML = `
            <div id="loading-boot-text" style="text-align:left;margin-bottom:30px;font-size:14px;line-height:1.6;max-width:600px;"></div>
            <div style="width:80%;height:20px;border:2px solid #0f0;margin-bottom:20px;position:relative;box-shadow:0 0 10px #0f0;">
                <div id="loading-progress" style="width:0%;height:100%;background:#0f0;transition:width 0.3s;"></div>
            </div>
            <div id="loading-percentage" style="font-size:24px;margin-bottom:20px;">LOADING... 0%</div>
            <div id="loading-message" style="color:#aaa;font-size:12px;"></div>
        `;

        document.body.appendChild(this.container);
        this.progressBar = document.getElementById('loading-progress');
        this.loadingText = document.getElementById('loading-percentage');
        this.bootText = document.getElementById('loading-boot-text');
        this.messageText = document.getElementById('loading-message');
    }

    show(platform = 'amiga') {
        this.create();
        this.visible = true;
        this.setPlatformMessages(platform);
        this.container.style.display = 'flex';
        
        // Play startup sound
        if (window.ShowetAudio) {
            ShowetAudio.playPowerOn();
        }
    }

    hide() {
        if (!this.container) return;
        this.visible = false;
        this.container.style.opacity = '0';
        setTimeout(() => {
            this.container.style.display = 'none';
        }, 500);
    }

    setProgress(percent, message = '') {
        if (!this.progressBar) return;
        this.progressBar.style.width = `${percent}%`;
        if (this.loadingText) {
            this.loadingText.textContent = `LOADING... ${percent}%`;
        }
        if (message && this.messageText) {
            this.messageText.textContent = message;
        }
    }

    addBootLine(text, delay = 100) {
        if (!this.bootText) return;
        
        setTimeout(() => {
            this.bootText.innerHTML += `<div>> ${text}</div>`;
            this.bootText.scrollTop = this.bootText.scrollHeight;
            
            // Play keyboard click for each line
            if (window.SoundThemes) {
                SoundThemes.playKeyboardClick(0.05);
            }
        }, this.bootLines.length * delay);
        
        this.bootLines.push(text);
    }

    setPlatformMessages(platform) {
        const messages = {
            c64: [
                "COMMODORE 64 BASIC V2.0",
                "64K RAM SYSTEM 38911 BASIC BYTES FREE",
                "READY.",
                "LOAD\"$\",8,1"
            ],
            amiga: [
                "Amiga 500 Boot Sequence",
                "Kickstart 1.3 - Loading...",
                "Chipset: Original Chip Set",
                "Memory: 512KB Chip RAM + 512KB Fast RAM",
                "Starting Workbench..."
            ],
            dos: [
                "MS-DOS 6.22",
                "HIMEM.SYS loaded",
                "EMM386.EXE loaded",
                "Creative Sound Blaster detected",
                "Loading demo engine..."
            ],
            pc: [
                "PC Engine TurboGrafx-16",
                "HuC6280 CPU @ 7.16 MHz",
                "Initializing CD-ROM...",
                "Loading HuCard data..."
            ]
        };

        const lines = messages[platform] || messages.amiga;
        lines.forEach((line, i) => {
            this.addBootLine(line, 300);
        });
        
        this.addBootLine("DEMONSTRATION LOADING...", 500);
    }

    simulateLoading(duration = 3000, onComplete = null) {
        let progress = 0;
        const interval = 50;
        const steps = duration / interval;
        
        const timer = setInterval(() => {
            progress += Math.random() * 10;
            if (progress >= 100) {
                progress = 100;
                clearInterval(timer);
                setTimeout(() => {
                    this.hide();
                    if (onComplete) onComplete();
                }, 500);
            }
            this.setProgress(Math.min(progress, 100));
        }, interval);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetLoading = new ShowetLoadingScreen();
});