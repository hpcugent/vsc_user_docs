#!/bin/bash

set -e -u

ec=0

# Don't exit if grep doesn't find anything (exit code is 1)
result=$(grep -B 20 'Latexmk: All targets (.*) are up-to-date' $LOGFILE | grep undefined) || true
if [[ "$result" ]]; then
    echo "One or more references were undefined"
    echo "$result"
    ec=1
fi

if [[ "$ec" -eq 0 ]]; then
    echo "All checks passed"
fi

exit $ec
