# RetroPie/Batocera Integration

This guide explains how to integrate showet into RetroPie or Batocera for demo scene playback on Raspberry Pi.

## Quick Install (RetroPie)

```bash
# Download and run the integration script
wget https://raw.githubusercontent.com/itsdarklikehell/showet/main/scripts/retropie-install.sh
chmod +x retropie-install.sh
./retropie-install.sh
```

## Manual Installation

### 1. Install Dependencies (RetroPie)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3-pip python3-urllib3 ffmpeg

# Install RetroArch cores (if not already installed)
# RetroPie typically includes these
sudo apt install -y lr-vice lr-puae lr-quicknes lr-snes9x lr-genesis-plus-gx lr-fuse
```

### 2. Install Showet
```bash
git clone https://github.com/itsdarklikehell/showet.git
cd showet
pip3 install --user -e .

# Set up thumbnail cache directory
mkdir -p ~/.showet/thumbnails
mkdir -p ~/.showet/cache
```

### 3. Add to RetroPie Menu
Create a script at `~/RetroPie/retropiemenu/showet.sh`:
```bash
#!/bin/bash
cd ~/showet
python3 -m showet_webui --port 8765 &
sleep 2
kweb http://localhost:8765  # or chromium-browser
```

Make it executable:
```bash
chmod +x ~/RetroPie/retropiemenu/showet.sh
```

### 4. Controller Configuration
Add to RetroArch input config for demo controller:
```
input_exit_emulator = "escape"
input_menu_toggle = "f1"
input_screenshot = "f2"  # Takes demo screenshot
```

## Steam Deck Integration

### Prerequisites
- Steam Deck in Desktop mode
- Konsole terminal access

### Setup
```bash
# Install via Discover or apt
sudo apt install python3-pip ffmpeg

# Clone and install
git clone https://github.com/itsdarklikehell/showet.git
cd showet
pip3 install -e .

# Create Steam shortcut
cat > ~/.local/share/applications/showet.desktop << EOF
[Desktop Entry]
Name=Showet Demo Runner
Exec=showet-executor
Icon=applications-games
Type=Application
Categories=Game;
EOF
```

### Steam Deck Optimizations
- Use `--retroarch-only` flag for best compatibility
- Set `SHOWET_TIMEOUT=120` for shorter demo sessions
- Use `showet-jukebox --mode sequential --timeout 60` for quick demos

## Batocera Integration

Batocera uses a different structure. Place the script in:

```bash
# For Batocera
/share_init/system/custom.sh
```

Or access via network share:
- The web UI can be accessed from any device on the network
- SSH into Batocera and run `python3 -m showet_webui`
- Access `http://<batocera-ip>:8765` from another device

### Batocera Demo Folder
```bash
# Mount ROM share
cd /userdata/roms/demos
# Create platform subdirectories
mkdir -p commodore_64 amiga nes snes dos
```

## Demo Folder Structure

Showet expects demos in `~/.showet/data/<pouet_id>/`:

```bash
# Example: Download demo for offline use
mkdir -p ~/.showet/data/12345
# Place demo files in this folder

# Generate thumbnails for web UI
showet-thumbnails --batch-ids 12345 67890
```

## Controller Support

The web UI works with:
- USB gamepads (via browser)
- Keyboard navigation
- Touch screens (on handheld setups)
- Steam Deck controller (Desktop mode)

## Performance Tips for Raspberry Pi

- Enable GPU memory split in `/boot/config.txt`: `gpu_mem=256`
- Use lightweight browsers: `sudo apt install kweb`
- Pre-extract demos: `showet-archive extract demos.zip`
- Generate thumbnails offline: `showet-thumbnails --batch-ids ...`

## Notes

- RetroPie typically runs on Raspberry Pi with limited resources
- Some demos may require more powerful hardware than Pi can provide
- The Raspberry Pi bare-metal demos are optimized for Pi
- Internet connection required for pouet.net API access
- Thumbnails in `~/.showet/thumbnails/` improve web UI loading

## Useful Commands

```bash
# List available platforms
showet --platforms

# Check system status on Pi
showet-status

# Generate playlist for offline viewing
showet-jukebox --generate-playlist --ids 12345 67890

# Stream from Pi to another device
showet-stream --rtsp --demo 12345
```