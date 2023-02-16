#!/bin/bash

RETROPIE_DIR="/opt/retropie"
RETROPIE_EMU_DIR="$RETROPIE_DIR/emulators"
RETROARCH_EXEC="$RETROPIE_EMU_DIR/retroarch/bin/retroarch"
RETROARCH_CORES_DIRS="$RETROPIE_DIR/libretrocores/"
USED_SYSTEMS=(
    "3do"
    "4do"
)

if $USED_SYSTEMS[0]; then
    COREPATH=$RETROARCH_CORES_DIRS/4do_libretro

fi
if $USED_SYSTEMS[1]; then

fi

USED_CORES=(
    "atari800_libretro"
    ""
)

echo "Checking for available retroarch executable"
if [ -f "$RETROARCH_EXEC" ]; then
    echo "Found: $RETROARCH_EXEC"
    ls $RETROARCH_EXEC
else
    echo "$RETROARCH_EXEC NOT FOUND!"
    exit 1
fi

echo "Checking for available retroarch cores"
if [ -d "$RETROARCH_CORES_DIRS" ]; then
    echo "Found: $RETROARCH_CORES_DIRS"
    ls - $RETROARCH_CORES_DIRS
else
    echo "$RETROARCH_CORES_DIRS NOT FOUND!"
    exit 1
fi
