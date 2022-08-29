#!/bin/bash
# Showet install helper script
# author: Bauke Molenaar.

cd ~
inst_emulators(){
    echo "Installing retroarch Reposetories."
    sudo add-apt-repository ppa:libretro/stable
    sudo add-apt-repository ppa:libretro/extra
    sudo add-apt-repository ppa:libretro/testing
    sudo apt update
    sudo apt install retroarch* libretro*
}
inst_deps(){
    echo "Installing dependencies..."
    deps=( \
        "python3" \
        "python3-urllib3" \
        "unzip" \
        "fs-uae" \
        "lhasa" \
        "vice" \
        "qml-module-qtquick-controls" \
        "qml-module-qtgraphicaleffects" \
        "qml-module-qtquick-layouts" \
        "qml-module-qtwebengine" \
        "debhelper" \
        "qt5-qmake" \
        "qtbase5-dev" \
        "qtdeclarative5-dev" \
        "python3" \
        "python3-urllib3" \
        "unrar" \
        "p7zip-full" \
        "p7zip-rar" \
        "gzip" \
        "unzip" \
        "wine" \
    )
    for dep in "${deps[@]}"
    do
        if ! dpkg -s $dep >/dev/null 2>&1; then
            echo "Installing $dep"
            sudo apt install $dep
        fi
    done
}
inst_showet(){
    sudo apt update
    sudo apt upgrade
    if [ -d ~/showet ]; then
        echo "Old Showet installation Found. moving it to ~/showet.old"
        mv ~/showet ~/showet.old
    fi
    if [ ! -d ~/showet ]; then
        echo "Installing Showet..."
        git clone https://github.com/itsdarklikehell/showet
        cd showet
        debuild -us -uc -b
        make
        sudo make install
    fi
}
updt_showet(){
    if [ ! -d ~/showet ]; then
        echo "Directory ~/Showet was not found, please install it first"
    else
        echo "Updating..."
        sudo apt update
        sudo apt upgrade
        cd ~/showet
        git pull
        debuild -us -uc -b
        make
        sudo make install
    fi
}
if [[ $1 = "--update" ]]; then
    updt_showet
    inst_emulators
fi
if [[ $1 = "--install-emulators" ]]; then
    inst_emulators
fi
if [[ $1 = "--install-showet" ]]; then
    inst_deps
    inst_showet
    inst_emulators
fi
if [[ $# -eq 0 ]] ; then
    echo "Usage:    ./install.sh [OPTION]"
    echo "Options:"
    echo "          --install-showet"
    echo "          --install-emulators"
    echo "          --update"
    exit 0
fi
echo "Done!"