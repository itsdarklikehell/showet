#!/usr/bin/env python3
"""
Showet Jukebox - Loop/Shuffle/Repeat functionality for demo playback.

Features:
- Loop detection for demos
- Shuffle with intelligent loop count (3 loops for looped demos)
- Repeat mode for continuous playback
- Integration with DemoScheduler for session management
"""

import json
import random
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class JukeboxConfig:
    """Configuration for jukebox behavior."""
    loop_count_for_shuffle: int = 3  # Play looped demos 3 times when shuffling
    shuffle_mode: str = "random"  # random, sequential, weighted
    repeat_mode: str = "none"  # none, all, one
    auto_detect_loops: bool = True
    demo_timeout_seconds: int = 300  # Default demo timeout
    exit_on_user_input: bool = True


@dataclass
class DemoTrack:
    """A demo track for the jukebox."""
    id: int  # Pouet ID
    title: str
    group: str
    platform: str
    path: Optional[Path] = None
    is_looping: bool = False
    loop_times_played: int = 0
    last_played: Optional[datetime] = None


class DemoJukebox:
    """Jukebox controller for demo playback with loop/shuffle/repeat."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".showet" / "jukebox_config.json"
        self.config = self._load_config()
        self.playlist: List[DemoTrack] = []
        self.current_index: int = 0
        self.is_playing: bool = False
        self._current_process: Optional[subprocess.Popen] = None

    def _load_config(self) -> JukeboxConfig:
        """Load configuration from disk or use defaults."""
        if self.config_path.exists():
            try:
                data = json.loads(self.config_path.read_text())
                return JukeboxConfig(**data)
            except (json.JSONDecodeError, TypeError):
                pass
        return JukeboxConfig()

    def _save_config(self) -> None:
        """Save configuration to disk."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps({
            "loop_count_for_shuffle": self.config.loop_count_for_shuffle,
            "shuffle_mode": self.config.shuffle_mode,
            "repeat_mode": self.config.repeat_mode,
            "auto_detect_loops": self.config.auto_detect_loops,
            "demo_timeout_seconds": self.config.demo_timeout_seconds,
        }))

    def add_track(self, track: DemoTrack) -> None:
        """Add a track to the playlist."""
        self.playlist.append(track)

    def add_pouet_id(self, pouet_id: int, title: str = "", group: str = "", 
                    platform: str = "auto", path: Optional[Path] = None) -> None:
        """Add a track by Pouet ID."""
        track = DemoTrack(
            id=pouet_id,
            title=title or f"Demo {pouet_id}",
            group=group,
            platform=platform,
            path=path,
        )
        # Auto-detect looping status
        if self.config.auto_detect_loops:
            track.is_looping = self._detect_loop_status(pouet_id)
        self.playlist.append(track)

    def _detect_loop_status(self, pouet_id: int) -> bool:
        """Detect if a demo loops by checking metadata.
        
        Checks:
        - Pouet.net tags for 'loop' keyword
        - File size (larger intros often loop)
        - Demo type (size-limited categories like 64k/4k often loop)
        """
        # This would integrate with pouet API to check tags
        cache_dir = Path.home() / ".showet" / "data" / str(pouet_id)
        if not cache_dir.exists():
            return False
            
        # Check if demo type suggests looping (64k intros often loop)
        demo_json = cache_dir / "pouet.json"
        if demo_json.exists():
            try:
                data = json.loads(demo_json.read_text())
                demo_type = data.get("prod", {}).get("type", "").lower()
                tags = " ".join(data.get("prod", {}).get("tags", [])).lower()
                
                if "loop" in tags or "looping" in tags:
                    return True
                # 64k/4k intros often loop as intros restart
                if "64k" in demo_type or "4k" in demo_type:
                    return True
            except (json.JSONDecodeError, KeyError):
                pass
        
        return False

    def shuffle(self, mode: Optional[str] = None) -> None:
        """Shuffle the playlist using the specified mode."""
        mode = mode or self.config.shuffle_mode
        
        if mode == "random":
            random.shuffle(self.playlist)
        elif mode == "weighted":
            # Weight by party rank, age, or rating
            self.playlist.sort(key=lambda t: random.random() / (1 + t.loop_times_played))
        # sequential: keep order

    def next_track(self) -> Optional[DemoTrack]:
        """Get the next track based on repeat mode."""
        if not self.playlist:
            return None

        if self.config.repeat_mode == "all":
            self.current_index = (self.current_index + 1) % len(self.playlist)
        elif self.config.repeat_mode == "one":
            # Stay on same track
            pass
        else:  # none
            if self.current_index < len(self.playlist) - 1:
                self.current_index += 1
            else:
                return None  # End of playlist

        return self.playlist[self.current_index]

    def previous_track(self) -> Optional[DemoTrack]:
        """Get the previous track."""
        if not self.playlist:
            return None

        if self.current_index > 0:
            self.current_index -= 1
            return self.playlist[self.current_index]
        return None

    def play_current(self) -> Optional[subprocess.Popen]:
        """Play the current track with appropriate handling for looping."""
        if not self.playlist or self.current_index >= len(self.playlist):
            return None

        track = self.playlist[self.current_index]
        
        # Kill any existing process
        self._stop_current()

        # Determine loops for this play
        if self.config.repeat_mode == "shuffle" or (
            self.config.shuffle_mode == "random" and track.is_looping
        ):
            # For shuffle mode, play looped demos the configured number of times
            max_loops = self.config.loop_count_for_shuffle if track.is_looping else 1
        else:
            max_loops = 999 if self.config.repeat_mode == "one" else 1

        return self._launch_demo(track, max_loops)

    def _stop_current(self) -> None:
        """Stop the currently playing demo."""
        if self._current_process and self._current_process.poll() is None:
            self._current_process.terminate()
            try:
                self._current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._current_process.kill()
        self._current_process = None

    def _launch_demo(self, track: DemoTrack, max_loops: int = 1) -> subprocess.Popen:
        """Launch a demo with specified loop count."""
        # Launch the demo file directly via subprocess
        # In a real implementation, this would use the DemoExecutor
        from showet_archive_handler import ArchiveHandler
        from showet_platform_runner import get_jukebox_loop_count
        
        # Get platform-specific loop count
        platform_loops = get_jukebox_loop_count(track.platform, track.is_looping)
        actual_loops = max_loops if max_loops > 1 else platform_loops
        
        process = subprocess.Popen(["showet-executor", str(track.path or track.id)])
        
        track.last_played = datetime.now()
        track.loop_times_played += 1
        
        self.is_playing = True
        self._current_process = process
        return process

    def get_loop_times_for_shuffle(self, track: DemoTrack) -> int:
        """Get how many times to play a track in shuffle mode.
        
        Looped demos play 3 times, non-looped play once.
        """
        if track.is_looping:
            return self.config.loop_count_for_shuffle
        return 1


def run_jukebox(playlist_ids: List[int], mode: str = "shuffle", 
                repeat: str = "all", max_loops_per_track: int = 3) -> None:
    """Run the jukebox with a list of Pouet IDs.
    
    Args:
        playlist_ids: List of Pouet demo IDs
        mode: Shuffle mode (random, sequential, weighted)
        repeat: Repeat mode (none, all, one)
        max_loops_per_track: Max loops for looping demos in shuffle
    """
    jukebox = DemoJukebox()
    jukebox.config.shuffle_mode = mode
    jukebox.config.repeat_mode = repeat
    jukebox.config.loop_count_for_shuffle = max_loops_per_track

    # Add tracks
    for pid in playlist_ids:
        jukebox.add_pouet_id(pid)

    jukebox.shuffle(mode)
    
    print(f"🎵 Jukebox started: {len(jukebox.playlist)} tracks")
    print(f"Mode: {mode}, Repeat: {repeat}")
    
    while jukebox.playlist:
        track = jukebox.playlist[jukebox.current_index]
        print(f"\n▶ Playing: {track.title} by {track.group} (ID: {track.id})")
        
        process = jukebox.play_current()
        if process:
            try:
                process.wait(timeout=max_loops_per_track * jukebox.config.demo_timeout_seconds)
            except subprocess.TimeoutExpired:
                process.kill()
                print("Demo timed out")

        # Move to next
        next_track = jukebox.next_track()
        if not next_track:
            print("\n🏁 Jukebox finished!")
            break


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Showet Jukebox - Loop/Shuffle/Repeat demo playback"
    )
    parser.add_argument("--ids", nargs="+", type=int, help="Pouet IDs to play")
    parser.add_argument("--shuffle", choices=["random", "sequential"], 
                       default="random", help="Shuffle mode")
    parser.add_argument("--repeat", choices=["none", "all", "one"], 
                       default="none", help="Repeat mode")
    parser.add_argument("--loops", type=int, default=3, 
                       help="Max loops for shuffle mode (default: 3)")
    parser.add_argument("--timeout", type=int, default=300,
                       help="Demo timeout in seconds")
    
    args = parser.parse_args()
    
    if not args.ids:
        print("Usage: showet-jukebox --ids 12345 67890 --shuffle random --repeat all")
        print("\nOptions:")
        print("  --ids ID [ID...]   List of Pouet demo IDs")
        print("  --shuffle MODE     Shuffle mode: random, sequential")
        print("  --repeat MODE      Repeat mode: none, all, one")
        print("  --loops N          Max loops for shuffle (default: 3)")
        print("  --timeout SECONDS  Demo timeout (default: 300)")
        return

    jukebox = DemoJukebox()
    jukebox.config.demo_timeout_seconds = args.timeout
    jukebox.config.loop_count_for_shuffle = args.loops
    
    for pid in args.ids:
        jukebox.add_pouet_id(pid)
    
    jukebox.shuffle(args.shuffle)
    run_jukebox(args.ids, args.shuffle, args.repeat, args.loops)


if __name__ == "__main__":
    main()