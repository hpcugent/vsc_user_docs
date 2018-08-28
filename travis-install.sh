#!/bin/bash

set -e -u

travis_retry() {
  local result=0
  local count=1
  while [ $count -le 3 ]; do
    [ $result -ne 0 ] && {
      echo -e "\n${ANSI_RED}The command \"$@\" failed. Retrying, $count of 3.${ANSI_RESET}\n" >&2
    }
    "$@"
    result=$?
    [ $result -eq 0 ] && break
    count=$(($count + 1))
    sleep 1
  done

  [ $count -gt 3 ] && {
    echo -e "\n${ANSI_RED}The command \"$@\" failed 3 times.${ANSI_RESET}\n" >&2
  }

  return $result
}

install_texlive()
{
    cd /tmp
    # Obtain TeX Live
    travis_retry wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
    tar -xzf install-tl-unx.tar.gz
    cd install-tl-*
    sed -i "s:MYPREFIX:$CACHEDIR:g" $TRAVIS_BUILD_DIR/texlive.profile

    # Install a minimal system
    ./install-tl -profile $TRAVIS_BUILD_DIR/texlive.profile
    cd
}

# See if there is a cached version of TL available
export PATH=$CACHEDIR/.texlive/bin/x86_64-linux:$PATH
if ! command -v pdflatex > /dev/null; then
    echo "First install"
    install_texlive
else
    # Force a cache update once every 100 builds (on average)
    if ! (( $RANDOM % 100 )); then
        echo "Throwing away cache and updating..."
        rm -rf $CACHEDIR
        install_texlive
    fi
fi
