#!/usr/bin/env bash

printf "\n  ____________   _____  \n /  ___/\\____ \\ /     \\ \n \\___ \\ |  |_> >  Y Y  \\ \n/____  >|   __/|__|_|  /\n     \\/ |__|         \\/ "
echo "Getting ready to install"
sleep 1

if ! [[ $EUID = 0 && "$(ps -o comm= | sed -n '1p')" = "su" ]]; then
    echo "To install this you must use sudo- but not in the shell as root."
fi

# ---------------------------------------------------------------------------- #
#                                   Functions                                  #
# ---------------------------------------------------------------------------- #

# ------------------------ Shell spinner - UI element ------------------------ #
sp="/-\|"
sc=0
spin() {
    printf "\b${sp:sc++:1}"
    ((sc==${#sp})) && sc=0
}
endspin() {
    printf "\r%s\n" "$@"
}

# ------------------------------ Install via apt ----------------------------- #
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

# ---------------------------------------------------------------------------- #
#                                  Pre-install                                 #
# ---------------------------------------------------------------------------- #

# ------------------------- Install required packages ------------------------ #
REQUIRED_PKG="git" && installpackage
REQUIRED_PKG="python3" && installpackage
REQUIRED_PKG="python3-pip" && installpackage
REQUIRED_PKG="unzip" && installpackage

# -------------------------------- Clone repo -------------------------------- #
echo "Finished installing dependencies"
echo "Preparing ~/.spm"
mkdir ~/.spm
mkdir ~/.spm/install

echo "Cloning repository..."
spin
if ! git clone https://github.com/dudeisbrendan03/SPM-CLI ~/.spm/install > /dev/null; then
    echo "Error occured while cloning the repository"
    exit 1
fi

endspin
echo "Cloned."
sleep 1
clear

echo "Installing SPM..."

echo "Changing directory to ~/.spm"
cd ~/.spm

echo "Checking in correct directory"
if ! [[ $(pwd) = */home/$(whoami)/.spm* ]]; then
    echo "You're working in $(pwd) but we expected $(echo /home/$(whoami)/.spm)"
    exit 1
fi
clear

echo "git release- not compiled executable"
echo "Copying over spm.py to /usr/local/bin"
sudo cp ~/.spm/install/spm.py /usr/local/bin/spm
echo "Copying libs over to /usr/local/bin"
sudo cp -r ~/.spm/install/lib /usr/local/bin/lib
echo "Copying defaults over to ~/.spm/defaults"
cp -r ~/.spm/install/defaults ~/.spm
echo "Deleting install cache"
rm -rf ~/.spm/install
echo "Setting spm as executable"
sudo chmod +x /usr/local/bin/spm
echo "Install completed, type 'spm' to see usage."
