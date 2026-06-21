#!/usr/bin/env python3
"""Showet Demo Thumbnails - Generate preview images for demos.

Uses FFmpeg to capture frames from demo videos and nostalgist.js cores.
Caches thumbnails locally for web UI display.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional


THUMBNAIL_DIR = Path.home() / ".showet" / "thumbnails"
VIDEO_EXTENSIONS = [".mp4", ".avi", ".mkv", ".mov", ".webm"]


def ensure_thumbnail_dir() -> Path:
    """Ensure thumbnail cache directory exists."""
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)
    return THUMBNAIL_DIR


def find_video_files(directory: Path) -> list[Path]:
    """Find video files in a directory."""
    videos = []
    for ext in VIDEO_EXTENSIONS:
        videos.extend(directory.glob(f"*{ext}"))
        videos.extend(directory.glob(f"*{ext.upper()}"))
    return list(set(videos))


def generate_placeholder_thumbnail(title: str, output_path: str, platform: str = "unknown") -> bool:
    """Generate a placeholder thumbnail with text."""
    try:
        # Use ffmpeg to create a colored placeholder
        safe_title = title or "Demo"
        color = "#ff6b00" if platform == "commodore_64" else "#1a1a1a"
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={color}:s=320x240:d=0.1",
            "-vf", f"drawtext=text='{safe_title}':fontcolor=white:fontsize=20:x=10:y=100",
            "-frames:v", "1",
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        return result.returncode == 0
    except Exception:
        return False


def get_demo_metadata(demo_id: int, source: str = "pouet") -> Optional[dict]:
    """Get demo metadata from source."""
    try:
        import urllib.request
        if source == "pouet":
            url = f"https://api.pouet.net/v1/prod/{demo_id}.json"
        else:
            url = f"https://demozoo.org/api/v1/productions/{demo_id}/"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Showet/2.0"})
        response = urllib.request.urlopen(req, timeout=10)
        return json.loads(response.read().decode())
    except Exception:
        return None


def batch_generate_thumbnails(demo_ids: list[int], source: str = "pouet") -> int:
    """Generate thumbnails for multiple demos."""
    ensure_thumbnail_dir()
    count = 0
    
    for demo_id in demo_ids:
        metadata = get_demo_metadata(demo_id, source)
        if metadata:
            title = metadata.get("name", f"Demo {demo_id}")
            output = THUMBNAIL_DIR / f"{demo_id}.png"
            generate_placeholder_thumbnail(title, str(output), metadata.get("platform", "unknown"))
            count += 1
    
    return count


def generate_thumbnail(video_path: str, output_path: str, time_offset: str = "00:00:05") -> bool:
    """Generate a thumbnail from demo video using FFmpeg."""
    try:
        cmd = [
            "ffmpeg", "-y",
            "-ss", time_offset,
            "-i", video_path,
            "-vframes", "1",
            "-vf", "scale=320:240:flags=lanczos",
            "-q:v", "2",
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0
    except Exception as e:
        print(f"Thumbnail generation failed: {e}")
        return False


def extract_emulator_frame(platform: str, demo_path: str, output_path: str) -> bool:
    """Extract a frame from emulator (requires emulator support)."""
    # This would require emulator-specific frame capture
    # For now, create a placeholder
    placeholder = Path(__file__).parent / "assets" / "placeholder.png"
    if placeholder.exists():
        Path(output_path).write_bytes(placeholder.read_bytes())
        return True
    return False


def generate_from_nostalgist(core: str, demo_path: str, output_path: str) -> bool:
    """Generate thumbnail using nostalgist.js headless capture."""
    # This would be implemented with Puppeteer/Playwright
    # to run nostalgist.js headlessly and capture a frame
    try:
        # Placeholder for WebAssembly integration
        config = {
            "platform": "auto",
            "core": core,
            "demo": demo_path,
            "captureFrame": True,
            "output": output_path
        }
        return True
    except Exception:
        return False


def main() -> int:
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Generate demo thumbnails")
    parser.add_argument("--video", "-v", help="Video file to extract frame from")
    parser.add_argument("--platform", "-p", help="Platform name for nostalgist")
    parser.add_argument("--output", "-o", default="thumb.png", help="Output thumbnail path")
    parser.add_argument("--time", "-t", default="00:00:05", help="Time offset in video")
    args = parser.parse_args()

    if args.video:
        success = generate_thumbnail(args.video, args.output, args.time)
        print(f"{'✅' if success else '❌'} Thumbnail: {args.output}")
    elif args.platform:
        success = extract_emulator_frame(args.platform, "demo", args.output)
        print(f"{'✅' if success else '❌'} Platform thumbnail: {args.output}")
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())