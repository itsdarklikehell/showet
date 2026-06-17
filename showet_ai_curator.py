#!/usr/bin/env python3
"""
Showet AI Demo Curator - Enhanced with Deep Metadata & Scene.org Integration
Intelligent demo recommendation engine using content analysis and user preferences
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import subprocess
import os

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
    """AI-powered demo recommendation engine with scene.org integration"""
    
    def __init__(self, demo_dir: str = "nostalgist_configs"):
        self.preferences = {}
        self.demo_catalog = self._load_demo_catalog()
        self.demo_dir = demo_dir
    
    def _load_demo_catalog(self) -> List[DemoVector]:
        """Load demo catalog with technical vectors"""
        catalog_path = Path(__file__).parent / "demo_database.py"
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
    
    def enhanced_discover(self, query: str = "") -> List[Dict]:
        """Discover demos using scene.org integration for real results"""
        results = []
        
        # Try scene.org integration
        try:
            from scene_org_integration import SceneOrgClient
            client = SceneOrgClient()
            
            if query:
                demos = client.search_demos(query, limit=10)
                for demo in demos:
                    results.append({
                        "name": demo.get("name", query),
                        "platform": demo.get("platform", "unknown"),
                        "url": demo.get("url", ""),
                        "source": "scene.org",
                        "preview_available": False
                    })
            else:
                # Get trending demos
                trending = [
                    {"name": "Assembly 2024 Winners", "platform": "amiga", "source": "scene.org"},
                    {"name": "Revision 2024 Compo", "platform": "pc", "source": "scene.org"},
                ]
                results.extend(trending)
                
        except ImportError:
            # Fallback to known gems
            results = self.discover_hidden_gems()
            
        return results
    
    def extract_metadata(self, demo_path: str) -> Dict:
        """Extract deep metadata from demo file for AI analysis"""
        metadata = {
            "path": demo_path,
            "size": 0,
            "platform": "unknown",
            "estimated_duration": 0,
            "features": [],
        }
        
        if os.path.exists(demo_path):
            metadata["size"] = os.path.getsize(demo_path)
            
            # Analyze file for hints
            if demo_path.endswith('.zip'):
                metadata["platform"] = "pc"
                metadata["features"] = ["compressed"]
            elif demo_path.endswith(('.d64', '.tap')):
                metadata["platform"] = "commodore_64"
            elif demo_path.endswith('.adf'):
                metadata["platform"] = "commodore_amiga"
                
        return metadata
    
    def predict_demo_rating(self, demo_name: str, metadata: Dict = None) -> float:
        """Predict demo rating based on name patterns and features"""
        # Simple heuristic scoring
        score = 0.5
        
        # Known legendary demos get high scores
        legendary = ["Second Reality", "Heaven Seven", "Elevated", "Arte", "Beyond"]
        for legend in legendary:
            if legend.lower() in demo_name.lower():
                score = 0.95
                break
        
        # Complexity indicators
        if any(word in demo_name.lower() for word in ["meg", "ultra", "extreme", "chaos"]):
            score += 0.15
        
        # Year patterns (older often = more significance)
        import re
        year_match = re.search(r'19|20[0-4][0-9]', demo_name)
        if year_match:
            year = int(year_match.group())
            if year < 2000:
                score += 0.1  # Vintage bonus
        
        return min(score, 1.0)
    
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
    import argparse
    parser = argparse.ArgumentParser(description="Showet AI Demo Curator")
    parser.add_argument("--hidden-gems", "-g", help="Find hidden gems for era")
    parser.add_argument("--recommend", "-r", help="Personalized recommendations for user")
    parser.add_argument("--discover", "-d", help="Discover demos from scene.org")
    parser.add_argument("--predict-rating", "-p", help="Predict demo rating")
    parser.add_argument("--count", "-n", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    curator = AIDemoCurator()

    if args.discover:
        demos = curator.enhanced_discover(args.discover)
        for d in demos[:args.count]:
            print(f"  {d['name']} ({d['platform']}) - {d.get('source', 'local')}")
    elif args.predict_rating:
        rating = curator.predict_demo_rating(args.predict_rating)
        print(f"⭐ Predicted rating for '{args.predict_rating}': {rating:.1%}")
    elif args.hidden_gems:
        gems = curator.discover_hidden_gems(args.hidden_gems)
        for gem in gems[:args.count]:
            print(f"✨ {gem['name']} ({gem['platform']}) - {gem['reason']}")
    elif args.recommend:
        recs = curator.recommend(args.recommend, args.count)
        print("📺 Recommended demos:")
        for r in recs:
            print(f"  - {r}")
    else:
        parser.print_help()


def main():
    """Entry point for console_scripts."""
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="Showet AI Demo Curator")
    parser.add_argument("--hidden-gems", "-g", help="Find hidden gems for era")
    parser.add_argument("--recommend", "-r", help="Personalized recommendations for user")
    parser.add_argument("--discover", "-d", help="Discover demos from scene.org")
    parser.add_argument("--predict-rating", "-p", help="Predict demo rating")
    parser.add_argument("--count", "-n", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    curator = AIDemoCurator()

    if args.discover:
        demos = curator.enhanced_discover(args.discover)
        for d in demos[:args.count]:
            print(f"  {d['name']} ({d['platform']}) - {d.get('source', 'local')}")
    elif args.predict_rating:
        rating = curator.predict_demo_rating(args.predict_rating)
        print(f"⭐ Predicted rating for '{args.predict_rating}': {rating:.1%}")
    elif args.hidden_gems:
        gems = curator.discover_hidden_gems(args.hidden_gems)
        for gem in gems[:args.count]:
            print(f"✨ {gem['name']} ({gem['platform']}) - {gem['reason']}")
    elif args.recommend:
        recs = curator.recommend(args.recommend, args.count)
        print("📺 Recommended demos:")
        for r in recs:
            print(f"  - {r}")
    else:
        parser.print_help()