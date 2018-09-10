#!/bin/bash

result=$(find . -type f -name "*.tex" | xargs -n1 ./find_white_in_terminal.py)

ec=0

if [[ $result ]]; then
    echo "Found one or more LaTeX commands in prompt environment, please close them with {}"
    echo "$result"
    ec=1
fi

if [[ "$ec" -eq 0 ]]; then
    echo "All checks passed"
fi

exit $ec
