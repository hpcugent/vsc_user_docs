#!/bin/bash

result=$(find . -type f -name "*.tex" | xargs -n1 ./find_white_in_terminal.py)

if [[ $result ]]; then
    echo "Found latex command in prompt environment, please close them with {}"
    echo "$result"
    exit 1
fi

echo "No style violations found"
exit 0
