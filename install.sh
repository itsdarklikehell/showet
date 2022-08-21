#!/bin/bash
echo "Installing dependencies..."
deps=( "debhelper" "qt5-qmake" "qtbase5-dev" "qtdeclarative5-dev" "python3" "python3-urllib3" "unzip" "wine" "fs-uae" "lhasa" "vice" "qml-module-qtquick-controls" "qml-module-qtgraphicaleffects" "qml-module-qtquick-layouts" "qml-module-qtwebengine" )
for dep in "${deps[@]}"
do
    if ! dpkg -s $dep >/dev/null 2>&1; then
        echo "Installing $dep"
        sudo apt install $dep
    fi
done
debuild -us -uc -b
make
sudo make install
echo "Done!"