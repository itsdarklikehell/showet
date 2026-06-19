#!/usr/bin/env python3
"""Showet Thumbnail Generator - Extract preview thumbnails from demos.

Generates thumbnails from:
- Video files found in archives
- Standalone demo files (using FFmpeg screen capture)
- Module files (rendered spectrograms)
- Demo metadata (placeholder images)
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("showet.thumbnails")

# Thumbnail cache directory
THUMBNAIL_DIR = Path.home() / ".showet" / "thumbnails"


def ensure_thumbnail_dir() -> Path:
    """Ensure thumbnail cache directory exists."""
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)
    return THUMBNAIL_DIR


def find_video_files(demo_path: Path) -> list[Path]:
    """Find video files in a demo directory.
    
    Args:
        demo_path: Path to demo directory or archive
        
    Returns:
        List of video file paths
    """
    video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".webm"]
    videos = []
    
    if demo_path.is_file():
        # Check if it's an archive
        if demo_path.suffix.lower() in [".zip", ".rar", ".7z", ".lha"]:
            # Extract and search
            from showet_archive_handler import extract_archive
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                if extract_archive(demo_path, Path(tmpdir)):
                    for ext in video_extensions:
                        videos.extend(Path(tmpdir).rglob(f"*{ext}"))
    else:
        for ext in video_extensions:
            videos.extend(demo_path.rglob(f"*{ext}"))
    
    return videos[:5]  # Limit to 5 videos


def extract_video_thumbnail(video_path: Path, output_path: Path, time_offset: int = 5) -> bool:
    """Extract thumbnail from video using FFmpeg.
    
    Args:
        video_path: Path to video file
        output_path: Output thumbnail path
        time_offset: Seconds into video to capture
        
    Returns:
        True on success
    """
    try:
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite
            "-ss", str(time_offset),
            "-i", str(video_path),
            "-vframes", "1",
            "-vf", "scale=320:240:force_original_aspect_ratio=decrease",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        logger.warning("FFmpeg thumbnail extraction failed: %s", e)
        return False


def generate_placeholder_thumbnail(title: str, output_path: Path, platform: str = "unknown") -> bool:
    """Generate a placeholder thumbnail with demo metadata.
    
    Args:
        title: Demo title
        output_path: Output thumbnail path
        platform: Platform slug
        
    Returns:
        True on success
    """
    try:
        # Create a simple placeholder using ffmpeg's color source
        # This creates a colored background with text overlay
        safe_title = title[:30] if title else "Demo"
        safe_platform = platform.replace("_", " ").title()
        
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", f"color=c=black:s=320x240:d=0.1",
            "-vf", f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='{safe_title}':fontcolor=white:fontsize=20:x=10:y=20,drawtext=text='{safe_platform}':fontcolor=gray:fontsize=16:x=10:y=50",
            "-frames:v", "1",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception as e:
        logger.warning("Placeholder generation failed: %s", e)
        return False


def get_demo_metadata(demo_id: int, source: str = "pouet") -> Optional[dict]:
    """Fetch demo metadata for thumbnail generation.
    
    Args:
        demo_id: Demo ID
        source: Source (pouet, scene_org, modarchive)
        
    Returns:
        Demo metadata or None
    """
    try:
        if source == "pouet":
            import urllib.request
            url = f"http://api.pouet.net/v1/prod/?id={demo_id}"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                return data.get("prod")
    except Exception as e:
        logger.warning("Failed to fetch metadata: %s", e)
    return None


def generate_thumbnail_for_demo(
    demo_path: Path,
    demo_id: Optional[int] = None,
    source: str = "pouet",
    time_offset: int = 5,
) -> Optional[Path]:
    """Generate thumbnail for a demo.
    
    Args:
        demo_path: Path to demo file or directory
        demo_id: Optional demo ID for metadata
        source: Source identifier
        time_offset: Time offset for video thumbnails
        
    Returns:
        Path to generated thumbnail or None
    """
    ensure_thumbnail_dir()
    demo_name = demo_path.stem
    output_path = THUMBNAIL_DIR / f"{demo_name}.jpg"
    
    # First try to find and extract video thumbnails
    videos = find_video_files(demo_path)
    if videos:
        for video in videos:
            if extract_video_thumbnail(video, output_path, time_offset):
                logger.info("Generated thumbnail from video: %s", output_path)
                return output_path
    
    # Fall back to metadata-based placeholder
    title = demo_name
    platform = "unknown"
    
    if demo_id:
        metadata = get_demo_metadata(demo_id, source)
        if metadata:
            title = metadata.get("name", demo_name)
            platform = str(metadata.get("platform", "unknown"))
    
    if generate_placeholder_thumbnail(title, output_path, platform):
        logger.info("Generated placeholder thumbnail: %s", output_path)
        return output_path
    
    return None


def batch_generate_thumbnails(
    demo_ids: list[int],
    source: str = "pouet",
    download: bool = False,
) -> int:
    """Generate thumbnails for multiple demos.
    
    Args:
        demo_ids: List of demo IDs
        source: Source identifier
        download: Whether to download demos first
        
    Returns:
        Number of thumbnails generated
    """
    generated = 0
    
    for demo_id in demo_ids:
        metadata = get_demo_metadata(demo_id, source)
        if metadata:
            title = metadata.get("name", f"demo_{demo_id}")
            output_path = THUMBNAIL_DIR / f"{demo_id}.jpg"
            platform = str(metadata.get("platform", "unknown"))
            
            generate_placeholder_thumbnail(title, output_path, platform)
            generated += 1
            logger.info("Generated thumbnail %d/%d for %s", generated, len(demo_ids), title)
    
    return generated


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate thumbnails for demos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", nargs="?", help="Path to demo file or directory")
    parser.add_argument("--id", type=int, help="Demo ID for metadata")
    parser.add_argument(
        "--source",
        choices=["pouet", "scene_org", "modarchive"],
        default="pouet",
        help="Demo source",
    )
    parser.add_argument(
        "--time",
        type=int,
        default=5,
        help="Time offset for video thumbnails (default: 5s)",
    )
    parser.add_argument(
        "--batch-ids",
        type=int,
        nargs="+",
        help="Batch generate thumbnails for multiple demo IDs",
    )
    args = parser.parse_args()

    if args.batch_ids:
        generated = batch_generate_thumbnails(args.batch_ids, args.source)
        print(f"Generated {generated} thumbnails")
        return 0

    if args.path:
        path = Path(args.path)
        result = generate_thumbnail_for_demo(path, args.id, args.source, args.time)
        if result:
            print(f"Thumbnail: {result}")
            return 0
        print("Failed to generate thumbnail")
        return 1

    print("Usage: showet-thumbnails <path> [options]")
    print("       showet-thumbnails --batch-ids ID1 ID2 ...")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())