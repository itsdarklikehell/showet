#!/bin/bash
# Showet multi-disk demo runner

DEMO_NAME="Black'n White Slide 2"

# Run from extracted directory
echo "=== Running $DEMO_NAME (extracted disks) ==="
fs-uae /home/rizzo/FS-UAE/showet_demo.conf

# Or for zipfile (uncomment to try):
# unzip -o /home/rizzo/FS-UAE/BlackWhite2.zip -d /tmp/demo_disks
# fs-uae --floppy-directory=/tmp/demo_disks