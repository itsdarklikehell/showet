#!/usr/bin/env python3
"""
Showet Demo Historical Significance Scoring
Ranks demos for Museum Mode curation based on historical impact
"""

from typing import Dict, List
from datetime import datetime

class DemoScorer:
    def __init__(self):
        self.historical_weight = 0.4  # Era importance
        self.innovation_weight = 0.3  # Technical innovations
        self.cultural_weight = 0.2    # Cultural impact
        self.rating_weight = 0.1      # Community ratings
    
    def score_demo(self, demo: Dict) -> float:
        """Calculate historical significance score (0-100)"""
        year_score = self._score_era(demo.get('year', 2000))
        innovation_score = self._score_innovations(demo.get('tags', []))
        cultural_score = self._score_cultural(demo.get('group', ''))
        rating_score = self._score_rating(demo.get('rank', 0))
        
        total = (
            year_score * self.historical_weight +
            innovation_score * self.innovation_weight +
            cultural_score * self.cultural_weight +
            rating_score * self.rating_weight
        )
        
        return round(total, 2)
    
    def _score_era(self, year: int) -> float:
        """Score based on historical era"""
        if year < 1985:
            return 100.0  # Foundational era
        elif year < 1990:
            return 90.0   # Early scene
        elif year < 1995:
            return 85.0   # Cracktro golden age
        elif year < 2000:
            return 95.0   # Peak AGA/PC era
        elif year < 2005:
            return 80.0   # Modern demo era
        elif year < 2010:
            return 70.0   # Shader emergence
        else:
            return 60.0   # Contemporary work
    
    def _score_innovations(self, tags: List[str]) -> float:
        """Score based on technical innovations"""
        innovation_keywords = {
            'raytracing': 100,
            'photorealistic': 95,
            '3d': 80,
            'procedural': 85,
            'glsl': 75,
            'neural': 90,
            'realtime': 85,
            'procedural_generation': 90
        }
        
        max_score = 50.0  # Base score
        for tag in tags:
            for keyword, score in innovation_keywords.items():
                if keyword in tag.lower():
                    max_score = max(max_score, score)
        
        return max_score
    
    def _score_cultural(self, group: str) -> float:
        """Score based on group cultural impact"""
        legendary_groups = {
            'future crew': 100,
            'farbrausch': 95,
            'conspiracy': 90,
            'fairlight': 85,
            'elite': 80,
            'booze design': 75,
            'sanctuary': 70
        }
        
        group_lower = group.lower()
        for name, score in legendary_groups.items():
            if name in group_lower:
                return score
        
        return 40.0
    
    def _score_rating(self, rank: int) -> float:
        """Score based on competition ranking (0-10)"""
        if rank <= 1:
            return 100.0
        elif rank <= 3:
            return 80.0
        elif rank <= 5:
            return 60.0
        else:
            return 30.0
    
    def rank_demos(self, demos: List[Dict]) -> List[Dict]:
        """Rank demos by historical significance"""
        scored = []
        for demo in demos:
            score = self.score_demo(demo)
            demo['historical_score'] = score
            scored.append(demo)
        
        return sorted(scored, key=lambda d: d['historical_score'], reverse=True)
    
    def get_museum_collection(self, demos: List[Dict], limit: int = 50) -> List[Dict]:
        """Get top demos for Museum Mode collection"""
        ranked = self.rank_demos(demos)
        return ranked[:limit]


# CLI interface
if __name__ == "__main__":
    import json
    import sys
    
    scorer = DemoScorer()
    
    # Sample demo list
    sample_demos = [
        {"name": "Second Reality", "year": 1993, "group": "Future Crew", "rank": 1, "tags": ["raytracing", "3d"]},
        {"name": "Heaven Seven", "year": 2003, "group": "Conspiracy", "rank": 1, "tags": ["photorealistic"]},
        {"name": "Arte", "year": 1991, "group": "Sanctuary", "rank": 2, "tags": ["3d"]},
        {"name": "Elevated", "year": 2004, "group": "Conspiracy", "rank": 1, "tags": ["neural", "glsl"]}
    ]
    
    ranked = scorer.rank_demos(sample_demos)
    
    print("🏛️ Museum Mode Demo Rankings:")
    for demo in ranked:
        print(f"  {demo['historical_score']:>5.1f} - {demo['name']} ({demo['year']}) [{demo['group']}]")
    
    # Output Museum Mode ready JSON
    museum_collection = scorer.get_museum_collection(sample_demos)
    print("\n📋 Museum Mode Collection (top 10):")
    print(json.dumps(museum_collection, indent=2))