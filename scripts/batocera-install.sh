#!/bin/bash
# Batocera Integration Script for Showet
# Batocera stores scripts in /userdata/system/ or provides network access

set -e

# Configuration  
SHOWET_REPO="https://github.com/itsdarklikehell/showet.git"

log() {
    echo "[showet-batocera] $1"
}

install_showet_batocera() {
    # Batocera typically has /storage or /userdata for persistent storage
    local showet_dir="${HOME}/showet"
    local share_dir="/userdata/system"
    
    log "Installing showet for Batocera..."
    
    # Check if we're on Batocera
    if [[ ! -d "/userdata" ]]; then
        log "Warning: Not running on Batocera. Adjust paths accordingly."
    fi
    
    # Create installation directory
    mkdir -p "$showet_dir"
    
    if [[ -d "$showet_dir/.git" ]]; then
        cd "$showet_dir"
        git pull
    else
        git clone "$SHOWET_REPO" "$showet_dir"
    fi
    
    cd "$showet_dir"
    
    # Install Python dependencies
    pip3 install --user -e . 2>/dev/null || pip install --user -e .
    
    log "Showet installed to $showet_dir"
    log "Run with: python3 -m showet_webui"
    log "Access via: http://$(hostname -I | awk '{print $1}'):8765"
}

# Run if executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    install_showet_batocera "$@"
fi