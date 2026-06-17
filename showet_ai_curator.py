#!/usr/bin/env python3
"""
Showet AI Demo Curator
Intelligent demo recommendation engine using content analysis and user preferences
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class DemoEra(Enum):
    CLASSIC_8BIT = "8bit_classic"      # C64, Apple II, Atari 800
    ARCADE_ERA = "arcade_era"          # Arcade machines, Vector era
    AMIGA_GLORY = "amiga_glory"        # Amiga demo scene golden age
    PC_POWER = "pc_power"               # PC demoscene (1990s)
    MODERN_SHADER = "modern_shader"     # WebGL/GLSL modern demos
    RETRO_FUTURE = "retro_future"       # Modern demos on vintage hardware

@dataclass
class DemoVector:
    """Technical and aesthetic vector for demo classification"""
    platform: str
    era: DemoEra
    style: str  # visual, musical, technical, combined
    complexity: int  # 1-10 scale
    color_depth: int  # bits
    resolution: tuple  # (width, height)
    features: List[str]  # ["scanlines", "vectors", "3d", "chaos"]

class AIDemoCurator:
    """AI-powered demo recommendation engine"""
    
    def __init__(self):
        self.preferences = {}  # user_id -> preferred styles
        self.demo_catalog = self._load_demo_catalog()
    
    def _load_demo_catalog(self) -> List[DemoVector]:
        """Load demo catalog with technical vectors"""
        catalog_path = Path(__file__).parent / "demo_database.py"
        # Placeholder for real catalog loading
        return [
            DemoVector(
                platform="commodore_64",
                era=DemoEra.CLASSIC_8BIT,
                style="visual",
                complexity=7,
                color_depth=16,
                resolution=(320, 200),
                features=["raster", "color", "animation"]
            ),
            DemoVector(
                platform="commodore_amiga",
                era=DemoEra.AMIGA_GLORY,
                style="combined",
                complexity=9,
                color_depth=4096,
                resolution=(320, 240),
                features=["3d", "music", "effects"]
            ),
        ]
    
    def analyze_preferences(self, user_id: str, watched_demos: List[str]) -> Dict:
        """Analyze user watching history to build preference profile"""
        features_used = {}
        
        for demo_id in watched_demos:
            demo = self._find_demo(demo_id)
            if demo:
                # Weight preferences by complexity
                self.preferences[user_id] = self.preferences.get(user_id, {})
                
                self.preferences[user_id]['preferred_era'] = self.preferences[user_id].get('preferred_era', demo.era.value)
                self.preferences[user_id]['avg_complexity'] = (
                    self.preferences[user_id].get('avg_complexity', 0) + demo.complexity
                ) / 2
                
                for feature in demo.features:
                    features_used[feature] = features_used.get(feature, 0) + 1
        
        self.preferences[user_id]['favorite_features'] = sorted(
            features_used.keys(), 
            key=lambda x: features_used[x], 
            reverse=True
        )[:3]
        
        return self.preferences.get(user_id, {})
    
    def recommend(self, user_id: Optional[str] = None, count: int = 10) -> List[str]:
        """Generate personalized demo recommendations"""
        recommendations = []
        
        if user_id and user_id in self.preferences:
            prefs = self.preferences[user_id]
            # Match user preferences
            for demo in self.demo_catalog:
                score = self._calculate_match_score(demo, prefs)
                if score > 0.7:
                    recommendations.append(demo.platform)
        else:
            # Popular/random recommendations
            recommendations = [
                "commodore_64",
                "commodore_amiga",
                "nintendo_famicom",
                "sega_megadrive",
                "ms-dos",
            ]
        
        return list(set(recommendations))[:count]
    
    def _calculate_match_score(self, demo: DemoVector, prefs: Dict) -> float:
        """Calculate recommendation match score"""
        score = 0.5
        
        if 'preferred_era' in prefs and demo.era.value == prefs['preferred_era']:
            score += 0.3
        
        if 'favorite_features' in prefs:
            overlap = set(demo.features) & set(prefs['favorite_features'])
            score += 0.1 * len(overlap)
        
        return min(score, 1.0)
    
    def _find_demo(self, demo_id: str) -> Optional[DemoVector]:
        """Find demo by ID in catalog"""
        # Placeholder for real lookup
        return self.demo_catalog[0] if demo_id else None
    
    def discover_hidden_gems(self, era: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """Find lesser-known demos matching specified era"""
        hidden_gems = [
            {
                "name": "Fr-Act 94",
                "platform": "commodore_64",
                "era": "8bit_classic",
                "rarity": "rare",
                "reason": "Pure raster magic on 64K"
            },
            {
                "name": "Speedtrap",
                "platform": "ms-dos",
                "era": "pc_power",
                "rarity": "obscure",
                "reason": "Underrated Future Crew production"
            },
            {
                "name": "Pouet.net #21557",
                "platform": "commodore_amiga",
                "era": "amiga_glory",
                "rarity": "hidden",
                "reason": "Minimalist masterpiece"
            }
        ]
        
        if era:
            return [g for g in hidden_gems if g['era'] == era][:limit]
        return hidden_gems[:limit]

# CLI entry point
if __name__ == "__main__":
    import sys
    
    curator = AIDemoCurator()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--hidden-gems":
        gems = curator.discover_hidden_gems(sys.argv[2] if len(sys.argv) > 2 else None)
        for gem in gems:
            print(f"✨ {gem['name']} ({gem['platform']}) - {gem['reason']}")
    elif len(sys.argv) > 1 and sys.argv[1] == "--recommend":
        user_id = sys.argv[2] if len(sys.argv) > 2 else None
        recs = curator.recommend(user_id, 5)
        print("📺 Recommended demos:")
        for r in recs:
            print(f"  - {r}")
    else:
        print("Usage: python3 showet_ai_curator.py [--hidden-gems [era]]")
        print("       python3 showet_ai_curator.py --recommend [user_id]")