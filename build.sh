#!/bin/bash
# python3 -m pip install --ignore-installed --prefix $PWD/pypkgs -r requirements.txt
# python3 -m pip install --prefix $PWD/pypkgs $PWD/custom_plugin
# python3 -m pip install --prefix $PWD/pypkgs $PWD/computational_macros
PYTHONPATH=$PWD/pypkgs/lib/python3.9/site-packages:$PWD/custom_plugin:$PWD/computational_macros:$PYTHONPATH python3 build.py
