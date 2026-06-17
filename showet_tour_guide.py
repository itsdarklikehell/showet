#!/usr/bin/env python3
"""
Showet Tour Guide - Interactive demoscene history tour
Curated journey through iconic demos and their technical achievements
"""

from dataclasses import dataclass
from typing import List, Optional
import asyncio

@dataclass
class TourStop:
    demo_name: str
    platform: str
    year: int
    group: str
    party: str
    technical_achievement: str
    cultural_impact: str
    demo_file: Optional[str] = None

class ShowetTourGuide:
    """Interactive guided tour through demoscene history"""
    
    TOUR_STOPS = [
        TourStop("Pouet", "commodore_64", 1987, "Bonzai", "Unknown", 
                 "First cracktro with embedded scroller", 
                 "Established intro culture on C64"),
        
        TourStop("The Cuddly Demos", "commodore_amiga", 1992, "Fairlight", "The Party",
                 "Real-time 3D rendered teddy bears", 
                 "Proved Amiga could do Pixar-style graphics in real-time"),
        
        TourStop("Second Reality", "ms-dos", 1993, "Future Crew", "Assembly",
                 "Revolutionary GUS sound + VGA graphics", 
                 "The demo that inspired a generation of PC coders"),
        
        TourStop("Heaven Seven", "commodore_amiga", 2003, "Conspiracy", "Assembly",
                 "Real-time raytraced reflections", 
                 "Took first place at Assembly 2003"),
        
        TourStop("Loonies", "commodore_64", 2010, "Loonies", "Breakpoint",
                 "Maximum optimization within 64K", 
                 "4K executable demo winner"),
        
        TourStop("Elevated", "ms-dos", 2004, "Conspiracy", "Assembly",
                 "Software-rendered raytracing", 
                 "PC demo that pushed boundaries"),
        
        TourStop("Pimp My Spectrum", "spectrum", 2007, "Fairlight", "Breakpoint",
                 "Creative use of ZX Spectrum limitations", 
                 "Wild compo winner - pure creativity"),
    ]
    
    def __init__(self):
        self.current_stop = 0
        self.tour_active = False
    
    def generate_tour_script(self) -> str:
        """Generate a narration script for the tour"""
        script = "# 🎞️ SHOWET DEMOSCENE TOUR GUIDE\n\n"
        script += "Embark on a journey through the history of digital art...\n\n"
        
        for i, stop in enumerate(self.TOUR_STOPS):
            script += f"## Stop {i+1}: {stop.demo_name} ({stop.year})\n"
            script += f"**Platform:** {stop.platform.replace('_', ' ').title()}\n"
            script += f"**Group:** {stop.group}\n"
            script += f"**Party:** {stop.party}\n"
            script += f"\n**Technical Marvel:** {stop.technical_achievement}\n"
            script += f"**Cultural Impact:** {stop.cultural_impact}\n\n"
        
        script += "---\n*Every frame tells a story. Every pixel holds a memory.*\n"
        return script
    
    def get_next_stop(self) -> Optional[TourStop]:
        """Get next tour stop"""
        if self.current_stop < len(self.TOUR_STOPS):
            stop = self.TOUR_STOPS[self.current_stop]
            self.current_stop += 1
            return stop
        return None
    
    def reset_tour(self):
        """Reset tour to beginning"""
        self.current_stop = 0
        self.tour_active = True
    
    def get_tour_config(self) -> dict:
        """Generate JavaScript config for in-browser tour"""
        return {
            "stops": [
                {
                    "demo": s.demo_name,
                    "platform": s.platform,
                    "year": s.year,
                    "group": s.group,
                    "party": s.party,
                    "fact": f"{s.technical_achievement} - {s.cultural_impact}"
                }
                for s in self.TOUR_STOPS
            ],
            "autoplay": True,
            "transition_time": 30
        }

# JavaScript tour player
TOUR_PLAYER_JS = """
class ShowetTourPlayer {
    constructor() {
        this.currentStop = 0;
        this.stops = [];
        this.autoplay = false;
        this.interval = null;
    }
    
    loadStops(config) {
        this.stops = config.stops || [];
        this.autoplay = config.autoplay || false;
    }
    
    async startTour() {
        if (this.stops.length === 0) return;
        
        const stop = this.stops[this.currentStop];
        if (!stop) return;
        
        // Play stop
        await this.playStop(stop);
        
        // Advance
        this.currentStop = (this.currentStop + 1) % this.stops.length;
        
        if (this.autoplay && this.stops.length > 0) {
            this.interval = setTimeout(() => this.startTour(), 30000);
        }
    }
    
    async playStop(stop) {
        console.log(`🎬 Now playing: ${stop.demo} by ${stop.group} (${stop.year})`);
        console.log(`📜 Fact: ${stop.fact}`);
        
        // Would integrate with actual player
        if (window.launchDemo) {
            window.launchDemo(stop.platform);
        }
        
        // Show fact overlay
        this.showFactOverlay(stop);
    }
    
    showFactOverlay(stop) {
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
        `;
        
        document.body.appendChild(overlay);
        
        // Auto-remove after 15 seconds
        setTimeout(() => {
            const el = document.getElementById('tour-overlay');
            if (el) el.remove();
        }, 15000);
    }
    
    stopTour() {
        this.autoplay = false;
        if (this.interval) {
            clearInterval(this.interval);
        }
    }
}

// Global tour instance
window.ShowetTour = new ShowetTourPlayer();
"""

# Generate tour script
if __name__ == "__main__":
    guide = ShowetTourGuide()
    print(guide.generate_tour_script())