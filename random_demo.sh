#!/bin/bash
# Showet random demo picker script
# author: Bauke Molenaar.
function update(){
    cd ~/showet
    git pull
}

TIMEOUT=3 # seconds
MAX_POUETIDS=88912

# if $1 is empty, then dont loop
if [ -z $1 ]; then
    loop="false"
    random="false"
    elif [ $1 = "-p" ] && [ $2 !-z ]; then
    loop="false"
    random="false"
    pouet_id=$2
    elif [[ $1 = "-pl" ]]; then
    loop="true"
    random="false"
    pouet_id=$2
    elif [ $1 = "-r" ]; then
    random="true"
    elif [ $1 = "-rl" ]; then
    loop="true"
    random="true"
    elif [ $1 = "-h" ]; then
    echo "Usage: random_demo.sh [-p <pouet_id>] [-r] [-rl]"
    echo " -p <pouet_id> : select demo from pouet id"
    echo " -pl <pouet_id> : loop and select demo from pouet id"
    echo " -r : select random demo"
    echo " -rl : select random demo and loop"
    echo " -h : show this help"
    exit 0
else
    echo "Invalid argument"
    exit 1
fi

play_demo(){
    update
    # if random is enabled, then play a random demo
    if [ $random = "true" ]; then
        echo "Random selection...(insert drumroll...)"
        pouet_id=$(shuf -i0-$MAX_POUETIDS -n1)
        echo "I randomly selected production no: $pouet_id from the massive pouet.net database containting: $MAX_POUETIDS productions...(insert windows TADAA! sfx...)"
    fi
    python3 ~/showet/showet.py $pouet_id && chmod +x ~/.showet/data/$pouet_id/*
    resoreset
    sleep 1
    read -p "Press [q] to quit or [enter] to continue (or wait a few seconds)..." -n1 -s -t $TIMEOUT
    # if q is pressed, then quit
    if [[ $REPLY = "q" ]]; then
        echo "Quitting..."
        loop="false"
        # Cleanup after script
        rm -rf ~/.showet/data/*
        resoreset
        exit 0
    fi
}



# if loop is enabled, then loop forever
if [ $loop = "true" ]; then
    while true; do
        play_demo
    done
else
    play_demo
fi
# Cleanup after script
rm -rf ~/.showet/data/* >/dev/null 2>&1

