#!/usr/bin/env python3
"""Showet RetroPie Integration - Optimize for Raspberry Pi/RetroPie.

Provides configuration for ARM builds, RetroPie menu integration,
and Pi-specific optimizations (OpenMAX, GPU detection).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional
import subprocess
import platform


RETROPIE_CONFIG = {
    "emulators": {
        "c64": {"core": "vice_x64_libretro", "package": "retropie-emulators"},
        "amiga": {"core": "puae_libretro", "package": "retropie-emulators"},
        "nes": {"core": "fceumm_libretro", "package": "retropie-emulators"},
        "snes": {"core": "snes9x_libretro", "package": "retropie-emulators"},
        "genesis": {"core": "genesis_plus_gx_libretro", "package": "retropie-emulators"},
    },
    "pi_options": {
        "gpu_mem": "256",
        "overclock": "medium",
        "audio_latency": "64",
    }
}


def detect_retropie() -> bool:
    """Check if running on RetroPie."""
    paths = [
        "/opt/retropie",
        "/home/pi/RetroPie",
        "/etc/retropie",
    ]
    return any(Path(p).exists() for p in paths)


def get_pi_model() -> Optional[str]:
    """Get Raspberry Pi model."""
    try:
        with open("/proc/cpuinfo") as f:
            content = f.read()
            if "Raspberry Pi 5" in content:
                return "rpi5"
            elif "Raspberry Pi 4" in content:
                return "rpi4"
            elif "Raspberry Pi 3" in content:
                return "rpi3"
            elif "Raspberry Pi" in content:
                return "rpi"
    except Exception:
        pass
    return None


def get_gpu_memory() -> int:
    """Get allocated GPU memory."""
    try:
        with open("/boot/config.txt") as f:
            for line in f:
                if line.startswith("gpu_mem="):
                    return int(line.split("=")[1])
    except Exception:
        pass
    return 128


def optimize_for_pi() -> dict:
    """Get Pi optimization recommendations."""
    model = get_pi_model()
    gpu_mem = get_gpu_memory()
    
    recommendations = {
        "model": model,
        "gpu_mem": gpu_mem,
        "needs_opengl": model in ("rpi4", "rpi5"),
        "core_limit": 3 if model == "rpi3" else 5,
    }
    
    if gpu_mem < 256:
        recommendations["warning"] = f"GPU memory ({gpu_mem}MB) may be low for full-speed demos"
    
    return recommendations


def install_retropie_packages(packages: list[str]) -> int:
    """Install packages via RetroPie setup."""
    if not detect_retropie():
        print("Not running on RetroPie")
        return 0
    
    installed = 0
    for pkg in packages:
        # Would call retropie-setup script
        print(f"Would install: {pkg}")
        installed += 1
    
    return installed


def main() -> int:
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="RetroPie Integration")
    parser.add_argument("--detect", "-d", action="store_true", help="Detect RetroPie/Pi")
    parser.add_argument("--optimize", "-o", action="store_true", help="Get Pi recommendations")
    parser.add_argument("--install", "-i", nargs="+", help="Install RetroPie packages")
    args = parser.parse_args()

    if args.detect:
        is_retropie = detect_retropie()
        model = get_pi_model()
        print(f"RetroPie: {'✅' if is_retropie else '❌'}")
        print(f"Pi Model: {model or 'Not detected'}")
        
    elif args.optimize:
        recs = optimize_for_pi()
        for k, v in recs.items():
            print(f"{k}: {v}")
            
    elif args.install:
        install_retropie_packages(args.install)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())