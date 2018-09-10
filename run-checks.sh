#!/bin/bash

ec=0

result=$(find . -type f -name "*.tex" | xargs -n1 ./find_white_in_terminal.py)
if [[ $result ]]; then
    echo "Found one or more LaTeX commands in prompt environment, please close them with {}"
    echo "$result"
    ec=1
fi

# Style guide can use \verb to say it's not okay to use \verb
result=$(grep -R --include=\*.tex '\\verb[^\w]' | grep -v style-guide)
if [[ $result ]]; then
    echo "Found a \\verb command, please use \\lstinline instead"
    echo "$result"
    ec=1
fi

if [[ "$ec" -eq 0 ]]; then
    echo "All checks passed"
fi

exit $ec
