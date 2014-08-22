#!/bin/bash

# Check if the input Directory exists
if [ ! -d "./output" ] ; then
  echo "The output directory does not exist!"
  exit
fi

# Just concatenate all output files
touch all_output.txt
for i in {1..100}; 
do
  cat ./output/output_$i.dat >> all_output.txt
done
