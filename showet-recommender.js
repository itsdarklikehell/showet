/**
 * Showet Demo Recommender
 * 
 * AI-powered demo recommendations with historical context and era matching.
 */

class ShowetRecommender {
    constructor() {
        this.demos = [
            { name: "Second Reality", group: "Future Crew", year: 1993, platform: "commodore_amiga", score: 94.0, tags: ["pc-dos", "3d", "intro"] },
            { name: "Heaven Seven", group: "Conspiracy", year: 2003, platform: "commodore_amiga", score: 91.0, tags: ["pc-dos", "wild", "4k"] },
            { name: "Especially for You", group: "Fairlight", year: 2009, platform: "commodore_64", score: 88.0, tags: ["c64", "music", "demo"] },
            { name: "Bad Apple!!", group: "ZUN", year: 2007, platform: "nintendo_famicom", score: 85.0, tags: ["nes", "video", "famicom"] },
            { name: "Pimp Pistols", group: "Boozoholics", year: 2000, platform: "commodore_64", score: 82.0, tags: ["c64", "wild", "amiga"] },
        ];
    }

    // Get random demo seed for Shader Playground
    getRandomDemoSeed() {
        const seed = Math.floor(Math.random() * 10000);
        return `seed=${seed}&platform=demo&effect=${['plasma','tunnel','starfield','raster'][Math.floor(Math.random()*4)]}`;
    }

    // Get trending demos from current era
    getTrendingDemos(count = 5) {
        // Sort by score descending, take top N
        return [...this.demos].sort((a, b) => b.score - a.score).slice(0, count);
    }

    // Get demos by platform
    getDemosByPlatform(platform) {
        return this.demos.filter(d => d.platform.includes(platform.toLowerCase()));
    }

    // Get random demo for party mode
    getRandomDemo() {
        return this.demos[Math.floor(Math.random() * this.demos.length)];
    }

    // Get era-based recommendations
    getEraRecommendations(era) {
        const eraYears = {
            '80s': { min: 1980, max: 1989 },
            '90s': { min: 1990, max: 1999 },
            '2000s': { min: 2000, max: 2009 },
            '2010s': { min: 2010, max: 2019 },
            'modern': { min: 2020, max: 2026 }
        };
        
        const range = eraYears[era.toLowerCase()];
        if (!range) return this.getTrendingDemos();
        
        return this.demos.filter(d => d.year >= range.min && d.year <= range.max);
    }

    // Create recommendation HTML for showcase
    createRecommendationPanel() {
        const trending = this.getTrendingDemos(3);
        
        let html = `
        <div style="margin-top:15px;padding:15px;background:#111;border-radius:5px;border:1px solid var(--accent);">
            <h4 style="color:var(--accent);margin-top:0;">🎯 AI Recommendations</h4>
            <div id="rec-list"></div>
            <button onclick="ShowetRecommender.shuffle()" style="background:#333;color:white;padding:8px 15px;border:1px solid var(--accent);margin-top:10px;cursor:pointer;">
                🎲 Shuffle Recommendations
            </button>
        </div>
        `;
        
        return html;
    }

    // Render recommendations
    renderRecommendations() {
        const container = document.getElementById('rec-list');
        if (!container) return;
        
        const trending = this.getTrendingDemos(3);
        container.innerHTML = trending.map(d => `
            <div style="font-size:0.85em;margin:5px 0;padding:8px;background:#222;border-radius:3px;cursor:pointer;" 
                 onclick="launchDemo('${d.platform}')">
                <strong>${d.name}</strong> by ${d.group}<br>
                <span style="color:#666;">${d.year} • Score: ${d.score}/100</span>
            </div>
        `).join('');
    }

    static shuffle() {
        const recommender = new ShowetRecommender();
        recommender.renderRecommendations();
    }
}

// Initialize
window.ShowetRecommender = new ShowetRecommender();

// Add to showcase if available
document.addEventListener('DOMContentLoaded', () => {
    const demoInfo = document.getElementById('demo-info');
    if (demoInfo) {
        demoInfo.insertAdjacentHTML('beforeend', ShowetRecommender.createRecommendationPanel());
        ShowetRecommender.renderRecommendations();
    }
});