#!/bin/bash

set -e -u

install_texlive()
{
    rm -rf $CACHEDIR
    mkdir -p $CACHEDIR
    cd /tmp
    # Obtain TeX Live
    wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
    tar -xzf install-tl-unx.tar.gz
    cd install-tl-*
    sed -i "s:MYPREFIX:$CACHEDIR:g" $TRAVIS_BUILD_DIR/texlive.profile

    # Install a minimal system
    ./install-tl -profile $TRAVIS_BUILD_DIR/texlive.profile
    cd
}

# See if there is a cached version of TL available
export PATH=$CACHEDIR/.texlive/bin/x86_64-linux:$PATH

install_texlive
