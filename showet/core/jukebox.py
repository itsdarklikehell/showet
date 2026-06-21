"""Jukebox module for Showet.

Intelligent demo playback with loop/shuffle/repeat functionality.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import urllib.request
from pathlib import Path
from typing import Any, Optional

from showet.core.config import DEBUG, DEFAULT_TIMEOUT, DEFAULT_LOOP_LIMIT, LOOPED_KEYWORDS

logger = logging.getLogger("showet.jukebox")

# Demo type mappings for loop detection
LOOPED_DEMO_TYPES = frozenset(["64k", "4k", "intro", "wild", "1k", "8k", "dentro", "cracktro"])

# Demo type to estimated duration mapping (seconds)
DEMO_DURATION_ESTIMATES = {
    "32b": 10, "64b": 15, "128b": 20, "256b": 30, "512b": 45,
    "1k": 60, "4k": 120, "8k": 90, "16k": 120, "32k": 150,
    "40k": 180, "64k": 180, "80k": 200, "96k": 220, "100k": 240,
    "128k": 270, "256k": 300, "intro": 90, "demo": 300, "wild": 120,
    "artpack": 180, "slideshow": 150, "cracktro": 60, "dentro": 120,
}


def get_demo_info(pouet_id: int) -> Optional[dict]:
    """Fetch demo metadata from Pouet.net."""
    try:
        url = f"http://api.pouet.net/v1/prod/?id={pouet_id}"
        with urllib.request.urlopen(url, timeout=10) as response:
            import json
            data = json.loads(response.read().decode())
            return data.get("prod")
    except Exception as e:
        logger.error("Failed to fetch demo %d: %s", pouet_id, e)
        return None


def is_looped_demo(demo_info: Optional[dict], source: str = "pouet") -> bool:
    """Detect if a demo loops based on metadata and type.
    
    Uses multiple heuristics:
    - Demo type (64k/4k intros)
    - Tags/keywords (loop, looping)
    - Rating (high-rated intros often loop)
    - File size (smaller files often loop infinitely)
    
    Args:
        demo_info: Demo metadata dictionary
        source: Source identifier (pouet, scene_org, modarchive)
        
    Returns:
        True if demo is likely looped, False otherwise
    """
    if not demo_info:
        return False
    
    rating = demo_info.get("rating", 0)
    demo_type = demo_info.get("type", "").lower()
    tags = demo_info.get("tags", "")
    filename = demo_info.get("name", "").lower()
    size = demo_info.get("size", 0)
    
    # High-rated intros often loop
    if rating and rating > 4.0 and "intro" in demo_type:
        return True
    
    # Check demo type (64k/4k intros)
    if any(t in demo_type for t in LOOPED_DEMO_TYPES):
        return True
    
    # Check tags
    if tags:
        tags_lower = tags.lower()
        for keyword in LOOPED_KEYWORDS:
            if keyword in tags_lower:
                return True
    
    # Check filename for loop indicators (scene.org style)
    loop_patterns = ["loop", "endless", "forever", "replay", "continuous"]
    if any(p in filename for p in loop_patterns):
        return True
    
    # Size heuristic: very small demos (<5MB) often loop infinitely
    if size and size < 5 * 1024 * 1024:
        return True
    
    return False


def estimate_demo_duration(demo_info: Optional[dict], source: str = "pouet") -> int:
    """Estimate demo duration based on type and metadata.
    
    Uses multiple heuristics:
    - Demo type (64k intros are typically 2-3 min)
    - File size (larger files often mean longer demos)
    - Rating (higher rated demos often longer)
    
    Args:
        demo_info: Demo metadata dictionary
        source: Source identifier (pouet, scene_org, modarchive)
        
    Returns:
        Estimated duration in seconds
    """
    if not demo_info:
        return 180
    
    demo_type = demo_info.get("type", "").lower()
    size = demo_info.get("size", 0)
    rating = demo_info.get("rating", 0)
    
    # Check type-based estimates
    for demo_type_key, duration in DEMO_DURATION_ESTIMATES.items():
        if demo_type_key in demo_type:
            # Adjust for rating
            if rating and rating > 4.0:
                duration = int(duration * 1.2)  # Longer for highly rated
            # Adjust for size
            if size and size > 100 * 1024 * 1024:  # > 100MB
                duration = int(duration * 1.5)  # Probably a full demo
            return duration
    
    return 180