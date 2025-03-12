#!/bin/bash

if [ "${DEBUG:-0}" -gt 0 ]; then
    set -x
fi

DEPSDIR="$PWD/pypkgs"
pyver=python$(python3.12 -c "import sys; print(\"%s.%s\" % sys.version_info[:2])")
export PYTHONPATH=$DEPSDIR/lib/$pyver/site-packages:$DEPSDIR/lib64/$pyver/site-packages:$PWD/custom_plugin:$PWD/computational_macros:$PYTHONPATH
export PATH=$DEPSDIR/bin:$PATH


if [ "${INSTALLDEPS:-0}" -gt 0 ]; then
    python3.12 -m pip install --use-pep517 --ignore-installed --prefix "$DEPSDIR" -r requirements.txt
    python3.12 -m pip install --use-pep517 --prefix "$DEPSDIR" "$PWD"/custom_plugin
    python3.12 -m pip install --use-pep517 --prefix "$DEPSDIR" "$PWD"/computational_macros
    # not needed for actual page
    python3.12 -m pip install --use-pep517 --ignore-installed --prefix "$DEPSDIR" linkchecker
fi

python3.12 build.py "$@"

if [ "${WEBSERVER:-0}" -gt 0 ]; then
    webbase=build
    if cd "$webbase"; then
        port=8000
        url=http://localhost:$port
        {
            sleep 1
            if command -v xdg-open >& /dev/null; then
                xdg-open $url
                echo "Tab opened for $url"
            else
                echo "Go to $url"
            fi

            # run tests
            linkchecker $url
        } &
        python -m http.server --cgi 8000
    else
        echo "Can't change dir to $webbase. Build failed?"
    fi
fi
