#!/bin/bash

# Check if the input Directory exists
if [ ! -d "./input" ] ; then
  mkdir ./input
fi

# Just generate all dummy input files
for i in {1..100}; 
do
  echo "This is input file #$i" >  ./input/input_$i.dat 
  echo "Parameter #1 = $i" >>  ./input/input_$i.dat 
  echo "Parameter #2 = 25.67" >>  ./input/input_$i.dat
  echo "Parameter #3 = Batch" >>  ./input/input_$i.dat
  echo "Parameter #4 = 0x562867" >>  ./input/input_$i.dat
done
