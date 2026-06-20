#!/bin/bash
# showet-demo-run.sh - Run Amiga demos with FS-UAE

DEMO_FILE="$1"
if [ -z "$DEMO_FILE" ]; then
    echo "Usage: ./showet-demo-run.sh <demo.adf>"
    echo "Available demos:"
    ls -la ~/.showet/data/*/Drifters-*.adf 2>/dev/null || echo "No demos found"
    exit 1
fi

# Create temp config
cat > /tmp/showet_fsuae.conf << EOF
[config]
amiga_model = A500

[floppy_drive_0]
floppy_image = $DEMO_FILE

[video]
fullscreen = false
width = 720
height = 568
EOF

echo "Launching FS-UAE with: $DEMO_FILE"
fs-uae /tmp/showet_fsuae.conf