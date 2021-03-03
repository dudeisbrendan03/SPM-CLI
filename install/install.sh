#!/bin/bash

printf "\n  ____________   _____  \n /  ___/\\____ \\ /     \\ \n \\___ \\ |  |_> >  Y Y  \\ \n/____  >|   __/|__|_|  /\n     \\/ |__|         \\/ "
echo "Getting ready to install"

sp="/-\|"
sc=0
spin() {
    printf "\b${sp:sc++:1}"
    ((sc==${#sp})) && sc=0
}
endspin() {
    printf "\r%s\n" "$@"
}

installpackage () {
    clear
    PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
    echo Checking for $REQUIRED_PKG: $PKG_OK
    if [ "" = "$PKG_OK" ]; then
        echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
        spin
        sudo apt-get --yes install $REQUIRED_PKG
        endspin
    fi
    
}

REQUIRED_PKG="git" && installpackage
REQUIRED_PKG="python3" && installpackage
REQUIRED_PKG="pip" && installpackage
REQUIRED_PKG="zip" && installpackage

echo "Finished installing dependencies"
echo "Cloning repository..."
spin
git clone https://github.com/dudeisbrendan03/SPM-CLI
endspin
echo "Cloned."
sleep 1
clear

echo "Installing SPM..."
spin
mkdir ~/.spm

echo "Download default configurations"
curl -s https://github.com/dudeisbrendan03/SPM-CLI/releases/someversion/config.zip > /dev/null

exit_status = $?
if [ $exit_status != 0 ]
    then
        echo "Error occured while downloading default configurations"
        exit $exit_status
fi
