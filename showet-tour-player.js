// Showet Tour Player - Guided demoscene history tour
class ShowetTourPlayer {
    constructor() {
        this.currentStop = 0;
        this.stops = [];
        this.autoplay = false;
        this.interval = null;
        this.init();
    }
    
    init() {
        // Default tour stops (curated classics)
        this.stops = [
            {demo: "Pouet", platform: "commodore_64", year: 1987, group: "Bonzai", party: "Unknown",
             fact: "First cracktro with embedded scroller - Established intro culture on C64"},
            
            {demo: "The Cuddly Demos", platform: "commodore_amiga", year: 1992, group: "Fairlight", party: "The Party",
             fact: "Real-time 3D rendered teddy bears - Proved Amiga could do Pixar-style graphics"},
            
            {demo: "Second Reality", platform: "ms-dos", year: 1993, group: "Future Crew", party: "Assembly",
             fact: "Revolutionary GUS sound + VGA graphics - The demo that inspired a generation"},
            
            {demo: "Heaven Seven", platform: "commodore_amiga", year: 2003, group: "Conspiracy", party: "Assembly",
             fact: "Real-time raytraced reflections - Took first place at Assembly 2003"},
            
            {demo: "Loonies", platform: "commodore_64", year: 2010, group: "Loonies", party: "Breakpoint",
             fact: "Maximum optimization within 64K - 4K executable demo winner"},
        ];
        
        this.createTourButton();
    }
    
    createTourButton() {
        const btn = document.createElement('button');
        btn.textContent = '🎞️ Tour';
        btn.style.cssText = `
            position: fixed;
            bottom: 120px;
            right: 20px;
            background: rgba(255,45,85,0.8);
            color: white;
            border: 1px solid white;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            z-index: 999;
        `;
        btn.onclick = () => this.toggleTour();
        document.body.appendChild(btn);
    }
    
    toggleTour() {
        if (this.autoplay) {
            this.stopTour();
        } else {
            this.startTour();
        }
    }
    
    async startTour() {
        this.autoplay = true;
        ShowetAudio.click();
        await this.nextStop();
    }
    
    async nextStop() {
        if (!this.autoplay) return;
        
        const stop = this.stops[this.currentStop];
        if (!stop) {
            this.currentStop = 0;
            return;
        }
        
        this.showFactOverlay(stop);
        
        // Advance with interval
        this.interval = setTimeout(() => {
            this.currentStop = (this.currentStop + 1) % this.stops.length;
            this.nextStop();
        }, 20000);
    }
    
    showFactOverlay(stop) {
        // Remove existing overlay
        const existing = document.getElementById('tour-overlay');
        if (existing) existing.remove();
        
        const overlay = document.createElement('div');
        overlay.id = 'tour-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.95);
            padding: 20px;
            border: 2px solid var(--accent);
            border-radius: 8px;
            z-index: 2000;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 0 30px rgba(255,107,0,0.5);
        `;
        
        overlay.innerHTML = `
            <div style="font-size:1.2em;color:var(--accent);margin-bottom:10px;">
                🎞️ TOUR STOP: ${stop.demo}
            </div>
            <div style="margin-bottom:5px;"><strong>Group:</strong> ${stop.group}</div>
            <div style="margin-bottom:5px;"><strong>Year:</strong> ${stop.year}</div>
            <div style="margin-bottom:10px;"><strong>Party:</strong> ${stop.party}</div>
            <div style="color:#aaa;font-size:0.9em;border-top:1px solid #333;padding-top:10px;">
                ${stop.fact}
            </div>
            <div style="margin-top:10px;color:#666;font-size:0.8em;">
                Stop ${this.currentStop + 1} of ${this.stops.length}
            </div>
        `;
        
        document.body.appendChild(overlay);
        
        // Auto-launch demo on platform
        if (typeof launchPlatform === 'function') {
            setTimeout(() => launchPlatform(stop.platform), 1000);
        } else {
            console.log(`[Tour] Would launch: ${stop.platform}`);
        }
    }
    
    stopTour() {
        this.autoplay = false;
        if (this.interval) {
            clearTimeout(this.interval);
        }
        const overlay = document.getElementById('tour-overlay');
        if (overlay) overlay.remove();
        ShowetAudio.click();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetTour = new ShowetTourPlayer();
});