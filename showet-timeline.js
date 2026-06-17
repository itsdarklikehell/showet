// Showet Demo Timeline - Interactive demoscene explorer
class ShowetDemoTimeline {
    constructor(containerId = 'demo-info') {
        this.container = document.getElementById(containerId);
        this.eras = [
            {year: 1980, name: "Foundations", color: "#6b00ff", desc: "First C64/Apple demos", demos: ["Commodore 64 Cracktros", "Apple II Scenewares"] },
            {year: 1985, name: "Cracktro Era", color: "#00d4ff", desc: "Intro music & effects", demos: ["Fairlight Cracktros", "Booze Design intros"] },
            {year: 1990, name: "Amiga Glory", color: "#ff6b00", desc: "AGA demo scene golden age", demos: ["Second Reality", "Arte", "Phenomena"] },
            {year: 1995, name: "PC Power", color: "#ff2d55", desc: "90s PC demonstrations", demos: ["Future Crew", "Farbrausch classics", "Conspiracy"] },
            {year: 2000, name: "Modern Age", color: "#00ff88", desc: "GLSL shaders emerge", demos: ["Elevated", "FR-08", "Loonies"] },
            {year: 2010, name: "Wild Demos", color: "#ffff00", desc: "Creative wild category", demos: ["Chaos Constructions", "Artfield", "RNO"] },
            {year: 2020, name: "AI Era", color: "#ff00ff", desc: "Neural style transfer", demos: ["Revision AI Compo", "Demosplash Neural", "GLSL Generative"] }
        ];
        this.init();
    }

    init() {
        // Add timeline button to showcase
        const timelineBtn = document.createElement('button');
        timelineBtn.textContent = '📅 Timeline';
        timelineBtn.style.cssText = `
            position: fixed;
            bottom: 60px;
            right: 20px;
            background: rgba(255,107,0,0.8);
            color: white;
            border: 1px solid white;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            z-index: 999;
        `;
        timelineBtn.onclick = () => this.showTimeline();
        document.body.appendChild(timelineBtn);
    }

    showTimeline() {
        if (!this.container) return;
        
        let html = '<div style="background:#111;padding:15px;border-radius:8px;border:1px solid var(--accent);max-height:80vh;overflow-y:auto;">';
        html += '<h4 style="color:var(--accent);margin-top:0;">📅 Demo Scene Timeline Explorer</h4>';
        
        this.eras.forEach((era, i) => {
            html += `
                <div style="margin:10px 0;padding:10px;border-left:3px solid ${era.color};background:#1a1a1a;border-radius:0 4px 4px 0;cursor:pointer;" onclick="ShowetTimeline.loadEraDemos('${era.name}')">
                    <strong style="color:${era.color}">[${era.year}]</strong> ${era.name}
                    <br><small style="color:#888">${era.desc}</small>
                    <div style="font-size:0.8em;color:#aaa;margin-top:5px;">
                        <em>Click to explore demos →</em>
                    </div>
                </div>
            `;
        });
        
        html += `
            <div style="margin-top:15px;padding:10px;background:#1a1a1a;border-radius:5px;">
                <strong style="color:var(--accent)">🕹️ Legendary Demos:</strong>
                <div style="font-size:0.85em;margin-top:5px;">
                    • <span style="color:#ff6b00">Heaven Seven</span> (Amiga '03)
                    • <span style="color:#ff2d55">Second Reality</span> (PC '93)
                    • <span style="color:#00d4ff">Pouet</span> (C64 '87)
                    • <span style="color:#00ff88">Elevated</span> (GLSL '04)
                </div>
                <button onclick="ShowetTimeline.loadDemo(12345)" style="margin-top:10px;padding:5px 10px;background:#00d4ff;color:black;border:none;border-radius:3px;cursor:pointer;">Stream Trending Demo</button>
            </div>
        `;
        
        html += '</div>';
        this.container.innerHTML = html;
    }

    async loadEraDemos(eraName) {
        // Find the era
        const era = this.eras.find(e => e.name === eraName);
        if (!era) return;
        
        // Show loading state
        if (this.container) {
            this.container.innerHTML = `<div style="background:#111;padding:15px;border-radius:8px;color:var(--accent);">Loading demos for ${eraName}...</div>`;
        }
        
        // In a real implementation, this would fetch from Pouet API
        // For now, simulate with the demo list
        let html = `<div style="background:#111;padding:15px;border-radius:8px;border:1px solid ${era.color};">`;
        html += `<h4 style="color:${era.color};margin-top:0;">${era.name} Demos</h4>`;
        
        era.demos.forEach(demo => {
            html += `
                <div style="padding:8px;margin:5px 0;background:#1a1a1a;border-radius:4px;cursor:pointer;" onclick="ShowetTimeline.launchDemo('${demo}')">
                    ▶ ${demo}
                </div>
            `;
        });
        
        html += `<button onclick="ShowetTimeline.showTimeline()" style="margin-top:10px;padding:5px 10px;background:#333;color:white;border:1px solid #555;border-radius:3px;cursor:pointer;">← Back to Timeline</button>`;
        html += '</div>';
        
        if (this.container) {
            this.container.innerHTML = html;
        }
    }

    launchDemo(demoName) {
        // Trigger the click event on platform items or launch via API
        console.log(`Launching demo: ${demoName}`);
        // Would integrate with the main launcher
    }

    async loadDemo(demoId) {
        // This would integrate with showet API to stream a demo
        console.log(`Loading demo ID: ${demoId}`);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetTimeline = new ShowetDemoTimeline();
});