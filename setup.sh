#!/bin/bash

# (Un)Install pimme from user's home directory.

set -e

function install_pimme {
    # copy files to ~/lib/python/
    mkdir -p ~/lib/python/pimme
    cp *py ~/lib/python/pimme/
    cp setup.sh ~/lib/python/pimme/

    # make soft link to ~/bin/
    mkdir -p ~/bin
    ln -s ~/lib/python/pimme/pimme.py ~/bin/pimme
    chmod u+x ~/bin/pimme

    # create default config file
    PATH=$PATH:~/bin pimme -w

    # print additional configuration needed
    echo "Please add ~/bin to your PATH."
}

function uninstall_pimme {
    # remove all files
    rm -f ~/bin/pimme
    rm -rf ~/lib/python/pimme
    rm -f ~/.pimme.conf
}

nargs=1
trap uninstall INT KILL TERM

if [ $nargs -ne $# ]; then
    echo 'Use install(uninstall) to install(uninstall).'
    exit -1
fi

if [ $1 = 'install' ]; then
    install_pimme
else
    if [ $1 = 'uninstall' ]; then
	uninstall_pimme
    else
	echo 'Wrong argument.'
	exit -1
    fi
fi
exit 0
