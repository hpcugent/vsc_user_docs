#!/bin/bash
set -x
if [ ${INSTALLDEPS:-0} -gt 0 ]; then
    python3 -m pip install --ignore-installed --prefix $PWD/pypkgs -r requirements.txt
    python3 -m pip install --prefix $PWD/pypkgs $PWD/custom_plugin
    python3 -m pip install --prefix $PWD/pypkgs $PWD/computational_macros
fi

pyver=python$(python3 -c "import sys; print(\"%s.%s\" % sys.version_info[:2])")
export PYTHONPATH=$PWD/pypkgs/lib/$pyver/site-packages:$PWD/pypkgs/lib64/$pyver/site-packages:$PWD/custom_plugin:$PWD/computational_macros:$PYTHONPATH
export PATH=$PWD/pypkgs/bin:$PATH

python3 build.py "$@"

if [ ${WEBSERVER:-0} -gt 0 ]; then
    cd build/HPC
    port=8000
    {
        sleep 1
        if command -v xdg-open >& /dev/null; then
            xdg-open http://localhost:$port
            echo "Tab opened for http://localhost:$port"
        else
            echo "Go to http://localhost:$port"
        fi
    } &
    python -m http.server --cgi 8000
fi
