#!/bin/bash

set -e -u

function set_timestamp() {
    directory=$1;
    last_modified=$(git log -n 1 --pretty='format:%cd' --date=format:'%B %e %Y' "$1")
    echo "$1 ${last_modified}"
    sed --in-place "s/DATEPLACEHOLDER/${last_modified}/g" "$1/title.tex"
}

set_timestamp perfexpert
set_timestamp intro-Linux
set_timestamp intro-HPC
