#!/usr/bin/env python3
"""Show Flow Director - The central state machine for the entire streaming experience.

This script orchestrates the entire event, managing state transitions, timing,
and inter-module communication:
1.  Setup -> Warmup -> Main Act -> Intermission -> Next Suggestion

Manages:
- OBS Scene Transitions
- Demo Scheduling (PartyCountdown/Scheduler)
- Live Streaming (StreamManager/Relay)
- Contextual Guidance (DemosceneCurator)
- Audio/Visual Overlays (ChatOverlay/DemoInfoOverlay)
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

# Import core components
from demo_database import get_db
from demo_scheduler import DemoScheduler, PartyCountdown
from intelligence_curator import DemosceneCurator
from streaming import StreamManager, StreamConfig, StreamPlatform, QUALITY_PRESETS
from retro_effects import get_preset, CRT_PRESETS
from obs_integration import OBSController, SCENES
from chat_overlay import generate_chat_overlay_html
from demo_recorder import DemoRecorder

class ShowDirector:
    """Manages the state and flow of a complete show."""
    
    def __init__(self, initial_context: str, desired_platform: str = "commodore_64", initial_demo_id: Optional[int] = None):
        self.db = get_db()
        self.curator = DemosceneCurator(context=initial_context)
        self.obs = OBSController()
        self.stream_manager = StreamManager()
        self.recorder = DemoRecorder()
        self.current_platform = desired_platform
        self.current_demo_id = initial_demo_id
        
    def setup_show(self, demo_id: int, platform: str, initial_context: str):
        """Initial setup phase: preparing the OBS and metadata."""
        print("--- [STATE]: SETUP ---")
        
        # 1. Setup OBS
        self.obs.switch_scene(SCENES["setup"])
        print("OBS scene set to 'Setup'. Waiting for visual confirmation...")
        
        # 2. Initialize Stream State
        demo = self.db.get_demo_info(demo_id)
        if "error" in demo:
            print(f"ERROR: Cannot start show. Could not fetch demo info: {demo['error']}")
            return False
            
        # 3. Setup Stream/Graphics
        stream_key = input(f"Enter streaming key for {StreamPlatform(platform).value}: ")
        config = StreamConfig(
            platform=StreamPlatform(platform),
            stream_key=stream_key,
            quality="1080p",
            include_webcam=True,
            overlay_text=f"Showet Demo: {demo['name']} ({platform.upper()})",
        )
        self.stream_manager.configure(config)
        
        # 4. Display Pre-show Info
        self.obs.update_stream_info(demo['name'], platform)
        print("Setup complete. Now transitioning to Warmup...")
        return True

    def run_show(self, demo_id: int):
        """Executes the main show sequence."""
        print("\n=============================================================================")
        print("🎬 STARTING SHOW FLOW DIRECTOR")
        print("=============================================================================")
        
        if not self.setup_show(demo_id, self.current_platform, "The show focuses on pre-1995 tech."):
            return False

        # 1. WARMUP PHASE
        print("\n--- [STATE]: WARMUP ---")
        self.obs.switch_scene(SCENES["waiting"])
        print("OBS scene set to 'Waiting Room'. Playing Hall of Fame Ticker.")
        # Simulation of WebRTC/Chat Overlay running...
        
        # 2. MAIN ACT
        print("\n--- [STATE]: MAIN ACT ---")
        self.obs.switch_scene(SCENES["demo"])
        print("OBS scene transitioned to 'Demo Playback'. Beginning stream.")
        
        # Stream the demo
        self.stream_manager.start(window_id="0")
        print("Streaming active. Playing demo for 30 seconds...")
        time.sleep(30) # Simulate demo playback time
        
        # 3. POST-DEMO (INTERMISSION & CURATION)
        print("\n--- [STATE]: INTERMISSION ---")
        self.obs.switch_scene(SCENES["intermission"])
        print("Demo finished. Displaying intermission screen and running chat overlay.")
        
        # Simulate chat/curator running
        from chat_overlay import generate_chat_overlay_html
        chat_html = generate_chat_overlay_html("twitch", spectator_mode=True)
        print("🌐 Chat overlay displayed. Awaiting viewer comments...")
        
        # Curate the next suggestion
        self.curator.suggest_next_demo(self.current_platform, self.current_demo_id)
        
        # Final cleanup
        self.stream_manager.stop()
        self.obs.switch_scene(SCENES["credits"])
        print("SHOW ENDED. Crew credits shown. Session complete.")

        
# === CLI ENTRY POINT FOR TESTING ===
if __name__ == "__main__":
    print("✨ Show Flow Director Ready!")
    print("Usage: python3 showet_director.py --demo 12345 --platform commodore_64 --context \"The user loves Amiga sci-fi.\"")
    print("\nNOTE: This script requires all other showet modules to be present and functional.")
EOF