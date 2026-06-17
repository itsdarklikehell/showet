/**
 * Showet Museum Mode - Exhibition-Quality Demo Presentation
 * Automatic demo curation with curatorial notes and kiosk mode
 */

class ShowetMuseumMode {
    constructor() {
        this.demos = [];
        this.currentIndex = 0;
        this.isPlaying = false;
        this.kioskMode = false;
        this.curatorNotes = {
            "Second Reality": "Future Crew's 1993 PC demo masterpiece. Introduced groundbreaking effects including real-time raytracing and the famous 'Unreal' engine.",
            "Heaven Seven": "Conspiracy's 2003 Amiga demo. Peak of the AGA era with stunning graphics and iconic soundtrack by Radix.",
            "Elevated": "Conspiracy's 2004 PC demo. Revolutionary for its time, featuring photo-realistic graphics and advanced lighting techniques.",
            "Arte": "Sanctuary's 1991 Amiga demo. Classic example of early 90s demo aesthetics with smooth 3D vectors."
        };
    }

    // Initialize museum mode
    init() {
        this.addMuseumButton();
    }

    addMuseumButton() {
        const btn = document.createElement('button');
        btn.textContent = '🏛️ Museum Mode';
        btn.style.cssText = `
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: rgba(123, 67, 255, 0.8);
            color: white;
            border: 1px solid white;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            z-index: 999;
        `;
        btn.onclick = () => this.toggleKiosk();
        document.body.appendChild(btn);
    }

    async loadMilestoneDemos() {
        // In real implementation, fetch from Pouet API and integrate demo scoring
        // For now, use pre-scored demos
        this.demos = [
            { id: "second-reality", name: "Second Reality", year: 1993, score: 94.0, platform: "commodore_amiga", notes: this.curatorNotes["Second Reality"] },
            { id: "heaven-seven", name: "Heaven Seven", year: 2003, score: 88.5, platform: "commodore_amiga", notes: this.curatorNotes["Heaven Seven"] },
            { id: "elevated", name: "Elevated", year: 2004, score: 87.0, platform: "pc", notes: this.curatorNotes["Elevated"] },
            { id: "arte", name: "Arte", year: 1991, score: 80.0, platform: "commodore_amiga", notes: this.curatorNotes["Arte"] }
        ];
    }

    toggleKiosk() {
        this.kioskMode = !this.kioskMode;
        if (this.kioskMode) {
            this.enterKiosk();
        } else {
            this.exitKiosk();
        }
    }

    enterKiosk() {
        document.body.style.margin = '0';
        document.body.style.padding = '0';
        document.body.style.overflow = 'hidden';
        
        const kioskOverlay = document.createElement('div');
        kioskOverlay.id = 'museum-overlay';
        kioskOverlay.style.cssText = `
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: black;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        `;
        
        kioskOverlay.innerHTML = `
            <div style="color: white; font-family: monospace; text-align: center;">
                <h2 style="font-size: 2em; margin-bottom: 20px;">🏛️ SHOWET MUSEUM MODE</h2>
                <p style="font-size: 1.2em; color: #aaa;">Loading demoscene milestones...</p>
                <div id="curator-notes" style="margin-top: 30px; max-width: 600px; padding: 20px; background: #111; border-radius: 8px;"></div>
                <div id="progress-bar" style="width: 100%; height: 4px; background: #333; margin-top: 30px; border-radius: 2px; overflow: hidden;">
                    <div id="progress-fill" style="width: 0%; height: 100%; background: #ff6b00;"></div>
                </div>
            </div>
        `;
        
        document.body.appendChild(kioskOverlay);
        
        // Start automated demo rotation
        this.loadMilestoneDemos().then(() => {
            this.showNextDemo();
        });
    }

    exitKiosk() {
        const overlay = document.getElementById('museum-overlay');
        if (overlay) overlay.remove();
        document.body.style.margin = '';
        document.body.style.padding = '';
        document.body.style.overflow = '';
    }

    showNextDemo() {
        if (this.currentIndex >= this.demos.length) this.currentIndex = 0;
        
        const demo = this.demos[this.currentIndex];
        const notesEl = document.getElementById('curator-notes');
        
        if (notesEl) {
            notesEl.innerHTML = `
                <div style="color: #ff6b00; font-size: 1.5em; margin-bottom: 10px;">${demo.name}</div>
                <div style="color: #888; font-size: 0.9em;">${demo.year} • ${demo.platform} • Score: ${demo.score || 'N/A'}</div>
                <div style="color: #ccc; margin-top: 15px;">${demo.notes}</div>
            `;
        }
        
        // Launch demo
        this.launchDemo(demo);
        this.currentIndex++;
    }

    launchDemo(demo) {
        // Trigger demo launch
        console.log(`[Museum] Launching ${demo.name}`);
        
        // Progress bar animation
        let progress = 0;
        const fill = document.getElementById('progress-fill');
        if (fill) {
            const interval = setInterval(() => {
                progress += 2;
                fill.style.width = progress + '%';
                if (progress >= 100) {
                    clearInterval(interval);
                    setTimeout(() => this.showNextDemo(), 5000); // 5s per demo
                }
            }, 100);
        }
    }
}

// Initialize Museum Mode
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetMuseum = new ShowetMuseumMode();
    ShowetMuseum.init();
});