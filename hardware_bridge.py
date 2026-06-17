#!/usr/bin/env python3
"""
Showet Hardware Encoder Bridge
VAAPI/V4L2 integration for low-latency, production-quality streaming
"""

import subprocess
import asyncio
from pathlib import Path
from typing import Optional, List
import os

class HardwareEncoderBridge:
    """Hardware-accelerated video encoding for demo streaming"""
    
    def __init__(self):
        self.vaapi_available = self._check_vaapi()
        self.v4l2_available = self._check_v4l2()
        self.current_encoder = None
    
    def _check_vaapi(self) -> bool:
        """Check if VAAPI is available (Intel/AMD GPU encoding)"""
        try:
            result = subprocess.run(
                [' vainfo'],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _check_v4l2(self) -> bool:
        """Check if V4L2 is available (Linux video capture)"""
        return Path('/dev/video0').exists()
    
    def build_ffmpeg_command(
        self,
        input_source: str = "x11grab",
        output_url: str = "rtmp://localhost/live/stream",
        encoder: str = "vaapi",
        quality: str = "medium"
    ) -> List[str]:
        """Build ffmpeg command with hardware encoding"""
        
        if encoder == "vaapi" and self.vaapi_available:
            return self._build_vaapi_command(input_source, output_url, quality)
        elif encoder == "v4l2" and self.v4l2_available:
            return self._build_v4l2_command(input_source, output_url, quality)
        else:
            return self._build_software_fallback(input_source, output_url, quality)
    
    def _build_vaapi_command(self, input_source: str, output_url: str, quality: str) -> List[str]:
        """VAAPI Intel/AMD hardware encoding"""
        bitrate_map = {
            "low": "2M",
            "medium": "4M", 
            "high": "8M",
            "ultra": "16M"
        }
        bitrate = bitrate_map.get(quality, "4M")
        
        return [
            'ffmpeg',
            '-hwaccel', 'vaapi',
            '-hwaccel_device', '/dev/dri/renderD128',
            '-i', ':0.0' if input_source == "x11grab" else input_source,
            '-vf', 'format=nv12,hwupload,scale_vaapi=1280:720',
            '-c:v', 'h264_vaapi',
            '-b:v', bitrate,
            '-f', 'flv',
            output_url
        ]
    
    def _build_v4l2_command(self, input_source: str, output_url: str, quality: str) -> List[str]:
        """V4L2 direct camera/video device capture"""
        bitrate_map = {"low": "2000k", "medium": "4000k", "high": "8000k", "ultra": "16000k"}
        bitrate = bitrate_map.get(quality, "4000k")
        
        return [
            'ffmpeg',
            '-f', 'v4l2',
            '-video_size', '1280x720',
            '-i', '/dev/video0',
            '-c:v', 'h264_v4l2m2m',
            '-b:v', bitrate,
            '-f', 'flv',
            output_url
        ]
    
    def _build_software_fallback(self, input_source: str, output_url: str, quality: str) -> List[str]:
        """Software fallback for systems without hardware encoding"""
        bitrate_map = {"low": "2000k", "medium": "4000k", "high": "8000k", "ultra": "16000k"}
        bitrate = bitrate_map.get(quality, "4000k")
        
        return [
            'ffmpeg',
            '-f', 'x11grab' if input_source == "x11grab" else 'gdigrab',
            '-video_size', '1280x720',
            '-i', ':0.0',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-b:v', bitrate,
            '-f', 'flv',
            output_url
        ]
    
    async def start_stream(
        self,
        platform: str,
        demo_id: Optional[int] = None,
        output_url: str = "rtmp://localhost/live/showet",
        quality: str = "medium"
    ):
        """Start hardware-accelerated streaming session"""
        
        cmd = self.build_ffmpeg_command(
            input_source="x11grab",
            output_url=output_url,
            encoder="vaapi" if self.vaapi_available else "v4l2" if self.v4l2_available else "software",
            quality=quality
        )
        
        print(f"🚀 Starting stream with: {' '.join(cmd[:3])}...")
        
        self.current_encoder = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        return self.current_encoder
    
    def stop_stream(self):
        """Stop current streaming session"""
        if self.current_encoder:
            self.current_encoder.terminate()
            self.current_encoder = None
            print("🛑 Stream stopped")

# CLI utility
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Hardware-Accelerated Demo Streaming")
    parser.add_argument('--test', action='store_true', help='Test hardware availability')
    parser.add_argument('--platform', '-p', help='Target platform')
    parser.add_argument('--output', '-o', default='rtmp://localhost/live/showet', help='Output URL')
    parser.add_argument('--quality', '-q', default='medium', choices=['low', 'medium', 'high', 'ultra'])
    
    args = parser.parse_args()
    
    bridge = HardwareEncoderBridge()
    
    if args.test:
        print(f"VAAPI available: {'✅ Yes' if bridge.vaapi_available else '❌ No'}")
        print(f"V4L2 available: {'✅ Yes' if bridge.v4l2_available else '❌ No'}")
    else:
        asyncio.run(bridge.start_stream(args.platform or "demo", output_url=args.output, quality=args.quality))