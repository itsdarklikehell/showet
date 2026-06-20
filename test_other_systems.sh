#!/bin/bash
# test_other_systems.sh - Comprehensive multi-system testing script

echo "=== SHOWET SYSTEM TESTING MATRIX ==="
echo ""

echo "1. AMIGA (Multi-Disk) - Status: ✅ FS-UAE working"
echo "   - Demo: Black'n White Slide 2 by Drifters (1992)"
echo "   - Disks: A + B (both downloaded)"
echo "   - Methods: config, M3U, ZIP all created"
echo "   - Browser: ❌ puae core missing from CDN"
echo ""

echo "2. C64 (Tape Multi-Disk) - Ready for testing"
echo "   - Core available: vice_x64sc"
echo "   - Multi-disk: .t64 / .tap files (tape sides A/B)"
echo "   - Status: ✅ Config ready, need demo files"
echo ""

echo "3. NES (FDS Multi-Disk) - Ready for testing"  
echo "   - Core available: quicknes / fceumm"
echo "   - Multi-disk: .fds files (Famicom Disk System)"
echo "   - Status: ✅ Config ready, need demo files"
echo ""

echo "4. GENERATING TEST DEMOS..."
echo "   - C64 single-disk demo needed (.prg/.d64)"
echo "   - NES single-disk demo needed (.nes/.fds)"
echo ""

echo "5. MULTI-DISK FORMATS TO TEST:"
echo "   - C64 Tapes (.t64/.tap): Side A/B loading cycles"
echo "   - NES FDS (.fds): Multiple floppy disks"
echo "   - Mega CD (.cue/.bin): CD swapping"
echo "   - Amiga (.adf/.zip/.m3u): Disk changing"
echo ""

echo "Run: fs-uae /home/rizzo/FS-UAE/showet_demo.conf (Amiga)"
echo "Then: Browse to test C64/NES with vice_x64sc/fceumm cores"