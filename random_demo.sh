#!/bin/bash
# Showet random demo picker script
# author: Bauke Molenaar.

# function extract () {
#     if [ -f $1 ] ; then
#         case $1 in
#             *.tar.bz2)    tar xvjf $1    ;;
#             *.tar.gz)    tar xvzf $1    ;;
#             *.tar.xz)    tar xf $1      ;;
#             *.bz2)        bunzip2 $1     ;;
#             *.rar)        unrar x $1     ;;
#             *.gz)        gunzip $1      ;;
#             *.tar)        tar xvf $1     ;;
#             *.tbz2)        tar xvjf $1    ;;
#             *.tgz)        tar xvzf $1    ;;
#             *.zip)        unzip $1       ;;
#             *.Z)        uncompress $1  ;;
#             *.7z)        7z x $1        ;;
#             *)        echo "don't know how to extract '$1'..." ;;
#         esac
#     else
#         echo "'$1' is not a valid file!"
#     fi
# }

TIMEOUT=3 # seconds
MAX_POUETIDS=88863

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
    # if random is enabled, then play a random demo
    if [ $random = "true" ]; then
        echo "Random selection...(insert drumroll...)"
        pouet_id=$(shuf -i0-$MAX_POUETIDS -n1)
        echo "I randomly selected production no: $pouet_id from the massive pouet.net database containting: $MAX_POUETIDS productions...(insert windows TADAA! sfx...)"
    fi    
    python3 ~/showet/showet.py $pouet_id
    read -p "Press [q] to quit or [enter] to continue (or wait a few seconds)..." -n1 -s -t $TIMEOUT
    # if q is pressed, then quit
    if [[ $REPLY = "q" ]]; then
        echo "Quitting..."
        loop="false"
        # Cleanup after script
        rm -rf ~/.showet/data/* >/dev/null 2>&1
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

