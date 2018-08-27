#!/usr/bin/env sh

install_texlive()
{
    cd /tmp
    # Obtain TeX Live
    wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
    tar -xzf install-tl-unx.tar.gz
    cd install-tl-*
    sed -i "s:MYPREFIX:$HOME:g" $TRAVIS_BUILD_DIR/texlive.profile

    # Install a minimal system
    ./install-tl -profile $TRAVIS_BUILD_DIR/texlive.profile
    cd
}

# See if there is a cached version of TL available
export PATH=/tmp/texlive/bin/x86_64-linux:$PATH
if ! command -v pdflatex > /dev/null; then
    echo "First install"
    install_texlive
else
    if ! (( $RANDOM % 100 )); then
        echo "Throwing away cache and updating..."
        rm -rf $HOME/.texlive
        rm -rf $HOME/texmf
        install_texlive
    fi
fi
