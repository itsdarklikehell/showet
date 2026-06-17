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
sudo apt install -y python3-pip python3-urllib3

# Install RetroArch cores (if not already installed)
# RetroPie typically includes these
```

### 2. Install Showet
```bash
git clone https://github.com/itsdarklikehell/showet.git
cd showet
pip3 install --user -e .
```

### 3. Add to RetroPie Menu
Create a script at `~/RetroPie/retropiemenu/showet.sh`:
```bash
#!/bin/bash
cd ~/showet
python3 -m showet_webui &
sleep 2
kweb http://localhost:8765  # or chromium-browser
```

Make it executable:
```bash
chmod +x ~/RetroPie/retropiemenu/showet.sh
```

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

## Demo Folder Structure

Showet expects demos in `~/.showet/data/<pouet_id>/`:

```bash
# Example: Download demo for offline use
mkdir -p ~/.showet/data/12345
# Place demo files in this folder
```

## Controller Support

The web UI works with:
- USB gamepads (via browser)
- Keyboard navigation
- Touch screens (on handheld setups)

## Notes

- RetroPie typically runs on Raspberry Pi with limited resources
- Some demos may require more powerful hardware than Pi can provide
- The Raspberry Pi bare-metal demos (`Platform_Raspberry_Pi`) are optimized for Pi
- Internet connection required for pouet.net API access