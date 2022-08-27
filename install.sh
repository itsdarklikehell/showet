#!/bin/bash

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
    deps=( "debhelper" "qt5-qmake" "qtbase5-dev" "qtdeclarative5-dev" "python3" "python3-urllib3" "unzip" "wine" "fs-uae" "lhasa" "vice" "qml-module-qtquick-controls" "qml-module-qtgraphicaleffects" "qml-module-qtquick-layouts" "qml-module-qtwebengine" )
    for dep in "${deps[@]}"
    do
        if ! dpkg -s $dep >/dev/null 2>&1; then
            echo "Installing $dep"
            sudo apt install $dep
        fi
    done
}
inst_showet(){
    debuild -us -uc -b
    make
    sudo make install
}
inst_emulators
inst_deps
inst_showet
echo "Done!"