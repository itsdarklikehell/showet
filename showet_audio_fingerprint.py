#!/usr/bin/env python3
"""Showet Audio Fingerprinting - Module format detection and loop analysis.

Analyzes demo audio modules (MOD, S3M, XM, IT) for format detection
and loop point identification to improve jukebox mode.
"""

from __future__ import annotations

from pathlib import Path


# Module format magic bytes
MODULE_SIGNATURES = {
    b"M.K.": "protracker",      # ProTracker MOD
    b"M!K!": "protracker",     # ProTracker MOD (alternate)
    b"FLT4": "star_trekker",   # Star Trekker MOD
    b"4CHN": "fasttracker",    # FastTracker MOD
    b"6CHN": "fasttracker",    # FastTracker 6-channel
    b"8CHN": "fasttracker",    # FastTracker 8-channel
    b"S3M": "s3m",             # Scream Tracker 3
    b"XM": "xm",                # FastTracker 2 Extended Module
    b"#ivo": "it",              # Impulse Tracker
}

# Loop pattern heuristics
LOOP_PATTERNS = {
    "protracker": ["loop", "repeat", "forever", "break", "endless"],
    "s3m": ["loop", "pattern", "order"],
    "xm": ["loop", "phrase", "pattern"],
    "it": ["loop", "row", "break"],
}


def detect_module_format(file_path: str) -> dict:
    """Detect module format from file header."""
    path = Path(file_path)
    if not path.exists() or path.stat().st_size < 1084:
        return {"format": "unknown", "confidence": 0}

    with open(path, "rb") as f:
        header = f.read(1084)

    # Check for ProTracker MOD signature
    if len(header) >= 1080:
        sig = header[1080:1084]
        for magic, fmt in MODULE_SIGNATURES.items():
            if sig.startswith(magic) or sig == magic:
                return {
                    "format": fmt,
                    "type": "mod",
                    "confidence": 0.95,
                    "channels": int(sig[0:2]) if sig[0:2].isdigit() else 4,
                }

    # Check for S3M signature
    if header[44:47] == b"S3M":
        return {"format": "s3m", "type": "s3m", "confidence": 0.9}

    # Check for XM signature
    if header[0:2] == b"XM":
        return {"format": "xm", "type": "xm", "confidence": 0.9}

    # Check for IT signature
    if header[0:4] == b"#ivo":
        return {"format": "it", "type": "it", "confidence": 0.9}

    return {"format": "unknown", "confidence": 0}


def analyze_loop_points(file_path: str, module_format: str) -> dict:
    """Analyze module for loop points using heuristics."""
    path = Path(file_path)
    if not path.exists():
        return {}

    scores = {
        "has_loop_pattern": False,
        "estimated_loop_frames": 0,
        "loop_tendency": 0.0,
        "pattern_count": 0,
    }

    # Try to read module name from header
    try:
        with open(path, "rb") as f:
            header = f.read(30)
            if len(header) >= 20:
                name_field = header[0:20]
                # Check for loop keywords in module name
                name = name_field.decode("utf-8", errors="ignore").lower()
                patterns = LOOP_PATTERNS.get(module_format, [])
                scores["has_loop_pattern"] = any(p in name for p in patterns)
    except Exception:
        pass

    return scores


def get_module_info(path: str) -> dict:
    """Get comprehensive module information."""
    fmt = detect_module_format(path)
    if fmt["confidence"] > 0:
        loops = analyze_loop_points(path, fmt["format"])
        fmt.update(loops)
    return fmt


def main() -> int:
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Analyze demo modules")
    parser.add_argument("--detect", "-d", help="Detect module format")
    parser.add_argument("--analyze", "-a", help="Full analysis")
    parser.add_argument("--file", "-f", help="Module file path")
    args = parser.parse_args()

    if args.detect:
        info = detect_module_format(args.detect)
        print(f"Format: {info['format']} (confidence: {info['confidence']:.0%})")
    elif args.analyze:
        info = get_module_info(args.analyze)
        for k, v in info.items():
            print(f"  {k}: {v}")
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())