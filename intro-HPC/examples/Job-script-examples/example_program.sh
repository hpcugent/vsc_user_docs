#!/bin/bash
# This is an example program
# It takes two arguments: a number of times to loop and a file to write to
# In total, it will run for (the number of times to loop) minutes

if [ $# -ne 2 ]; then
    echo "Usage: ./example_program amount filename" && exit 1
fi

for ((i = 0; i < $1; i++ )); do
    echo "${i} => $(date)" >> $2
    sleep 60
done
