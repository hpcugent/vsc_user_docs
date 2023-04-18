#!/bin/bash

DEPSDIR="$PWD/pypkgs"
if [ "${INSTALLDEPS:-0}" -gt 0 ]; then
    python3 -m pip install --ignore-installed --prefix "$DEPSDIR" -r requirements.txt
    python3 -m pip install --prefix "$DEPSDIR" "$PWD"/custom_plugin
    python3 -m pip install --prefix "$DEPSDIR" "$PWD"/computational_macros
fi

pyver=python$(python3 -c "import sys; print(\"%s.%s\" % sys.version_info[:2])")
export PYTHONPATH=$DEPSDIR/lib/$pyver/site-packages:$DEPSDIR/lib64/$pyver/site-packages:$PWD/custom_plugin:$PWD/computational_macros:$PYTHONPATH
export PATH=$DEPSDIR/bin:$PATH

python3 build.py "$@"

if [ "${WEBSERVER:-0}" -gt 0 ]; then
    webbase=build
    if cd "$webbase"; then
        port=8000
        {
            sleep 1
            if command -v xdg-open >& /dev/null; then
                xdg-open http://localhost:$port
                echo "Tab opened for http://localhost:$port"
            else
                echo "Go to http://localhost:$port"
            fi
            echo "To have working legacy pdf links, also do a 'cp -a pdf build'"
        } &
        python -m http.server --cgi 8000
    else
        echo "Can't change dir to $webbase. Build failed?"
    fi
fi
