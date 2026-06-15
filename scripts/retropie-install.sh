#!/bin/bash
# Showet RetroPie Integration Script
# Installs showet into RetroPie's menu system for easy demo launching

set -e

# Configuration
SHOWET_REPO="https://github.com/itsdarklikehell/showet.git"
SHOWET_DIR="$HOME/showet"
RETROPIE_MENU_DIR="$HOME/RetroPie/retropiemenu"

log() {
    echo "[showet-retropie] $1"
}

check_retropie() {
    if [[ ! -d "$RETROPIE_MENU_DIR" ]]; then
        log "RetroPie menu directory not found at $RETROPIE_MENU_DIR"
        log "This script should be run on a RetroPie system"
        return 1
    fi
}

install_showet() {
    if [[ -d "$SHOWET_DIR" ]]; then
        log "Showet already installed, updating..."
        cd "$SHOWET_DIR"
        git pull
    else
        log "Cloning showet repository..."
        git clone "$SHOWET_REPO" "$SHOWET_DIR"
    fi
    
    cd "$SHOWET_DIR"
    log "Installing showet Python package..."
    pip3 install --user -e .
}

create_menu_entry() {
    local menu_entry="$RETROPIE_MENU_DIR/showet.sh"
    
    log "Creating RetroPie menu entry at $menu_entry"
    cat > "$menu_entry" << 'EOF'
#!/bin/bash
# Showet Demo Viewer - Launch from RetroPie menu
echo "Starting Showet Demo Viewer..."
cd ~/showet || exit 1

# Start the web UI
python3 -m showet_webui &

# Wait a moment for server to start
sleep 2

# Launch in browser (RetroPie has kweb or chromium-browser)
if command -v kweb &> /dev/null; then
    kweb http://localhost:8765
elif command -v chromium-browser &> /dev/null; then
    chromium-browser --kiosk http://localhost:8765
else
    echo "No browser found. Access http://localhost:8765 manually"
fi
EOF
    
    chmod +x "$menu_entry"
    
    # Create menu metadata
    cat > "$RETROPIE_MENU_DIR/showet.png" 2>/dev/null || true
}

create_system_entry() {
    # Create as a "system" in EmulationStation
    local es_systems="$HOME/.emulationstation/es_systems.cfg"
    
    if [[ -f "$es_systems" ]]; then
        # Check if showet system already exists
        if ! grep -q "showet" "$es_systems"; then
            log "Adding showet system to EmulationStation..."
            # Append showet system (would need proper XML formatting)
            log "Note: Manual system entry may be required for EmulationStation"
        fi
    fi
}

# Main execution
main() {
    check_retropie || exit 1
    
    install_showet
    create_menu_entry
    
    log "Installation complete!"
    log "You can now find 'Showet Demo Viewer' in the RetroPie menu"
    log "Make sure to configure your demo folder in ~/.showet"
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi