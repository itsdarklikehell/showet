# Streaming Guide

Showet supports live streaming demos to Twitch, YouTube Live, Facebook Live, and RTSP endpoints.

## Quick Start

```bash
# Install ffmpeg (required for streaming)
# Ubuntu/Debian:
sudo apt install ffmpeg

# Save your stream key
showet-stream --save-key twitch --key YOUR_STREAM_KEY

# Stream a demo
showet-stream --platform twitch --demo 12345
```

## Platforms

| Platform | Ingest URL Format | Stream Key Location |
|----------|-------------------|---------------------|
| Twitch | `rtmp://live.twitch.tv/app/{key}` | Dashboard → Creator Tools → Stream Key |
| YouTube | `rtmp://a.rtmp.youtube.com/live2/{key}` | YouTube Studio → Go Live → Stream Settings |
| Facebook | `rtmp://live-upload.facebook.com:443/rtmp/{key}` | Creator Studio → Live Producer |
| Custom | Any RTMP endpoint | Use `--platform custom` |

## CLI Options

```
--platform         twitch, youtube, facebook, custom, or rtsp
--stream-key       RTMP stream key (or set SHOWET_STREAM_KEY)
--demo             Pouet.net demo ID to stream
--quality          480p, 720p, 1080p, 1440p, 4k (default: 720p)
--overlay          Custom text overlay on stream
--webcam           Include webcam picture-in-picture
--no-audio         Disable audio capture
--record           Record stream locally while broadcasting
--record-path      Path for local recording (default: ~/.showet/recordings/)
--fullscreen       Stream in fullscreen mode
--rtsp             Use RTSP server instead of RTMP
--rtsp-port        RTSP port (default: 8554)
--save-key         Save stream key to ~/.showet/{platform}_stream_key
--key              Stream key (used with --save-key)
```

## Examples

### Basic Twitch Stream
```bash
showet-stream --platform twitch --demo 12345
```

### YouTube Live with Custom Quality
```bash
showet-stream --platform youtube --quality 1080p --demo 12345
```

### Local RTSP Stream (for OBS capture)
```bash
showet-stream --rtsp
# Then add in OBS: Media Source → rtsp://localhost:8554/showet
```

### Stream with Webcam Overlay
```bash
showet-stream --platform twitch --webcam --demo 12345
# Webcam appears in top-right corner by default
```

### Record While Streaming
```bash
showet-stream --platform twitch --record --demo 12345
```

### Multiple Stream Keys
Save different keys for different platforms:
```bash
showet-stream --save-key twitch --key TWITCH_KEY
showet-stream --save-key youtube --key YOUTUBE_KEY
showet-stream --save-key facebook --key FACEBOOK_KEY
```

## Advanced Configuration

### Hardware Encoding (NVIDIA)
For better performance with NVIDIA GPUs, add to config:
```python
StreamConfig(
    ...
    extra_ffmpeg_args=[
        "-c:v", "h264_nvenc",
        "-preset", "p5",
        "-cq", "28",
    ]
)
```

### Audio Source Selection
Modify the pulse audio source in streaming.py:
```python
# Find available sources: pactl list sources short
"-f", "pulse",
"-i", "alsa_output.pci-0000_00_1b.0.analog-stereo",
```

## Troubleshooting

### "FFmpeg not found"
Install ffmpeg:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# macOS
brew install ffmpeg
```

### "No window to capture"
Ensure X11 is running or modify the input source in streaming.py for Wayland:
```python
# For Wayland, use:
"-f", "gdigrab",  # Windows
# or
"-f", "xcbgrab",  # XCB (newer X11)
```

### Stream Won't Connect
- Verify stream key is correct
- Check firewall allows outbound RTMP (port 1935)
- Confirm platform status (stream may be in retry mode)

### High CPU Usage
- Lower quality: `--quality 480p`
- Use hardware encoder (NVENC/VAAPI)
- Add sleep between frames in demo loop

## Streaming Architecture

```
+------------------+     +-------------------+     +------------------+
|   Demo Runner    | --> |   StreamManager   | --> |  RTMP/RTSP Out   |
|  (showet.py)    |     | (streaming.py)    |     |  (Twitch/YouTube)|
+------------------+     +-------------------+     +------------------+
                              |
                              v
                       +--------------+
                       |  Recording   |
                       |  (optional)  |
                       +--------------+
```

## Notes

- Stream keys are stored with restrictive permissions (0600)
- RTSP mode creates a standalone stream server
- Webcam requires `/dev/video0` or custom device path
- Overlay text shows demo name automatically when available