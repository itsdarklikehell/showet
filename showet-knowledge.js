// Showet Knowledge Base - Real-time demoscene trivia and history
class ShowetKnowledgeBase {
    constructor() {
        this.trivia = [
            "🎵 The demoscene began in the 1980s with cracktros - intros attached to pirated software.",
            "💾 '64K' demos must fit in 64 kilobytes - smaller than a single JPEG!",
            "🏆 Assembly is the world's largest demoparty, held annually in Finland since 1992.",
            "🎸 The original Amiga had only 4096 colors - modern demos show what's possible with that limit.",
            "🕹️ 'Wild' demos allow any platform - from Game Boys to toasters!",
            "🌐 Pouet.net has been the demoscene's database since 1997.",
            "⚡ Raytracing in demos was pioneered on PCs in the mid-90s - years before Pixar's Toy Story.",
            "🎨 'Procedural' graphics generate art mathematically without artists.",
            "🎹 The SID chip on C64 could synthesize entire orchestras in 3 voices.",
            "🚀 Some demos achieve 60fps on hardware from 1987 - pure optimization magic!"
        ];
        this.currentTrivia = 0;
        this.triviaInterval = null;
        this.init();
    }
    
    init() {
        this.createTriviaButton();
        this.setupAutoTrivia();
    }
    
    createTriviaButton() {
        const btn = document.createElement('button');
        btn.textContent = '❓';
        btn.title = "Show demoscene trivia";
        btn.style.cssText = `
            position: fixed;
            bottom: 150px;
            right: 20px;
            background: rgba(0,212,255,0.8);
            color: black;
            border: 1px solid white;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            z-index: 999;
        `;
        btn.onclick = () => this.showRandomTrivia();
        document.body.appendChild(btn);
    }
    
    showRandomTrivia() {
        const fact = this.trivia[Math.floor(Math.random() * this.trivia.length)];
        this.showFact(fact);
    }
    
    showFact(fact) {
        const info = document.getElementById('demo-info');
        if (!info) return;
        
        const existing = info.querySelector('.knowledge-fact');
        if (existing) existing.remove();
        
        const div = document.createElement('div');
        div.className = 'knowledge-fact';
        div.style.cssText = `
            margin-top: 15px;
            padding: 10px;
            background: rgba(255,107,0,0.2);
            border-left: 3px solid var(--accent);
            font-size: 0.85em;
            color: #aaa;
        `;
        div.innerHTML = `<strong style="color:var(--accent);">💡 Scene Fact:</strong> ${fact}`;
        
        info.appendChild(div);
        
        // Auto-remove after 10 seconds
        setTimeout(() => div.remove(), 10000);
    }
    
    setupAutoTrivia() {
        // Show trivia every 60 seconds during playback
        // Check for demo playback in various ways
        setInterval(() => {
            const demoInfo = document.getElementById('demo-info');
            const crtFrame = document.getElementById('crt-frame');
            if (demoInfo && crtFrame && crtFrame.style.display !== 'none') {
                this.showRandomTrivia();
            }
        }, 60000);
    }
    
    getPlatformHistory(platform) {
        const history = {
            'commodore_64': "The C64 sold 12 million units and remains the best-selling computer model of all time. Its SID chip and VIC-II graphics made it a demoscene icon.",
            'commodore_amiga': "Amiga brought us the first consumer multitasking OS, 4096 colors, and 4-channel stereo sound. The demoscene golden age platform.",
            'ms-dos': "PC demoscene exploded with Gravis UltraSound and VGA. Groups like Future Crew pushed multimedia to new heights.",
            'nintendo_famicom': "Famicom demos emerged from Japan's doujin scene - proving console restrictions breed creativity.",
            'sega_megadrive': "Genesis/Mega Drive had 64 colors from a palette of 512 - demos like 'Red Zone' showed incredible 3D on cartridge!"
        };
        return history[platform] || "Every platform has its own unique story in the demoscene saga.";
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetKnowledge = new ShowetKnowledgeBase();
});